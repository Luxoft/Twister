
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

    global globEpId
    global TWISTER_PATH
    EP_CACHE = TWISTER_PATH + '/.twister_cache/' + globEpId

    if not os.path.exists(EP_CACHE):
        print('TC error: Execution Process must be started first! Exiting!')
        exit(1)

    cache_file = EP_CACHE + '/data.pkl'

    if 0: # PIPE ?
        try:
            f = os.open(cache_file, os.O_RDONLY)
            data = os.read(f, 1024)
            CONFIG = pickle.loads(data)
            os.close(f) ; del f
            return CONFIG
        except:
            print('TC error: cannot read config file `%s`! Exiting!' % cache_file)
            exit(1)

    else:
        try:
            f = open(cache_file, 'rb')
            data = f.read()
            CONFIG = pickle.loads(data)
            f.close() ; del f
            return CONFIG
        except:
            print('TC error: cannot read config file `%s`! Exiting!' % cache_file)
            exit(1)

#

def Suicide(sig=None, msg=None, filename=None, status_f=None, timer_f=None):
    '''
    Function Suicide is used to kill current process.
    '''
    if msg:
        proxy.echo(':: {0} {1}...'.format(globEpId, msg.strip()))
    if (filename is not None) and (status_f is not None) and (timer_f is not None):
        proxySetTestStatus(globEpId, filename, status_f, timer_f)
    pid = os.getpid()
    print('TC debug: Killing PID `{0}`.'.format(pid))
    # Kill PID
    if sig and type(sig)==type(0):
        os.kill(pid, sig)
    else:
        os.kill(pid, 9)

#

def proxySetTestStatus(epid, filename, status, time_t):
    '''
    STATUS_PENDING  : 10 : Not yet run, waiting to start
    STATUS_WORKING  : 1  : Is running now
    STATUS_PASS     : 2  : Test is finished successful
    STATUS_FAIL     : 3  : Test failed
    STATUS_SKIPPED  : 4  : When file doesn't exist, or test has flag `runnable = False`
    STATUS_ABORTED  : 5  : When test is stopped while running
    STATUS_NOT_EXEC : 6  : Not executed, is sent from TC when tests are paused, and then stopped instead of being resumed
    STATUS_TIMEOUT  : 7  : When timer expired
    STATUS_INVALID  : 8  : When timer expired, the next run
    STATUS_WAITING  : 9  : Is waiting for another test
    '''
    #
    global proxy
    if proxy is not None:
        proxy.setTestStatus(epid, filename, status, time_t)
    else:
        print('Offline mode: Filename `{0}`, status [ {1} ], time [ {2} ]'.format(filename, status, time_t))
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

    for filename in files:

        # Timer for current cycle, must be after checking CE/ EP Status
        timer_i = time.time()
        # Reset result
        result = None

        file_ext = os.path.splitext(filename)[1].lower()

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
            print('TC warning: File `{0}` is an unknown type of file and will be ignored!'.format(filename))
            continue

        str_to_execute = fnamex()
        str_to_execute.data = open(filename, 'r').read()

        # --------------------------------------------------
        # RUN CURRENT TEST!
        try:
            result = current_runner._eval(str_to_execute)
            print('\n>>> File `%s` returned `%s`. <<<\n' % (filename, result))

        except Exception, e:
            print('TC error: Error executing file `%s`!' % filename)
            print('Exception: `%s` !\n' % e)
            continue

        # END OF TESTS!
        timer_f = time.time() - timer_i
        # --------------------------------------------------

        if result==STATUS_PASS or result in ['pass', 'PASS']:
            proxySetTestStatus(globEpId, filename, STATUS_PASS, timer_f) # File status PASS
        elif result==STATUS_SKIPPED or result in ['skip', 'skipped', 'SKIP', 'SKIPPED']:
            proxySetTestStatus(globEpId, filename, STATUS_SKIPPED, timer_f) # File status SKIPPED
        elif result==STATUS_ABORTED or result in ['abort', 'aborted', 'ABORT', 'ABORTED']:
            proxySetTestStatus(globEpId, filename, STATUS_ABORTED, timer_f) # File status ABORTED
        elif result==STATUS_NOT_EXEC or result in ['not-exec', 'not exec', 'NOT-EXEC', 'NOT EXEC']:
            proxySetTestStatus(globEpId, filename, STATUS_NOT_EXEC, timer_f) # File status NOT_EXEC
        elif result==STATUS_TIMEOUT or result in ['timeout', 'TIMEOUT']:
            proxySetTestStatus(globEpId, filename, STATUS_TIMEOUT, timer_f) # File status TIMEOUT
        elif result==STATUS_INVALID or result in ['invalid', 'INVALID']:
            proxySetTestStatus(globEpId, filename, STATUS_INVALID, timer_f) # File status INVALID
        else:
            proxySetTestStatus(globEpId, filename, STATUS_FAIL, timer_f) # File status FAIL

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

    globEpId = sys.argv[1:2]

    if not globEpId:
        print('TC error: TestCaseRunner must be started with EpId argument! Exiting!')
        exit(1)
    else:
        globEpId = globEpId[0]
        print('TC debug: TestCaseRunner started with Id: {0}.'.format(globEpId))

    tc_tcl = None; tc_perl = None; tc_python = None
    proxy = None

    if globEpId == 'OFFLINE':
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

    if CONFIG['STATUS'] == 'running':
        print('TC debug: Connected to proxy, running tests!')
    else:
        print('TC debug: EpId {0} is NOT running! Exiting!'.format(globEpId))
        exit(1)

    # Connect to RPC server
    try:
        proxy = xmlrpclib.ServerProxy(CONFIG['PROXY'])
        tStats = proxy.getTestStatusAll(globEpId).split(',')
    except:
        print('TC debug: Cannot to CE path `{0}`! Exiting!'.format(CONFIG['PROXY']))
        exit(1)

    if '7' in tStats:
        print('TC debug: Resuming after timeout...')
        # Get Test Suites List for this EP, DON'T reset statuses when asking for files
        tList = proxy.getTestSuiteFileList(globEpId, False)
    else:
        # Get list of files and reset stats
        tList = proxy.getTestSuiteFileList(globEpId)

    if not tList:
        print('TC warning: Nothing to do! Exiting!')
        proxy.setExecStatus(globEpId, STATUS_STOP) # EP status STOP
        exit(0)

    # If last file from last run is with TIMEOUT, set status STOP and exit
    if tStats[-1] == str(STATUS_TIMEOUT):
        print('TC debug: Dry run after timeout.')
        proxySetTestStatus(globEpId, tList[-1], STATUS_INVALID, 0.0) # File status INVALID
        proxy.setExecStatus(globEpId, STATUS_STOP) # EP status STOP
        exit(0)

    if len(tStats) != len(tList):
        print('TC error: Well, this is embarrassing... the len of statuses is differend from the len of files! Exiting!')
        print('Stats: {0} ; Files: {1}\n'.format(tStats, tList))
        exit(1)
    else:
        print('TC debug: Stats from last run : {0}'.format(tStats))

    def Rindex(l, val):
        ''' Find element in list from the end '''
        for i, j in enumerate(reversed(l)):
            if j == val: return len(l) - i - 1
        return -1


    print('\n===== ===== ===== ===== =====')
    print('TC debug: Starting test suite...')
    print('===== ===== ===== ===== =====\n')

    for iIndex in range(len(tList)):

        filename = tList[iIndex]
        status = tStats[iIndex]

        # Reset the TIMEOUT status for the next execution!
        if status == '7':
            proxySetTestStatus(globEpId, filename, STATUS_INVALID, 0.0) # Status INVALID

        # If there was a TIMEOUT last time, must continue with the next file after timeout
        # First file in the suite is always executed
        if '7' in tStats and iIndex != 0 and iIndex <= Rindex(tStats, '7'):
            print('TC debug: Skipping file {0}: `{1}` with status {2}, aborted because of timeout!'.format(
                iIndex, filename, status))
            continue

        # Reload config file written by EP
        CONFIG = loadConfig()
        # Get dependency file, if any
        DEP_FILE = proxy.getTestCaseDependency(globEpId, filename)

        if CONFIG['STATUS'] == 'stopped':
            # When a test file is about to be executed and STOP is received, send status ABORTED
            Suicide('ABORTED: Status STOP, while running!', filename, 5, 0.0)

        elif CONFIG['STATUS'] == 'paused': # On pause, freeze cycle and wait for Resume or Stop
            proxy.echo(':: {0} is paused!... Must RESUME to continue, or STOP to exit test suite...'.format(globEpId))
            vPauseMsg = False
            while 1:
                # Print pause message
                if not vPauseMsg:
                    print('Runner: Execution paused. Waiting for RESUME signal.\n')
                    vPauseMsg = True
                time.sleep(0.5)
                # Reload config file written by EP
                CONFIG = loadConfig()
                # On resume, stop waiting
                if CONFIG['STATUS'] == 'running' or CONFIG['STATUS'] == 'resume':
                    proxy.echo(':: {0} is no longer paused !'.format(globEpId))
                    break
                # On stop...
                elif CONFIG['STATUS'] == 'stopped':
                    # When a test is waiting for resume, but receives STOP, send status NOT EXECUTED
                    Suicide('NOT EXECUTED: Status STOP, while waiting for resume!', filename, 6, 0.0)

        # If dependency file is PENDING or WORKING, wait to finish, for any other status, go next.
        if DEP_FILE and proxy.getTestStatus(DEP_FILE['epid'], DEP_FILE['file']) in ['pending', 'working']:
            proxy.echo(':: {0} is waiting for {1}::{2} to finish execution...'.format(globEpId, DEP_FILE['epid'], DEP_FILE['file']))
            proxySetTestStatus(globEpId, filename, STATUS_WAITING, 0.0) # Status WAITING
            while 1:
                time.sleep(1)
                # Reload info about dependency file
                if proxy.getTestStatus(DEP_FILE['epid'], DEP_FILE['file']) not in ['pending', 'working']:
                    proxy.echo(':: {0} is not longer waiting !'.format(globEpId))
                    break

        # Timer for current cycle, must be after checking CE/ EP Status
        timer_i = time.time()

        str_to_execute = proxy.getTestCaseFile(globEpId, filename)
        # If CE sent False, it means the file is empty, does not exist, or it's not runnable.
        if not str_to_execute:
            print('TC debug: File `{0}` will be skipped.'.format(filename))
            proxySetTestStatus(globEpId, filename, STATUS_SKIPPED, 0.0) # Status SKIPPED
            continue

        file_ext = os.path.splitext(filename)[1].lower()

        # --------------------------------------------------
        # Start TIMER !
        interval = 5 # The interval should be in MASTER XML.
        timr = Timer(interval, lambda: Suicide(26, 'ABORTED execution: Timer expired!\n', filename, 7, interval)) # Send status TIMEOUT
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
            continue

        result = None
        proxySetTestStatus(globEpId, filename, STATUS_WORKING, 0.0) # Status WORKING

        # --------------------------------------------------
        # RUN CURRENT TEST!
        try:
            result = current_runner._eval(str_to_execute)
            print('\n>>> File `%s` returned `%s`. <<<\n' % (filename, result))

        except Exception, e:
            # On error, print the error message, but don't exit
            print('\nException:')
            print(traceback.format_exc())
            print('\n>>> File `%s` returned `FAIL`. <<<\n' % filename)

            proxy.echo('TC error: Error executing file `%s`!' % filename)
            proxySetTestStatus(globEpId, filename, STATUS_FAIL, 0.0) # File status FAIL
            proxy.setFileInfo(globEpId, filename, 'twister_tc_crash_detected', 1) # Crash detected True
            #proxy.setExecStatus(globEpId, STATUS_STOP, 'Kill sent by the Runner, because of `%s` file error!' % filename)

        # END OF TESTS!
        timer_f = time.time() - timer_i
        # --------------------------------------------------

        if result==STATUS_PASS or result in ['pass', 'PASS']:
            proxySetTestStatus(globEpId, filename, STATUS_PASS, timer_f) # File status PASS
        elif result==STATUS_SKIPPED or result in ['skip', 'skipped', 'SKIP', 'SKIPPED']:
            proxySetTestStatus(globEpId, filename, STATUS_SKIPPED, timer_f) # File status SKIPPED
        elif result==STATUS_ABORTED or result in ['abort', 'aborted', 'ABORT', 'ABORTED']:
            proxySetTestStatus(globEpId, filename, STATUS_ABORTED, timer_f) # File status ABORTED
        elif result==STATUS_NOT_EXEC or result in ['not-exec', 'not exec', 'NOT-EXEC', 'NOT EXEC']:
            proxySetTestStatus(globEpId, filename, STATUS_NOT_EXEC, timer_f) # File status NOT_EXEC
        elif result==STATUS_TIMEOUT or result in ['timeout', 'TIMEOUT']:
            proxySetTestStatus(globEpId, filename, STATUS_TIMEOUT, timer_f) # File status TIMEOUT
        elif result==STATUS_INVALID or result in ['invalid', 'INVALID']:
            proxySetTestStatus(globEpId, filename, STATUS_INVALID, timer_f) # File status INVALID
        else:
            proxySetTestStatus(globEpId, filename, STATUS_FAIL, timer_f) # File status FAIL

        sys.stdout.flush() # Just in case

        # --------------------------------------------------
        # Cancel TIMER !
        timr.cancel() ; del timr
        del timer_i, timer_f
        del current_runner
        # --------------------------------------------------

    print('\n===== ===== ===== =====')
    print('TC debug: All tests done!')
    print('===== ===== ===== =====\n')

    # If success, manually clean pointers
    del tc_tcl, tc_perl, tc_python

#
