#!/usr/bin/python

# File: start_client.py ; This file is part of Twister.

# version: 2.012

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

import os, sys
import socket
socket.setdefaulttimeout(3)
import cherrypy
import xmlrpclib
import subprocess
import traceback

from time import sleep
from datetime import datetime
from cherrypy import _cptools
from ConfigParser import SafeConfigParser
from json import loads as jsonLoads, dumps as jsonDumps
from socket import gethostname, gethostbyaddr
from thread import start_new_thread

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

def keepalive(service):
    """  """
    print('Keep-Alive process started...')
    service.registerEPs()

    while True:
        ce_down = list()
        for ce in service.proxyList:
            try:
                response = service.proxyList[ce].echo('ping')
            except Exception as e:
                ce_down.append(ce)

        for ce in ce_down:
            _proxy = ce.split(':')
            newProxy = xmlrpclib.ServerProxy('http://{}:EP@{}:{}/'.format(service.username,
                                                                        _proxy[0], _proxy[1]))
            service.proxyList.update([(ce, newProxy), ])
            for currentEP in service.eps:
                if ('{ip}:{p}'.format(ip=service.eps[currentEP]['ce_ip'],
                        p=service.eps[currentEP]['ce_port']) == _proxy):
                    currentEP['proxy'] = newProxy

            sleep(2.8)
            service.registerEPs(ce)

        sleep(0.8)

#

class TwisterClientService(_cptools.XMLRPCController):
    """ Twister Client XML-RPC Service. """

    def __init__(self, username):
        """  """

        print('Twister Client Service init..')
        self.username = username
        self.hostname = gethostname().lower()

        self.snifferEth = None

        self.eps = dict()
        self.proxyList = dict()

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
            self.snifferEth = cfg.get('PACKETSNIFFERPLUGIN', 'ETH_INTERFACE')
        else:
            self.snifferEth = 'eth0'


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
                    if self.hostname in gethostbyaddr(cfg.get(ep, 'EP_HOST'))[0].lower():
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

            if self.proxyList.has_key(_proxy):
                # Re-use Central Engine connection
                newEP['proxy'] = self.proxyList[_proxy]
            else:
                # Create a new Central Engine connection
                newEP['proxy'] = \
                    xmlrpclib.ServerProxy('http://{}:EP@{}:{}/'.format(self.username, newEP['ce_ip'], newEP['ce_port']))
                self.proxyList.update([(_proxy, newEP['proxy']), ])

            newEP['exec_str'] = 'nohup {python} -u {twister_path}/client/executionprocess/ExecutionProcess.py '\
                '{user} {ep} "{ip}:{port}" {sniff} > "{twister_path}/.twister_cache/{ep}_LIVE.log" &'.format(
                    python = sys.executable,
                    twister_path = os.getenv('TWISTER_PATH').rstrip('/'),
                    user = self.username,
                    ep = currentEP,
                    ip = newEP['ce_ip'],
                    port = newEP['ce_port'],
                    sniff = self.snifferEth,
                )
            newEP['pid'] = None
            self.eps.update([(currentEP, newEP), ])


    def registerEPs(self, ce_proxy=None):
        """ Register EPs to Central Engines """

        if ce_proxy:
            print('Starting Client Service register on `{}`...'.format(ce_proxy))
        else:
            print('Starting Client Service register...')

        # List of Central Engine connections
        proxyEpsList = dict()

        for currentEP in self.eps:
            _proxy = '{}:{}'.format(self.eps[currentEP]['ce_ip'], self.eps[currentEP]['ce_port'])
            # If Central Engine proxy filter is specified, use it
            if ce_proxy and ce_proxy != _proxy:
                continue

            if not proxyEpsList.has_key(_proxy):
                proxyEpsList[_proxy] = [
                    ep for ep in self.eps if self.eps[ep]['ce_ip'] == self.eps[currentEP]['ce_ip'] and
                                             self.eps[ep]['ce_port'] == self.eps[currentEP]['ce_port']
                    ]

        unregistered = True

        # Try to register to Central Engine, forever
        while unregistered:
            ce_down = list()
            for currentCE in proxyEpsList:
                try:
                    proxy = self.eps[proxyEpsList[currentCE][0]]['proxy']
                    __proxy = proxy._ServerProxy__host.split('@')[1].split(':')
                except Exception, e:
                    print('CE proxy error: `{}` on `{}`.'.format(e, __proxy))
                    continue

                clientKey = ':{port}'.format(port=self.clientPort)
                try:
                    userCeClientInfo = proxy.getUserVariable(self.username, 'clients')

                    if not userCeClientInfo:
                        userCeClientInfo = {}
                    else:
                        userCeClientInfo = jsonLoads(userCeClientInfo)

                    while True:
                        ceStatus = proxy.getExecStatusAll(self.username)

                        if ceStatus.startswith('invalid'):
                            break
                        elif ceStatus.startswith('stopped'):
                            # Reset user project
                            proxy.resetProject(self.username)
                            print('User project reset.')
                            break
                        else:
                            print('CE on `{}` is running with status `{}`.'.format(
                                  proxy._ServerProxy__host.split('@')[1], ceStatus))
                            print('Waiting to stop ...')
                        sleep(2)

                    for (prxy, eps) in userCeClientInfo.items():
                        for ep in eps:
                            if ep in proxyEpsList[currentCE]:
                                print('Warning: epname {} already registered. Trying to stop..'.format(ep))
                                try:
                                    p = xmlrpclib.ServerProxy('http://{}:{}/twisterclient/'.format(
                                                            prxy.split(':')[0], prxy.split(':')[1]))

                                    try:
                                        last_seen_alive = self.eps[ep]['proxy'].getEpVariable(
                                                            self.username, ep, 'last_seen_alive')
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

                    proxy.registerClient(self.username, userCeClientInfo)
                    unregistered = False

                except Exception as e:
                    ce_down.append(currentCE)
                    print('Error: {er}'.format(er=e))

            if unregistered:
                print('Error: Central Engine is down... will retry...')
            sleep(2)

        for ce in ce_down:
            self.proxyList.pop(ce)

        print('Client is now registered on CE.\n')


    @cherrypy.expose
    def startEP(self, epname, *args, **kwargs):
        """  """

        if not epname in self.eps.keys():
            print('Error: Unknown EP name : `{}` !'.format(epname))
            return False

        sleep(2.4)
        try:
            proxy = self.eps[epname]['proxy']
            last_seen_alive = proxy.getEpVariable(self.username, epname, 'last_seen_alive')
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

        if self.eps[epname]['pid']:
            print('Error: Process {} is already started for user {}! (pid={})\n'.format(
                  epname, username, self.eps[epname]['pid']))
            return False

        print('Executing: {}'.format(self.eps[epname]['exec_str']))
        self.eps[epname]['pid'] = subprocess.Popen(
                                  self.eps[epname]['exec_str'], shell=True, preexec_fn=os.setsid)
        print('EP `{}` for user `{}` launched in background!\n'.format(epname, self.username))

        return True


    @cherrypy.expose
    def stopEP(self, epname, *args, **kwargs):
        """  """

        if not epname in self.eps.keys():
            print('Error: Unknown EP name : `{}` !'.format(epname))
            return False

        if not self.eps[epname]['pid']:
            print('Error: EP `{}` is not running !'.format(epname))
            return False

        sleep(2.4)

        try:
            os.killpg(self.eps[epname]['pid'].pid, 9)
            self.eps[epname]['pid'] = None
        except:
            trace = traceback.format_exc()[34:].strip()
            print(trace)
            return False

        print('Stopping EP `{}` !'.format(epname))
        return True


    @cherrypy.expose
    def restartEP(self, epname, *args, **kwargs):
        """  """

        if not epname in self.eps.keys():
            print('Error: Unknown EP name : `{}` !'.format(epname))
            return False

        if self.eps[epname]['pid']:
            try:
                os.killpg(self.eps[epname]['pid'].pid, 9)
                self.eps[epname]['pid'] = None
                print('Killing EP `{}` !'.format(epname))
            except:
                trace = traceback.format_exc()[34:].strip()
                print(trace)
                return False

        print('Executing: {}'.format(self.eps[epname]['exec_str']))
        self.eps[epname]['pid'] = subprocess.Popen(
                                  self.eps[epname]['exec_str'], shell=True, preexec_fn=os.setsid)
        print('Restarted EP `{}` for user `{}` !\n'.format(epname, self.username))

        return True

#

if __name__ == "__main__":

    # Run client service
    service = TwisterClientService(username)

    # Find firs free port in range ...
    connectionEstablished = False
    minport, maxport = 4444, 4488
    clientPort = minport

    while clientPort < maxport:
        try:
            socket.create_connection(('0.0.0.0', clientPort), 2)
            print('Client warning, the port `{}` is taken!'.format(clientPort))
            clientPort += 1
        except Exception as e:
            connectionEstablished = True
            break

    if not connectionEstablished:
        print('Cound not find any free port in range {} - {} !'.format(minport, maxport))
        exit(1)

    print('Client will start on : `0.0.0.0:{}`.'.format(clientPort))

    service.clientPort = clientPort


    # Config
    conf = {'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': clientPort,
            'engine.autoreload.on': False,
            'log.screen': False
            }
        }

    start_new_thread(keepalive, (service, ))

    # Start !
    cherrypy.quickstart(service, '/twisterclient/', config=conf)

#
