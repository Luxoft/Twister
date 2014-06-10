
# File: TscCommonLib.py ; This file is part of Twister.

# version: 3.009

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
except Exception:
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
    global_vars = {}


    def __init__(self):
        """
        Some initialization code.
        """
        self._reload_libs()


    def _reload_libs(self):
        ce_path = '{}/.twister_cache/{}/ce_libs/ce_libs.py'.format(TWISTER_PATH, self.epName)
        cfg = iniparser.ConfigObj(ce_path)
        for n, v in cfg.iteritems():
            setattr(self, '_' + n, v)
        del cfg


    @property
    def sutName(self):
        self._reload_libs()
        name = self.ce_proxy.getSuiteVariable(self.epName, self._SUITE_ID, 'sut')
        return name


    @property
    def SUT(self):
        self._reload_libs()
        name = self.ce_proxy.getSuiteVariable(self.epName, self._SUITE_ID, 'sut')
        return name


    @property
    def SUITE_ID(self):
        self._reload_libs()
        return self._SUITE_ID


    @property
    def FILE_ID(self):
        self._reload_libs()
        return self._FILE_ID


    @property
    def SUITE_NAME(self):
        self._reload_libs()
        name = self.ce_proxy.getSuiteVariable(self.epName, self._SUITE_ID, 'name')
        return name


    @property
    def FILE_NAME(self):
        self._reload_libs()
        name = self.ce_proxy.getFileVariable(self.epName, self._FILE_ID, 'file')
        if name: name = os.path.split(name)[1]
        return name


    @classmethod
    def _ce_proxy(cls):
        """
        Dinamically connect to the Central Engine.
        This is a class method.
        """
        stack = inspect.stack()
        # The upper stack is either the EP, or the library that derives this
        stack_fpath = stack[1][1]
        stack_fname = os.path.split(stack_fpath)[1]
        proxy = None

        # If the upper stack is not ExecutionProcess, the library is derived
        if stack_fname != 'ExecutionProcess.py':
            # The EP stack is always the last
            ep_code = stack[-1][0]
            # It's impossible to access the globals from the EP any other way
            p = ep_code.f_globals.get('ceProxy')
            if p: return p.root
        del stack, stack_fpath

        # Try to reuse the old connection
        try:
            cls.__ce_proxy.echo('ping')
            return cls.__ce_proxy
        except Exception:
            pass

        # RPyc config
        config = {
            'allow_pickle': True,
            'allow_getattr': True,
            'allow_setattr': True,
            'allow_delattr': True,
            'allow_all_attrs': True,
            }

        ce_ip, ce_port = cls.proxy_path.split(':')

        # If the old connection is broken, connect to the RPyc server
        try:
            # Transform XML-RPC port into RPyc Port; RPyc port = XML-RPC port + 10 !
            ce_port = int(ce_port) + 10
            proxy = rpyc.connect(ce_ip, ce_port, config=config)
            proxy.root.hello('lib::{}'.format(cls.epName))
        except Exception:
            print('*ERROR* Cannot connect to CE path `{}`! Exiting!'.format(cls.proxy_path))
            raise Exception('Cannot connect to CE')

        # Authenticate on RPyc server
        try:
            proxy.root.login(cls.userName, 'EP')
        except Exception:
            print('*ERROR* Cannot authenticate on CE path `{}`! Exiting!'.format(cls.proxy_path))
            raise Exception('Cannot authenticate on CE')

        # Launch bg server
        try:
            bg = BgServingThread(proxy)
            cls.__ce_proxy = proxy.root
            return cls.__ce_proxy
        except Exception:
            print('*ERROR* Cannot launch Bg serving thread! Exiting!')
            raise Exception('Cannot launch Bg thread')


    @property
    def ce_proxy(self):
        """
        Make this an instance property.
        """
        return self._ce_proxy()


    def logMsg(self, logType, logMessage):
        """
        Shortcut function for sending a message in a log to Central Engine.
        """
        self.ce_proxy.logMessage(logType, logMessage)


    @classmethod
    def getGlobal(cls, var):
        """
        Function to get variables saved from Test files.
        The same dictionary must be used, both in Testcase and derived Library.
        """
        if var in cls.global_vars:
            return cls.global_vars[var]
        # Else...
        ce = cls._ce_proxy()
        return ce.getGlobalVariable(var)


    @classmethod
    def setGlobal(cls, var, value):
        """
        Function to keep variables sent from Test files.
        The same dictionary must be used, both in Testcase and derived Library.
        """
        try:
            marshal.dumps(value)
            ce = cls._ce_proxy()
            return cls.ce_proxy.setGlobalVariable(var, value)
        except Exception:
            cls.global_vars[var] = value
            return True


    def getConfig(self, cfg_path, var_path=''):
        """
        Function to get a config, using the full path to a config file and
        the full path to a config variable in that file.
        """
        return self.ce_proxy.getConfig(cfg_path, var_path)


    def getBinding(self, cfg_root):
        """
        Function to get a cfg -> SUT binding.
        """
        if not hasattr(self, 'bindings'):
            self.bindings = self.ce_proxy.getUserVariable('bindings') or {}
        return self.bindings.get(cfg_root)


    def getBindId(self, component_name, test_config='default_binding'):
        """
        Function to get a cfg -> SUT binding ID.
        Some syntactic sugar.
        """
        if not hasattr(self, 'bindings'):
            self.bindings = self.ce_proxy.getUserVariable('bindings') or {}
        # Fix cfg root maybe ?
        if not test_config:
            test_config = 'default_binding'
        config_data = self.bindings.get(test_config, {})
        # If the component cannot be found in the requested config, search in default config
        if test_config != 'default_binding' and (component_name not in config_data):
            config_data = self.bindings.get('default_binding', {})
        return config_data.get(component_name, False)


    def getBindName(self, component_name, test_config='default_binding'):
        """
        Function to get a cfg -> SUT binding name.
        Some syntactic sugar.
        """
        sid = self.getBindId(component_name, test_config)
        if not sid: return False
        sut = self.getSut(sid)
        if not sut: sut = {}
        return sut.get('path', False)


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
        data = self.ce_proxy.getEpVariable(self.epName, 'suites')
        SuitesManager = copy.deepcopy(data)
        files = SuitesManager.getFiles(recursive=True)
        try: return files.index(self.FILE_ID)
        except Exception: return -1


    def countSuiteFiles(self):
        """
        Returns the number of files inside a suite ID.
        If the ID is not found, the count will fail.
        """
        data = self.ce_proxy.getSuiteVariable(self.epName, self.SUITE_ID, 'children')
        SuitesManager = copy.deepcopy(data)
        files = SuitesManager.keys() # First level of files, depth=1
        return len(files)


    def currentFSuiteIndex(self):
        """
        Returns the index of this file, inside this suite.
        If the ID is not found, the count will fail.
        """
        data = self.ce_proxy.getSuiteVariable(self.epName, self.SUITE_ID, 'children')
        SuitesManager = copy.deepcopy(data)
        files = SuitesManager.keys() # First level of files, depth=1
        try: return files.index(self.FILE_ID)
        except Exception: return -1


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


    def _encodeUnicode(self, input):
        if isinstance(input, dict):
            return {self._encodeUnicode(key): self._encodeUnicode(value) for key, value in input.iteritems()}
        elif isinstance(input, list):
            return [self._encodeUnicode(elem) for elem in input]
        elif isinstance(input, unicode):
            return input.encode('utf-8')
        else:
            return input


    def getResource(self, query, type=unicode):
        try:
            data = self.ce_proxy.getResource(query)
            if type==str:
                return self._encodeUnicode(data)
            else:
                return data
        except Exception as e:
            print('Error on get Resource! `{}`!'.format(e))
            return None


    def setResource(self, name, parent=None, props={}):
        try: return self.ce_proxy.setResource(name, parent, props)
        except Exception: return None


    def renameResource(self, res_query, new_name):
        try: return self.ce_proxy.renameResource(res_query, new_name)
        except Exception: return None


    def deleteResource(self, query):
        try: return self.ce_proxy.deleteResource(query)
        except Exception: return None


    def getSut(self, query, type=unicode):
        try:
            data = self.ce_proxy.getSut(query)
            if type==str:
                return self._encodeUnicode(data)
            else:
                return data
        except Exception as e:
            print('Error on get SUT! `{}`!'.format(e))
            return None


    def setSut(self, name, parent=None, props={}):
        try: return self.ce_proxy.setSut(name, parent, props)
        except Exception: return None


    def renameSut(self, res_query, new_name):
        try: return self.ce_proxy.renameSut(res_query, new_name)
        except Exception: return None


    def deleteSut(self, query):
        try: return self.ce_proxy.deleteSut(query)
        except Exception: return None


    def getResourceStatus(self, query):
        try: return self.ce_proxy.getResourceStatus(query)
        except Exception: return None


    def allocResource(self, query):
        try: return self.ce_proxy.allocResource(query)
        except Exception: return None


    def reserveResource(self, query):
        try: return self.ce_proxy.reserveResource(query)
        except Exception: return None


    def freeResource(self, query):
        try: return self.ce_proxy.freeResource(query)
        except Exception: return None


# Eof()
