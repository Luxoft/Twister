
# File: TestCaseRunner.py ; This file is part of Twister.

# Copyright (C) 2012 , Luxoft

# Authors:
#    Andrei Costachi <acostachi@luxoft.com>
#    Andrei Toma <atoma@luxoft.com>
#    Cristian Constantin <crconstantin@luxoft.com>
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
 - Connects to CE to receive the files that must be executed on this station.
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
This script should NOT be run manually.
'''

import os
import sys
import time
import csv
import pickle
import xmlrpclib
import traceback
from threading import Timer

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print('TWISTER_PATH environment variable is not set! Exiting!')
    exit(1)
sys.path.append(TWISTER_PATH)

from common.constants import *
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
        print('TC error: cannot read config file `%s`! Exiting!' % cache_file)
        exit(1)

#

def saveLibraries(proxy):
    '''
    Saves all libraries from CE.
    Not used in offline mode.
    '''
    global TWISTER_PATH
    libs_list = proxy.getLibrariesList()
    libs_path = TWISTER_PATH + '/.twister_cache/ce_libs/'

    try: os.makedirs(libs_path)
    except: pass

    __init = open(libs_path + '/__init__.py', 'w')
    __init.write('\nimport os\n')
    __init.write('\nPROXY = "%s"\n' % CE_Path)
    all_libs = [os.path.splitext(lib)[0] for lib in libs_list if not lib.endswith('.zip')]
    __init.write('\nall = ["%s"]\n\n' % ('", "'.join(all_libs)))

    for lib_file in libs_list:
        # Write in __init__ file.
        ext = os.path.splitext(lib_file)
        if ext[1] == '.zip':
            __init.write('sys.path.append(os.path.split(__file__)[0] + "/%s")\n\n' % lib_file)
        else:
            __init.write('import %s\n' % ext[0])
            __init.write('from %s import *\n\n' % ext[0])

        lib_pth = libs_path + os.sep + lib_file
        print('Downloading library `{0}` ...'.format(lib_pth))
        f = open(lib_pth, 'wb')
        lib_data = proxy.getLibraryFile(lib_file)
        f.write(lib_data.data)
        f.close() ; del f

    __init.close()

#

def Suicide(sig=None, msg=None, file_id=None, status_f=None, timer_f=None):
    '''
    Function Suicide is used to kill current process.
    '''
    if msg:
        proxy.echo(':: {0} {1}...'.format(globEpName, msg.strip()))
    if (file_id is not None) and (status_f is not None) and (timer_f is not None):
        proxySetTestStatus(globEpName, file_id, status_f, timer_f)
    pid = os.getpid()
    print('TC debug: Killing PID `{0}`.'.format(pid))
    # Kill PID
    if sig and type(sig)==type(0):
        os.kill(pid, sig)
    else:
        os.kill(pid, 9)

#

def proxySetTestStatus(epid, file_id, status, time_t):
    #
    global proxy
    if proxy is not None:
        proxy.setFileStatus(epid, file_id, status, time_t)
    else:
        print('Offline mode: file_id `{0}`, status [ {1} ], time [ {2} ]'.format(file_id, status, time_t))
    #

#

def runOffline(filelist):
    '''
    This function is used to run the tests files WITHOUT connecting to CE.
    '''
    #
    tc_tcl = None; tc_perl = None; tc_python = None
    class fnamex: pass # Dummy class
    files = []

    for fname in csv.reader(open(filelist, 'rb')):
        if not fname: continue
        if not os.path.isfile(fname[0]):
            print('EP error: Test file `{0}` doesn\'t exist and won\'t be executed!'.format(fname[0]))
            continue
        else:
            files.append(fname[0])

    print('\n===== ===== ===== ===== =====')
    print('TC OFFLINE: Starting test suite...')
    print('===== ===== ===== ===== =====\n')

    for file_name in files:

        # Timer for current cycle, must be after checking CE/ EP Status
        timer_i = time.time()
        # Reset result
        result = None

        file_ext = os.path.splitext(file_name)[1].lower()

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
            print('TC warning: File `{0}` is an unknown type of file and will be ignored!'.format(file_name))
            continue

        str_to_execute = fnamex()
        str_to_execute.data = open(file_name, 'r').read()

        # --------------------------------------------------
        # RUN CURRENT TEST!
        try:
            result = current_runner._eval(str_to_execute)
            print('\n>>> File `%s` returned `%s`. <<<\n' % (file_name, result))

        except Exception, e:
            print('TC error: Error executing file `%s`!' % file_name)
            print('Exception: `%s` !\n' % e)
            continue

        # END OF TESTS!
        timer_f = time.time() - timer_i
        # --------------------------------------------------

        if result==STATUS_PASS or result in ['pass', 'PASS']:
            proxySetTestStatus(globEpName, file_name, STATUS_PASS, timer_f) # File status PASS
        elif result==STATUS_SKIPPED or result in ['skip', 'skipped', 'SKIP', 'SKIPPED']:
            proxySetTestStatus(globEpName, file_name, STATUS_SKIPPED, timer_f) # File status SKIPPED
        elif result==STATUS_ABORTED or result in ['abort', 'aborted', 'ABORT', 'ABORTED']:
            proxySetTestStatus(globEpName, file_name, STATUS_ABORTED, timer_f) # File status ABORTED
        elif result==STATUS_NOT_EXEC or result in ['not-exec', 'not exec', 'NOT-EXEC', 'NOT EXEC']:
            proxySetTestStatus(globEpName, file_name, STATUS_NOT_EXEC, timer_f) # File status NOT_EXEC
        elif result==STATUS_TIMEOUT or result in ['timeout', 'TIMEOUT']:
            proxySetTestStatus(globEpName, file_name, STATUS_TIMEOUT, timer_f) # File status TIMEOUT
        elif result==STATUS_INVALID or result in ['invalid', 'INVALID']:
            proxySetTestStatus(globEpName, file_name, STATUS_INVALID, timer_f) # File status INVALID
        else:
            proxySetTestStatus(globEpName, file_name, STATUS_FAIL, timer_f) # File status FAIL

        sys.stdout.flush() # Just in case

        # --------------------------------------------------
        del timer_i, timer_f
        del current_runner
        # --------------------------------------------------

    print('\n===== ===== ===== =====')
    print('TC OFFLINE: All tests done!')
    print('===== ===== ===== =====\n')

    # If success, manually clean pointers
    del tc_tcl, tc_perl, tc_python
    #

#

if __name__=='__main__':

    globEpName = sys.argv[1:2]

    if not globEpName:
        print('TC error: TestCaseRunner must be started with EpId argument! Exiting!')
        exit(1)
    else:
        globEpName = globEpName[0]
        print('TC debug: TestCaseRunner started with Id: {0}.'.format(globEpName))

    if globEpName == 'OFFLINE':
        filelist = sys.argv[2:3]
        if not filelist:
            print('TC error: Must start the Runner with 2 parameters, EpId and Filelist! Exiting!')
            exit(1)
        if not os.path.exists(filelist[0]):
            print('TC error: File list file `{0}` does not exist! Exiting!')
            exit(1)
        runOffline(filelist[0])
        exit(0) # Exit code 0 ??

    CONFIG = loadConfig()

    tc_tcl = None; tc_perl = None; tc_python = None
    proxy = None
    suite_number = 0
    abort_suite = False

    CE_Path = CONFIG['PROXY']

    if CONFIG['STATUS'] == 'running':
        print('TC debug: Connected to proxy, running tests!')
    else:
        print('TC debug: EpId {0} is NOT running! Exiting!'.format(globEpName))
        exit(1)

    # Connect to RPC server
    try:
        proxy = xmlrpclib.ServerProxy(CONFIG['PROXY'])
        tSuites = proxy.listSuites(globEpName).split(',')
    except:
        print('TC debug: Cannot to CE path `{0}`! Exiting!'.format(CONFIG['PROXY']))
        exit(1)

    # If not offline, save all libraries from CE
    if globEpName != 'OFFLINE':
        saveLibraries(proxy)

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

        try: suite = tSuites[suite_number]
        except: break

        print('\n===== ===== ===== ===== =====')
        print('   Starting suite `%s`' % suite)
        print('===== ===== ===== ===== =====\n')


        # File stats for current Suite
        tStats = proxy.getFileStatusAll(globEpName, suite).split(',')
        # File list for current Suite
        tList = proxy.getSuiteFiles(globEpName, suite)

        if not tList:
            print('TC warning: Nothing to do in suite `%s`!\n' % suite)
            suite_number += 1
            continue

        # If last file from last run is with TIMEOUT, fix file status and exit Suite
        if tStats[-1] == str(STATUS_TIMEOUT):
            print('TC debug: Dry run after timeout...')
            proxySetTestStatus(globEpName, tList[-1], STATUS_INVALID, 0.0) # File status INVALID
            suite_number += 1
            continue

        if len(tStats) != len(tList):
            print('TC error: The len of statuses is different from the len of files! Abort suite!')
            print('Stats: {0} ; Files: {1}\n'.format(tStats, tList))
            suite_number += 1
            continue
        else:
            print('TC debug: Stats from last run : {0}'.format(tStats))


        for iIndex in range(len(tList)):

            file_id = tList[iIndex]
            status = tStats[iIndex]

            # The name of the file
            filename = proxy.getFileVariable(file_id, 'file')
            # Is this file Prerequisite?
            prerequisite = proxy.getFileVariable(file_id, 'Prerequisite')
            # Test-case dependency, if any
            dependancy = proxy.getFileVariable(file_id, 'dependancy')
            # Get args
            args = proxy.getFileVariable(file_id, 'param')
            if args:
                args = [p for p in args.split(',') if p]
            else:
                args = []

            print('Starting to RUN filename: `%s`, dependancy = `%s`, is prerequisite = `%s` ...\n' % (filename, dependancy, prerequisite))

            # Reset abort suite variable for every first file in the suite
            if iIndex == 0:
                abort_suite = False

            # If this suite is aborted because of the prerequisite file, send status ABORT
            if abort_suite:
                print('TC debug: Abort file `{0}` because of prerequisite file!\n'.format(filename))
                proxySetTestStatus(globEpName, file_id, STATUS_ABORTED, 0.0) # File status ABORTED
                continue

            # Reset the TIMEOUT status for the next execution!
            if status == '7':
                proxySetTestStatus(globEpName, file_id, STATUS_INVALID, 0.0) # Status INVALID

            # If there was a TIMEOUT last time, must continue with the next file after timeout
            # First file in the suite is always executed
            if '7' in tStats and iIndex != 0 and iIndex <= Rindex(tStats, '7'):
                print('TC debug: Skipping file {0}: `{1}` with status {2}, aborted because of timeout!\n'.format(
                    iIndex, filename, status))
                continue

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
            if dependancy and  proxy.getFileVariable(dependancy, 'status')  in [-1, False, STATUS_PENDING, STATUS_WORKING]:
                dependancy_suite = proxy.getFileVariable(dependancy, 'suite')
                dependancy_file = proxy.getFileVariable(dependancy, 'file')

                if dependancy_file:
                    proxy.echo(':: {0} is waiting for file `{1}::{2}` to finish execution...'.format(globEpName, dependancy_suite, dependancy_file))
                    proxySetTestStatus(globEpName, file_id, STATUS_WAITING, 0.0) # Status WAITING

                    while 1:
                        time.sleep(3)
                        # Reload info about dependency file
                        if  proxy.getFileVariable(dependancy, 'status')  not in [-1, False, STATUS_PENDING, STATUS_WORKING]:
                            proxy.echo(':: {0} is not longer waiting !'.format(globEpName))
                            break

            # Timer for current cycle, must be after checking CE/ EP Status
            timer_i = time.time()

            str_to_execute = proxy.getTestFile(globEpName, file_id)
            # If CE sent False, it means the file is empty, does not exist, or it's not runnable.
            if str_to_execute == '':
                print('TC debug: File path `{0}` does not exist!\n'.format(filename))
                proxySetTestStatus(globEpName, file_id, STATUS_SKIPPED, 0.0) # Status SKIPPED
                continue
            elif not str_to_execute:
                print('TC debug: File `{0}` will be skipped.\n'.format(filename))
                proxySetTestStatus(globEpName, file_id, STATUS_SKIPPED, 0.0) # Status SKIPPED
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
                proxySetTestStatus(globEpName, file_id, STATUS_NOT_EXEC, 0.0) # Status NOT_EXEC
                continue

            result = None
            proxySetTestStatus(globEpName, file_id, STATUS_WORKING, 0.0) # Status WORKING

            # --------------------------------------------------
            # RUN CURRENT TEST!
            try:
                result = current_runner._eval(str_to_execute, globals(), args)
                print('\n>>> File `%s` returned `%s`. <<<\n' % (filename, result))

            except Exception, e:
                # On error, print the error message, but don't exit
                print('\nException:')
                print(traceback.format_exc())
                print('\n>>> File `%s` execution `FAILED`. <<<\n' % filename)

                proxy.echo('TC error: Error executing file `%s`!' % filename)

                proxySetTestStatus(globEpName, file_id, STATUS_FAIL, 0.0) # File status FAIL
                proxy.setFileVariable(globEpName, suite, file_id, 'twister_tc_crash_detected', 1) # Crash detected True

            # END OF TEST!
            timer_f = time.time() - timer_i
            # --------------------------------------------------

            if result==STATUS_PASS or result in ['pass', 'PASS']:
                proxySetTestStatus(globEpName, file_id, STATUS_PASS, timer_f) # File status PASS
            elif result==STATUS_SKIPPED or result in ['skip', 'skipped', 'SKIP', 'SKIPPED']:
                proxySetTestStatus(globEpName, file_id, STATUS_SKIPPED, timer_f) # File status SKIPPED
            elif result==STATUS_ABORTED or result in ['abort', 'aborted', 'ABORT', 'ABORTED']:
                proxySetTestStatus(globEpName, file_id, STATUS_ABORTED, timer_f) # File status ABORTED
            elif result==STATUS_NOT_EXEC or result in ['not-exec', 'not exec', 'NOT-EXEC', 'NOT EXEC']:
                proxySetTestStatus(globEpName, file_id, STATUS_NOT_EXEC, timer_f) # File status NOT_EXEC
            elif result==STATUS_TIMEOUT or result in ['timeout', 'TIMEOUT']:
                proxySetTestStatus(globEpName, file_id, STATUS_TIMEOUT, timer_f) # File status TIMEOUT
            elif result==STATUS_INVALID or result in ['invalid', 'INVALID']:
                proxySetTestStatus(globEpName, file_id, STATUS_INVALID, timer_f) # File status INVALID
            else:
                proxySetTestStatus(globEpName, file_id, STATUS_FAIL, timer_f) # File status FAIL

                # If status if FAIL, and the file is prerequisite, CANCEL all suite
                if iIndex == 0 and prerequisite:
                    abort_suite = True
                    print('TC error: Prerequisite file for suite `%s` returned FAIL! All suite will be ABORTED!' % suite)
                    proxy.echo('TC error: Prerequisite file for `{0}::{1}` returned FAIL! All suite will be ABORTED!'.format(globEpName, suite))

            sys.stdout.flush() # Flush just in case

            # --------------------------------------------------
            # Cancel TIMER !
            timr.cancel() ; del timr
            del timer_i, timer_f
            del current_runner
            # --------------------------------------------------

        suite_number += 1 # Next suite...

        # # #  END  SUITES CYCLE   # # #

    print('\n===== ===== ===== =====')
    print('. . . All tests done . . .')
    print('===== ===== ===== =====\n')

    # Manually clean pointers
    del tc_tcl, tc_perl, tc_python

#
