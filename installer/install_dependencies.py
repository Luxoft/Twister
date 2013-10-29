#!/usr/bin/python

# version: 2.003

# File: install.py ; This file is part of Twister.

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
When installing the server, must run as ROOT! When installing the client, ROOT is optional.

When installing Twister for the first time, it is STRONGLY RECOMMENDED to have an internet connection
and run as ROOT, to allow the setup of all the dependencies.

Twister Client will be installed in the home of your user, in the folder `twister`.
The server will be installed by default in `/opt/twister`.
'''

import os, sys
import glob
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
    print('\nDependency installer must run with ROOT! Exiting!\n')
    exit(1)

# The proxy is used ONLY if you need a proxy to connect to internet,
# And `setuptools` is not installed, or some dependencies are missing
# HTTP_PROXY = 'http://UserName:PassWord@http-proxy:3128'
HTTP_PROXY = ''

__dir__ = os.path.split(__file__)[0]
if __dir__: os.chdir(__dir__)

# Python executable. Alternatively, it can be "python2.7".
PYTHON_EXE = sys.executable

# --------------------------------------------------------------------------------------------------
# Dependencies lists and configs
# --------------------------------------------------------------------------------------------------

# The dependencies must be installed in this exact order:
dependencies = [
    'Mako',
    'CherryPy',
    'LXML-Python',
    'MySQL-python',
    'Scapy-real',
    'Paramiko',
    'PyCrypto',
    'six',
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
    'scapy',
    'paramiko',
    'Crypto',
    'six',
    'plumbum',
    'rpyc',
    'pexpect'
]

# Versions
library_versions = [
    '0.9',
    '3.2',
    '2.0',
    '1.2',
    '2.1',
    '1.1',
    '2.6',
    '1.4',
    '1.3',
    '3.3',
    '2.2'
]


def install_w_internet(lib_name):

    global library_err

    # MySQL Python requires Python-DEV and must be installed from repositories
    if lib_name == 'MySQL-python':
        print('\n~~~ Installing `{}` from System repositories ~~~\n'.format(lib_name))

        if platform.dist()[0] == 'SuSE':
            tcr_proc = subprocess.Popen(['zypper', 'install', '-yl', 'mysql-devel'])
        elif platform.dist()[0] in ['fedora', 'centos']:
            tcr_proc = subprocess.Popen(['yum', '-y', 'install', 'mysql-devel'])
        else:
            tcr_proc = subprocess.Popen(['apt-get', 'install', 'python-mysqldb', '-y', '--force-yes'])

        try: tcr_proc.wait()
        except: print('Error while installing `Python-MySQL`!')

        tcr_proc = subprocess.Popen(['easy_install', 'MySQL-python'], cwd=pkg_path)
        tcr_proc.wait()

    elif lib_name == 'LXML-Python':
        print('\n~~~ Installing `{}` from System repositories ~~~\n'.format(lib_name))

        if platform.dist()[0] in ['fedora', 'centos']:
            tcr_proc = subprocess.Popen(['yum', '-y', 'install', 'libxslt-devel', 'libxml2-devel'])
        else:
            tcr_proc = subprocess.Popen(['apt-get', 'install', 'python-lxml', '-y', '--force-yes'])

        try: tcr_proc.wait()
        except: print('Error while installing `Python LXML`!')

        tcr_proc = subprocess.Popen(['easy_install', 'lxml'], cwd=pkg_path)
        tcr_proc.wait()

    # All other packages are installed with easy_install
    else:
        print('\n~~~ Installing `%s` from Python repositories ~~~\n' % lib_name)
        tcr_proc = subprocess.Popen(['easy_install', lib_name], cwd=pkg_path)
        tcr_proc.wait()

    if tcr_proc.returncode:
        print('\n~~~ `%s` cannot be installed! It MUST be installed manually! ~~~\n' % lib_name)
        library_err.append(lib_name)
    else:
        print('\n~~~ Successfully installed `{}` ~~~\n'.format(lib_name))


def install_offline(lib_name):

    global library_err

    # MySQL Python requires Python-DEV and must be installed from repositories
    if INTERNET and lib_name == 'MySQL-python':
        print('\n~~~ Installing `{}` from System repositories ~~~\n'.format(lib_name))

        if platform.dist()[0] == 'SuSE':
            tcr_proc = subprocess.Popen(['zypper', 'install', '-yl', 'mysql-devel'])
        elif platform.dist()[0] in ['fedora', 'centos']:
            tcr_proc = subprocess.Popen(['yum', '-y', 'install', 'mysql-devel'])
        else:
            tcr_proc = subprocess.Popen(['apt-get', 'install', 'python-mysqldb', '-y', '--force-yes'])

        try:
            tcr_proc.wait()
            print('\n~~~ Successfully installed `{}` ~~~\n'.format(lib_name))
            return True
        except:
            print('Error while installing `Python-MySQL`!')

    elif INTERNET and lib_name == 'LXML-Python':
        print('\n~~~ Installing `{}` from System repositories ~~~\n'.format(lib_name))

        if platform.dist()[0] in ['fedora', 'centos']:
            tcr_proc = subprocess.Popen(['yum', '-y', 'install', 'libxslt-devel', 'libxml2-devel'])
        else:
            tcr_proc = subprocess.Popen(['apt-get', 'install', 'python-lxml', '-y', '--force-yes'])

        try:
            tcr_proc.wait()
            print('\n~~~ Successfully installed `{}` ~~~\n'.format(lib_name))
            return True
        except:
            print('Error while installing `Python LXML`!')


    print('\n~~~ Installing `{}` from tar files ~~~'.format(lib_name))

    if not p_library:
        print('\n~~~ Cannot find `%s`! You MUST install it manually! ~~~\n' % (lib_name+'*.tar.gz'))
        library_err.append(lib_name)
        return

    fopen = tarfile.open(p_library[0])
    print('Extracting `{}`...\nThis might take some time...\n'.format(p_library[0]))
    p_library_root = fopen.getnames()[0].split(os.sep)[0]
    fopen.extractall()
    fopen.close() ; del fopen

    # Install library
    tcr_proc = subprocess.Popen([PYTHON_EXE, '-u', (cwd_path+os.sep+p_library_root+'/setup.py'), 'install', '-f'],
        cwd=cwd_path + os.sep + p_library_root)
    tcr_proc.wait()

    # Remove library folder
    try:
        dir_util.remove_tree(cwd_path + os.sep + p_library_root)
    except:
        pass

    if tcr_proc.returncode:
        print('\n~~~ `%s` cannot be installed! It MUST be installed manually! ~~~\n' % import_name)
    else:
        print('\n~~~ Successfully installed `{}` ~~~\n'.format(lib_name))


#
cwd_path = os.path.split( os.path.abspath(__file__) )[0]
pkg_path = cwd_path + '/packages/'
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
    goo = urllib2.urlopen('http://www.google.com/')
    if goo.read(255):
        INTERNET = True
        print('Internet connection available.\n')
    else:
        INTERNET = False
        print('Cannot connect! Check the internet connection, or the Proxy settings!\n')
    del goo
except:
    INTERNET = False
    print('Cannot connect! Check the internet connection, or the Proxy settings!\n')

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
        print('Python library `%s` is not installed...' % import_name)

    if ver < lib_version:
        print('Testing dependency: Library `%s` has version `%s` and it must be `%s` or newer! Will install...' %
            (import_name, ver, lib_version))
    else:
        print('Testing dependency: Imported `%s` version `%s` is OK. No need to re-install.' % (import_name, ver))
        continue

    p_library = glob.glob(pkg_path + lib_name + '*gz')

    if INTERNET and not p_library:
        install_w_internet(lib_name)
    else:
        install_offline(lib_name)

if library_err:
    print('\nThe following libraries could not be installed: `%s`.\n'
          'Twister Framework will not run without them!' % ', '.join(library_err))

#

print('\nDependency installation done!\n')
