#!/usr/bin/env python

# version: 2.002

# File: ExecutionProcess.py ; This file is part of Twister.

# Copyright (C) 2012-2013 , Luxoft

# Authors:
#    Adrian Toader <adtoader@luxoft.com>
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
Execution Process (EP) should be started as a service, on system startup.
Each EP (machine) has a unique name, called Ep Name.
EP gets his status from CE every second. The status can be changed using the Java interface.
When it receives START from CE, it will start the Runner that will execute all test files from suite,
  send all Runner logs to CE and after the execution, it will wait for another START to repeat the cycle.
EP is basically a simple service, designed to start and stop the Runner.
All the hard work is made by the Runner.
'''

import os
import sys
import time
import xmlrpclib
import pickle
import binascii
import socket
import threading
import subprocess
import platform

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print('TWISTER_PATH environment variable is not set! Exiting!')
    exit(1)
sys.path.append(TWISTER_PATH)

from common.constants import *

#

def saveConfig():
    '''
    Saves EpName, RPC Server IP/ Port and current EpName status in a file.
    This file will be read by the Runner.
    '''
    global userName, globEpName, CE_Path, epStatus, TWISTER_PATH

    EP_CACHE = TWISTER_PATH + '/.twister_cache/' + globEpName
    cache_file = EP_CACHE + '/data.pkl'

    try: os.makedirs(EP_CACHE)
    except: pass

    CONFIG = {}
    CONFIG['ID'] = globEpName
    CONFIG['PROXY'] = CE_Path
    CONFIG['STATUS'] = epStatus
    CONFIG['USER']   = userName
    CONFIG['EP'] = globEpName

    f = open(cache_file, 'wb')
    data = pickle.dumps(CONFIG)
    f.write(data)
    f.close() ; del f

#

def packetSnifferStatus(ce):
    """
    Check Packet Sniffer plugin status.
    """
    if not 'PacketSnifferPlugin' in ce.listPlugins(userName):
        return

    global sniffer
    global snifferMessage

    pipe = subprocess.Popen('ps ax | grep start_packet_sniffer.py',
                                    shell=True, stdout=subprocess.PIPE).stdout
    lines = pipe.read().splitlines()
    if len(lines) > 2: return

    if sniffer:
        args = {'command': 'echo'}
        result = ce.runPlugin(userName, 'PacketSnifferPlugin', args)

        if result == 'running':
            if os.getuid() == 0:
                scriptPath =  os.path.join(TWISTER_PATH, 'bin/start_packet_sniffer.py')
                command = ['sudo', 'python', scriptPath, '-u', userName,
                            '-i', str(sniffer), '-t', TWISTER_PATH]
                subprocess.Popen(command, shell=False)
            elif not snifferMessage:
                snifferMessage = True
                print 'Sniffer not starting because the EP is not running as ROOT !'

#

class threadCheckStatus(threading.Thread):
    '''
    Threaded class for checking CE Status.
    Not used in offline mode.
    '''
    def __init__(self):
        global CE_Path
        self.errMsg = True
        self.cycle = 0
        self.proxy = xmlrpclib.ServerProxy(CE_Path)
        threading.Thread.__init__(self)

    def run(self):
        #
        global epStatus, newEpStatus
        global programExit, globEpName
        #
        while not programExit:

            try:
                # Try to get status from CE!
                newEpStatus = self.proxy.getExecStatus(userName, globEpName)
                if not self.errMsg:
                    print('EP warning: Central Engine is running. Reconnected successfully.')
                    self.errMsg = True
            except:
                if self.errMsg:
                    print('EP warning: Central Engine is down. Trying to reconnect...')
                    self.errMsg = False
                # Wait and retry...
                time.sleep(2)
                continue

            # If status changed
            if newEpStatus != epStatus:
                print('Py debug: For EP %s, CE Server returned a new status: %s.' %
                    (globEpName.upper(), str(newEpStatus)))
            epStatus = newEpStatus

            saveConfig() # Save configuration EVERY cycle
            packetSnifferStatus(self.proxy) # Check Packet Sniffer EVERY cycle

            # Save EP info like OS, IP, user id, user group, EVERY 10 cycles
            if not self.cycle:
                try:
                    if not proxy.getEpVariable(userName, globEpName, 'twister_ep_hostname'):
                        proxy.setEpVariable(userName, globEpName, 'twister_ep_os',
                            (platform.machine() +' '+ platform.system() +', '+ ' '.join(platform.linux_distribution())))
                        proxy.setEpVariable(userName, globEpName, 'twister_ep_hostname', socket.gethostname())
                        proxy.setEpVariable(userName, globEpName, 'twister_ep_ip', socket.gethostbyname(socket.gethostname()) )
                        proxy.setEpVariable(userName, globEpName, 'twister_ep_python_revision', '.'.join([str(v) for v in sys.version_info]) )
                except:
                    pass
            self.cycle += 1
            if self.cycle > 10: self.cycle = 0

            if newEpStatus == 'stopped':
                # PID might be invalid, trying to kill it anyway.
                global tcr_pid
                if tcr_pid:
                    try:
                        os.kill(tcr_pid, 9)
                        print('EP warning: STOP from Central Engine! Killing Runner PID %s.' % str(tcr_pid))
                        tcr_pid = None
                    except:
                        pass

            time.sleep(2)
            #

#

class threadCheckLog(threading.Thread):
    '''
    Threaded class for checking LIVE.log.
    '''
    def __init__(self):
        global CE_Path
        self.proxy = xmlrpclib.ServerProxy(CE_Path)
        self.read_len = 0
        threading.Thread.__init__(self)

    def tail(self, file_path):
        global globEpName
        f = open(file_path, 'rb')
        # Go at "current position"
        f.seek(self.read_len, 0)
        vString = f.read()
        vLen = len(vString)
        # Fix double new-line
        vString = vString.replace('\r\n', '\n')
        vString = vString.replace('\n\r', '\n')
        # Increment "current position"
        self.read_len += vLen
        f.close()
        return vString

    def run(self):
        #
        global globEpName, TWISTER_PATH, programExit

        while not programExit:
            #
            vString = self.tail('{0}/.twister_cache/{1}_LIVE.log'.format(TWISTER_PATH, globEpName))

            try:
                # Send log to CE server.
                self.proxy.logLIVE(userName, globEpName, binascii.b2a_base64(vString))
            except:
                # Wait and retry...
                time.sleep(2)
                continue

            time.sleep(2)
            #

#

if __name__=='__main__':

    epStatus = ''
    newEpStatus = ''
    proxy = ''
    filelist = ''
    programExit = False
    sniffer = None
    snifferMessage = False

    try: os.mkdir(TWISTER_PATH + '/.twister_cache/')
    except: pass

    if len(sys.argv) != 5:
        print('EP error: must supply 4 parameters!')
        print('usage:  python ExecutionProcess.py User_Name Ep_Name Host:Port Sniff')
        exit(1)
    else:
        userName = sys.argv[1]
        globEpName = sys.argv[2]
        host = sys.argv[3]
        sniffer = (sys.argv[4], None)[sys.argv[4]=='None']
        print('User: {0} ;  EP: {1} ;  host: {2}'.format(userName, globEpName, host))

    CE_Path = 'http://' + host + '/'
    tcr_pid = None # PID of TC Runner

    proxy = xmlrpclib.ServerProxy(CE_Path)

    threadCheckStatus().start() # Start checking CE status and sending Logs
    threadCheckLog().start() # Start checking CE status and sending Logs

    print('EP debug: Setup done, waiting for START signal.')

    # Run forever and ever
    while 1:

        if epStatus == 'running':

            print('EP debug: Received start signal from CE!')

            # The same Python interpreter that started EP, will be used to start the Runner
            tcr_fname = TWISTER_PATH + '/client/executionprocess/TestCaseRunner.py'
            tcr_proc = subprocess.Popen([sys.executable, '-u', tcr_fname, userName, globEpName, filelist], shell=False)
            # The PID is used in the status thread
            tcr_pid = tcr_proc.pid

            # TestCaseRunner should suicide if timer expired
            tcr_proc.wait()
            ret = tcr_proc.returncode

            # Set EP status STOPPED
            if not ret:
                print('EP debug: Successful run!\n')
                proxy.setExecStatus(userName, globEpName, STATUS_STOP, 'Successful run!')
            if ret == -26:
                print('EP debug: TC Runner exit because of timeout!\n')
                proxy.setExecStatus(userName, globEpName, STATUS_STOP, 'TC Runner exit because of timeout!')
            # Return code != 0
            elif ret:
                print('EP debug: TC Runner exit with error code `{0}`!\n'.format(ret))
                # Set EP status STOPPED
                proxy.setExecStatus(userName, globEpName, STATUS_STOP, 'TC Runner exit with error code `{0}`!'.format(ret))

        time.sleep(2)

    # If the cicle is broken, try to kill the threads...!
    programExit = True

#
