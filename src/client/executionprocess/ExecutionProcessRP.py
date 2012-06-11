
# File: ExecutionProcessRP.py ; This file is part of Twister.

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
import time
import shutil
import time
import xmlrpclib
from subprocess import Popen
from zipfile import ZipFile

import win32com.client
from win32com.client import Dispatch

# -------------------------------------------------------
outDir = os.getcwd()
globEpName = 'EP-1001'
proxy = xmlrpclib.ServerProxy('http://11.126.32.9:8000/')   # Tsc Server
#proxy = xmlrpclib.ServerProxy('http://11.126.32.12:8000/') # Dan Ubuntu
#proxy = xmlrpclib.ServerProxy('http://11.126.32.14:8000/') # Cro Windows
#proxy = xmlrpclib.ServerProxy('http://127.0.0.1:8000/')    # VirtualBox VM
# -------------------------------------------------------

try:
    print 'Central Engine Status:', proxy.getExecStatus(globEpName)
    print 'You can start the test from user interface!\n'
except: print 'Cannot connect to Central Engine!'

#

def RUN(tList):

    for i in range(len(tList)):

        tcId = tList[i]
        tcName = proxy.getFileVariable(tcId, 'file')

        timer_i = time.time()

        STATUS = proxy.getExecStatus(globEpName)

        if STATUS == 'stopped': # On stop, DIE!
            print 'EP::Windows: STOP! Exiting.\n'
            return

        elif STATUS == 'paused': # On pause, freeze cycle and wait for Resume or Stop
            print('EP::Windows: Paused!... Press RESUME to continue, or STOP to exit test suite...')
            while 1:
                time.sleep(0.5)
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

        # Ignores non-sikuli/ selenium/ testcomplete files
        if file_ext != '.zip' and file_ext != '.py' and file_ext != '.testcomplete':
            print 'EP::Windows: ... file ignored.\n'
            proxy.setFileStatus(globEpName, tcId, 4) # Send status SKIPPED
            continue
        else:
            proxy.setFileStatus(globEpName, tcId, 1) # Send status WORKING



        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        #
        if file_ext == '.zip':
            with open(outDir + os.sep + outFile, "wb") as handle:
                handle.write(proxy.getTestFile(globEpName, tcId).data)
            with ZipFile(outDir + os.sep + outFile, 'r') as handle:
                handle.extractall(outDir)
            #
            # Sikuli file and folder
            toExecute = outDir + os.sep + os.path.splitext(outFile)[0] + '.skl'
            toDelete = outDir + os.sep + os.path.splitext(outFile)[0] + '.sikuli'
            if not os.path.exists(toExecute) and not os.path.exists(toDelete):
                print 'EP::Sikuli: Cannot find sikuli file and folder!'
                print(toExecute)
                print(toDelete)
        #
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        #
        elif file_ext == '.testcomplete':
            with open(outDir + os.sep + outFile, "wb") as handle:
                handle.write(proxy.getTestFile(globEpName, tcId).data)
            with ZipFile(outDir + os.sep + outFile, 'r') as handle:
                handle.extractall(outDir) # This is a FOLDER !
            #
            # Testcomplete files
            toExecute = outDir + os.sep + os.path.splitext(outFile)[0] + os.sep + os.path.splitext(outFile)[0] + '.pjs'
            toDelete = outDir + os.sep + os.path.splitext(outFile)[0]
            if not os.path.exists(toExecute) and not os.path.exists(toDelete):
                print 'EP::Testcomplete: Cannot find testcomplete files!'
                print(toExecute)
                print(toDelete)
        #
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        #
        elif file_ext == '.py':
            outPython = outDir + os.sep + outFile
            with open(outPython, "wb") as handle:
                print 'EP::Selenium: Writing selenium file `%s`.' % outPython
                handle.write(proxy.getTestFile(globEpName, tcId).data)

        proxy.logMessage('logRunning', 'EP::Windows: Executing file `%s`...\n' % toExecute)



        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        #
        if file_ext == '.zip':
            tcr_proc = Popen('"C:\Program Files\Sikuli X\Sikuli-ide.bat" -r "%s"' % toExecute, shell=True)
            ret = tcr_proc.wait()
        #
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        #
        elif file_ext == '.testcomplete':

            try:
                TestCompleteObject = Dispatch('TestComplete.TestCompleteApplication')
                TestCompleteObject.Visible = 1
                IntegrationObject = TestCompleteObject.Integration
            except:
                print('EP::TestComplete: Cannot create COM Object!')
                TestCompleteObject = None
                IntegrationObject = None

            print('Debug: COM object:', TestCompleteObject)
            print('Debug: COM integr:', IntegrationObject)

            if TestCompleteObject:

                IntegrationObject.OpenProjectSuite(toExecute)

                if not IntegrationObject.IsProjectSuiteOpened():
                    print('EP::TestComplete: The project suite was not opened!')
                    TestCompleteObject.Quit()
                    TestCompleteObject = None
                    IntegrationObject = None
                    exit(1)

            if TestCompleteObject:

                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                # Project name must be loaded from some config file
                IntegrationObject.RunProject('Project5')

                while IntegrationObject.IsRunning():
                    pass

                ret = IntegrationObject.GetLastResultDescription().Status
                print('EP::TestComplete: Test status:', ret)

                TestCompleteObject.Quit()
                TestCompleteObject = None
                IntegrationObject = None
                os.system('taskkill /F /IM testcomplete.exe /T')
        #
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        #
        elif file_ext == '.py':
            tcr_proc = Popen('"C:\Python27\python.exe" -B "%s"' % outPython, shell=True)
            ret = tcr_proc.wait()



        proxy.logMessage('logRunning',
            'EP::Windows: Finished execution of file `%s`, return code is `%i`.\n\n' % (toExecute, ret))
        timer_f = time.time() - timer_i

        if ret:
            proxy.setFileStatus(globEpName, tcId, 3, timer_f) # Status FAIL
        else:
            proxy.setFileStatus(globEpName, tcId, 2, timer_f) # Status PASS



        # Cleanup !
        if file_ext == '.zip':
            try: os.remove(outDir + os.sep + outFile)
            except: print 'EP::Sikuli: Cannot cleanup %s!\n' % (outDir + os.sep + outFile)
            try: os.remove(toExecute)
            except: print 'EP::Sikuli: Cannot cleanup %s!\n' % toExecute
            try: shutil.rmtree(path=toDelete, ignore_errors=True)
            except: print 'EP::Sikuli: Cannot cleanup %s!\n' % toDelete
        #
        elif file_ext == '.testcomplete':
            try: os.remove(outDir + os.sep + outFile)
            except: print 'EP::Testcomplete: Cannot cleanup %s!\n' % (outDir + os.sep + outFile)
            try: os.remove(toExecute)
            except: print 'EP::Testcomplete: Cannot cleanup %s!\n' % toExecute
            try: shutil.rmtree(path=toDelete, ignore_errors=True)
            except: print 'EP::Testcomplete: Cannot cleanup %s!\n' % toDelete
        #
        elif file_ext == '.py':
            try: os.remove(outDir + os.sep + outFile)
            except: print 'EP::Python: Cannot cleanup %s!\n' % (outDir + os.sep + outFile)
        #

#

errMsg = True
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
        time.sleep(2)
        continue

    if STATUS == 'running':
        print('EP debug: Starting the runner!!!')
        tList = proxy.getEpFiles(globEpName)
        RUN(tList)
        proxy.setExecStatus(globEpName, 0) # Set EpId status STOP

    time.sleep(2)
