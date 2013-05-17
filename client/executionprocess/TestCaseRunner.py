
# File: TestCaseRunner.py ; This file is part of Twister.

# version: 2.003

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
Test Case Runner has the following roles:
 - Connects to CE to receive the libs and files that must be executed on this station.
 - Takes the statuses from last run to see if the last run was killed by timeout,
    and if it was, it must skip the files that were already executed.
 - It reads the START/ STOP/ PAUSE/ RESUME status and if it's PAUSE, it waits for RESUME.
 - It checks for current file dependencies, if there are any, it waits for the dependency to be executed.
 - It skips the files that have status SKIP.
 - It downloads the files that must be executed, directly from CE.
 - It executes test files, counting the execution time. If the file takes too long, the Runner exits
    and will be restarted by EP. If the execution is successful, it sends the status and the time to CE.
 - The files that must be executed can be in many formats, ex: Python, Perl, TCL, the Runner detects
    them by extension.

This script should NOT be run manually!
'''

import os
import sys
import shutil
import time
import csv
import pickle
import marshal
import xmlrpclib
import tarfile
import traceback
from threading import Timer

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print('TWISTER_PATH environment variable is not set! Exiting!')
    exit(1)
sys.path.append(TWISTER_PATH)

from common.constants import *
import TestCaseRunnerClasses
from TestCaseRunnerClasses import *

#

def loadConfig():

    global globEpName
    global TWISTER_PATH
    EP_CACHE = TWISTER_PATH + '/.twister_cache/' + globEpName

    if not os.path.exists(EP_CACHE):
        print('TC error: Execution Process must be started first! Exiting!')
        exit(1)

    try:
        f = open(EP_CACHE + '/data.pkl', 'rb')
        data = f.read()
        CONFIG = pickle.loads(data)
        f.close() ; del f
        return CONFIG
    except:
        print('TC error: cannot read config file `%s`! Exiting!' % EP_CACHE)
        exit(1)

#

def saveLibraries(proxy, libs_list=''):
    '''
    Downloads all libraries from Central Engine.
    Not used in offline mode.
    '''
    global userName, globEpName, TWISTER_PATH

    libs_path = '{0}/.twister_cache/{1}/ce_libs'.format(TWISTER_PATH, globEpName)
    reset_libs = False

    if not libs_list:
        libs_list = proxy.getLibrariesList(userName)
        reset_libs = True
    else:
        libs_list = [lib.strip() for lib in libs_list.split(';')]

    if reset_libs:
        # Remove libs path only if saving libraries for all project
        shutil.rmtree(libs_path, ignore_errors=True)
        # Create the path, after removal
        try: os.makedirs(libs_path)
        except: pass

    all_libs = [] # Normal python files or folders
    zip_libs = [] # Zip libraries

    # If Reseting libs, open and destroy
    if reset_libs:
        __init = open(libs_path + os.sep + '__init__.py', 'w')
        __init.write('\nimport os, sys\n')
        __init.write('\nPROXY = "%s"\n' % CE_Path)
        __init.write('USER = "%s"\n' % userName)
        __init.write('EP = "%s"\n' % globEpName)
    # If not Reseting, just append
    else:
        __init = open(libs_path + os.sep + '__init__.py', 'a')

    for lib in libs_list:
        if not lib:
            continue
        if lib.endswith('.zip'):
            zip_libs.append(lib)
        else:
            all_libs.append(lib)

    if reset_libs:
        __init.write('\nall = ["%s"]\n\n' % ('", "'.join([os.path.splitext(lib)[0] for lib in all_libs])))
    else:
        __init.write('\nall += ["%s"]\n\n' % ('", "'.join([os.path.splitext(lib)[0] for lib in all_libs])))

    for lib_file in zip_libs:
        lib_data = proxy.downloadLibrary(userName, lib_file)
        time.sleep(0.2) # Must take it slow
        if not lib_data:
            print('ZIP library `{0}` does not exist!'.format(lib_file))
            continue

        print('Downloading Zip library `{0}` ...'.format(lib_file))

        # Write ZIP imports.
        __init.write('\nsys.path.append(os.path.split(__file__)[0] + "/%s")\n\n' % lib_file)
        lib_pth = libs_path + os.sep + lib_file

        f = open(lib_pth, 'wb')
        f.write(lib_data.data)
        f.close() ; del f

    for lib_file in all_libs:
        lib_data = proxy.downloadLibrary(userName, lib_file)
        time.sleep(0.2) # Must take it slow
        if not lib_data:
            print('Library `{0}` does not exist!'.format(lib_file))
            continue

        print('Downloading library `{0}` ...'.format(lib_file))

        ext = os.path.splitext(lib_file)
        # Write normal imports.
        __init.write('try:\n')
        __init.write('\timport %s\n' % ext[0])
        __init.write('\tfrom %s import *\n' % ext[0])
        __init.write('except Exception, e:\n\tprint("Cannot import library `{}`! Exception `%s`!" % e)\n\n'.format(ext[0]))
        lib_pth = libs_path + os.sep + lib_file

        f = open(lib_pth, 'wb')
        f.write(lib_data.data)
        f.close() ; del f

        # If the file doesn't have an ext, it's a TGZ library and must be extracted
        if not ext[1]:
            # Rename the TGZ
            tgz = lib_pth + '.tgz'
            os.rename(lib_pth, tgz)
			# Need to wait more on slow machines
            for i in range(20):
                try: tarfile.open(tgz, 'r:gz')
                except: time.sleep(0.5)
            with tarfile.open(tgz, 'r:gz') as binary:
                os.chdir(libs_path)
                binary.extractall()

    __init.close()

#

def Suicide(sig=None, msg=None, file_id=None, status_f=None, timer_f=None):
    '''
    Function Suicide is used to kill current process.
    '''
    if msg:
        proxy.echo(':: {0} {1}...'.format(globEpName, msg.strip()))
    if (file_id is not None) and (status_f is not None) and (timer_f is not None):
        proxySetTestStatus(file_id, status_f, timer_f)
    pid = os.getpid()
    print('TC debug: Killing PID `{0}`.'.format(pid))
    # Kill PID
    if sig and type(sig)==type(0):
        os.kill(pid, sig)
    else:
        os.kill(pid, 9)

#

def proxySetTestStatus(file_id, status, time_t):
    """
    Shortcut function for setting Test status.
    """
    global proxy, userName, globEpName
    proxy.setFileStatus(userName, globEpName, file_id, status, time_t)


def nextFile(iIndex):
    global proxy, userName, globEpName, tStats, tList, suite_id

    # Check again - file stats for current Suite
    tStats = proxy.getFileStatusAll(userName, globEpName, suite_id).split(',')
    # Check again - file list for current Suite
    tListN = proxy.getSuiteFiles(userName, globEpName, suite_id)

    if tList != tListN:
        print('The length of the suite has changed during runtime!\nOld suite: `{}`'\
              ', new suite: `{}`!\n'.format(tList, tListN))
        tList = tListN

    if len(tStats) != len(tList):
        print('TC critical: The len of statuses is different from the len of files! Exiting!')
        print('Stats: {0} ; Files: {1}\n'.format(tStats, tList))
        exit(1)

    # Increment and run the next file
    iIndex += 1
    # The last file in the suite
    if iIndex >= len(tList):
        return False

    return iIndex


def logMsg(logType, logMessage):
    """
    Shortcut function for sending a message in a log to Central Engine.
    """
    global proxy, userName
    proxy.logMessage(userName, logType, logMessage)


def getGlobal(var):
    """
    Function to get variables saved from Test files.
    """
    global proxy, userName, global_vars
    if var in global_vars:
        return global_vars[var]
    # Else...
    return proxy.getGlobalVariable(userName, var)


def setGlobal(var, value):
    """
    Function to keep variables sent from Test files.
    """
    global proxy, userName, global_vars
    try:
        marshal.dumps(value)
        return proxy.setGlobalVariable(userName, var, value)
    except:
        global_vars[var] = value
        return True

#

def py_exec(code_string):
    """
    Exposed Python function and class instances for TCL.
    """
    global global_vars

    if not isinstance(code_string, str):
        print('py_exec: Error, the code must be a string `{}`!'.format(code_string))
        return False

    try: ret = eval(code_string, global_vars, global_vars)
    except Exception, e:
        print('py_exec: Error execution code `{}`! Exception `{}`!'.format(code_string, e))
        ret = False

    return ret

#

if __name__=='__main__':

    userName   = sys.argv[1:2]
    globEpName = sys.argv[2:3]

    if not userName:
        print('TC error: TestCaseRunner must be started with username argument! Exiting!')
        exit(1)
    else:
        userName = userName[0]
    if not globEpName:
        print('TC error: TestCaseRunner must be started with EpName argument! Exiting!')
        exit(1)
    else:
        globEpName = globEpName[0]
        print('TC debug: TestCaseRunner started with  User: {0} ;  EP: {1}.'.format(userName, globEpName))

    # Inject libraries path for the current EP
    sys.path.append(TWISTER_PATH + '/.twister_cache/' + globEpName)

    CONFIG = loadConfig()

    tc_tcl = None; tc_perl = None; tc_python = None
    proxy = None
    tSuites = None
    suite_number = 0
    abort_suite  = False

    suite_id = False
    tStats = False
    tList  = False

    # For storing temporary variables
    global_vars = {}

    CE_Path = CONFIG['PROXY']

    if CONFIG['STATUS'] == 'running':
        print('TC debug: Connected to proxy, running tests!')
    else:
        print('TC debug: EpName {0} is NOT running! Exiting!'.format(globEpName))
        exit(1)

    # Connect to RPC server
    try:
        proxy = xmlrpclib.ServerProxy(CONFIG['PROXY'])
        tSuites = proxy.listSuites(userName, globEpName).split(',')
    except:
        print('TC debug: Cannot connect to CE path `{0}`! Exiting!'.format(CONFIG['PROXY']))
        exit(1)

    # Save all libraries from CE
    saveLibraries(proxy)

    try: import ce_libs
    except ImportError:
        print('TC ImportError: TestCaseRunner cannot import the shared libraries!')
        exit(1)
    except Exception, e:
        print('TC LibrariesError: TestCaseRunner cannot import the shared libraries, exception `{}`!'.format(e))
        exit(1)

    # Get the `exit on test Fail` value
    exit_on_test_fail = proxy.getUserVariable(userName, 'exit_on_test_fail')

    def Rindex(l, val):
        ''' Find element in list from the end '''
        for i, j in enumerate(reversed(l)):
            if j == val: return len(l) - i - 1
        return -1

# # #

    while 1:

        # = = =  CYCLE  IN  SUITES = = =
        # This cycle will run forever,
        # To complete all test files.

        try:
            suite_str  = tSuites[suite_number]
            suite_id   = suite_str.split(':')[0]
            suite_name = suite_str.split(':')[1]
        except: break

        print('\n===== ===== ===== ===== =====')
        print('  Starting suite `%s`' % suite_str)
        print('===== ===== ===== ===== =====\n')

        # Set suite = current suite
        proxy.setEpVariable(userName, globEpName, 'current_suite', suite_id)

        # Default - file stats for current Suite
        tStats = proxy.getFileStatusAll(userName, globEpName, suite_id).split(',')
        # Default - file list for current Suite
        tList  = proxy.getSuiteFiles(userName, globEpName, suite_id)

        if not tList:
            print('TC warning: Nothing to do in suite `%s`!\n' % suite_str)
            suite_number += 1
            continue

        # The Test Bed name
        tbname = proxy.getSuiteVariable(userName, globEpName, suite_id, 'tb')

        # Get list of libraries for current suite
        libList = proxy.getSuiteVariable(userName, globEpName, suite_id, 'libraries')
        if libList:
            saveLibraries(proxy, libList)
            print('')


        # Cycle for Files
        iIndex = 0

        while 1:

            # File ID
            file_id = tList[iIndex]
            # File status
            status = tStats[iIndex]
            # The name of the file, based on the ID
            filename = proxy.getFileVariable(userName, file_id, 'file')
            # Is this file Prerequisite?
            prerequisite = proxy.getFileVariable(userName, file_id, 'Prerequisite')
            # Test-case dependency, if any
            dependancy = proxy.getFileVariable(userName, file_id, 'dependancy')
            # Is this test file optional?
            optional_test = proxy.getFileVariable(userName, file_id, 'Optional')
            # Get testcase delay
            tc_delay = proxy.getUserVariable(userName, 'tc_delay')
            # Get args
            args = proxy.getFileVariable(userName, file_id, 'param')
            if args:
                args = [p for p in args.split(',') if p]
            else:
                args = []

            # print('<<< START filename: `%s:%s` >>>\n\nDebug: dependancy = `%s`, prereq = `%s`, optional = `%s` ...\n' %
            #      (file_id, filename, dependancy, prerequisite, optional_test))

            # Reset abort suite variable for every first file in the suite
            if iIndex == 0:
                abort_suite = False

            # If this suite is aborted because of the prerequisite file, send status ABORT
            if abort_suite:
                print('TC info: Abort file `{0}` because of prerequisite file!\n'.format(filename))
                proxySetTestStatus(file_id, STATUS_ABORTED, 0.0) # File status ABORTED
                print('<<< END filename: `%s:%s` >>>\n' % (file_id, filename))
                iIndex = nextFile(iIndex)
                if not iIndex: break
                continue

            # Reset the TIMEOUT status for the next execution!
            if status == '7':
                proxySetTestStatus(file_id, STATUS_INVALID, 0.0) # Status INVALID

            # # If there was a TIMEOUT last time, must continue with the next file after timeout
            # # First file in the suite is always executed
            # if '7' in tStats and iIndex != 0 and iIndex <= Rindex(tStats, '7'):
            #     print('TC info: Skipping file {0}: `{1}` with status {2}, aborted because of timeout!\n'.format(
            #         iIndex, filename, status))
            #     if iIndex == 0 and prerequisite:
            #         abort_suite = True
            #         print('TC error: Prerequisite file for suite `%s` returned FAIL! All suite will be ABORTED!' % suite_name)
            #     print('<<< END filename: `%s:%s` >>>\n' % (file_id, filename))
            #     continue

            # Reload config file written by EP
            CONFIG = loadConfig()

            if CONFIG['STATUS'] == 'stopped':
                # When a test file is about to be executed and STOP is received, send status ABORTED
                Suicide('ABORTED: Status STOP, while running!', file_id, 5, 0.0)

            elif CONFIG['STATUS'] == 'paused': # On pause, freeze cycle and wait for Resume or Stop
                proxy.echo(':: {0} is paused!... Must RESUME to continue, or STOP to exit test suite...'.format(globEpName))
                vPauseMsg = False
                while 1:
                    # Print pause message
                    if not vPauseMsg:
                        print('Runner: Execution paused. Waiting for RESUME signal.\n')
                        vPauseMsg = True
                    time.sleep(3)
                    # Reload config file written by EP
                    CONFIG = loadConfig()
                    # On resume, stop waiting
                    if CONFIG['STATUS'] == 'running' or CONFIG['STATUS'] == 'resume':
                        proxy.echo(':: {0} is no longer paused !'.format(globEpName))
                        break
                    # On stop...
                    elif CONFIG['STATUS'] == 'stopped':
                        # When a test is waiting for resume, but receives STOP, send status NOT EXECUTED
                        Suicide('NOT EXECUTED: Status STOP, while waiting for resume!', file_id, 6, 0.0)

            # If dependency file is PENDING or WORKING, wait to finish, for any other status, go next.
            if dependancy and  proxy.getFileVariable(userName, dependancy, 'status')  in [-1, False, STATUS_PENDING, STATUS_WORKING]:
                dependancy_suite = proxy.getFileVariable(userName, dependancy, 'suite')
                dependancy_file = proxy.getFileVariable(userName, dependancy, 'file')

                if dependancy_file:
                    proxy.echo(':: {0} is waiting for file `{1}::{2}` to finish execution...'.format(globEpName, dependancy_suite, dependancy_file))
                    proxySetTestStatus(userName, file_id, STATUS_WAITING, 0.0) # Status WAITING

                    while 1:
                        time.sleep(3)
                        # Reload info about dependency file
                        if  proxy.getFileVariable(userName, dependancy, 'status')  not in [-1, False, STATUS_PENDING, STATUS_WORKING]:
                            proxy.echo(':: {0} is not longer waiting !'.format(globEpName))
                            break

            str_to_execute = proxy.getTestFile(userName, globEpName, file_id)
            # If CE sent False, it means the file is empty, does not exist, or it's not runnable.
            if str_to_execute == '':
                print('TC error: File path `{0}` does not exist!\n'.format(filename))
                if iIndex == 0 and prerequisite:
                    abort_suite = True
                    print('TC error: Prerequisite file for suite `%s` returned FAIL! All suite will be ABORTED!' % suite_name)
                proxySetTestStatus(file_id, STATUS_SKIPPED, 0.0) # Status SKIPPED
                print('<<< END filename: `%s:%s` >>>\n' % (file_id, filename))
                iIndex = nextFile(iIndex)
                if not iIndex: break
                continue

            elif not str_to_execute:
                print('TC info: File `{0}` will be skipped.\n'.format(filename))
                # Skipped prerequisite are ok.
                proxySetTestStatus(file_id, STATUS_SKIPPED, 0.0) # Status SKIPPED
                print('<<< END filename: `%s:%s` >>>\n' % (file_id, filename))
                iIndex = nextFile(iIndex)
                if not iIndex: break
                continue

            file_ext = os.path.splitext(filename)[1].lower()

            # --------------------------------------------------
            # Start TIMER
            interval = 5 # The interval should be in Test-Suites.XML.
            timr = Timer(interval, lambda: Suicide(26, 'ABORTED execution: Timer expired!\n', file_id, 7, interval)) # Send status TIMEOUT
            #timr.start()
            # --------------------------------------------------

            # If file type is TCL
            if file_ext in ['.tcl']:
                if not tc_tcl:
                    tc_tcl = TCRunTcl()
                current_runner = tc_tcl

            # If file type is PERL
            elif file_ext in ['.plx']:
                if not tc_perl:
                    tc_perl = TCRunPerl()
                current_runner = tc_perl

            # If file type is PYTHON
            elif file_ext in ['.py', '.pyc', '.pyo']:
                if not tc_python:
                    tc_python = TCRunPython()
                current_runner = tc_python

            # Unknown file type
            else:
                print('TC warning: Extension type `%s` is unknown and will be ignored!' % file_ext)
                if iIndex == 0 and prerequisite:
                    abort_suite = True
                    print('TC error: Prerequisite file for suite `%s` returned FAIL! All suite will be ABORTED!' % suite_name)
                proxySetTestStatus(file_id, STATUS_NOT_EXEC, 0.0) # Status NOT_EXEC
                print('<<< END filename: `%s:%s` >>>\n' % (file_id, filename))
                iIndex = nextFile(iIndex)
                if not iIndex: break
                continue

            # If there is a delay between tests, wait here
            if tc_delay:
                print('TC debug: Waiting %i seconds before starting the test...\n' % tc_delay)
                time.sleep(tc_delay)

            # Start counting time
            timer_i = time.time()
            result = None

            proxySetTestStatus(file_id, STATUS_WORKING, 0.0) # Status WORKING

            # --------------------------------------------------
            # RUN CURRENT TEST!
            try:
                globs = globals()
                globs['tbname'] = tbname
                result = current_runner._eval(str_to_execute, globs, args)
                result = str(result).upper()
                print('\n>>> File `%s` returned `%s`. <<<\n' % (filename, result))

            except Exception, e:
                # On error, print the error message, but don't exit
                print('\nException:')
                print(traceback.format_exc())
                print('\n>>> File `%s` execution `FAILED`. <<<\n' % filename)

                proxy.echo('TC error: Error executing file `%s`!' % filename)

                proxySetTestStatus(file_id, STATUS_FAIL, (time.time() - timer_i))
                # When crash detected = True
                proxy.setFileVariable(userName, globEpName, suite_id, file_id, 'twister_tc_crash_detected', 1)
                print('<<< END filename: `%s:%s` >>>\n' % (file_id, filename))
                iIndex = nextFile(iIndex)
                if not iIndex: break
                continue

            # END OF TEST!
            timer_f = time.time() - timer_i
            # --------------------------------------------------

            if result==STATUS_PASS or result == 'PASS':
                proxySetTestStatus(file_id, STATUS_PASS, timer_f) # File status PASS
            elif result==STATUS_SKIPPED or result in ['SKIP', 'SKIPPED']:
                proxySetTestStatus(file_id, STATUS_SKIPPED, timer_f) # File status SKIPPED
            elif result==STATUS_ABORTED or result in ['ABORT', 'ABORTED']:
                proxySetTestStatus(file_id, STATUS_ABORTED, timer_f) # File status ABORTED
            elif result==STATUS_NOT_EXEC or result in ['NOT-EXEC', 'NOT EXEC', 'NOT EXECUTED']:
                proxySetTestStatus(file_id, STATUS_NOT_EXEC, timer_f) # File status NOT_EXEC
            elif result==STATUS_TIMEOUT or result == 'TIMEOUT':
                proxySetTestStatus(file_id, STATUS_TIMEOUT, timer_f) # File status TIMEOUT
            elif result==STATUS_INVALID or result == 'INVALID':
                proxySetTestStatus(file_id, STATUS_INVALID, timer_f) # File status INVALID
            else:
                proxySetTestStatus(file_id, STATUS_FAIL, timer_f) # File status FAIL

                # If status is FAIL, and the file is not Optional and Exit on test fail is ON, CLOSE the runner
                if not optional_test and exit_on_test_fail:
                    print('TC error: Mandatory file `{0}` returned FAIL! Closing the runner!'.format(filename))
                    proxy.echo('TC error: Mandatory file `{0}::{1}::{2}` returned FAIL! Closing the runner!'\
                        ''.format(globEpName, suite_name, filename))
                    print('<<< END filename: `%s:%s` >>>\n' % (file_id, filename))
                    exit(1)

                # If status is FAIL, and the file is prerequisite, CANCEL all suite
                if iIndex == 0 and prerequisite:
                    abort_suite = True
                    print('TC error: Prerequisite file for suite `%s` returned FAIL! All suite will be ABORTED!' % suite_name)
                    proxy.echo('TC error: Prerequisite file for `{0}::{1}` returned FAIL! All suite will be ABORTED!'\
                        ''.format(globEpName, suite_name))

            print('<<< END filename: `%s:%s` >>>\n' % (file_id, filename))

            sys.stdout.flush() # Flush just in case

            # --------------------------------------------------
            # Cancel TIMER !
            timr.cancel() ; del timr
            del timer_i, timer_f
            del current_runner
            # --------------------------------------------------

            # Jump to next file, if it's the last file, break
            iIndex = nextFile(iIndex)
            if not iIndex: break


        suite_number += 1 # Next suite...

        # # #  END  SUITES CYCLE   # # #

    print('\n===== ===== ===== =====')
    print('. . . All tests done . . .')
    print('===== ===== ===== =====\n')

    # Manually clean pointers
    del tc_tcl, tc_perl, tc_python

#
