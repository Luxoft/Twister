
# File: ExecutionManager.py ; This file is part of Twister.

# version: 2.002

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
import thread
import rpyc

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

connections = {}
conn_lock = thread.allocate_lock()

#

class ExecutionManagerService(rpyc.Service):

    """
    Execution Manager class organizes the EP / Suite / Testcase functions.
    """

    project = None


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
        tuple_addr = self._conn._config['endpoints'][1]
        return '{}:{}'.format(tuple_addr[0], tuple_addr[1])


    def on_connect(self):
        """
        On client connect
        """
        global connections, conn_lock
        str_addr = self._get_addr()

        try:
            with conn_lock:
                connections[str_addr] = {}
                logDebug('EE: Connected from `{}`.'.format(str_addr))
        except Exception as e:
            logError('EE: Connect error: {er}.'.format(er=e))


    def on_disconnect(self):
        """
        On client disconnect
        """
        global connections, conn_lock
        str_addr = self._get_addr()

        try:
            with conn_lock:
                del connections[str_addr]
                logDebug('EE: Disconnected from `{}`.'.format(str_addr))
        except Exception as e:
            logError('EE: Disconnect error: {er}.'.format(er=e))


    def exposed_hello(self):
        """
        For testing connection
        """
        return True


    def exposed_echo(self, msg):
        """
        For testing connection
        """
        return 'Echo: {}'.format(msg)


    def exposed_login(self, user, passwd):
        """
        Log in. A user cannot execute commands without logging in first!
        """
        global connections, conn_lock
        str_addr = self._get_addr()
        resp = self.project.rpyc_check_passwd(user, passwd)

        try:
            with conn_lock:
                connections[str_addr] = {'checked': resp, 'user': user}
        except Exception as e:
            logError('EE: Disconnect error: {er}.'.format(er=e))

        print('Connections ::', connections)
        return resp


    def _check_login(self):
        """
        Check user login.
        Uses the internal connection to auto-detect the user.
        """
        global connections, conn_lock
        str_addr = self._get_addr()
        check = connections[str_addr].get('checked')
        user  = connections[str_addr].get('user')
        if (not check) or (not user):
            return False
        else:
            return user


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
        return data


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
        epList = self.project.getUserInfo(user, 'eps').keys()
        return ','.join(epList)


    def exposed_getEpVariable(self, epname, variable, compress=False):
        """
        Send an EP variable
        """
        user = self._check_login()
        if not user: return False
        return self.project.getEpInfo(user, epname).get(variable, False)


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


    def registerClient(self, user, clients):
        " "
        return False


    def startEP(self, user, epname):
        " "
        return False


    def stopEP(self, user, epname):
        " "
        return False


    def restartEP(self, user, epname):
        " "
        return False


# # #


    def getEpStatus(self, user, epname):
        " "
        return False


    def getEpStatusAll(self, user):
        " "
        return False


    def setEpStatus(self, user, epname, new_status, msg=''):
        " "
        return self.project.setExecStatus(user, epname, new_status, msg)


    def setEpStatusAll(self, user, new_status, msg=''):
        " "
        return self.project.setExecStatusAll(user, new_status, msg)


# # #


    def getLibrariesList(self, user='', all=True):
        " "
        return False


    def downloadLibrary(self, user, name):
        " "
        return False


    def getTestFile(self, user, epname, file_id):
        " "
        return False


    def getEpFiles(self, user, epname):
        " "
        return False


    def getSuiteFiles(self, user, epname, suite):
        " "
        return False


# Eof()
