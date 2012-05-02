
import os
import sys
import re
import time
import datetime
import shutil
import xmlrpclib
import MySQLdb

from subprocess import Popen
from zipfile import ZipFile

# -------------------------------------------------------
globEpId = 'EP-1001'
PHOENIX_ROOT = r'C:\Simulations' + os.sep
proxy = xmlrpclib.ServerProxy('http://11.126.32.9:8000/')   # Tsc Server
# -------------------------------------------------------

try:
    print 'Central Engine Status:', proxy.getExecStatus(globEpId)
    print 'You can start the test from user interface!\n'
except: print 'Cannot connect to Central Engine!'

#

def RUN(tList):

    for tcName in tList:

        timer_i = time.time()

        STATUS = proxy.getExecStatus(globEpId)

        if STATUS == 'stopped': # On stop, DIE!
            print 'EP::Windows: STOP! Exiting.\n'
            return

        elif STATUS == 'paused': # On pause, freeze cycle and wait for Resume or Stop
            print('EP::Windows: Paused!... Press RESUME to continue, or STOP to exit test suite...')
            while 1:
                time.sleep(0.5)
                STATUS = proxy.getExecStatus(globEpId)
                # On resume, stop waiting
                if STATUS == 'running' or STATUS == 'resume':
                    break
                # On stop...
                elif STATUS == 'stopped': # DIE!
                    print 'EP::Windows: STOP! Exiting!...\n'
                    return

        print 'EP::Windows: File: %s ...' % tcName
        file_ext = os.path.splitext(tcName)[1].lower()
        outFile = os.path.split(tcName)[1] # Exec file

        # Ignores NON phoenix
        if file_ext != '.tst':
            print 'EP::Windows: ... file ignored.\n'
            proxy.setTestStatus(globEpId, tcName, 4) # Send status SKIPPED
            continue
        else:
            proxy.setTestStatus(globEpId, tcName, 1) # Send status WORKING

        # The file that will be executed
        toExecute = PHOENIX_ROOT + r'TestNetwork\twister' + os.sep + outFile
        # Download the file from the Central Engine
        with open(toExecute, "wb") as handle:
            handle.write(proxy.getTestCaseFile(globEpId, tcName).data)

        proxy.logMessage('logRunning', 'EP::Windows: Downloading file `%s`...\n' % toExecute)

        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        # Must start the logging,
        # then write the TST file to be executed into the config,
        # then start Simulator.exe.
        # Find the latest log and parse it

        # Parse the TST test files
        tst_data = open(PHOENIX_ROOT + r'TestNetwork\twister' +os.sep+ outFile, 'rb').read()
        test_cases = re.findall('(TestCase\d+) STARTED', tst_data)
        for tcase in test_cases:
            if tcase + ' COMPLETED' not in tst_data:
                print('ERROR! `%s` is started, but not completed in the test file `%s` !' % (tcase, outFile))
                exit(1)


        # Open Phoenix sys monitor
        proxy.logMessage('logRunning', 'EP::Windows: Opened sys monitor...\n')
        log_name = PHOENIX_ROOT + time.strftime('%Y-%m-%d %H.%M.%S.log')
        plog = Popen([PHOENIX_ROOT + 'SysMonitor.exe', '192.168.42.122', 'password', 'C:/Simulations', log_name],
            cwd='C:/Simulations')


        cfg_lines = open(PHOENIX_ROOT + 'TestNetwork/config.txt', 'r').readlines()
        proxy.logMessage('logRunning', 'EP::Windows: Preparing config file...\n')
        for i in range(len(cfg_lines)):
            line = cfg_lines[i]
            if line.strip().startswith('(script2)'):
                cfg_lines[i] = '    (script2)' + toExecute + '\n'
        open('C:/Simulations/TestNetwork/config.txt', 'w').write(''.join(cfg_lines))
        del cfg_lines


        # Open Avaya simulator
        proxy.logMessage('logRunning', 'EP::Windows: Executing test file `%s`...\nRunning...\n\n' % toExecute)
        Popen([PHOENIX_ROOT + 'Simulator/Debug/Simulator.exe', '-iC:\Simulations\TestNetwork\config.txt'],
            cwd='C:/Simulations/Simulator/Debug').wait()
        # The simulator should EXIT after each test suite


        # Read the monitor log
        log_data = open(log_name, 'rb').read()
        # Kill the sys monitor
        plog.terminate()


        # Parse the logs
        results = {}
        for tcase in test_cases:
            # Test passed ?
            if tcase + ' STARTED' in log_data and tcase + ' COMPLETED' in log_data:
                results[tcase] = 'PASS'
                print 'EP::Windows: Result: %s passed :) !' % tcase
                proxy.logMessage('logRunning', 'EP::Windows: Result: %s passed !\n' % tcase)
            elif tcase + ' STARTED' in log_data:
                results[tcase] = 'FAIL'
                print 'Result: %s failed :( !' % tcase
                proxy.logMessage('logRunning', 'EP::Windows: Result: %s failed !\n' % tcase)
            else:
                results[tcase] = 'NOT EXEC'
                print 'Result: %s not executed :(( !' % tcase
                proxy.logMessage('logRunning', 'EP::Windows: Result: %s not executed !\n' % tcase)


        timer_f = time.time() - timer_i

        if 'FAIL' in results.values() or 'NOT EXEC' in results.values():
            final_result = 'FAIL'
            proxy.setTestStatus(globEpId, tcName, 3, timer_f) # Status FAIL
        else:
            final_result = 'PASS'
            proxy.setTestStatus(globEpId, tcName, 2, timer_f) # Status PASS

        proxy.logMessage('logRunning',
            'EP::Windows: Finished execution of file `%s`, the result was `%s`.\n\n' % (toExecute, final_result))


        # Cleanup !
        try: os.remove(toExecute)
        except: print 'EP::Python: Cannot cleanup %s!' % toExecute

        global curs
        now = datetime.datetime.today().isoformat()

        for tcase in test_cases:
            curs.execute("INSERT INTO results ( build, station, suite, test_case, date_started, duration, status ) "
                " VALUES ('{build}', '{station}', '{suite}', '{test_case}', '{date_started}', {duration}, '{status}')".format(
                    build = 'b1',
                    station = globEpId,
                    suite = os.path.split(outFile)[0],
                    test_case = tcase,
                    date_started = now,
                    duration = 1,
                    status = results[tcase]
                    ))
        #

#

errMsg = True
conn = MySQLdb.connect(host='11.126.32.9', db='phoenix',user='tsc', passwd='tsc')
curs = conn.cursor()

# Run forever
while 1:

    try:
        # Try to get status from CE!
        STATUS = proxy.getExecStatus(globEpId)
        if not errMsg:
            print('EP warning: Central Engine is running. Reconnected successfully.')
            errMsg = True
    except:
        STATUS = False
        if errMsg:
            print('EP warning: Central Engine is down. Trying to reconnect...')
            errMsg = False
        # Wait and retry...
        time.sleep(2)
        continue

    if STATUS == 'running':
        print('EP debug: Starting the runner!!!')
        tList = proxy.getTestSuiteFileList(globEpId)
        RUN(tList)
        proxy.setExecStatus(globEpId, 0) # Set EpId status STOP

    time.sleep(1)

curs.close()
conn.close()
del errMsg
