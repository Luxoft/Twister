#!/usr/bin/python

import os, sys
import json
import subprocess
import xmlrpclib
from datetime import datetime

if not sys.version.startswith('2.7'):
    print('Python version error! Central Engine must run on Python 2.7!')
    exit(1)

try:
    user_name = os.getenv('USER')
    if user_name=='root':
        user_name = os.getenv('SUDO_USER')
except:
    print('Cannot guess user name for this Execution Process! Exiting!')
    exit(1)

if os.path.exists(os.getenv('HOME') + '/twister/src'):
    os.environ['TWISTER_PATH'] = os.getenv('HOME') + '/twister/src'
else:
    os.environ['TWISTER_PATH'] = os.getenv('HOME') + '/twister'

eps = json.load(open('config_ep.json'))

#

for val in eps:

    if val['ENABLED']:

        proxy = xmlrpclib.ServerProxy("http://{0}:{1}/".format(val['CE_IP'], val['CE_PORT']))

        now_dtime = datetime.today()
        last_seen_alive = proxy.getEpVariable(user_name, val['ID'], 'last_seen_alive')
        if last_seen_alive:
            diff = now_dtime - datetime.strptime(last_seen_alive, '%Y-%m-%d %H:%M:%S')
            if diff.seconds < 5:
                print('Error: Process {0} is already started for user {1}! (ping={2} sec)\n'\
                    .format(val['ID'], user_name, diff.seconds))
                exit(1)

        del proxy

        str_exec = 'nohup python -u {twister_path}/client/executionprocess/ExecutionProcess.py '\
            '{user} {ep} "{ip}:{port}" > "{twister_path}/.twister_cache/{ep}_LIVE.log" &'.format(
            twister_path = os.getenv('TWISTER_PATH'),
            user = user_name,
            ep = val['ID'],
            ip = val['CE_IP'],
            port = val['CE_PORT'],
        )

        print 'Will execute:', str_exec
        subprocess.call(str_exec, shell=True)
        print 'Ok! `%s` for user `%s` launched in background!' % (val['ID'], user_name)

#
