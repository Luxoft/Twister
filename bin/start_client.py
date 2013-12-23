#!/usr/bin/env python2.7

# File: start_client.py ; This file is part of Twister.

# version: 3.001

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

"""
This file will register ALL Execution Processes that are enabled,
from file `twister/config/epname.ini` !
To be able to start the Packet Sniffer, this must run as ROOT.
"""
from __future__ import print_function
from __future__ import with_statement

import os
import sys
import time
import signal
import socket
socket.setdefaulttimeout(5)
import thread
import traceback
import platform
import subprocess
import rpyc

from pprint import pprint
from datetime import datetime
from rpyc import BgServingThread
from ConfigParser import SafeConfigParser


if not sys.version.startswith('2.7'):
    print('Python version error! The client must run on Python 2.7!')
    exit(1)

def userHome(user):
    """ Return user home path for all kind of users """
    if platform.system().lower() == 'windows':
        return os.getenv('HOME')
    else:
        return subprocess.check_output('echo ~' + user, shell=True).strip()

try:
    userName = os.getenv('USER') or os.getenv('USERNAME')
    if userName=='root':
        userName = os.getenv('SUDO_USER') or userName
    print('\nHello username `{}`!'.format(userName))
except:
    userName = ''
if not userName:
    print('\nCannot guess user name for the Twister Client! Exiting!\n')
    exit(1)


# Twister path environment
TWISTER_PATH = userHome(userName).rstrip('/') + '/twister'
os.environ['TWISTER_PATH'] = TWISTER_PATH


# # #


class TwisterClient(object):

    def __init__(self):

        global userName
        self.userName = userName
        self.hostName = socket.gethostname().lower()
        self.epList = []
        self.epNames = {}
        self.proxyDict = {}
        self.proxyLock = thread.allocate_lock()
        # Kill all sniffers and EPs
        self.killAll()
        # Parse and register EPs
        self.parseConfiguration()
        self.registerEPs()

#

    def _kill(self, lines, descr=''):
        """
        Helper function.
        """
        for line in lines.strip().splitlines():
            li = line.strip().split()
            PID = int(li[0])
            del li[1:4]
            if li[1] == '/bin/sh' and li[2] == '-c': continue
            print('Killing ugly zombie {} `{}`'.format(descr, ' '.join(li)))
            try:
                os.kill(PID, 9)
            except:
                pass

#

    def killAll(self):
        """
        Close all Sniffers and EPs for this user.
        """
        global userName

        pids = subprocess.check_output('ps ax | grep /bin/start_packet_sniffer.py | grep "\-u {}"'.format(userName), shell=True)
        self._kill(pids, 'Sniffer')

        pids = subprocess.check_output('ps ax | grep /executionprocess/ExecutionProcess.py | grep "\-u {}"'.format(userName), shell=True)
        self._kill(pids, 'EP')

#

    def _createConn(self, ce_ip, ce_port, epNames=[], debug=False):
        """
        Helper for creating a Central Engine connection, the most basic func.
        """
        config = {
            'allow_pickle': True,
            'allow_getattr': True,
            'allow_setattr': True,
            'allow_delattr': True,
            'allow_all_attrs': True,
        }

        # Connect to RPyc server
        try:
            proxy = rpyc.connect(ce_ip, ce_port, service=TwisterClientService, config=config)
            print('Client Debug: Connected to CE at `{}:{}`...'.format(ce_ip, ce_port))
        except Exception as e:
            if debug:
                print('*ERROR* Cannot connect to CE path `{}:{}`! Exception: `{}`!'.format(ce_ip, ce_port, e))
            return None

        # Authenticate on RPyc server
        try:
            check = proxy.root.login(self.userName, 'EP')
            if check: print('Client Debug: Authentication successful!')
        except Exception as e:
            check = False

        if not check:
            if debug:
                print('*ERROR* Cannot authenticate on CE path `{}:{}`!'.format(ce_ip, ce_port))
            return None

        # Say Hello and Register all EPs on the current Central Engine
        if epNames:
            try:
                # Call the user status to create the User Project
                proxy.root.getUserVariable('status')
                proxy.root.hello('client', {'eps': epNames})
                print('Client Debug: Register EPs successful!')
            except Exception as e:
                print('Exception:', e)
                check = False

        if not check:
            if debug:
                print('*ERROR* Cannot send hello on CE path `{}:{}`!'.format(ce_ip, ce_port))
            return None

        bg = BgServingThread(proxy)
        return proxy

#

    def _createConnLong(self, cePath, epNames=[]):
        """
        Create connection to Central Engine, return the connection and
        auto-save it in the Proxy Dict.
        """
        proxy = None
        ce_ip, ce_port = cePath.split(':')
        ce_port = int(ce_port)

        # Transform XML-RPC port into RPyc Port; RPyc port = XML-RPC port + 10 !
        ce_port += 10

        with self.proxyLock:
            # Try to re-use the old Central Engine connection
            proxy = self.proxyDict.get(cePath, None)

            if proxy:
                # If the hello works, the connection is just fine
                try:
                    proxy.root.echo('ping')
                    print('Connection to Central Engine at `{}` is ok!'.format(cePath))
                    return True
                # If the hello doesn't work, it means the connection was lost/ destroyed
                except:
                    proxy = None

        err_msg = True
        last_time = time.time()
        # When to print the next Warning that this thread is trying to reconnect
        time_diff = 30

        while True:
            if not proxy:
                # Try creating a new Central Engine connection.
                proxy = self._createConn(ce_ip, ce_port, epNames, err_msg)
            else:
                break

            # Save the connection, or the failed result, in a thread safe mode.
            with self.proxyLock:
                self.proxyDict[cePath] = proxy

            if not proxy:
                if err_msg:
                    print('*ERROR* Cannot connect to Central Engine at `{}`! Will Retry forever and ever...'.format(cePath))
                    err_msg = False
                elif time.time() > last_time + time_diff:
                    print('*ERROR* Still trying to connect to Central Engine at `{}`...'.format(cePath))
                    last_time = time.time()
                # Wait a little, before trying to connect again.
                time.sleep(2)
            else:
                break

        return True

#

    def lazyRegister(self, cePath, epNames):
        """
        Register EP Names on Central Engine.
        Used in a thread to try and connect to the required Central Engine.
        """
        print('\n### Will REGISTER EPs on CE `{}` :: `{}` ###\n'.format(cePath, epNames))
        # Cleanup all zombie processes
        self.killAll()
        # This operation might take a while!...
        self._createConnLong(cePath, epNames)
        print('\n### Success REGISTER EPs on CE `{}` :: `{}` ###\n'.format(cePath, epNames))

#

    def _reloadEps(self, cfg):
        """
        Use the config from EPNAMES to create a list of EPs, filtered by IP and Host.
        """
        # Sniffer config
        snifferEth = None
        if (cfg.has_option('PACKETSNIFFERPLUGIN', 'ETH_INTERFACE') and cfg.get('PACKETSNIFFERPLUGIN', 'ENABLED') == '1'):
            snifferEth = cfg.get('PACKETSNIFFERPLUGIN', 'ETH_INTERFACE')
        else:
            snifferEth = 'eth0'

        TwisterClientService.snifferEth = snifferEth

        print('Sniffer eth = `{}`.'.format(snifferEth))
        print('Building the EP list for this machine...')

        # This will be a temporary list of valid EP names, filtered by Enabled/ IP/ host
        epList = []

        # Cycle all EPs
        for ep in cfg.sections():
            # EP disabled ?
            if cfg.has_option(ep, 'ENABLED'):
                if cfg.get(ep, 'ENABLED') in ['0', 'false']:
                    print('EP `{}` is disabled.'.format(ep))
                    continue
            # Invalid EP tag ?
            if not cfg.has_option(ep, 'CE_IP') or not cfg.has_option(ep, 'CE_PORT'):
                # print('Section `{}` is not a valid EP.'.format(ep))
                continue
            # If this EP does NOT have a HOST filter, it's a valid EP
            if not cfg.has_option(ep, 'EP_HOST'):
                print('EP `{}` doesn\'t have a HOST filter, so is valid.'.format(ep))
                epList.append(ep)
                continue
            # If the HOST filter is empty, it's a valid EP
            if not cfg.get(ep, 'EP_HOST'):
                print('EP `{}` has an empty HOST filter, so is valid.'.format(ep))
                epList.append(ep)
                continue

            # This is an EP with EP HOST filter!
            ep_host = cfg.get(ep, 'EP_HOST')
            # If the host from EPNAMES matches, it's a valid EP
            if ep_host == self.hostName:
                print('EP `{}` has a HOST match ({}), so is valid.'.format(ep, ep_host))
                epList.append(ep)
            try:
                # If the ip from EPNAMES matches this IP, it's a valid EP
                if ep_host in socket.gethostbyaddr(self.hostName)[-1]:
                    print('EP `{}` has an IP match ({}), so is valid.'.format(ep, ep_host))
                    epList.append(ep)
            except Exception as e:
                pass

            print('EP `{}` doesn\'t match with required HOST `{}`, so is ignored.'.format(ep, ep_host))

        # Sort and eliminate duplicates
        self.epList = sorted(set(epList))

        print('Found `{}` EPs: {}.\n'.format(len(self.epList), self.epList))
        return self.epList

#

    def addEp(self, epname, ce_ip, ce_port):
        """
        Shortcut function to add a new EP in the EP structure.
        """
        # A lot of meta-data for current EP
        epData = {}
        epData['pid'] = None
        epData['ce_ip'] = ce_ip
        epData['ce_port'] = ce_port

        epData['exec_str'] = 'nohup {py} -u {path}/client/executionprocess/ExecutionProcess.py '\
                '-u {user} -e {ep} -s {ip}:{port} > "{path}/.twister_cache/{ep}_LIVE.log" '.format(
                py = sys.executable,
                path = TWISTER_PATH,
                user = self.userName,
                ep = epname,
                ip = epData['ce_ip'],
                port = epData['ce_port']
            )

        self.epNames[epname] = epData
        return True

#

    def parseConfiguration(self):
        """
        Parse the EPNAMES.ini and prepare to launch the Execution Processes.
        """
        global TWISTER_PATH

        # The Config Parser instance
        cfg = SafeConfigParser()
        cfg.read('{}/config/epname.ini'.format(TWISTER_PATH))

        epList = self._reloadEps(cfg)

        # Generate meta-data for each EP + the Anonymous EP
        for currentEP in epList:
            # Incomplete EP tag ?
            if not cfg.has_option(currentEP, 'CE_IP') or not cfg.has_option(currentEP, 'CE_PORT'):
                continue
            self.addEp(currentEP, cfg.get(currentEP, 'CE_IP'), cfg.get(currentEP, 'CE_PORT'))

        return True

#

    def registerEPs(self, ce_proxy=None):
        """
        Register EPs to Central Engines.
        The function is called on START and on DISCONNECT from a Central Engine.
        """
        if ce_proxy:
            print('Starting Client Service register on `{}`...'.format(ce_proxy))
        else:
            print('Starting Client Service register...')

        # print('\n----- Config Data ----')
        # pprint(self.epNames, indent=2, width=100) # DEBUG !
        # print('----------------------\n')

        # Central Engine addrs and the EPs that must be registered for each CE
        epsToRegister = {}

        for currentEP, epData in self.epNames.iteritems():
            cePath = '{}:{}'.format(epData['ce_ip'], epData['ce_port'])
            # If Central Engine proxy filter is specified, use it
            if ce_proxy and ce_proxy != epData['ce_ip']:
                continue

            epsToRegister[cePath] = [
                ep for ep in self.epNames
                if self.epNames[ep]['ce_ip'] == self.epNames[currentEP]['ce_ip'] and
                self.epNames[ep]['ce_port'] == self.epNames[currentEP]['ce_port']
              ]

        print('\n------- EPs to register -------')
        pprint(epsToRegister, indent=2, width=100)
        print('-------------------------------\n')

        # For each Central Engine address
        for cePath, epNames in epsToRegister.iteritems():
            if not epNames: continue
            thread.start_new_thread( self.lazyRegister, (cePath, epNames) )

        print('Register EPs function finished.\n'\
              'If not all CE connections are made, they will be created asynchronously.')

#

    def run(self):
        """
        Blocked forever and ever.
        """
        while 1:
            time.sleep(1)


# # #


class TwisterClientService(rpyc.Service):

    connections = {}
    config = None
    snifferEth = None


    def on_connect(self):
        """
        Runs when a connection is created (to init the service).
        `_conn` is a weakproxy that points to this local service and the remote service.
        `_conn._config` is a dict containing all the information about the connection.
        `_conn.root` is the netref to the Central Engine remote service.
        """
        connid = self._conn._config['connid']
        self.connections[connid] = None
        # print('ClientService: New Client connection: `{}`.'.format(connid))


    def on_disconnect(self):
        """
        Runs when the connection has already closed (to finalize the service).
        """
        global client
        connid = self._conn._config['connid']

        try:
            proxy = self.connections.pop(connid)
            if proxy: client.registerEPs(proxy)
        except Exception as e:
            trace = traceback.format_exc()[34:].strip()
            print('ClientService: Disconnect Error: `{}`!'.format(trace))


    def exposed_echo(self, msg):
        """
        For testing connection
        """
        if msg != 'ping': print(':: {}'.format(msg))
        return 'Echo: {}'.format(msg)


    def exposed_hello(self, proxy):
        """
        The first function called.
        """
        connid = self._conn._config['connid']

        try:
            self.connections[connid] = proxy
            print('ClientService: Hello `{}`!'.format(proxy))
            return True
        except:
            trace = traceback.format_exc()[34:].strip()
            print('ClientService: Error on Hello: `{}`.'.format(trace))
            return False


    def exposed_add_ep(self, epname, ce_ip, ce_port):
        """
        Add a new EP in the EP structure.
        """
        global client
        try:
            client.addEp(self, epname, ce_ip, ce_port)
            return True
        except:
            trace = traceback.format_exc()[34:].strip()
            print('ClientService: Error on Add EP: `{}`.'.format(trace))
            return False


    def exposed_start_ep(self, epname):
        """
        Start 1 EP.
        """
        global userName, client

        if epname not in client.epNames:
            print('*ERROR* Cannot start! Unknown EP name : `{}` !'.format(epname))
            return False

        tproc = client.epNames[epname].get('pid')

        if tproc:
            print('Error: Process {} is already started for user {}! (proc={})\n'.format(epname, userName, tproc))
            return False

        exec_str = client.epNames[epname]['exec_str']
        print('Executing: `{}`.'.format(exec_str))

        try:
            tproc = subprocess.Popen(exec_str, shell=True, preexec_fn=os.setsid)
            client.epNames[epname]['pid'] = tproc
        except:
            trace = traceback.format_exc()[34:].strip()
            print('ClientService: Error on Start EP: `{}`.'.format(trace))
            return False

        print('EP `{}` for user `{}` launched in background!\n'.format(epname, userName))
        return True


    def exposed_stop_ep(self, epname):
        """
        Stop 1 EP.
        """
        global userName, client

        if epname not in client.epNames:
            print('*ERROR* Cannot stop! Unknown EP name : `{}` !'.format(epname))
            return False

        tproc = client.epNames[epname].get('pid')
        if not tproc: return False

        print('Preparing to stop EP `{}`...'.format(epname))
        PID = tproc.pid

        try:
            os.killpg(PID, signal.SIGINT)
            time.sleep(0.5)
            os.killpg(PID, 9)
            client.epNames[epname]['pid'] = None
        except:
            trace = traceback.format_exc()[34:].strip()
            print('ClientService: Error on Stop EP: `{}`.'.format(trace))
            return False

        # Normally, this will Never execute, but kill the stubborn zombies, just in case
        Tries = 3
        while Tries > 0:
            ps = subprocess.check_output('ps ax | grep ExecutionProcess.py | grep -u {} | grep -e {}'.format(userName, epname), shell=True)
            ps = ps.strip().splitlines()[:-2] # Ignore the last 2 lines (the grep and shell=True)
            # If all the processes are dead, it's ok
            if not ps: break

            # Another small delay, before killing the zombie
            time.sleep(0.25)
            Tries -= 1

            for line in ps:
                li = line.strip().split()
                PID = li[0]
                del li[1:4]
                print('Killing `{}`'.format(' '.join(li)))
                try:
                    os.kill(int(PID), 9)
                    client.epNames[epname]['pid'] = None
                except:
                    trace = traceback.format_exc()[34:].strip()
                    print('ClientService: Error on Stop EP: `{}`.'.format(trace))
                    # return False # No need to exit

        print('Stopped EP `{}`! (pid = {})\n'.format(epname, PID))
        return True


    def exposed_start_sniffer(self):
        """ start sniffer """

        # check if already running
        pipe = subprocess.Popen('ps ax | grep start_packet_sniffer.py',
                                    shell=True, stdout=subprocess.PIPE).stdout
        lines = pipe.read().splitlines()
        del pipe
        if len(lines) > 2:
            return False

        snifferEth = ['eth0', self.snifferEth][self.snifferEth is not None]

        # start sniffer
        scriptPath = os.path.join(TWISTER_PATH, 'bin/start_packet_sniffer.py')
        logPath = os.path.join(TWISTER_PATH, 'sniffer_log.log')
        command = ['python', '-u', scriptPath, '-u', userName,
                        '-i', snifferEth, '-t', TWISTER_PATH]
        with open(logPath, 'wb+') as logFile:
            subprocess.Popen(command, stdout=logFile, stderr=logFile)

        return True


    def exposed_stop_sniffer(self):
        """ stop sniffer """

        pipe = subprocess.Popen('ps ax | grep start_packet_sniffer.py', shell=True, stdout=subprocess.PIPE)
        for line in pipe.stdout.read().splitlines():
            try:
                os.kill(int(line.split()[0]), 9)
            except Exception as e:
                pass
        del pipe


# # #


if __name__ == "__main__":

    print('Starting Twister Client...\n')

    # This will read everything from epnames and connect to all CEs
    client = TwisterClient()
    client.run()

    print('Stopping Twister Client.')


# Eof()
