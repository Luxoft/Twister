#!/usr/bin/env python2.7

# version: 3.006

# File: install.py ; This file is part of Twister.

# Copyright (C) 2012-2014, Luxoft

# Authors:
#    Andrei Costachi <acostachi@luxoft.com>
#    Cristi Constantin <crconstantin@luxoft.com>
#    Daniel Cioata <dcioata@luxoft.com>
#    Mihai Tudoran <mtudoran@luxoft.com>

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

if not PYTHON_EXE:
    try: PYTHON_EXE = subprocess.check_output('which python2.7', shell=True).strip()
    except Exception as e: print(e)

if not PYTHON_EXE:
    print('*ERROR* Cannot find the current python executable in {} !\nExiting!\n'.format(os.getenv('PATH')))
    exit(1)

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
    'scapy',
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
    '2.2', # Scapy
    '0.1', # Ecdsa
    '1.1', # Paramiko
    '2.6', # PyCrypto
    '1.4', # Plumbum
    '3.3', # Rpyc
    '3.3'  # pExpect
]

setuptools_version = '3.4'


def install_setuptools():

    tgz_setuptools = glob.glob(pkg_path + 'setuptools-*.tar.gz')

    if not tgz_setuptools:
        print('\n~~~ Cannot find `setuptools-*gz`! You MUST install it manually! ~~~\n')
        return False

    fopen = tarfile.open(tgz_setuptools[0])
    print('Extracting `{}`...\nThis might take some time...\n'.format(tgz_setuptools[0]))
    tgz_library_root = fopen.getnames()[0].split(os.sep)[0]
    fopen.extractall()
    fopen.close()

    # Install library
    tcr_proc = subprocess.Popen([PYTHON_EXE, '-u', (cwd_path+os.sep+tgz_library_root+'/setup.py'), 'install', '-f'],
        cwd=cwd_path + os.sep + tgz_library_root)
    tcr_proc.wait()

    # Remove library folder
    try:
        dir_util.remove_tree(cwd_path +os.sep+ tgz_library_root)
    except:
        pass

    if tcr_proc.returncode:
        print('\n~~~ `Setuptools` cannot be installed! It MUST be installed manually! ~~~\n')
        return False
    else:
        print('\n~~~ Successfully installed `Setuptools` ~~~\n')
        return True


def install_w_internet(lib_name):
    """
    Install online.
    """

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

        if platform.dist()[0] in ['fedora', 'centos', 'redhat']:
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
    """
    Install offline, using the tar.gz files.
    """

    global library_err

    # MySQL Python requires Python-DEV and must be installed from repositories
    if INTERNET and lib_name == 'MySQL-python':
        print('\n~~~ Installing `{}` from System repositories ~~~\n'.format(lib_name))

        if platform.dist()[0] == 'SuSE':
            tcr_proc = subprocess.Popen(['zypper', 'install', '-yl', 'mysql-devel'])
        elif platform.dist()[0] in ['fedora', 'centos', 'redhat']:
            tcr_proc = subprocess.Popen(['yum', '-y', 'install', 'mysql-devel'])
        else:
            tcr_proc = subprocess.Popen(['apt-get', 'install', 'python-mysqldb', '-y', '--force-yes'])

        try:
            tcr_proc.wait()
            print('\n~~~ Successfully installed `{}` ~~~\n'.format(lib_name))
            return True
        except:
            print('Error while installing `Python-MySQL`!')
            return False

    elif INTERNET and lib_name == 'LXML-Python':
        print('\n~~~ Installing `{}` from System repositories ~~~\n'.format(lib_name))

        # Requires libxml2 and libxslt
        if platform.dist()[0] in ['fedora', 'centos', 'redhat']:
            tcr_proc = subprocess.Popen(['yum', '-y', 'install', 'libxslt-devel', 'libxml2-devel'])
        else:
            tcr_proc = subprocess.Popen(['apt-get', 'install', 'libxslt-dev', 'python-lxml', '-y', '--force-yes'])

        try:
            tcr_proc.wait()
        except:
            print('Error while installing `Python LXML`!')
            return False

        # Continue with the TAR.GZ file, included in `packages` folder !

    print('\n~~~ Installing `{}` from tar files ~~~\n'.format(lib_name))

    if not tgz_library:
        print('\n~~~ Cannot find `%s`! You MUST install it manually! ~~~\n' % (lib_name+'*.tar.gz'))
        library_err.append(lib_name)
        return

    fopen = tarfile.open(tgz_library[0])
    print('Extracting `{}`...\nThis might take some time...\n'.format(tgz_library[0]))
    tgz_library_root = fopen.getnames()[0].split(os.sep)[0]
    fopen.extractall()
    fopen.close() ; del fopen

    # Install library
    tcr_proc = subprocess.Popen([PYTHON_EXE, '-u', (cwd_path+os.sep+tgz_library_root+'/setup.py'), 'install', '-f'],
        cwd=cwd_path + os.sep + tgz_library_root)
    tcr_proc.wait()

    # Remove library folder
    try:
        dir_util.remove_tree(cwd_path + os.sep + tgz_library_root)
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
    print('Python setuptools is installed. Ok.\n')
except:
    print('Python setuptools is not installed...\n')
    install_setuptools()

if setuptools.__version__ >= setuptools_version:
    print('Python setuptools version is Ok.\n')
else:
    print('Python setuptools version `{}` is too low...\n'.format(setuptools.__version__))
    install_setuptools()

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
        print('Python library `{}` is not installed...'.format(import_name))

    elif ver < lib_version:
        print('Testing dependency: Library `{}` has version `{}` '
              'and it must be `{}`, or newer !!'.format(import_name, ver, lib_version))
        print('\nLibrary `{}` is installed in `{}` and this script cannot remove it!\n'
              'You will have to manually uninstall this library !!'.format(import_name, lib.__file__))
        print('\nUninstall `{}` and run this script again !!'.format(import_name))
        library_err.append(import_name)
        continue

    else:
        print('Testing dependency: Imported `{}` version `{}` is OK. '
            'No need to re-install.'.format(import_name, ver))
        continue

    tgz_library = glob.glob(pkg_path + lib_name + '*gz')

    # If the missing library has a tar.gz file, install offline
    if tgz_library:
        install_offline(lib_name)
    # If internet connection is available, install online
    elif INTERNET:
        install_w_internet(lib_name)
    else:
        print('Library `{}` cannot be installed! tar.gz file cannot '
              'be found and internet is not available!'.format(lib_name))


if library_err:
    print('\n############################################################')
    print('\nThe following libraries could not be installed:\n`%s`\n'
          'Twister Framework will not run without them!' % ', '.join(library_err))
    print('\nDependency installation FAILED!')
    print('\n############################################################')
    exit()


print('\nDependency installation COMPLETED!\n')
