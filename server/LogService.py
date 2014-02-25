
# File: LogService.py ; This file is part of Twister.

# version: 3.002

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
User Log Server, based on RPyc.
This process runs in the Twister Client folder.
"""

import os, sys
import time
import datetime
import glob
import json
import random
import logging

import rpyc
from rpyc.utils.server import ThreadedServer


log = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.NOTSET,
    format='%(asctime)s  %(levelname)-8s %(message)s',
    datefmt='%y-%m-%d %H:%M:%S',
    filename='log_srv.log',
    filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.NOTSET)
log.addHandler(console)


if not sys.version.startswith('2.7'):
    print('Python version error! Log Server must run on Python 2.7!')
    exit(1)

#

class LogService(rpyc.Service):

    def __init__(self, conn):
        log.debug('Warming up the Log Service...')
        self._conn = conn


    def on_connect(self):
        client_addr = self._conn._config['endpoints'][1]
        log.debug('Connected from `{}`.'.format(client_addr))


    def on_disconnect(self):
        client_addr = self._conn._config['endpoints'][1]
        log.debug('Disconnected from `{}`.'.format(client_addr))


    def exposed_hello(self):
        return True


    def exposed_write_log(self, data):
        """ Write a Log Message """
        global log
        logFile, logMsg = data.split(':')[0], ':'.join( data.split(':')[1:] )
        logPath = os.path.split(logFile)[0]

        if not os.path.isdir(logPath):
            try:
                os.makedirs(logPath)
                log.debug('Created logs folder at `{}`.'.format(logPath))
            except:
                resp = 'Log folder at `{}` cannot be created!'.format(logPath)
                log.error(resp)
                return False

        try:
            f = open(logFile, 'a')
        except Exception as e:
            resp = 'Exception or writing log file `{}`! `{}`!'.format(logFile, e)
            log.error(resp)
            return False

        f.write(logMsg)
        f.close()
        return True


    def exposed_reset_log(self, data):
        """ Reset 1 Log """
        global log

        try:
            info = json.loads(data)
        except:
            log.error('Cannot parse JSON data!')
            return False

        logFile = info['logPath']
        logPath = os.path.split(logFile)[0]

        if not os.path.isdir(logPath):
            try:
                os.makedirs(logPath)
                log.debug('Created logs folder at `{}`.'.format(logPath))
            except:
                resp = 'Log folder at `{}` cannot be created!'.format(logPath)
                log.error(resp)
                return False

        try:
            open(logFile, 'w').close()
            log.debug('Cleaned log `{}`.'.format(logFile))
            return True
        except:
            resp = 'Log folder `{}` cannot be reset!'.format(logFile)
            log.error(resp)
            return False


    def exposed_reset_logs(self, data):
        """ Reset all Logs """
        global log

        try:
            info = json.loads(data)
        except:
            log.error('Cannot parse JSON data!')
            return False

        log.debug('Cleaning `{}` log files...'.format(len(info['logTypes'])))
        err = False

        for logType in info['logTypes']:
            # For CLI
            if logType.lower() == 'logcli':
                for epname in info['epnames'].split(','):
                    # Name and full path of logCLI
                    logCli = os.path.split(info['logTypes'][logType])[1]
                    logPath = info['logsPath'] +'/'+ epname +'_'+ logCli
                    try:
                        open(logPath, 'w').close()
                    except:
                        log.error('CLI log file `{}` cannot be re-written!'.format(logPath))
                        err = True
            # For normal logs
            else:
                logPath = info['logTypes'][logType]
                try:
                    open(logPath, 'w').close()
                except:
                    log.error('Log file `{}` cannot be re-written!'.format(logPath))
                    err = True

        if err:
            return False
        else:
            return True


    def exposed_exit(self):
        """ Must Exit """
        global t, log
        log.warning('Log Server: *sigh* received EXIT signal...')
        t.close()
        # Reply to client.
        return True

    def exposed_backup_logs(self, data, start_time):
        """ Backup all Logs """
        global log

        try:
            info = json.loads(data)
        except:
            log.error('Cannot parse JSON data!')
            return False

        log.debug(' `{}` log files...'.format(len(info['logTypes'])))
        err = False

        for log_path in glob.glob(info['logsPath'] + os.sep + '*.log'):
            if info['archiveLogsPath'] and info['archiveLogsActive'] == 'true':
                archiveLogsPath = info['archiveLogsPath'].rstrip('/')
                archPath = '{}/{}.{}'.format(archiveLogsPath, os.path.basename(log_path), start_time)
                # Create path if it doesn't exist
                try: os.makedirs(archiveLogsPath)
                except: pass
                # Move file in archive
                try:
                    os.rename(log_path, archPath)
                    log.debug('Log file `{}` archived in `{}`.'.format(log_path, archPath))
                except Exception as e:
                    log.error('Cannot archive log `{}` in `{}`! Exception `{}`!'.format(log_path, archiveLogsPath, e))
            try:
                os.remove(log_path)
            except Exception as e:
                pass

        if err:
            return False
        else:
            return True


#

if __name__ == '__main__':

    PORT = sys.argv[1:2]

    if not PORT:
        log.error('Log Server: Must start with parameter PORT number!')
        exit(1)

    t = ThreadedServer(LogService, port=int(PORT[0]))
    t.start()

    log.warning('Log Server: Bye bye.')


# Eof()
