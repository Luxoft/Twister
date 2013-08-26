
# File: CentralEngineClasses.py ; This file is part of Twister.

# version: 2.022

# Copyright (C) 2012-2013 , Luxoft

# Authors:
#    Adrian Toader <adtoader@luxoft.com>
#    Andrei Costachi <acostachi@luxoft.com>
#    Andrei Toma <atoma@luxoft.com>
#    Cristi Constantin <crconstantin@luxoft.com>
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

"""
Central Engine Class
********************

All functions from Central Engine are EXPOSED and can be accesed via XML-RPC.\n
The Central Engine and each EP have a status that can be: start/ stop/ paused.\n
Each test file has a status that can be: pending, working, pass, fail, skip, etc.\n
All the statuses are defined in "constants.py".\n
Central Engine role is to send files and libraries to User EPs, collect statistics and logs from
each file executed, send e-mail and save to database after each Project execution, run plug-ins.
"""
from __future__ import with_statement

import os
import sys
import re
import glob
import time
import datetime
import traceback
import random
import socket
import binascii
import tarfile
import xmlrpclib
import urlparse
import platform
import subprocess
import MySQLdb

import pickle
try: import simplejson as json
except: import json


if not sys.version.startswith('2.7'):
    print('Python version error! Central Engine must run on Python 2.7!')
    exit(1)

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print('$TWISTER_PATH environment variable is not set! Exiting!')
    exit(1)
sys.path.append(TWISTER_PATH)


import cherrypy
from cherrypy import _cptools

from CentralEngineOthers import Project
from ServiceManager    import ServiceManager
from CentralEngineRest import WebInterface
from ResourceAllocator import ResourceAllocator
from ReportingServer   import ReportingServer

from common.constants  import *
from common.helpers    import *
from common.tsclogging import *
from common.xmlparser  import *


# --------------------------------------------------------------------------------------------------
# # # #    C L A S S    C e n t r a l - E n g i n e    # # #
# --------------------------------------------------------------------------------------------------


class CentralEngine(_cptools.XMLRPCController):

    """
    *This class is the core of all operations.*
    """

    def __init__(self):

        # Build all Parsers + EP + Files structure
        try:
            srv_ver = open(TWISTER_PATH + '/server/version.txt').read().strip()
            srv_ver = 'version `{}`'.format(srv_ver)
        except: srv_ver = ''

        logDebug('CE: Starting Twister Server {}...'.format(srv_ver)) ; ti = time.clock()
        self.project = Project()
        logDebug('CE: Initialization took %.4f seconds.' % (time.clock()-ti))

        # User loggers
        self.loggers = {}

        self.manager = ServiceManager()
        self.rest = WebInterface(self, self.project)
        self.ra   = ResourceAllocator(self, self.project)
        self.report = ReportingServer(self, self.project)


    @cherrypy.expose
    def default(self, *vpath, **params):
        user_agent = cherrypy.request.headers['User-Agent'].lower()
        if 'xmlrpc' in user_agent or 'xml rpc' in user_agent:
            return super(CentralEngine, self).default(*vpath, **params)
        # If the connection is not XML-RPC, redirect to REST
        raise cherrypy.HTTPRedirect('/rest/' + '/'.join(vpath))


# --------------------------------------------------------------------------------------------------
#           H E L P E R   F U N C T I O N S
# --------------------------------------------------------------------------------------------------


    @cherrypy.expose
    def echo(self, msg):
        """
        Simple echo function, for testing connection.
        """
        if msg != 'ping':
            logInfo(':: %s' % str(msg))
        return 'CE reply: ' + msg


    @cherrypy.expose
    def getTwisterPath(self):
        '''
        Returns the Twister Path.
        '''
        global TWISTER_PATH
        return TWISTER_PATH


    @cherrypy.expose
    def getSysInfo(self):
        '''
        Returns some system information.
        '''
        system = platform.machine() +' '+ platform.system() +', '+ ' '.join(platform.linux_distribution())
        python = '.'.join([str(v) for v in sys.version_info])
        return '{}\nPython {}'.format(system.strip(), python)


    @cherrypy.expose
    def getLogsPath(self, user):
        '''
        Returns the path to Logs files.
        '''
        return self.project.getUserInfo(user, 'logs_path')


    @cherrypy.expose
    def encryptText(self, text):
        """
        Encrypt a piece of text, using AES.\n
        This function is called from the Java GUI.
        """
        if not text: return ''
        return self.project.encryptText(text)


    @cherrypy.expose
    def decryptText(self, text):
        """
        Decrypt a piece of text, using AES.\n
        This function is called from the Java GUI.
        """
        if not text: return ''
        return self.project.decryptText(text)


    @cherrypy.expose
    def runUserScript(self, script_path):
        """
        Executes a script.
        Returns a string containing the text printed by the script.\n
        This function is called from the Java GUI.
        """
        return execScript(script_path)


#


    @cherrypy.expose
    def serviceManagerCommand(self, command, name='', *args, **kwargs):
        """
        Send commands to Service Manager.\n
        Valid commands are: list, start, stop, status, get config, save config, get log.
        """
        # Check the username from CherryPy connection
        cherry_roles = self.project._checkUser()
        if not cherry_roles: return False
        if 'CHANGE_SERVICES' not in cherry_roles['roles']:
            logDebug('Privileges ERROR! Username `{user}` cannot use Service Manager!'.format(**cherry_roles))
            return False
        return self.manager.sendCommand(command, name, args, kwargs)


    @cherrypy.expose
    def usersAndGroupsManager(self, cmd, name='', *args, **kwargs):
        """
        Manage users, groups and permissions.
        """
        return self.project.usersAndGroupsManager(cmd, name, args, kwargs)


    @cherrypy.expose
    def runDBSelect(self, user, field_id):
        """
        Selects from database.
        This function is called from the Java GUI.
        """
        # Get the path to DB.XML
        db_file = self.project.getUserInfo(user, 'db_config')
        if not db_file:
            errMessage = 'Null DB.XML file for user `{}`! Nothing to do!'.format(user)
            logError(errMessage)
            return errMessage

        # Database parser, fields, queries
        dbparser = DBParser(db_file)
        query = dbparser.getQuery(field_id)
        db_config = dbparser.db_config
        del dbparser

        # Decode database password
        db_password = self.project.decryptText( db_config.get('password') )
        if not db_password:
            errMessage = 'Cannot decrypt the database password!'
            logError(errMessage)
            return errMessage

        try:
            conn = MySQLdb.connect(host=db_config.get('server'), db=db_config.get('database'),
                user=db_config.get('user'), passwd=db_password)
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
    def sendMail(self, user, force=False):
        """
        Send e-mail after the suites are run.\n
        Server must be in the form `adress:port`.\n
        Username and password are used for authentication.\n
        This function is called every time the Central Engine stops.
        """

        try:
            ret = self.project.sendMail(user, force)
            return ret
        except Exception as e:
            trace = traceback.format_exc()[34:].strip()
            logError('E-mail: Sending e-mail exception `{}` !'.format(trace))
            return False


    @cherrypy.expose
    def commitToDatabase(self, user):
        """
        For each EP, for each Suite and each File, the results of the tests are saved to database,
        exactly as the user defined them in Database.XML.\n
        This function is called from the Java GUI, or from an EP.
        """

        logDebug('CE: Preparing to save into database...')
        time.sleep(3)
        ret = self.project.saveToDatabase(user)
        if ret:
            logDebug('CE: Saving to database was successful!')
        else:
            logDebug('CE: Could not save to database!')
        return ret


# --------------------------------------------------------------------------------------------------
#           S E T T I N G S
# --------------------------------------------------------------------------------------------------


    @cherrypy.expose
    def listSettings(self, user, config='', x_filter=''):
        """
        List all available settings, for 1 config of a user.
        """
        return self.project.listSettings(user, config, x_filter)


    @cherrypy.expose
    def getSettingsValue(self, user, config, key):
        """
        Fetch a value from 1 config of a user.
        """
        return self.project.getSettingsValue(user, config, key)


    @cherrypy.expose
    def setSettingsValue(self, user, config, key, value):
        """
        Set a value for a key in the config of a user.
        """
        return self.project.setSettingsValue(user, config, key, value)


    @cherrypy.expose
    def delSettingsKey(self, user, config, key, index=0):
        """
        Del a key from the config of a user.
        """
        return self.project.delSettingsKey(user, config, key, index)


# --------------------------------------------------------------------------------------------------
#           E P ,   S U I T E   AND   F I L E   V A R I A B L E S
# --------------------------------------------------------------------------------------------------


    @cherrypy.expose
    def listUsers(self, active=False):
        """
        Function called from the CLI,
        to list the users that are using Twister.
        """
        data = self.project.listUsers(active)
        return data


    @cherrypy.expose
    def getUserVariable(self, user, variable):
        """
        Function called from the Execution Process,
        to get information that is available only here, or are hard to get.
        """

        data = self.project.getUserInfo(user, variable)
        if data is None: data = False
        return data


    @cherrypy.expose
    def setUserVariable(self, user, key, variable):
        """
        Function called from the Execution Process,
        to set information that is available only here, or are hard to get.
        """

        return self.project.setUserInfo(user, key, variable)


    @cherrypy.expose
    def searchEP(self, user, epname):
        """
        Search one EP and return True or False.
        """
        epDict = self.project.getUserInfo(user, 'eps')
        return epname in epDict


    @cherrypy.expose
    def listEPs(self, user):
        """
        Returns all EPs for current user.
        """
        epList = self.project.getUserInfo(user, 'eps').keys()
        return ','.join(epList)


    @cherrypy.expose
    def getEpVariable(self, user, epname, variable, compress=False):
        """
        This function is called from the Execution Process,
        to get information that is available only here, or are hard to get:

        - what the user selected in the Java GUI (release, build, comments, etc)
        - the name of the suite, the test files, etc.
        """

        data = self.project.getEpInfo(user, epname).get(variable, False)
        if compress:
            return pickle.dumps(data)
        else:
            return data


    @cherrypy.expose
    def setEpVariable(self, user, epname, variable, value):
        """
        This function is called from the Execution Process,
        to inject values inside the EP classes.\n
        The values can saved in the Database, when commiting.\n
        Eg: the OS, the IP, or other information can be added this way.
        """

        return self.project.setEpInfo(user, epname, variable, value)


    @cherrypy.expose
    def listSuites(self, user, epname):
        """
        Returns all Suites for one EP from current user.
        """
        if not self.searchEP(user, epname):
            logError('CE ERROR! EP `%s` is not in the list of defined EPs: `%s`!' %\
                     (str(epname), self.listEPs(user)) )
            return False

        suiteList   = [str(k)+':'+v['name'] for k, v in self.project.getEpInfo(user, epname)['suites'].items()]
        return ','.join(suiteList)


    @cherrypy.expose
    def getSuiteVariable(self, user, epname, suite, variable):
        """
        Function called from the Execution Process,
        to get information that is available only here, or are hard to get.
        """

        data = self.project.getSuiteInfo(user, epname, suite)
        if not data: return False
        return data.get(variable, False)


    @cherrypy.expose
    def getFileVariable(self, user, epname, file_id, variable):
        """
        Get information about a test file: dependencies, runnable, status, etc.
        """

        data = self.project.getFileInfo(user, epname, file_id)
        if not data: return False
        return data.get(variable, False)


    @cherrypy.expose
    def setFileVariable(self, user, epname, filename, variable, value):
        """
        Set extra information for a Filename, like Crash detected, OS, IP.\n
        Can be called from the Runner.\n
        This change only happens in the memory structure and it is reset every time
        Central Engine is start. If you need to make a persistent change, use setPersistentFile.
        """

        return self.project.setFileInfo(user, epname, filename, variable, value)


    @cherrypy.expose
    def setStartedBy(self, user, name):
        """
        Remember the user that started the Central Engine.\n
        Called from the Java GUI.
        """

        logDebug('CE: Started by user name `%s`.'  % str(name))
        self.project.setUserInfo(user, 'started_by', str(name))
        return 1


    @cherrypy.expose
    def getGlobalVariable(self, user, var_path):
        """
        Sending a global variable, using a path.
        """
        return self.project.getGlobalVariable(user, var_path)


    @cherrypy.expose
    def setGlobalVariable(self, user, var_path, value):
        """
        Set a global variable path, for a user.\n
        The change is not persistent.
        """
        return self.project.setGlobalVariable(user, var_path, value)


# --------------------------------------------------------------------------------------------------
#           C L I E N T   C O N T R O L
# --------------------------------------------------------------------------------------------------


    def _getClientEpProxy(self, user, epname):
        """ Helper function. """

        # Check if epname is known and registered
        userClientsInfo = self.project.getUserInfo(user, 'clients')
        if not userClientsInfo:
            return False
        else:
            userClientsInfo = json.loads(userClientsInfo)

        userClientsInfoEPs = list()
        for cl in userClientsInfo:
            userClientsInfoEPs += userClientsInfo[cl]
        if not self.searchEP(user, epname) or not epname in userClientsInfoEPs:
            logError('Error: Unknown EP : `{}`.'.format(epname))
            return False

        # Get proxy address
        for cl in userClientsInfo:
            if epname in userClientsInfo[cl]:
                return cl

        logError('Error: Unknown proxy for EP : `{}`.'.format(epname))
        return False


    @cherrypy.expose
    def registerClient(self, user, clients):
        """ Register client. """

        clients = json.loads(clients)
        _clients = {}

        for client in clients:
            if client.split(':')[0]:
                addr = client.split(':')[0]
            else:
                addr = cherrypy.request.headers['Remote-Addr']
            _clients.update([('{}:{}'.format(addr,
                                      client.split(':')[1]), clients[client]), ])
        clients = json.dumps(_clients)

        self.setUserVariable(user, 'clients', clients)
        logDebug('Registered client manager for user\n\t`{}` -> {}.'.format(user, clients))
        return True


    @cherrypy.expose
    def startEP(self, user, epname):
        """ Start EP for client. """

        _proxy = self._getClientEpProxy(user, epname)
        if not _proxy:
            logDebug('Cannot start `{}` for user `{}` ! The Client Manager is not started !'.format(epname, user))
            return False

        proxy = xmlrpclib.ServerProxy('http://{pr}/twisterclient/'.format(pr=_proxy))
        ip, port = _proxy.split(':')

        try:
            socket.create_connection((ip, int(port)), 2)
            logDebug('Trying to start `{} {}`.'.format(user, epname))
            return proxy.startEP(epname)
        except Exception as e:
            trace = traceback.format_exc()[34:].strip()
            logError('Error: Start EP error: {}'.format(trace))
            return False


    @cherrypy.expose
    def stopEP(self, user, epname):
        """ Stop EP for client. """

        _proxy = self._getClientEpProxy(user, epname)
        if not _proxy:
            logDebug('Cannot stop `{}` for user `{}` ! The Client Manager is not started !'.format(epname, user))
            return False

        proxy = xmlrpclib.ServerProxy('http://{pr}/twisterclient/'.format(pr=_proxy))
        ip, port = _proxy.split(':')

        try:
            socket.create_connection((ip, int(port)), 2)
            logWarning('Trying to stop `{} {}`.'.format(user, epname))
            return proxy.stopEP(epname)
        except Exception as e:
            trace = traceback.format_exc()[34:].strip()
            logError('Error: Stop EP error: {}'.format(trace))
            return False


    @cherrypy.expose
    def restartEP(self, user, epname):
        """ Restart EP for client. """

        _proxy = self._getClientEpProxy(user, epname)
        if not _proxy:
            logDebug('Cannot restart `{}` for user `{}` ! The Client Manager is not started !'.format(epname, user))
            return False

        proxy = xmlrpclib.ServerProxy('http://{pr}/twisterclient/'.format(pr=_proxy))
        ip, port = _proxy.split(':')

        try:
            socket.create_connection((ip, int(port)), 2)
            logWarning('Trying to restart `{} {}`.'.format(user, epname))
            return proxy.restartEP(epname)
        except Exception as e:
            trace = traceback.format_exc()[34:].strip()
            logError('Error: Restart EP error: {}'.format(trace))
            return False


    @cherrypy.expose
    def queueFile(self, user, suite, fname):
        """
        Queue a file at the end of a suite, during runtime.
        If there are more suites with the same name, the first one is used.\n
        This function writes in TestSuites.XML file, so the change is persistent.
        """
        return self.project.queueFile(user, suite, fname)


    @cherrypy.expose
    def deQueueFiles(self, user, data):
        """
        Remove a file from the files queue.
        """
        return self.project.deQueueFiles(user, data)


# --------------------------------------------------------------------------------------------------
#           C R E A T E   P E R S I S T E N T   S U I T E S
# --------------------------------------------------------------------------------------------------


    @cherrypy.expose
    def setPersistentSuite(self, user, suite, info={}, order=-1):
        """
        Create a new suite, using the INFO, at the position specified.\n
        This function writes in TestSuites.XML file.\n
        The changes will be available at the next START.
        """
        return self.project.setPersistentSuite(user, suite, info, order)


    @cherrypy.expose
    def delPersistentSuite(self, user, suite):
        """
        Delete an XML suite, using a name ; if there are more suites with the same name,
        only the first one is deleted.\n
        This function writes in TestSuites.XML file.
        """
        return self.project.delPersistentSuite(user, suite)


    @cherrypy.expose
    def setPersistentFile(self, user, suite, fname, info={}, order=-1):
        """
        Create a new file in a suite, using the INFO, at the position specified.\n
        This function writes in TestSuites.XML file.\n
        The changes will be available at the next START.
        """
        return self.project.setPersistentFile(user, suite, fname, info, order)


    @cherrypy.expose
    def delPersistentFile(self, user, suite, fname):
        """
        Delete an XML file from a suite, using a name ; if there are more files
        with the same name, only the first one is deleted.\n
        This function writes in TestSuites.XML file.
        """
        return self.project.delPersistentFile(user, suite, fname)


# --------------------------------------------------------------------------------------------------
#           E X E C U T I O N   S T A T U S
# --------------------------------------------------------------------------------------------------


    @cherrypy.expose
    def resetProject(self, user):
        """
        Reset project for user.
        """
        twister_cache = userHome(user) + '/twister/.twister_cache'
        setFileOwner(user, twister_cache)
        return self.project.reset(user)


    @cherrypy.expose
    def getExecStatus(self, user, epname):
        """
        Return execution status for one EP. (stopped, paused, running, invalid)\n
        Called from the EP.
        """
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
        """
        Return execution status for all EPs. (stopped, paused, running, invalid)\n
        Called from the Java GUI.
        """
        # If this is a temporary run, return the statuses of the backup user!
        user_agent = cherrypy.request.headers['User-Agent'].lower()
        if 'xml rpc' in user_agent and (user+'_old') in self.project.users:
            user += '_old'

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
        """
        Set execution status for one EP. (0, 1, 2, or 3)\n
        Returns a string (stopped, paused, running).\n
        Called from the EP.
        """
        # Check the username from CherryPy connection
        cherry_roles = self.project._checkUser()
        if not cherry_roles:
            return False
        if not 'RUN_TESTS' in cherry_roles['roles']:
            logDebug('Privileges ERROR! Username `{user}` cannot change EP status!'.format(**cherry_roles))
            return False

        if not self.searchEP(user, epname):
            logError('CE ERROR! EP `{}` is not in the list of defined EPs: `{}`!'
                     ''.format(epname, self.listEPs(user)) )
            return False
        if new_status not in execStatus.values():
            logError("CE ERROR! Status value `{}` is not in the list of defined statuses: `{}`!"
                     "".format(new_status, execStatus.values()) )
            return False

        # Status resume => start running
        if new_status == STATUS_RESUME:
            new_status = STATUS_RUNNING

        ret = self.project.setEpInfo(user, epname, 'status', new_status)
        reversed = dict((v,k) for k,v in execStatus.iteritems())

        if ret:
            if msg:
                logDebug('CE: Status changed for `{} {}` - {} (from `{}`).\n\tMessage: `{}`.'.format(
                    user, epname, reversed[new_status], cherrypy.request.headers['Remote-Addr'], msg))
            else:
                logDebug('CE: Status changed for `{} {}` - {} (from `{}`).'.format(
                    user, epname, reversed[new_status], cherrypy.request.headers['Remote-Addr']))
        else:
            logError('CE ERROR! Cannot change status for `{} {}` !'.format(user, epname))

        # Send start/ stop command to EP !
        if new_status == STATUS_RUNNING:
            self.startEP(user, epname)
        elif new_status == STATUS_STOP:
            self.stopEP(user, epname)

        # If all Stations are stopped, the status for current user is also stop!
        # This is important, so that in the Java GUI, the buttons will change to [Play | Stop]
        if not sum([self.project.getEpInfo(user, ep).get('status', 8) for ep in self.project.parsers[user].getActiveEps()]):

            # If User status was not Stop
            if self.project.getUserInfo(user, 'status'):

                self.project.setUserInfo(user, 'status', STATUS_STOP)

                logDebug('CE: All processes stopped for user `{}`! General status changed to STOP.\n'.format(user))

                # If this run is Not temporary
                if not (user + '_old' in self.project.users):
                    # On Central Engine stop, send e-mail
                    self.sendMail(user)

                    # Execute "Post Script"
                    script_post = self.project.getUserInfo(user, 'script_post')
                    script_mandatory = self.project.getUserInfo(user, 'script_mandatory')
                    save_to_db = True
                    if script_post:
                        result = execScript(script_post)
                        if result: logDebug('Post Script executed!\n"{}"\n'.format(result))
                        elif script_mandatory:
                            logError('CE: Post Script failed and script is mandatory! Will not save the results into database!')
                            save_to_db = False

                    # On Central Engine stop, save to database
                    db_auto_save = self.project.getUserInfo(user, 'db_auto_save')
                    if db_auto_save and save_to_db: self.commitToDatabase(user)

                    # Find the log process for this User and kill it
                    logProc = self.loggers[user].get('proc')

                    if logProc:
                        try:
                            subprocess.call('kill $(pgrep -P %i)' % logProc.pid, shell=True)
                            logProc.terminate()
                            logProc.wait()
                            logDebug('Terminated log server PID `{}`, for user `{}`.'.format(logProc.pid, user))
                        except Exception as e:
                            trace = traceback.format_exc()[33:].strip()
                            logWarning('Cannot stop Log Server PID `{}`, for user `{}`! '\
                                       'Exception `{}`!'.format(logProc.pid, user, trace))

                    # Execute "onStop" for all plugins!
                    parser = PluginParser(user)
                    plugins = parser.getPlugins()
                    for pname in plugins:
                        plugin = self._buildPlugin(user, pname,  {'ce_stop': 'automatic'})
                        try:
                            plugin.onStop()
                        except Exception as e:
                            trace = traceback.format_exc()[33:].strip()
                            logWarning('Error on running plugin `{} onStop` - Exception: `{}`!'.format(pname, trace))
                    del parser, plugins

                    # Cycle all files to change the PENDING status to NOT_EXEC
                    eps_pointer = self.project.users[user]['eps']
                    statuses_changed = 0

                    # All files, for current EP
                    files = eps_pointer[epname]['suites'].getFiles()
                    for file_id in files:
                        current_status = self.project.getFileInfo(user, epname, file_id).get('status', -1)
                        # Change the files with PENDING status, to NOT_EXEC
                        if current_status in [STATUS_PENDING, -1]:
                            self.project.setFileInfo(user, epname, file_id, 'status', STATUS_NOT_EXEC)
                            statuses_changed += 1

                    if statuses_changed:
                        logDebug('Changed `{}` file statuses from Pending to Not executed.'.format(statuses_changed))


        return reversed[new_status]


    @cherrypy.expose
    def setExecStatusAll(self, user, new_status, msg=''):
        """
        Set execution status for all EPs. (STATUS_STOP, STATUS_PAUSED, STATUS_RUNNING).\n
        Returns a string (stopped, paused, running).\n
        The `message` parameter can explain why the status has changed.\n
        Both CE and EP have a status.
        """
        # Check the username from CherryPy connection
        cherry_roles = self.project._checkUser()
        if not cherry_roles:
            return False
        if not 'RUN_TESTS' in cherry_roles['roles']:
            logDebug('Privileges ERROR! Username `{user}` cannot change exec status!'.format(**cherry_roles))
            return False

        if new_status not in execStatus.values():
            logError("CE ERROR! Status value `{}` is not in the list of defined statuses: `{}`!"
                     "".format(new_status, execStatus.values()) )
            return False

        reversed = dict((v,k) for k,v in execStatus.iteritems())

        # If this is a Temporary user
        user_agent = cherrypy.request.headers['User-Agent'].lower()
        if 'xml rpc' in user_agent and (user+'_old') in self.project.users:
            if msg.lower() != 'kill' and new_status != STATUS_STOP:
                return '*ERROR*! Cannot change status while running temporary!'
            else:
                # Update status for User
                self.project.setUserInfo(user, 'status', STATUS_STOP)

                # Update status for all active EPs
                active_eps = self.project.parsers[user].getActiveEps()
                for epname in active_eps:
                    self.project.setEpInfo(user, epname, 'status', STATUS_STOP)

                if msg:
                    logDebug("CE: Status chang for TEMP `%s %s` -> %s. Message: `%s`.\n" % (user, active_eps, reversed[STATUS_STOP], str(msg)))
                else:
                    logDebug("CE: Status chang for TEMP `%s %s` -> %s.\n" % (user, active_eps, reversed[STATUS_STOP]))
                return reversed[STATUS_STOP]

        # Status resume => start running. The logs must not reset on resume
        if new_status == STATUS_RESUME:
            new_status = STATUS_RUNNING

        # Return the current status, or 8 = INVALID
        executionStatus = self.project.getUserInfo(user, 'status') or 8

        # Re-initialize the Master XML and Reset all logs on fresh start!
        # This will always happen when the START button is pressed, if CE is stopped
        if (executionStatus == STATUS_STOP or executionStatus == STATUS_INVALID) and new_status == STATUS_RUNNING:

            # If the Msg contains 2 paths, separated by comma
            if msg and len(msg.split(',')) == 2:
                path1 = msg.split(',')[0]
                path2 = msg.split(',')[1]
                if os.path.isfile(path1) and os.path.isfile(path2):
                    logDebug('CE: Using custom XML files: `{}` and `{}`.'.format(path1, path2))
                    self.project.reset(user, path1, path2)
                    msg = ''

            # Or if the Msg is a path to an existing file...
            elif msg and os.path.isfile(msg):
                data = open(msg).read().strip()
                # If the file is XML, send it to project reset function
                if data[0] == '<' and data [-1] == '>':
                    logDebug('CE: Using custom XML file: `{}`...'.format(msg))
                    self.project.reset(user, msg)
                    msg = ''
                else:
                    logDebug('CE: You are probably trying to use file `{}` as config file, but it\'s not a valid XML!'.format(msg))
                    self.project.reset(user)
                del data

            else:
                self.project.reset(user)

            self.resetLogs(user)

            # User start time and elapsed time
            self.project.setUserInfo(user, 'start_time', datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            self.project.setUserInfo(user, 'elapsed_time', 0)

            # Execute "Pre Script"
            script_pre = self.project.getUserInfo(user, 'script_pre')
            script_mandatory = self.project.getUserInfo(user, 'script_mandatory')
            if script_pre:
                result = execScript(script_pre)
                if result: logDebug('Pre Script executed! {}'.format(result))
                elif script_mandatory:
                    logError('CE: Pre Script failed and script is mandatory! The project failed!')
                    return reversed[STATUS_STOP]

            # Execute "onStart" for all plugins!
            parser = PluginParser(user)
            plugins = parser.getPlugins()
            for pname in plugins:
                plugin = self._buildPlugin(user, pname)
                try:
                    plugin.onStart()
                except Exception as e:
                    trace = traceback.format_exc()[34:].strip()
                    logWarning('Error on running plugin `{} onStop` - Exception: `{}`!'.format(pname, trace))
            del parser, plugins

            # Start all active EPs !
            active_eps = self.project.parsers[user].getActiveEps()
            for epname in active_eps:
                self.startEP(user, epname)

        # If the engine is running, or paused and it received STOP from the user...
        elif (executionStatus == STATUS_RUNNING or executionStatus == STATUS_PAUSED) and new_status == STATUS_STOP:

            # Execute "Post Script"
            script_post = self.project.getUserInfo(user, 'script_post')
            script_mandatory = self.project.getUserInfo(user, 'script_mandatory')
            if script_post:
                result = execScript(script_post)
                if result: logDebug('Post Script executed!\n"{}"\n'.format(result))
                elif script_mandatory:
                    logError('CE: Post Script failed!')

            # Execute "onStop" for all plugins... ?
            parser = PluginParser(user)
            plugins = parser.getPlugins()
            for pname in plugins:
                plugin = self._buildPlugin(user, pname, {'ce_stop': 'manual'})
                try:
                    plugin.onStop()
                except Exception as e:
                    trace = traceback.format_exc()[34:].strip()
                    logWarning('Error on running plugin `{} onStop` - Exception: `{}`!'.format(pname, trace))
            del parser, plugins

            # Cycle all active EPs to: STOP them and to change the PENDING status to NOT_EXEC
            active_eps = self.project.parsers[user].getActiveEps()
            eps_pointer = self.project.users[user]['eps']
            statuses_changed = 0

            for epname in active_eps:
                # All files, for current EP
                files = eps_pointer[epname]['suites'].getFiles()
                for file_id in files:
                    current_status = self.project.getFileInfo(user, epname, file_id).get('status', -1)
                    # Change the files with PENDING status, to NOT_EXEC
                    if current_status in [STATUS_PENDING, -1]:
                        self.project.setFileInfo(user, epname, file_id, 'status', STATUS_NOT_EXEC)
                        statuses_changed += 1
                # Send STOP to EP Manager
                self.stopEP(user, epname)

            if statuses_changed:
                logDebug('Changed `{}` file statuses from Pending to Not executed.'.format(statuses_changed))


        # Update status for User
        self.project.setUserInfo(user, 'status', new_status)

        # Update status for all active EPs
        active_eps = self.project.parsers[user].getActiveEps()
        for epname in active_eps:
            self.project.setEpInfo(user, epname, 'status', new_status)

        reversed = dict((v,k) for k,v in execStatus.iteritems())


        if msg and msg != ',':
            logDebug('CE: Status changed for `{} {}` - {} (from `{}`).\n\tMessage: `{}`.'.format(
                user, active_eps, reversed[new_status], cherrypy.request.headers['Remote-Addr'], msg))
        else:
            logDebug('CE: Status changed for `{} {}` - {} (from `{}`).'.format(
                user, active_eps, reversed[new_status], cherrypy.request.headers['Remote-Addr']))

        return reversed[new_status]


# --------------------------------------------------------------------------------------------------
#           T E S T   F I L E   S T A T U S E S
# --------------------------------------------------------------------------------------------------


    @cherrypy.expose
    def getFileStatusAll(self, user, epname=None, suite=None):
        """
        Returns a list with all statuses, for all files, in order.\n
        The status of one file can be obtained with get File Variable.\n
        Called from the Java GUI.
        """
        if epname and not self.searchEP(user, epname):
            logError('CE ERROR! EP `%s` is not in the list of defined EPs: `%s`!' % \
                (str(epname), self.listEPs(user)) )
            return ''

        # If this is a temporary run, return the statuses of the backup user!
        user_agent = cherrypy.request.headers['User-Agent'].lower()
        if 'xml rpc' in user_agent and (user+'_old') in self.project.users:
            statuses = self.project.getFileStatusAll(user + '_old', epname, suite)
            return ','.join(statuses)

        statuses = self.project.getFileStatusAll(user, epname, suite)
        return ','.join(statuses)


    @cherrypy.expose
    def setFileStatus(self, user, epname, file_id, new_status=10, time_elapsed=0.0):
        """
        Set status for one file and write in log summary.\n
        Called from the Runner.
        """
        if not self.searchEP(user, epname):
            logError('CE ERROR! EP `%s` is not in the list of defined EPs: `%s`!' % \
                (str(epname), self.listEPs(user)) )
            return False
        if new_status not in testStatus.values():
            logError("CE ERROR! Status value `%s` is not in the list of defined statuses: `%s`!" % \
                (str(new_status), str(testStatus.values())) )
            return False

        data = self.project.getFileInfo(user, epname, file_id)
        if not data:
            logDebug('CE ERROR! Invalid File ID `{}` !'.format(file_id))
            return False

        filename = os.path.split(data['file'])[1]
        suite = data['suite']

        # Sets file status
        self.project.setFileInfo(user, epname, file_id, 'status', new_status)
        reversed = dict((v,k) for k,v in testStatus.iteritems())
        status_str = reversed[new_status]

        # Get logSummary path from framework config
        logPath = self.project.getUserInfo(user, 'log_types')['logSummary']

        # Write all statuses in logs, because all files will be saved to database
        if status_str=='not executed': status_str='*NO EXEC*'
        else: status_str='*%s*' % status_str.upper()

        if new_status != STATUS_WORKING:

            # Inject information into Files. This will be used when saving into database.
            now = datetime.datetime.today()

            self.project.setFileInfo(user, epname, file_id, 'twister_tc_status', status_str.replace('*', ''))
            self.project.setFileInfo(user, epname, file_id, 'twister_tc_crash_detected',
                                    data.get('twister_tc_crash_detected', 0))
            self.project.setFileInfo(user, epname, file_id, 'twister_tc_time_elapsed',   int(time_elapsed))
            self.project.setFileInfo(user, epname, file_id, 'twister_tc_date_started',
                                    (now - datetime.timedelta(seconds=time_elapsed)).isoformat())
            self.project.setFileInfo(user, epname, file_id, 'twister_tc_date_finished',  (now.isoformat()))
            suite_name = self.project.getSuiteInfo(user, epname, suite).get('name')

            try:
                with open(logPath, 'a') as status_file:
                    status_file.write(' {ep}::{suite}::{file} | {status} | {elapsed} | {date}\n'.format(
                        ep = epname.center(9), suite = suite_name.center(9), file = filename.center(28),
                        status = status_str.center(11),
                        elapsed = ('%.2fs' % time_elapsed).center(10),
                        date = now.strftime('%a %b %d, %H:%M:%S')))
            except:
                logError('Summary log file `{}` cannot be written! User `{}` won\'t see any '\
                         'statistics!'.format(logPath, user))

        # Return string
        return status_str


    @cherrypy.expose
    def setFileStatusAll(self, user, epname, new_status):
        """
        Reset file status for all files of one EP.\n
        Called from the Runner.
        """
        return self.project.setFileStatusAll(user, epname, new_status)


# --------------------------------------------------------------------------------------------------
#           L I B R A R Y   AND   T E S T   S U I T E   F I L E S
# --------------------------------------------------------------------------------------------------


    def _buildPlugin(self, user, plugin, extra_data={}):
        """
        Parses the list of plugins and creates an instance of the requested plugin.
        All the data
        """

        # The pointer to the plugin = User name and Plugin name
        key = user +' '+ plugin

        if key in self.project.plugins:
            plugin = self.project.plugins.get(key)
            return plugin

        # If the plugin is not initialised
        parser = PluginParser(user)
        pdict = parser.getPlugins().get(plugin)
        if not pdict:
            logError('CE ERROR: Cannot find plugin `%s`!' % plugin)
            return False
        del parser

        data = dict(self.project.getUserInfo(user))
        data.update(pdict)
        data.update(extra_data)
        data['ce'] = self
        del data['eps']
        del data['status']
        del data['plugin']

        plugin = pdict['plugin'](user, data)
        self.project.plugins[key] = plugin
        return plugin


    @cherrypy.expose
    def listPlugins(self, user):

        parser = PluginParser(user)
        pluginsList = parser.getPlugins()

        return pluginsList.keys()


    @cherrypy.expose
    def runPlugin(self, user, plugin, args):

        # If argument is a string
        if type(args) == type(str()):
            try:
                args = urlparse.parse_qs(args)
            except:
                msg = 'CE ERROR: Cannot run plugin `%s` with arguments `%s`!' % (plugin, args)
                logError(msg)
                return msg
        # If argument is a valid dict, pass
        elif type(args) == type(dict()):
            if not 'command' in args:
                return 'CE ERROR: Invalid dictionary for plugin `%s` : %s !' % (plugin, args)
        else:
            return 'CE ERROR: Invalid type of argument for plugin `%s` : %s !' % (plugin, type(args))

        plugin_p = self._buildPlugin(user, plugin)

        if not plugin_p:
            msg = 'CE ERROR: Plugin `{0}` does not exist for user `{1}`!'.format(plugin, user)
            logError(msg)
            return msg
        # else:
        #    logDebug('Running plugin:: `{0}` ; user `{1}` ; {2}'.format(plugin, user, args))

        try:
            return plugin_p.run(args)
        except Exception as e:
            trace = traceback.format_exc()[34:].strip()
            logError('CE ERROR: Plugin `{}`, ran with arguments `{}` and returned EXCEPTION: `{}`!'\
                     .format(plugin, args, trace))
            return 'Error on running plugin `{}` - Exception: `{}`!'.format(plugin, e)


    @cherrypy.expose
    def runTemporary(self, user, files_xml):
        """
        This function allows the Central Engine to run a temporary Test-Suite XML file
        that contains any valid combination of suites and files.
        The temporary run does not affect the normal suites and files.
        The results are Not saved to database and No report is sent on e-mail.
        """

        # Cannot run temporary more than once
        if user + '_old' in self.project.users:
            logError('CE ERROR: User `{0}` is already running temporary!'.format(user))
            return '*ERROR!* User `{0}` is already running temporary!'.format(user)
        # If the user is already running something, DON'T run temporary
        if self.project.getUserInfo(user, 'status'):
            logError('*ERROR!* User `{0}` must be stopped, before running temporary!'.format(user))
            return '*ERROR!* User `{0}` must be stopped, before running temporary!'.format(user)

        # Backup all username data, under a different name
        self.project.renameUser(user, user + '_old')
        # Create a temporary user
        self.project.createUser(user, base_config='', files_config=files_xml)

        # Update status for temporary user
        self.project.setUserInfo(user, 'status', STATUS_RUNNING)
        # Update status for all active EPs
        active_eps = self.project.parsers[user].getActiveEps()
        for epname in active_eps:
            self.project.setEpInfo(user, epname, 'status', STATUS_RUNNING)

        i = 0
        while self.project.getUserInfo(user, 'status') == STATUS_RUNNING:
            if not i:
                logWarning('Temporary user `{}` is running on EP list `{}`...'.format(user, active_eps))
            i += 1
            if i == 12: i = 0
            time.sleep(1)

        # Delete temporary user
        self.project.deleteUser(user)
        # Restore previous user
        self.project.renameUser(user + '_old', user)

        return True


    @cherrypy.expose
    def getLibrariesList(self, user=''):
        """
        Returns the list of exposed libraries, from CE libraries folder.\n
        This list will be used to syncronize the libs on all EP computers.\n
        Called from the Runner.
        """
        global TWISTER_PATH
        libs_path = (TWISTER_PATH + '/lib/').replace('//', '/')
        user_path = ''
        if self.project.getUserInfo(user, 'libs_path'):
            user_path = self.project.getUserInfo(user, 'libs_path') + os.sep
        if user_path == '/':
            user_path = ''

        glob_libs = []
        user_libs = []

        # All libraries for user
        if user:
            # If `libraries` is empty, will default to ALL libraries
            tmp_libs = self.project.getUserInfo(user, 'libraries') or ''
            glob_libs = [x.strip() for x in tmp_libs.split(';')] if tmp_libs else []
            del tmp_libs

        # All Python source files from Libraries folder AND all library folders
        if not glob_libs:
            glob_libs = [d for d in os.listdir(libs_path) if \
                    ( os.path.isfile(libs_path + d) and \
                    '__init__.py' not in d and \
                    os.path.splitext(d)[1] in ['.py', '.zip']) or \
                    os.path.isdir(libs_path + d) ]

            if user_path and os.path.isdir(user_path):
                user_libs = [d for d in os.listdir(user_path) if \
                        ( os.path.isfile(user_path + d) and \
                        '__init__.py' not in d and \
                        os.path.splitext(d)[1] in ['.py', '.zip']) or \
                        os.path.isdir(user_path + d) ]

        return sorted( list(set(glob_libs + user_libs)) )


    @cherrypy.expose
    def downloadLibrary(self, user, name):
        """
        Sends required library to EP, to be syncronized.\n
        The library can be global for all users, or per user.\n
        Called from the Runner.
        """
        global TWISTER_PATH

        lib_path = (TWISTER_PATH + '/lib/' + name).replace('//', '/')
        if self.project.getUserInfo(user, 'libs_path'):
            user_lib = self.project.getUserInfo(user, 'libs_path') + os.sep + name
        else:
            user_lib = ''

        # If the requested library is in the second path (user path)
        if os.path.exists(user_lib):
            final_path = user_lib
        # If the requested library is in the main path (global path)
        elif os.path.exists(lib_path):
            final_path = lib_path
        else:
            logError('ERROR! Library `{}` does not exist!'.format(name))
            return False

        # Python and Zip files
        if os.path.isfile(final_path):
            logDebug('CE: Requested library file: `{}`.'.format(name))
            with open(final_path, 'rb') as binary:
                return xmlrpclib.Binary(binary.read())

        # Library folders must be compressed
        else:
            logDebug('CE: Requested library folder: `{}`.'.format(name))
            split_name = os.path.split(final_path)
            rnd = binascii.hexlify(os.urandom(5))
            tgz = split_name[1] + '_' + rnd + '.tgz'
            os.chdir(split_name[0])
            with tarfile.open(tgz, 'w:gz') as binary:
                binary.add(name=split_name[1], recursive=True)
            with open(tgz, 'r') as binary:
                data = xmlrpclib.Binary(binary.read())
            os.remove(tgz)
            return data


    @cherrypy.expose
    def getEpFiles(self, user, epname):
        """
        Returns all files that must be run on one EP.\n
        Called from the Runner.
        """
        if not self.searchEP(user, epname):
            logError('CE ERROR! EP `%s` is not in the list of defined EPs: `%s`!' %\
                     (str(epname), self.listEPs(user)) )
            return False

        try: data = self.project.getEpFiles(user, epname)
        except: data = False
        return data


    @cherrypy.expose
    def getSuiteFiles(self, user, epname, suite):
        """
        Returns all files that must be run on one Suite.\n
        Called from the Runner.
        """
        if not self.searchEP(user, epname):
            logError('CE ERROR! EP `%s` is not in the list of defined EPs: `%s`!' %\
                     (str(epname), self.listEPs(user)) )
            return False

        try: data = self.project.getSuiteFiles(user, epname, suite)
        except: data = False
        return data


    @cherrypy.expose
    def getTestFile(self, user, epname, file_id):
        """
        Sends requested file to TC, to be executed.\n
        Called from the Runner.
        """
        if not self.searchEP(user, epname):
            logError('CE ERROR! EP `{}` is not in the list of defined EPs: `{}`!'.format(epname, self.listEPs(user)))
            return False
        if not self.project.getEpInfo(user, epname).get('status'):
            logError('CE ERROR! `{}` requested file list, but the EP is closed! Exiting!'.format(epname))
            return False

        data = self.project.getFileInfo(user, epname, file_id)
        if not data:
            logError('CE ERROR! Invalid File ID `{}` !'.format(file_id))
            return False

        filename = data['file']
        tests_path = self.project.getUserInfo(user, 'tests_path')

        if filename.startswith('~'):
            filename = userHome(user) + filename[1:]
        if not os.path.isfile(filename):
            if not os.path.isfile(tests_path + os.sep + filename):
                logError('CE ERROR! TestCase file: `{}` does not exist!'.format(filename))
                return ''
            else:
                filename = tests_path + os.sep + filename.lstrip('/')

        logDebug('CE: Station {} requested file `{}`'.format(epname, filename))

        with open(filename, 'rb') as handle:
            return xmlrpclib.Binary(handle.read())


    @cherrypy.expose
    def getTestDescription(self, fname):
        """
        Returns the title, description and all tags from a test file.\n
        Called from the Java GUI.
        """
        try:
            text = open(fname,'rb').read()
        except:
            return ''

        # Find starting with #, optional space, followed by a <tag> ended with the same </tag>
        # containing any character in range 0x20 to 0x7e (all numbers, letters and ASCII symbols)
        # This returns 2 groups : the tag name and the text inside it
        tags = re.findall('#[ ]+?<(?P<tag>\w+)>([ -~\n]+?)</(?P=tag)>', text)

        return '<br>\n'.join(['<b>' + title + '</b> : ' + descr for title, descr in tags])


# --------------------------------------------------------------------------------------------------
#           L O G S
# --------------------------------------------------------------------------------------------------


    @cherrypy.expose
    def getLogFile(self, user, read, fstart, filename):
        """
        Called in the Java GUI to show the logs.
        """
        if fstart is None:
            return '*ERROR for {0}!* Parameter FSTART is NULL!'.format(user)
        if not filename:
            return '*ERROR for {0}!* Parameter FILENAME is NULL!'.format(user)

        fpath = self.project.getUserInfo(user, 'logs_path')

        if not fpath or not os.path.exists(fpath):
            return '*ERROR for {0}!* Logs path `{1}` is invalid! Using master config `{2}` and suites config `{3}`.'\
                .format(user, fpath, self.project.getUserInfo(user, 'config_path'), self.project.getUserInfo(user, 'project_path'))

        filename = fpath + os.sep + filename

        if not os.path.exists(filename):
            return '*ERROR for {0}!* File `{1}` does not exist! Using master config `{2}` and suites config `{3}`'.\
                format(user, filename, self.project.getUserInfo(user, 'config_path'), self.project.getUserInfo(user, 'project_path'))

        if not read or read=='0':
            return os.path.getsize(filename)

        fstart = long(fstart)
        f = open(filename)
        f.seek(fstart)
        data = f.read()
        f.close()

        return binascii.b2a_base64(data)


    def _logServer(self, user):
        """
        Launch a log server.
        """
        # Searching for a free port in the safe range...
        while 1:
            free = False
            port = random.randrange(60000, 62000)
            try:
                socket.create_connection((None, port), 1)
            except:
                free = True
            if free: break

        p_cmd = 'su {} -c "{} -u {}/server/LogServer.py {}"'.format(user, sys.executable, TWISTER_PATH, port)
        proc = subprocess.Popen(p_cmd, cwd='{}/twister'.format(userHome(user)), shell=True)
        proc.poll()

        time.sleep(0.3)
        logDebug('Log Server for user `{}` launched on `127.0.0.1:{}` - PID `{}`.'.format(user, port, proc.pid))

        self.loggers[user] = {'proc': proc, 'port': port}


    def _logConnect(self, user, port):
        """
        Create a log server connection.
        """
        for res in socket.getaddrinfo('127.0.0.1', port, socket.AF_UNSPEC, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                sock = socket.socket(af, socktype, proto)
            except socket.error as msg:
                logWarning('Sock create exception: `{}`.'.format(msg))
                sock = None
                continue
            try:
                sock.connect(sa)
            except socket.error as msg:
                logWarning('Sock connect exception: `{}`.'.format(msg))
                sock.close()
                sock = None
                continue
            break
        if sock is None:
            logError('Internal Log Error! Could not connect to Log Server!')
            return False
        else:
            return sock


    def _logServerMsg(self, user, msg):
        """
        Helper function to access the Log Server.
        """
        if user not in self.loggers:
            self._logServer(user)

        sock = self._logConnect(user, self.loggers[user]['port'])

        if not sock:
            logError('Creating a new connection...')
            self._logServer(user)
            sock = self._logConnect(user, self.loggers[user]['port'])
            if not sock:
                return False

        sock.sendall(msg)
        resp = sock.recv(1024)

        if resp == 'Ok!':
            sock.close()
            return True
        else:
            sock.close()
            return False


    @cherrypy.expose
    def logMessage(self, user, logType, logMessage):
        """
        This function is exposed in all tests, all logs are centralized in the HOME of the user.\n
        In order for the user to be able to access the logs written by CE, which runs as ROOT,
        CE will start a small process in the name of the user and the process will write the logs.
        """
        if os.getuid():
            logError('Log Error! Central Engine must run as ROOT in order to start the Log Server!')
            return False

        logType = str(logType)
        logTypes = self.project.getUserInfo(user, 'log_types')

        if logType == 'logsummary':
            logWarning('Log Warning! logSummary is reserved and cannot be written into!')
            return False

        if logType not in logTypes:
            logError('Log Error! Log type `{}` is not in the list of defined types: `{}`!'.format(logType, logTypes))
            return False

        logPath = self.project.getUserInfo(user, 'log_types')[logType]

        return self._logServerMsg(user, logPath + ':' + logMessage)


    @cherrypy.expose
    def logLIVE(self, user, epname, logMessage):
        """
        Writes CLI messages in a big log, so all output can be checked LIVE.\n
        Called from the EP.
        """
        if os.getuid():
            logError('Log Error! Central Engine must run as ROOT in order to start the Log Server!')
            return False

        logFolder = self.project.getUserInfo(user, 'logs_path')

        if not logFolder:
            logError('Log Error! Invalid logs folder `{}`!'.format(logFolder))
            return False

        try:
            log_string = binascii.a2b_base64(logMessage)
        except:
            logError('Live Log Error: Invalid base64 log!')
            return False

        # Execute "onLog" for all plugins
        parser = PluginParser(user)
        plugins = parser.getPlugins()
        for pname in plugins:
            plugin = self._buildPlugin(user, pname, {'log_type': 'cli'})
            try:
                plugin.onLog(epname, log_string)
            except Exception as e:
                trace = traceback.format_exc()[34:].strip()
                logWarning('Error on running plugin `{} onStop` - Exception: `{}`!'.format(pname, trace))
        del parser, plugins

        # Calling Panic Detect
        pd = self._panicDetectLogParse(user, epname, log_string)

        logTypes = self.project.getUserInfo(user, 'log_types')
        _, logCli = os.path.split( logTypes.get('logCli', 'CLI.log') )
        # Logs Path + EP Name + CLI Name
        logPath = logFolder + os.sep + epname +'_'+ logCli

        if pd:
            self.logMessage(user, 'logRunning', 'PANIC DETECT: Execution stopped.')

        return self._logServerMsg(user, logPath + ':' + log_string)


    @cherrypy.expose
    def resetLogs(self, user):
        """
        All logs defined in master config are erased.\n
        Called from the Java GUI and every time the project is reset.
        """
        logsPath = self.project.getUserInfo(user, 'logs_path')
        logTypes = self.project.getUserInfo(user, 'log_types')

        # Archive logs
        archiveLogsActive = self.project.getUserInfo(user, 'archive_logs_path_active')
        archiveLogsPath   = self.project.getUserInfo(user, 'archive_logs_path')

        data = json.dumps({
            'cmd': 'reset',
            'logsPath': logsPath,
            'logTypes': logTypes,
            'archiveLogsActive': archiveLogsActive,
            'archiveLogsPath': archiveLogsPath,
            'epnames': self.listEPs(user),
            })

        ret = self._logServerMsg(user, data)
        if ret:
            logDebug('Logs reset.')
        return ret


    @cherrypy.expose
    def resetLog(self, user, logName):
        """
        Resets one log.\n
        Called from the Java GUI.
        """
        logTypes = self.project.getUserInfo(user, 'log_types')
        logPath = ''

        # Cycle all log types and paths
        for logType, logN in logTypes.iteritems():
            _, logShort = os.path.split(logN)
            # CLI Logs are special, exploded for each EP
            if logType.lower() == 'logcli':
                for epname in self.listEPs(user).split(','):
                    logCli = epname +'_'+ logShort
                    if logName == logCli:
                        logPath = _ +'/'+ logCli
                        break
            else:
                # For normal, non-CLI logs...
                if logName == logShort:
                    logPath = logN
                    break

        if not logPath:
            logError('Log Error! Log name `{}` cannot be found!'.format(logName))
            return False

        data = json.dumps({
            'cmd': 'del',
            'logPath': logPath,
            })

        ret = self._logServerMsg(user, data)
        if ret:
            logDebug('Cleaned log `{}`.'.format(logPath))
        return ret


    def _panicDetectLogParse(self, user, epname, log_string):
        """
        Panic Detect parse log mechanism.
        """
        status = False

        self.project.panicDetectConfig(user, {'command': 'list'})

        if not self.project.panicDetectRegularExpressions.has_key(user):
            return status

        # Verify if for current suite Panic Detect is enabled
        suiteID = self.getEpVariable(user, epname, 'curent_suite')
        # When running first, the current_suite is not defined yet
        if not suiteID:
            return status

        enabled = self.getSuiteVariable(user, epname, suiteID, 'pd')

        if not enabled or enabled.lower() == 'false':
            return status

        for key, value in self.project.panicDetectRegularExpressions[user].iteritems():
            if value.get('enabled') == 'true':
                try:
                    if re.search(value['expression'], log_string):
                        # Stop EP
                        self.setExecStatus(user, epname, STATUS_STOP,
                            msg='Panic detect activated, expression `{}` found in CLI log!'.format(value['expression']))
                        status = True
                except Exception as e:
                    trace = traceback.format_exc()[34:].strip()
                    logError(trace)

        return status


    @cherrypy.expose
    def panicDetectConfig(self, user, command, data=None):
        """
        Configure Panic Detect.
        """
        # If argument is a string
        if type(data) == type(str()):
            try:
                _data = urlparse.parse_qs(data)
                if _data:
                    data = {k: v[0] if isinstance(v, list) else v for k,v in _data.iteritems()}
            except:
                msg = 'CE ERROR: PD cannot parse data: {d}!'.format(d=data)
                logError(msg)
                return msg

        if data:
            args = {
                'command': command,
                'data': data,
            }
        else:
            args = {
                'command': command,
            }

        return self.project.panicDetectConfig(user, args)


# Eof()
