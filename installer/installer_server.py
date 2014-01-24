
# version: 2.004

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

By default, the server will be installed in `/opt/twister`.
'''

import os, sys
import glob
import shutil
import subprocess
from string import Template

from distutils import file_util
from distutils import dir_util

__dir__ = os.path.split(__file__)[0]
if __dir__: os.chdir(__dir__)

# Need the username for NIS machines, where the ROOT cannot access the user documents !
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

print('Welcome to the Twister Installer !\n')

print('Please type where you wish to install the servers.')
print('Don\'t forget to add `twister` at the end of the path!')
print('Leave EMPTY to install in default path `/opt/twister`:')
selected = raw_input('Path : ')
selected = selected.rstrip('/')

if selected and not os.path.isdir( os.path.split(selected)[0] ):
    print('The path to `{}` does not exist! Exiting!\n'.format(os.path.split(selected)[0]))
    exit(1)

# Twister server path
if selected:
    # Use the path from user, add '/' at the end
    INSTALL_PATH = selected + os.sep
else:
    INSTALL_PATH = '/opt/twister/'
del selected

if os.path.exists(INSTALL_PATH):
    print('\nWARNING! Another version of Twister is installed at `{}`!'.format(INSTALL_PATH))
    print('If you continue, all files from that folder will be PERMANENTLY DELETED!!')
    print('If you created custom libs (in lib/ folder) and plugins (in plugin/ folder),')
    print('you should make a back-up, then restart the installer.')
    selected = raw_input('Are you sure you want to continue? (yes/no): ')

    if selected.strip().lower() not in ['y', 'yes']:
        print('\nPlease backup your data, then restart the installer.')
        print('Exiting.\n')
        exit(0)

# Backup CONFIG folder for server
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
try:
    dir_util.remove_tree(INSTALL_PATH)
    print('Removed folder `%s`.' % INSTALL_PATH)
    err1 = False
except:
    print('Warning! Cannot delete Twister dir `{0}` !'.format(INSTALL_PATH))
    err1 = True
try:
    os.makedirs(INSTALL_PATH)
    print('Created folder `%s`.' % INSTALL_PATH)
    err2 = False
except:
    print('Warning! Cannot create Twister dir `{0}` !'.format(INSTALL_PATH))
    err2 = True

if err1 and err2:
    print('\nFatal Error! You cannot install Twister in that location!')
    print('You probably don\'t have enough privileges to read and write in `{}` !\n'.format(INSTALL_PATH))
    exit(1)

# --------------------------------------------------------------------------------------------------
# Start copying files
# --------------------------------------------------------------------------------------------------

# Files to move in Server folder
to_copy = [
    'bin/cli.py',
    'bin/start_server',
    'doc/',
    'server/',
    'common/',
    'lib/',
    'config/sut',
    'config/resources.json',
    'config/services.ini',
    'config/users_and_groups.ini',
    'config/server_init.ini',
    'plugins/',
    'services/',
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
    print('\nMoving `config` folder back (from `{}` to `{}`)...'.format(tmp_config, INSTALL_PATH+'config'))
    dir_util.copy_tree(tmp_config, INSTALL_PATH+'config')
    dir_util.remove_tree(tmp_config)


tcr_proc = subprocess.Popen(['chmod', '775', INSTALL_PATH, '-R'],)
tcr_proc.wait()


for ext in ['txt', 'xml', 'py', 'tcl', 'plx', 'json', 'ini', 'htm', 'js', 'css']:
    os.system('find %s -name "*.%s" -exec chmod 664 {} \;' % (INSTALL_PATH, ext))


# Add twister path export
for fname in glob.glob(INSTALL_PATH + 'bin/*'):
    # Ignore all files with extension
    if os.path.splitext(fname)[1]: continue

    lines = open(fname).readlines()
    lines.insert(4, ('export TWISTER_PATH=%s\n\n' % INSTALL_PATH.rstrip('/')))
    open(fname, 'w').write(''.join(lines))


print('\nTwister installation done!\n')
