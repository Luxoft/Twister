#!/usr/bin/env python2.7

# version: 3.003

# File: installer.py ; This file is part of Twister.

# Copyright (C) 2012-2013 , Luxoft

# Authors:
#    Andrei Costachi <acostachi@luxoft.com>
#    Cristi Constantin <crconstantin@luxoft.com>
#    Daniel Cioata <dcioata@luxoft.com>
#    Mihail Tudoran <mtudoran@luxoft.com>
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

import os, sys
import platform

if platform.system().lower() != 'linux':
    print('Error! This installer works only in Linux!')
    exit(1)

# Install option.
TO_INSTALL = ''

while 1:
    print('\nPlease select what you wish to install:')
    print('[1] the Twister dependencies (must be ROOT)')
    print('[2] the Twister clients')
    print('[3] the Twister servers')
    print('[q] e[x]it, don\'t install anything')

    selected = raw_input('Your choice: ')
    if selected == '1':
        print('Will install dependencies.\n')
        TO_INSTALL = 'dependencies'
        break
    elif selected == '2':
        print('Will install clients.\n')
        TO_INSTALL = 'client'
        break
    elif selected == '3':
        print('Will install servers.\n')
        TO_INSTALL = 'server'
        break
    elif selected in ['0', 'q', 'x']:
        print('Ok, exiting!\n')
        exit(0)
    else:
        print('`%s` is not a valid choice! try again!' % selected)
    del selected


def test_dependencies():
    """
    Test that all Twister dependencies are ok.
    """

    # The dependencies:
    dependencies = [
        'Mako',
        'CherryPy',
        'LXML-Python',
        'MySQL-python',
        'ecdsa',
        'paramiko',
        'PyCrypto',
        'plumbum',
        'rpyc',
        'pExpect'
    ]
    # Import names used for testing
    library_names = [
        'mako',
        'cherrypy',
        'lxml',
        'MySQLdb',
        'ecdsa',
        'paramiko',
        'Crypto',
        'plumbum',
        'rpyc',
        'pexpect'
    ]
    # Versions
    library_versions = [
        '0.9', # Mako
        '3.2', # CherryPy
        '3.3', # Lxml
        '1.2', # MySql
        '0.1', # Ecdsa
        '1.1', # Paramiko
        '2.6', # PyCrypto
        '1.4', # Plumbum
        '3.3', # Rpyc
        '3.3'  # pExpect
    ]

    try:
        import setuptools
        import pkg_resources
    except:
        print('*ERROR* Python setuptools is not installed!\n')
        return False

    for i in range(len(dependencies)):

        lib_name = dependencies[i]
        import_name = library_names[i]
        lib_version = library_versions[i]

        try:
            # Scapy is really special ... the package name is Scapy-real
            if import_name == 'scapy': import_name = 'scapy-real'
            # The version is ok (try 1) ?
            ver1 = pkg_resources.get_distribution(import_name).version
            if import_name == 'scapy-real': import_name = 'scapy'
        except:
            ver1 = None

        try:
            lib = __import__(import_name)
            # The version is ok (try 2) ?
            ver2 = eval('lib.__version__')
            del lib
        except:
            ver2 = None

        if ver1:
            ver = ver1
        else:
            ver = ver2

        try:
            # Can be imported ?
            lib = __import__(import_name)
        except:
            ver = None

        if not ver:
            print('Python library `{}` is not installed !! Cannot continue installation.\n'.format(lib_name))
            return False
        elif ver < lib_version:
            print('Testing dependency: Library `{}` has version `{}` '
                  'and it must be `{}`, or newer !!'.format(import_name, ver, lib_version))
            print('\nUninstall `{}` and run the dependencies installer again !!\n'.format(lib_name))
            return False
        else:
            print('Testing dependency: Library `{}` version `{}` is OK.'.format(lib_name, ver))

    import socket
    try:
        socket.create_connection(('127.0.0.1', '22'), 5)
    except Exception:
        print('\nTesting dependency: Cannot connect to local OpenSSH Server!\n')
        print('Please install `openssh-server` system package!\n')
        return False

    print('')
    return True


# Import options

if TO_INSTALL == 'client':
    if test_dependencies():
        import installer_client

elif TO_INSTALL == 'server':
    if test_dependencies():
        import installer_server

elif TO_INSTALL == 'dependencies':
    import install_dependencies

else:
    print('\nExiting!\n')
