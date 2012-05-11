
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


# --- Configuration information --------------------------------------------------------------------
globEpId     =  r'EP-1001'
PHOENIX_ROOT =  r'C:\Simulations' + os.sep
PHOENIX_IP   =  r'11.126.32.81'
# --------------------------------------------------------------------------------------------------

#

try:
    proxy = xmlrpclib.ServerProxy('http://'+PHOENIX_IP+':8000/')
    print 'Central Engine Status:', proxy.getExecStatus(globEpId)
    print 'You can start the test from user interface!\n'
except:
    print 'Cannot connect to Central Engine at `%s`!' % PHOENIX_IP
    os.system('pause')
    exit(1)

#

try:
    conn = MySQLdb.connect(host=PHOENIX_IP, db='phoenix', user='usr', passwd='pwd')
    curs = conn.cursor()
    errMsg = True
except:
    print 'Cannot connect to MySQL Server at `%s`!' % PHOENIX_IP
    os.system('pause')
    exit(1)

#

def RUN(tList):

    global conn, curs

    for tcName in tList:

        timer_i = time.time()
        now = datetime.datetime.today().isoformat()

        STATUS = proxy.getExecStatus(globEpId)

        if STATUS == 'stopped': # On stop, DIE!
            print 'EP::Windows: STOP! Exiting.\n'
            return

        elif STATUS == 'paused': # On pause, freeze cycle and wait for Resume or Stop
            print('EP::Windows: Paused!... Press RESUME to continue, or STOP to exit test suite...')
            while 1:
                time.sleep(1)
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
        # then start Simulator.exe ...

        # Parse the TST test files
        tst_data = open(PHOENIX_ROOT + r'TestNetwork\twister' +os.sep+ outFile, 'rb').read()
        test_cases = re.findall('(TestCase\d+) STARTED', tst_data)
        test_descrip = '... description ...'
        for tcase in test_cases:
            if tcase + ' COMPLETED' not in tst_data:
                print('ERROR! `%s` is started, but not completed in the test file `%s` !' % (tcase, outFile))
                exit(1)


        # Open Phoenix sys monitor
        proxy.logMessage('logRunning', 'EP::Windows: Opened sys monitor...\n')
        log_name = PHOENIX_ROOT + time.strftime('%Y-%m-%d %H.%M.%S.log')
        plog = Popen([PHOENIX_ROOT + 'SysMonitor.exe', '192.168.42.122', 'password', 'C:/Simulations', log_name],
            cwd='C:/Simulations')


        # --------- Saving to database ---------

        # # Save in config table. The filename must be unique in the table, so i'll use INSERT OR IGNORE.
        # curs.execute( "SELECT id FROM conf_file ORDER BY id DESC " )
        # conf_id = curs.fetchone()[0] + 1
        # curs.execute( "INSERT IGNORE INTO conf_file (id,file) VALUES (%i,'%s')" % (conf_id, ...) )
        # curs.execute( "SELECT id FROM conf_file WHERE file = '%s' " % ... )
        # conf_id = curs.fetchone()[0]

        # # Save in ipo table. The IP + build_ver are unique together, so i'll use INSERT OR IGNORE.
        # curs.execute( "SELECT id FROM ipo ORDER BY id DESC " )
        # ipo_id = curs.fetchone()[0] + 1
        # r = curs.execute( "INSERT IGNORE INTO ipo (id,ip,build_ver) VALUES (%i,'%s','%s')" %\
        #     (ipo_id, ..., ...) )
        # curs.execute( "SELECT id FROM ipo WHERE ip='%s' AND build_ver='%s' " % (..., ...) )
        # ipo_id = curs.fetchone()[0]

        conf_id = proxy.getEpVariable(globEpId, 'conf_id')
        ipo_id  = proxy.getEpVariable(globEpId, 'ipo_id')

        # Save in log table.
        curs.execute( "INSERT INTO log (file) VALUES ('%s')" % log_name )
        curs.execute( "SELECT id FROM log ORDER BY id DESC " )
        log_id = curs.lastrowid

        conn.commit()
        # --------- End of saving ---------


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


        # --------- Saving to database ---------

        # Save into `suite` table :
        r = curs.execute( "INSERT INTO suite (suite_name, start_time, duration, description, conf_id, ipo_id, log_id) "\
            " VALUES ('{suite_name}', '{start_time}', {duration}, '{description}', {conf_id}, {ipo_id}, {log_id} )".format(
                suite_name  = outFile,
                start_time  = now,
                duration    = timer_f,
                description = test_descrip,
                conf_id     = conf_id,
                ipo_id      = ipo_id,
                log_id      = log_id,
                ))

        # Save into `results` table.
        for tcase in test_cases:
            curs.execute("INSERT INTO results ( suite_id, res_value, test_starttime, test_duration ) "
                " VALUES ('{suite_id}', '{res_value}', '{date_started}', {duration}, )".format(
                    suite_id  = 0,
                    res_value = results[tcase],
                    date_started = now,
                    duration  = 1,
                    ))

        # --------- End of saving ---------

#

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
        time.sleep(3)
        continue

    if STATUS == 'running':
        print('EP debug: Starting the runner !')
        tList = proxy.getTestSuiteFileList(globEpId)
        RUN(tList)
        proxy.setExecStatus(globEpId, 0) # Set EpId status STOP

    time.sleep(2)

curs.close()
conn.close()

# Eof()
