#!/usr/bin/env python2.7

# version: 3.001

# File: setup_shared_db.py ; This file is part of Twister.

# Copyright (C) 2012-2014, Luxoft

# Authors:
#    Andrei Costachi <acostachi@luxoft.com>
#    Cristi Constantin <crconstantin@luxoft.com>
#    Mihai Dobre <mihdobre@luxoft.com>

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import binascii
from lxml import etree
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2


if sys.version_info[0] != 2 and sys.version_info[1] != 7:
    print('\nPython version must be 2.7! Exiting!\n')
    exit(1)

if os.getuid() != 0:
    print('\nSetup Shared DB must run with ROOT! Exiting!\n')
    exit(1)

TWISTER_PATH = '/opt/twister'


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


def setup_server():
    """ Setup """
    print('\nPlease type the IP or name of the MySQL server.')
    print('Type a name to change, or press ENTER to skip.')
    data = ''
    if db_xml.xpath('server_section/db_config/server/text()'):
        data = db_xml.xpath('server_section/db_config/server')[0].text
    selected = raw_input('[Currently `{}`] : '.format(data))
    if selected:
        node = db_xml.xpath('server_section/db_config/server')[0]
        node.text = selected


def setup_database():
    """ Setup """
    print('\nPlease type name of the MySQL database.')
    print('Type a name to change, or press ENTER to skip.')
    data = ''
    if db_xml.xpath('server_section/db_config/database/text()'):
        data = db_xml.xpath('server_section/db_config/database')[0].text
    selected = raw_input('[Currently `{}`] : '.format(data))
    if selected:
        node = db_xml.xpath('server_section/db_config/database')[0]
        node.text = selected


def setup_user():
    """ Setup """
    print('\nPlease type the MySQL username.')
    print('Type a name to change, or press ENTER to skip.')
    data = ''
    if db_xml.xpath('server_section/db_config/user/text()'):
        data = db_xml.xpath('server_section/db_config/user')[0].text
    selected = raw_input('[Currently `{}`] : '.format(data))
    if selected:
        node = db_xml.xpath('server_section/db_config/user')[0]
        node.text = selected


def setup_password():
    """ Setup """
    print('\nPlease type the MySQL password.')
    print('Type something to change, or press ENTER to skip.')
    if db_xml.xpath('server_section/db_config/password/text()'):
        data = db_xml.xpath('server_section/db_config/password')[0].text
        selected = raw_input('[Currently `{}`] : '.format('*' * len(data)))
    else:
        selected = raw_input('[Currently EMPTY] : ')
    if selected:
        node = db_xml.xpath('server_section/db_config/password')[0]
        node.text = encrypt(selected, shared_kk)


if __name__ == '__main__':

    os.environ['TWISTER_PATH'] = TWISTER_PATH

    if TWISTER_PATH not in sys.path:
        sys.path.append(TWISTER_PATH)

    from common.configobj import ConfigObj

    users_groups = ConfigObj('{}/config/users_and_groups.ini'.format(TWISTER_PATH),
        create_empty=True, write_empty_values=True)
    shared_db = users_groups.get('shared_db_cfg')
    shared_kk = users_groups.get('shared_db_key', 'Luxoft')

    db_xml = etree.parse(shared_db)

    setup_server()
    setup_database()
    setup_user()
    setup_password()

    xml = etree.tostring(db_xml, pretty_print=True)
    open(shared_db, 'w').write(xml)

    print('\nEverything saved in file `{}`!\n'.format(shared_db))


# Eof()
