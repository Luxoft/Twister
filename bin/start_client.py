#!/usr/bin/env python

# File: start_client.py ; This file is part of Twister.

# version: 1.005

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

    def killAll(self):
        """
        Close all Sniffers and EPs.
        """
        pipe = subprocess.Popen('ps ax | grep start_packet_sniffer.py', shell=True, stdout=subprocess.PIPE)
        for line in pipe.stdout.read().splitlines():
            try:
                os.kill(int(line.split()[0]), 9)
            except Exception as e:
                pass
        del pipe

        pipe = subprocess.Popen('ps ax | grep ExecutionProcess.py', shell=True, stdout=subprocess.PIPE)
        for line in pipe.stdout.read().splitlines():
            try:
                os.kill(int(line.split()[0]), 9)
            except Exception as e:
                pass
        del pipe

#

    def _createConn(self, ce_ip, ce_port, debug=True):
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
            proxy.root.hello('client')
            print('Client Debug: Connected to CE at `{}:{}`...'.format(ce_ip, ce_port))
        except Exception as e:
            if debug:
                print('*ERROR* Cannot connect to CE path `{}:{}`! Exception `{}`!'.format(ce_ip, ce_port, e))
            return None

        # Authenticate on RPyc server
        try:
            check = proxy.root.login(self.userName, 'EP')
            print('Client Debug: Authentication successful!\n')
        except Exception as e:
            check = False

        if not check:
            print('*ERROR* Cannot authenticate on CE path `{}:{}`!'.format(ce_ip, ce_port))
            return None

        bg = BgServingThread(proxy)
        return proxy

#

    def _createConnLong(self, cePath):
        """
        Create connection to Central Engine, return the connection and
        auto-save it in the Proxy Dict.
        """
        proxy = None
        ce_ip, ce_port = cePath.split(':')
        ce_port = int(ce_port)

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
                proxy = self._createConn(ce_ip, ce_port, err_msg)
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
        print('\nWill REGISTER EPs on CE `{}` :: `{}`...\n'.format(cePath, epNames))
        # This operation might take a while!...
        self._createConnLong(cePath)
        # Register all this information on the current Central Engine
        self.proxyDict[cePath].root.registerEps(epNames)
        print('\nSuccess REGISTER EPs on CE `{}` :: `{}` !\n'.format(cePath, epNames))

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

        # This will be a temporary list of valid EP names, filtered by IP/ host
        self.epList = []

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
                self.epList.append(ep)
                continue
            # If the HOST filter is empty, it's a valid EP
            if not cfg.get(ep, 'EP_HOST'):
                print('EP `{}` has an empty HOST filter, so is valid.'.format(ep))
                self.epList.append(ep)
                continue

            # This is an EP with EP HOST filter!
            ep_host = cfg.get(ep, 'EP_HOST')
            # If the host from EPNAMES matches, it's a valid EP
            if ep_host == self.hostName:
                print('EP `{}` has a HOST match ({}), so is valid.'.format(ep, ep_host))
                self.epList.append(ep)
            try:
                # If the ip from EPNAMES matches this IP, it's a valid EP
                if ep_host in socket.gethostbyaddr(self.hostName)[-1]:
                    print('EP `{}` has an IP match ({}), so is valid.'.format(ep, ep_host))
                    self.epList.append(ep)
            except Exception as e:
                pass

            print('EP `{}` doesn\'t match with required HOST `{}`, so is ignored.'.format(ep, ep_host))

        # Sort and eliminate duplicates
        self.epList = sorted(set(self.epList))

        print('Found `{}` EPs: {}.\n'.format(len(self.epList), self.epList))
        return self.epList

#

    def parseConfiguration(self):
        """
        Parse the EPNAMES.ini and prepare to launch the Execution Processes.
        """
        global TWISTER_PATH

        # The Config Parser instance
        cfg = SafeConfigParser()
        cfg.read('{}/config/epname.ini'.format(TWISTER_PATH))

        self._reloadEps(cfg)

        # Generate meta-data for each EP
        for currentEP in self.epList:
            # Incomplete EP tag ?
            if not cfg.has_option(currentEP, 'CE_IP') or not cfg.has_option(currentEP, 'CE_PORT'):
                continue

            # A lot of meta-data for current EP
            epData = {}
            epData['pid']   = None
            epData['ce_ip'] = cfg.get(currentEP, 'CE_IP')
            epData['ce_port'] = cfg.get(currentEP, 'CE_PORT')

            epData['exec_str'] = 'nohup {py} -u {path}/client/executionprocess/ExecutionProcess.py '\
                   '{user} {ep} "{ip}:{port}" > /dev/null &'.format(
                    py = sys.executable,
                    path = TWISTER_PATH,
                    user = self.userName,
                    ep = currentEP,
                    ip = epData['ce_ip'],
                    port = epData['ce_port']
                )

            self.epNames[currentEP] = epData

        del cfg

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
        except Exception as e:
            trace = traceback.format_exc()[34:].strip()
            print('ClientService: Error on Hello: `{}`.'.format(trace))
            return False


    def exposed_start_ep(self, epname):
        """
        Start 1 EP.
        """
        global userName, client

        if epname not in client.epNames:
            print('*ERROR* Unknown EP name : `{}` !'.format(epname))
            return False

        if client.epNames[epname]['pid']:
            print('Error: Process {} is already started for user {}! (pid={})\n'.format(
                  epname, userName, client.epNames[epname]['pid']))
            return False

        print('Executing: `{}`.'.format(client.epNames[epname]['exec_str']))

        try:
            p = subprocess.Popen(client.epNames[epname]['exec_str'], shell=True, preexec_fn=os.setsid)
            client.epNames[epname]['pid'] = p
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
            print('*ERROR* Unknown EP name : `{}` !'.format(epname))
            return False

        if not client.epNames[epname]['pid']:
            print('Error: EP `{}` is not running !'.format(epname))
            return False

        print('Preparing to stop EP `{}`...'.format(epname))
        time.sleep(1) # A small delay

        try:
            os.kill(client.epNames[epname]['pid'].pid, signal.SIGTERM)
            client.epNames[epname]['pid'] = None
        except:
            trace = traceback.format_exc()[34:].strip()
            print('ClientService: Error on Stop EP: `{}`.'.format(trace))
            return False

        print('Stopped EP `{}` !'.format(epname))
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
