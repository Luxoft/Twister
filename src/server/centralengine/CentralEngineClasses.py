
'''
REQUIRES Python 2.7!
This file contains 3 classes: EpId, Test File and Central Engine.
All functions from CentralEngine are EXPOSED and can be accesed via RPC.
The CE and each EP have a status that can be: start/ stop/ paused.
Each test file has a status that can be: pending, working, pass, fail, skip, etc.
All the statuses are defined in "constants.py".
'''

import os
import sys
import re
import time
import datetime
import binascii
import smtplib
import xmlrpclib
import MySQLdb

if not sys.version.startswith('2.7'):
    print('Python version error! Central Engine must run on Python 2.7!')
    exit(1)

from collections import OrderedDict
from email.mime.text import MIMEText

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print('$TWISTER_PATH environment variable is not set! Exiting!')
    exit(1)
sys.path.append(TWISTER_PATH)

from common.constants import *
from common.tsclogging import *
from common.xmlparser import *

dictStatus = {'stopped':STATUS_STOP, 'paused':STATUS_PAUSED, 'running':STATUS_RUNNING, 'resume':STATUS_RESUME}

testStatus = {'pending':STATUS_PENDING, 'working':STATUS_WORKING, 'pass':STATUS_PASS, 'fail':STATUS_FAIL,
    'skipped':STATUS_SKIPPED, 'aborted':STATUS_ABORTED, 'not executed':STATUS_NOT_EXEC, 'timeout':STATUS_TIMEOUT,
    'invalid':STATUS_INVALID, 'waiting':STATUS_WAITING}


# --------------------------------------------------------------------------------------------------
# # # # # # # # # # # # # # # # # #
# --------------------------------------------------------------------------------------------------


class TestFile:

    def __init__(self, props):

        # File properties
        self.epid =     props.get('epid', '')
        self.suite =    props.get('suite', '')
        self.name =     props.get('file', '')
        self.runnable = props.get('runnable', '')
        self.status = STATUS_PENDING

        if (not self.name) or (not self.epid) or (not self.suite):
            logError('TestFile: Error! Created empty file, without Name, EP or Suite!')

        # Preparing the known variables for mapping in query
        del props['epid']
        del props['suite']
        del props['file']
        self.data = props

        self.data['twister_ep_name'] = self.epid
        self.data['twister_suite_name'] = self.suite
        self.data['twister_tc_name'] = self.name


    def __repr__(self):
        reversed = dict((v,k) for k,v in testStatus.iteritems())
        return '{ep}::{suite}::{file} - {status}'.format(self.epid, self.suite, self.name, reversed[self.status])


    def setStatus(self, new_status):
        # Status must be valid
        if new_status not in testStatus.values():
            logError("TF ERROR! Status value `%s` is not in the list of defined statuses: `%s`!" % \
                (str(new_status), str(testStatus.values())) )
            return False

        self.status = new_status
        reversed = dict((v,k) for k,v in testStatus.iteritems())
        self.data['twister_tc_status'] = reversed[new_status]

        return reversed[new_status]


    def saveToDatabase(self, db_config, fields, queries):
        '''
        This function will populate user query with data collected from:
        Master XML, Central Engine, or from SQL Queries.
        All queries will be executed for each filename.

        twister_ce_os              # from CE
        twister_ep_os              # from EP
        twister_ce_ip              # from CE
        twister_ep_ip              # from EP

        twister_ep_name            # from master XML
        twister_suite_name         # suite from master XML
        twister_tc_name            # test case name from master XML
        twister_tc_title           # from ...?
        twister_tc_description     # from ...?

        twister_tc_status          # from Runner
        twister_tc_crash_detected  # from EP service
        twister_tc_time_elapsed    # from Runner
        twister_tc_date_started    # calculated
        twister_tc_date_finished   # from Runner
        twister_tc_log             # parsed from logs
        '''

        conn = MySQLdb.connect(host=db_config.get('server'), db=db_config.get('database'),
            user=db_config.get('user'), passwd=db_config.get('password'))
        curs = conn.cursor()

        for query in queries:

            # All variables that must be replaced in Insert
            vars_to_replace = re.findall('(@.+?@)', query)

            for field in vars_to_replace:
                u_query = fields.get(field.replace('@', ''))

                if not u_query:
                    logError('File: {0}, cannot build query! Field {1} is not defined in the fields section!'.format(self.name, field))
                    return False

                # Execute User Query
                curs.execute(u_query)
                q_value = curs.fetchone()[0]
                # Replace @variables@ with real Database values
                query = query.replace(field, str(q_value))

            try:
                query = query.format(**self.data)
            except Exception, e:
                logError('File: {0}, cannot build query! Key error: {1}!'.format(self.name, str(e)))
                return False

            # For DEBUG ::
            open(os.getenv('HOME')+os.sep+'Query.debug', 'a').write('File Query:: `{0}` ::\n{1}\n\n\n'.format(self.name, query))

            try:
                curs.execute(query)
            except MySQLdb.Error, e:
                logError('Error in query ``{0}``'.format(query))
                logError('MySQL Error %d: %s!' % (e.args[0], e.args[1]))
                return False

        curs.close()
        conn.close()


    def saveToExcel(self):
        pass


# --------------------------------------------------------------------------------------------------
# # # # # # # # # # # # # # # # # #
# --------------------------------------------------------------------------------------------------


class EpId:

    '''
    An EP (Execution Process) is actually the representation of a machine/ station/ computer.
    When creating the list of suites, each suite must run on one EP (station).
    It's not possible to run multiple suites on the same EP, at the same time,
    but one Master XML can have more suites on the same EP, that will run sequential.
    Execution in parallel means that the tests are run in parallel on many differend EPs.
    '''

    def __init__(self, id=None):

        # EP id number
        self.id = id
        # The EP, the Suite and the File must have data
        self.data = {}
        # Dictionary of test files
        self.tfList = OrderedDict()
        self.executionStatus = STATUS_STOP


    def __repr__(self):
        reversed = dict((v,k) for k,v in dictStatus.iteritems())
        return '%s -> %s' % (str(self.id), reversed[self.executionStatus])


    def setStatus(self, new_status):
        # Status must be valid
        if new_status not in dictStatus.values():
            logError('Station %s ERROR! Cannot change status! Status value `%s` is not in the list of defined '\
                'statuses: `%s`!' % (str(self.id), str(new_status), str(dictStatus.values())) )
            return False

        reversed = dict((v,k) for k,v in dictStatus.iteritems())
        self.executionStatus = new_status
        return reversed[new_status]


    def getFileInfo(self, filename):
        '''
        Get all information available about one file.
        '''
        if filename not in self.tfList:
            logError('Station %s ERROR! Cannot get status! Filename `%s` is not in the list of defined '\
                'files: `%s`!' % (str(self.id), str(filename), str(self.tfList)) )
            return False

        return self.tfList[filename].data


    def addFileInfo(self, filename, key, value):
        '''
        Add extra information on one file.
        '''
        if filename not in self.tfList:
            logError('Station %s ERROR! Cannot get status! Filename `%s` is not in the list of defined '\
                'files: `%s`!' % (str(self.id), str(filename), str(self.tfList)) )
            return False

        self.tfList[filename].data[key] = value
        return True


    def getTfStatus(self, filename):
        '''
        Get status for one Test File. The file must exist.
        '''
        if filename not in self.tfList:
            logError('Station %s ERROR! Cannot get status! Filename `%s` is not in the list of defined '\
                'files: `%s`!' % (str(self.id), str(filename), str(self.tfList)) )
            return False

        reversed = dict((v,k) for k,v in testStatus.iteritems())
        status = self.tfList[filename].status
        return reversed[status]


    def getStatusAll(self):
        '''
        Returns status for all files that must be executed on this EP.
        Pairs like : file name => status
        '''
        statuses = OrderedDict()
        for filename in self.tfList:
            statuses[filename] = self.tfList[filename].status
        return statuses


    def setTfStatus(self, filename, new_status):
        '''
        Set status for one Test File. The file must exist.
        '''
        if filename not in self.tfList:
            logError('Station %s ERROR! Cannot change file status! Filename `%s` is not in the list of defined '\
                'files: `%s`!' % (str(self.id), str(filename), str(self.tfList.keys())) )
            return False

        status = self.tfList[filename].setStatus(new_status)
        return status


    def setTfStatusAll(self, new_status):
        '''
        Set status for all Test File.
        '''
        for filename in self.tfList:
            self.tfList[filename].setStatus(new_status)

        reversed = dict((v,k) for k,v in testStatus.iteritems())
        return reversed[new_status]


    def toDatabase(self):
        '''
        Save all files into database.
        '''
        for filename in self.tfList:
            self.tfList[filename].saveToDatabase(self.db_config, self.fields, self.queries)
        return True


# --------------------------------------------------------------------------------------------------
# # # # # # # # # # # # # # # # # #
# --------------------------------------------------------------------------------------------------


class CentralEngine:

    def __init__(self, config_path=None):

        # Before executing a test, EP / TC is checking CE status

        # String status values
        self.executionStatus = STATUS_STOP
        self.config_path = config_path
        # Central engine timers
        self.start_time = 0
        self.elapsed_time = 0
        # Build all Parsers + EP + Files structure
        logDebug('CE: Starting Central Engine...') ; ti = time.clock()
        self._initialize(reset=True)
        logDebug('CE: Initialization took %.4f seconds.' % (time.clock()-ti))


    def _initialize(self, reset=False):
        '''
        This function re-builds:
        - the framework config parser
        - the list of all files defined in Test Suite XML
        - the list of EP-IDs
        - and the list of files for each EP-ID.
        This can take a long time if there are many test files !
        '''
        if reset:
            # Framework config XML
            self.parser = TSCParser(self.config_path)

            # List with all EP-Ids
            epList = self.parser.getEpIdsList()
            if not epList:
                logCritical('CE: Cannot load the list of EPs !')
                return -1
            else:
                self.EpIds = [EpId(id) for id in epList]

        # The list with all test files defined in Test Suite XML, in order
        self.all_test_files = self.parser.getAllTestFiles()

        # Database parser, fields, queries
        self.db_path = self.parser.getDbConfigPath()
        dbparser = DBParser(self.db_path)
        db_config = dbparser.db_config
        queries = dbparser.getQueries()
        fields = dbparser.getFields()
        del dbparser

        for ep in self.EpIds:
            # Add queries for each EP
            ep.db_config = db_config # DB.XML connections
            ep.queries = queries # DB.XML insert queries
            ep.fields = fields # DB.XML field queries

            # Populate files inside each EP
            fileList = self.parser.getTestSuiteFileList(ep.id)
            ep.tfList = OrderedDict([ (filename, TestFile(self.parser.getFileInfo(ep.id, filename))) \
                for filename in fileList ])


    def echo(self, msg):
        '''
        Simple echo function, for testing connection.
        '''
        logInfo('Echo: %s' % str(msg))
        return 'CE reply: ' + msg


    def getAllVars():
        '''
        Returns available variables from CE, used in Java interface.
        This information is at test file level, NOT suite level.
        '''
        ce_vars = '''
        twister_ce_os
        twister_ep_os
        twister_ce_ip
        twister_ep_ip
        twister_ep_name
        twister_suite_name
        twister_tc_name
        twister_tc_title
        twister_tc_description
        twister_tc_status
        twister_tc_crash_detected
        twister_tc_time_elapsed
        twister_tc_date_started
        twister_tc_date_finished
        twister_tc_log
        '''
        return ce_vars


    def getConfigPath(self):
        '''
        The path to Master config file.
        '''
        return self.config_path


    def getLogsPath(self):
        '''
        The path to Logs files.
        '''
        return self.parser.getLogsPath()


    def getLogTypes(self):
        '''
        All types of logs defined in Master config file will be exposed in TCL environment.
        '''
        return self.parser.getLogTypes()


    def searchEP(self, epid):
        '''
        Search one EpId and return True or False.
        '''
        for ep in self.EpIds:
            if(ep.id==epid):
                return True
        return False


    def runDBSelect(self, field_id):
        '''
        Selects from database.
        '''
        dbparser = DBParser(self.db_path)
        query = dbparser.getQuery(field_id)
        db_config = dbparser.db_config
        del dbparser

        try:
            conn = MySQLdb.connect(host=db_config.get('server'), db=db_config.get('database'),
                user=db_config.get('user'), passwd=db_config.get('password'))
            curs = conn.cursor()
            curs.execute(query)
        except MySQLdb.Error, e:
            errMessage = 'MySQL Error %d: %s' % (e.args[0], e.args[1])
            logError(errMessage)
            return errMessage

        rows = curs.fetchall()
        msg_str = ','.join( '|'.join([str(i) for i in row]) for row in rows )

        curs.close()
        conn.close()

        return msg_str


    def sendMail(self):
        '''
        Send e-mail.
        Server must be in the form `adress:port`.
        Username and password are used for autentification.
        '''

        eMailConfig = self.parser.getEmailConfig()

        if (not eMailConfig['Enabled']) or (eMailConfig['Enabled'] in ['0', 'false']):
            return

        logPath = self.parser.getLogFileForType('logSummary')
        logSummary = open(logPath).read()

        head = ''
        head += 'Tests executed: %i\n' % len(logSummary.strip().splitlines())
        head += 'Tests passed: %i\n' % logSummary.count('*PASS*')
        head += 'Tests failed: %i\n' % logSummary.count('*FAIL*')
        head += 'Tests aborted: %i\n' % logSummary.count('*ABORTED*')
        head += 'Tests not exec: %i\n' % logSummary.count('*NO EXEC*')
        head += 'Tests timeout: %i\n' % logSummary.count('*TIMEOUT*')
        head += 'Pass rate: %.2f%%\n\nDetails:\n\n' % (float(logSummary.count('*PASS*'))/ len(logSummary.strip().splitlines())* 100)
        head += ' Suite :: Ep :: Test file                       |   Status    |  Elapsed   |      Date  Time\n'

        msg = MIMEText(head + logSummary + eMailConfig['Message'])
        msg['From'] = eMailConfig['From']
        msg['To'] = eMailConfig['To']
        msg['Subject'] = 'Central Engine status [{0}]'.format(time.strftime("%Y.%m.%d %H.%M"))

        try:
            server = smtplib.SMTP(eMailConfig['SMTPPath'])
        except:
            logError('SMTP: Cannot connect to SMTP server!')
            return False

        try:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(eMailConfig['SMTPUser'], eMailConfig['SMTPPwd'])
            logDebug('SMTP connect success!')
        except:
            logError('SMTP: Cannot autentificate to SMTP server!')
            return False

        try:
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            logDebug('SMTP: E-mail sent successfully!')
            server.quit()
            return True
        except:
            logError('SMTP: Cannot send e-mail!')
            return False


    def commitToDatabase(self):
        '''
        For each EP, for each File, the results of the tests are saved to database,
        exactly as the user defined them.
        '''

        logDebug('CE: Preparing to save into database...')
        time.sleep(3)

        # Inject extra information, then commit
        for ep in self.EpIds:
            for filename in ep.tfList:

                logFile = self.findLog(ep.id, filename)
                ep.addFileInfo(filename, 'twister_tc_log', logFile)

            ep.toDatabase()

        logDebug('CE: Ok, done saving to database!')
        return 1


# --------------------------------------------------------------------------------------------------
#           E X E C U T I O N   S T A T U S
# --------------------------------------------------------------------------------------------------


    def getExecStatus(self, epid):
        '''
        Return execution status for one EP. (stopped, paused, running)
        '''
        if not self.searchEP(epid):
            logError('CE ERROR! EpId `%s` is not in the list of defined EpIds: `%s`!' % \
                (str(epid), str(self.EpIds)) )
            return False
        reversed = dict((v,k) for k,v in dictStatus.iteritems())
        for ep in self.EpIds:
            if(ep.id==epid):
                # Will return a string: stopped, paused, OR running
                status = reversed[ep.executionStatus]
                return status
        return False


    def getExecStatusAll(self):
        '''
        Return execution status for all EPs. (stopped, paused, running)
        Used in the GUI.
        '''
        reversed = dict((v,k) for k,v in dictStatus.iteritems())
        # Will return a string: stopped, paused, OR running
        status = reversed[self.executionStatus]
        if self.start_time:
            start_time = self.start_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            start_time = 'xxxx-xx-xx'
        # If the engine is not stopped, update elapsed time
        if self.executionStatus != STATUS_STOP:
            self.elapsed_time = str(datetime.datetime.today() - self.start_time).split('.')[0]
        # Status + start time + elapsed time
        return '{0};{1};{2}'.format(status, start_time, self.elapsed_time)


    def setExecStatus(self, epid, new_status, msg=''):
        '''
        Set execution status for one EP. (0, 1, 2, or 3)
        Returns a string (stopped, paused, running).
        '''
        #
        if not self.searchEP(epid):
            logError('CE ERROR! EpId `%s` is not in the list of defined EpIds: `%s`!' % \
                (str(epid), str(self.EpIds)) )
            return False

        # Status resume => start running
        if new_status == STATUS_RESUME:
            new_status = STATUS_RUNNING

        ret = False
        for ep in self.EpIds:
            # Only for THIS EP
            if ep.id==epid:
                ret = ep.setStatus(new_status)
                if ret:
                    if msg:
                        logDebug('STATUS changed for EpId %s: %s. Message: `%s`.' % \
                            (epid, ret, str(msg)))
                    else:
                        logDebug('STATUS changed for EpId %s: %s.' % (epid, ret))
                else:
                    logError('Cannot change status for EpId %s!' % epid)

        # If all Stations are stopped, the Central Engine must also stop!
        # This is important, so that in the Java interface, the buttons will change to [Play | Stop]
        if not sum([ep.executionStatus for ep in self.EpIds if ep.id in self.parser.getActiveEpIds()]):
            if self.executionStatus:

                self.executionStatus = STATUS_STOP
                logDebug('CE: All stations stopped! Central engine will also stop.')

                # !!! Send mail
                # self.SendMail(...)

        return ret


    def setExecStatusAll(self, new_status, msg=''):
        '''
        Set execution status for one EP. (0, 1, 2, or 3).
        Returns a string (stopped, paused, running).
        #
        Must try to change status for ALL EPs.
        Both CE and EP have a status.
        '''
        #
        reversed = dict((v,k) for k,v in dictStatus.iteritems())
        # Status must be valid
        if new_status not in dictStatus.values():
            logError("CE ERROR! Status value `%s` is not in the list of defined statuses: `%s`!" % \
                (str(new_status), str(dictStatus.values())) )
            return False

        # Re-initialize the Master XML and Reset all logs on fresh start!
        # This will always happen when the START button is pressed
        if self.executionStatus != STATUS_PAUSED and new_status == STATUS_RUNNING:
            logWarning('CE: RESET Central Engine configuration...') ; ti = time.clock()
            self.parser.updateConfigTS()
            self._initialize(reset=False)
            self.resetLogs()
            logWarning('CE: RESET operation took %.4f seconds.' % (time.clock()-ti))
            # Central engine start time and elapsed time
            self.start_time = datetime.datetime.today() # strftime('%Y-%m-%d %H:%M:%S')
            self.elapsed_time = 0

        # Change test status to PENDING, for all files, on status START, from status STOP
        if new_status == STATUS_RUNNING and self.executionStatus == STATUS_STOP:
            for ep in self.EpIds:
                ep.setTfStatusAll(10)

        # Status resume => start running. The logs must not reset on resume
        if new_status == STATUS_RESUME:
            new_status = STATUS_RUNNING

        # Change status for CE
        self.executionStatus = new_status

        # Change status for ALL EPs
        for ep in self.EpIds:
            ret = ep.setStatus(new_status)
            if not ret:
                logError('Cannot change status for EpId %s!' % ep.id)

        if msg:
            logDebug("Status changed for all EpIds: %s. Message: `%s`." % (reversed[new_status], str(msg)))
        else:
            logDebug("Status changed for all EpIds: %s." % reversed[new_status])

        return reversed[new_status]


# --------------------------------------------------------------------------------------------------
#           L I B R A R Y   AND   T E S T   S U I T E   F I L E S
# --------------------------------------------------------------------------------------------------


    def getLibrariesList(self):
        '''
        Returns the list of exposed libraries, from CE libraries folder.
        This list will be used to syncronize the libs on all EP computers.
        '''
        global TWISTER_PATH
        libs_path = TWISTER_PATH + os.sep + 'lib'
        # All Python source files from Libraries folder
        libs = [d for d in os.listdir(libs_path) if \
            os.path.isfile(libs_path + os.sep + d) and \
            '__init__.py' not in d and \
            os.path.splitext(d)[1]=='.py']
        return sorted(libs)


    def getLibraryFile(self, filename):
        '''
        Sends required library to EP, to be syncronized.
        '''
        global TWISTER_PATH
        filename = TWISTER_PATH + os.sep + 'lib' +os.sep + filename
        if not os.path.isfile(filename):
            logError('CE ERROR! Library file: `%s` does not exist!' % filename)
            return False
        logDebug('CE: Requested library: ' + filename)
        with open(filename, 'rb') as handle:
            return xmlrpclib.Binary(handle.read())


    def getTestSuiteFileList(self, epid, reset_list=True):
        '''
        Returns all TCL/Py files that must be run in current test suite and
        creates the list of files for this EP.
        '''
        if not self.searchEP(epid):
            logError('CE ERROR! EpId `%s` is not in the list of defined EpIds: `%s`!' % \
                (str(epid), str(self.EpIds)) )
            return False

        for ep in self.EpIds:
            if ep.id == epid:
                if not ep.executionStatus:
                    logError('CE ERROR! `%s` requested file list, but the EP is closed! Exiting!' % epid)
                    return False
                break

        fileList = self.parser.getTestSuiteFileList(epid)
        if reset_list: # Reset filelist to pending, only for THIS EP
            for ep in self.EpIds:
                if ep.id == epid:
                    ep.tfList = OrderedDict([ (filename, TestFile(self.parser.getFileInfo(ep.id, filename))) \
                        for filename in fileList ])
        return fileList


    def getTestCaseFile(self, epid, filename):
        '''
        Sends requested filename to TC, to be executed.
        '''
        if not self.searchEP(epid):
            logError('CE ERROR! EpId `%s` is not in the list of defined EpIds: `%s`!' % \
                (str(epid), str(self.EpIds)) )
            return False

        for ep in self.EpIds:
            if ep.id == epid:
                if not ep.executionStatus:
                    logError('CE ERROR! `%s` requested file `%s`, but the EP is closed! Exiting!' % (epid, filename))
                    return False
                break

        runnable = self.parser.getFileInfo(epid, filename).get('Runnable', 'not set')

        if runnable=='true' or runnable=='not set':
            if filename.startswith('~'):
                filename = os.getenv('HOME') + filename[1:]
            if not os.path.isfile(filename):
                logError('CE ERROR! TestCase file: `%s` does not exist!' % filename)
                return False

            logDebug('CE: Station {0} requested file `{1}`'.format(epid, filename))

            with open(filename, 'rb') as handle:
                return xmlrpclib.Binary(handle.read())
        else:
            logDebug('CE: Skipped file `{0}`'.format(filename))
            return False


    def getTestCaseDependency(self, epid, filename):
        '''
        Find dependency for specified file name, or file ID.
        '''
        if not self.searchEP(epid):
            logError('CE ERROR! EpId `%s` is not in the list of defined EpIds: `%s`!' % \
                (str(epid), str(self.EpIds)) )
            return False

        # This is the ID of the file that needs to be checked.
        dep_id = self.parser.getFileInfo(epid, filename).get('dep', None)

        if dep_id:
            # There are dependencies.
            dep_id = dep_id[2:]
            try:
                tc = self.parser.configTS.find(text=dep_id).parent.parent
                return self.parser.getFileInfo(tc.parent.epid.text, dep_id)
            except:
                return False
        elif dep_id is not None:
            # No dependencies.
            return ''
        else:
            # File error.
            logError('CE ERROR! Cannot find info about file `{0}`!'.format(filename))
            return False


    def getTestDescription(self, fname):

        from xml.dom.minidom import parseString
        s = ''
        c = ''
        a = False
        b = False

        for line in open(fname,'r'):
            if "<description>" in line:
                a = True
            if "<title>" in line:
                b = True
            if a:
                s += line.replace('#','')
            if b:
                c += line.replace('#','')
            if "</description>" in line:
                a = False
            if "</title>" in line:
                b = False
            if len(s)>0 and len(c)>0 and not a and not b:
                break

        if len(s) > 0:
            source = parseString(s)
            element = source.getElementsByTagName('description')
            s = element[0].childNodes[0].nodeValue
        if len(c) > 0:
            source = parseString(c)
            element = source.getElementsByTagName('title')
            c = element[0].childNodes[0].nodeValue

        return '-'+c+'-;--'+s


# --------------------------------------------------------------------------------------------------
#           T E S T   F I L E   S T A T U S E S
# --------------------------------------------------------------------------------------------------


    def getTestStatusAll(self, epid=None):
        '''
        Returns a list with all statuses, for all files, in order.
        '''
        if epid and not self.searchEP(epid):
            logError('CE ERROR! EpId `%s` is not in the list of defined EpIds: `%s`!' % \
                (str(epid), str(self.EpIds)) )
            return ''

        o_fnames = self.all_test_files   # Ordered list with all filenames
        u_statuses = OrderedDict()       # Ordered file + status
        fin_statuses = []                # Final statuses, ordered
        #ti = time.clock()

        # Collect file statuses from each EP
        for ep in self.EpIds:
            # If EPID is provided, skip other EPIDs
            if epid and ep.id != epid:
                continue
            all_statuses = ep.getStatusAll()
            if all_statuses:
                u_statuses.update(all_statuses)

        if epid:
            return ','.join([str(s) for s in u_statuses.values()])

        # Append statuses in order
        for fname in o_fnames:
            s = u_statuses.get(fname, '')
            if s: fin_statuses.append(str(s))

        #print('Get Test Status All took %.4f seconds.' % (time.clock()-ti))
        #import random # For testing random statuses
        #fin_statuses[random.randrange(0,len(fin_statuses)-1,1)] = random.choice(['2','3','4','10'])
        return ','.join(fin_statuses)
        #


    def getTestStatus(self, epid, filename):
        '''
        Returns the status for EpId > FileName.
        '''
        if not self.searchEP(epid):
            logError('CE ERROR! EpId `%s` is not in the list of defined EpIds: `%s`!' % \
                (str(epid), str(self.EpIds)) )
            return False

        for ep in self.EpIds:
            # Only for this EP
            if ep.id==epid:
                return ep.getTfStatus(filename)
                #


    def setTestStatus(self, epid, filename, new_status=10, time_elapsed=0.0):
        '''
        Sets status for EpId > FileName.
        '''
        if not self.searchEP(epid):
            logError('CE ERROR! EpId `%s` is not in the list of defined EpIds: `%s`!' % \
                (str(epid), str(self.EpIds)) )
            return False

        # Get logSummary path from FMWCONFIG
        logPath = self.parser.getLogFileForType('logSummary')
        status_str = None

        for ep in self.EpIds:
            # Only for this EP...
            if ep.id == epid:
                #print('CE Info: Status changed {0} -> {1} -> {2}'.format(epid, filename, status_str))

                # Sets file status
                status_str = ep.setTfStatus(filename, new_status)

                # Write important statuses in logs
                if status_str in ['pass', 'fail', 'aborted', 'timeout', 'not executed']:
                    if status_str=='not executed': status_str='*NO EXEC*'
                    else: status_str='*%s*' % status_str.upper()

                    suite = ep.getFileInfo(filename).get('twister_suite_name', '')
                    crash_detected = ep.getFileInfo(filename).get('twister_tc_crash_detected', 0)

                    # Inject information into File Classes
                    now = datetime.datetime.today()
                    ep.addFileInfo(filename, 'twister_tc_status',         status_str.replace('*', ''))
                    ep.addFileInfo(filename, 'twister_tc_crash_detected', crash_detected)
                    ep.addFileInfo(filename, 'twister_tc_time_elapsed',   int(time_elapsed))
                    ep.addFileInfo(filename, 'twister_tc_date_started',  (now - datetime.timedelta(seconds=time_elapsed)).isoformat())
                    ep.addFileInfo(filename, 'twister_tc_date_finished', (now.isoformat()))
                    # The LOG is inserted at the end of the suite, not here.

                    with open(logPath, 'a') as status_file:
                        status_file.write(' {ep}::{suite}::{file} | {status} | {elapsed} | {date}\n'.format(\
                            ep = epid.ljust(9), suite = suite, file = os.path.split(filename)[1].ljust(28),
                            status = status_str.center(11),
                            elapsed = ('%.2fs' % time_elapsed).center(10),
                            date = now.strftime('%a %b %d, %H:%M:%S')))

                # Return string
                return status_str
                #


    def setFileInfo(self, epid, filename, key, value):
        '''
        Set extra information for EpId > Filename.
        Information like Crash detected, OS, IP.
        This can be called from the Runner.
        '''
        if not self.searchEP(epid):
            logError('CE ERROR! EpId `%s` is not in the list of defined EpIds: `%s`!' % \
                (str(epid), str(self.EpIds)) )
            return False

        for ep in self.EpIds:
            # Only for this EP...
            if ep.id == epid:
                ep.addFileInfo(filename, key, value)

        return True


# --------------------------------------------------------------------------------------------------
#           L O G S
# --------------------------------------------------------------------------------------------------

    def getLogFile(self, read, fstart, filename):

        if fstart is None:
            return '*ERROR!* Parameter FEND is NULL!'
        if not filename:
            return '*ERROR!* Parameter FILENAME is NULL!'

        filename = self.parser.getLogsPath() + os.sep + filename

        if not os.path.exists(filename):
            return '*ERROR!* File `%s` does not exist!' % filename

        if not read or read=='0':
            return os.path.getsize(filename)

        fstart = int(fstart)
        f = open(filename)
        f.seek(fstart)
        data = f.read()
        f.close()
        return data


    def logMessage(self, logType, logMessage):
        '''
        This function is exposed in all TCL/Py tests, all logs are centralized.
        '''
        logTypes = self.parser.getLogTypes()
        logType = str(logType).lower()

        if logType == 'logCli' or logType == 'logSummary':
            logError('CE ERROR! logCLI and logSummary are reserved and cannot be written into!')
            return False

        if not logType in logTypes:
            logError("CE ERROR! Log type `%s` is not in the list of defined types: `%s`!" % \
                (logType, logTypes))
            return False

        logPath = self.parser.getLogFileForType(logType)

        f = None
        try:
            f = open(logPath, 'a')
        except:
            logFolder = os.path.split(logPath)[0]
            try:
                os.mkdir(logFolder)
            except:
                logError("CE ERROR! Log file `%s` cannot be written!" % logPath)
            return False
        f.write(logMessage)
        f.close()
        return True
        #


    def logLIVE(self, epid, logMessage):
        '''
        Writes messages in a big log, so all output can be checked LIVE,
        in the java user interface.
        '''
        logPath = self.parser.getLogsPath() + os.sep + epid + '_CLI.log'
        f = None

        try:
            f = open(logPath, 'a')
        except:
            logFolder = os.path.split(logPath)[0]
            try:
                os.mkdir(logFolder)
            except:
                logError("CE ERROR! Log file `%s` cannot be written!" % logPath)
            return False

        f.write(binascii.a2b_base64(logMessage))
        f.close()
        return True
        #


    def findLog(self, epid, filename):
        '''
        Parses the log file of one EPID and returns the log of one test file.
        '''
        logPath = self.parser.getLogsPath() + os.sep + epid + '_CLI.log'

        try:
            data = open(logPath, 'r').read()
        except:
            logError("CE ERROR! Log file `%s` cannot be read!" % logPath)
            return False

        try:
            log = re.search(('(?:.*>>> File `.*` returned `\w+`. <<<)(.+?>>> File `%s` returned `\w+`. <<<)' % filename), data, re.S).group(1)
        except:
            try:
                log = re.search(('(?:.*===== ===== ===== ===== =====)(.+?>>> File `%s` returned `\w+`. <<<)' % filename), data, re.S).group(1)
            except:
                logError("CE ERROR! Cannot find file {0} in the log for {1}!".format(filename, epid))
                return '*no log*'

        return log.replace("'", "\\'")


    def resetLogs(self):
        '''
        All logs defined in master config are erased.
        Log CLI is *magic*, there are more logs, one for each EP.
        '''
        logTypes = self.parser.getLogTypes()
        vError = False
        logDebug('CE debug! Cleaning log files...')

        for logType in logTypes:
            # For CLI
            if logType.lower()=='logcli':
                for ep in self.EpIds:
                    logPath = self.parser.getLogsPath() + os.sep + ep.id + '_CLI.log'
                    try:
                        open(logPath, 'w').close()
                    except:
                        logError("CE ERROR! Log file `%s` cannot be reset!" % logPath)
                        vError = True
                continue
            else:
                logPath = self.parser.getLogFileForType(logType)
            #
            try:
                open(logPath, 'w').close()
            except:
                logError("CE ERROR! Log file `%s` cannot be reset!" % logPath)
                vError = True

        # On error, return IN-succes
        if vError:
            return False
        else:
            return True
        #


    def resetLog(self, logName):
        '''
        Resets one log.
        '''
        logPath = self.parser.getLogsPath() + logName

        try:
            open(logPath, 'w').close()
        except:
            logError("CE ERROR! Log file `%s` cannot be reset!" % logPath)
            return False
        #

# Eof()
