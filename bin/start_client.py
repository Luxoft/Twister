#!/usr/bin/env python2.7

# File: start_client.py ; This file is part of Twister.

# version: 3.018

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
import re
import shutil
import time
import signal
import socket
socket.setdefaulttimeout(5)
try:
    import thread
except Exception:
    import _thread as thread
import traceback
import platform
import subprocess
import json
import copy
import rpyc
import datetime
import urlparse

from pprint import pformat
from rpyc import BgServingThread
try:
    from ConfigParser import SafeConfigParser
except Exception:
    from configparser import SafeConfigParser


def logPrint(msg):
    """ Prints message + date-time stamp """
    dateTag = datetime.datetime.now().strftime("%Y-%b-%d %H-%M-%S")
    print('{}\t{}'.format(dateTag, msg))

def user_home(user):
    """ Return user home path for all kind of users """
    if platform.system().lower() == 'windows':
        return os.getenv('HOME')
    else:
        return subprocess.check_output('echo ~' + user, shell=True).strip().decode('utf')

try:
    USER_NAME = os.getenv('USER') or os.getenv('USERNAME')
    if USER_NAME == 'root':
        USER_NAME = os.getenv('SUDO_USER') or USER_NAME
    logPrint('Hello username `{}`!'.format(USER_NAME))
except Exception:
    USER_NAME = ''
if not USER_NAME:
    logPrint('Cannot guess user name for the Twister Client! Exiting!')
    exit(1)


# Twister path environment
TWISTER_PATH = user_home(USER_NAME).rstrip('/') + '/twister'
os.environ['TWISTER_PATH'] = TWISTER_PATH

PS_SNIFFER = 'ps ax | grep /bin/start_packet_sniffer.py  | grep "\\-u {}" '
PS_EPS = 'ps ax | grep /executionprocess/ExecutionProcess.py  | grep "\\-u {}" '


# # #


class TwisterClient(object):
    """ client class """
    def __init__(self):

        self.user_name = USER_NAME
        self.host_name = socket.gethostname().lower()
        self.ep_list = []
        self.ep_names = {}
        self.proxy_dict = {}
        self.proxy_lock = thread.allocate_lock()
        # Kill all sniffers and EPs
        self.kill_all()
        # Parse and register EPs
        self.parse_configuration()
        self.register_eps()

#

    def _kill(self, lines, descr=''):
        """
        Helper function.
        """
        for line in lines.strip().splitlines():
            line = line.strip().decode('utf').split()
            pid = int(line[0])
            del line[1:4]
            if '/bin/sh' in line and '-c' in line:
                continue
            logPrint('Killing ugly zombie {} `{}`'.format(descr, ' '.join(line)))
            try:
                os.kill(pid, 9)
            except Exception:
                pass

#

    def kill_all(self):
        """
        Close all Sniffers and EPs for this user.
        """
        pids = subprocess.check_output(PS_SNIFFER.format(USER_NAME), shell=True)
        self._kill(pids, 'Sniffer')

        pids = subprocess.check_output(PS_EPS.format(USER_NAME), shell=True)
        self._kill(pids, 'EP')

#

    def _create_conn(self, ce_ip, ce_port, ep_names, debug=False):
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
            logPrint('Client Debug: Connected to CE at `{}:{}`...'.format(ce_ip, ce_port))
        except Exception as e:
            if debug:
                logPrint('*ERROR* Cannot connect to CE path `{}:{}`! '\
                    'Exception: `{}`!'.format(ce_ip, ce_port, e))
            return None

        # Authenticate on RPyc server
        try:
            check = proxy.root.login(self.user_name, 'EP')
            if check:
                logPrint('Client Debug: Authentication successful!')
        except Exception as e:
            check = False

        if not check:
            if debug:
                logPrint('*ERROR* Cannot authenticate on CE path `{}:{}`!'.format(ce_ip, ce_port))
            return None

        # Say Hello and Register all EPs on the current Central Engine
        if ep_names:
            try:
                proxy.ping(data='Hello', timeout=3)
                # Call the user status to create the User Project
                s = proxy.root.get_user_variable('user_roles')
                if not s:
                    raise Exception('Cannot get roles for user `{}`!'.format(self.user_name))
                # Fire up the User Service
                proxy.root.read_file('~/twister/config/fwmconfig.xml')
            except Exception as e:
                logPrint('Exception: `{}`'.format(e))
                check = False

            try:
                proxy.root.hello('client', {'eps': ep_names})
                logPrint('Client Debug: Register EPs successful!')
            except Exception as e:
                logPrint('Exception: `{}`'.format(e))
                check = False

        if not check:
            if debug:
                logPrint('*ERROR* Cannot send hello on CE path `{}:{}`!'.format(ce_ip, ce_port))
            return None

        BgServingThread(proxy)
        return proxy

#

    def _create_conn_long(self, ce_path, ep_names):
        """
        Create connection to Central Engine, return the connection and
        auto-save it in the Proxy Dict.
        """
        proxy = None
        ce_ip, ce_port = ce_path.split(':')
        ce_port = int(ce_port)

        # Transform XML-RPC port into RPyc Port; RPyc port = XML-RPC port + 10 !
        ce_port += 10

        with self.proxy_lock:
            # Try to re-use the old Central Engine connection
            proxy = self.proxy_dict.get(ce_path, None)

            if proxy:
                # If the hello works, the connection is just fine
                try:
                    proxy.root.echo('ping')
                    logPrint('Connection to Central Engine at `{}` is ok!'.format(ce_path))
                    return True
                # If the hello doesn't work, it means the connection was lost/ destroyed
                except Exception:
                    proxy = None

        err_msg = True
        last_time = time.time()
        # When to print the next Warning that this thread is trying to reconnect
        time_diff = 30

        while True:
            if not proxy:
                # Try creating a new Central Engine connection.
                proxy = self._create_conn(ce_ip, ce_port, ep_names, err_msg)
            else:
                break

            # Save the connection, or the failed result, in a thread safe mode.
            with self.proxy_lock:
                self.proxy_dict[ce_path] = proxy

            if not proxy:
                if err_msg:
                    logPrint('*ERROR* Cannot connect to Central Engine at `{}`! '\
                        'Will Retry forever and ever...'.format(ce_path))
                    err_msg = False
                elif time.time() > last_time + time_diff:
                    logPrint('*ERROR* Still trying to connect to Central Engine at `{}`...'.format(ce_path))
                    last_time = time.time()
                # Wait a little, before trying to connect again.
                time.sleep(2)
            else:
                break

        return True

#

    def lazy_register(self, ce_path, ep_names):
        """
        Register EP Names on Central Engine.
        Used in a thread to try and connect to the required Central Engine.
        """
        logPrint('### Will REGISTER EPs on CE `{}` :: `{}` ###'.format(ce_path, ep_names))
        # Cleanup all zombie processes
        self.kill_all()
        # This operation might take a while!...
        self._create_conn_long(ce_path, ep_names)
        logPrint('### Success REGISTER EPs on CE `{}` :: `{}` ###'.format(ce_path, ep_names))

#

    def _reload_eps(self, cfg):
        """
        Use the config from EPNAMES to create a list of EPs, filtered by IP and Host.
        """
        # Sniffer config
        snifferEth = None
        if (cfg.has_option('PACKETSNIFFERPLUGIN', 'ETH_INTERFACE') and
            cfg.get('PACKETSNIFFERPLUGIN', 'ENABLED') == '1'):
            snifferEth = cfg.get('PACKETSNIFFERPLUGIN', 'ETH_INTERFACE')
        else:
            snifferEth = 'eth0'

        TwisterClientService.snifferEth = snifferEth

        logPrint('Sniffer eth = `{}`.'.format(snifferEth))
        logPrint('Building the EP list for this machine...')

        # This will be a temporary list of valid EP names, filtered by Enabled/ IP/ host
        ep_list = []

        # Cycle all EPs
        for ep in cfg.sections():
            # EP disabled ?
            if cfg.has_option(ep, 'ENABLED'):
                if cfg.get(ep, 'ENABLED') in ['0', 'false']:
                    logPrint('EP `{}` is disabled.'.format(ep))
                    continue
            # Invalid EP tag ?
            if not cfg.has_option(ep, 'CE_IP') or not cfg.has_option(ep, 'CE_PORT'):
                logPrint('Section `{}` is not a valid EP, because it needs '\
                    'CE_IP and CE_PORT.'.format(ep))
                continue
            # If this EP does NOT have a HOST filter, it's a valid EP
            if not cfg.has_option(ep, 'EP_HOST'):
                logPrint('EP `{}` doesn\'t have a HOST filter, so is valid.'.format(ep))
                ep_list.append(ep)
                continue
            # If the HOST filter is empty, it's a valid EP
            if not cfg.get(ep, 'EP_HOST'):
                logPrint('EP `{}` has an empty HOST filter, so is valid.'.format(ep))
                ep_list.append(ep)
                continue

            # This is an EP with EP HOST filter!
            ep_host = cfg.get(ep, 'EP_HOST')
            # If the host from EPNAMES matches, it's a valid EP
            if ep_host == self.host_name:
                logPrint('EP `{}` has a HOST match ({}), so is valid.'.format(ep, ep_host))
                ep_list.append(ep)
            try:
                # If the ip from EPNAMES matches this IP, it's a valid EP
                if ep_host in socket.gethostbyaddr(self.host_name)[-1]:
                    logPrint('EP `{}` has an IP match ({}), so is valid.'.format(ep, ep_host))
                    ep_list.append(ep)
            except Exception:
                pass

            logPrint('EP `{}` doesn\'t match with required HOST `{}`, '\
                'so is ignored.'.format(ep, ep_host))

        # Sort and eliminate duplicates
        self.ep_list = sorted(set(ep_list))

        logPrint('Found `{}` EPs: {}.'.format(len(self.ep_list), self.ep_list))
        return self.ep_list

#

    def add_ep(self, epname, ce_ip, ce_port):
        """
        Shortcut function to add a new EP in the EP structure.
        """
        # A lot of meta-data for current EP
        epData = {}
        epData['pid'] = None
        epData['ce_ip'] = ce_ip
        # set the ce_port; it can be an int or a string so we have to check
        if isinstance(ce_port, int):
            epData['ce_port'] = ce_port
        else:
            if ';' in ce_port:
                ce_port = ce_port.split(';')[0]
            epData['ce_port'] = ce_port.strip()

        epData['exec_str'] = 'nohup {py} -u {path}/client/executionprocess/ExecutionProcess.py '\
                '-u {user} -e {ep} -s {ip}:{port} > "{path}/.twister_cache/{ep}_LIVE.log" '.format(
                py = sys.executable,
                path = TWISTER_PATH,
                user = self.user_name,
                ep = epname,
                ip = epData['ce_ip'],
                port = epData['ce_port']
            )

        self.ep_names[epname] = epData
        return True

#

    def parse_configuration(self):
        """
        Parse the EPNAMES.ini and prepare to register the Execution Processes.
        If the file is not found, create a single `hostname_auto` EP on localhost.
        If the file is found but there are no EPs, create a single `hostname_auto` EP,
        on AUTO_CE_IP and AUTO_CE_PORT.
        """
        # EPs file
        epnames = '{}/config/epname.ini'.format(TWISTER_PATH)

        if not os.path.isfile(epnames):
            # Register the Hostname + Auto. The Central Engine MUST be on localhost:8000
            logPrint('Cannot find `epname.ini` file! Will register `{}` EP on '\
                ' `localhost:8000`...'.format(self.host_name + '_auto'))
            self.add_ep(self.host_name + '_auto', '127.0.0.1', 8000)
            return True

        # The Config Parser instance
        cfg = SafeConfigParser()
        cfg.read(epnames)

        ep_list = self._reload_eps(cfg)

        # Use the auto ?
        if not ep_list:
            if cfg.has_option('AUTO', 'AUTO_CE_IP') and cfg.has_option('AUTO', 'AUTO_CE_PORT'):
                auto_ip = cfg.get('AUTO', 'AUTO_CE_IP')
                auto_port = cfg.get('AUTO', 'AUTO_CE_PORT')
                logPrint('No EPs found, but found [AUTO] section with AUTO_CE_IP and AUTO_CE_PORT.'
                      '\n\tWill register `{}` EP on Central Engine `{}:{}`...'.format(
                        self.host_name + '_auto', auto_ip, auto_port))
                self.add_ep(self.host_name + '_auto', auto_ip, auto_port)
                return True
            else:
                logPrint('No EPs found and cannot find [AUTO] section with AUTO_CE_IP and AUTO_CE_PORT!'
                      '\n\tThis client will hang forever...')
                return False

        # Generate meta-data for each EP + the Anonymous EP
        for currentEP in ep_list:
            # Incomplete EP tag ?
            if not cfg.has_option(currentEP, 'CE_IP') or not cfg.has_option(currentEP, 'CE_PORT'):
                continue
            # Register the Hostname + EP name
            self.add_ep(self.host_name + '_' + currentEP,
                    cfg.get(currentEP, 'CE_IP'),
                    cfg.get(currentEP, 'CE_PORT'))

        return True

#

    def register_eps(self):
        """
        Register EPs to Central Engines.
        The function is called on START and on DISCONNECT from a Central Engine.
        """
        addr = ['127.0.0.1', 'localhost']
        host_name = socket.gethostname()
        addr.append(host_name)
        try:
            addr.append(socket.gethostbyaddr(host_name)[-1][0])
        except Exception:
            pass

        logPrint('Starting Client Service register on `{}`...'.format(addr))

        # print('\n----- Config Data ----')
        # pformat(self.ep_names, indent=2, width=100) # DEBUG !
        # print('----------------------\n')

        # Central Engine addrs and the EPs that must be registered for each CE
        epsToRegister = {}

        for currentEP, epData in self.ep_names.items():
            ce_path = '{}:{}'.format(epData['ce_ip'], epData['ce_port'])
            epsToRegister[ce_path] = [
                ep for ep in self.ep_names
                if self.ep_names[ep]['ce_ip'] == self.ep_names[currentEP]['ce_ip'] and
                self.ep_names[ep]['ce_port'] == self.ep_names[currentEP]['ce_port']
              ]

        logPrint('------- EPs to register -------')
        logPrint(pformat(epsToRegister, indent=2, width=100))
        logPrint('-------------------------------')

        # For each Central Engine address
        for ce_path, ep_names in epsToRegister.items():
            if not ep_names:
                continue
            thread.start_new_thread(self.lazy_register, (ce_path, ep_names))

        logPrint('Register EPs function finished.'\
              '\n\tIf not all CE connections are made, they will be created asynchronously.\n')

#

    def run(self):
        """
        Blocked forever and ever.
        """
        while 1:
            time.sleep(1)


# # #


class TwisterClientService(rpyc.Service):
    """ start e service client """
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
        connid = self._conn._config['connid']

        try:
            self.connections.pop(connid)
            CLIENT.register_eps()
        except Exception:
            trace = traceback.format_exc()[34:].strip()
            logPrint('ClientService: Disconnect Error: `{}`!'.format(trace))


    def exposed_echo(self, msg):
        """
        For testing connection
        """
        if msg != 'ping':
            logPrint(':: {}'.format(msg))
        return 'Echo: {}'.format(msg)


    def exposed_hello(self, proxy):
        """
        The first function called.
        """
        connid = self._conn._config['connid']

        try:
            self.connections[connid] = proxy
            logPrint('ClientService: Hello `{}`!'.format(proxy))
            return True
        except Exception:
            trace = traceback.format_exc()[34:].strip()
            logPrint('ClientService: Error on Hello: `{}`.'.format(trace))
            return False


    def exposed_add_ep(self, epname, ce_ip, ce_port):
        """
        Add a new EP in the EP structure.
        """
        try:
            CLIENT.add_ep(self, epname, ce_ip, ce_port)
            return True
        except Exception:
            trace = traceback.format_exc()[34:].strip()
            logPrint('ClientService: Error on Add EP: `{}`.'.format(trace))
            return False


    def exposed_start_ep(self, epname):
        """
        Start 1 EP.
        """
        if epname not in CLIENT.ep_names:
            logPrint('*ERROR* Cannot start! Unknown EP name : `{}` !'.format(epname))
            return False

        tproc = CLIENT.ep_names[epname].get('pid')

        if tproc:
            logPrint('Error: Process {} is already started for user {}! (proc={})'.format(epname, USER_NAME, tproc))
            return False

        exec_str = CLIENT.ep_names[epname]['exec_str']
        logPrint('Executing: `{}`.'.format(exec_str))

        try:
            tproc = subprocess.Popen(exec_str, shell=True, preexec_fn=os.setsid)
            CLIENT.ep_names[epname]['pid'] = tproc
        except Exception:
            trace = traceback.format_exc()[34:].strip()
            logPrint('ClientService: Error on Start EP: `{}`.'.format(trace))
            return False

        logPrint('EP `{}` for user `{}` launched in background!'.format(epname, USER_NAME))
        return True


    def exposed_stop_ep(self, epname):
        """
        Stop 1 EP.
        """
        if epname not in CLIENT.ep_names:
            logPrint('*ERROR* Cannot stop! Unknown EP name : `{}` !'.format(epname))
            return False

        tproc = CLIENT.ep_names[epname].get('pid')
        if not tproc:
            return False

        logPrint('Preparing to stop EP `{}`...'.format(epname))
        PID = tproc.pid

        try:
            os.killpg(PID, signal.SIGINT)
            time.sleep(0.5)
            os.killpg(PID, 9)
            CLIENT.ep_names[epname]['pid'] = None
        except Exception:
            trace = traceback.format_exc()[34:].strip()
            logPrint('ClientService: Error on Stop EP: `{}`.'.format(trace))
            return False

        # Normally, this will Never execute, but kill the stubborn zombies, just in case
        Tries = 3
        while Tries > 0:
            ps = subprocess.check_output('ps ax | grep ExecutionProcess.py | grep -u {} '\
                ' | grep -e {}'.format(USER_NAME, epname), shell=True)
            ps = ps.strip().splitlines()[:-2] # Ignore the last 2 lines (the grep and shell=True)
            # If all the processes are dead, it's ok
            if not ps:
                break

            # Another small delay, before killing the zombie
            time.sleep(0.25)
            Tries -= 1

            for line in ps:
                li = line.strip().split()
                PID = li[0]
                del li[1:4]
                logPrint('Killing `{}`'.format(' '.join(li)))
                try:
                    os.kill(int(PID), 9)
                    CLIENT.ep_names[epname]['pid'] = None
                except Exception:
                    trace = traceback.format_exc()[34:].strip()
                    logPrint('ClientService: Error on Stop EP: `{}`.'.format(trace))
                    # return False # No need to exit

        CLIENT.ep_names[epname]['pid'] = None
        logPrint('Stopped EP `{}`! (pid = {})'.format(epname, PID))
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
        command = ['python', '-u', scriptPath, '-u', USER_NAME,
                        '-i', snifferEth, '-t', TWISTER_PATH]
        with open(logPath, 'w+b') as logFile:
            subprocess.Popen(command, stdout=logFile, stderr=logFile)

        return True


    def exposed_stop_sniffer(self):
        """ stop sniffer """

        pipe = subprocess.Popen('ps ax | grep start_packet_sniffer.py',
                                shell=True, stdout=subprocess.PIPE)
        for line in pipe.stdout.read().splitlines():
            try:
                os.kill(int(line.split()[0]), 9)
            except Exception:
                pass
        del pipe
        return True


    def exposed_save_suts(self, sut_list):
        """ save sut to file """

        logPrint('Received save SUTS {}'.format(sut_list))
        # Save sut files
        for (name, sut) in sut_list:
            try:
                logPrint('Save SUT Name {}'.format(name))
                sutsPath = self._conn.root.get_user_variable('sut_path')
                if not sutsPath:
                    sutsPath = '{}/config/sut/'.format(TWISTER_PATH)
                childPath = os.path.join(sutsPath, name)

                if os.path.isfile(childPath):
                    with open(childPath, 'r') as f:
                        sut = json.loads(json.dumps(copy.deepcopy(sut)))
                        f_content = json.load(f)
                        diff = set(o for o in set(sut.keys()).intersection(f_content) if f_content[o] != sut[o])
                        if diff:
                            with open(childPath, 'w') as _f:
                                json.dump(sut, _f, indent=4)
                else:
                    with open(childPath, 'w') as _f:
                        json.dump(sut, _f, indent=4)
            except IOError:
                return "Cannot save SUT file"
            except Exception as e:
                logPrint('Save SUTS exception {}'.format(e))
                return e

        return True


    def exposed_get_suts(self):
        """ get all suts from files """

        suts = list()
        try:
            sutsPath = self._conn.root.get_user_variable('sut_path')
            if not sutsPath:
                sutsPath = '{}/config/sut/'.format(TWISTER_PATH)
            sutPaths = [p for p in os.listdir(sutsPath) if os.path.isfile(os.path.join(sutsPath, p))
                        and p.split('.')[-1] == 'json']

            for sutPath in sutPaths:
                try:
                    sutName = '.'.join(['.'.join(sutPath.split('.')[:-1]  + ['user'])])
                    with open(os.path.join(sutsPath, sutPath), 'r') as f:
                        suts.append((sutName, json.load(f)))
                except Exception:
                    traceback.format_exc()[34:].strip()
        except Exception:
            suts = None

        return suts


    def exposed_get_suts_len(self):
        """ get all suts from files """

        sutsLen = None
        try:
            sutsPath = self._conn.root.get_user_variable('sut_path')
            if not sutsPath:
                sutsPath = '{}/config/sut/'.format(TWISTER_PATH)
            sutPaths = [p for p in os.listdir(sutsPath) if os.path.isfile(os.path.join(sutsPath, p))
                        and p.split('.')[-1] == 'json']
            sutsLen = len(sutPaths)
        except Exception:
            sutsLen = None

        return sutsLen


    def exposed_delete_sut(self, name):
        """ get all suts from files """

        logPrint('Try to delete SUT {}'.format(name))
        try:
            sutsPath = self._conn.root.get_user_variable('sut_path')
            if not sutsPath:
                sutsPath = '{}/config/sut/'.format(TWISTER_PATH)
            logPrint('Delete SUT {}'.format(os.path.join(sutsPath, '.'.join([name, 'json']))))
            os.remove(os.path.join(sutsPath, '.'.join([name, 'json'])))
        except Exception:
            return False


    def exposed_list_all_suts(self):
        """ get all suts from files """

        logPrint('List all suts')
        suts = list()
        try:
            sutsPath = self._conn.root.get_user_variable('sut_path')
            if not sutsPath:
                sutsPath = '{}/config/sut/'.format(TWISTER_PATH)
            sutPaths = [p for p in os.listdir(sutsPath) if os.path.isfile(os.path.join(sutsPath, p))
                        and p.split('.')[-1] == 'json']

            for sutPath in sutPaths:
                sutName = '.'.join(['.'.join(sutPath.split('.')[:-1]  + ['user'])])
                suts.append(sutName)

        except Exception:
            logPrint('Error getting all suts')
            suts = None

        return suts


    def exposed_generate_index(self):
        """
        Store in a json file the tags from each test case file
        """
        ti = time.time()
        globalDict = {}

        with open('{}/config/fwmconfig.xml'.format(TWISTER_PATH)) as data_file:
            try:
                testCasesPath = re.search('TestCaseSourcePath>(.*)<', data_file.read()).group(1)
            except Exception:
                return '*ERROR* Cannot find the test cases source path !'

        for path, _, files in os.walk(testCasesPath):
            for name in files:
                fname = os.path.join(path, name)
                try:
                    text = open(fname, 'rb').read()
                except Exception:
                    return '*ERROR* Cannot find file name `%s` !' % (fname)
                tags = re.findall('^[ ]*?[#]*?[ ]*?<(?P<tag>\\w+)>([ -~\n]+?)</(?P=tag)>', text, re.MULTILINE)
                tagsDict = {title:descr for title, descr in tags}
                if tagsDict:
                    globalDict[fname] = tagsDict

        with open('{}/config/file_tags.json'.format(TWISTER_PATH), 'w') as file_tags:
            json.dump(globalDict, file_tags, indent=2)

        logPrint('Took `{:.4f}` seconds to generate index for {}.'.format(time.time()-ti, len(globalDict)))
        return True


    def exposed_parse_index(self, query):
        """
        Search for a query in the file index
        Example: search_index('filename=*.tcl')
                 search_index('description=Test status&title=init file')
        """
        if not os.path.isfile('{}/config/file_tags.json'.format(TWISTER_PATH)):
            return '*ERROR* You must generate the file tags!'
        ti = time.time()

        try:
            args = urlparse.parse_qs(query)
            logPrint('Searching for query {}'.format(args))
            try:
                fname = args.get('filename')[0]
                del args['filename']
                fname = fname.strip()
                if not fname:
                    fname = None
            except Exception:
                fname = None
        except Exception:
            msg = 'Cannot search having the arguments {} !'.format(query)
            return msg

        len_args = len(args)
        result = []

        with open('{}/config/file_tags.json'.format(TWISTER_PATH)) as data_file:
            data = json.load(data_file)

        for key, value in data.items():
            match = []
            short_fname = key[key.rfind('/')+1:]
            if fname:
                if fname.startswith('*') and key.endswith(fname[1:]) or \
                    fname.endswith('*') and short_fname.startswith(fname[:-1]) \
                    or fname.replace('*', '') in short_fname:
                    if not len_args:
                        result.append(key)
                    match = [key for k, v in args.items() if v[0] in value.get(k, "None")]
            else:
                match = [key for k, v in args.items() if v[0] in value.get(k, "None")]
            if len_args and len(match) == len_args:
                result.append(key)

        logPrint('Took `{:.4f}` seconds for {} elements and found {} entries' \
            ' that match.'.format(time.time()-ti, len(data), len(result)))
        return result


# # #


if __name__ == "__main__":

    logPrint('Starting Twister Client...')

    # This will read everything from epnames and connect to all CEs
    CLIENT = TwisterClient()
    CLIENT.run()

    logPrint('Stopping Twister Client.')


# Eof()
