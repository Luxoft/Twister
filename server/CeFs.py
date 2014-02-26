
# File: CeFs.py ; This file is part of Twister.

# version: 3.001

# Copyright (C) 2012-2014 , Luxoft

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

import os, sys
import time
import copy
import random
import socket
import subprocess
import rpyc

socket.setdefaulttimeout(3)
from thread import allocate_lock

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print('$TWISTER_PATH environment variable is not set! Exiting!')
    exit(1)
if TWISTER_PATH not in sys.path:
    sys.path.append(TWISTER_PATH)

from common.helpers    import *
from common.tsclogging import *

#
__all__ = ['LocalFS']
#

def singleton(cls):
    instances = {}
    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return getinstance


@singleton
class LocalFS(object):
    """
    All local file operations should be done via THIS class.
    This is a singleton.
    """
    services = {}
    srv_lock = allocate_lock()


    def __init__(self):
        if os.getuid():
            logError('Local FS: Central Engine must run as ROOT in order to start the User Service!')
        logInfo('Created Local FS.')


    def _usrService(self, user):
        """
        Launch a user service.
        """
        if not userHome(user):
            logError('Local FS: Username `{}` is not valid!'.format(user))
            return False

        # # DEBUG. Show all available User Services, for current user.
        # try:
        #     pids = subprocess.check_output('ps aux | grep /server/UserService.py | grep "^{} "'.format(user), shell=True)
        #     pids_li = []

        #     for line in pids.strip().splitlines():
        #         li = line.strip().split()
        #         PID = int(li[1])
        #         del li[2:10]
        #         pids_li.append( ' '.join(li) )

        #     logDebug('Active User Services for `{}`::\n\t{}'.format(user, '\n\t'.join(pids_li)))
        # except:
        #     logDebug('No User Services found for `{}`.'.format(user))

        # Try to re-use the logger server, if available
        conn = self.services.get(user, {}).get('conn', None)
        if conn:
            try:
                conn.root.hello()
                logDebug('Reuse old User Service connection for `{}` OK.'.format(user))
                return conn
            except:
                pass

        logDebug('Preparing to launch/ reuse a User Service for `{}`...'.format(user))
        port = None

        # If the server is not available, search for a free port in the safe range...
        while 1:
            port = random.randrange(63000, 65000)
            try:
                socket.create_connection((None, port), 1)
            except:
                break

        p_cmd = 'su {} -c "{} -u {}/server/UserService.py {}"'.format(user, sys.executable, TWISTER_PATH, port)
        proc = subprocess.Popen(p_cmd, cwd='{}/twister'.format(userHome(user)), shell=True,
               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.poll()
        time.sleep(0.2)

        config = {
            'allow_pickle': True,
            'allow_getattr': True,
            'allow_setattr': True,
            'allow_delattr': True
        }

        # Must block here, so more users cannot launch Logs at the same time and lose the PID
        with self.srv_lock:

            retries = 10
            success = False

            while retries > 0:
                try:
                    conn = rpyc.connect('127.0.0.1', port, config=config)
                    conn.root.hello()
                    logDebug('Connected to User Service for `{}`.'.format(user))
                    success = True
                    break
                except Exception as e:
                    logWarning('Cannot connect to User Service for `{}` - Exception: `{}`! Retry...'.format(user, e))
                retries -= 1
                time.sleep(0.5)

            if not success:
                logError('Error on starting User Service for `{}`!'.format(user))
                return False

            # Save the process inside the block.  99% of the time, this block is executed instantly!
            self.services[user] = {'proc': proc, 'conn': conn, 'port': port}

        logDebug('User Service for `{}` launched on `127.0.0.1:{}` - PID `{}`.'.format(user, port, proc.pid))
        return conn


    # ----- USER ---------------------------------------------------------------

    def readUserFile(self, user, fpath):
        srvr = self._usrService(user)
        if srvr:
            return srvr.root.read_file(fpath)
        else:
            return False


    def writeUserFile(self, user, fpath, fdata, mode='w'):
        srvr = self._usrService(user)
        if srvr:
            return srvr.root.write_file(fpath, fdata, mode)
        else:
            return False


    def copyUserFile(self, user, fpath, newpath):
        srvr = self._usrService(user)
        if srvr:
            return srvr.root.copy_file(fpath, newpath)
        else:
            return False


    def moveUserFile(self, user, fpath, newpath):
        srvr = self._usrService(user)
        if srvr:
            return srvr.root.move_file(fpath, newpath)
        else:
            return False


    def deleteUserFile(self, user, fpath):
        srvr = self._usrService(user)
        if srvr:
            return srvr.root.delete_file(fpath)
        else:
            return False


    def createUserFolder(self, user, fdir):
        srvr = self._usrService(user)
        if srvr:
            return srvr.root.create_folder(fdir)
        else:
            return False


    def listUserFiles(self, user, fdir):
        srvr = self._usrService(user)
        if srvr:
            files = srvr.root.list_files(fdir)
            return copy.copy(files)
        else:
            return False


    def deleteUserFolder(self, user, fdir):
        srvr = self._usrService(user)
        if srvr:
            return srvr.root.delete_folder(fdir)
        else:
            return False


    # ----- SYSTEM -------------------------------------------------------------

    def readSystemFile(self, fname):
        pass


    def writeSystemFile(self, fname):
        pass


    def deleteSystemFile(self, fname):
        pass


    def createSystemFolder(self, fdir):
        pass


    def listSystemFiles(self, fdir):
        pass


    def deleteSystemFolder(self, fdir):
        pass

#

if __name__ == '__main__':

    fs1 = LocalFS()
    fs2 = LocalFS()

    assert fs1 == fs2, 'Not equal!'
    assert fs1 is fs2, 'Not identical!'

    print(fs1)
    print(fs2)
    print('Ok.')


# Eof()
