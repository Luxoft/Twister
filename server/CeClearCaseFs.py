
# File: CeClearCaseFs.py ; This file is part of Twister.

# version: 3.018

# Copyright (C) 2012-2014, Luxoft

# Authors:
#    Andrei Costachi <acostachi@luxoft.com>
#    Cristi Constantin <crconstantin@luxoft.com>
#    Daniel Cioata <dcioata@luxoft.com>
#    Mihai Tudoran <mtudoran@luxoft.com>

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
ClearCase file system; used to work with CC views
"""


import os, sys
import time
import copy
import random
import socket
import pexpect
from plumbum import local
import rpyc

socket.setdefaulttimeout(3)
from thread import allocate_lock

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print('$TWISTER_PATH environment variable is not set! Exiting!')
    exit(1)
if TWISTER_PATH not in sys.path:
    sys.path.append(TWISTER_PATH)

if pexpect.__version__ < '3.1':
    raise Exception('pExpect version `{}` is too low!'
        ' ClearCase FS will crash!'.format(pexpect.__version__))

from common.helpers    import *
from common.tsclogging import *
from CeFs import BaseFS

# def logDebug(s)   : print s
# def logInfo(s)    : print s
# def logWarning(s) : print s
# def logError(s)   : print s


class ClearCaseFs(BaseFS, CcBorg):
    """
    All ClearCase file operations should be done via THIS class.
    This is a singleton.
    """

    def __init__(self):
        CcBorg.__init__(self)
        self.name = 'ClearCase'
        if os.getuid():
            logError('{} FS: Central Engine must run as ROOT in order to start the User Service!'.format(self.name))
        logInfo('Created {} FS.'.format(self.name))


    def _usr_service(self, user_view_actv, op='read'):
        """
        Launch a user service.
        Open a ClearCase view first.
        """
        if user_view_actv.count(':') == 1 and user_view_actv[-1] != ':':
            user_view_actv += ':'
        try:
            user, view, actv = user_view_actv.split(':')
        except Exception:
            # We don't really know the user in here !
            msg = 'Invalid ClearCase user-view-activity parameter: `{}`!'.format(user_view_actv)
            logWarning(msg)
            return '*ERROR* ' + msg

        view = view.strip()
        actv = actv.strip()
        user_view = user + ':' + view

        if not view:
            # We don't know the view in here !
            msg = 'Empty view in `{}`!'.format(user_view_actv)
            logWarning(msg)
            return '*ERROR* ' + msg

        # Must block here, so more users cannot launch Logs at the same time and lose the PID
        with self._srv_lock:

            def pread():
                """ Read proc stdout """
                while 1:
                    try:
                        line = proc.readline().strip()
                        if not line:
                            continue
                        plog.append(line)
                    except:
                        break

            # Try to re-use the FS, if available
            conn = self._services.get(user_view, {}).get('conn', None)
            if conn:
                try:
                    conn.ping(data='Hello', timeout=30.0)
                    # logDebug('Reuse old ClearCase Service connection for `{}` OK.'.format(user))
                    proc = self._services.get(user_view, {}).get('proc', None)
                    old_actv = self._services.get(user_view, {}).get('actv', None)
                    if actv != old_actv:
                        logInfo('Changing activity to `{}`, for `{}`.'.format(actv, user_view))
                        # Set cc activity again !
                        proc.sendline('cleartool setactivity {}'.format(actv))
                        time.sleep(1.0)
                        pread()
                        self._services.get(user_view, {})['actv'] = actv
                    return conn
                except Exception as e:
                    logWarning('Cannot connect to ClearCase Service for `{}`: `{}`.'.format(user_view, e))
                    self._kill(user)
                    proc = self._services.get(user_view, {}).get('proc', None)
                    PID = proc.pid
                    proc.terminate()
                    logInfo('Terminated CC User Service `{}` for user `{}`.'.format(PID, user))
            else:
                logInfo('Launching a ClearCase Service for `{}`, the first time...'.format(user_view))

            proc = pexpect.spawn(['bash'], timeout=2.5, maxread=2048)
            time.sleep(2.0)
            plog = []

            proc.sendline('su {}'.format(user))
            time.sleep(2.0)
            pread()
            # User's home folder
            proc.sendline('cd ~/twister')
            pread()
            # Set cc view only the first time !
            proc.sendline('cleartool setview {}'.format(view))
            time.sleep(2.0)
            pread()
            # Empty line after set view
            proc.sendline('')
            pread()

            if actv:
                # Set cc activity for the first time !
                proc.sendline('cleartool setactivity {}'.format(actv))
                time.sleep(1.0)
                pread()

            port = None

            # If the server is not available, search for a free port in the safe range...
            while 1:
                port = random.randrange(63000, 65000)
                try:
                    socket.create_connection((None, port), 1)
                except:
                    break

            # Launching 1 UserService inside the SSH terminal, with ClearCase View open
            p_cmd = '{} -u {}/server/UserService.py {} {} & '.format(sys.executable, TWISTER_PATH, port, self.name)
            proc.sendline(p_cmd)
            time.sleep(2.0)
            pread()

            # Empty line after proc start
            proc.sendline('')
            pread()

            logDebug('ClearCase startup log \n:: -------\n{}\n:: -------'.format('\n'.join(plog)))

            config = {
                'allow_pickle': True,
                'allow_getattr': True,
                'allow_setattr': True,
                'allow_delattr': True
            }

            retry = 10
            delay = 0.5
            success = False

            while retry > 0:
                try:
                    stream = rpyc.SocketStream.connect('127.0.0.1', port, timeout=5.0)
                    conn = rpyc.connect_stream(stream, config=config)
                    conn.root.hello()
                    logDebug('Connected to ClearCase Service for `{}`.'.format(user_view))
                    success = True
                    break
                except Exception as e:
                    logWarning('Cannot connect to ClearCase Service for `{}`!'\
                        'Exception: `{}`! Retry...'.format(user_view, e))
                time.sleep(delay)
                retry -= 1
                delay += 0.75

            if not success:
                logError('Error on starting ClearCase Service for `{}`!'.format(user_view))
                return None

            # Save the process inside the block.
            self._services[user_view] = {'proc': proc, 'conn': conn, 'port': port, 'actv': actv}

        logDebug('ClearCase Service for `{}` launched on `127.0.0.1:{}`.'.format(user_view, port))
        return conn


    def system_command(self, user_view, cmd):
        """ Execute a system command """
        logDebug('System command {} {}'.format(user_view, cmd))

        # if the view string ends with : , it means the activity is not set
        # and we have to strip the last :
        if user_view.endswith(':'):
            user_view = user_view.rstrip(':')

        # make sure the CC service is started
        self._usr_service('bpopescu:twister_view_dev_2')

        proc = self._services.get(user_view, {}).get('proc')
        if proc:
            # Empty buffer
            plog = []
            while 1:
                try:
                    line = proc.readline().strip()
                    if not line:
                        continue
                    plog.append(line)
                except:
                    break
            # Send command
            proc.sendline(cmd)
            time.sleep(1)
            plog = []
            # Catch buffer
            while 1:
                try:
                    line = proc.readline().strip()
                    if not line:
                        continue
                    plog.append(line)
                except:
                    break
            return '\n'.join(plog)
        else:
            return False

#

if __name__ == '__main__':

    FS_1 = ClearCaseFs()
    FS_1._usr_service('user:bogdan_twister')

    print FS_1.list_user_files('user:bogdan_twister', '/vob/metronext_DO_5/test_cases')
    print '---'
    print FS_1.read_user_file('user:bogdan_twister', '/vob/metronext_DO_5/test_cases/python/test_py_printnlogs.py')
    print '---'

    print FS_1.system_command('user:bogdan_twister', 'ls -la')

    FS_1._kill('user')


# Eof()
