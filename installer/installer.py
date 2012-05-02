
'''
Twister Installer
Requires Python 2.7 and must run as ROOT.
If you are installing the Twister Server, it is strongly recommended
to have an internet connection, or else, you must manually install :
 - Python-DEV and
 - python-mysql.
'''

import os, sys
import glob
import shutil
import urllib2
import tarfile
import subprocess
import platform

from distutils import file_util
from distutils import dir_util

if sys.version_info[0] != 2 and sys.version_info[1] != 7:
    print('Python version must be 2.7! Exiting!\n')
    exit(1)

if os.getuid() != 0:
    print('Installer must be run as ROOT! Exiting!\n')
    exit(1)


TO_INSTALL = ''
USER = ''
GROUP = ''

# Python executable. Alternatively, it can be "python2.7".
PYTHON_EXE = sys.executable

# The proxy is used only if you need a proxy to connect to internet,
# And `setuptools` is not installed, or some dependencies are missing
HTTP_PROXY = 'http://CrConstantin:1XXX@http-proxy.itcnetworks:3128'


# --------------------------------------------------------------------------------------------------
# Install  Server  or  Client ?
# --------------------------------------------------------------------------------------------------

# If installer was run with parameter "--server"
if sys.argv[1:2] == ['--server']:
    TO_INSTALL = 'server'

# If installer was run with parameter "--client"
elif sys.argv[1:2] == ['--client']:
    TO_INSTALL = 'client'

# If installer was run with parameter "--both"
elif sys.argv[1:2] == ['--both']:
    TO_INSTALL = 'both'

else:
    while 1:
        print('\nPlease select what you wish to install:')
        print('[1] the Twister clients')
        print('[2] the Twister servers')
        print('[3] both client and server')
        print('[0] exit, don\'t install anything')

        selected = raw_input('Your choice: ')
        if selected == '1':
            print('Will install clients.\n')
            TO_INSTALL = 'client'
            break
        elif selected == '2':
            print('Will install servers.\n')
            TO_INSTALL = 'server'
            break
        elif selected == '3':
            print('Will install both client and server.\n')
            TO_INSTALL = 'both'
            break
        elif selected in ['0', 'q', 'x']:
            print('Ok, exiting!\n')
            exit(0)
        else:
            print('`%s` is not a valid choice!' % selected)
        del selected


# --------------------------------------------------------------------------------------------------
# For what user will you install ?
# --------------------------------------------------------------------------------------------------

# Find the users
users = os.listdir('/home/')
users.sort()

try:
    i = users.index('lost+found')
    users.pop(i)
except: pass

# If there are more users, choose
if len(users) > 1:

    while 1:
        print('Please select the user you are installing for:')
        for i in range(1, len(users)+1):
            print('[%i] : %s' % (i, users[i-1]))

        selected = raw_input('Your choice: ')
        try:
            usr = int(selected)
        except:
            usr = None
            print('`%s` is not a valid choice!' % selected)
            continue
        if usr not in range(1, len(users)+1):
            print('`%s` is not a valid choice!' % selected)
            continue

        USER = users[usr - 1]
        g = subprocess.check_output(['groups', USER])
        GROUP = ''.join(g.split()[:3])

        selected = raw_input('\nYou selected user `%s` from group `%s`.\nIs that correct? (yes/no): ' % \
            (USER, GROUP))
        if selected.strip().lower() == 'yes':
            break
        else:
            print('Canceling...')
            continue

# If there's only 1 user, no need to choose
else:

    USER = users[0]
    g = subprocess.check_output(['groups', USER])
    GROUP = ''.join(g.split()[:3])

del users


# --------------------------------------------------------------------------------------------------
# Previous installations of Twister
# --------------------------------------------------------------------------------------------------

INSTALL_PATH = '/home/%s/twister/' % USER

if os.path.exists(INSTALL_PATH):
    print('WARNING! Another version of Twister is installed at `%s`!' % INSTALL_PATH)
    print('If you continue, all files from that folder will be DELETED,')
    print('Only the `config` folder will be saved!')
    selected = raw_input('Are you sure you want to continue? (yes/no): ')

    if selected.strip().lower() == 'yes':

        if os.path.exists(INSTALL_PATH + 'config'):
            print('Back-up `config` folder...')
            shutil.move(INSTALL_PATH + 'config', os.getcwd())

        # Deleting previous versions of Twister
        try: dir_util.remove_tree(INSTALL_PATH)
        except: pass
        try: os.mkdir(INSTALL_PATH)
        except: pass

        if os.path.exists(os.getcwd() + '/config'):
            print('Moving `config` folder back...')
            shutil.move(os.getcwd() + '/config', INSTALL_PATH)
    else:
        print('\nPlease backup all your data, then restart the installer.')
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
        'MySQL-python',
    ]

    # Import names used for testing
    library_names = [
        'beaker',
        'mako',
        'cherrypy',
        'MySQLdb',
    ]

    # Versions
    library_versions = [
        '1.6',
        '0.6',
        '3.2',
        '1.2',
    ]

    # Files to move in twister folder
    to_copy = [
        'bin/start_ce',
        'bin/start_ra',
        'bin/start_httpserver',
        'demo/',
        'doc/',
        'src/server/',
        'src/common/',
        'src/config/',
        'src/lib/',
        'src/trd_party/',
    ]

elif TO_INSTALL == 'client':
    # The client doesn't have important dependencies
    dependencies = ['pexpect']
    library_names = ['pexpect']
    library_versions = ['2.3']

    # Files to move in twister folder
    to_copy = [
        'bin/start_ep.py',
        'bin/config_ep.json',
        'doc/',
        'src/client/',
        'src/common/__init__.py',
        'src/common/constants.py',
    ]

else:
    # Client + Server
    dependencies = [
        'pexpect',
        'Beaker',
        'Mako',
        'CherryPy',
        'MySQL-python',
    ]

    # Import names used for testing
    library_names = [
        'pexpect',
        'beaker',
        'mako',
        'cherrypy',
        'MySQLdb',
    ]

    # Versions
    library_versions = [
        '2.3',
        '1.6',
        '0.6',
        '3.2',
        '1.2',
    ]

    # Files to move in twister folder
    to_copy = [
        'bin/start_ep.py',
        'bin/config_ep.json',
        'bin/start_ce',
        'bin/start_ra',
        'bin/start_httpserver',
        'demo/',
        'doc/',
        'src/client/',
        'src/server/',
        'src/common/',
        'src/config/',
        'src/lib/',
        'src/trd_party/',
    ]


# Using HTTP_PROXY environment variable?
if HTTP_PROXY:
    os.putenv('HTTP_PROXY', HTTP_PROXY)
    proxy_support = urllib2.ProxyHandler({'http': HTTP_PROXY})
    opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)

# Checking internet connection and Pypi availability
try:
    pypi = urllib2.urlopen('http://pypi.python.org/simple/')
    if pypi.read(255):
        INTERNET = True
        print('\nInternet connection is available.\n')
    else:
        INTERNET = False
        print('\nCannot connect! Check the internet connection, or the Proxy settings!\n')
    del pypi
except:
    INTERNET = False
    print('\nCannot connect! Check the internet connection, or the Proxy settings!\n')


# --------------------------------------------------------------------------------------------------
# Starting the install process
# --------------------------------------------------------------------------------------------------

root_folder = os.sep.join( os.getcwd().split(os.sep)[:-1] )
cwd_path = os.getcwd() + os.sep
pkg_path = cwd_path + 'packages/'

try:
    import setuptools
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

for i in range(len(dependencies)):

    lib_name = dependencies[i]
    lib_version = library_versions[i]
    import_name = library_names[i]

    try:
        # Can be imported ?
        lib = __import__(import_name)
        # The version is ok ?
        ver = eval('lib.__version__')
        del lib
        if ver < lib_version:
            print('Testing: Library `%s` has version `%s` and it must be `%s` or newer! Will install...' %
                (import_name, ver, lib_version))
        else:
            print('Testing: Imported `%s` ver %s OK. No need to re-install.' % (import_name, ver))
            continue
    except:
        print('Testing: Python library `%s` will be installed...' % import_name)

    # ----------------------------------------------------------------------------------------------
    # Internet connection available
    # ----------------------------------------------------------------------------------------------

    if INTERNET:

        # MySQL Python requires Python-DEV and must be installed from repositories
        if lib_name == 'MySQL-python':
            print('\n~~~ Installing `%s` from System repositories ~~~\n' % lib_name)

            if platform.dist()[0] == 'SuSE':
                tcr_proc = subprocess.Popen(['zypper', 'install', 'python-mysql'], cwd=pkg_path)
            if platform.dist()[0] == 'fedora':
                tcr_proc = subprocess.Popen(['yum', '-y', 'install', 'python-mysql'], cwd=pkg_path)
            else:
                tcr_proc = subprocess.Popen(['apt-get', 'install', 'python-mysqldb', '--yes'], cwd=pkg_path)

            tcr_proc.wait()

        # All other packages are installed with easy_install
        else:
            print('\n~~~ Installing `%s` from Python repositories ~~~\n' % lib_name)
            tcr_proc = subprocess.Popen(['easy_install', lib_name], cwd=pkg_path)
            tcr_proc.wait()

        if tcr_proc.returncode:
            print('\n~~~ `%s` cannot be installed! It MUST be installed manually! ~~~\n' % lib_name)
        else:
            print('\n~~~ Successfully installed %s ~~~\n' % lib_name)

    # ----------------------------------------------------------------------------------------------
    # No internet connection
    # ----------------------------------------------------------------------------------------------

    else:
        print('\n~~~ Installing `%s` from tar files ~~~\n' % lib_name)

        p_library = glob.glob(pkg_path + lib_name + '*.tar.gz')

        if not p_library:
            print('\n~~~ Cannot find `%s`! You MUST install it manually! ~~~\n' % (lib_name+'*.tar.gz'))
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


# --------------------------------------------------------------------------------------------------
# Start copying files
# --------------------------------------------------------------------------------------------------

print('')

for fname in to_copy:
    fpath = root_folder + os.sep + fname
    dpath = os.path.dirname(fname)

    # Copy into folder without `src`
    if dpath.startswith('src/'):
        dpath = dpath[4:]

    if dpath:
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
        if fname.startswith('src/'):
            fname = fname[4:]
        try:
            file_util.copy_file(fpath, INSTALL_PATH + dpath)
            print('Copied file `%s` to `%s`.' % (fpath, INSTALL_PATH+dpath))
        except:
            print('Cannot copy file `%s` to `%s`!' % (fpath, INSTALL_PATH+dpath))

    else:
        print('Path `%s` does not exist and will not be copied!' % fpath)

#

tcr_proc = subprocess.Popen(['chown', GROUP, INSTALL_PATH, '-R'],)
tcr_proc.wait()
tcr_proc = subprocess.Popen(['chmod', '774', INSTALL_PATH, '-R'],)
tcr_proc.wait()

os.system('chown %s %s -R' % (GROUP, INSTALL_PATH))
os.system('chmod 774 %s -R' % INSTALL_PATH)
os.system('find %s -name "*.xml" -exec chmod 664 {} \;' % INSTALL_PATH)
os.system('find %s -name "*.py" -exec chmod 664 {} \;' % INSTALL_PATH)
os.system('find %s -name "*.tcl" -exec chmod 664 {} \;' % INSTALL_PATH)

#
try: os.mkdir(INSTALL_PATH + 'src/.twister_cache')
except: pass
#

for fname in glob.glob(INSTALL_PATH + 'bin/*'):
    lines = open(fname).readlines()
    lines.insert(4, ('export TWISTER_PATH=%s\n' % INSTALL_PATH))
    open(fname, 'w').write(''.join(lines))

print('Twister installation done!\n')
