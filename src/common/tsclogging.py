
# File: tsclogging.py ; This file is part of Twister.

# Copyright (C) 2012 , Luxoft

# Authors:
#    Andrei Costachi <acostachi@luxoft.com>
#    Andrei Toma <atoma@luxoft.com>
#    Cristian Constantin <crconstantin@luxoft.com>
#    Daniel Cioata <dcioata@luxoft.com>

# Twister is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 2 of the License.

# Twister is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Twister.  If not, see <http://www.gnu.org/licenses/>.

import logging as log

import os
import datetime
import inspect

if not os.path.exists('logs'):
    os.mkdir('logs')

dateTag = datetime.datetime.now().strftime("%Y-%b-%d %H-%M-%S")
FILENAME = 'logs/Log %s.txt' % dateTag
log.basicConfig(level=log.NOTSET, format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%y-%m-%d %H:%M:%S', filename=FILENAME, filemode='w')

console = log.StreamHandler()
console.setLevel(log.NOTSET)
log.getLogger('').addHandler(console)

__all__ = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL',
            'logMsg', 'logDebug', 'logInfo', 'logWarning', 'logError', 'logCritical']

DEBUG    = 1
INFO     = 2
WARNING  = 3
ERROR    = 4
CRITICAL = 5

def setLogLevel(Level):
    #
    if Level not in (DEBUG, INFO, WARNING, ERROR, CRITICAL):
        log.error('LOG: Invalid error level `%s`!' % str(Level))
        return
    #
    log.setLevel(Level * 10)
    #

def setLogLevelConsole(Level):
    #
    if Level not in (DEBUG, INFO, WARNING, ERROR, CRITICAL):
        log.error('LOG: Invalid error level `%s`!' % str(Level))
        return
    #
    global console
    console.setLevel(Level * 10)
    #

def logMsg(Level, *args):
    #
    if Level not in (DEBUG, INFO, WARNING, ERROR, CRITICAL):
        log.error('LOG: Invalid error level `%s`!' % str(Level))
        return
    #
    frame = inspect.stack()[-2][0]
    info = inspect.getframeinfo(frame)
    msg = info.function + ': ' + ' '.join([str(i) for i in args])
    #msg = os.path.split(info.filename)[1] +':'+ str(info.lineno) +'  '+ info.function +': '+ ' '.join([str(i) for i in args])
    #
    if Level == 1:
        log.debug(msg)
    elif Level == 2:
        log.info(msg)
    elif Level == 3:
        log.warning(msg)
    elif Level == 4:
        log.error(msg)
    else:
        log.critical(msg)
    #

def logDebug(*args):
    logMsg(DEBUG, *args)

def logInfo(*args):
    logMsg(INFO, *args)

def logWarning(*args):
    logMsg(WARNING, *args)

def logError(*args):
    logMsg(ERROR, *args)

def logCritical(*args):
    logMsg(CRITICAL, *args)
