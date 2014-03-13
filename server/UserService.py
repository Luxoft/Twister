
# File: UserService.py ; This file is part of Twister.

# version: 3.003

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

"""
User Service, based on RPyc.
This process runs in the Twister Client folder.
"""

import os
import sys
import pwd
import grp
import time
import shutil
import subprocess
import logging

import rpyc
from rpyc.utils.server import ThreadedServer


log = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.NOTSET,
    format='%(asctime)s  %(levelname)-8s %(message)s',
    datefmt='%y-%m-%d %H:%M:%S',
    filename='usr_srv.log',
    filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.NOTSET)
log.addHandler(console)


if sys.version < '2.7':
    log.error('Python version error! User Service must run on Python 2.7++ !')
    exit(1)

try:
    userName = os.getenv('USER') or os.getenv('USERNAME')
    if userName == 'root':
        userName = os.getenv('SUDO_USER') or userName
    log.debug('Hello username `{}`!'.format(userName))
except Exception:
    userName = ''
if not userName:
    log.error('Cannot guess user name for the User Service! Exiting!')
    exit(1)

def userHome():
    """
    Find the home folder for a given user.
    """
    return subprocess.check_output('echo ~' + userName, shell=True).strip().rstrip('/')

lastMsg = ''

#

class UserService(rpyc.Service):

    def __init__(self, conn):
        log.debug('Warming up the User Service...')
        self._conn = conn


    def on_connect(self):
        client_addr = self._conn._config['endpoints'][1]
        log.debug('Connected from `{}`.'.format(client_addr))


    def on_disconnect(self):
        client_addr = self._conn._config['endpoints'][1]
        log.debug('Disconnected from `{}`.'.format(client_addr))


    @staticmethod
    def exposed_hello():
        """
        Say hello to server.
        """
        return True


    @staticmethod
    def exposed_file_size(fpath):
        """
        Get file size for 1 file.
        """
        global lastMsg
        if fpath[0] == '~':
            fpath = userHome() + fpath[1:]
        try:
            fsize = os.stat(fpath).st_size
            msg = 'File `{}` is size `{}`.'.format(fpath, fsize)
            if msg != lastMsg:
                log.debug(msg)
                lastMsg = msg
            return fsize
        except Exception as e:
            err = '*ERROR* Cannot find file `{}`! {}'.format(fpath, e)
            log.warning(err)
            return err


    @staticmethod
    def exposed_read_file(fpath, flag='r', fstart=0):
        """
        Read 1 file.
        """
        global lastMsg
        if fpath[0] == '~':
            fpath = userHome() + fpath[1:]
        if flag not in ['r', 'rb']:
            err = '*ERROR* Invalid flag `{}`! Cannot read!'.format(flag)
            log.warning(err)
            return err
        if not os.path.isfile(fpath):
            err = '*ERROR* No such file `{}`!'.format(fpath)
            log.warning(err)
            return err
        try:
            with open(fpath, flag) as f:
                msg = 'Reading file `{}`, flag `{}`.'.format(fpath, flag)
                if msg != lastMsg:
                    log.debug(msg)
                    lastMsg = msg
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
            log.warning(err)
            return err


    @staticmethod
    def exposed_write_file(fpath, fdata, flag='a'):
        """
        Write data in a file.
        Overwrite or append, ascii or binary.
        """
        if fpath[0] == '~':
            fpath = userHome() + fpath[1:]
        if flag not in ['w', 'wb', 'a', 'ab']:
            err = '*ERROR* Invalid flag `{}`! Cannot read!'.format(flag)
            log.warning(err)
            return err
        try:
            with open(fpath, flag) as f:
                f.write(fdata)
            if flag == 'w':
                log.debug('Written `{}` chars in ascii file `{}`.'.format(len(fdata), fpath))
            elif flag == 'wb':
                log.debug('Written `{}` chars in binary file `{}`.'.format(len(fdata), fpath))
            elif flag == 'a':
                log.debug('Appended `{}` chars in ascii file `{}`.'.format(len(fdata), fpath))
            else:
                log.debug('Appended `{}` chars in binary file `{}`.'.format(len(fdata), fpath))
            return True
        except Exception as e:
            err = '*ERROR* Cannot write into file `{}`! {}'.format(fpath, e)
            log.warning(err)
            return err


    @staticmethod
    def exposed_copy_file(fpath, newpath):
        """
        Copy 1 file.
        """
        if fpath[0] == '~':
            fpath = userHome() + fpath[1:]
        if newpath[0] == '~':
            newpath = userHome() + newpath[1:]
        try:
            shutil.copy2(fpath, newpath)
            log.debug('Copied file `{}` in `{}`.'.format(fpath, newpath))
            return True
        except Exception as e:
            err = '*ERROR* Cannot copy file `{}`! {}'.format(fpath, e)
            log.warning(err)
            return err


    @staticmethod
    def exposed_move_file(fpath, newpath):
        """
        Move 1 file.
        """
        if fpath[0] == '~':
            fpath = userHome() + fpath[1:]
        if newpath[0] == '~':
            newpath = userHome() + newpath[1:]
        try:
            shutil.move(fpath, newpath)
            log.debug('Moved file `{}` in `{}`.'.format(fpath, newpath))
            return True
        except Exception as e:
            err = '*ERROR* Cannot move file `{}`! {}'.format(fpath, e)
            log.warning(err)
            return err


    @staticmethod
    def exposed_delete_file(fpath):
        """
        Delete a file. This is IREVERSIBLE!
        """
        if fpath[0] == '~':
            fpath = userHome() + fpath[1:]
        try:
            os.remove(fpath)
            log.debug('Deleted file `{}`.'.format(fpath))
            return True
        except Exception as e:
            err = '*ERROR* Cannot delete file `{}`! {}'.format(fpath, e)
            log.warning(err)
            return err


    @staticmethod
    def exposed_create_folder(folder):
        """
        Create a new folder.
        """
        if folder[0] == '~':
            folder = userHome() + folder[1:]
        try:
            os.makedirs(folder)
            log.debug('Created folder `{}`.'.format(folder))
            return True
        except Exception as e:
            err = '*ERROR* Cannot create folder `{}`! {}'.format(folder, e)
            log.warning(err)
            return err


    @staticmethod
    def exposed_list_files(folder, hidden=True):
        """
        List all files, recursively.
        """
        if folder[0] == '~':
            folder = userHome() + folder[1:]
        if folder == '/':
            err = '*ERROR* Cannot list ROOT folder!'
            log.warning(err)
            return err

        def dirList(base_path, path, new_dict):
            """
            Create recursive list of folders and files from base path.
            The format of a node is: {"path": "/..." "data": "name", "folder":true|false, "children": []}
            """
            len_path = len(base_path) + 1
            if os.path.isdir(path):
                dlist = [] # Folders list
                flist = [] # Files list
                for fname in sorted(os.listdir(path), key=str.lower):
                    # Ignore hidden files
                    if hidden and fname[0] == '.':
                        continue
                    long_path  = path + os.sep + fname
                    short_path = (long_path)[len_path:]
                    fstat = os.stat(long_path)
                    try:
                        uname = pwd.getpwuid(fstat.st_uid).pw_name
                    except Exception:
                        uname = fstat.st_uid
                    try:
                        gname = grp.getgrgid(fstat.st_gid).gr_name
                    except Exception:
                        gname = fstat.st_gid
                    meta_info = '{}|{}|{}|{}'.format(uname, gname, fstat.st_size,
                        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(fstat.st_mtime)))
                    nd = {'path': short_path, 'data': fname, 'meta': meta_info}
                    if os.path.isdir(long_path):
                        nd['folder'] = True
                        nd['children'] = []
                        dlist.append(nd)
                    else:
                        flist.append(nd)
                # Folders first, files second
                new_dict['children'] = dlist + flist
            for nitem in new_dict.get('children', []):
                # Recursive !
                dirList(base_path, base_path + os.sep + nitem['path'], nitem)

        if not os.path.isdir(folder):
            err = '*ERROR* Folder path `{}`!'.format(folder)
            log.warning(err)
            return err

        paths = {'path':'/', 'data':folder, 'folder':True, 'children':[]}
        dirList(folder, folder, paths)
        clen = len(paths['children'])
        log.debug('Listing dir `{}`, it has `{}` direct children.'.format(folder, clen))
        return paths


    @staticmethod
    def exposed_delete_folder(folder):
        """
        Create a user folder.
        """
        if folder[0] == '~':
            folder = userHome() + folder[1:]
        try:
            shutil.rmtree(folder)
            log.debug('Deleted folder `{}`.'.format(folder))
            return True
        except Exception as e:
            err = '*ERROR* Cannot delete folder `{}`! {}'.format(folder, e)
            log.warning(err)
            return err


    @staticmethod
    def exposed_exit():
        """ Must Exit """
        log.warning('User Service: *sigh* received EXIT signal...')
        t.close()
        # Reply to client.
        return True

#

if __name__ == '__main__':

    PORT = sys.argv[1:2]

    if not PORT:
        log.error('User Service: Must start with parameter PORT number!')
        exit(1)

    config = {
        'allow_pickle': True,
        'allow_getattr': True,
        'allow_setattr': True,
        'allow_delattr': True
    }

    t = ThreadedServer(UserService, port=int(PORT[0]), protocol_config=config)
    t.start()

    log.warning('User Service: Bye bye.')


# Eof()
