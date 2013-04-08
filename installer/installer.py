#!/usr/bin/python

# version: 2.002

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

TO_INSTALL = ''

# Python executable. Alternatively, it can be "python2.7".
PYTHON_EXE = sys.executable

# The proxy is used only if you need a proxy to connect to internet,
# And `setuptools` is not installed, or some dependencies are missing
if os.getenv('HTTP_PROXY'):
    HTTP_PROXY = os.getenv('HTTP_PROXY')
else:
    HTTP_PROXY = 'http://UserName:PassWord@http-proxy:3128'

__dir__ = os.path.split(__file__)[0]
if __dir__: os.chdir(__dir__)

# --------------------------------------------------------------------------------------------------
# Install  Server  or  Client ?
# --------------------------------------------------------------------------------------------------

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
    INSTALL_PATH = os.getenv('HOME') + os.sep + 'twister/'

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
    # The dependencies must be installed in this exact order:
    dependencies = [
        'Beaker',
        'Mako',
        'CherryPy',
        'LXML-Python',
        'MySQL-python',
    ]

    # Import names used for testing
    library_names = [
        'beaker',
        'mako',
        'cherrypy',
        'lxml',
        'MySQLdb',
    ]

    # Versions
    library_versions = [
        '1.6',
        '0.7',
        '3.2',
        '2.0',
        '1.2',
    ]

    # Files to move in Server folder
    to_copy = [
        'bin/start_ce',
        'bin/start_httpserver',
        'doc/',
        'server/',
        'common/',
        'lib/',
        'config/resources.json',
        'config/services.ini',
        'plugins/',
        'services/',
    ]

elif TO_INSTALL == 'client':
    # The client doesn't have important dependencies
    dependencies = ['Scapy-real', 'pExpect']
    library_names = ['scapy', 'pexpect']
    library_versions = ['2.1', '2.2']

    # Files to move in Client folder
    to_copy = [
        'bin/start_ep.py',
        'bin/start_packets_twist.py',
        'doc/',
        'demo/',
        'config/',
        'client/',
        'services/PacketsTwist/',
        'common/__init__.py',
        'common/constants.py',
        'common/configobj.py',
    ]

else:
    print('This is really wrong! Exiting!')
    exit(1)

#
ROOT_FOLDER = os.sep.join( os.getcwd().split(os.sep)[:-1] )
cwd_path = os.getcwd() + os.sep
pkg_path = cwd_path + 'packages/'
#

# Using HTTP_PROXY environment variable?
if HTTP_PROXY:
    os.putenv('HTTP_PROXY', HTTP_PROXY)
    proxy_support = urllib2.ProxyHandler({'http': HTTP_PROXY})
    opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)

# Checking internet connection and Pypi availability
print('\nChecking internet connection...')
try:
    pypi = urllib2.urlopen('http://pypi.python.org/simple/')
    if pypi.read(255):
        INTERNET = True
        print('Internet connection available.\n')
    else:
        INTERNET = False
        print('Cannot connect! Check the internet connection, or the Proxy settings!\n')
    del pypi
except:
    INTERNET = False
    print('Cannot connect! Check the internet connection, or the Proxy settings!\n')


if not INTERNET:
    selected = raw_input('Internet connection NOT available. The required packages will not be installed.\n'
        'Are you sure you want to continue? (yes/no): ')
    if selected.strip().lower() not in ['y', 'yes']:
        print('\nExiting.\n')
        exit(0)


# --------------------------------------------------------------------------------------------------
# Starting the install process
# --------------------------------------------------------------------------------------------------

try:
    import setuptools
    import pkg_resources
    print('Python setuptools is installed. Ok.')
except:
    if INTERNET:
        # Try to install python distribute (the new version of setuptools)
        tcr_proc = subprocess.Popen([PYTHON_EXE, '-u', (pkg_path+'distribute_setup.py')], cwd=cwd_path)
        tcr_proc.wait()
        del tcr_proc

        # Remove the downloaded file
        distribute_file = glob.glob('distribute*.tar.gz')
        if distribute_file:
            try: os.remove(distribute_file[0])
            except: print('Installer cannot delete `distribute*.tar.gz`! You must delete it yourself!')
        del distribute_file

print('')

# --------------------------------------------------------------------------------------------------
# Testing installed packages
# If a package does not exists, or is an old version, it must be installed
# --------------------------------------------------------------------------------------------------

library_err = [] # Used to keep the libraries that could not be installed

for i in range(len(dependencies)):

    lib_name = dependencies[i]
    lib_version = library_versions[i]
    import_name = library_names[i]

    try:
        # The version is ok (try 1) ?
        ver1 = pkg_resources.get_distribution(import_name).version
    except:
        ver1 = None

    try:
        # Can be imported ?
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

    if not ver:
        print('Python library `%s` is not installed...' % import_name)

    if ver < lib_version:
        print('Testing dependency: Library `%s` has version `%s` and it must be `%s` or newer! Will install...' %
            (import_name, ver, lib_version))
    else:
        print('Testing dependency: Imported `%s` version `%s` is OK. No need to re-install.' % (import_name, ver))
        continue

    # ----------------------------------------------------------------------------------------------
    # Internet connection available
    # ----------------------------------------------------------------------------------------------

    if INTERNET:

        # MySQL Python requires Python-DEV and must be installed from repositories
        if lib_name == 'MySQL-python':
            print('\n~~~ Installing `%s` from System repositories ~~~\n' % lib_name)

            if platform.dist()[0] == 'SuSE':
                tcr_proc = subprocess.Popen(['zypper', 'install', '-yl', 'python-mysql'], cwd=pkg_path)
            elif platform.dist()[0] == 'fedora':
                tcr_proc = subprocess.Popen(['yum', '-y', 'install', 'python-mysql'], cwd=pkg_path)
            else:
                tcr_proc = subprocess.Popen(['apt-get', 'install', 'python-mysqldb', '-y', '--force-yes'], cwd=pkg_path)

            try: tcr_proc.wait()
            except: print('Error while installing `MySQL-python`!')

        elif lib_name == 'LXML-Python':
            print('\n~~~ Installing `%s` from System repositories ~~~\n' % lib_name)

            tcr_proc = subprocess.Popen(['apt-get', 'install', 'python-lxml', '-y', '--force-yes'], cwd=pkg_path)

            try: tcr_proc.wait()
            except: print('Error while installing `Python LXML`!')

        # All other packages are installed with easy_install
        else:
            print('\n~~~ Installing `%s` from Python repositories ~~~\n' % lib_name)
            tcr_proc = subprocess.Popen(['easy_install', lib_name], cwd=pkg_path)
            tcr_proc.wait()

        if tcr_proc.returncode:
            print('\n~~~ `%s` cannot be installed! It MUST be installed manually! ~~~\n' % lib_name)
            library_err.append(lib_name)
        else:
            print('\n~~~ Successfully installed %s ~~~\n' % lib_name)

    # ----------------------------------------------------------------------------------------------
    # No internet connection
    # ----------------------------------------------------------------------------------------------

    else:
        print('\n~~~ Installing `%s` from tar files ~~~' % lib_name)

        p_library = glob.glob(pkg_path + lib_name + '*.tar.gz')

        if not p_library:
            print('\n~~~ Cannot find `%s`! You MUST install it manually! ~~~\n' % (lib_name+'*.tar.gz'))
            library_err.append(lib_name)
            continue

        fopen = tarfile.open(p_library[0])
        p_library_root = fopen.getnames()[0].split(os.sep)[0]
        fopen.extractall()
        fopen.close() ; del fopen

        # Install library
        tcr_proc = subprocess.Popen([PYTHON_EXE, '-u', (cwd_path+p_library_root+'/setup.py'), 'install', '-f'],
            cwd=cwd_path + p_library_root)
        tcr_proc.wait()

        # Remove library folder
        dir_util.remove_tree(cwd_path + p_library_root)

        if tcr_proc.returncode:
            print('\n~~~ `%s` cannot be installed! It MUST be installed manually! ~~~\n' % import_name)
        else:
            print('\n~~~ Successfully installed `%s` ~~~\n' % lib_name)

if library_err:
    print('The following libraries could not be installed: `%s`.\n'
          'Twister Framework will not run without them!' % ', '.join(library_err))


# --------------------------------------------------------------------------------------------------
# Start copying files
# --------------------------------------------------------------------------------------------------

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

for ext in ['txt', 'xml', 'py', 'tcl', 'plx', 'json', 'ini', 'htm', 'js', 'css']:
    os.system('find %s -name "*.%s" -exec chmod 664 {} \;' % (INSTALL_PATH, ext))

# Make executables
if TO_INSTALL == 'client':
    os.system('find %s -name "start_ep.py" -exec chmod +x {} \;' % INSTALL_PATH)
    os.system('find %s -name "start_packets_twist.py" -exec chmod +x {} \;' % INSTALL_PATH)

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
    open(INSTALL_PATH + 'config/fwmconfig.xml', 'w').write( fwm.substitute(HOME=os.getenv('HOME').rstrip('/')) )
    del fwm

#

print('\nTwister installation done!\n')
