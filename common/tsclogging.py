
# File: tsclogging.py ; This file is part of Twister.

# version: 3.006

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

FORMATTER = log.Formatter('%(asctime)s  %(levelname)-8s %(message)s',
            datefmt='%y-%m-%d %H:%M:%S')

# CherryPy logging
CHERRY_LOG = cherrypy.log.error_log

# Config file logging
DATE_TAG = datetime.datetime.now().strftime("%Y-%b-%d %H-%M-%S")
LOG_FILE = LOGS_PATH + 'Log %s.txt' % DATE_TAG
FILEHND = log.FileHandler(LOG_FILE, mode='w')
FILEHND.setLevel(log.NOTSET)
FILEHND.setFormatter(FORMATTER)
CHERRY_LOG.addHandler(FILEHND)

# Config console logging
CONSOLE = log.StreamHandler()
CONSOLE.setLevel(log.NOTSET)
CONSOLE.setFormatter(FORMATTER)
CHERRY_LOG.addHandler(CONSOLE)

# Current level
_LVL = CHERRY_LOG.getEffectiveLevel()


__all__ = ['FULL', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', 'LEVELS', 'LOG_FILE',
            'log_msg', 'logFull', 'logDebug', 'logInfo', 'logWarning', 'logError', 'logCritical']

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
    """ return current log level """
    global _LVL
    return LEVELS[_LVL]
    #

def setLogLevel(level):
    """ set the logging details level """
    all_levels = dict(LEVELS)
    all_levels.update( dict((v, k) for k, v in LEVELS.iteritems()) )

    # Fix integer levels
    try:
        level = int(level)
    except:
        pass

    if level not in all_levels:
        print('---[ Invalid Log Level {}! ]---'.format(level))
        return False

    # Map string levels
    if isinstance(level, str):
        level = all_levels[level]

    global _LVL, FILEHND, CONSOLE
    _LVL = level
    CHERRY_LOG.setLevel(_LVL)
    FILEHND.setLevel(_LVL)
    CONSOLE.setLevel(_LVL)

    if isinstance(level, str):
        print('---[ Set Log Level {} ]---'.format(level))
    else:
        print('---[ Set Log Level {} ]---'.format(all_levels[level]))
    return True
    #

def log_msg(level, *args):
    """ log a message """
    #
    if level not in LEVELS:
        CHERRY_LOG.error('LOG: Invalid error level `{}`! The value must be in {}!'.format(level, LEVELS.keys()))
        return
    #
    stack = CHERRY_LOG.findCaller()
    msg = '{}: {}: {}  {}'.format(os.path.split(stack[0])[1], str(stack[1]), stack[2],
          ' '.join([str(i) for i in args]))
    #
    if level == FULL or level == DEBUG:
        CHERRY_LOG.debug(msg)
    elif level == INFO:
        CHERRY_LOG.info(msg)
    elif level == WARNING:
        CHERRY_LOG.warning(msg)
    elif level == ERROR:
        CHERRY_LOG.error(msg)
    else:
        CHERRY_LOG.critical(msg)
    #

def logFull(*args):
    """ ALL details """
    global _LVL
    if _LVL < DEBUG:
        log_msg(FULL, *args)

def logDebug(*args):
    """ debug """
    log_msg(DEBUG, *args)

def logInfo(*args):
    """ info """
    log_msg(INFO, *args)

def logWarning(*args):
    """ warning """
    log_msg(WARNING, *args)

def logError(*args):
    """ error """
    log_msg(ERROR, *args)

def logCritical(*args):
    """ critical errors """
    log_msg(CRITICAL, *args)
