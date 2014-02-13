
# version: 2.003

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
import binascii
import shutil
import subprocess
from string import Template

from distutils import file_util
from distutils import dir_util

__dir__ = os.path.split(__file__)[0]
if __dir__: os.chdir(__dir__)

# --------------------------------------------------------------------------------------------------
# Install  Client ?
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
tmp_config   = ''

print('Hello `{}` !\n'.format(user_name))

if os.path.exists(INSTALL_PATH):
    print('WARNING! Another version of Twister is installed at `%s`!' % INSTALL_PATH)
    print('If you continue, all files from that folder will be PERMANENTLY DELETED,')
    print('Only the `config` folder will be saved!')
    selected = raw_input('Are you sure you want to continue? (yes/no): ')

    if selected.strip().lower() in ['y', 'yes']:

        # Backup CONFIG folder for client
        if os.path.exists(INSTALL_PATH + 'config'):
            if os.getuid() != 0: # Normal user
                tmp_config = userHome(user_name) + '/.twister'
                try: os.mkdir(tmp_config)
                except:
                    print('Error! Cannot create .twister dir `{}`! The installation cannot continue!\n'.format(tmp_config))
                    exit(1)
            else: # ROOT user
                tmp_config = '/tmp/twister_server_config'
            print('\nBack-up `config` folder (from `{}` to `{}`)...'.format(INSTALL_PATH+'config', tmp_config))
            try:
                shutil.move(INSTALL_PATH+'config', tmp_config)
            except Exception as e:
                print('\nInsuficient rights to move the config folder `{}`!\n'
                      'The installation cannot continue if you don\'t have permissions to move that folder!\n'.format(INSTALL_PATH+'config'))
                exit(1)
        else:
            tmp_config = ''

        # Deleting previous versions of Twister
        try: dir_util.remove_tree(INSTALL_PATH)
        except: print('Error! Cannot delete Twister dir `{}` !'.format(INSTALL_PATH))
        try: os.mkdir(INSTALL_PATH)
        except: print('Error! Cannot create Twister dir `{}` !'.format(INSTALL_PATH))

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


# Restore CONFIG folder, if any
if os.path.exists(tmp_config):
    print('\nMoving `config` folder back (from `{}` to `{}`)...'.format(tmp_config, INSTALL_PATH))
    dir_util.copy_tree(tmp_config, INSTALL_PATH)
    dir_util.remove_tree(tmp_config)


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
try: os.remove(INSTALL_PATH +os.sep+ 'config/server_init.ini')
except: pass
try: os.remove(INSTALL_PATH +os.sep+ 'config/users_and_groups.ini')
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


# Check user's encr key
user_key = '{}config/twister.key'.format(INSTALL_PATH)
if os.path.isfile(user_key) and open(user_key).read():
    print('User key ok.')
else:
    print('Generating user key...')
    with open(user_key, 'w') as f:
        f.write(binascii.hexlify(os.urandom(16)))
    print('User key saved in "config/twister.key". Don\'t change this file!')


print('\nTwister installation done!\n')
