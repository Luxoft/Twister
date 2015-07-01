
# File: helpers.py ; This file is part of Twister.

# version: 3.008

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
This module contains a lot of helper, common functions.
"""

import os
import sys
import re
import time
import binascii
import platform
import subprocess
from functools import wraps
from thread import allocate_lock

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

from common.tsclogging import logFull, logDebug, logWarning

#

class FsBorg(object):

    _shared_state = {}
    project = None
    _services = {}
    _srv_lock = allocate_lock()

    def __init__(self):
        self.__dict__ = self._shared_state


class CcBorg(object):

    _shared_state = {}
    project = None
    _services = {}
    _srv_lock = allocate_lock()

    def __init__(self):
        self.__dict__ = self._shared_state


def cache_ttl(ttl=1):
    """
    Caching decorator within TTL period in seconds.

    Example use:

        import time, random

        @cache_ttl(60)
        def randint():
            # will only be evaluated every 60 sec at maximum.
            return random.randint(0, 100)

        print randint()
        print randint()
        time.sleep(1)
        print randint()
        print randint()

    """
    saved = {}

    def cache(func):
        @wraps(func)
        def memoizer(*args, **kwargs):
            now = time.time()
            key = str(args) + str(kwargs)
            if key in saved:
                last_update = saved[key]['t']
                if now - last_update <= ttl:
                    return saved[key]['r']
            result = func(*args, **kwargs)
            saved[key] = {'t': now, 'r': result}
            return result
        return memoizer
    return cache


@cache_ttl(3600)
def userHome(user):
    """
    Find the home folder for the given user.
    """
    return subprocess.check_output('echo ~' + user, shell=True).strip()


def setFileOwner(user, path):
    """
    Update file ownership for 1 file or folder.\n
    `Chown` function works ONLY in Linux.
    """
    logFull('helpers:setFileOwner user `{}`.'.format(user))
    try:
        from pwd import getpwnam
        uid = getpwnam(user)[2]
        gid = getpwnam(user)[3]
    except:
        return False

    if os.path.isdir(path):
        try:
            proc = subprocess.Popen(['chown', str(uid)+':'+str(gid), path, '-R', '--silent'],)
            proc.wait()
        except:
            logWarning('Cannot change owner! Cannot chown folder `{}:{}` on `{} -R`!'.format(uid, gid, path))
            return False

    else:
        try:
            os.chown(path, uid, gid)
        except:
            logWarning('Cannot set owner! Cannot chown file `{}:{}` on `{}`!'.format(uid, gid, path))
            return False

    return True


def getFileTags(fname):
    """
    Returns the title, description and all tags from a test file.
    """
    logFull('helpers:getFileTags')
    try:
        text = open(fname, 'rb').read()
    except:
        return ''

    # Find lines starting with # or beggining of line, followed by optional space,
    # followed by a <tag> ended with the same </tag> containing any character
    # in range 0x20 to 0x7e (all numbers, letters and ASCII symbols)
    # This returns 2 groups : the tag name and the text inside it.
    tags = re.findall('^[ ]*?[#]*?[ ]*?<(?P<tag>\w+)>([ -~\n]+?)</(?P=tag)>', text, re.MULTILINE)

    return '<br>\n'.join(['<b>' + title + '</b> : ' + descr for title, descr in tags])


def dirList(tests_path, path, newdict):
    """
    Create recursive list of folders and files from Tests path.
    The format of a node is: {"data": "name", "attr": {"rel": "folder"}, "children": []}
    """
    logFull('helpers:dirList')
    len_path = len(tests_path) + 1
    if os.path.isdir(path):
        dlist = [] # Folders list
        flist = [] # Files list
        for fname in sorted(os.listdir(path), key=str.lower):
            short_path = (path + os.sep + fname)[len_path:]
            c_nd = {'data': short_path, 'children': []}
            if os.path.isdir(path + os.sep + fname):
                c_nd['attr'] = {'rel': 'folder'}
                dlist.append(c_nd)
            else:
                flist.append(c_nd)
        # Folders first, files second
        newdict['children'] = dlist + flist
    for nitem in newdict['children']:
        # Recursive !
        dirList(tests_path, tests_path + os.sep + nitem['data'], nitem)


def calcMemory():
    """
    Calculate used memory percentage.
    """
    mem_line = subprocess.check_output(['free', '-o']).split('\n')[1]
    mem_used = int(mem_line.split()[2])
    meb_buff = int(mem_line.split()[-2])
    mem_cache = int(mem_line.split()[-1])
    total = float(mem_line.split()[1])
    mem_per = ((mem_used - meb_buff - mem_cache) * 100.) / total
    return float('%.2f' % mem_per)

def _getCpuData():
    """ Helper function """
    stat_line = open('/proc/stat', 'r').readline()
    time_list = stat_line.split(' ')[2:6]
    for i in range(len(time_list)):
        time_list[i] = float(time_list[i])
    return time_list

def calcCpu():
    """
    Calculate used CPU percentage.
    """
    x_val = _getCpuData()
    time.sleep(0.5)
    y_val = _getCpuData()
    for i in range(len(x_val)):
        y_val[i] -= x_val[i]
    cpu_per = sum(y_val[:-1]) / sum(y_val) * 100.
    return float('%.2f' % cpu_per)


@cache_ttl(3600)
def systemInfo():
    """
    Returns some system information.
    """
    logFull('helpers:systemInfo')
    system = platform.machine() +' '+ platform.system() +', '+ ' '.join(platform.linux_distribution())
    python = '.'.join([str(v) for v in sys.version_info])
    return '{}\nPython {}'.format(system.strip(), python)


def execScript(script_path):
    """
    Execute a user script and return the text printed on the screen.
    """
    logFull('helpers:execScript')
    if not os.path.exists(script_path):
        logWarning('Exec script: The path `{}` does not exist!'.format(script_path))
        return False

    try:
        os.system('chmod +x {}'.format(script_path))
    except:
        pass

    logDebug('Executing script `{}`...'.format(script_path))

    try:
        txt = subprocess.check_output(script_path, shell=True)
        return txt.strip()
    except Exception as exp_err:
        logWarning('Exec script `{}`: Exception - `{}`.'.\
        format(script_path, exp_err))
        return False


def encrypt(bdata, encr_key):
    """
    Encrypt some data.
    """
    logFull('helpers:encrypt')
    # Enhance user password with PBKDF2
    pwd = PBKDF2(password=encr_key, salt='^0Twister-Salt9$', dkLen=32, count=100)
    crypt = AES.new(pwd)
    pad_len = 16 - (len(bdata) % 16)
    padding = (chr(pad_len) * pad_len)
    # Encrypt user data + correct padding
    data = crypt.encrypt(bdata + padding)
    return binascii.hexlify(data)


def decrypt(bdata, encr_key):
    """
    Decrypt some data.
    """
    logFull('helpers:decrypt')
    # Enhance user password with PBKDF2
    pwd = PBKDF2(password=encr_key, salt='^0Twister-Salt9$', dkLen=32, count=100)
    crypt = AES.new(pwd)
    try:
        data = binascii.unhexlify(bdata)
    except:
        return ''
    try:
        decrypted = crypt.decrypt(data)
    except:
        return ''
    pad_len = ord(decrypted[-1])
    # Trim the padding
    return decrypted[:-pad_len]


# Eof()
