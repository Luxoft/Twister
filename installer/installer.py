
'''
Twister has the following dependencies:

- Python 2.7	: The Central Engine, the Execution Process, the Test Runner, the Resource Allocator
		: and the reporting framework are all written in Python.

- BeautifulSoup	: www.crummy.com/software/BeautifulSoup/
		: Parses XML and HTML documents easily
		: (BeautifulSoup is included in `trd_party` folder and should not be installed)

- MySQL-python	: mysql-python.sourceforge.net/
		: Connects to MySQL databases
		: (MySQL-python requires the python2.7-dev headers in order to compile)

- CherryPy	: www.cherrypy.org/
		: High performance, minimalist Python web framework
		: (CherryPy is used to serve the reports and the Java Applet)

- Mako		: www.makotemplates.org/
		: Hyperfast and lightweight templating for the Python platform
		: (Mako is used for the reports)

- Beaker	: beaker.readthedocs.org/
		: Library for caching and sessions, in web applications and stand-alone Python scripts
		: (Beaker is optional; it is used by Mako, to cache the pages for better performance)

- pExpect	: sourceforge.net/projects/pexpect/
		: Spawn child applications, control them, respond to expected patterns in their output
		: (pExpect is optional; it is used by the Python test cases, to connect to FTP/ Telnet)

'''

import os, sys
import glob

import tarfile
import subprocess
from distutils import file_util
from distutils import dir_util

if not subprocess.check_output('id').startswith('uid=0(root)'):
    print('Installer must be run as ROOT! Exiting!\n')
    exit(1)

if sys.version_info[0] != 2 and sys.version_info[1] != 7:
    print('Python version must be 2.7! Exiting!\n')
    exit(1)


TO_INSTALL = ''
USER = ''
GROUP = ''

# Python executable. Alternatively, it can be "python2.7".
PYTHON_EXE = sys.executable
# The proxy is used only if `setuptools` is not installed, or some dependencies are missing
HTTP_PROXY = 'http://CrConstantin:1XXX@http-proxy.itcnetworks:3128/'


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
        elif selected in ['0', 'q', 'x']:
            print('Ok, exiting!\n')
            exit(0)
        else:
            print('`%s` is not a valid choice!' % selected)
        del selected


# Find the users
users = os.listdir('/home/')
users.sort()

try:
    i = users.index('lost+found')
    users.pop(i)
except: pass

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
    if selected.lower() == 'yes':
        break
    else:
        continue


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
else:
    # The client doesn't have important dependencies
    dependencies = ['pexpect']
    library_names = ['pexpect']
    library_versions = ['2.3']
    # Files to move in twister folder
    to_copy = [
        'bin/start_ep',
        'doc/',
        'src/client/',
        'src/common/__init__.py',
        'src/common/constants.py',
    ]


# --------------------------------------------------------------------------------------------------
# Starting the install process
# --------------------------------------------------------------------------------------------------

root_folder = os.sep.join( os.getcwd().split(os.sep)[:-1] )
cwd_path = os.getcwd() + os.sep
pkg_path = cwd_path + 'packages/'

# Using HTTP_PROXY environment variable?
if HTTP_PROXY:
    os.putenv('HTTP_PROXY', HTTP_PROXY)

try:
    import setuptools
    print('Python setuptools is installed. Ok.')
except:
    # Try to install python distribute (the new version of setuptools)
    tcr_proc = subprocess.Popen([PYTHON_EXE, '-u', (pkg_path+'distribute_setup.py')], cwd=cwd_path)
    tcr_proc.wait()
    del tcr_proc

    # Remove the downloaded file
    distribute_file = glob.glob('distribute*.tar.gz')
    if distribute_file:
        try: os.remove(distribute_file[0])
        except: print('Installer cannot delete file `%s`! You must delete it yourself!' % distribute_file[0])

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

    if distribute_file:

        print('\n~~~ Internet connection available, installing `%s` from Python repositories ~~~\n' % lib_name)

        tcr_proc = subprocess.Popen(['easy_install', lib_name], cwd=pkg_path)
        tcr_proc.wait()
        del tcr_proc

        print('\n~~~ Successfully installed %s ~~~\n' % lib_name)

    # ----------------------------------------------------------------------------------------------
    # No internet connection
    # ----------------------------------------------------------------------------------------------

    else:
        print('\n~~~ No internet connection, installing `%s` from tar files ~~~\n' % lib_name)

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

#

INSTALL_PATH = '/home/%s/twister/' % USER
print('')

# Delete previous version of Twister!
try: dir_util.remove_tree(INSTALL_PATH)
except: pass
try: os.mkdir(INSTALL_PATH)
except: pass

#

for fname in to_copy:
    fpath = root_folder + os.sep + fname
    dpath = os.path.dirname(fname)

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
        try:
            file_util.copy_file(fpath, INSTALL_PATH + dpath)
            print('Copied file `%s` to `%s`.' % (fpath, INSTALL_PATH+dpath))
        except:
            print('Cannot copy file `%s` to `%s`!' % (fpath, INSTALL_PATH+dpath))

    else:
        print('Path `%s` does not exist and will not be copied!' % dpath)

#

tcr_proc = subprocess.Popen(['chown', GROUP, INSTALL_PATH, '-R'],)
tcr_proc.wait()
tcr_proc = subprocess.Popen(['chmod', '774', INSTALL_PATH, '-R'],)
tcr_proc.wait()
del tcr_proc

print('Twister installation done!\n')
