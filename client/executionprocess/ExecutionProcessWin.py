
# File: ExecutionProcessWin.py ; This file is part of Twister.

# version: 2.004

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

import os
import time
import shutil
import logging
import xmlrpclib
from subprocess import Popen
from zipfile import ZipFile

log = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.NOTSET,
    format='%(asctime)s  %(levelname)-8s %(message)s',
    datefmt='%y-%m-%d %H:%M:%S',
    filename='ep_win.log',
    filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.NOTSET)
log.addHandler(console)

import win32com.client
from win32com.client import Dispatch

# -------------------------------------------------------
outDir = os.getcwd()
userName   = 'tscguest'
globEpName = 'EP-1002'
# Central Engine IP and PORT ::
ce_ip_port = '11.126.32.9:8000'
SIKULI_PATH = 'C:/SikuliIDE'
# -------------------------------------------------------

try:
    proxy = xmlrpclib.ServerProxy('http://{}:EP@{}/'.format(userName, ce_ip_port))
    log.debug('Central Engine Status: `{}`.'.format(proxy.getExecStatus(userName, globEpName)))
    log.debug('You can start the test from user interface!\n')
except:
    log.error('Cannot connect to Central Engine!')
    os.system('pause')
    exit(1)

#

def RUN(tList):

    for i in range(len(tList)):

        tcId = tList[i]
        tcName = proxy.getFileVariable(userName, globEpName, tcId, 'file')

        timer_i = time.time()

        STATUS = proxy.getExecStatus(userName, globEpName)

        if STATUS == 'stopped': # On stop, DIE!
            log.debug('EP::Windows: STOP! Exiting.\n')
            return

        elif STATUS == 'paused': # On pause, freeze cycle and wait for Resume or Stop
            log.debug('EP::Windows: Paused!... Press RESUME to continue, or STOP to exit test suite...')
            while 1:
                time.sleep(2)
                STATUS = proxy.getExecStatus(userName, globEpName)
                # On resume, stop waiting
                if STATUS == 'running' or STATUS == 'resume':
                    break
                # On stop...
                elif STATUS == 'stopped': # DIE!
                    log.debug('EP::Windows: STOP! Exiting!...\n')
                    return

        log.debug('EP::Windows: File: `{}` ...'.format(tcName))
        file_ext = os.path.splitext(tcName)[1].lower()
        outFile = os.path.split(tcName)[1] # Exec file

        # Ignores non-sikuli/ selenium/ testcomplete files
        if file_ext != '.zip' and file_ext != '.py' and file_ext != '.testcomplete':
            log.debug('EP::Windows: ... file ignored.\n')
            proxy.setFileStatus(userName, globEpName, tcId, 4) # Send status SKIPPED
            continue
        else:
            proxy.setFileStatus(userName, globEpName, tcId, 1) # Send status WORKING



        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        #
        if file_ext == '.zip':
            with open(outDir + os.sep + outFile, "wb") as handle:
                handle.write(proxy.getTestFile(userName, globEpName, tcId).data)
            with ZipFile(outDir + os.sep + outFile, 'r') as handle:
                handle.extractall(outDir)
            #
            # Sikuli file and folder
            toExecute = outDir + os.sep + os.path.splitext(outFile)[0] + '.skl'
            toDelete = outDir + os.sep + os.path.splitext(outFile)[0] + '.sikuli'
            if not os.path.exists(toExecute) and not os.path.exists(toDelete):
                log.debug('EP::Sikuli: Cannot find sikuli file and folder!')
                print(toExecute)
                print(toDelete)
        #
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        #
        elif file_ext == '.testcomplete':
            with open(outDir + os.sep + outFile, "wb") as handle:
                handle.write(proxy.getTestFile(userName, globEpName, tcId).data)
            with ZipFile(outDir + os.sep + outFile, 'r') as handle:
                handle.extractall(outDir) # This is a FOLDER !
            #
            # Testcomplete files
            toExecute = outDir + os.sep + os.path.splitext(outFile)[0] + os.sep + os.path.splitext(outFile)[0] + '.pjs'
            toDelete = outDir + os.sep + os.path.splitext(outFile)[0]
            if not os.path.exists(toExecute) and not os.path.exists(toDelete):
                log.debug('EP::Testcomplete: Cannot find testcomplete files!')
                print(toExecute)
                print(toDelete)
        #
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        #
        elif file_ext == '.py':
            outPython = outDir + os.sep + outFile
            toExecute = outPython
            with open(outPython, "wb") as handle:
                log.debug('EP::Selenium: Writing selenium file `{}`.'.format(outPython))
                handle.write(proxy.getTestFile(userName, globEpName, tcId).data)

        proxy.logMessage(userName, 'logRunning', 'EP::Windows: Executing file `{}`...\n'.format(toExecute))



        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        #
        if file_ext == '.zip':
            tcr_proc = Popen('"{}/sikuli-script.cmd" -r "{}"'.format(SIKULI_PATH, toExecute), shell=True)
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
                log.warning('EP::TestComplete: Cannot create COM Object!')
                TestCompleteObject = None
                IntegrationObject = None

            log.debug('Debug: COM object:', TestCompleteObject)
            log.debug('Debug: COM integr:', IntegrationObject)

            if TestCompleteObject:

                IntegrationObject.OpenProjectSuite(toExecute)

                if not IntegrationObject.IsProjectSuiteOpened():
                    log.warning('EP::TestComplete: The project suite was not opened!')
                    TestCompleteObject.Quit()
                    TestCompleteObject = None
                    IntegrationObject = None
                    continue

            if TestCompleteObject:

                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                # Project name must be loaded from some config file
                IntegrationObject.RunProject('Project5')

                while IntegrationObject.IsRunning():
                    pass

                ret = IntegrationObject.GetLastResultDescription().Status
                log.debug('EP::TestComplete: Test status:', ret)

                TestCompleteObject.Quit()
                TestCompleteObject = None
                IntegrationObject = None
                os.system('taskkill /F /IM testcomplete.exe /T')
        #
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        #
        elif file_ext == '.py':
            try:
                tcr_proc = Popen('"C:\Python27\python.exe" -B "{}"'.format(outPython), shell=True)
                ret = tcr_proc.wait()
            except:
                ret = -1



        proxy.logMessage(userName, 'logRunning',
            'EP::Windows: Finished execution of file `{}`, return code is `{}`.\n\n'.format(toExecute, ret))
        timer_f = time.time() - timer_i

        if ret:
            proxy.setFileStatus(userName, globEpName, tcId, 3, timer_f) # Status FAIL
        else:
            proxy.setFileStatus(userName, globEpName, tcId, 2, timer_f) # Status PASS



        # Cleanup !
        if file_ext == '.zip':
            try: os.remove(outDir + os.sep + outFile)
            except: log.warning('EP::Sikuli: Cannot cleanup %s!\n' % (outDir + os.sep + outFile))
            try: os.remove(toExecute)
            except: log.warning('EP::Sikuli: Cannot cleanup %s!\n' % toExecute)
            try: shutil.rmtree(path=toDelete, ignore_errors=True)
            except: log.warning('EP::Sikuli: Cannot cleanup %s!\n' % toDelete)
        #
        elif file_ext == '.testcomplete':
            try: os.remove(outDir + os.sep + outFile)
            except: log.warning('EP::Testcomplete: Cannot cleanup %s!\n' % (outDir + os.sep + outFile))
            try: os.remove(toExecute)
            except: log.warning('EP::Testcomplete: Cannot cleanup %s!\n' % toExecute)
            try: shutil.rmtree(path=toDelete, ignore_errors=True)
            except: log.warning('EP::Testcomplete: Cannot cleanup %s!\n' % toDelete)
        #
        elif file_ext == '.py':
            try: os.remove(outDir + os.sep + outFile) ; log.debug('Py cleanup successful.\n')
            except: log.warning('EP::Python: Cannot cleanup %s!\n' % (outDir + os.sep + outFile))
        #

    log.debug('EP debug: Run complete!\n')
    proxy.setExecStatus(userName, globEpName, 0, 'Run complete!') # Set EpId status STOP

#

errMsg = True
# Run forever
while 1:

    try:
        # Try to get status from CE!
        STATUS = proxy.getExecStatus(userName, globEpName)
        if not errMsg:
            log.warning('EP warning: Central Engine is running. Reconnected successfully.')
            errMsg = True
    except:
        STATUS = False
        if errMsg:
            log.warning('EP warning: Central Engine is down. Trying to reconnect...')
            errMsg = False
        # Wait and retry...
        time.sleep(2)
        continue

    if STATUS == 'running':
        log.debug('EP debug: Starting the runner !')
        tList = proxy.getEpFiles(userName, globEpName)
        RUN(tList)

    time.sleep(2)
