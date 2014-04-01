
# File: CeFs.py ; This file is part of Twister.

# version: 3.008

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

import os, sys
import time
import copy
import random
import socket
import subprocess
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
    _services = {}
    _srv_lock = allocate_lock()


    def __init__(self, project=None):
        if os.getuid():
            logError('Local FS: Central Engine must run as ROOT in order to start the User Service!')
        self.project = project
        logInfo('Created Local FS.')


    def _kill(self, user):

        ps   = local['ps']
        grep = local['grep']

        try:
            pids = (ps['aux'] | grep['/server/UserService.py'] | grep['^' + user] | grep['FS'])()
        except Exception:
            return

        # Kill all leftover processes
        for line in pids.strip().splitlines():
            li = line.strip().decode('utf').split()
            PID = int(li[1])
            del li[2:5]
            if '/bin/sh' in li: continue
            if '/bin/grep' in li: continue
            logDebug('User {}: Killing ugly zombie `{}`.'.format(user,' '.join(li)))
            try:
                os.kill(PID, 9)
            except:
                pass


    def _usrService(self, user):
        """
        Launch a user service.
        """

        # Must block here, so more users cannot launch Logs at the same time and lose the PID
        with self._srv_lock:

            # Try to re-use the logger server, if available
            conn = self._services.get(user, {}).get('conn', None)
            if conn:
                try:
                    conn.ping(data='Hello', timeout=5.0)
                    # logDebug('Reuse old User Service connection for `{}` OK.'.format(user))
                    return conn
                except Exception as e:
                    logWarning('Cannot connect to User Service for `{}`: `{}`.'.format(user, e))
                    self._kill(user)
            else:
                logInfo('Launching a User Service for `{}`, the first time...'.format(user))

            port = None

            # If the server is not available, search for a free port in the safe range...
            while 1:
                port = random.randrange(63000, 65000)
                try:
                    socket.create_connection((None, port), 1)
                except:
                    break

            p_cmd = 'su {} -c "{} -u {}/server/UserService.py {} FS"'.format(user, sys.executable, TWISTER_PATH, port)
            proc = subprocess.Popen(p_cmd, cwd='{}/twister'.format(userHome(user)), shell=True,
                   close_fds=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            proc.poll()
            time.sleep(5.0)

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
                if success:
                    break

                try:
                    stream = rpyc.SocketStream.connect('127.0.0.1', port, timeout=5.0)
                    conn = rpyc.connect_stream(stream, config=config)
                    conn.root.hello()
                    logDebug('Connected to User Service for `{}`.'.format(user))
                    success = True
                    break
                except Exception as e:
                    logWarning('Cannot connect to User Service for `{}` - Exception: `{}`! '
                            'Wait {}s...'.format(user, e, delay))

                time.sleep(delay)
                retry -= 1
                delay += 0.75

            if not success:
                logError('Error on starting User Service for `{}`!'.format(user))
                return False

            # Save the process inside the block.  99% of the time, this block is executed instantly!
            self._services[user] = {'proc': proc, 'conn': conn, 'port': port}

        logDebug('User Service for `{}` launched on `127.0.0.1:{}` - PID `{}`.'.format(user, port, proc.pid))
        return conn


    # ----- USER ---------------------------------------------------------------


    def fileSize(self, user, fpath):
        """
        Get file size for 1 file. Client access via RPyc.
        """
        if not fpath:
            return False
        srvr = self._usrService(user)
        if srvr:
            return srvr.root.file_size(fpath)
        else:
            return False


    def readUserFile(self, user, fpath, flag='r', fstart=0):
        """
        Read 1 file. Client access via RPyc.
        """
        logDebug('Read {} {} {}'.format(user,fpath,fstart))
        if not fpath:
            return False
        srvr = self._usrService(user)
        if srvr:
            return srvr.root.read_file(fpath, flag, fstart)
        else:
            logError('Read {} {} {}'.format(user,fpath,fstart))
            return False


    def writeUserFile(self, user, fpath, fdata, flag='w'):
        """
        Read 1 file. Client access via RPyc.
        """
        if not fpath:
            return False
        srvr = self._usrService(user)
        if len(fdata) > 20*1000*1000:
            err = '*ERROR* File data too long `{}`: {}; User {}!'.format(fpath, len(fdata),user)
            logWarning(err)
            return err
        if srvr:
            return srvr.root.write_file(fpath, fdata, flag)
        else:
            return False


    def copyUserFile(self, user, fpath, newpath):
        if not fpath:
            return False
        srvr = self._usrService(user)
        if srvr:
            return srvr.root.copy_file(fpath, newpath)
        else:
            return False


    def moveUserFile(self, user, fpath, newpath):
        if not fpath:
            return False
        srvr = self._usrService(user)
        if srvr:
            return srvr.root.move_file(fpath, newpath)
        else:
            return False


    def deleteUserFile(self, user, fpath):
        if not fpath:
            return False
        srvr = self._usrService(user)
        if srvr:
            return srvr.root.delete_file(fpath)
        else:
            return False


    def createUserFolder(self, user, fdir):
        if not fdir:
            return False
        srvr = self._usrService(user)
        if srvr:
            return srvr.root.create_folder(fdir)
        else:
            return False


    def listUserFiles(self, user, fdir, hidden=True, recursive=True):
        if not fdir:
            return False
        srvr = self._usrService(user)
        if srvr:
            files = srvr.root.list_files(fdir, hidden, recursive)
            return copy.copy(files)
        else:
            return False


    def deleteUserFolder(self, user, fdir):
        if not fdir:
            return False
        srvr = self._usrService(user)
        if srvr:
            return srvr.root.delete_folder(fdir)
        else:
            return False


    def targzUserFolder(self, user, fdir):
        if not fdir:
            return False
        srvr = self._usrService(user)
        if srvr:
            return srvr.root.targz_folder(fdir)
        else:
            return False


    # ----- SYSTEM -------------------------------------------------------------


    @staticmethod
    def sysFileSize(fpath):
        """
        Get file size for 1 file. ROOT access.
        """
        if not fpath:
            return False
        try:
            fsize = os.stat(fpath).st_size
            # logDebug('File `{}` is size `{}`.'.format(fpath, fsize))
            return fsize
        except Exception as e:
            err = '*ERROR* Cannot find file `{}`! {}'.format(fpath, e)
            logWarning(err)
            return err


    @staticmethod
    def readSystemFile(fpath, flag='r', fstart=0):
        """
        Read 1 file. ROOT access.
        """
        if not fpath:
            return False
        if flag not in ['r', 'rb']:
            err = '*ERROR* Invalid flag `{}`! Cannot read!'.format(flag)
            logWarning(err)
            return err
        if not os.path.isfile(fpath):
            err = '*ERROR* No such file `{}`!'.format(fpath)
            logWarning(err)
            return err
        try:
            with open(fpath, flag) as f:
                # logDebug('Reading file `{}`, flag `{}`.'.format(fpath, flag))
                if fstart:
                    f.seek(fstart)
                fdata = f.read()
                if len(fdata) > 20*1000*1000:
                    err = '*ERROR* File data too long `{}`: {}!'.format(fpath, len(fdata))
                    logWarning(err)
                    return err
                return fdata
        except Exception as e:
            err = '*ERROR* Cannot read file `{}`! {}'.format(fpath, e)
            logWarning(err)
            return err


    @staticmethod
    def writeSystemFile(fpath, fdata, flag='a'):
        """
        Write data in a file. ROOT access.
        Overwrite or append, ascii or binary.
        """
        if not fpath:
            return False
        if flag not in ['w', 'wb', 'a', 'ab']:
            err = '*ERROR* Invalid flag `{}`! Cannot read!'.format(flag)
            logWarning(err)
            return err
        try:
            with open(fpath, flag) as f:
                f.write(fdata)
            # if flag == 'w':
            #     logDebug('Written `{}` chars in ascii file `{}`.'.format(len(fdata), fpath))
            # elif flag == 'wb':
            #     logDebug('Written `{}` chars in binary file `{}`.'.format(len(fdata), fpath))
            # elif flag == 'a':
            #     logDebug('Appended `{}` chars in ascii file `{}`.'.format(len(fdata), fpath))
            # else:
            #     logDebug('Appended `{}` chars in binary file `{}`.'.format(len(fdata), fpath))
            return True
        except Exception as e:
            err = '*ERROR* Cannot write into file `{}`! {}'.format(fpath, e)
            logWarning(err)
            return err


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
