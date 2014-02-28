
# File: UserService.py ; This file is part of Twister.

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

"""
User Service, based on RPyc.
This process runs in the Twister Client folder.
"""

import os, sys
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
    if userName=='root':
        userName = os.getenv('SUDO_USER') or userName
    log.debug('Hello username `{}`!'.format(userName))
except:
    userName = ''
if not userName:
    log.error('Cannot guess user name for the User Service! Exiting!')
    exit(1)

def userHome():
    """
    Find the home folder for a given user.
    """
    global userName
    return subprocess.check_output('echo ~' + userName, shell=True).strip()

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


    def exposed_hello(self):
        return True


    def exposed_read_file(self, fpath):
        """
        Read 1 file.
        """
        if fpath[0] == '~':
            fpath = userHome() + fpath[1:]
        try:
            with open(fpath, 'r') as f:
                return f.read()
        except Exception as e:
            err = '*ERROR* Cannot read file `{}`! {}'.format(fpath, e)
            log.warning(err)
            return err


    def exposed_write_file(self, fpath, fdata, mode='w'):
        """
        Write data in a file.
        Overwrite, or append.
        """
        if fpath[0] == '~':
            fpath = userHome() + fpath[1:]
        try:
            with open(fpath, mode) as f:
                f.write(fdata)
            if mode == 'a':
                log.debug('Appended `{}` chars in file `{}`.'.format(len(fdata), fpath))
            else:
                log.debug('Written `{}` chars in file `{}`.'.format(len(fdata), fpath))
            return True
        except Exception as e:
            err = '*ERROR* Cannot write into file `{}`! {}'.format(fpath, e)
            log.warning(err)
            return err


    def exposed_copy_file(self, fpath, newpath):
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


    def exposed_move_file(self, fpath, newpath):
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


    def exposed_delete_file(self, fpath):
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


    def exposed_create_folder(self, folder):
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


    def exposed_list_files(self, folder):
        """
        List all files, recursively.
        """
        if folder[0] == '~':
            folder = userHome() + folder[1:]

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
                    short_path = (path + os.sep + fname)[len_path:]
                    nd = {'path': short_path, 'data': fname}
                    if os.path.isdir(path + os.sep + fname):
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
            err = '*ERROR* Invalid config path `{}`!'.format(folder)
            log.warning(err)
            return err

        paths = {'path':'/', 'data':folder, 'folder':True, 'children':[]}
        dirList(folder, folder, paths)
        return paths


    def exposed_delete_folder(self, folder):
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


    def exposed_exit(self):
        """ Must Exit """
        global t, log
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
