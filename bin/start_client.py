#!/usr/bin/env python

# File: start_client.py ; This file is part of Twister.

# version: 1.004

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
import json
import socket
import traceback
import subprocess
import rpyc

from pprint import pprint
from datetime import datetime
from ConfigParser import SafeConfigParser
from rpyc.utils.helpers import BgServingThread


if not sys.version.startswith('2.7'):
    print('Python version error! The client must run on Python 2.7!')
    exit(1)

def userHome(user):
    """ Return user home path for all kind of users """
    return subprocess.check_output('echo ~' + user, shell=True).strip()

try:
    userName = os.getenv('USER')
    if userName=='root':
        userName = os.getenv('SUDO_USER')
except:
    print('Cannot guess user name for the Twister Client! Exiting!')
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
        self.snifferEth = ''
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

    def _createConn(self, ce_ip, ce_port):
        """
        Helper for creating Central Engine connection.
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
            BgServingThread(proxy)
            proxy.root.hello('client')
            print('Client Debug: Connected to CE at `{}:{}`...'.format(ce_ip, ce_port))
        except Exception as e:
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

        return proxy

#

    def createConnection(self, cePath):
        """
        Create connection to Central Engine, return the connection and
        alsosave it in proxyDict.
        """
        proxy = None
        retries = 0
        maxRetries = 9

        ce_ip, ce_port = cePath.split(':')
        ce_port = int(ce_port)

        # Try to re-use the old Central Engine connection
        proxy = self.proxyDict.get(cePath, None)
        if proxy:
            # If the hello works, the connection is just fine
            try:
                proxy.root.hello('client')
                return proxy
            # If the hello doesn't work, it means the connection was destroyed
            except:
                proxy = None

        while retries <= maxRetries:
            retries += 1
            if not proxy:
                # Maybe creating a new Central Engine connection will work ?
                proxy = self._createConn(ce_ip, ce_port)
                self.proxyDict[cePath] = proxy
            else:
                break
            if not proxy:
                self.proxyDict[cePath] = None
                print('*ERROR* Cannot connect to Central Engine at `{}`... Retry {}...'.format(cePath, retries))
                time.sleep(2)
            else:
                break

        if not proxy:
            print('*ERROR* Central Engine is down forever.')
            return {}

        return proxy

#

    def _reloadEps(self, cfg):
        """
        Use the config from EPNAMES to create a list of EPs, filtered by IP and Host.
        """
        # Sniffer config
        if (cfg.has_option('PACKETSNIFFERPLUGIN', 'EP_HOST') and cfg.get('PACKETSNIFFERPLUGIN', 'ENABLED') == '1'):
            self.snifferEth = cfg.get('PACKETSNIFFERPLUGIN', 'ETH_INTERFACE')
        else:
            self.snifferEth = 'eth0'

        print('Sniffer eth = `{}`.'.format(self.snifferEth))
        print('Building the EP list for this machine...')

        # This will be a temporary list of valid EP names, filtered by IP/ host
        self.epList = []

        for ep in cfg.sections():
            # Invalid EP tag ?
            if not cfg.has_option(ep, 'CE_IP') or not cfg.has_option(ep, 'CE_PORT'):
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
            if ep_host == hostName:
                print('EP `{}` has a HOST match ({}), so is valid.'.format(ep, ep_host))
                self.epList.append(ep)
            try:
                # If the ip from EPNAMES matches this IP, it's a valid EP
                if ep_host in socket.gethostbyaddr(hostName)[-1]:
                    print('EP `{}` has an IP match ({}), so is valid.'.format(ep, ep_host))
                    self.epList.append(ep)
            except Exception as e:
                pass

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
                   '{user} {ep} "{ip}:{port}" {sniff} > "{path}/.twister_cache/{ep}_LIVE.log" &'.format(
                    py = sys.executable,
                    path = TWISTER_PATH,
                    user = self.userName,
                    ep = currentEP,
                    ip = epData['ce_ip'],
                    port = epData['ce_port'],
                    sniff = self.snifferEth,
                )

            # Making, or re-using the Central Engine connection
            cePath = '{}:{}'.format(epData['ce_ip'], epData['ce_port'])
            epData['proxy'] = self.createConnection(cePath)

            self.epNames[currentEP] = epData

        del cfg

#

    def registerEPs(self, ce_proxy=None):
        """
        Register EPs to Central Engines.
        """
        if ce_proxy:
            print('Starting Client Service register on `{}`...'.format(ce_proxy))
        else:
            print('Starting Client Service register...')

        print('\n----- Config Data ----')
        pprint(self.epNames, indent=2, width=100)
        print('----------------------\n')

        # Central Engine addrs and the EPs that must be registered for each CE
        proxyEpsList = {}

        for currentEP, epData in self.epNames.iteritems():
            cePath = '{}:{}'.format(epData['ce_ip'], epData['ce_port'])
            # If Central Engine proxy filter is specified, use it
            if ce_proxy and ce_proxy != epData['ce_ip']:
                continue

            proxyEpsList[cePath] = [
                ep for ep in self.epNames
                if self.epNames[ep]['ce_ip'] == self.epNames[currentEP]['ce_ip'] and
                self.epNames[ep]['ce_port'] == self.epNames[currentEP]['ce_port']
              ]

        print('----- Proxy EPs ------')
        pprint(proxyEpsList, indent=2, width=100)
        print('----------------------\n')


        # For each Central Engine address
        for cePath, epNames in proxyEpsList.iteritems():

            if not epNames: continue
            proxy = self.createConnection(cePath)
            # If the connection was not established after X retries... move on!
            if not proxy: continue

            print('Updating client info on CE `{}` :: `{}`.'.format(cePath, epNames))

            # Register all this information on the current Central Engine
            proxy.root.registerEps(epNames)


        print('The Client is registered on all Central Engines.\n')

#

    def run(self):
        """
        Wait forever.
        """
        while 1:
            time.sleep(1)


# # #


class TwisterClientService(rpyc.Service):

    connections = {}
    config = None


    def on_connect(self):
        """
        Runs when a connection is created (to init the service).
        `_conn` is a weakproxy that points to this local service and the remote service.
        `_conn._config` is a dict containing all the information about the connection.
        `_conn.root` is the netref to the Central Engine remote service.
        """
        connid = self._conn._config['connid']
        self.connections[connid] = None

        print('ClientService: New Client connection: `{}`.'.format(connid))


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
        """  """
        global client

        if epname not in client.epNames:
            print('*ERROR* Unknown EP name : `{}` !'.format(epname))
            return False

        time.sleep(1)

        try:
            proxy = client.epNames[epname]['proxy'].root
            last_seen_alive = proxy.getEpVariable(epname, 'last_seen_alive')
        except:
            trace = traceback.format_exc()[34:].strip()
            print('Error: Cannot connect to Central Engine to check the EP! Exception `{}`!'.format(trace))
            return False

        if client.epNames[epname]['pid']:
            print('Error: Process {} is already started for user {}! (pid={})\n'.format(
                  epname, username, client.epNames[epname]['pid']))
            return False

        print('Executing: {}'.format(client.epNames[epname]['exec_str']))
        client.epNames[epname]['pid'] = subprocess.Popen(
                               client.epNames[epname]['exec_str'], shell=True, preexec_fn=os.setsid
                               )

        print('EP `{}` for user `{}` launched in background!\n'.format(epname, glob_config['username']))
        return True


    def exposed_restart_ep(self, epname):
        """  """
        global client

        if epname not in client.epNames:
            print('*ERROR* Unknown EP name : `{}` !'.format(epname))
            return False

        if client.epNames[epname]['pid']:
            try:
                os.killpg(client.epNames[epname]['pid'].pid, 9)
                client.epNames[epname]['pid'] = None
                print('Killing EP `{}` !'.format(epname))
            except:
                trace = traceback.format_exc()[34:].strip()
                print(trace)
                return False

        print('Executing: {}'.format(client.epNames[epname]['exec_str']))
        client.epNames[epname]['pid'] = subprocess.Popen(
                               client.epNames[epname]['exec_str'], shell=True, preexec_fn=os.setsid
                               )

        print('Restarted EP `{}` for user `{}` !\n'.format(epname, glob_config['username']))
        return True


    def exposed_stop_ep(self, epname):
        """  """
        global client

        if epname not in client.epNames:
            print('*ERROR* Unknown EP name : `{}` !'.format(epname))
            return False

        if not client.epNames[epname]['pid']:
            print('Error: EP `{}` is not running !'.format(epname))
            return False

        time.sleep(1)

        try:
            os.killpg(client.epNames[epname]['pid'].pid, 9)
            client.epNames[epname]['pid'] = None
        except:
            trace = traceback.format_exc()[34:].strip()
            print(trace)
            return False

        print('Stopping EP `{}` !'.format(epname))
        return True


# # #


if __name__ == "__main__":

    print('Starting Twister Client...\n')

    # This will read everything from epnames and connect to all CEs
    client = TwisterClient()
    client.run()

    print('Stopping Twister Client.')


# Eof()
