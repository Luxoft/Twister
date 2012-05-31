
# File: ExecutionProcessPhoenix.py ; This file is part of Twister.

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

import os
import sys
import re
import time
import datetime
import json
import xmlrpclib
import MySQLdb

from subprocess import Popen

try: CONFIG = json.load(open('phoenix_ep.config'))
except:
    print 'Cannot load Phoenix EP Config !!!'
    print 'The file is corrupted, or it does not exits!'
    exit(1)

# --- Configuration information --------------------------------------------------------------------
globEpName  =  CONFIG['EP']
PHOENIX_IP  =  CONFIG['server']
# --------------------------------------------------------------------------------------------------

#

try:
    proxy = xmlrpclib.ServerProxy('http://'+PHOENIX_IP+':8000/')
    print 'Central Engine started on:', PHOENIX_IP
    print 'Central Engine Status:', proxy.getExecStatus(globEpName)
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

        STATUS = proxy.getExecStatus(globEpName)

        if STATUS == 'stopped': # On stop, DIE!
            print 'EP::Windows: STOP! Exiting.\n'
            return

        elif STATUS == 'paused': # On pause, freeze cycle and wait for Resume or Stop
            print('EP::Windows: Paused!... Press RESUME to continue, or STOP to exit test suite...')
            while 1:
                time.sleep(3)
                STATUS = proxy.getExecStatus(globEpName)
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
            proxy.setFileStatus(globEpName, tcName, 4) # Send status SKIPPED
            continue
        else:
            proxy.setFileStatus(globEpName, tcName, 1) # Send status WORKING

        # The file that will be executed
        toExecute = CONFIG['tests_path'] +os.sep+ outFile

        # Download the file from the Central Engine
        with open(toExecute, "wb") as handle:
            if not proxy.getTestFile(globEpName, tcName):
                print 'EP::Windows: File `%s` will be skipped...' % tcName
                proxy.setFileStatus(globEpName, tcName, 4, 0) # Status SKIP
                continue
            # If the file is not SKIP...
            handle.write(proxy.getTestFile(globEpName, tcName).data)

        proxy.logMessage('logRunning', 'EP::Windows: Downloading file `%s`...\n' % toExecute)

        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        # Must start the logging,
        # then write the TST file to be executed into the config,
        # then start Simulator.exe ...

        # Parse the TST test files
        tst_data = open(toExecute, 'rb').read()
        test_cases = re.findall('(TestCase\d+) STARTED', tst_data)
        test_descrip = '... description ...'

        for tcase in test_cases:
            if tcase + ' COMPLETED' not in tst_data:
                print('ERROR! `%s` is started, but not completed in the test file `%s` !' % (tcase, outFile))
                exit(1)


        # Open Phoenix sys monitor
        proxy.logMessage('logRunning', 'EP::Windows: Opened sys monitor...\n')
        log_name = CONFIG['logs_path'] +os.sep+ time.strftime('%Y-%m-%d %H.%M.%S.log')
        plog = Popen([CONFIG['sys_mon_exe'], CONFIG['sys_mon_IP'], 'password', CONFIG['logs_path'], log_name],
            cwd=CONFIG['logs_path'])


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

        conf_id = proxy.getEpVariable(globEpName, 'conf_id')
        curs.execute( "SELECT file FROM conf_file WHERE id = %s " % conf_id )
        conf_file = curs.fetchone()[0]   # User chosen config file
        ipo_id  = proxy.getEpVariable(globEpName, 'ipo_id')

        # Save in log table.
        curs.execute( "INSERT INTO log (file) VALUES ('%s')" % log_name.replace('\\', '/') )
        curs.execute( "SELECT id FROM log ORDER BY id DESC " )
        log_id = curs.lastrowid

        conn.commit()
        # --------- End of saving ---------

        # Config file path, chosen by user
        conf_file_path = CONFIG['cfg_path'] +os.sep+ conf_file

        cfg_lines = open(conf_file_path, 'r').readlines()
        proxy.logMessage('logRunning', 'EP::Windows: Preparing config file...\n')
        for i in range(len(cfg_lines)):
            line = cfg_lines[i]
            if line.strip().startswith('(script2)'):
                cfg_lines[i] = '    (script2)' + toExecute + '\n'
        open(conf_file_path, 'w').write(''.join(cfg_lines))
        del cfg_lines


        # Open Avaya simulator
        proxy.logMessage('logRunning', 'EP::Windows: Executing test file `%s`...\nRunning...\n\n' % toExecute)
        Popen([CONFIG['simulator_exe'], '-i' + conf_file_path],
            cwd = os.path.split(CONFIG['simulator_exe'])[0] ).wait()
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
            proxy.setFileStatus(globEpName, tcName, 3, timer_f) # Status FAIL
        else:
            final_result = 'PASS'
            proxy.setFileStatus(globEpName, tcName, 2, timer_f) # Status PASS

        proxy.logMessage('logRunning',
            'EP::Windows: Finished execution of file `%s`, the result was `%s`.\n\n' % (toExecute, final_result))


        # Cleanup !
        try: os.remove(toExecute)
        except: print 'EP::Python: Cannot cleanup %s!' % toExecute


        # --------- Saving to database ---------

        # Save into `suite` table :
        curs.execute( "INSERT INTO suite (suite_name, start_time, duration, description, conf_id, ipo_id, log_id) "\
            " VALUES ('{suite_name}', '{start_time}', {duration}, '{description}', {conf_id}, {ipo_id}, {log_id} )".format(
                suite_name  = outFile,
                start_time  = now,
                duration    = timer_f,
                description = test_descrip,
                conf_id     = conf_id,
                ipo_id      = ipo_id,
                log_id      = log_id,
                ))
        suite_id = curs.lastrowid

        # # Save into `results` table.
        for tcase in test_cases:
            curs.execute("INSERT INTO results ( suite_id, test_name, res_value, test_starttime, test_duration ) "
                " VALUES ('{suite_id}', '{test_name}', '{res_value}', '{date_started}', {duration} )".format(
                    suite_id  = suite_id,
                    test_name = tcase,
                    res_value = results[tcase],
                    date_started = now, # TO CHANGE LATER
                    duration     = 0,   # TO CHANGE LATER
                    ))

        conn.commit()
        # --------- End of saving ---------

#

# Run forever
while 1:

    try:
        # Try to get status from CE!
        STATUS = proxy.getExecStatus(globEpName)
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
        tList = proxy.getEpFiles(globEpName)
        RUN(tList)
        proxy.setExecStatus(globEpName, 0) # Set EpId status STOP

    time.sleep(3)

curs.close()
conn.close()

# Eof()
