
# File: LogServer.py ; This file is part of Twister.

# version: 2.006

# Copyright (C) 2012-2013 , Luxoft

"""
User Log Socket server.
This process runs in the Twister Client folder.
"""

import os, sys
import time
import glob
import random
import socket
import json
import logging

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

def create_listener(PORT):
    """
    Create streaming socket server on a local host and a random port.
    """
    log.debug('Log: Preparing to start on `{}`...'.format(PORT))
    for res in socket.getaddrinfo(None, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
        af, socktype, proto, canonname, sa = res
        try:
            sock = socket.socket(af, socktype, proto)
        except socket.error as msg:
            sock = None
            continue
        try:
            sock.bind(sa)
            sock.listen(1)
        except socket.error as msg:
            sock.close()
            sock = None
            continue
        break
    if sock is None:
        log.error('Cannot open socket!')
        sys.exit(1)
    else:
        log.debug('Log: Started server on `{}`.'.format(sa))
        return sock


def process_cmd(sock):
    """
    Process 1 command, from 1 client.
    """
    global log
    conn, addr = sock.accept()
    # log.debug('Connected by `{}`.'.format(addr))

    while 1:
        resp = 'Ok!' # Default response
        buff = 2**15

        # Message from client.
        data = conn.recv(buff)

        # if data:
        #    log.debug('Log: Received message with `len = {}`.'.format(len(data)))

        # ~~~ Reset 1 Log ~~~
        if data.startswith("{") and '"del"' in data:
            try:
                info = json.loads(data)
            except:
                log.error('Cannot parse JSON data!')
                return False

            logPath = info['logPath']

            try:
                open(logPath, 'w').close()
                log.debug('Log: Cleaned log `{}`.'.format(logPath))
            except:
                resp = 'Log folder `{}` cannot be reset!'.format(logPath)
                log.error(resp)


        # ~~~ Reset all Logs ~~~
        elif data.startswith("{") and '"reset"' in data:
            try:
                info = json.loads(data)
            except:
                log.error('Cannot parse JSON data!')
                return False

            log.debug('Log: Cleaning `{}` log files...'.format(len(info['logTypes'])))
            err = False

            for log_path in glob.glob(info['logsPath'] + os.sep + '*.log'):
                if info['archiveLogsPath'] and info['archiveLogsActive'] == 'true':
                    archiveLogsPath = info['archiveLogsPath'].rstrip('/')
                    log_time = str(time.time()).split('.')[0]
                    archPath = '{}/{}.{}'.format(archiveLogsPath, os.path.basename(log_path), log_time)
                    # Create path if it doesn't exist
                    try: os.makedirs(archiveLogsPath)
                    except: pass
                    # Move file in archive
                    try:
                        os.rename(log_path, archPath)
                        log.debug('Log: File `{}` archived in `{}`.'.format(log_path, archPath))
                    except Exception as e:
                        log.error('Cannot archive log `{}` in `{}`! Exception `{}`!'.format(log_path, archiveLogsPath, e))
                try:
                    os.remove(log_path)
                except Exception as e:
                    pass

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
                            log.error('Log file `{}` cannot be re-written!'.format(logPath))
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
                resp = 'Cound not reset all logs!'
            else:
                log.debug('Success!')


        # ~~~ Write Log Message ~~~
        elif ':' in data:
            logFile, logMsg = data.split(':')[0], ':'.join( data.split(':')[1:] )

            try:
                f = open(logFile, 'a')
            except:
                logFolder = os.path.split(logFile)[0] + '/logs'
                try:
                    os.makedirs(logFolder)
                except:
                    resp = 'Log folder `{}` cannot be created!'.format(logFolder)
                    log.error(resp)

            f.write(logMsg)
            f.close()


        # ~~~ Write Log Message ~~~
        elif data.upper() == 'EXIT':
            # log.warning('Log Server:  *sigh* received EXIT signal...')
            # Reply to client.
            conn.send('EXIT!')
            return True


        # ~~~ Null ~~~
        else:
            resp = 'Null!'
            break

        # Reply to client.
        conn.send(resp)

    conn.close()
    # log.debug('Closed conn from `{}`.'.format(addr))

#

if __name__ == '__main__':

    PORT = sys.argv[1:2]

    if not PORT:
        log.error('Log Server: Must start with parameter PORT number!')
        exit(1)

    sock = create_listener(int(PORT[0]))

    while True:
        p = process_cmd(sock)
        # If the response is True, time to exit
        if p: break

    log.warning('Log Server: Bye bye.')


# Eof()
