
# File: UserService.py ; This file is part of Twister.

# version: 3.015

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
import re
import sys
import pwd
import grp
import time
import shutil
import subprocess
import tarfile
import cStringIO
import multiprocessing


import rpyc
from rpyc.utils.server import ThreadedServer

TYPE = sys.argv[2:3]

if TYPE == ['ClearCase']:
    log_file = 'clear_srv.log'
else:
    log_file = 'usr_srv.log'

def log_msg(level, msg):
    """ common logger """
    date_tag = time.strftime('%Y-%b-%d %H-%M-%S')
    with open(log_file, 'a') as f:
        f.write('{}\t{}\t{}\n'.format(date_tag, level, msg))

def logDebug(msg):
    """ debug """
    log_msg("DEBUG", msg)

def logInfo(msg):
    """ info """
    log_msg("INFO", msg)

def logWarning(msg):
    """ warning """
    log_msg("WARN", msg)

def logError(msg):
    """ error """
    log_msg("ERROR", msg)

pattern = re.compile('from[\s]+([\w]+).*?[\s]+import|[\s]*import[\s]+([\w]+)[\s]*\n')

def worker(files):
    """
    A worker that parses a batch of tests. Returns all the import statements found.
    """
    missing = set([])
    for file in files:
        f = open(file, 'r')
        data = f.read()
        f.close()
        imports = pattern.findall(data)
        missing.update([i[0] or i[1] for i in imports])
    return sorted(missing)

if sys.version < '2.7':
    logError('Python version error! User Service must run on Python 2.7++ !')
    exit(1)


lastMsg = ''

#

class UserService(rpyc.Service):

    def __init__(self, conn):
        logInfo('Warming up the User Service ({})...'.format(TYPE))
        self._conn = conn


    def on_connect(self):
        client_addr = self._conn._config['endpoints'][1]
        logDebug('User Service: Connected from endpoint `{}`.'.format(client_addr))


    def on_disconnect(self):
        client_addr = self._conn._config['endpoints'][1]
        logDebug('User Service: Disconnected from endpoint `{}`.'.format(client_addr))


    @staticmethod
    def exposed_hello():
        """
        Say hello to server.
        """
        return True


    @staticmethod
    def exposed_is_folder(fpath):
        """
        True or False ?
        """
        if fpath[0] == '~':
            fpath = USER_HOME + fpath[1:]
        try:
            return os.path.isdir(fpath)
        except Exception as e:
            err = '*ERROR* Cannot find file/ folder `{}`! {}'.format(fpath, e)
            logWarning(err)
            return err


    @staticmethod
    def exposed_file_size(fpath):
        """
        Get file size for 1 file.
        Less spam, please.
        """
        global lastMsg
        if fpath[0] == '~':
            fpath = USER_HOME + fpath[1:]
        try:
            fsize = os.stat(fpath).st_size
            msg = 'File `{}` is size `{}`.'.format(fpath, fsize)
            if msg != lastMsg:
                logDebug(msg)
                lastMsg = msg
            return fsize
        except Exception as e:
            err = '*ERROR* Cannot find file `{}`! {}'.format(fpath, e)
            logWarning(err)
            return err


    @staticmethod
    def exposed_read_file(fpath, flag='r', fstart=0):
        """
        Read 1 file.
        Less spam, please.
        """
        global lastMsg
        if fpath[0] == '~':
            fpath = USER_HOME + fpath[1:]
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
                msg = 'Reading file `{}`, flag `{}`.'.format(fpath, flag)
                if msg != lastMsg:
                    logDebug(msg)
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
            logWarning(err)
            return err


    @staticmethod
    def exposed_write_file(fpath, fdata, flag='a'):
        """
        Write data in a file.
        Overwrite or append, ascii or binary.
        Show me the spam.
        """
        if fpath[0] == '~':
            fpath = USER_HOME + fpath[1:]
        if flag not in ['w', 'wb', 'a', 'ab']:
            err = '*ERROR* Invalid flag `{}`! Cannot read!'.format(flag)
            logWarning(err)
            return err
        try:
            with open(fpath, flag) as f:
                f.write(fdata)
            if flag == 'w':
                logDebug('Written `{}` chars in ascii file `{}`.'.format(len(fdata), fpath))
            elif flag == 'wb':
                logDebug('Written `{}` chars in binary file `{}`.'.format(len(fdata), fpath))
            elif flag == 'a':
                logDebug('Appended `{}` chars in ascii file `{}`.'.format(len(fdata), fpath))
            else:
                logDebug('Appended `{}` chars in binary file `{}`.'.format(len(fdata), fpath))
            return True
        except Exception as e:
            err = '*ERROR* Cannot write into file `{}`! {}'.format(fpath, e)
            logWarning(err)
            return err


    @staticmethod
    def exposed_copy_file(fpath, newpath):
        """
        Copy 1 file.
        """
        if fpath[0] == '~':
            fpath = USER_HOME + fpath[1:]
        if newpath[0] == '~':
            newpath = USER_HOME + newpath[1:]
        try:
            shutil.copy2(fpath, newpath)
            logDebug('Copied file `{}` in `{}`.'.format(fpath, newpath))
            return True
        except Exception as e:
            err = '*ERROR* Cannot copy file `{}`! {}'.format(fpath, e)
            logWarning(err)
            return err


    @staticmethod
    def exposed_move_file(fpath, newpath):
        """
        Move 1 file.
        """
        if fpath[0] == '~':
            fpath = USER_HOME + fpath[1:]
        if newpath[0] == '~':
            newpath = USER_HOME + newpath[1:]
        try:
            shutil.move(fpath, newpath)
            logDebug('Moved file `{}` in `{}`.'.format(fpath, newpath))
            return True
        except Exception as e:
            err = '*ERROR* Cannot move file `{}`! {}'.format(fpath, e)
            logWarning(err)
            return err


    @staticmethod
    def exposed_delete_file(fpath):
        """
        Delete a file. This is IREVERSIBLE!
        """
        if fpath[0] == '~':
            fpath = USER_HOME + fpath[1:]
        try:
            os.remove(fpath)
            logDebug('Deleted file `{}`.'.format(fpath))
            return True
        except Exception as e:
            err = '*ERROR* Cannot delete file `{}`! {}'.format(fpath, e)
            logWarning(err)
            return err


    @staticmethod
    def exposed_create_folder(folder):
        """
        Create a new folder.
        """
        if folder[0] == '~':
            folder = USER_HOME + folder[1:]
        try:
            os.makedirs(folder)
            logDebug('Created folder `{}`.'.format(folder))
            return True
        except Exception as e:
            err = '*ERROR* Cannot create folder `{}`! {}'.format(folder, e)
            logWarning(err)
            return err


    @staticmethod
    def exposed_list_files(folder, hidden=True, recursive=True, accept=[], reject=[]):
        """
        List all files, recursively.
        """
        if folder[0] == '~':
            folder = USER_HOME + folder[1:]
        if folder == '/':
            base_path = '/'
            logWarning('*WARN* Listing folders from system ROOT.')
            recursive = False
        else:
            base_path = folder.rstrip('/')

        if not os.path.isdir(folder):
            err = '*ERROR* Invalid folder path `{}`!'.format(folder)
            logWarning(err)
            return err

        def dirList(path):
            """
            Create recursive list of folders and files from base path.
            The format of a node is: {"path": "/..." "data": "name", "folder":true|false, "children": []}
            """
            # The node is valid ?
            if not path:
                return False
            # Cleanup '/'
            if path != '/':
                path = path.rstrip('/')
            # This is folder ?
            if os.path.isfile(path):
                return False

            len_path = len(base_path) + 1
            dlist = [] # Folders list
            flist = [] # Files list

            try:
                names = sorted(os.listdir(path), key=str.lower)
            except Exception as e:
                logWarning('*WARN* Cannot list folder `{}`: `{}`!'.format(path, e))
                return []

            # Cycle a folder
            for fname in names:
                long_path  = path + '/' + fname

                # If Accept is active and file doesn't match, ignore file
                if accept and os.path.isfile(long_path):
                    valid = True
                    if isinstance(accept, list):
                        # If nothing from the Accept matches the file
                        if True not in [(long_path.startswith(f) or long_path.endswith(f)) for f in accept]:
                            valid = False
                    elif isinstance(accept, str):
                        if not (long_path.startswith(accept) or long_path.endswith(accept)):
                            valid = False
                    if not valid:
                        continue

                # If Reject is active and file matches, ignore the file
                if reject and os.path.isfile(long_path):
                    valid = True
                    if isinstance(reject, list):
                        # If nothing from the Reject matches the file
                        if True in [(long_path.startswith(f) or long_path.endswith(f)) for f in reject]:
                            valid = False
                    elif isinstance(reject, str):
                        if long_path.startswith(reject) or long_path.endswith(reject):
                            valid = False
                    if not valid:
                        continue

                # Ignore hidden files
                if hidden and fname[0] == '.':
                    continue
                # Meta info
                try:
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
                except Exception:
                    meta_info = ''

                # Semi long path
                short_path = long_path[len_path:]
                # Data to append
                nd = {'path': short_path, 'data': fname, 'meta': meta_info}

                if os.path.isdir(long_path):
                    nd['folder'] = True
                    # Recursive !
                    if recursive:
                        children = dirList(long_path)
                    else:
                        children = []
                    if children in [False, None]:
                        continue
                    nd['children'] = children
                    dlist.append(nd)
                else:
                    flist.append(nd)

            # Folders first, files second
            return dlist + flist

        paths = {
            'path' : '/',
            'data' : base_path,
            'folder' : True,
            'children' : dirList(base_path) or []
        }

        clen = len(paths['children'])
        logDebug('Listing dir `{}`, it has `{}` direct children.'.format(base_path, clen))
        return paths


    @staticmethod
    def exposed_delete_folder(folder):
        """
        Create a user folder.
        """
        if folder[0] == '~':
            folder = USER_HOME + folder[1:]
        try:
            shutil.rmtree(folder)
            logDebug('Deleted folder `{}`.'.format(folder))
            return True
        except Exception as e:
            err = '*ERROR* Cannot delete folder `{}`! {}'.format(folder, e)
            logWarning(err)
            return err


    @staticmethod
    def exposed_targz_folder(folder, root=''):
        """
        Compress a folder in memory and return the result.
        """
        if (root not in folder) or (not os.path.isdir(root)):
            root = ''
        if folder[0] == '~':
            folder = USER_HOME + folder[1:]
        if not os.path.exists(folder):
            err = '*ERROR* Invalid path `{}`!'.format(folder)
            logWarning(err)
            return err
        if root:
            name = folder[len(root):]
        else:
            root, name = os.path.split(folder)
        logDebug('Tar.gz folder: `{}`, root: `{}`.'.format(name, root))
        os.chdir(root)
        io = cStringIO.StringIO()
        # Write the folder tar.gz into memory
        with tarfile.open(fileobj=io, mode='w:gz') as binary:
            binary.add(name=name, recursive=True)
        return io.getvalue()


    @staticmethod
    def exposed_detect_libraries(files):
        """
        Autodetect libraries: parses all the tests and finds the import statements.
        Returns a list of the modules not available by default in python path.
        """
        numthreads = 4*multiprocessing.cpu_count()
        num_files = len(files)/numthreads

        # create the process pool
        pool = multiprocessing.Pool(processes=numthreads)
        #start = time.time()
        result_list = pool.map(worker, (files[i*num_files:((i+1)*num_files if i != numthreads-1 else len(files))] for i in range(0,numthreads)))
        #print 'Total time: {}'.format(time.time() - start)

        result = []

        for l in result_list:
            result+=l

        old_stdout = sys.stdout
        new_stdout = cStringIO.StringIO()
        new_stdout.flush()
        sys.stdout = new_stdout
        help('modules')
        sys.stdout = old_stdout
        modules = new_stdout.getvalue().split('\n')[3:-5]
        avail_modules = []
        modules = map((lambda m:avail_modules.extend(re.sub('[\s]+',' ',m).split(' '))), modules)

        result_list = sorted(set(result) - set(avail_modules))
        return result_list


    @staticmethod
    def exposed_exit():
        """ Must Exit """
        logWarning('User Service: *sigh* received EXIT signal...')
        t.close()
        # Reply to client.
        return True

#

if __name__ == '__main__':

    PORT = sys.argv[1:2]

    if not PORT:
        logError('User Service: Must start with parameter PORT number!')
        exit(1)

    config = {
        'allow_pickle': True,
        'allow_getattr': True,
        'allow_setattr': True,
        'allow_delattr': True
    }

    try:
        userName = os.getenv('USER') or os.getenv('USERNAME')
        if userName == 'root':
            userName = os.getenv('SUDO_USER') or userName
        logDebug('Hello username `{}`!'.format(userName))
    except Exception:
        userName = ''
    if not userName:
        logError('Cannot guess user name for the User Service! Exiting!')
        exit(1)

    open(log_file, 'w').close()

    logInfo('User Service: Starting...')

    USER_HOME = subprocess.check_output('echo ~' + userName, shell=True).strip().rstrip('/')

    t = ThreadedServer(UserService, port=int(PORT[0]), protocol_config=config, listener_timeout=1)
    t.start()

    logInfo('User Service: Bye bye.')


# Eof()
