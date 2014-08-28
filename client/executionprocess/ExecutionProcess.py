#!/usr/bin/env python2.7

# version: 3.019

# File: ExecutionProcess.py ; This file is part of Twister.

# Copyright (C) 2012-2014, Luxoft

# Authors:
#    Andreea Proca <aproca@luxoft.com>
#    Andrei Costachi <acostachi@luxoft.com>
#    Cristi Constantin <crconstantin@luxoft.com>

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Execution Process (EP) should be started as a service, on system startup.
Each EP has a unique name for its user, called Ep Name.
EP gets his status from CE every few seconds. The status can be changed using the Java interface.
When it receives START from CE, it will start the Runner that will execute all test files from suite,
  send all Runner logs to CE and after the execution, it will wait for another START to repeat the cycle.
EP is basically a simple service, designed to start and stop the Runner.
All the hard work is made by the Runner.
"""
from __future__ import print_function
from __future__ import with_statement

import os
import sys
import time
import copy
import socket
import signal
import shutil
import binascii
import platform
import inspect
import traceback
import tarfile
import argparse

from pprint import pprint
from string import Template
from threading import Thread
from thread import allocate_lock

import rpyc
from rpyc import BgServingThread

# The path when run from ./start_client
TWISTER_PATH = os.getenv('TWISTER_PATH')
# If running portable, find the path of the script
if not TWISTER_PATH:
    TWISTER_PATH, _ = os.path.split(__file__)
# Or the current directory
if not TWISTER_PATH:
    TWISTER_PATH = os.getcwd()
# Make absolute path and strip the eventual slash
TWISTER_PATH = os.path.abspath(TWISTER_PATH).rstrip('/')

os.environ['TWISTER_PATH'] = TWISTER_PATH
if not TWISTER_PATH:
    print('\nTWISTER_PATH environment variable is not set! Exiting!\n')
    exit(1)
else:
    print('\nTWISTER_PATH is set to `{}`.\n'.format(TWISTER_PATH))
sys.path.append(TWISTER_PATH)

PORTABLE = False
EP_CACHE, EP_LOG = None, None
PROXY_LOCK = allocate_lock() # Lock the connection access
RUNNER = None
LOGGER = None
DEBUG = False
CE_PROXY   = None # Used to keep the current Central Engine connection
BG_SERVER  = None # Background serving server
USER_NAME  = None # Used to check the Central Engine connection
EP_NAME    = None # Used by the logger when sending the Live Log

TMPL_LIB = """
PROXY_ADDR = "$proxy"
USER = "$user"
EP = "$ep"
SUT = "$sut"
SUITE_ID = "$suite_id"
SUITE_NAME = "$suite_name"
FILE_ID = "$file_id"
FILE_NAME = "$file_name"
"""

from RunnerClasses import *


# ------------------------------------------------------------------------------

# Test statuses :

STATUS_PENDING  = 10
STATUS_WORKING  = 1
STATUS_PASS     = 2
STATUS_FAIL     = 3
STATUS_SKIPPED  = 4
STATUS_ABORTED  = 5
STATUS_NOT_EXEC = 6
STATUS_TIMEOUT  = 7
STATUS_INVALID  = 8
STATUS_WAITING  = 9

TEST_STATUS = {'pending':STATUS_PENDING,
    'working':STATUS_WORKING, 'pass':STATUS_PASS, 'fail':STATUS_FAIL,
    'skipped':STATUS_SKIPPED, 'aborted':STATUS_ABORTED,
    'not executed':STATUS_NOT_EXEC, 'timeout':STATUS_TIMEOUT,
    'invalid':STATUS_INVALID, 'waiting':STATUS_WAITING}

REVERSED_STATUS = dict((v, k) for k, v in TEST_STATUS.iteritems())

# ------------------------------------------------------------------------------

class EpService(rpyc.Service):
    """
    Dummy service.
    """
    def exposed_hello(self, param=None):
        """
        For testing connection.
        """
        return True

    def exposed_start_ep(self, *arg, **kw):
        """
        Fake function.
        """
        return True

    def exposed_stop_ep(self, *arg, **kw):
        """
        Fake function.
        """
        return True

    def exposed_echo(self, text):
        """
        Echo function.
        """
        print('Echo: {}'.format(text))
        return None

    def exposed_dbg_continue(self):
        """
        Continue Debug.
        """
        global DEBUG
        DEBUG = False
        return None


def proxy():
    """
    Dinamically connect to the Central Engine.
    """
    global USER_NAME, EP_NAME, CE_PATH
    global CE_PROXY, BG_SERVER

    # RPyc config
    config = {
        'allow_pickle': True,
        'allow_getattr': True,
        'allow_setattr': True,
        'allow_delattr': True,
        'allow_all_attrs': True,
        }

    with PROXY_LOCK:

        ce_ip, ce_port = CE_PATH.split(':')

        # Try to reuse the old connection
        if  CE_PROXY is not None:
            try:
                CE_PROXY.ping(data='Hello', timeout=5.0)
                return CE_PROXY.root
            except Exception:
                CE_PROXY = None
                print('EP Warn: Disconnected from the Central Engine...\n')
        else:
            CE_PROXY = None

        # Connect to the RPyc server
        print('EP Info: Connecting to the Central Engine...')

        try:
            # Transform XML-RPC port into RPyc Port; RPyc port = XML-RPC port + 10 !
            p = rpyc.connect(ce_ip, int(ce_port) + 10, service=EpService, config=config)
            p.root.hello('ep::{}'.format(EP_NAME))
        except Exception:
            print('*ERROR* Cannot connect to CE path `{}`! Exiting!'.format(CE_PATH))
            CE_PROXY = None
            return None

        # Authenticate on RPyc server
        try:
            p.root.login(USER_NAME, 'EP')
            CE_PROXY = p
        except Exception:
            print('*ERROR* Cannot authenticate on CE path `{}`! Exiting!'.format(CE_PATH))
            CE_PROXY = None
            return None

        print('EP Debug: Connected and authenticated to CE at `{}`.\n'.format(CE_PATH))

        # Launch bg server
        try:
            BG_SERVER = BgServingThread(CE_PROXY)
        except Exception:
            print('*ERROR* Cannot launch Bg serving thread! Exiting!')
            CE_PROXY = None
            return None

        if PORTABLE:
            print('EP Debug: Must register the EP...')
            try:
                # Register this EP to the Central Engine
                p.root.hello('client', {'eps': [EP_NAME]})
                print('EP Debug: Register EP successful!\n')
                return CE_PROXY.root
            except Exception:
                print('*ERROR* Cannot register this EP! Exiting!')
                return None
        else:
            return CE_PROXY.root

#

class Logger(object):

    def __init__(self):
        self.closed = False
        self.buffer = ''  # The text buffer
        self.timer = 0    # Last time the log was sent to CE
        sys.__stdout__.write('EP Debug: Creating a portable logger...')
        sys.__stdout__.flush()
        sys.stdout = self


    def write(self, text):
        """
        Write in the OUT stream, in the log file and send to CE.
        """
        # Write in the OUTPUT stream
        sys.__stdout__.write(text)
        sys.__stdout__.flush()
        # Write in the file
        with open(EP_LOG, 'a') as logfile:
            logfile.write(text)
        # Send the message to the Central Engine
        if  CE_PROXY is not None:
            self.logLive(text)

    def logLive(self, text):
        """
        If the time is right and the buffer is large enough,
        send the text to the Central Engine.
        """
        if  CE_PROXY is None:
            return
        ctimer = time.time()
        self.buffer += text

        if ((ctimer - self.timer) > 1.5) and len(self.buffer):
            proxy().log_live(EP_NAME, binascii.b2a_base64(self.buffer))
            self.timer = ctimer
            self.buffer = ''
        elif len(self.buffer) > 256:
            proxy().log_live(EP_NAME, binascii.b2a_base64(self.buffer))
            self.buffer = ''

    def close(self, *args, **kw):
        """
        Close the logger.
        """
        # Restore the normal stdout
        sys.stdout = sys.__stdout__
        # Send last chunk
        if self.buffer:
            proxy().log_live(EP_NAME, binascii.b2a_base64(self.buffer))
            self.buffer = ''
        self.closed = True

#

class ThreadedLogger(Thread):

    def __init__(self):
        """
        Mock Logger.
        """
        Thread.__init__(self)
        self.setDaemon(True)
        self.buffer = ''   # The text buffer
        self.read_len = 0  # Read file position
        self.timer  = 0    # Last time the log was sent to CE
        self.closed = False
        self.acc_lock = allocate_lock()
        print('EP Debug: Creating a threaded logger...')

    def run(self):
        """
        Watch file changes.
        The log files will be reset by CE.
        """
        # Wait a little, before enter the cycle
        time.sleep(1)
        while not self.closed:
            with self.acc_lock:
                data = self.tail()
                self.logLive(data)
            # Wait and retry...
            time.sleep(1)
        # The end
        with self.acc_lock:
            data = self.tail()
            self.logLive(data, force=True)

    def tail(self):
        """
        Tail on a file.
        """
        vString = ''
        with open(EP_LOG, 'r') as f:
            # Go at "current position"
            f.seek(self.read_len, 0)
            vString = f.read()
            vLen = len(vString)
        # Fix double new-line
        vString = vString.replace('\r\n', '\n')
        vString = vString.replace('\n\r', '\n')
        # Increment "current position"
        self.read_len += vLen
        return vString

    def logLive(self, text, force=False):
        """
        If the time is right and the buffer is large enough,
        send the text to the Central Engine.
        """
        if  CE_PROXY is None:
            return
        ctimer = time.time()
        self.buffer += text

        if ((ctimer - self.timer) > 1.5) and len(self.buffer):
            proxy().log_live(EP_NAME, binascii.b2a_base64(self.buffer))
            self.timer = ctimer
            self.buffer = ''
        elif len(self.buffer) > 256 or force:
            proxy().log_live(EP_NAME, binascii.b2a_base64(self.buffer))
            self.buffer = ''

    def write(self, text):
        # The write is from nohup, not here
        pass

    def close(self, *args, **kw):
        """
        This will force the thread to exit.
        """
        # Last read to make sure all CLI.log is captured
        data = self.tail()
        self.logLive(data, force=True)
        self.closed = True


# # #


def dbg_breakpoint():
    """
    This function be called only from a test!
    It will block the test and wait for the "NEXT" command.
    """
    global DEBUG
    DEBUG = True
    print('\n>> Enter Breakpoint >>\n')

    stack = inspect.stack()
    f_vars = dict(stack[1][0].f_locals)
    del f_vars['__builtins__']
    pprint(f_vars)
    print('\n--- End of Stack ---\n')

    while DEBUG:
        time.sleep(0.5)
    print('>> Exit Breakpoint >>')


# # #


class TwisterRunner(object):

    def __init__(self, USER_NAME, EP_NAME, CE_PATH):
        self.epName   = EP_NAME
        self.userName = USER_NAME
        self.cePath   = CE_PATH
        self.sut      = ''

        self.runners = {}
        self.libs_list = []
        self.commonLib = None
        self.exit_on_test_fail = False
        self.tc_delay = 0


    def __del__(self):
        self.exit()


    def stop(self, timer_f=0.0, *args, **kw):
        """
        Send stop status.
        """
        print('\n~ Stop the Execution Process ~\n')
        # Send the STOP signal? Default, yes.
        stop = kw.get('stop', True)
        if stop:
            try:
                proxy().set_ep_status(self.epName, 0, msg='Execution finished in `{:.2f}` seconds.'.format(timer_f))
            except Exception as e:
                print('Exception on change status: `{}`!'.format(e))
        return True


    def exit(self, timer_f=0.0, *args, **kw):
        """
        Exit safely.
        """
        # Wait a while...
        if not PORTABLE:
            time.sleep(1)
        # Send stop status
        self.stop(timer_f, args, kw)
        # Flush all messages
        LOGGER.close()
        # Close everything
        CE_PROXY.close()
        BG_SERVER.stop()
        # Ok to exit
        return True


    def main(self):

        ce = proxy()
        if not ce:
            print('*ERROR* Cannot connect to server! Farewell!\n')
            exit(1)

        print('~ Start the Execution Process ~')
        print('~ User: {} ; EP: {} ; CE path: {} ~\n'.format(self.userName, self.epName, self.cePath))

        # All known runners
        self.runners = {
            'tcl': None,
            'python': None,
            'perl': None,
            'java': None,
        }

        # Inject all known info about this EP
        ep_host = socket.gethostname()
        try: ep_ip = socket.gethostbyname(ep_host)
        except Exception: ep_ip = ''
        if platform.system().lower() == 'windows':
            system = platform.machine() +' '+ platform.system() +', '+ platform.release()
        else:
            system = platform.machine() +' '+ platform.system() +', '+ ' '.join(platform.linux_distribution())
        ce.set_ep_variable(self.epName, 'twister_ep_os', system)
        ce.set_ep_variable(self.epName, 'twister_ep_hostname', ep_host)
        ce.set_ep_variable(self.epName, 'twister_ep_ip', ep_ip)
        ce.set_ep_variable(self.epName, 'twister_ep_python_revision', '.'.join([str(v) for v in sys.version_info]) )
        ce.set_ep_variable(self.epName, 'last_seen_alive', time.strftime('%Y-%m-%d %H:%M:%S'))

        # Get the `exit on test Fail` value
        self.exit_on_test_fail = ce.get_user_variable('exit_on_test_fail')
        # Get tests delay
        self.tc_delay = ce.get_user_variable('tc_delay')

        # After getting Test-Bed name, save all libraries from CE
        self.libs_list = []
        self.saveLibraries()
        # After download, inject libraries path for the current EP
        sys.path.insert(0, '{}/ce_libs'.format(EP_CACHE))

        try:
            import ce_libs
        except Exception as e:
            print('*ERROR* Cannot import the CE libraries! `{}`'.format(e))
            self.exit()
        try:
            from TscCommonLib import TscCommonLib
            self.commonLib = TscCommonLib()
        except Exception as e:
            print('*ERROR* Cannot import the Common libraries! `{}`'.format(e))
            self.exit()

        # Run the tests!
        try:
            while 1:
                self.tests()
                if not PORTABLE:
                    break
        except Exception:
            trace = traceback.format_exc()[34:].strip()
            print('Break cycle: `{}`'.format(trace))

        return True


    def makeCeLibs(self, suite_id='', suite_name='', file_id='', file_name=''):
        """
        Re-create the ce_libs library file.
        """
        libs_path = '{}/ce_libs'.format(EP_CACHE)

        # Create ce_libs library file
        __init = open(libs_path + os.sep + 'ce_libs.py', mode='w', buffering=0)
        tmpl = Template(TMPL_LIB)
        data = {
            'proxy': self.cePath, 'user': self.userName, 'ep': self.epName,
            'sut': self.sut, 'suite_id': suite_id, 'suite_name': suite_name,
            'file_id': file_id, 'file_name': file_name,
        }
        __init.write(tmpl.substitute(**data))
        __init.close()

        return True


    def saveLibraries(self, libs_list=''):
        """
        Downloads all libraries from Central Engine.
        """
        libs_path = '{}/ce_libs'.format(EP_CACHE)
        reset_libs = False

        if not libs_list:
            # This is a list with unique names, sorted alphabetically
            libs_list = proxy().list_libraries(False)
            # Pop CommonLib from the list of libraries...
            if 'TscCommonLib.py' in libs_list:
                libs_list.pop(libs_list.index('TscCommonLib.py'))
            # And inject it in the first position! This is important!
            libs_list.insert(0, 'TscCommonLib.py')
            # Save the list for later
            self.libs_list.extend(libs_list)
            reset_libs = True
        else:
            libs_list = [lib.strip() for lib in libs_list.split(';') if lib.strip() not in self.libs_list]
            self.libs_list.extend(libs_list)

        if reset_libs:
            # Remove libs path only if saving libraries for all project
            shutil.rmtree(libs_path, ignore_errors=True)
            # Create the path, after removal
            try: os.makedirs(libs_path)
            except Exception as e: pass

        # Create the ce_libs file
        self.makeCeLibs()

        all_libs = [] # Normal python files or folders
        zip_libs = [] # Zip libraries

        for lib in libs_list:
            # Null libraries ?
            if not lib:
                continue
            # Fix / and // issues
            lib = lib.lstrip('/').replace('//', '/')
            # Already in the list ?
            if lib in zip_libs or lib in all_libs:
                continue
            if lib.endswith('.zip'):
                zip_libs.append(lib)
            else:
                all_libs.append(lib)

        for lib_file in zip_libs:
            lib_data = proxy().download_library(lib_file)
            time.sleep(0.1) # Must take it slow
            if not lib_data:
                print('ZIP library `{}` does not exist!'.format(lib_file))
                continue

            print('Downloading Zip library `{}` ...'.format(lib_file))

            lib_pth = libs_path + os.sep + lib_file

            f = open(lib_pth, 'wb')
            f.write(lib_data)
            f.close() ; del f

        for lib_file in all_libs:
            lib_data = proxy().download_library(lib_file)
            time.sleep(0.1) # Must take it slow
            if not lib_data:
                print('Library `{}` does not exist!'.format(lib_file))
                continue

            print('Downloading library `{}` ...'.format(lib_file))

            # If this is a "deep" file, or folder
            if '/' in lib_file:
                lib_pth = libs_path + '/deep'
            else:
                lib_pth = libs_path + '/' + lib_file

            try:
                with open(lib_pth, 'wb') as f:
                    f.write(lib_data)
            except Exception as e:
                print('Cannot save library file `{}`: `{}`!'.format(lib_file, e))
                continue

            # If the file doesn't have an ext, or it's a deep file, or folder,
            # it's a TGZ library and must be extracted
            if (not os.path.splitext(lib_file)[1]) or ('/' in lib_file):
                # Rename the TGZ
                tgz = lib_pth + '.tgz'
                os.rename(lib_pth, tgz)
                with tarfile.open(tgz, 'r:gz') as binary:
                    os.chdir(libs_path)
                    binary.extractall()
                    time.sleep(0.05)
                    os.remove(tgz)

        if reset_libs:
            print('... all libraries downloaded.\n')


    def tests(self):
        """
        Cycle in all files, run each file, in order.
        """
        # Count the time
        glob_time = time.time()
        last_time = glob_time
        time_diff = 30

        if proxy().get_ep_status(self.epName) == 'running':
            print('EP Info: Start running the tests!')
        # Portable ?
        elif PORTABLE:
            print('EP Info: Waiting for the EP to start...\n')
            while True:
                time.sleep(2)
                glob_time = time.time()
                if  glob_time > last_time + time_diff:
                    last_time = glob_time
                    print('Still waiting for the start signal...')
                # Running !
                if proxy().get_ep_status(self.epName) == 'running':
                    break
            # Must re-check the libraries !
            self.saveLibraries()
        else:
            print('EP Warn: EP name `{}` is NOT running! Exiting!\n'.format(self.epName))
            return self.exit(timer_f=0.0, stop=False)

        # Download the Suites Manager structure from Central Engine!
        # This is the initial structure, created from the Project.XML file.
        data = proxy().get_ep_variable(self.epName, 'suites')
        suitesManager = copy.deepcopy(data)
        del data

        # Used by all files
        suite_id    = None
        suite_data  = None
        suite_name  = None # Suite name string. This varies for each file.
        abort_suite = False # Abort suite X, when setup file fails.

        # Import all custom exceptions
        from TscCommonLib import ExceptionTestFail, ExceptionTestAbort, ExceptionTestTimeout, ExceptionTestSkip


        for id, node in suitesManager.iter_nodes(None, []):

            # When starting a new suite or sub-suite ...
            # Some files don't belong to this suite, they might belong to the parent of this suite,
            # so each file must update the suite ID!
            if node['type'] == 'suite':

                if not node['children']:
                    print('TC warning: Nothing to do in suite `{}`!\n'.format(id))
                    continue

                self.sut = node['sut']
                suite_id   = id
                suite_data = node
                suite_name = node['name']
                suite_str  = suite_id +' - '+ suite_name

                # If this is a top level suite, set current_suite flag in EP Variables
                if suite_id in suitesManager:
                    proxy().set_ep_variable(self.epName, 'curent_suite', suite_id)

                print('\n===== ===== ===== ===== =====')
                print(' Starting suite `{}`'.format(suite_str))
                print('===== ===== ===== ===== =====\n')

                # Get list of libraries for current suite
                libList = node['libraries']
                if libList:
                    self.saveLibraries(libList)
                    print('')

                # The suite does not execute, so this is the end
                continue


            # Files section
            file_id = id
            suite_id = node['suite']
            # Update suite name from CE
            suite_name = proxy().get_suite_variable(self.epName, suite_id, 'name')

            # The name of the file
            filename = node['file']
            # If the file is NOT runnable, download it, but don't execute!
            runnable = node.get('Runnable', 'true')
            # Is this file a setup file?
            setup_file = node.get('setup_file', False)
            # Is this file a teardown file?
            teardown_file = node.get('teardown_file', False)
            # Test-case dependency, if any
            dependency = node.get('_depend').strip()
            # Is this test file optional?
            optional_test = node.get('Optional')
            # Configuration files?
            config_files = [c['name'] for c in node.get('_cfg_files', [])]
            # Get args
            args = node.get('param')
            if args:
                args = [p for p in args.split(',') if p]
            else:
                args = []

            # Extra properties, from the applet
            props = dict(node)
            props.update(suite_data)
            for prop in ['type', 'ep', 'sut', 'name', 'pd', 'libraries', 'children', 'clearcase',
                        'twister_tc_revision', 'status', 'file', 'suite', '_depend', '_dep_id',
                        'Runnable', 'setup_file', 'teardown_file', 'Optional', '_cfg_files', 'param']:
                # Removing all known File properties
                try:
                    del props[prop]
                except Exception:
                    pass

            # Re-create the ce_libs file
            self.makeCeLibs(suite_id, suite_name, file_id, os.path.split(filename)[1])


            print('<<< START filename: `{}:{}` >>>\n'.format(file_id, filename))

            # Set Last seen alive flag on this EP
            proxy().set_ep_variable(self.epName, 'last_seen_alive', time.strftime('%Y-%m-%d %H:%M:%S'))


            # If a setup file failed, abort the current suite and all sub-suites,
            # unless it's another setup, or teardown file from the current suite!
            # Abort_suite flag is set by the setup files from the beggining of a suite.
            if abort_suite:
                aborted_ids = suitesManager.get_files(suite_id=abort_suite, recursive=True)
                current_ids = suitesManager.get_files(suite_id=abort_suite, recursive=False)
                if aborted_ids and (file_id in aborted_ids):
                    # If it's a teardown file from current level suite, run it
                    if teardown_file and (file_id in current_ids):
                        print('Running a tear-down file...\n')
                    else:
                        print('EP Debug: Not executed file `{}` because of failed setup file!\n\n'.format(filename))
                        proxy().set_file_status(self.epName, file_id, STATUS_NOT_EXEC, 0.0) # File status ABORTED
                        try:
                            proxy().set_file_variable(self.epName, file_id, '_reason', 'Not executed, because of failed setup file!')
                        except Exception:
                            trace = traceback.format_exc()[34:].strip()
                            print('Exception on sending reason `{}`!'.format(trace))
                        print('<<< END filename: `{}:{}` >>>\n'.format(file_id, filename))
                        continue
                del aborted_ids, current_ids

            try:
                STATUS = proxy().get_ep_status(self.epName)
            except Exception:
                print('Cannot connect to the Central Engine! Exiting!\n')
                return False

            # When a test file is about to be executed and STOP is received, send status ABORTED
            if STATUS == 'stopped':
                proxy().set_file_status(self.epName, file_id, STATUS_ABORTED, 0.0) # File status ABORTED
                try:
                    proxy().set_file_variable(self.epName, file_id, '_reason', 'Manual stop! Time to exit!')
                except Exception:
                    trace = traceback.format_exc()[34:].strip()
                    print('Exception on sending reason `{}`!'.format(trace))
                print('~ STOP: Time to exit! ~')
                diff_time = time.time() - glob_time
                return self.exit(timer_f=diff_time, stop=False)

            # On pause, freeze cycle and wait for Resume or Stop
            elif STATUS == 'paused':
                proxy().echo(':: {} is paused!... Must RESUME to continue, or STOP to exit test suite...'.format(self.epName))
                vPauseMsg = False

                while 1:
                    # Print pause message
                    if not vPauseMsg:
                        print('~ PAUSE: Waiting for RESUME signal... ~\n')
                        vPauseMsg = True

                    # Wait ...
                    time.sleep(2)

                    try:
                        STATUS = proxy().get_ep_status(self.epName)
                    except Exception:
                        print('~ NOT EXECUTED: Connection lost, while waiting for resume ! ~\n')
                        return False

                    # On resume, stop waiting
                    if STATUS == 'running' or STATUS == 'resume':
                        proxy().echo(':: {} is no longer paused !'.format(self.epName))
                        break
                    # On stop...
                    elif STATUS == 'stopped':
                        # When a test is waiting for resume, but receives STOP, send status NOT EXECUTED
                        proxy().set_file_status(self.epName, file_id, STATUS_NOT_EXEC, 0.0)
                        try:
                            proxy().set_file_variable(self.epName, file_id, '_reason', 'Manual stop, while waiting for resume!')
                        except Exception:
                            trace = traceback.format_exc()[34:].strip()
                            print('Exception on sending reason `{}`!'.format(trace))
                        print('~ STOP: Received STOP, while waiting for resume ! ~')
                        # Exit the cycle
                        diff_time = time.time() - glob_time
                        return self.exit(timer_f=diff_time, stop=False)

            if dependency:
                dep_ok = True

                # Dependencies are separated by semi-colon
                for dep in dependency.split(';'):
                    dep = dep.strip()
                    if not dep:
                        continue
                    try:
                        (dep_id, dep_status) = dep.split(':')
                        dep_status = dep_status.lower()
                        if dep_status != 'any' and dep_status not in TEST_STATUS:
                            dep_status = 'invalid'
                    except Exception:
                        print('Invalid dependency `{}` will be ignored!'.format(dep))
                        continue

                    # Dependency file information
                    dep_info = proxy().get_dependency_info(dep_id)
                    if not dep_info:
                        print('Invalid dependency `{}` will be ignored!'.format(dep_id))
                        continue

                    dep_curr_status = REVERSED_STATUS.get(dep_info.get('status', -1), 'invalid')

                    # Wait for dependency to run
                    if  dep_curr_status in ['invalid', 'pending', 'working']:
                        print('\nWaiting for file `{}::{}` to finish execution...\n'.format(dep_info['id'], dep_info['file']))
                        while 1:
                            time.sleep(2)
                            dep_info['status'] = proxy().get_file_variable(dep_info['ep'], dep_info['id'], 'status')
                            dep_curr_status = REVERSED_STATUS.get(dep_info.get('status', -1), 'invalid')
                            # Reload info about dependency file
                            if  dep_curr_status not in ['invalid', 'pending', 'working']:
                                print('Dependency `{}::{}` ended with `{}`.\n'.format(dep_info['id'], dep_info['file'], dep_curr_status))
                                break
                    else:
                        print('Dependency `{}::{}` ended with `{}`.\n'.format(dep_info['id'], dep_info['file'], dep_curr_status))

                    if  dep_status == 'any':
                        print('Dependency `any` is ok.\n')
                    elif  dep_status != dep_curr_status:
                        print('Test file will be skipped (dependency required status to be `{}`) !\n'.format(dep_status))
                        dep_ok = False
                        break
                    else:
                        print('Dependency matched with success: `{}`.\n'.format(dep_status))

                if not dep_ok:
                    try:
                        # Send status SKIP
                        proxy().set_file_status(self.epName, file_id, STATUS_SKIPPED, 0.0)
                    except Exception:
                        trace = traceback.format_exc()[34:].strip()
                        print('Exception on dependency change file status `{}`!\n'.format(trace))
                    try:
                        proxy().set_file_variable(self.epName, file_id, '_reason', 'Skip, dependency not ok!')
                    except Exception:
                        trace = traceback.format_exc()[34:].strip()
                        print('Exception on sending reason `{}`!'.format(trace))
                    print('<<< END filename: `{}:{}` >>>\n'.format(file_id, filename))
                    continue


            # Download file from Central Engine!
            str_to_execute = proxy().download_file(self.epName, file_id)

            # If CE sent False, it means the file is empty, does not exist, or it's not runnable.
            if str_to_execute == '':
                print('EP Debug: File path `{}` does not exist!\n'.format(filename))
                if setup_file:
                    abort_suite = suite_id
                    print('*ERROR* Setup file for suite `{}` cannot run! No such file! All suite will be ABORTED!\n\n'.format(suite_name))
                try:
                    proxy().set_file_status(self.epName, file_id, STATUS_SKIPPED, 0.0) # Status SKIPPED
                except Exception:
                    trace = traceback.format_exc()[34:].strip()
                    print('Exception on change file status `{}`!\n'.format(trace))
                try:
                    proxy().set_file_variable(self.epName, file_id, '_reason', 'Skip, invalid setup file!')
                except Exception:
                    trace = traceback.format_exc()[34:].strip()
                    print('Exception on sending reason `{}`!'.format(trace))
                print('<<< END filename: `{}:{}` >>>\n'.format(file_id, filename))
                continue

            elif not str_to_execute:
                print('EP Debug: File `{}` will be skipped.\n'.format(filename))
                # Skipped setup files are ok, no need to abort.
                try:
                    proxy().set_file_status(self.epName, file_id, STATUS_SKIPPED, 0.0) # Status SKIPPED
                except Exception:
                    trace = traceback.format_exc()[34:].strip()
                    print('Exception on change file status `{}`!\n'.format(trace))
                try:
                    proxy().set_file_variable(self.epName, file_id, '_reason', 'File marked skip!')
                except Exception:
                    trace = traceback.format_exc()[34:].strip()
                    print('Exception on sending reason `{}`!'.format(trace))
                print('<<< END filename: `{}:{}` >>>\n'.format(file_id, filename))
                continue

            # Don' Run NON-runnable files, but Download them!
            if runnable.lower() != 'true':
                print('File `{}` is not runnable, it will be downloaded, but not executed.\n'.format(filename))
                fpath = EP_CACHE +os.sep+ os.path.split(filename)[1]
                f = open(fpath, 'wb')
                f.write(str_to_execute)
                f.close() ; del f
                try:
                    proxy().set_file_status(self.epName, file_id, STATUS_SKIPPED, 0.0) # Status SKIPPED
                except Exception:
                    trace = traceback.format_exc()[34:].strip()
                    print('Exception on change file status `{}`!\n'.format(trace))
                try:
                    proxy().set_file_variable(self.epName, file_id, '_reason', 'Skip, file is not runnable!')
                except Exception:
                    trace = traceback.format_exc()[34:].strip()
                    print('Exception on sending reason `{}`!'.format(trace))
                print('<<< END filename: `{}:{}` >>>\n'.format(file_id, filename))
                continue


            file_ext = os.path.splitext(filename)[1].lower()

            # If file type is TCL
            if file_ext in ['.tcl']:
                if not self.runners['tcl']:
                    self.runners['tcl'] = TCRunTcl()
                current_runner = self.runners['tcl']

            # If file type is PERL
            elif file_ext in ['.plx']:
                if not self.runners['perl']:
                    self.runners['perl'] = TCRunPerl()
                current_runner = self.runners['perl']

            # If file type is PYTHON
            elif file_ext in ['.py', '.pyc', '.pyo']:
                if not self.runners['python']:
                    self.runners['python'] = TCRunPython()
                current_runner = self.runners['python']

            # If file type is JAVA
            elif file_ext in ['.java']:
                if not self.runners['java']:
                    self.runners['java'] = TCRunJava()
                current_runner = self.runners['java']

            # Unknown file type
            else:
                print('TC warning: Extension type `{}` is unknown and will be ignored!\n'.format(file_ext))
                if setup_file:
                    abort_suite = suite_id
                    print('*ERROR* Setup file for suite `{}` cannot run! Unknown file extension! All suite will be ABORTED!\n\n'.format(suite_name))
                try:
                    proxy().set_file_status(self.epName, file_id, STATUS_NOT_EXEC, 0.0) # Status NOT_EXEC
                except Exception:
                    trace = traceback.format_exc()[34:].strip()
                    print('Exception on change file status `{}`!\n'.format(trace))
                try:
                    proxy().set_file_variable(self.epName, file_id, '_reason', 'Not executed, unknown file extension!')
                except Exception:
                    trace = traceback.format_exc()[34:].strip()
                    print('Exception on sending reason `{}`!'.format(trace))
                print('<<< END filename: `{}:{}` >>>\n'.format(file_id, filename))
                continue


            # If there is a delay between tests, wait here
            if self.tc_delay:
                print('EP Debug: Waiting {} seconds before starting the test...\n'.format(self.tc_delay))
                time.sleep(self.tc_delay)


            # Check the general status again...
            try:
                if proxy().get_ep_status(self.epName) == 'stopped':
                    # Exit the cycle
                    diff_time = time.time() - glob_time
                    return self.exit(timer_f=diff_time, stop=False)
            except Exception:
                print('Cannot connect to the Central Engine! Exiting!\n')
                return False

            # The file is preparing
            try:
                proxy().set_file_status(self.epName, file_id, STATUS_WORKING, 0.0) # Status WORKING
            except Exception:
                trace = traceback.format_exc()[34:].strip()
                print('Exception on change file status `{}`!\n'.format(trace))

            # Start counting test time
            timer_i = time.time()
            start_time = time.strftime('%Y-%m-%d %H:%M:%S')

            result = None
            reason = ''

            # --------------------------------------------------------------------------------------
            # RUN CURRENT TEST!

            globs = {
                'USER'      : self.userName,
                'EP'        : self.epName,
                'SUT'       : self.sut,
                'SUITE_ID'  : suite_id,
                'SUITE_NAME': suite_name,
                'FILE_ID'   : file_id,
                'FILE_NAME' : filename,
                'PROPERTIES': props,
                'CONFIG'    : config_files,
                'PROXY'     : proxy(),
                'breakpoint' : dbg_breakpoint
            }

            # Find all functions from commonLib
            to_inject = [f for f in dir(self.commonLib) if callable(getattr(self.commonLib, f))]
            # Expose all known function in tests
            for f in to_inject:
                # Ignore "private" functions
                if f[0] == '_':
                    continue
                # print('DEBUG: Exposing Python command `{}` into TCL...'.format(f))
                globs[f] = getattr(self.commonLib, f)

            try:
                result = current_runner._eval(str_to_execute, globs, args)
                # If the result is a pair of _RESULT, _REASON, unpack !
                if isinstance(result, tuple):
                    result, reason = result

            except AssertionError as e:
                result = 'FAIL'
                reason = str(e)

            except ExceptionTestFail as e:
                result = 'FAIL'
                reason = str(e)

            except ExceptionTestAbort as e:
                result = 'ABORT'
                reason = str(e)

            except ExceptionTestTimeout as e:
                result = 'TIMEOUT'
                reason = str(e)

            except ExceptionTestSkip as e:
                result = 'SKIP'
                reason = str(e)

            except (Exception, SystemExit):
                # On error, print the error message, but don't exit
                print('\nTest case exception:')
                print(traceback.format_exc()[34:].strip())
                print('\n>>> File `{}` execution CRASHED. <<<\n'.format(filename))

                proxy().echo('*ERROR* Error executing file `{}`!'.format(filename))
                try:
                    proxy().set_file_status(self.epName, file_id, STATUS_FAIL, (time.time() - timer_i))
                except Exception:
                    trace = traceback.format_exc()[34:].strip()
                    print('Exception on change file status `{}`!\n'.format(trace))

                try:
                    proxy().set_file_variable(self.epName, file_id, '_reason', 'Test execution CRASHED!')
                except Exception:
                    trace = traceback.format_exc()[34:].strip()
                    print('Exception on sending reason `{}`!'.format(trace))

                # If status is FAIL and the file is not Optional and Exit on test fail is ON, CLOSE the EP
                if not optional_test and self.exit_on_test_fail:
                    print('*ERROR* Mandatory file `{}` CRASHED! Closing the EP!\n\n'.format(filename))
                    proxy().echo('*ERROR* Mandatory file `{}::{}::{}` CRASHED! Closing the EP!'\
                        ''.format(self.epName, suite_name, filename))
                    print('<<< END filename: `{}:{}` >>>\n'.format(file_id, filename))
                    # Exit the cycle
                    break

                # If status is FAIL, and the file is a setup file, CANCEL all suite
                if setup_file:
                    abort_suite = suite_id
                    print('*ERROR* Setup file for suite `{}` returned FAIL! All suite will be ABORTED!\n\n'.format(suite_name))
                    proxy().echo('*ERROR* Setup file for `{}::{}` returned FAIL! All suite will be ABORTED!'\
                        ''.format(self.epName, suite_name))

                # Send crash detected = True
                proxy().set_file_variable(self.epName, file_id, 'twister_tc_crash_detected', 1)
                # Stop counting time. END OF TEST!
                timer_f = time.time() - timer_i
                end_time = time.strftime('%Y-%m-%d %H:%M:%S')
                print('Test statistics: Start time {} -- End time {} -- {:0.2f} sec.\n'.format(start_time, end_time, timer_f))
                print('<<< END filename: `{}:{}` >>>\n'.format(file_id, filename))
                # Skip this cycle, go to next file
                continue

            print('\n>>> File `{}` returned `{}`. <<<\n'.format(filename, result))

            # Stop counting time. END OF TEST!
            timer_f = time.time() - timer_i
            end_time = time.strftime('%Y-%m-%d %H:%M:%S')
            # --------------------------------------------------------------------------------------

            print('Test statistics: Start time {} -- End time {} -- {:0.2f} sec.\n'.format(start_time, end_time, timer_f))

            # Status as integer, or string
            try:
                result = int(result)
            except Exception:
                result = str(result).upper()

            try:
                if  result == 0 or result == STATUS_PASS or result == 'PASS':
                    result = STATUS_PASS
                    proxy().set_file_status(self.epName, file_id, STATUS_PASS, timer_f) # File status PASS
                elif result == STATUS_SKIPPED or result in ['SKIP', 'SKIPPED']:
                    result = STATUS_SKIPPED
                    proxy().set_file_status(self.epName, file_id, STATUS_SKIPPED, timer_f) # File status SKIPPED
                elif result == STATUS_ABORTED or result in ['ABORT', 'ABORTED']:
                    result = STATUS_ABORTED
                    proxy().set_file_status(self.epName, file_id, STATUS_ABORTED, timer_f) # File status ABORTED
                elif result == STATUS_NOT_EXEC or result in ['NOT-EXEC', 'NOT EXEC', 'NOT EXECUTED']:
                    result = STATUS_NOT_EXEC
                    proxy().set_file_status(self.epName, file_id, STATUS_NOT_EXEC, timer_f) # File status NOT_EXEC
                elif result == STATUS_TIMEOUT or result == 'TIMEOUT':
                    result = STATUS_TIMEOUT
                    proxy().set_file_status(self.epName, file_id, STATUS_TIMEOUT, timer_f) # File status TIMEOUT
                elif result == STATUS_INVALID or result == 'INVALID':
                    proxy().set_file_status(self.epName, file_id, STATUS_INVALID, timer_f) # File status INVALID
                else:
                    result = STATUS_FAIL
                    proxy().set_file_status(self.epName, file_id, STATUS_FAIL, timer_f) # File status FAIL
            except Exception:
                trace = traceback.format_exc()[34:].strip()
                print('EXCEPTION on changing file status `{}`!'.format(trace))

            try:
                proxy().set_file_variable(self.epName, file_id, '_reason', reason)
            except Exception:
                trace = traceback.format_exc()[34:].strip()
                print('EXCEPTION on sending reason `{}`!'.format(trace))


            # If status is not PASS
            if result != STATUS_PASS and result != 'PASS':

                # If status is FAIL and the file is not Optional and Exit on test fail is ON, CLOSE the EP
                if not optional_test and self.exit_on_test_fail:
                    print('*ERROR* Mandatory file `{}` did not PASS! Closing the EP!\n\n'.format(filename))
                    proxy().echo('*ERROR* Mandatory file `{}::{}::{}` did not PASS! Closing the EP!'\
                        ''.format(self.epName, suite_name, filename))
                    print('<<< END filename: `{}:{}` >>>\n'.format(file_id, filename))
                    # Exit the cycle
                    break

                if setup_file:
                    # If the file is a setup file, CANCEL all suite
                    abort_suite = suite_id
                    print('*ERROR* Setup file for suite `{}` did not PASS! All suite will be ABORTED!\n\n'.format(suite_name))
                    proxy().echo('*ERROR* Setup file for `{}::{}` returned FAIL! All suite will be ABORTED!'\
                        ''.format(self.epName, suite_name))

            if reason:
                if result == STATUS_FAIL:
                    print('Test failed because: `{}`.\n'.format(reason))
                elif result == STATUS_ABORTED:
                    print('Test was aborted because: `{}`.\n'.format(reason))
                elif result == STATUS_TIMEOUT:
                    print('Test timed out because: `{}`.\n'.format(reason))
                elif result == STATUS_SKIPPED:
                    print('Test was skipped because: `{}`.\n'.format(reason))


            print('<<< END filename: `{}:{}` >>>\n'.format(file_id, filename))

            #---------------------------------------------------------------------------------------

        print('\n==========================')
        print('. . . All tests done . . .')
        print('==========================\n')


        del suitesManager

        # Print the final message
        diff_time = time.time() - glob_time

        if PORTABLE:
            return self.stop(timer_f=diff_time)
        else:
            return self.exit(timer_f=diff_time)

#

def warmup():
    """
    Main function.
    """
    global EP_CACHE, EP_LOG, PORTABLE, LOGGER

    EP_CACHE = TWISTER_PATH + '/.twister_cache/' + EP_NAME
    EP_LOG = '{}/.twister_cache/{}_LIVE.log'.format(TWISTER_PATH, EP_NAME)

    # Create the EP folder
    try: os.makedirs(EP_CACHE)
    except Exception: pass

    # If this scripts is running Portable from twister/client/exec ...
    path = TWISTER_PATH
    path_exploded = []

    while 1:
        path, folder = os.path.split(path)
        if folder:
            path_exploded.append(folder)
        else:
            if path:
                path_exploded.append(path.rstrip(os.sep))
            break

    path_exploded.reverse()

    # Then append ths Twister Path to Python path
    if path_exploded[-1] == 'executionprocess':
        PORTABLE = True
        path_exploded = path_exploded[:-2]
        path = os.sep.join(path_exploded)
        print('Portable mode: Appending `{}` to python path.\n'.format(path))
        sys.path.append(path)

    # Reset the "portable log" file. If done here, the EP messages will be logged
    if PORTABLE:
        open(EP_LOG, 'w').close()

    # Launch a connection before the logger
    ce = proxy()
    if not ce:
        print('Cannot connect to server! Farewell!\n')
        exit(1)

    if  PORTABLE:
        # This will redirect all print into the EP log file
        LOGGER = Logger()
    else:
        LOGGER = ThreadedLogger()
        LOGGER.start()

    print('EP Debug: Created the logger.\n')


def signal_handler(*arg, **kw):
    global RUNNER
    del RUNNER
    CE_PROXY.close()
    BG_SERVER.stop()
    sys.exit()


# # #


if __name__ == '__main__':

    #
    # python -Bu ExecutionProcess.py -u user -e Windows-EP -s 127.0.0.1:8000
    #

    pars = argparse.ArgumentParser(prog='Execution Process', description='Linux/ Windows test runner for Twister.')
    pars.add_argument('-u', '--user', type=str, help='The username')
    pars.add_argument('-e', '--epname', type=str, help='The Execution Process name')
    pars.add_argument('-s', '--server', type=str, help='The Central Engine IP:Port', default='127.0.0.1:8000')
    argv = pars.parse_args()

    if not argv.user:
        print('Must specify an user ! Exiting !\n')
        exit(1)
    else:
        USER_NAME = argv.user

    if not argv.epname:
        print('Must specify an EP Name ! Exiting !\n')
        exit(1)
    else:
        EP_NAME = argv.epname

    # Central Engine
    CE_PATH = argv.server

    if os.name == "nt":
        try:
            import win32api
            win32api.SetConsoleCtrlHandler(signal_handler, True)
            print('Catching `Ctrl + C` signal OK.\n')
        except ImportError:
            raise Exception('Cannot import `win32api`!\n')
    else:
        signal.signal(signal.SIGINT, signal_handler)

    # Prepare everything
    warmup()

    # Launch !
    RUNNER = TwisterRunner(USER_NAME, EP_NAME, CE_PATH)
    RUNNER.main()
    del RUNNER


# Eof()
