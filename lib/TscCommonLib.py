
# File: TscCommonLib.py ; This file is part of Twister.

# version: 2.005

# Copyright (C) 2012-2013 , Luxoft

# Authors:
#    Adrian Toader <adtoader@luxoft.com>
#    Andrei Costachi <acostachi@luxoft.com>
#    Andrei Toma <atoma@luxoft.com>
#    Cristi Constantin <crconstantin@luxoft.com>
#    Daniel Cioata <dcioata@luxoft.com>
#    Mihail Tudoran <mtudoran@luxoft.com>

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
This module contains common functions to communicate with the Central Engine.
You can use : getGlobal, setGlobal, getResource, setResource, logMessage.
'''

import os, sys
import platform
import marshal
import rpyc
from rpyc import BgServingThread

# This will work, because TWISTER_PATH is appended to sys.path.
try:
    from ce_libs import PROXY, USER, EP, SUT
except:
    raise Exception('CommonLib must run from Twister!\n')

__all__ = ['TscCommonLib']

#

class TscCommonLib(object):

    platform_sys = platform.system().lower()
    proxy_path = PROXY
    userName = USER
    epName   = EP
    sutName  = SUT
    global_vars = {}


    def __init__(self):
        """
        Some initialization code.
        """
        self.__ce_proxy = None


    @property
    def ce_proxy(self):
        """
        Dinamically connect to the Central Engine.
        """
        # Try to reuse the old connection
        try:
            self.__ce_proxy.echo('ping')
            return self.__ce_proxy
        except:
            pass

        # RPyc config
        config = {
            'allow_pickle': True,
            'allow_getattr': True,
            'allow_setattr': True,
            'allow_delattr': True,
            'allow_all_attrs': True,
            }
        proxy = None

        # If the old connection is broken, connect to the RPyc server
        try:
            ce_ip, ce_port = self.proxy_path.split(':')
            proxy = rpyc.connect(ce_ip, int(ce_port), config=config)
            proxy.root.hello('lib::{}'.format(self.epName))
        except:
            print('*ERROR* Cannot connect to CE path `{}`! Exiting!'.format(self.proxy_path))
            exit(1)

        # Authenticate on RPyc server
        try:
            proxy.root.login(self.userName, 'EP')
            bg = BgServingThread(proxy)
            self.__ce_proxy = proxy.root
            return self.__ce_proxy
        except:
            print('*ERROR* Cannot authenticate on CE path `{}`! Exiting!'.format(self.proxy_path))
            exit(1)


    def logMsg(self, logType, logMessage):
        """
        Shortcut function for sending a message in a log to Central Engine.
        """
        self.ce_proxy.logMessage(logType, logMessage)


    def getGlobal(self, var):
        """
        Function to get variables saved from Test files.
        """
        if var in self.global_vars:
            return self.global_vars[var]
        # Else...
        return self.ce_proxy.getGlobalVariable(var)


    def setGlobal(self, var, value):
        """
        Function to keep variables sent from Test files.
        """
        try:
            marshal.dumps(value)
            return self.ce_proxy.setGlobalVariable(var, value)
        except:
            self.global_vars[var] = value
            return True


    def getConfig(self, cfg_path, var_path=''):
        """
        Function to get a config, using the full path to a config file and
        the full path to a config variable in that file.
        """
        return self.ce_proxy.getConfig(cfg_path, var_path)


    def countProjectFiles(self):
        """
        Returns the number of files inside the current project.
        """
        p = self.ce_proxy.getEpVariable(self.userName, self.epName, 'suites', True)
        data = pickle.loads(p)
        files = data.getFiles(recursive=True)
        return len(files)


    def currentFileIndex(self, FILE_ID=None):
        """
        Returns the index of this file in the project.
        """
        file_id = None
        if FILE_ID:
            file_id = FILE_ID
        else:
            try: file_id = self.FILE_ID
            except: pass
        if not file_id:
            return -1

        p = self.ce_proxy.getEpVariable(self.userName, self.epName, 'suites', True)
        data = pickle.loads(p)
        files = data.getFiles(recursive=True)
        try: return files.index(file_id)
        except: return -1


    def countSuiteFiles(self, SUITE_ID=None):
        """
        Returns the number of files inside a suite ID.
        If the suite ID is not provided, the count will try to use `self.SUITE_ID`.
        If the ID is not found, the count will fail.
        """
        suite_id = None
        if SUITE_ID:
            suite_id = SUITE_ID
        else:
            try: suite_id = self.SUITE_ID
            except: pass
        if not suite_id:
            return -1

        p = self.ce_proxy.getSuiteVariable(self.userName, self.epName, suite_id, 'children', True)
        data = pickle.loads(p)
        files = data.keys() # First level of files, depth=1
        return len(files)


    def currentFSuiteIndex(self, SUITE_ID=None, FILE_ID=None):
        """
        If the suite ID is not provided, the count will try to use `self.SUITE_ID`.
        If the ID is not found, the count will fail.
        Same with the file ID.
        """
        suite_id = None
        if SUITE_ID:
            suite_id = SUITE_ID
        else:
            try: suite_id = self.SUITE_ID
            except: pass
        if not suite_id:
            return -1

        file_id = None
        if FILE_ID:
            file_id = FILE_ID
        else:
            try: file_id = self.FILE_ID
            except: pass
        if not file_id:
            return -1

        p = self.ce_proxy.getSuiteVariable(self.userName, self.epName, suite_id, 'children', True)
        data = pickle.loads(p)
        files = data.keys() # First level of files, depth=1
        try: return files.index(file_id)
        except: return -1


    def py_exec(self, code_string):
        """
        Exposed Python function and class instances for TCL.
        """
        if not isinstance(code_string, str):
            print('py_exec: Error, the code must be a string `{}`!'.format(code_string))
            return False

        try: ret = eval(code_string, self.global_vars, self.global_vars)
        except Exception, e:
            print('py_exec: Error execution code `{}`! Exception `{}`!'.format(code_string, e))
            ret = False

        return ret


    def getResource(self, query):
        try: return self.ce_proxy.getResource(query)
        except: return None


    def setResource(self, name, parent=None, props={}):
        try: return self.ce_proxy.setResource(name, parent, props)
        except: return None


    def renameResource(self, res_query, new_name):
        try: return self.ce_proxy.renameResource(res_query, new_name)
        except: return None


    def deleteResource(self, query):
        try: return self.ce_proxy.deleteResource(query)
        except: return None


    def getSut(self, query):
        try: return self.ce_proxy.getSut(query)
        except: return None


    def setSut(self, name, parent=None, props={}):
        try: return self.ce_proxy.setSut(name, parent, props)
        except: return None


    def renameSut(self, res_query, new_name):
        try: return self.ce_proxy.renameSut(res_query, new_name)
        except: return None


    def deleteSut(self, query):
        try: return self.ce_proxy.deleteSut(query)
        except: return None


    def getResourceStatus(self, query):
        try: return self.ce_proxy.getResourceStatus(query)
        except: return None


    def allocResource(self, query):
        try: return self.ce_proxy.allocResource(query)
        except: return None


    def reserveResource(self, query):
        try: return self.ce_proxy.reserveResource(query)
        except: return None


    def freeResource(self, query):
        try: return self.ce_proxy.freeResource(query)
        except: return None


# Eof()
