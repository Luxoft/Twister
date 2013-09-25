
# File: ClearCasePlugin.py ; This file is part of Twister.

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

"""
    ClearCase plugin wraps cleartool library.
    Executes the given commands using cleartool library.
"""
from __future__ import print_function

from BasePlugin import BasePlugin

import os, sys
import time
import random
import socket
import subprocess
import xmlrpclib

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print('TWISTER_PATH environment variable is not set! Exiting!')
    exit(1)

from common.helpers import userHome

#

class Plugin(BasePlugin):

    """
    ClearCase plugin
    """

    def __init__(self, user, data):

        if not data: return False
        BasePlugin.__init__(self, user, data)
        self.user = user
        self.data = data
        self.conn = None


    def __del__(self):
        try: self.conn.cmd({'command': 'exit'})
        except: pass
        del self.user
        del self.data
        del self.conn


    def _connect(self):

        # Searching for a free port in the safe range...
        while 1:
            free = False
            port = random.randrange(59000, 60000)
            try:
                socket.create_connection((None, port), 1)
            except:
                free = True
            if free: break

        p_cmd = 'su {} -c "{} -u {}/plugins/ClearCaseSrv.py {}"'.format(self.user, sys.executable, TWISTER_PATH, port)
        proc = subprocess.Popen(p_cmd, cwd='{}/twister'.format(userHome(self.user)), shell=True)
        proc.poll()

        time.sleep(0.5)
        print('CC Srv for user `{}` launched on `127.0.0.1:{}` - PID `{}`.'.format(self.user, port, proc.pid))

        try:
            self.conn = xmlrpclib.ServerProxy('http://127.0.0.1:{}/'.format(port))
            self.conn.hello()
        except Exception as e:
            print('Cannot connect to CC Srv on `127.0.0.1:{}` - `{}` !'.format(port, e))
            proc.terminate()
            self.conn = None
            return False

        return True


    def run(self, args):
        """
        Called for every command
        """
        # Create connection ...
        if not isinstance(self.conn, xmlrpclib.ServerProxy):
            resp = self._connect()
            # Connection failed !
            if not resp:
                return False
        try:
            self.conn.hello()
        except:
            resp = self._connect()
            # Connection failed !
            if not resp:
                return False
        try:
            resp = self.conn.cmd(args)
        except Exception as e:
            print('CC Plug-in: Exception on args `{}` - `{}` !'.format(args, e))
            return False

        return resp


    def onStart(self, clear_case_view=None):
        """
        Called on project start.
        """
        # No data provided ?
        if not clear_case_view:
            return False
        # The view is already active ?
        if 'clear_case_view' in self.data:
            return True

        print('CC Plug-in: Changing ClearCase View to `{}`.'.format(clear_case_view))

        self.data['clear_case_view'] = clear_case_view
        self.run( {'command': 'setview {}'.format(clear_case_view)} )


    def getTestFile(self, fname):
        """
        Send 1 ClearCase file.
        """
        return self.conn.getTestFile(fname)


    def getTestDescription(self, user, fname):
        """
        Returns the title, description and all tags from a test file.
        """
        return self.conn.getTestDescription(user, fname)

#

"""

#### plugins.xml config ####

<Plugin>
    <name>ClearCase</name>
    <jarfile>ClearCasePlugin.jar</jarfile>
    <pyfile>ClearCasePlugin.py</pyfile>
    <status>disabled</status>
</Plugin>

"""
