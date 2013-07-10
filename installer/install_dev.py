#!/usr/bin/python

# version: 2.002

# File: install_dev.py ; This file is part of Twister.

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

Requires Python 2.7 and must run as ROOT.
If you are installing the Twister Server, it is strongly recommended
to have an internet connection, to allow the installer to setup all the dependencies.
'''

import os, sys
import glob
import shutil
import urllib2
import tarfile
import subprocess
import platform
from string import Template

from distutils import file_util
from distutils import dir_util

if sys.version_info[0] != 2 and sys.version_info[1] != 7:
    print('\nPython version must be 2.7! Exiting!\n')
    exit(1)

if os.getuid() != 0:
    print('\nTwister installer must run wish SUDO! Exiting!\n')
    exit(1)

#

__dir__ = os.path.split(__file__)[0]
if __dir__: os.chdir(__dir__)

# Install option.
TO_INSTALL = ''

# --------------------------------------------------------------------------------------------------
# Install  Server  or  Client ?
# --------------------------------------------------------------------------------------------------

def userHome(user):
    return subprocess.check_output('echo ~' + user, shell=True).strip()

# If installer was run with parameter "--server"
if sys.argv[1:2] == ['--server']:
    TO_INSTALL = 'server'

# If installer was run with parameter "--client"
elif sys.argv[1:2] == ['--client']:
    TO_INSTALL = 'client'

else:
    while 1:
        print('\nPlease select what you wish to install:')
        print('[1] the Twister clients')
        print('[2] the Twister servers')
        print('[q] e[x]it, don\'t install anything')

        selected = raw_input('Your choice: ')
        if selected == '1':
            print('Will install clients.\n')
            TO_INSTALL = 'client'
            break
        elif selected == '2':
            print('Will install servers.\n')
            TO_INSTALL = 'server'
            break
        elif selected in ['0', 'q', 'x']:
            print('Ok, exiting!\n')
            exit(0)
        else:
            print('`%s` is not a valid choice! try again!' % selected)
        del selected

if TO_INSTALL == 'client':
    try:
        user_name = os.getenv('USER')
        if user_name=='root':
            user_name = os.getenv('SUDO_USER')
        if (not user_name):
            print('Cannot guess the User Name! Please start this process using SUDO! Exiting!\n')
            exit(1)
    except:
        print('Cannot guess the User Name! Please start this process using SUDO! Exiting!\n')
        exit(1)

# --------------------------------------------------------------------------------------------------
# Previous installations of Twister
# --------------------------------------------------------------------------------------------------

if TO_INSTALL == 'server':

    print('Please type where you wish to install the servers.')
    print('Don\'t forget to add `twister` at the end of the path!')
    print('Leave EMPTY to install in default path `/opt/twister`:')
    selected = raw_input('Path : ')
    selected = selected.rstrip('/')

    if selected and not os.path.isdir( os.path.split(selected)[0] ):
        print('The path to `{0}` does not exist! Exiting!\n'.format(os.path.split(selected)[0]))
        exit(1)

    # Twister server path
    if selected:
        # Use the path from user, add '/' at the end
        INSTALL_PATH = selected + os.sep
    else:
        INSTALL_PATH = '/opt/twister/'
    del selected

    if os.path.exists(INSTALL_PATH):
        print('\nWARNING! Another version of Twister is installed at `%s`!' % INSTALL_PATH)
        print('If you continue, all files from that folder will be PERMANENTLY DELETED!!')
        print('If you created custom libs (in lib/ folder) and plugins (in plugin/ folder),')
        print('you should make a back-up, then restart the installer.')
        selected = raw_input('Are you sure you want to continue? (yes/no): ')

        if selected.strip().lower() not in ['y', 'yes']:
            print('\nPlease backup your data, then restart the installer.')
            print('Exiting.\n')
            exit(0)

    # Backup CONFIG folder for server
    try: os.remove(os.getcwd() + '/config')
    except: pass
    if os.path.exists(INSTALL_PATH + 'config'):
        print('\nBack-up `config` folder (from `{0}` to `{1}`)...'.format(INSTALL_PATH+'config', os.getcwd()))
        shutil.move(INSTALL_PATH + 'config', os.getcwd())

    # Deleting previous versions of Twister
    try:
        dir_util.remove_tree(INSTALL_PATH)
        print('Removed folder `%s`.' % INSTALL_PATH)
    except: print('Warning! Cannot delete Twister dir `{0}` !'.format(INSTALL_PATH))
    try:
        os.makedirs(INSTALL_PATH)
        print('Created folder `%s`.' % INSTALL_PATH)
    except: print('Warning! Cannot create Twister dir `{0}` !'.format(INSTALL_PATH))

else:

    # Twister client path
    INSTALL_PATH = userHome(user_name) + os.sep + 'twister/'

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
# Dependencies lists and configs
# --------------------------------------------------------------------------------------------------

if TO_INSTALL == 'server':

    # Files to move in Server folder
    to_link = [
        'bin/cli.py',
        'bin/start_server',
        'doc/',
        'server/',
        'common/',
        'lib/',
        'config/resources.json',
        'config/services.ini',
        'plugins/',
        'services/',
    ]

    to_copy = [
        'bin/start_server',
        'config/resources.json',
        'config/services.ini',
        'config/',
        'log/',
    ]

elif TO_INSTALL == 'client':

    # Files to move in Client folder
    to_link = [
        'bin/cli.py',
        'bin/start_client',
        'bin/start_client.py',
        'bin/start_packet_sniffer.py',
        'doc/',
        'demo/',
        'config/',
        'client/',
        'services/',
        'common/',
    ]

    to_copy = [
        'config/',
        'log/',
    ]

else:
    print('This is really wrong! Exiting!')
    exit(1)

#
ROOT_FOLDER = os.sep.join( os.getcwd().split(os.sep)[:-1] )
cwd_path = os.getcwd() + os.sep
#

# --------------------------------------------------------------------------------------------------
# Start copying files
# --------------------------------------------------------------------------------------------------

print('')

for fname in to_link:
    fpath = ROOT_FOLDER + os.sep + fname
    dpath = os.path.dirname(fname)

    # This is a normal folder
    if fname in to_copy:
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
            print('Path `%s` does not exist and will not be copied!' % fpath)

    # This is a symbolic link
    else:
        sym_name = '/' + os.path.split(fname)[1]
        sym_name = sym_name.rstrip('/')

        if sym_name.strip('/') and dpath and ( not os.path.exists(INSTALL_PATH+dpath) ):
            try:
                dir_util.mkpath(INSTALL_PATH + dpath)
                print('Created folder structure `%s`.' % (INSTALL_PATH+dpath))
            except:
                print('Cannot create folder `%s`!' % (INSTALL_PATH+dpath))

        if os.path.isdir(fpath):
            try:
                os.symlink(fpath, INSTALL_PATH + dpath + sym_name)
                print('Created SYM from dir `%s` to `%s`.' % (fpath, INSTALL_PATH+dpath+sym_name))
            except:
                print('Cannot create SYM from dir `%s` to `%s`!' % (fpath, INSTALL_PATH+dpath+sym_name))

        elif os.path.isfile(fpath):
            try:
                os.symlink(fpath, INSTALL_PATH + dpath + sym_name)
                print('Created SYM from file `%s` to `%s`.' % (fpath, INSTALL_PATH+dpath+sym_name))
            except:
                print('Cannot create SYM from file `%s` to `%s`!' % (fpath, INSTALL_PATH+dpath+sym_name))

        else:
            print('Path `%s` does not exist and will not be copied!' % fpath)

#

# Restore Config folder, if any
if os.path.exists(cwd_path + 'config'):
    print('\nMoving `config` folder back (from `{0}` to `{1}`)...'.format(cwd_path+'config', INSTALL_PATH+'config'))
    dir_util.copy_tree(cwd_path + 'config', INSTALL_PATH+'config')
    dir_util.remove_tree(cwd_path + 'config')

#

if TO_INSTALL == 'client':

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
    tcr_proc = subprocess.Popen(['chown', user_name+':'+user_name, INSTALL_PATH, '-R'],)
    tcr_proc.wait()

tcr_proc = subprocess.Popen(['chmod', '775', INSTALL_PATH, '-R'],)
tcr_proc.wait()

if TO_INSTALL == 'client':
    tcr_proc = subprocess.Popen(['chmod', '777', INSTALL_PATH +os.sep+ 'logs', '-R'],)
    tcr_proc.wait()


for ext in ['txt', 'xml', 'py', 'tcl', 'plx', 'json', 'ini', 'htm', 'js', 'css']:
    os.system('find %s -name "*.%s" -exec chmod 664 {} \;' % (INSTALL_PATH, ext))

# Make executables
if TO_INSTALL == 'client':
    os.system('find %s -name "cli.py" -exec chmod +x {} \;' % INSTALL_PATH)
    os.system('find %s -name "start_ep.py" -exec chmod +x {} \;' % INSTALL_PATH)
    os.system('find %s -name "start_packet_sniffer.py" -exec chmod +x {} \;' % INSTALL_PATH)

# Add twister path export
for fname in glob.glob(INSTALL_PATH + 'bin/*'):
    # Ignore all files with extension
    if os.path.splitext(fname)[1]: continue

    lines = open(fname).readlines()
    lines.insert(4, ('export TWISTER_PATH=%s\n\n' % INSTALL_PATH.rstrip('/')))
    open(fname, 'w').write(''.join(lines))

# Fix FWM Config XML
if TO_INSTALL == 'client':
    fwm = Template( open(INSTALL_PATH + 'config/fwmconfig.xml', 'r').read() )
    open(INSTALL_PATH + 'config/fwmconfig.xml', 'w').write( fwm.substitute(HOME=userHome(user_name)) )
    del fwm

#

print('\nTwister installation done!\n')
