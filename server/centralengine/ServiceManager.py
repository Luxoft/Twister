
# File: ServiceManager.py ; This file is part of Twister.

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

import os, sys
import json
import time
import subprocess

SM_LIST       = 0
SM_START      = 1
SM_STOP       = 2
SM_STATUS     = 3
SM_DESCRIP    = 4
SM_GET_CONFIG = 5
SM_SET_CONFIG = 6
SM_GET_LOG    = 7

sm_command_map = {
    SM_START      : 'start',
    SM_STOP       : 'stop',
    SM_STATUS     : 'status',
    SM_DESCRIP    : 'description',
    SM_GET_CONFIG : 'get config',
    SM_SET_CONFIG : 'set config',
    SM_GET_LOG    : 'get log',
    SM_LIST       : 'list'
}

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print('$TWISTER_PATH environment variable is not set! Exiting!')
    exit(1)
sys.path.append(TWISTER_PATH)

from common.tsclogging import *
from common import iniparser

#

class ServiceManager():

    def __init__(self):

        logDebug('SM: Starting Service Manager...')

        self.twister_services = []
        cfg_path = '{0}/config/services.ini'.format(TWISTER_PATH)
        cfg = iniparser.ConfigObj(cfg_path)

        for service in cfg:
            if service == 'DEFAULT':
                continue
            cfg[service]['name'] = service
            self.twister_services.append(cfg[service])

        logDebug('SM: Found `{0}` services: `{1}`.'.format(len(self.twister_services), ', '.join(cfg.keys())))
        del cfg, cfg_path


    def sendCommand(self, command, name='', args={}):

        if command==SM_LIST or command==sm_command_map[SM_LIST]:
            return self.listServices()

        found = False

        for service in self.twister_services:
            if name == service['name']:
                found = True
                break

        if not found:
            logDebug('SM: Invalid service name: `%s`!'.format(name))
            return None

        elif command==SM_STATUS or command==sm_command_map[SM_STATUS]:
            return self.serviceStatus(service)

        elif command==SM_DESCRIP or command==sm_command_map[SM_DESCRIP]:
            return service.get('descrip')

        if command==SM_START or command==sm_command_map[SM_START]:
            return self.serviceStart(service)

        elif command==SM_STOP or command==sm_command_map[SM_STOP]:
            return self.serviceStop(service)

        elif command==SM_GET_CONFIG or command==sm_command_map[SM_GET_CONFIG]:
            return self.readConfig(service)

        elif command==SM_SET_CONFIG or command==sm_command_map[SM_SET_CONFIG]:
            return self.saveConfig(service, args)

        elif command==SM_GET_LOG or command==sm_command_map[SM_GET_LOG]:
            return self.getConsoleLog(service)

        else:
            return 'SM: Unknown command number: `{0}`!'.format(command)


    def listServices(self):
        srv = []
        for service in self.twister_services:
            srv.append(service['name'])
        return ','.join(srv)


    def serviceStatus(self, service):
        # Values are: -1, 0, or any error code
        # -1 means the app is still running

        tprocess = service.get('pid', 0)
        rc = 0

        if tprocess:
            tprocess.poll()
            rc = tprocess.returncode

        if rc is None:
            # logDebug('SM: Service `{0}` is currently running.'.format(service['name']))
            rc = -1
        else:
            # logDebug('SM: Service `{0}` is not running.'.format(service['name']))
            service['pid'] = 0

        return rc


    def serviceStart(self, service):

        tprocess = service.get('pid', 0)
        if tprocess:
            logDebug('SM: Service name `{0}` is already running with PID `{1}`.'.format(
                service['name'], tprocess.pid
                ))
            return True

        script_path = '{0}/server/{1}/{2}'.format(TWISTER_PATH, service['name'], service['script'])

        if service['config']:
            config_path = '{0}/server/{1}/{2}'.format(TWISTER_PATH, service['name'], service['script'])
        else:
            config_path = ''

        if not os.path.isfile(script_path):
            logError('SM: Cannot start service `{0}`! No such script file `{1}`!'.format(
                service['name'], script_path))
            return False

        if service['config'] and (not config_path):
            logError('SM: Cannot start service `{0}`! No such config file `{1}`!'.format(
                service['name'], config_path))
            return False

        log_path = '{0}/server/{1}/{2}'.format(TWISTER_PATH, service['name'], service['logfile'])

        with open(log_path, 'wb') as out:
            tprocess = subprocess.Popen(['python', script_path, config_path], stdout=out)

        service['pid'] = tprocess
        logDebug('Started service `{}`, using script `{}` and config `{}`, with PID `{}`.'.format(
            service['name'], script_path, config_path, tprocess.pid))
        return True


    def serviceStop(self, service):

        rc = self.serviceStatus(service)
        if not rc:
            logDebug('SM: Service name `{0}` is not running.'.format(service['name']))
            return False

        logWarning('SM: Stopping service: `{0}`.'.format(service['name']))
        tprocess = service.get('pid', 0)
        tprocess.terminate()

        return True


    def serviceKill(self, service):

        rc = self.serviceStatus(service)
        if not rc:
            logDebug('SM: Service name `{0}` is not running.'.format(service['name']))
            return False

        logWarning('SM: Killing service: `{0}`.'.format(service['name']))
        tprocess = service.get('pid', 0)
        tprocess.kill()

        return True


    def readConfig(self, service):

        config_path = '{0}/server/{1}/{2}.py'.format(TWISTER_PATH, service['name'], service['config'])

        if not os.path.isfile(config_path):
            logError('SM: No such config file `{0}`!'.format(config_path))
            return False

        with open(config_path, 'rb') as out:
            data = out.read()

        return data


    def saveConfig(self, service, data):

        config_path = '{0}/server/{1}/{2}.py'.format(TWISTER_PATH, service['name'], service['config'])

        if not os.path.isfile(config_path):
            logError('SM: No such config file `{0}`!'.format(config_path))
            return False

        with open(config_path, 'wb') as out:
            out.write(data)

        return True


    def getConsoleLog(self, service):

        log_path = '{0}/server/{1}/{2}'.format(TWISTER_PATH, service['name'], service['logfile'])

        if not os.path.isfile(log_path):
            logError('SM: No such log file `{0}`!'.format(log_path))
            return False

        with open(log_path, 'rb') as log:
            data = log.read()

        return data


# Eof()
