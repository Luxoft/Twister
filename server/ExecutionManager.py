
# File: ExecutionManager.py ; This file is part of Twister.

# version: 2.003

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

import os
import sys
import json
import copy
import thread
import tarfile
import traceback
import rpyc
from pprint import pformat

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print('$TWISTER_PATH environment variable is not set! Exiting!')
    exit(1)
if TWISTER_PATH not in sys.path:
    sys.path.append(TWISTER_PATH)


from common.constants  import *
from common.helpers    import *
from common.tsclogging import *

#

class ExecutionManagerService(rpyc.Service):

    """
    Execution Manager class organizes the EP / Suite / Testcase functions.
    """

    project = None

    # This dictionary will contain pairs of:
    # - keys of connection ip+ports from remote locations
    # - values of meta info about each connection, like:
    #   {'checked': True, 'user': '...', 'type': 'client | ep'}
    conns = {}
    conn_lock = thread.allocate_lock()


    @classmethod
    def inject_object(self, name, obj):
        """
        Inject a variable inside this class
        """
        setattr(self, name, obj)
        return True


    def _get_addr(self):
        """
        Helper method to find the IP + Port of the current connection
        """
        try:
            return self._conn._config['connid']
        except:
            return ''


    def on_connect(self):
        """
        On client connect
        """
        str_addr = self._get_addr()

        # Add this connection in the list of connections,
        # If this connection CAN be added!
        try:
            with self.conn_lock:
                self.conns[str_addr] = {'conn': self._conn}
        except Exception as e:
            logError('EE: Connect error: {}.'.format(e))

        logDebug('EE: Connected from `{}`.'.format(str_addr))


    def on_disconnect(self):
        """
        On client disconnect
        """
        str_addr = self._get_addr()
        hello = self.conns[str_addr].get('hello', '')
        if hello: hello += ' - '

        # Delete everything for this address
        try:
            with self.conn_lock:
                del self.conns[str_addr]
        except Exception as e:
            logError('EE: Disconnect error: {}.'.format(e))

        logDebug('EE: Disconnected from `{}{}`.'.format(hello, str_addr))


    def exposed_cherryAddr(self):
        """
        Returns the CherryPy IP and PORT, for the Central Engine.
        This might be used to create an XML-RPC connection, using this addr.
        """
        return self.project.ip_port


    def exposed_echo(self, msg):
        """
        For testing connection
        """
        if msg != 'ping':
            logInfo(':: {}'.format(msg))
        return 'Echo: {}'.format(msg)


    def exposed_hello(self, hello=''):
        """
        For testing connection and setting a name.
        """
        str_addr = self._get_addr()

        with self.conn_lock:
            old_data = self.conns.get(str_addr, {})
            old_data.update({'hello': str(hello)})
            self.conns[str_addr] = old_data

        return True


    def exposed_login(self, user, passwd):
        """
        Log in before anything else.
        A user cannot execute commands without logging in first!
        """
        str_addr = self._get_addr()
        resp = self.project.rpyc_check_passwd(user, passwd)

        with self.conn_lock:
            old_data = self.conns.get(str_addr, {})
            old_data.update({'checked': resp, 'user': user})
            self.conns[str_addr] = old_data

        print('Connections :: {} //'.format(pformat(self.conns, indent=2, width=100)))
        return resp


    def _check_login(self):
        """
        Auto-detect the user based on the client connection,
        then check user login.
        """
        str_addr = self._get_addr()
        check = self.conns[str_addr].get('checked')
        user  = self.conns[str_addr].get('user')
        if (not check) or (not user):
            return False
        else:
            return user


# # #


    def exposed_resetProject(self):
        """
        Reset user project, to reload all config files
        """
        user = self._check_login()
        if not user: return False
        twister_cache = userHome(user) + '/twister/.twister_cache'
        setFileOwner(user, twister_cache)
        return self.project.reset(user)


    def exposed_getUserVariable(self, variable):
        """
        Send a user variable
        """
        user = self._check_login()
        if not user: return False
        data = self.project.getUserInfo(user, variable)
        if data is None: data = False
        return copy.copy(data)


    def exposed_setUserVariable(self, key, variable):
        """
        Create or overwrite a user variable
        """
        user = self._check_login()
        if not user: return False
        return self.project.setUserInfo(user, key, variable)


    def exposed_listEPs(self):
        """
        All known EPs for a user
        """
        user = self._check_login()
        if not user: return False
        return self.project.getUserInfo(user, 'eps').keys()


    def exposed_getEpVariable(self, epname, variable):
        """
        Send an EP variable
        """
        user = self._check_login()
        if not user: return False
        data = self.project.getEpInfo(user, epname).get(variable, False)
        if data is None: data = False
        return copy.copy(data)


    def exposed_setEpVariable(self, epname, variable, value):
        """
        Create or overwrite an EP variable
        """
        user = self._check_login()
        if not user: return False
        return self.project.setEpInfo(user, epname, variable, value)


    def exposed_listSuites(self, epname):
        " "
        user = self._check_login()
        if not user: return False
        suiteList = [str(k)+':'+v['name'] for k, v in self.project.getEpInfo(user, epname)['suites'].items()]
        return ','.join(suiteList)


    def exposed_getSuiteVariable(self, epname, suite, variable):
        """
        Send a Suite variable
        """
        user = self._check_login()
        if not user: return False
        data = self.project.getSuiteInfo(user, epname, suite)
        if not data: return False
        return data.get(variable, False)


    def exposed_getFileVariable(self, epname, file_id, variable):
        """
        Send a file variable
        """
        user = self._check_login()
        if not user: return False
        data = self.project.getFileInfo(user, epname, file_id)
        if not data: return False
        return data.get(variable, False)


    def exposed_setFileVariable(self, epname, filename, variable, value):
        """
        Create or overwrite a file variable
        """
        user = self._check_login()
        if not user: return False
        return self.project.setFileInfo(user, epname, filename, variable, value)


    def exposed_getGlobalVariable(self, var_path):
        """
        Global variables
        """
        user = self._check_login()
        if not user: return False
        return self.project.getGlobalVariable(user, var_path, False)


    def exposed_setGlobalVariable(self, var_path, value):
        """
        Global variables
        """
        user = self._check_login()
        if not user: return False
        return self.project.setGlobalVariable(user, var_path, value)


    def exposed_getConfig(self, cfg_path, var_path):
        """
        Config files
        """
        user = self._check_login()
        if not user: return False
        return self.project.getGlobalVariable(user, var_path, cfg_path)


# # #


    @classmethod
    def exposed_registeredEps(self, user=None):
        """
        Return all registered EPs for a client.
        The user MUST be given as a parameter.
        """
        if not user: return False
        eps = []

        for str_addr, data in self.conns.iteritems():
            # There might be more clients for a user...
            # And this Addr might be an EP, not a client
            if user == data['user'] and data['checked']:
                # If this connection has registered EPs, append them
                e = data.get('eps')
                if e: eps.extend(e)

        return sorted(set(eps))


    def exposed_registerEps(self, eps):
        """
        Register all EPs for a client.
        Only a VALID client will be able to register EPs!
        The user is identified automatically.
        """
        str_addr = self._get_addr()
        user = self._check_login()
        if not user: return False

        if not str_addr:
            logError('*ERROR* Cannot identify the remote address!')
            return False

        if not isinstance(eps, type([])):
            logError('*ERROR* Can only register a List of EP names!')
            return False
        else:
            eps = sorted(set(eps))

        try:
            # Send a Hello and this IP to the remote proxy Service
            hello = self._conn.root.hello(self.project.ip_port[0])
        except Exception as e:
            trace = traceback.format_exc()[34:].strip()
            logError('Error: Register client error: {}'.format(trace))
            hello = False

        # If the Hello from the other end of the connection returned False...
        if not hello:
            logDebug('Could not send Hello to the Client Manager `{}` for user `{}`!'.format(str_addr, user))
            return False

        # Register the EPs to this unique client address.
        # On disconnect, this client address will be deleted
        # And the EPs will be automatically un-registered.
        with self.conn_lock:
            self.conns[str_addr]['eps'] = eps

        logDebug('Registered client manager for user\n\t`{}` -> Client from `{}` = {}.'.format(user, str_addr, eps))
        return True


    @classmethod
    def exposed_startEP(self, epname, usr=None):
        """
        Start EP for client.
        This must work from any ExecManager instance.
        """
        if isinstance(self, ExecutionManagerService):
            user = self._check_login()
        else:
            user = usr
        if not user: return False

        conn = False

        # The EP that is required to be started is registered by a client
        # Must find the client that registered it, and use the RPyc connection
        for str_addr, data in self.conns.iteritems():
            # There might be more clients for a user...
            # And this Addr might be an EP, not a client
            if user == data['user'] and data['checked']:
                # If this connection has registered EPs
                eps = data.get('eps')
                if eps and epname in eps:
                    conn = data['conn']
                    break

        if not conn:
            logError('Unknown Execution Process: `{}` !'.format(epname))
            return False

        try:
            result = conn.root.start_ep(epname)
            logDebug('Starting `{} {}`... {}!'.format(user, epname, result))
            return result
        except Exception as e:
            trace = traceback.format_exc()[34:].strip()
            logError('Error: Start EP error: {}'.format(trace))
            return False


    @classmethod
    def exposed_stopEP(self, epname, usr=None):
        """
        Stop EP for client.
        This must work from any ExecManager instance.
        """
        if isinstance(self, ExecutionManagerService):
            user = self._check_login()
        else:
            user = usr
        if not user: return False

        conn = False

        # The EP that is required to be stopped is registered by a client
        # Must find the client that registered it, and use the RPyc connection
        for str_addr, data in self.conns.iteritems():
            # There might be more clients for a user...
            # And this Addr might be an EP, not a client
            if user == data['user'] and data['checked']:
                # If this connection has registered EPs
                eps = data.get('eps')
                if eps and epname in eps:
                    conn = data['conn']
                    break

        if not conn:
            logError('Unknown Execution Process: `{}` !'.format(epname))
            return False

        try:
            result = conn.root.stop_ep(epname)
            logDebug('Stopping `{} {}`... {}!'.format(user, epname, result))
            return result
        except Exception as e:
            trace = traceback.format_exc()[34:].strip()
            logError('Error: Stop EP error: {}'.format(trace))
            return False


# # #


    def exposed_getEpStatus(self, epname):
        """
        Return execution status for one EP. (stopped, paused, running, invalid)
        """
        user = self._check_login()
        if not user: return False

        if epname not in self.project.getUserInfo(user, 'eps'):
            logDebug('*ERROR* Invalid EP name `{}` !'.format(epname))
            return False

        data = self.project.getEpInfo(user, epname)

        reversed = dict((v,k) for k,v in execStatus.iteritems())
        return reversed[data.get('status', 8)]


    def exposed_getEpStatusAll(self):
        """
        Return execution status for all EPs. (stopped, paused, running, invalid)
        """
        user = self._check_login()
        if not user: return False

        data = self.project.getUserInfo(user)

        reversed = dict((v,k) for k,v in execStatus.iteritems())
        return reversed[data.get('status', 8)]


    def exposed_setEpStatus(self, epname, new_status, msg=''):
        """
        Set execution status for one EP. (0, 1, 2, or 3)
        Returns a string (stopped, paused, running).
        The `message` parameter can explain why the status has changed.
        """
        user = self._check_login()
        if not user: return False
        return self.project.setExecStatus(user, epname, new_status, msg)


    def exposed_setEpStatusAll(self, new_status, msg=''):
        """
        Set execution status for all EPs. (STATUS_STOP, STATUS_PAUSED, STATUS_RUNNING)
        Returns a string (stopped, paused, running).
        The `message` parameter can explain why the status has changed.
        """
        user = self._check_login()
        if not user: return False
        return self.project.setExecStatusAll(user, new_status, msg)


    def exposed_getFileStatusAll(self, epname=None, suite=None):
        """
        Returns a list with all statuses, for all files, in order.
        The status of one file can be obtained with ce.getFileVariable.
        """
        user = self._check_login()
        if not user: return False

        if epname not in self.project.getUserInfo(user, 'eps'):
            logDebug('*ERROR* Invalid EP name `{}` !'.format(epname))
            return False

        return self.project.getFileStatusAll(user, epname, suite)


    def exposed_setFileStatus(self, epname, file_id, new_status=10, time_elapsed=0.0):
        """
        Set status for one file and write in log summary.
        Called from the Runner.
        """
        user = self._check_login()
        if not user: return False
        return self.project.setFileStatus(user, epname, file_id, new_status, time_elapsed)


    def exposed_setFileStatusAll(self, epname, new_status):
        """
        Reset file status for all files of one EP.
        Called from the Runner.
        """
        user = self._check_login()
        if not user: return False
        return self.project.setFileStatusAll(user, epname, new_status)


# # #


    def exposed_listLibraries(self, all=True):
        """
        Returns the list of exposed libraries, from CE libraries folder.
        This list will be used to syncronize the libs on all EP computers.
        """
        user = self._check_login()
        if not user: return False
        return self.project.getLibrariesList(user, all)


    def exposed_downloadLibrary(self, name):
        """
        Sends required library to the EP, to be syncronized.
        The library can be global for all users, or per user.
        """
        user = self._check_login()
        if not user: return False
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
            logError('*ERROR* Library `{}` does not exist!'.format(name))
            return False

        # Python and Zip files
        if os.path.isfile(final_path):
            logDebug('CE: Requested library file: `{}`.'.format(name))
            with open(final_path, 'rb') as binary:
                return binary.read()

        # Library folders must be compressed
        else:
            logDebug('CE: Requested library folder: `{}`.'.format(name))
            final_dir, final_file = os.path.split(final_path)
            rnd = binascii.hexlify(os.urandom(5))
            tgz = final_file + '_' + rnd + '.tgz'
            os.chdir(final_dir)
            with tarfile.open(tgz, 'w:gz') as binary:
                binary.add(name=final_file, recursive=True)
            with open(tgz, 'r') as binary:
                data = binary.read()
            os.remove(tgz)
            return data


    def exposed_downloadFile(self, epname, file_info):
        """
        Sends requested file to the EP, to be executed.
        """
        user = self._check_login()
        if not user: return False

        if epname not in self.project.getUserInfo(user, 'eps'):
            logDebug('*ERROR* Invalid EP name `{}` !'.format(epname))
            return False

        tests_path = self.project.getUserInfo(user, 'tests_path')

        # If this is a test file path
        if os.path.isfile(tests_path + os.sep + file_info):
            filename = tests_path + os.sep + file_info

        # If this is a file ID
        else:
            file_id = file_info
            data = self.project.getFileInfo(user, epname, file_id)
            if not data:
                logError('*ERROR* Invalid File ID `{}` !'.format(file_id))
                return False

            filename = data['file']

            # Fix ~ $HOME path (from project XML)
            if filename.startswith('~'):
                filename = userHome(user) + filename[1:]
            # Fix incomplete file path (from project XML)
            if not os.path.isfile(filename):
                filename = tests_path + os.sep + filename

            # Inject this empty variable just to be sure.
            self.project.setFileInfo(user, epname, file_id, 'twister_tc_revision', '')

        logDebug('CE: Execution process `{}:{}` requested file `{}`.'.format(user, epname, filename))

        with open(filename, 'rb') as handle:
            return handle.read()


    def exposed_getEpFiles(self, epname):
        """
        Returns all files that must be run on one EP.
        """
        user = self._check_login()
        if not user: return False
        try: data = self.project.getEpFiles(user, epname)
        except: data = False
        return data


    def exposed_getSuiteFiles(self, epname, suite):
        """
        Returns all files that must be run on one Suite ID.
        """
        user = self._check_login()
        if not user: return False
        try: data = self.project.getSuiteFiles(user, epname, suite)
        except: data = False
        return data


# # #


    def exposed_logMessage(self, logType, logMessage):
        """
        This function is exposed in all tests and all logs are centralized in the HOME of the user.
        In order for the user to be able to access the logs written by CE, which runs as ROOT,
        CE will start a small process in the name of the user and the process will write the logs.
        """
        user = self._check_login()
        if not user: return False
        return self.project.logMessage(user, logType, logMessage)


    def exposed_logLIVE(self, epname, logMessage):
        """
        Writes CLI messages in a big log, so all output can be checked LIVE.
        """
        user = self._check_login()
        if not user: return False
        return self.project.logLIVE(user, epname, logMessage)


    def exposed_resetLog(self, logName):
        """
        Resets one log.
        """
        user = self._check_login()
        if not user: return False
        return self.project.resetLog(user, logName)


    def exposed_resetLogs(self):
        """
        All logs defined in master config are erased.\n
        """
        user = self._check_login()
        if not user: return False
        return self.project.resetLogs(user)


# Eof()
