
# File: TscCommonLib.py ; This file is part of Twister.

# version: 2.004

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
import socket
import platform
import marshal
import rpyc
import xmlrpclib

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
    cherry_path = None
    userName = USER
    epName   = EP
    sutName  = SUT
    global_vars = {}


    def __init__(self):

        # Connect to RPyc server
        try:
            ce_ip, ce_port = self.proxy_path.split(':')
            self.ce_proxy = rpyc.connect(ce_ip, int(ce_port))
            self.ce_proxy.root.hello()
        except:
            print('*ERROR* Cannot connect to CE path `{}`! Exiting!'.format(self.proxy_path))
            exit(1)

        # Authenticate on RPyc server
        try:
            check = self.ce_proxy.root.login(self.userName, 'EP')
        except:
            check = False
        if not check:
            print('*ERROR* Cannot authenticate on CE path `{}`! Exiting!'.format(self.proxy_path))
            exit(1)

        self.cherry_path = self.ce_proxy.root.cherryPort()

        try:
            socket.create_connection(self.cherry_path, 2)
        except:
            raise Exception('Invalid ip:port `{}`!\n'.format(self.cherry_path))
        try:
            self.ra_proxy = xmlrpclib.ServerProxy('http://{0}:EP@{1[0]}:{1[1]}/ra/'.format(self.userName, self.cherry_path))
        except:
            raise Exception('Invalid Resource Allocator ip:port `{}`!\n'.format(self.cherry_path))


    def logMsg(self, logType, logMessage):
        """
        Shortcut function for sending a message in a log to Central Engine.
        """
        self.ce_proxy.root.logMessage(logType, logMessage)


    def getGlobal(self, var):
        """
        Function to get variables saved from Test files.
        """
        if var in self.global_vars:
            return self.global_vars[var]
        # Else...
        return self.ce_proxy.root.getGlobalVariable(var)


    def setGlobal(self, var, value):
        """
        Function to keep variables sent from Test files.
        """
        try:
            marshal.dumps(value)
            return self.ce_proxy.root.setGlobalVariable(var, value)
        except:
            self.global_vars[var] = value
            return True


    def getConfig(self, cfg_path, var_path=''):
        """
        Function to get a config, using the full path to a config file and
        the full path to a config variable in that file.
        """
        return self.ce_proxy.root.getConfig(cfg_path, var_path)


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
        try: return self.ra_proxy.getResource(query)
        except: return None


    def setResource(self, name, parent=None, props={}):
        try: return self.ra_proxy.setResource(name, parent, props)
        except: return None


    def renameResource(self, res_query, new_name):
        try: return self.ra_proxy.renameResource(res_query, new_name)
        except: return None


    def deleteResource(self, query):
        try: return self.ra_proxy.deleteResource(query)
        except: return None


    def getSut(self, query):
        try: return self.ra_proxy.getSut(query)
        except: return None


    def setSut(self, name, parent=None, props={}):
        try: return self.ra_proxy.setSut(name, parent, props)
        except: return None


    def renameSut(self, res_query, new_name):
        try: return self.ra_proxy.renameSut(res_query, new_name)
        except: return None


    def deleteSut(self, query):
        try: return self.ra_proxy.deleteSut(query)
        except: return None


    def getResourceStatus(self, query):
        try: return self.ra_proxy.getResourceStatus(query)
        except: return None


    def allocResource(self, query):
        try: return self.ra_proxy.allocResource(query)
        except: return None


    def reserveResource(self, query):
        try: return self.ra_proxy.reserveResource(query)
        except: return None


    def freeResource(self, query):
        try: return self.ra_proxy.freeResource(query)
        except: return None


# Eof()
