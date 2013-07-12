#!/usr/bin/env python

# version: 2.001

# File: installer.py ; This file is part of Twister.

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

'''
Twister Installer
=================

Requires Python 2.7 and a Linux machine. The installer doesn't run on Windows!

When installing Twister for the first time, you must run install_dependencies first.

Twister Client will be installed in the home of your user, in the folder `twister`.
'''

import os, sys
import shutil
import subprocess
from string import Template

from distutils import file_util
from distutils import dir_util

__dir__ = os.path.split(__file__)[0]
if __dir__: os.chdir(__dir__)

# Python executable. Alternatively, it can be "python2.7".
PYTHON_EXE = sys.executable

# --------------------------------------------------------------------------------------------------
# Install  Server  or  Client ?
# --------------------------------------------------------------------------------------------------

def userHome(user):
    return subprocess.check_output('echo ~' + user, shell=True).strip()

try:
    user_name = os.getenv('USER')
    if user_name=='root':
        user_name = os.getenv('SUDO_USER')
    if not user_name:
        print('Cannot guess the Username! Exiting!\n')
        exit(1)
except:
    print('Cannot guess the Username! Exiting!\n')
    exit(1)

# --------------------------------------------------------------------------------------------------
# Previous installations of Twister
# --------------------------------------------------------------------------------------------------

# Twister client path
INSTALL_PATH = userHome(user_name) + os.sep + 'twister/'

print('\nHello `{}` !\n'.format(user_name))

if os.path.exists(INSTALL_PATH):
    print('WARNING! Another version of Twister is installed at `%s`!' % INSTALL_PATH)
    print('If you continue, all files from that folder will be PERMANENTLY DELETED,')
    print('Only the `config` folder will be saved!')
    selected = raw_input('Are you sure you want to continue? (yes/no): ')

    if selected.strip().lower() in ['y', 'yes']:

        # Backup CONFIG folder for client
        if os.path.exists(INSTALL_PATH + 'config'):
            print('\nBack-up `config` folder (from `{0}` to `{1}`)...'.format(INSTALL_PATH+'config', os.getcwd()))
            shutil.move(INSTALL_PATH + 'config', os.getcwd())

        # Deleting previous versions of Twister
        try: dir_util.remove_tree(INSTALL_PATH)
        except: print('Error! Cannot delete Twister dir `{0}` !'.format(INSTALL_PATH))
        try: os.mkdir(INSTALL_PATH)
        except: print('Error! Cannot create Twister dir `{0}` !'.format(INSTALL_PATH))

    else:
        print('\nPlease backup your data, then restart the installer.')
        print('Exiting.\n')
        exit(0)

# --------------------------------------------------------------------------------------------------
# Start copying files
# --------------------------------------------------------------------------------------------------

# Files to move in Client folder
to_copy = [
    'bin/cli.py',
    'bin/start_client',
    'bin/start_client.py',
    'bin/start_packet_sniffer.py',
    'doc/',
    'demo/',
    'config/',
    'client/',
    'services/PacketSniffer/',
    'services/__init__.py',
    'common/__init__.py',
    'common/constants.py',
    'common/suitesmanager.py',
    'common/configobj.py',
    'common/jython/',
]

ROOT_FOLDER = os.sep.join( os.getcwd().split(os.sep)[:-1] )
cwd_path = os.getcwd() + os.sep
pkg_path = cwd_path + 'packages/'

print('')

for fname in to_copy:
    fpath = ROOT_FOLDER + os.sep + fname
    dpath = os.path.dirname(fname)

    if dpath and ( not os.path.exists(INSTALL_PATH+dpath) ):
        try:
            dir_util.mkpath(INSTALL_PATH + dpath)
            print('Created folder structure `%s`.' % (INSTALL_PATH+dpath))
        except:
            print('Cannot create folder `%s`!' % (INSTALL_PATH+dpath))

    if os.path.isdir(fpath):
        try:
            dir_util.copy_tree(fpath, INSTALL_PATH + dpath)
            print('Copied dir `%s` to `%s`.' % (fpath, INSTALL_PATH+dpath))
        except:
            print('Cannot copy dir `%s` to `%s`!' % (fpath, INSTALL_PATH+dpath))

    elif os.path.isfile(fpath):
        try:
            file_util.copy_file(fpath, INSTALL_PATH + dpath)
            print('Copied file `%s` to `%s`.' % (fpath, INSTALL_PATH+dpath))
        except:
            print('Cannot copy file `%s` to `%s`!' % (fpath, INSTALL_PATH+dpath))

    else:
        print('Path `{}` does not exist and will not be copied!'.format(fpath))


# Restore Config folder, if any
if os.path.exists(cwd_path + 'config'):
    print('\nMoving `config` folder back (from `{}` to `{}`)...'.format(cwd_path+'config', INSTALL_PATH+'config'))
    dir_util.copy_tree(cwd_path + 'config', INSTALL_PATH+'config')
    dir_util.remove_tree(cwd_path + 'config')


# Create cache and logs folders
try: os.mkdir(INSTALL_PATH +os.sep+ '.twister_cache')
except: pass
try: os.mkdir(INSTALL_PATH +os.sep+ 'logs')
except: pass
# Delete Server config files...
try: os.remove(INSTALL_PATH +os.sep+ 'config/resources.json')
except: pass
try: os.remove(INSTALL_PATH +os.sep+ 'config/services.ini')
except: pass


# Change owner for install folder...
if os.getuid() == 0:
    tcr_proc = subprocess.Popen(['chown', user_name+':'+user_name, INSTALL_PATH, '-R'],)
    tcr_proc.wait()

tcr_proc = subprocess.Popen(['chmod', '775', INSTALL_PATH, '-R'],)
tcr_proc.wait()


try:
    tcr_proc = subprocess.Popen(['chmod', '777', INSTALL_PATH +os.sep+ 'logs', '-R'],)
    tcr_proc.wait()
except:
    print('Cannot CHMOD 777 the logs folder!')


for ext in ['txt', 'xml', 'py', 'tcl', 'plx', 'json', 'ini', 'htm', 'js', 'css']:
    os.system('find %s -name "*.%s" -exec chmod 664 {} \;' % (INSTALL_PATH, ext))


# Make executables
os.system('find %s -name "cli.py" -exec chmod +x {} \;' % INSTALL_PATH)
os.system('find %s -name "start_client" -exec chmod +x {} \;' % INSTALL_PATH)
os.system('find %s -name "start_client.py" -exec chmod +x {} \;' % INSTALL_PATH)
os.system('find %s -name "start_packet_sniffer.py" -exec chmod +x {} \;' % INSTALL_PATH)


# Fix FWM Config XML
fwm = Template( open(INSTALL_PATH + 'config/fwmconfig.xml', 'r').read() )
open(INSTALL_PATH + 'config/fwmconfig.xml', 'w').write( fwm.substitute(HOME=userHome(user_name)) )
del fwm


print('\nTwister installation done!\n')
