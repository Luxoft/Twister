
# File: TscCommonLib.py ; This file is part of Twister.

# version: 3.001

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
import copy
import inspect
import platform
import marshal
import rpyc
from rpyc import BgServingThread

# This will work, because TWISTER_PATH is appended to sys.path.
try:
    from ce_libs import *
except:
    raise Exception('CommonLib must run from Twister!\n')

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    raise Exception('$TWISTER_PATH environment variable is not set!\n')

from common import iniparser

__all__ = ['TscCommonLib']

#

class TscCommonLib(object):

    platform_sys = platform.system().lower()
    __ce_proxy = None
    proxy_path = PROXY_ADDR
    userName = USER
    epName   = EP
    sutName  = SUT
    global_vars = {}


    def __init__(self):
        """
        Some initialization code.
        """
        self.reload_libs()


    def reload_libs(self):
        ce_path = '{}/.twister_cache/{}/ce_libs/ce_libs.py'.format(TWISTER_PATH, self.epName)
        cfg = iniparser.ConfigObj(ce_path)
        for n, v in cfg.iteritems():
            setattr(self, n, v)
        del cfg


    @property
    def ce_proxy(self):
        """
        Dinamically connect to the Central Engine.
        """
        stack = inspect.stack()
        # The upper stack is either the EP, or the library that derives this
        stack_fpath = stack[1][1]
        stack_fname = os.path.split(stack_fpath)[1]

        # If the upper stack is not ExecutionProcess, the library is derived
        if stack_fname != 'ExecutionProcess.py':
            # The EP stack is always the last
            ep_code = stack[-1][0]
            # It's impossible to access the globals from the EP any other way
            return ep_code.f_globals.get('ceProxy')
        del stack, stack_fpath

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
            # Transform XML-RPC port into RPyc Port; RPyc port = XML-RPC port + 10 !
            ce_port = int(ce_port) + 10
            proxy = rpyc.connect(ce_ip, ce_port, config=config)
            proxy.root.hello('lib::{}'.format(self.epName))
        except:
            print('*ERROR* Cannot connect to CE path `{}`! Exiting!'.format(self.proxy_path))
            raise Exception

        # Authenticate on RPyc server
        try:
            proxy.root.login(self.userName, 'EP')
            bg = BgServingThread(proxy)
            self.__ce_proxy = proxy.root
            return self.__ce_proxy
        except:
            print('*ERROR* Cannot authenticate on CE path `{}`! Exiting!'.format(self.proxy_path))
            raise Exception

        return proxy


    def logMsg(self, logType, logMessage):
        """
        Shortcut function for sending a message in a log to Central Engine.
        """
        self.ce_proxy.logMessage(logType, logMessage)


    @classmethod
    def getGlobal(cls, var):
        """
        Function to get variables saved from Test files.
        """
        if var in cls.global_vars:
            return cls.global_vars[var]
        # Else...
        return cls.ce_proxy.getGlobalVariable(var)


    @classmethod
    def setGlobal(cls, var, value):
        """
        Function to keep variables sent from Test files.
        """
        try:
            marshal.dumps(value)
            return cls.ce_proxy.setGlobalVariable(var, value)
        except:
            cls.global_vars[var] = value
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
        data = self.ce_proxy.getEpVariable(self.epName, 'suites')
        SuitesManager = copy.deepcopy(data)
        files = SuitesManager.getFiles(recursive=True)
        return len(files)


    def currentFileIndex(self):
        """
        Returns the index of this file in the project.
        If the ID is not found, the count will fail.
        """
        self.reload_libs()
        if not self.FILE_ID:
            return -1

        data = self.ce_proxy.getEpVariable(self.epName, 'suites')
        SuitesManager = copy.deepcopy(data)
        files = SuitesManager.getFiles(recursive=True)
        try: return files.index(self.FILE_ID)
        except: return -1


    def countSuiteFiles(self):
        """
        Returns the number of files inside a suite ID.
        If the ID is not found, the count will fail.
        """
        self.reload_libs()
        if not self.SUITE_ID:
            return -1

        data = self.ce_proxy.getSuiteVariable(self.epName, self.SUITE_ID, 'children')
        SuitesManager = copy.deepcopy(data)
        files = SuitesManager.keys() # First level of files, depth=1
        return len(files)


    def currentFSuiteIndex(self):
        """
        Returns the index of this file, inside this suite.
        If the ID is not found, the count will fail.
        """
        self.reload_libs()
        if not self.SUITE_ID:
            return -1
        if not self.FILE_ID:
            return -1

        data = self.ce_proxy.getSuiteVariable(self.epName, self.SUITE_ID, 'children')
        SuitesManager = copy.deepcopy(data)
        files = SuitesManager.keys() # First level of files, depth=1
        try: return files.index(self.FILE_ID)
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
