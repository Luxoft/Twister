
# File: tsclogging.py ; This file is part of Twister.

# version: 3.005

# Copyright (C) 2012 , Luxoft

# Authors:
#    Andrei Costachi <acostachi@luxoft.com>
#    Andrei Toma <atoma@luxoft.com>
#    Cristian Constantin <crconstantin@luxoft.com>
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

'''
This module is used by the Central Engine and the Resource Allocator,
to print debug and error messages.
It shouldn't be used anywhere else.
'''

import os
import datetime

import cherrypy
import logging as log

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print('TWISTER_PATH environment variable is not set! Exiting!')
    exit(1)

LOGS_PATH = TWISTER_PATH + '/logs/'
if not os.path.exists(LOGS_PATH):
    os.makedirs(LOGS_PATH)

formatter = log.Formatter('%(asctime)s  %(levelname)-8s %(message)s',
            datefmt='%y-%m-%d %H:%M:%S')

# CherryPy logging
cherry_log = cherrypy.log.error_log

# Config file logging
dateTag = datetime.datetime.now().strftime("%Y-%b-%d %H-%M-%S")
LOG_FILE = LOGS_PATH + 'Log %s.txt' % dateTag
filehnd = log.FileHandler(LOG_FILE, mode='w')
filehnd.setLevel(log.NOTSET)
filehnd.setFormatter(formatter)
cherry_log.addHandler(filehnd)

# Config console logging
console = log.StreamHandler()
console.setLevel(log.NOTSET)
console.setFormatter(formatter)
cherry_log.addHandler(console)

# Current level
_LVL = cherry_log.getEffectiveLevel()


__all__ = ['FULL', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', 'LEVELS', 'LOG_FILE',
            'logMsg', 'logFull', 'logDebug', 'logInfo', 'logWarning', 'logError', 'logCritical']

FULL     = 5
DEBUG    = 10
INFO     = 20
WARNING  = 30
ERROR    = 40
CRITICAL = 50

LEVELS = {
    FULL:     'FULL',
    DEBUG:    'DEBUG',
    INFO:     'INFO',
    WARNING:  'WARNING',
    ERROR:    'ERROR',
    CRITICAL: 'CRITICAL'
}


def getLogLevel():
    #
    global _LVL
    return LEVELS[_LVL]
    #

def setLogLevel(Level):
    #
    all_levels = dict(LEVELS)
    all_levels.update( dict((v,k) for k,v in LEVELS.iteritems()) )

    # Fix integer levels
    try: Level = int(Level)
    except: pass

    if Level not in all_levels:
        print('---[ Invalid Log Level {}! ]---'.format(Level))
        return False

    # Map string levels
    if isinstance(Level, str):
        Level = all_levels[Level]

    global _LVL, filehnd, console
    _LVL = Level
    cherry_log.setLevel(_LVL)
    filehnd.setLevel(_LVL)
    console.setLevel(_LVL)

    if isinstance(Level, str):
        print('---[ Set Log Level {} ]---'.format(Level))
    else:
        print('---[ Set Log Level {} ]---'.format(all_levels[Level]))
    return True
    #

def logMsg(Level, *args):
    #
    if Level not in LEVELS:
        cherry_log.error('LOG: Invalid error level `{}`! The value must be in {}!'.format(Level, LEVELS.keys()))
        return
    #
    stack = cherry_log.findCaller()
    msg = '{}: {}: {}  {}'.format(os.path.split(stack[0])[1], str(stack[1]), stack[2],
          ' '.join([str(i) for i in args]))
    #
    if Level == FULL or Level == DEBUG:
        cherry_log.debug(msg)
    elif Level == INFO:
        cherry_log.info(msg)
    elif Level == WARNING:
        cherry_log.warning(msg)
    elif Level == ERROR:
        cherry_log.error(msg)
    else:
        cherry_log.critical(msg)
    #

def logFull(*args):
    global _LVL
    if _LVL < DEBUG: logMsg(FULL, *args)

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
