
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
import binascii

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


    def sendCommand(self, command, name='', *args, **kwargs):

        if command==SM_LIST or command==sm_command_map[SM_LIST]:
            return self.listServices()

        found = False

        for service in self.twister_services:
            if name == service['name']:
                found = True
                break

        if not found:
            logDebug('SM: Invalid service name: `%s`!'.format(name))
            return False

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
            try: return self.saveConfig(service, args[0][0])
            except: return 'SM: Invalid number of parameters for save config!'

        elif command==SM_GET_LOG or command==sm_command_map[SM_GET_LOG]:
            try: return self.getConsoleLog(service, read=args[0][0], fstart=args[0][1])
            except: return 'SM: Invalid number of parameters for read log!'

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
            rc = -1

        return rc


    def serviceStart(self, service):

        tprocess = service.get('pid', 0)

        if tprocess:
            # Check if child process has terminated
            tprocess.poll()

            if tprocess.returncode is None:
                logDebug('SM: Service name `{0}` is already running with PID `{1}`.'.format(
                    service['name'], tprocess.pid))
                return True

        del tprocess

        script_path = '{0}/server/{1}/{2}'.format(TWISTER_PATH, service['name'], service['script'])

        if service['config']:
            config_path = '{0}/server/{1}/{2}'.format(TWISTER_PATH, service['name'], service['config'])
        else:
            config_path = ''

        if not os.path.isfile(script_path):
            error = 'SM: Cannot start service `{0}`! No such script file `{1}`!'.format(
                service['name'], script_path)
            logError(error)
            return error

        if service['config'] and (not config_path):
            error = 'SM: Cannot start service `{0}`! No such config file `{1}`!'.format(
                service['name'], config_path)
            logError(error)
            return error

        service['pid'] = 0 # Delete process here
        env = os.environ
        env.update({'TWISTER_PATH': TWISTER_PATH})

        log_path = '{0}/server/{1}/{2}'.format(TWISTER_PATH, service['name'], service['logfile'])

        with open(log_path, 'wb') as out:
            try:
                tprocess = subprocess.Popen(['python', '-u', script_path, config_path],
                           stdout=out, stderr=out, env=env)
            except Exception, e:
                error = 'SM: Cannot start service `{0}` with config file `{1}`!\n'\
                    'Exception: `{2}`!'.format(service['name'], config_path, e)
                logError(error)
                return error

        service['pid'] = tprocess
        logDebug('Started service `{}`, using script `{}` and config `{}`, with PID `{}`.'.format(
            service['name'], script_path, config_path, tprocess.pid))
        return True


    def serviceStop(self, service):

        rc = self.serviceStatus(service)
        if not rc:
            logDebug('SM: Service name `{0}` is not running.'.format(service['name']))
            return False

        tprocess = service.get('pid', 0)

        if isinstance(tprocess, int):
            logError('SM: Cannot stop service `{0}`!'.format(service['name']))

        try:
            tprocess.terminate()
            logWarning('SM: Stopped service: `{0}`.'.format(service['name']))
            return True
        except Exception, e:
            logError('SM: Cannot stop service: `{0}`, exception `{1}`!'.format(service['name'], e))
            return False


    def serviceKill(self, service):

        rc = self.serviceStatus(service)
        if not rc:
            logDebug('SM: Service name `{0}` is not running.'.format(service['name']))
            return False

        tprocess = service.get('pid', 0)

        if isinstance(tprocess, int):
            logError('SM: Cannot kill service `{0}`!'.format(service['name']))

        try:
            tprocess.kill()
            logError('SM: Killed service: `{0}`.'.format(service['name']))
            return True
        except Exception, e:
            logError('SM: Cannot stop service: `{0}`, exception `{1}`!'.format(service['name'], e))
            return False


    def readConfig(self, service):

        config_path = '{0}/server/{1}/{2}'.format(TWISTER_PATH, service['name'], service['config'])

        if not os.path.isfile(config_path):
            logError('SM: No such config file `{0}`!'.format(config_path))
            return False

        with open(config_path, 'rb') as out:
            data = out.read()

        return data or ''


    def saveConfig(self, service, data):

        config_path = '{0}/server/{1}/{2}'.format(TWISTER_PATH, service['name'], service['config'])

        if not os.path.isfile(config_path):
            logError('SM: No such config file `{0}`!'.format(config_path))
            return False

        with open(config_path, 'wb') as out:
            out.write(data)

        return True


    def getConsoleLog(self, service, read, fstart):
        """
        Called in the Java GUI to show the logs.
        """
        if fstart is None:
            return '*ERROR for {0}!* Parameter FSTART is NULL!'.format(service['name'])

        filename = '{0}/server/{1}/{2}'.format(TWISTER_PATH, service['name'], service['logfile'])

        if not os.path.exists(filename):
            return '*ERROR for {0}!* No such log file `{0}`!'.format(service['name'], filename)

        if not read or read=='0':
            return os.path.getsize(filename)

        fstart = long(fstart)
        f = open(filename)
        f.seek(fstart)
        data = f.read()
        f.close()

        return binascii.b2a_base64(data)


# Eof()
