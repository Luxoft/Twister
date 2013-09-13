
# File: helpers.py ; This file is part of Twister.

# version: 2.002

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
import re
import binascii
import subprocess

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

from tsclogging import logDebug, logWarning

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
    try:
        from pwd import getpwnam
        uid = getpwnam(user)[2]
        gid = getpwnam(user)[3]
    except:
        return False

    if os.path.isdir(path):
        try:
            proc = subprocess.Popen(['chown', str(uid)+':'+str(gid), path, '-R'],)
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
    try: text = open(fname,'rb').read()
    except: return ''

    # Find lines starting with # or beggining of line, followed by optional space,
    # followed by a <tag> ended with the same </tag> containing any character
    # in range 0x20 to 0x7e (all numbers, letters and ASCII symbols)
    # This returns 2 groups : the tag name and the text inside it.
    tags = re.findall('^[ ]*?[#]*?[ ]*?<(?P<tag>\w+)>([ -~\n]+?)</(?P=tag)>', text, re.MULTILINE)

    return '<br>\n'.join(['<b>' + title + '</b> : ' + descr.replace('<', '&lt;') for title, descr in tags])


def execScript(script_path):
    """
    Execute a user script and return the text printed on the screen.
    """
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
