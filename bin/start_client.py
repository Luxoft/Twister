#!/usr/bin/python

# File: start_client.py ; This file is part of Twister.

# version: 3.000

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
# This file will register ALL Execution Processes that are enabled,
# from file `twister/config/epname.ini` !
# To be able to start the packet sniffer, this must run as ROOT.


import sys
import os
import traceback
import socket
import subprocess

import xmlrpclib

from time import sleep
from datetime import datetime

from thread import start_new_thread

from ConfigParser import SafeConfigParser

from json import loads as jsonLoads, dumps as jsonDumps

from rpyc import Service as rpycService
from rpyc.utils.server import ThreadedServer as rpycThreadedServer


#

if not sys.version.startswith('2.7'):
    print('Python version error! The client must run on Python 2.7!')
    exit(1)

def userHome(user):
    """ Return user home path for all kind of users """
    return subprocess.check_output('echo ~' + user, shell=True).strip()

try:
    username = os.getenv('USER')
    if username=='root':
        username = os.getenv('SUDO_USER')
except:
    print('Cannot guess user name for this Execution Process! Exiting!')
    exit(1)

# Twister path environment
os.environ['TWISTER_PATH'] = userHome(username).rstrip('/') +os.sep+ 'twister/'

#


def TwisterClientServiceConfigurationParse(conn):
    """  """

    while not conn.active:
        sleep(0.8)

    clientPort = conn.port

    response = dict()

    print('Twister Client Service init..')

    response.update([('username', username),])
    response.update([('hostname', socket.gethostname().lower()),])

    response.update([('clientPort', clientPort), ])

    response.update([('snifferEth', None),])

    response.update([('eps', dict()),])
    response.update([('proxyList', dict()),])

    # Close all sniffer and ep instaces and parse eps
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


    cfg = SafeConfigParser()
    cfg.read(os.getenv('TWISTER_PATH') + '/config/epname.ini')

    # sniffer config
    if (cfg.has_option('PACKETSNIFFERPLUGIN', 'EP_HOST') and
        cfg.get('PACKETSNIFFERPLUGIN', 'ENABLED') == '1'):
        response.update([('snifferEth', cfg.get('PACKETSNIFFERPLUGIN', 'ETH_INTERFACE')),])
    else:
        response.update([('snifferEth', 'eth0'),])


    allow_any_host = True
    for ep in cfg.sections():
        # check if the config has option EP_HOST and is
        # not commented out and it coantains an IP address
        if cfg.has_option(ep, 'EP_HOST'):
            host_value = (cfg.get(ep, 'EP_HOST'))
            if host_value:
                allow_any_host = False

    # All sections that have an option CE_IP, are EP names
    eps = []

    for ep in cfg.sections():
        if cfg.has_option(ep, 'CE_IP') and not allow_any_host:
            try:
                if response['hostname'] in socket.gethostbyaddr(cfg.get(ep, 'EP_HOST'))[0].lower():
                    eps.append(ep)
            except Exception as e:
                pass
        elif cfg.has_option(ep, 'CE_IP') and allow_any_host:
            eps.append(ep)
    print('Found `{}` EPs: `{}`.\n'.format(len(eps), ', '.join(eps)))

    if not eps:
        raise Exception('No EPS found!')

    # Generate list of EPs and connections
    for currentEP in eps:
        newEP = {}
        newEP['ce_ip'] = cfg.get(currentEP, 'CE_IP')
        newEP['ce_port'] = cfg.get(currentEP, 'CE_PORT')
        _proxy = '{ip}:{port}'.format(ip=newEP['ce_ip'], port=newEP['ce_port'])

        if response['proxyList'].has_key(_proxy):
            # Re-use Central Engine connection
            newEP['proxy'] = response['proxyList'][_proxy]
        else:
            # Create a new Central Engine connection
            newEP['proxy'] = \
                xmlrpclib.ServerProxy('http://{}:EP@{}:{}/'.format(response['username'], newEP['ce_ip'], newEP['ce_port']))
            response['proxyList'].update([(_proxy, newEP['proxy']), ])

        newEP['exec_str'] = 'nohup {python} -u {twister_path}/client/executionprocess/ExecutionProcess.py '\
            '{user} {ep} "{ip}:{port}" {sniff} > "{twister_path}/.twister_cache/{ep}_LIVE.log" &'.format(
                python = sys.executable,
                twister_path = os.getenv('TWISTER_PATH').rstrip('/'),
                user = response['username'],
                ep = currentEP,
                ip = newEP['ce_ip'],
                port = newEP['ce_port'],
                sniff = response['snifferEth'],
            )
        newEP['pid'] = None
        response['eps'].update([(currentEP, newEP), ])

    response = RegisterEPs(response)

    conn.service.config = response
    print('|||||||||config|||||||||')
    print(repr(conn.service.config))
    print('||||||||||||||||||||||||')
    return


def RegisterEPs(config, ce_proxy=None):
    """ Register EPs to Central Engines """

    if ce_proxy:
        print('Starting Client Service register on `{}`..'.format(ce_proxy))
    else:
        print('Starting Client Service register..')

    # List of Central Engine connections
    proxyEpsList = {}

    for currentEP in config['eps']:
        _proxy = '{}:{}'.format(config['eps'][currentEP]['ce_ip'],
                                config['eps'][currentEP]['ce_port'])
        # If Central Engine proxy filter is specified, use it
        if ce_proxy and ce_proxy != _proxy:
            continue

        if not proxyEpsList.has_key(_proxy):
            proxyEpsList[_proxy] = [
                ep for ep in config['eps']
                if config['eps'][ep]['ce_ip'] == config['eps'][currentEP]['ce_ip'] and
                config['eps'][ep]['ce_port'] == config['eps'][currentEP]['ce_port']
            ]

    unregistered = True
    retries = 0
    maxRetries = 8

    # Try to register to Central Engine, forever
    while unregistered:
        for currentCE in proxyEpsList:
            try:
                proxy = config['eps'][proxyEpsList[currentCE][0]]['proxy']
                __proxy = proxy._ServerProxy__host.split('@')[1].split(':')
                socket.create_connection((__proxy[0], __proxy[1]), 2)
            except Exception, e:
                print('CE proxy error: `{}` on `{}`.'.format(e, __proxy))
                continue

            clientKey = '{port}'.format(port=config['clientPort'])
            try:
                userCeClientInfo = proxy.getUserVariable(config['username'], 'clients')

                if not userCeClientInfo:
                    userCeClientInfo = {}
                else:
                    userCeClientInfo = jsonLoads(userCeClientInfo)

                while True:
                    ceStatus = proxy.getExecStatusAll(config['username'])

                    if ceStatus.startswith('invalid'):
                        break
                    elif ceStatus.startswith('stopped'):
                        # Reset user project
                        proxy.resetProject(config['username'])
                        print('User project reset.')
                        break
                    else:
                        print('CE on `{}` is running wi11257th status `{}`.'.format(
                              proxy._ServerProxy__host.split('@')[1], ceStatus))
                        print('Waiting to stop..')
                    sleep(2)

                for (prxy, eps) in userCeClientInfo.items():
                    for ep in eps:
                        if ep in proxyEpsList[currentCE]:
                            print('Warning: epname {} already registered. Trying to stop..'.format(ep))
                            try:
                                p = xmlrpclib.ServerProxy('http://{}:{}/twisterclient/'.format(
                                                        prxy.split(':')[0], prxy.split(':')[1]))

                                try:
                                    last_seen_alive = config['eps'][ep]['proxy'].getEpVariable(
                                                        config['username'], ep, 'last_seen_alive')
                                    now_dtime = datetime.today()
                                    if last_seen_alive:
                                        diff = now_dtime - datetime.strptime(last_seen_alive,
                                                                        '%Y-%m-%d %H:%M:%S')
                                        if diff.seconds <= 2.4:
                                            proxyEpsList[currentCE].pop(proxyEpsList[currentCE].index(ep))
                                            print('Warning: epname {} is running. Will not register.'.format(ep))
                                    else:
                                        p.stopEP(ep)
                                        userCeClientInfo[prxy].pop(userCeClientInfo[prxy].index(ep))
                                        if not userCeClientInfo[prxy]:
                                            userCeClientInfo.pop(prxy)
                                        print('Warning: epname {} stoped. Will register.'.format(ep))
                                except Exception as e:
                                    pass
                            except Exception as e:
                                pass

                if not proxyEpsList[currentCE]:
                    continue

                userCeClientInfo.update([(clientKey, proxyEpsList[currentCE]), ])
                userCeClientInfo = jsonDumps(userCeClientInfo)

                proxy.registerClient(config['username'], userCeClientInfo)
                unregistered = False

            except Exception as e:
                config['proxyList'].pop(currentCE)
                print('Error: {er}'.format(er=e))

        if unregistered:
            if retries > maxRetries:
                print('Error: Central Engine is down..')
                return False
            retries += 1
            print('Error: Central Engine is down.. will retry..')
        sleep(2)

    print('Client is now registered on CE.\n')

    return config




class TwisterClientService(rpycService):

    connections = dict()
    config = None


    def on_connect(self):
        """ runs when a connection is created (to init the serivce, if needed) """

        client_addr = self._conn._config['endpoints'][1]
        self.connections.update([('{ip}:{port}'.format(ip=client_addr[0], port=client_addr[1]), None), ])

        print('New connection from `{ip}:{port}`.'.format(ip=client_addr[0], port=client_addr[1]))


    def on_disconnect(self):
        """ runs when the connection has already closed (to finalize the service, if needed) """
        print('||||||||||||||||||||||||||||||||||||||||||||||||||')
        print(self._conn._config['endpoints'])
        print('||||||||||||||||||||||||||||||||||||||||||||||||||')
        client_addr = self._conn._config['endpoints'][1]
        try:
            proxy = self.connections.pop('{ip}:{port}'.format(ip=client_addr[0], port=client_addr[1]))
            self.config = RegisterEPs(self.config, proxy)
        except Exception as e:
            print('On disconnect error: {er}'.format(er=e))

        print('Disconnected from `{}`.'.format(ip=client_addr[0], port=client_addr[1]))

        if not self.connections:
            self.config = RegisterEPs(self.config)


    def exposed_hello(self, proxy):
        """  """

        client_addr = self._conn._config['endpoints'][1]
        try:
            self.connections.update([('{ip}:{port}'.format(ip=client_addr[0], port=client_addr[1]),
                                                                                        proxy), ])
        except Exception as e:
            print('Hello error: {er}'.format(er=e))


    def exposed_start_ep(self, epname):
        """  """

        if not self.config:
            print('Error: no config')
            return False

        if not epname in self.config['eps'].keys():
            print('Error: Unknown EP name : `{}` !'.format(epname))
            return False

        sleep(2.4)
        try:
            proxy = self.config['eps'][epname]['proxy']
            last_seen_alive = proxy.getEpVariable(self.config['username'], epname, 'last_seen_alive')
        except:
            print('Error: Cannot connect to Central Engine to check the EP!\n')
            trace = traceback.format_exc()[34:].strip()
            print(trace)
            return False

        now_dtime = datetime.today()

        if last_seen_alive:
            diff = now_dtime - datetime.strptime(last_seen_alive, '%Y-%m-%d %H:%M:%S')
            if diff.seconds < 2.5:
                print('Error: Process {} is already started for user {}! (ping={} sec)\n'.format(
                       epname, username, diff.seconds))
                return False

        if self.config['eps'][epname]['pid']:
            print('Error: Process {} is already started for user {}! (pid={})\n'.format(
                  epname, username, self.config['eps'][epname]['pid']))
            return False

        print('Executing: {}'.format(self.config['eps'][epname]['exec_str']))
        self.config['eps'][epname]['pid'] = subprocess.Popen(
                            self.config['eps'][epname]['exec_str'], shell=True, preexec_fn=os.setsid)
        print('EP `{}` for user `{}` launched in background!\n'.format(epname, self.config['username']))

        return True


    def exposed_restart_ep(self, epname):
        """  """

        if not self.config:
            print('Error: no config')
            return False

        if not epname in self.config['eps'].keys():
            print('Error: Unknown EP name : `{}` !'.format(epname))
            return False

        if self.config['eps'][epname]['pid']:
            try:
                os.killpg(self.config['eps'][epname]['pid'].pid, 9)
                self.config['eps'][epname]['pid'] = None
                print('Killing EP `{}` !'.format(epname))
            except:
                trace = traceback.format_exc()[34:].strip()
                print(trace)
                return False

        print('Executing: {}'.format(self.config['eps'][epname]['exec_str']))
        self.config['eps'][epname]['pid'] = subprocess.Popen(
                            self.config['eps'][epname]['exec_str'], shell=True, preexec_fn=os.setsid)
        print('Restarted EP `{}` for user `{}` !\n'.format(epname, self.config['username']))

        return True


    def exposed_stop_ep(self, epname):
        """  """

        if not self.config:
            print('Error: no config')
            return False

        if not epname in self.config['eps'].keys():
            print('Error: Unknown EP name : `{}` !'.format(epname))
            return False

        if not self.config['eps'][epname]['pid']:
            print('Error: EP `{}` is not running !'.format(epname))
            return False

        sleep(2.4)

        try:
            os.killpg(self.config['eps'][epname]['pid'].pid, 9)
            self.config['eps'][epname]['pid'] = None
        except:
            trace = traceback.format_exc()[34:].strip()
            print(trace)
            return False
        print('Stopping EP `{}` !'.format(epname))

        return True








if __name__ == "__main__":

    # find firs free port in range ..
    minport, maxport = 4444, 4488
    clientPort = minport

    while clientPort <= maxport:
        try:
            _rpycThreadedServer = rpycThreadedServer(TwisterClientService, port=clientPort)

            print('Client will start on : `0.0.0.0:{}`.'.format(clientPort))

            start_new_thread(TwisterClientServiceConfigurationParse, (_rpycThreadedServer, ))

            _rpycThreadedServer.start()
            break
        except Exception as e:
            print(e)
            print('Client warning, the port `{}` is taken!'.format(clientPort))
            clientPort += 1

            if clientPort > maxport:
                print('Cound not find any free port in range {} - {} !'.format(minport, maxport))
                exit(1)

    print('End.')
    exit(0)

