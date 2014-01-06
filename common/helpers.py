
# File: helpers.py ; This file is part of Twister.

# version: 3.002

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

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

from tsclogging import logFull, logDebug, logWarning

#

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
    try: text = open(fname,'rb').read()
    except: return ''

    # Find lines starting with # or beggining of line, followed by optional space,
    # followed by a <tag> ended with the same </tag> containing any character
    # in range 0x20 to 0x7e (all numbers, letters and ASCII symbols)
    # This returns 2 groups : the tag name and the text inside it.
    tags = re.findall('^[ ]*?[#]*?[ ]*?<(?P<tag>\w+)>([ -~\n]+?)</(?P=tag)>', text, re.MULTILINE)

    return '<br>\n'.join(['<b>' + title + '</b> : ' + descr.replace('<', '&lt;') for title, descr in tags])


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
            nd = {'data': short_path, 'children': []}
            if os.path.isdir(path + os.sep + fname):
                nd['attr'] = {'rel': 'folder'}
                dlist.append(nd)
            else:
                flist.append(nd)
        # Folders first, files second
        newdict['children'] = dlist + flist
    for nitem in newdict['children']:
        # Recursive !
        dirList(tests_path, tests_path + os.sep + nitem['data'], nitem)


def calcMemory():
    """
    Calculate used memory percentage.
    """
    logFull('helpers:calcMemory')
    memLine = subprocess.check_output(['free', '-o']).split('\n')[1]
    memUsed  = int(memLine.split()[2])
    mebBuff  = int(memLine.split()[-2])
    memCache = int(memLine.split()[-1])
    Total    = float(memLine.split()[1])
    memPer = ((memUsed - mebBuff - memCache) * 100.) / Total
    return float('%.2f' % memPer)

def _getCpuData():
    """ Helper function """
    statLine = open('/proc/stat', 'r').readline()
    timeList = statLine.split(' ')[2:6]
    for i in range(len(timeList)):
        timeList[i] = float(timeList[i])
    return timeList

def calcCpu():
    """
    Calculate used CPU percentage.
    """
    logFull('helpers:calcCpu')
    x = _getCpuData()
    time.sleep(0.5)
    y = _getCpuData()
    for i in range(len(x)):
        y[i] -= x[i]
    cpuPer = sum(y[:-1]) / sum(y) * 100.
    return float('%.2f' % cpuPer)


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

    try: os.system('chmod +x {}'.format(script_path))
    except: pass

    logDebug('Executing script `{}`...'.format(script_path))

    try:
        txt = subprocess.check_output(script_path, shell=True)
        return txt.strip()
    except Exception as e:
        logWarning('Exec script `{}`: Exception - `{}`.'.format(script_path, e))
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
    try: data = binascii.unhexlify(bdata)
    except : return ''
    try: decrypted = crypt.decrypt(data)
    except: return ''
    pad_len = ord(decrypted[-1])
    # Trim the padding
    return decrypted[:-pad_len]


# Eof()
