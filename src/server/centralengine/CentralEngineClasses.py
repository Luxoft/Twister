
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
Central Engine Class
********************

All functions from Central Engine are EXPOSED and can be accesed via XML-RPC.\n
The Central Engine and each EP have a status that can be: start/ stop/ paused.\n
Each test file has a status that can be: pending, working, pass, fail, skip, etc.\n
All the statuses are defined in "constants.py".\n
'''

import os, sys

if not sys.version.startswith('2.7'):
    print('Python version error! Central Engine must run on Python 2.7!')
    exit(1)

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print('$TWISTER_PATH environment variable is not set! Exiting!')
    exit(1)
sys.path.append(TWISTER_PATH)

import re
import glob
import time
import datetime
import binascii
import xmlrpclib
import MySQLdb
import cherrypy

from cherrypy import _cptools

from CentralEngineOthers import Project

from common.constants import *
from common.tsclogging import *
from common.xmlparser import *

#

# --------------------------------------------------------------------------------------------------
# # # #    C L A S S    C e n t r a l-E n g i n e    # # #
# --------------------------------------------------------------------------------------------------


class CentralEngine(_cptools.XMLRPCController):

    '''
    *This class is the core of all operations.*
    '''

    def __init__(self):

        # Build all Parsers + EP + Files structure
        logDebug('CE: Starting Central Engine...') ; ti = time.clock()
        self.project = Project()
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
    def stats(self, user, epname='', suite=''):
        '''
        This function should be used in the browser.
        It prints a few statistics about the Central Engine.
        '''
        if self._user_agent == 'x':
            return 0

        reversed = dict((v,k) for k,v in execStatus.iteritems())
        status = reversed[self.project.getUserInfo('status')]
        now = datetime.datetime.today()
        if now.second < 59:
            now_str = now.replace(second=now.second+1).strftime('%Y-%m-%d %H:%M:%S')
        else:
            now_str = now.replace(minute=now.minute+1, second=0).strftime('%Y-%m-%d %H:%M:%S')
        ce_host = cherrypy.config['server.socket_host']
        ce_port = cherrypy.config['server.socket_port']
        host = cherrypy.request.headers['Host']

        if epname:
            if not self.searchEP(user, epname):
                return '<b>Execution Process `{0}` doesn\'t exist!</b>'.format(epname)

            # EP name only
            if not suite:
                data = self.project.getEpInfo(epname)
                ret = '''
<head>
<title>Central Engine Statistics</title>
</head>
<body>
<h3>Execution Process `{epname}`</h3>
<b>Status</b>: {status}<br><br>
<b>Ping</b>: {ping}<br><br>
<b>Suites</b>: [<br>{suites}<br>]
</body>
            '''.format(
                    epname = epname,
                    status = reversed[data.get('status', STATUS_INVALID)],
                    ping = str( (now - datetime.datetime.strptime(data.get('last_seen_alive', now_str), '%Y-%m-%d %H:%M:%S')).seconds ) + 's',
                    suites = '<br>'.join(['&nbsp;&nbsp;<a href="http://{host}/stats?epname={ep}&suite={s}">{s}</a>'.format(
                             host = host, ep = epname, s = k)
                             for k in data['suites'].keys()])
                )

            # EP name and Suite name
            else:
                data = self.project.getSuiteInfo(suite)
                reversed = dict((v,k) for k,v in testStatus.iteritems())
                ret = '''
<head>
<title>Central Engine Statistics</title>
</head>
<body>
<h3>EP `{epname}` -> Suite `{suite}`</h3>
<b>Files</b>: [<br>{files}<br>]
</body>
                '''.format(
                    epname = epname,
                    suite = suite,
                    files = '<br>'.join(['&nbsp;&nbsp;{0}: {1}'.format(data['files'][k]['file'], reversed[data['files'][k]['status']] )
                            for k in data['files']])
                )

        # General statistics
        else:
            ret = '''
<head>
<title>Central Engine Statistics</title>
</head>
<body>
<h3>Central Engine Statistics</h3>
<b>Running on</b>: {host}:{port}<br><br>
<b>Status</b>: {status}<br><br>
<b>Processes</b>: [<br>{eps}<br>]
</body>
        '''.format(
            status = status,
            host = ce_host,
            port = ce_port,
            eps = '<br>'.join(
                ['&nbsp;&nbsp;<a href="http://{host}/stats?epname={ep}">{ep}</a>: {status}'.format(
                    ep=ep, host=host, status=reversed[self.listEPs(user)[ep].get('status', STATUS_INVALID)])
                    for ep in self.listEPs(user)]
                )
            )

        return ret

    @cherrypy.expose
    def status(self, user, epname='', suite=''):
        return self.stats(user, epname, suite)


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
    def getLogsPath(self, user):
        '''
        Returns the path to Logs files.
        '''
        return self.project.getUserInfo(user, 'logs_path')


    @cherrypy.expose
    def getLogTypes(self, user):
        '''
        Returns a list with all types of logs defined in Master config.
        All logs will be exposed to the testing environment.
        '''
        return self.project.getUserInfo(user, 'log_types')


    @cherrypy.expose
    def runDBSelect(self, user, field_id):
        '''
        Selects from database.
        This function is called from the Java GUI.
        '''
        dbparser = DBParser( self.project.parsers[user].getDbConfigPath() )
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
    def sendMail(self, user):
        '''
        Send e-mail after the suites are run.\n
        Server must be in the form `adress:port`.\n
        Username and password are used for authentication.\n
        This function is called every time the Central Engine stops.
        '''

        try:
            ret = self.project.sendMail(user)
            return ret
        except:
            return False


    @cherrypy.expose
    def commitToDatabase(self, user):
        '''
        For each EP, for each Suite and each File, the results of the tests are saved to database,
        exactly as the user defined them in Database.XML.\n
        This function is called from the Java GUI, or from an EP.
        '''

        logDebug('CE: Preparing to save into database...')
        time.sleep(3)
        ret = self.project.saveToDatabase(user)
        logDebug('CE: Done saving to database!')
        return ret


# --------------------------------------------------------------------------------------------------
#           E P   A N D   F I L E   V A R I A B L E S
# --------------------------------------------------------------------------------------------------


    @cherrypy.expose
    def searchEP(self, user, epname):
        '''
        Search one EP and return True or False.
        '''
        epList = self.project.getUserInfo(user, 'eps').keys()
        return epname in epList


    @cherrypy.expose
    def listEPs(self, user):
        '''
        Returns all EPs for current user.
        '''
        epList = self.project.getUserInfo(user, 'eps').keys()
        return ','.join(epList)


    @cherrypy.expose
    def listSuites(self, user, epname):
        '''
        Returns all Suites for one EP from current user.
        '''
        if not self.searchEP(user, epname):
            logError('CE ERROR! EP `%s` is not in the list of defined EPs: `%s`!' % \
                (str(epname), self.listEPs(user)) )
            return False

        suitesList = self.project.getEpInfo(user, epname)['suites'].keys()
        return ','.join(suitesList)


    @cherrypy.expose
    def getEpVariable(self, user, epname, variable):
        '''
        This function is called from the Execution Process,
        to get information that is available only here, or are hard to get:

        - what the user selected in the Java GUI (release, build, comments, etc)
        - the name of the suite, the test files, etc.
        '''

        data = self.project.getEpInfo(user, epname)
        return data.get(variable, False)


    @cherrypy.expose
    def setEpVariable(self, user, epname, variable, value):
        '''
        This function is called from the Execution Process,
        to inject values inside the EP classes.\n
        The values can saved in the Database, when commiting.\n
        Eg: the OS, the IP, or other information can be added this way.
        '''

        return self.project.setEpInfo(user, epname, variable, value)


    @cherrypy.expose
    def getSuiteVariable(self, user, epname, suite, variable):
        '''
        This function is called from the Execution Process,
        to get information that is available only here, or are hard to get.
        '''

        data = self.project.getSuiteInfo(user, epname, suite)
        return data.get(variable, False)


    @cherrypy.expose
    def getFileVariable(self, user, file_id, variable):
        '''
        Get information about a test file: dependencies, runnable, status, etc.
        '''

        data = self.project.getFileInfo(user, file_id)
        return data.get(variable, False)


    @cherrypy.expose
    def setFileVariable(self, user, epname, suite, filename, variable, value):
        '''
        Set extra information for a Filename, like Crash detected, OS, IP.\n
        Can be called from the Runner.
        '''

        return self.project.setFileInfo(user, epname, suite, filename, variable, value)


    @cherrypy.expose
    def setStartedBy(self, user, name):
        '''
        Remember the user that started the Central Engine.\n
        Called from the Java GUI.
        '''

        logDebug('CE: Started by user name `%s`.'  % str(name))
        self.project.setUserInfo(user, 'started_by', str(name))
        return 1


# --------------------------------------------------------------------------------------------------
#           E X E C U T I O N   S T A T U S
# --------------------------------------------------------------------------------------------------


    @cherrypy.expose
    def getExecStatus(self, user, epname):
        '''
        Return execution status for one EP. (stopped, paused, running, invalid)\n
        Called from the EP.
        '''
        if not self.searchEP(user, epname):
            logError('CE ERROR! EP `%s` is not in the list of defined EPs: `%s`!' %
                     (str(epname), self.listEPs(user)) )
            return False

        data = self.project.getEpInfo(user, epname)

        # Set EP last seen alive
        self.project.setEpInfo(user, epname, 'last_seen_alive', datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        # Return a status, or stop
        reversed = dict((v,k) for k,v in execStatus.iteritems())
        return reversed[data.get('status', 8)]


    @cherrypy.expose
    def getExecStatusAll(self, user):
        '''
        Return execution status for all EPs. (stopped, paused, running, invalid)\n
        Called from the Java GUI.
        '''

        data = self.project.getUserInfo(user)
        reversed = dict((v,k) for k,v in execStatus.iteritems())
        status = reversed[data.get('status', 8)]

        # If start time is not define, then define it
        if not data.get('start_time'):
            start_time = datetime.datetime.today()
            self.project.setUserInfo(user, 'start_time', start_time.strftime('%Y-%m-%d %H:%M:%S'))
        else:
            start_time = datetime.datetime.strptime(data['start_time'], '%Y-%m-%d %H:%M:%S')

        # If the engine is not stopped, update elapsed time
        if data.get('status', 8) != STATUS_STOP:
            elapsed_time = str(datetime.datetime.today() - start_time).split('.')[0]
            self.project.setUserInfo(user, 'elapsed_time', elapsed_time)
        else:
            elapsed_time = data.get('elapsed_time', 0)

        # Status + start time + elapsed time
        start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
        return '{0}; {1}; {2}; {3}'.format(status, start_time, elapsed_time, data.get('started_by', 'X'))


    @cherrypy.expose
    def setExecStatus(self, user, epname, new_status, msg=''):
        '''
        Set execution status for one EP. (0, 1, 2, or 3)\n
        Returns a string (stopped, paused, running).\n
        Called from the EP.
        '''
        if not self.searchEP(user, epname):
            logError('CE ERROR! EP `%s` is not in the list of defined EPs: `%s`!' %
                (str(epname), self.listEPs(user)) )
            return False
        if new_status not in execStatus.values():
            logError("CE ERROR! Status value `%s` is not in the list of defined statuses: `%s`!" %\
                     (str(new_status), str(execStatus.values())) )
            return False

        # Status resume => start running
        if new_status == STATUS_RESUME:
            new_status = STATUS_RUNNING

        ret = self.project.setEpInfo(user, epname, 'status', new_status)
        reversed = dict((v,k) for k,v in execStatus.iteritems())

        if ret:
            if msg:
                logDebug('CE: Status changed for `%s %s` - %s. Message: `%s`.' % (user, epname, reversed[new_status], str(msg)))
            else:
                logDebug('CE: Status changed for `%s %s` - %s.' % (user, epname, reversed[new_status]))
        else:
            logError('CE ERROR! Cannot change status for `%s %s` !' % (user, epname))

        # If all Stations are stopped, the Central Engine must also stop!
        # This is important, so that in the Java GUI, the buttons will change to [Play | Stop]
        if not sum([self.project.getEpInfo(user, ep).get('status', 8) for ep in self.project.parsers[user].getActiveEps()]):

            # If User status was not Stop
            if self.project.getUserInfo(user, 'status'):

                self.project.setUserInfo(user, 'status', STATUS_STOP)
                logDebug('CE: All stations stopped for user `%s`! Central engine will also STOP!\n' % user)

                # On Central Engine stop, send e-mail?
                self.sendMail(user)

                # On Central Engine stop, save to database?
                #self.commitToDatabase()

        return reversed[new_status]


    @cherrypy.expose
    def setExecStatusAll(self, user, new_status, msg=''):
        '''
        Set execution status for all EPs. (0, 1, 2, or 3).\n
        Returns a string (stopped, paused, running).\n
        The `message` parameter can explain why the status has changed.\n
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
        executionStatus = self.project.getUserInfo(user, 'status') or 8

        # Re-initialize the Master XML and Reset all logs on fresh start!
        # This will always happen when the START button is pressed, if CE is stopped
        if (executionStatus == STATUS_STOP or executionStatus == STATUS_INVALID) and new_status == STATUS_RUNNING:

            # If the msg is a path to an existing file...
            if msg and os.path.isfile(msg):
                data = open(msg).read().strip()
                # If the file is XML, send it to project reset function
                if data[0] == '<' and data [-1] == '>':
                    self.project.reset(user, msg)
                    msg = ''
                else:
                    logDebug('CE: You are probably trying to use file `%s` as config file, but it\'s not a valid XML!' % msg)
                    self.project.reset(user)
                del data
            else:
                self.project.reset(user)

            self.resetLogs(user)

            # User start time and elapsed time
            self.project.setUserInfo(user, 'start_time', datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            self.project.setUserInfo(user, 'elapsed_time', 0)

        # Update status for User
        self.project.setUserInfo(user, 'status', new_status)

        # Update status for all active EPs
        active_eps = self.project.parsers[user].getActiveEps()
        for epname in active_eps:
            self.project.setEpInfo(user, epname, 'status', new_status)

        reversed = dict((v,k) for k,v in execStatus.iteritems())

        if msg:
            logDebug("CE: Status changed for `%s %s` -> %s. Message: `%s`.\n" % (user, active_eps, reversed[new_status], str(msg)))
        else:
            logDebug("CE: Status changed for `%s %s` -> %s.\n" % (user, active_eps, reversed[new_status]))

        return reversed[new_status]


# --------------------------------------------------------------------------------------------------
#           L I B R A R Y   AND   T E S T   S U I T E   F I L E S
# --------------------------------------------------------------------------------------------------


    @cherrypy.expose
    def getLibrariesList(self):
        '''
        Returns the list of exposed libraries, from CE libraries folder.\n
        This list will be used to syncronize the libs on all EP computers.\n
        Called from the Runner.
        '''
        global TWISTER_PATH
        libs_path = TWISTER_PATH + os.sep + 'lib'
        # All Python source files from Libraries folder
        libs = [d for d in os.listdir(libs_path) if \
            os.path.isfile(libs_path + os.sep + d) and \
            '__init__.py' not in d and \
            os.path.splitext(d)[1] in ['.py', '.zip']]
        return sorted(libs)


    @cherrypy.expose
    def getLibraryFile(self, filename):
        '''
        Sends required library to EP, to be syncronized.\n
        Called from the Runner.
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
    def getEpFiles(self, user, epname):
        '''
        Returns all files that must be run on one EP.\n
        Called from the Runner.
        '''
        if not self.searchEP(user, epname):
            logError('CE ERROR! EP `%s` is not in the list of defined EPs: `%s`!' % \
                (str(epname), self.listEPs(user)) )
            return False

        try: data = self.project.getEpFiles(user, epname)
        except: data = False
        return data


    @cherrypy.expose
    def getSuiteFiles(self, user, epname, suite):
        '''
        Returns all files that must be run on one Suite.\n
        Called from the Runner.
        '''
        if not self.searchEP(user, epname):
            logError('CE ERROR! EP `%s` is not in the list of defined EPs: `%s`!' % \
                (str(epname), self.listEPs(user)) )
            return False

        try: data = self.project.getSuiteFiles(user, epname, suite)
        except: data = False
        return data


    @cherrypy.expose
    def getTestFile(self, user, epname, file_id):
        '''
        Sends requested file to TC, to be executed.\n
        Called from the Runner.
        '''
        if not self.searchEP(user, epname):
            logError('CE ERROR! EP `%s` is not in the list of defined EPs: `%s`!' % \
                (str(epname), self.listEPs(user)) )
            return False
        if not self.project.getEpInfo(user, epname).get('status'):
            logError('CE ERROR! `%s` requested file list, but the EP is closed! Exiting!' % epname)
            return False

        data = self.project.getFileInfo(user, file_id)
        filename = data.get('file', 'invalid file')
        runnable = data.get('Runnable', 'not set')

        if runnable=='true' or runnable=='not set':
            if filename.startswith('~'):
                filename = os.getenv('HOME') + filename[1:]
            if not os.path.isfile(filename):
                logError('CE ERROR! TestCase file: `%s` does not exist!' % filename)
                return ''

            logDebug('CE: Station {0} requested file `{1}`'.format(epname, filename))

            with open(filename, 'rb') as handle:
                return xmlrpclib.Binary(handle.read())
        else:
            logDebug('CE: Skipped file `{0}`'.format(filename))
            return False


    @cherrypy.expose
    def getTestDescription(self, fname):
        '''
        Returns the title and the description of a test file.\n
        Called from the Java GUI.
        '''
        title = ''
        descr = ''

        for line in open(fname,'r'):
            s = line.strip()
            if '<title>' in line and '</title>' in line:
                a = s.find('<title>') + len('<title>')
                b = s.find('</title>')
                title = s[a:b]
                if title: continue
            if '<description>' in line and '</description>' in line:
                a = s.find('<description>') + len('<description>')
                b = s.find('</description>')
                descr = s[a:b]
                if descr: continue

            if title and descr: break

        return '-'+title+'-;--'+descr


# --------------------------------------------------------------------------------------------------
#           T E S T   F I L E   S T A T U S E S
# --------------------------------------------------------------------------------------------------


    @cherrypy.expose
    def getFileStatusAll(self, user, epname=None, suite=None):
        '''
        Returns a list with all statuses, for all files, in order.\n
        The status of one file can be obtained with get File Variable.\n
        Called from the Java GUI.
        '''
        if epname and not self.searchEP(user, epname):
            logError('CE ERROR! EP `%s` is not in the list of defined EPs: `%s`!' % \
                (str(epname), self.listEPs(user)) )
            return ''

        statuses = self.project.getFileStatusAll(user, epname, suite)
        return ','.join(statuses)


    @cherrypy.expose
    def setFileStatus(self, user, epname, file_id, new_status=10, time_elapsed=0.0):
        '''
        Set status for one file and write in log summary.\n
        Called from the Runner.
        '''
        if not self.searchEP(user, epname):
            logError('CE ERROR! EP `%s` is not in the list of defined EPs: `%s`!' % \
                (str(epname), self.listEPs(user)) )
            return False
        if new_status not in testStatus.values():
            logError("CE ERROR! Status value `%s` is not in the list of defined statuses: `%s`!" % \
                (str(new_status), str(testStatus.values())) )
            return False

        data = self.project.getFileInfo(user, file_id)
        filename = os.path.split(data['file'])[1]
        suite = data['suite']

        # Sets file status
        self.project.setFileInfo(user, epname, suite, file_id, 'status', new_status)
        reversed = dict((v,k) for k,v in testStatus.iteritems())
        status_str = reversed[new_status]

        # Get logSummary path from framework config
        logPath = self.project.getUserInfo(user, 'log_types')['logsummary']

        # Write all statuses in logs, because all files will be saved to database
        if status_str=='not executed': status_str='*NO EXEC*'
        else: status_str='*%s*' % status_str.upper()

        if new_status != STATUS_WORKING:
            # Inject information into File Classes
            now = datetime.datetime.today()

            self.project.setFileInfo(user, epname, suite, file_id, 'twister_tc_status',
                status_str.replace('*', ''))
            self.project.setFileInfo(user, epname, suite, file_id, 'twister_tc_crash_detected',
                data.get('twister_tc_crash_detected', 0))
            self.project.setFileInfo(user, epname, suite, file_id, 'twister_tc_time_elapsed',
                int(time_elapsed))
            self.project.setFileInfo(user, epname, suite, file_id, 'twister_tc_date_started',
                (now - datetime.timedelta(seconds=time_elapsed)).isoformat())
            self.project.setFileInfo(user, epname, suite, file_id, 'twister_tc_date_finished',
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
    def setFileStatusAll(self, user, epname, new_status):
        '''
        Reset file status for all files of one EP.\n
        Called from the Runner.
        '''
        return self.project.setFileStatusAll(user, epname, new_status)


# --------------------------------------------------------------------------------------------------
#           L O G S
# --------------------------------------------------------------------------------------------------


    @cherrypy.expose
    def getLogFile(self, user, read, fstart, filename):
        '''
        Called in the Java GUI to show the logs.
        '''
        if fstart is None:
            return '*ERROR!* Parameter FEND is NULL!'
        if not filename:
            return '*ERROR!* Parameter FILENAME is NULL!'

        filename = self.project.getUserInfo(user, 'logs_path') + os.sep + filename

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
    def logMessage(self, user, logType, logMessage):
        '''
        This function is exposed in all tests, all logs are centralized.
        '''
        logType = str(logType).lower()
        logTypes = self.project.getUserInfo(user, 'log_types')

        if logType == 'logcli' or logType == 'logsummary':
            logError('CE Warning! logCLI and logSummary are reserved and cannot be written into!')
            return False

        if not logType in logTypes:
            logError("CE ERROR! Log type `%s` is not in the list of defined types: `%s`!" % \
                (logType, logTypes))
            return False

        logPath = self.project.getUserInfo(user, 'log_types')[logType]

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
    def logLIVE(self, user, epname, logMessage):
        '''
        Writes CLI messages in a big log, so all output can be checked LIVE.\n
        Called from the EP.
        '''
        logFolder = self.project.getUserInfo(user, 'logs_path')
        logPath = logFolder + os.sep + epname + '_CLI.log'

        try:
            f = open(logPath, 'a')
        except:
            try:
                os.mkdir(logFolder)
                f = open(logPath, 'a')
            except:
                logError("CE ERROR! Log file `%s` cannot be written!" % logPath)
            return False

        f.write(binascii.a2b_base64(logMessage))
        f.close()
        return True


    @cherrypy.expose
    def findLog(self, user, epname, filename):
        '''
        Parses the log file of one EP and returns the log of one test file.
        '''
        logPath = self.project.getUserInfo(user, 'logs_path') + os.sep + epname + '_CLI.log'

        try:
            data = open(logPath, 'r').read()
        except:
            logError("CE ERROR! Log file `%s` cannot be read!" % logPath)
            return False

        try:
            log = re.search(('(?:.*>>> File `.*` returned `\w+`. <<<)(.+?>>> File `%s` returned `\w+`. <<<)' %
                             filename), data, re.S).group(1)
        except:
            try:
                log = re.search(('(?:.*===== ===== ===== ===== =====)(.+?>>> File `%s` returned `\w+`. <<<)' %
                                 filename), data, re.S).group(1)
            except:
                logError("CE ERROR! Cannot find file {0} in the log for {1}!".format(filename, epname))
                return '*no log*'

        return log.replace("'", "\\'")


    @cherrypy.expose
    def resetLogs(self, user):
        '''
        All logs defined in master config are erased.
        Log CLI is *magic*, there are more logs, one for each EP.\n
        Called from the Java GUI.
        '''
        logTypes = self.project.getUserInfo(user, 'log_types')
        vError = False
        logDebug('Cleaning log files...')

        for log in glob.glob(self.project.getUserInfo(user, 'logs_path') + os.sep + '*.log'):
            try: os.remove(log)
            except: pass

        for logType in logTypes:
            # For CLI
            if logType.lower()=='logcli':
                for epname in self.listEPs(user).split(','):
                    logPath = self.project.getUserInfo(user, 'logs_path') + os.sep + epname + '_CLI.log'
                    try:
                        open(logPath, 'w').close()
                        self.project.setFileOwner(user, logPath)
                    except:
                        logError("CE ERROR! Log file `%s` cannot be reset!" % logPath)
                        vError = True
                continue
            else:
                logPath = logTypes[logType]
            #
            try:
                open(logPath, 'w').close()
                self.project.setFileOwner(user, logPath)
            except:
                logError("CE ERROR! Log file `%s` cannot be reset!" % logPath)
                vError = True

        # On error, return IN-succes
        if vError:
            return False
        else:
            return True


    @cherrypy.expose
    def resetLog(self, user, logName):
        '''
        Resets one log.\n
        Called from the Java GUI.
        '''
        logPath = self.project.getUserInfo(user, 'logs_path') + os.sep + logName

        if not os.path.exists(logPath):
            logWarning('CE: The file does not exist! Nothing to reset!')
            return False

        try:
            open(logPath, 'w').close()
            logDebug('Cleaned log `%s`.' % logPath)
            return True
        except:
            logError("CE ERROR! Log file `%s` cannot be reset!" % logPath)
            return False

# Eof()
