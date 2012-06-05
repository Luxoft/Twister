
# File: CentralEngineClasses.py ; This file is part of Twister.

# Copyright (C) 2012 , Luxoft

# Authors:
#    Andrei Costachi <acostachi@luxoft.com>
#    Andrei Toma <atoma@luxoft.com>
#    Cristian Constantin <crconstantin@luxoft.com>
#    Daniel Cioata <dcioata@luxoft.com>

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''
Requires Python 2.7 !

This file contains Central Engine Class.
All functions from Central Engine are EXPOSED and can be accesed via RPC.
The CE and each EP have a status that can be: start/ stop/ paused.
Each test file has a status that can be: pending, working, pass, fail, skip, etc.
All the statuses are defined in "constants.py".
'''

import os, sys

if not sys.version.startswith('2.7'):
    print('Python version error! Central Engine must run on Python 2.7!')
    exit(1)

import re
import glob
import time
import datetime
import binascii
import xmlrpclib
import MySQLdb

import cherrypy
from cherrypy import _cptools

from xml.dom.minidom import parseString


TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print('$TWISTER_PATH environment variable is not set! Exiting!')
    exit(1)
sys.path.append(TWISTER_PATH)

from CentralEngineOthers import Project

from common.constants import *
from common.tsclogging import *
from common.xmlparser import *

#

# --------------------------------------------------------------------------------------------------
# # # #    C L A S S    C e n t r a l-E n g i n e    # # #
# --------------------------------------------------------------------------------------------------


class CentralEngine(_cptools.XMLRPCController):

    def __init__(self, config_path=None):

        # Config path and XML parser
        self.config_path = config_path
        self.parser = TSCParser(config_path)

        # Build all Parsers + EP + Files structure
        logDebug('CE: Starting Central Engine...') ; ti = time.clock()
        self.project = Project(config_path)
        self.project.setFileStatusAll(STATUS_PENDING)
        logDebug('CE: Initialization took %.4f seconds.' % (time.clock()-ti))


# --------------------------------------------------------------------------------------------------
#           B R O W S E R   F U N C T I O N S
# --------------------------------------------------------------------------------------------------


    def _user_agent(self):
        '''
        User agent returns Browser or XML RPC client.
        This function is not exposed.
        '''
        if  cherrypy.request.headers['User-Agent'].startswith('xmlrpclib.py') or \
            cherrypy.request.headers['User-Agent'].startswith('Apache XML RPC'):
            # XML RPC client
            return 'x'
        else:
            # Browser
            return 'b'


    @cherrypy.expose
    def stats(self):
        '''
        This function should be used in the browser.
        It prints a few statistics about the Central Engine.
        '''
        if self._user_agent == 'x':
            return 0

        reversed = dict((v,k) for k,v in execStatus.iteritems())
        status = reversed[self.project.getUserInfo('status')]

        ret = '''
        <h3>Central Engine Statistics</h3>
        <b>Running on</b>: {host}:{port}<br><br>
        <b>Status</b>: {status}<br><br>
        <b>Processes</b>:<br>{eps}<br><br>
        '''.format(
            status=status,
            host=cherrypy.config['server.socket_host'],
            port=cherrypy.config['server.socket_port'],
            eps='<br>'.join(str(ep) +': '+ reversed[self.project.data['eps'][ep].get('status', STATUS_INVALID)] for ep in self.project.data['eps'])
            )

        return ret

    @cherrypy.expose
    def status(self):
        return self.stats()


    @cherrypy.expose
    def log(self):
        '''
        This function should be used in the browser.
        It prints the Central Engine log.
        '''
        if self._user_agent == 'x':
            return 0

        global LOG_FILE
        log = open(LOG_FILE).read()
        return log.replace('\n', '<br>')

    @cherrypy.expose
    def logs(self):
        return self.log()


# --------------------------------------------------------------------------------------------------
#           H E L P E R   F U N C T I O N S
# --------------------------------------------------------------------------------------------------


    @cherrypy.expose
    def echo(self, msg):
        '''
        Simple echo function, for testing connection.
        '''
        logInfo(':: %s' % str(msg))
        return 'CE reply: ' + msg


    @cherrypy.expose
    def getConfigPath(self):
        '''
        The path to Master config file.
        '''
        return self.config_path


    @cherrypy.expose
    def getLogsPath(self):
        '''
        The path to Logs files.
        '''
        return self.parser.getLogsPath()


    @cherrypy.expose
    def getLogTypes(self):
        '''
        All types of logs defined in Master config file will be exposed
        in the testing environment.
        '''
        return self.parser.getLogTypes()


    @cherrypy.expose
    def runDBSelect(self, field_id):
        '''
        Selects from database.
        This function is called from the Java Interface.
        '''
        dbparser = DBParser(self.parser.getDbConfigPath())
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


    @cherrypy.expose
    def sendMail(self):
        '''
        Send e-mail after the suites are run.
        Server must be in the form `adress:port`.
        Username and password are used for authentication.
        This function is called every time the Central Engine stops.
        '''

        ret = self.project.sendMail()
        return ret


    @cherrypy.expose
    def commitToDatabase(self):
        '''
        For each EP, for each Suite and each File, the results of the tests are saved to database,
        exactly as the user defined them in Database.XML.
        This function is called from the Java GUI, or from an EP.
        '''

        logDebug('CE: Preparing to save into database...')
        time.sleep(3)
        ret = self.project.saveToDatabase()
        logDebug('CE: Done saving to database!')
        return ret


# --------------------------------------------------------------------------------------------------
#           E P   A N D   F I L E   V A R I A B L E S
# --------------------------------------------------------------------------------------------------


    @cherrypy.expose
    def searchEP(self, epname):
        '''
        Search one EP and return True or False.
        '''
        epList = self.project.data['eps'].keys()
        return epname in epList


    @cherrypy.expose
    def listEPs(self):
        '''
        Returns all EPs for current user.
        '''
        epList = self.project.data['eps'].keys()
        return ','.join(epList)


    @cherrypy.expose
    def listSuites(self, epname):
        '''
        Returns all Suites for one EP from current user.
        '''
        if not self.searchEP(epname):
            logError('CE ERROR! EP `%s` is not in the list of defined EPs: `%s`!' % \
                (str(epname), str(self.project.data['eps'])) )
            return False

        suitesList = self.project.getEpInfo(epname)['suites'].keys()
        return ','.join(suitesList)


    @cherrypy.expose
    def getEpVariable(self, epname, variable):
        '''
        This function is called from the Execution Process,
        to get information that is available only here, or are hard to get:
        - what the user selected in the Java interface (release, build, comments)
        - the name of the suite, the test files, etc.
        '''

        data = self.project.getEpInfo(epname)
        return data.get(variable, False)


    @cherrypy.expose
    def setEpVariable(self, epname, variable, value):
        '''
        This function is called from the Execution Process,
        to inject values inside the EP classes.
        The values can saved in the Database, when commiting.
        Eg: the OS, the IP, or other information can be added this way.
        '''

        return self.project.setEpInfo(epname, variable, value)


    @cherrypy.expose
    def getFileVariable(self, file_id, variable):
        '''
        Get information about a test file:
        - dependencies, runnable, status, etc.
        '''

        data = self.project.getFileInfo(file_id)
        return data.get(variable, False)


    @cherrypy.expose
    def setFileVariable(self, epname, suite, filename, variable, value):
        '''
        Set extra information for a Filename.
        Information like Crash detected, OS, IP.
        This can be called from the Runner.
        '''

        return self.project.setFileInfo(epname, suite, filename, variable, value)


    @cherrypy.expose
    def setStartedBy(self, user):
        '''
        Remember the user that started the Central Engine.
        This function is called from the Java Interface.
        '''

        logDebug('CE: Started by user `%s`.' % str(user))
        self.project.setUserInfo('started_by', str(user))
        return 1


# --------------------------------------------------------------------------------------------------
#           E X E C U T I O N   S T A T U S
# --------------------------------------------------------------------------------------------------


    @cherrypy.expose
    def getExecStatus(self, epname):
        '''
        Return execution status for one EP. (stopped, paused, running, invalid)
        Used by EPs.
        '''

        data = self.project.getEpInfo(epname)
        # EP alive status = ping
        last_seen = data.get('last_seen_alive', 0)
        some_time = datetime.datetime.today()
        self.project.setEpInfo(epname, 'last_seen_alive', some_time.strftime('%Y-%m-%d %H:%M:%S'))

        if not last_seen:
            self.project.setEpInfo(epname, 'ping', 0)
        else:
            last_seen = datetime.datetime.strptime(last_seen, '%Y-%m-%d %H:%M:%S')
            #(now - datetime.timedelta(seconds=time_elapsed))
        # Return a status, or stop
        reversed = dict((v,k) for k,v in execStatus.iteritems())
        return reversed[data.get('status', 8)]


    @cherrypy.expose
    def getExecStatusAll(self):
        '''
        Return execution status for all EPs. (stopped, paused, running, invalid)
        Used in the Java GUI.
        '''

        data = self.project.getUserInfo()
        reversed = dict((v,k) for k,v in execStatus.iteritems())
        status = reversed[data.get('status', 8)]

        # If start time is not define, then define it
        if not data.get('start_time'):
            start_time = datetime.datetime.today()
            self.project.setUserInfo('start_time', start_time.strftime('%Y-%m-%d %H:%M:%S'))
        else:
            start_time = datetime.datetime.strptime(data['start_time'], '%Y-%m-%d %H:%M:%S')

        # If the engine is not stopped, update elapsed time
        if data.get('status', 8) != STATUS_STOP:
            elapsed_time = str(datetime.datetime.today() - start_time).split('.')[0]
            self.project.setUserInfo('elapsed_time', elapsed_time)
        else:
            elapsed_time = data.get('elapsed_time', 0)

        # Status + start time + elapsed time
        start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
        return '{0}; S {1}; E {2}; Usr {3}'.format(status, start_time, elapsed_time, data.get('started_by', 'X'))


    @cherrypy.expose
    def setExecStatus(self, epname, new_status, msg=''):
        '''
        Set execution status for one EP. (0, 1, 2, or 3)
        Returns a string (stopped, paused, running).
        '''
        if not self.searchEP(epname):
            logError('CE ERROR! EP `%s` is not in the list of defined EPs: `%s`!' % \
                (str(epname), str(self.project.data['eps'].keys())) )
            return False

        # Status resume => start running
        if new_status == STATUS_RESUME:
            new_status = STATUS_RUNNING

        ret = self.project.setEpInfo(epname, 'status', new_status)
        reversed = dict((v,k) for k,v in execStatus.iteritems())

        if ret:
            if msg:
                logDebug('CE: Status changed for EP %s: %s. Message: `%s`.' % (epname, reversed[new_status], str(msg)))
            else:
                logDebug('CE: Status changed for EP %s: %s.' % (epname, reversed[new_status]))
        else:
            logError('CE ERROR! Cannot change status for EP %s !' % epname)

        # If all Stations are stopped, the Central Engine must also stop!
        # This is important, so that in the Java GUI, the buttons will change to [Play | Stop]
        if not sum([self.project.getEpInfo(ep).get('status', 8) for ep in self.project.data['eps']]):

            # If User status was not Stop
            if self.project.getUserInfo('status'):

                self.project.setUserInfo('status', STATUS_STOP)
                logDebug('CE: All stations stopped! Central engine will also STOP!')

                # On Central Engine stop, send e-mail?
                #self.sendMail()

                # On Central Engine stop, save to database?
                #self.commitToDatabase()

        return reversed[new_status]


    @cherrypy.expose
    def setExecStatusAll(self, new_status, msg=''):
        '''
        Set execution status for all EPs. (0, 1, 2, or 3).
        Returns a string (stopped, paused, running).
        Both CE and EP have a status.
        '''
        if new_status not in execStatus.values():
            logError("CE ERROR! Status value `%s` is not in the list of defined statuses: `%s`!" % \
                (str(new_status), str(execStatus.values())) )
            return False

        # Status resume => start running. The logs must not reset on resume
        if new_status == STATUS_RESUME:
            new_status = STATUS_RUNNING

        # Return the current status, or 8 = INVALID
        executionStatus = self.project.getUserInfo('status') or 8

        # Re-initialize the Master XML and Reset all logs on fresh start!
        # This will always happen when the START button is pressed
        if (executionStatus != STATUS_PAUSED and executionStatus != STATUS_RUNNING) and new_status == STATUS_RUNNING:

            logWarning('CE: RESET Central Engine configuration...') ; ti = time.clock()
            self.project = Project(self.config_path)
            self.resetLogs()
            logWarning('CE: RESET operation took %.4f seconds.' % (time.clock()-ti))

            # User start time and elapsed time
            self.project.setUserInfo('start_time', datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            self.project.setUserInfo('elapsed_time', 0)

        # Change test status to PENDING, for all files, on status START, from status STOP
        if executionStatus == STATUS_STOP and new_status == STATUS_RUNNING:
            self.project.setFileStatusAll(STATUS_PENDING)

        # Change status for User
        self.project.setUserInfo('status', new_status)

        # Change status for ALL EPs
        for epname in self.project.data['eps']:
            self.project.setEpInfo(epname, 'status', new_status)

        reversed = dict((v,k) for k,v in execStatus.iteritems())

        if msg:
            logDebug("CE: Status changed for all EPs: %s. Message: `%s`." % (reversed[new_status], str(msg)))
        else:
            logDebug("CE: Status changed for all EPs: %s." % reversed[new_status])

        return reversed[new_status]


# --------------------------------------------------------------------------------------------------
#           L I B R A R Y   AND   T E S T   S U I T E   F I L E S
# --------------------------------------------------------------------------------------------------


    @cherrypy.expose
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


    @cherrypy.expose
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


    @cherrypy.expose
    def getEpFiles(self, epname):
        '''
        Returns all files that must be run on one EP.
        '''
        if not self.searchEP(epname):
            logError('CE ERROR! EP `%s` is not in the list of defined EPs: `%s`!' % \
                (str(epname), str(self.project.data['eps'])) )
            return False

        try: data = self.project.getEpFiles(epname)
        except: data = False
        return data


    @cherrypy.expose
    def getSuiteFiles(self, epname, suite):
        '''
        Returns all files that must be run on one Suite.
        '''
        if not self.searchEP(epname):
            logError('CE ERROR! EP `%s` is not in the list of defined EPs: `%s`!' % \
                (str(epname), str(self.project.data['eps'])) )
            return False

        try: data = self.project.getSuiteFiles(epname, suite)
        except: data = False
        return data


    @cherrypy.expose
    def getTestFile(self, epname, file_id):
        '''
        Sends requested file to TC, to be executed.
        '''
        if not self.searchEP(epname):
            logError('CE ERROR! EP `%s` is not in the list of defined EPs: `%s`!' % \
                (str(epname), str(self.project.data['eps'])) )
            return False
        if not self.project.getEpInfo(epname).get('status'):
            logError('CE ERROR! `%s` requested file list, but the EP is closed! Exiting!' % epname)
            return False

        data = self.project.getFileInfo(file_id)
        filename = data.get('file', 'invalid file')
        runnable = data.get('Runnable', 'not set')

        if runnable=='true' or runnable=='not set':
            if filename.startswith('~'):
                filename = os.getenv('HOME') + filename[1:]
            if not os.path.isfile(filename):
                logError('CE ERROR! TestCase file: `%s` does not exist!' % filename)
                return False

            logDebug('CE: Station {0} requested file `{1}`'.format(epname, filename))

            with open(filename, 'rb') as handle:
                return xmlrpclib.Binary(handle.read())
        else:
            logDebug('CE: Skipped file `{0}`'.format(filename))
            return False


    @cherrypy.expose
    def getTestDescription(self, fname):
        '''
        Used in Java GUI.
        Returns the title and the descrip of a test file.
        '''

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


    @cherrypy.expose
    def getFileStatusAll(self, epname=None, suite=None):
        '''
        Returns a list with all statuses, for all files, in order.
        The status of one file can be obtained with get File Variable.
        '''
        if epname and not self.searchEP(epname):
            logError('CE ERROR! EP `%s` is not in the list of defined EPs: `%s`!' % \
                (str(epname), str(self.project.data['eps'])) )
            return ''

        statuses = self.project.getFileStatusAll(epname, suite)
        return ','.join(statuses)


    @cherrypy.expose
    def setFileStatus(self, epname, file_id, new_status=10, time_elapsed=0.0):
        '''
        Set status for one file and write in log summary.
        '''
        if not self.searchEP(epname):
            logError('CE ERROR! EP `%s` is not in the list of defined EPs: `%s`!' % \
                (str(epname), str(self.project.data['eps'])) )
            return False
        if new_status not in testStatus.values():
            logError("CE ERROR! Status value `%s` is not in the list of defined statuses: `%s`!" % \
                (str(new_status), str(testStatus.values())) )
            return False

        data = self.project.getFileInfo(file_id)
        filename = os.path.split(data['file'])[1]
        suite = data['suite']

        # Sets file status
        self.project.setFileInfo(epname, suite, file_id, 'status', new_status)
        reversed = dict((v,k) for k,v in testStatus.iteritems())
        status_str = reversed[new_status]

        # Get logSummary path from framework config
        logPath = self.parser.getLogFileForType('logSummary')

        # Only write important statuses in logs
        if status_str in ['pass', 'fail', 'aborted', 'timeout', 'not executed']:
            if status_str=='not executed': status_str='*NO EXEC*'
            else: status_str='*%s*' % status_str.upper()

            # # Inject information into File Classes
            now = datetime.datetime.today()
            self.project.setFileInfo(epname, suite, file_id, 'twister_tc_status',
                status_str.replace('*', ''))
            self.project.setFileInfo(epname, suite, file_id, 'twister_tc_crash_detected',
                data.get('twister_tc_crash_detected', 0))
            self.project.setFileInfo(epname, suite, file_id, 'twister_tc_time_elapsed',
                int(time_elapsed))
            self.project.setFileInfo(epname, suite, file_id, 'twister_tc_date_started',
                (now - datetime.timedelta(seconds=time_elapsed)).isoformat())
            self.project.setFileInfo(epname, suite, file_id, 'twister_tc_date_finished',
                (now.isoformat()))

            with open(logPath, 'a') as status_file:
                status_file.write(' {ep}::{suite}::{file} | {status} | {elapsed} | {date}\n'.format(
                    ep = epname.center(9), suite = suite.center(9), file = filename.center(28),
                    status = status_str.center(11),
                    elapsed = ('%.2fs' % time_elapsed).center(10),
                    date = now.strftime('%a %b %d, %H:%M:%S')))

        # Return string
        return status_str


    @cherrypy.expose
    def setFileStatusAll(self, new_status, epname):
        '''
        Reset file status for all files of one EP.
        '''
        return self.project.setFileStatusAll(new_status, epname)


# --------------------------------------------------------------------------------------------------
#           L O G S
# --------------------------------------------------------------------------------------------------


    @cherrypy.expose
    def getLogFile(self, read, fstart, filename):
        '''
        Used in Java GUI to show the logs.
        '''

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

        return binascii.b2a_base64(data)


    @cherrypy.expose
    def logMessage(self, logType, logMessage):
        '''
        This function is exposed in all tests, all logs are centralized.
        '''

        logType = str(logType).lower()
        logTypes = self.parser.getLogTypes()

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


    @cherrypy.expose
    def logLIVE(self, epname, logMessage):
        '''
        Writes CLI messages in a big log, so all output can be checked LIVE,
        in the Java GUI.
        '''
        logPath = self.parser.getLogsPath() + os.sep + epname + '_CLI.log'
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


    @cherrypy.expose
    def findLog(self, epname, filename):
        '''
        Parses the log file of one EP and returns the log of one test file.
        '''
        logPath = self.parser.getLogsPath() + os.sep + epname + '_CLI.log'

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
                logError("CE ERROR! Cannot find file {0} in the log for {1}!".format(filename, epname))
                return '*no log*'

        return log.replace("'", "\\'")


    @cherrypy.expose
    def resetLogs(self):
        '''
        All logs defined in master config are erased.
        Log CLI is *magic*, there are more logs, one for each EP.
        '''
        logTypes = self.parser.getLogTypes()
        vError = False
        logDebug('Cleaning log files...')

        for log in glob.glob(self.parser.getLogsPath() + os.sep + '*.log'):
            try: os.remove(log)
            except: pass

        for logType in logTypes:
            # For CLI
            if logType.lower()=='logcli':
                for epname in self.project.data['eps']:
                    logPath = self.parser.getLogsPath() + os.sep + epname + '_CLI.log'
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


    @cherrypy.expose
    def resetLog(self, logName):
        '''
        Resets one log.
        '''
        logPath = self.parser.getLogsPath() + os.sep + logName

        try:
            open(logPath, 'w').close()
            logDebug('Cleaned log `%s`.' % logPath)
            return True
        except:
            logError("CE ERROR! Log file `%s` cannot be reset!" % logPath)
            return False

# Eof()
