
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
