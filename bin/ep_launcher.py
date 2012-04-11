#!/usr/bin/python

import os, sys
import json
import subprocess

if not sys.version.startswith('2.7'):
    print('Python version error! Central Engine must run on Python 2.7!')
    exit(1)

os.environ['TWISTER_PATH'] = os.getenv('HOME') + '/twister/src'

eps = json.load(open('config.json'))

#

for val in eps:

    if val['ENABLED']:

        str_exec = 'nohup python -u {twister_path}/client/executionprocess/ExecutionProcess.py {ep} '\
            '"{ip}:{port}" > "{twister_path}/.twister_cache/{ep}_LIVE.log" &'.format(
            twister_path = os.getenv('TWISTER_PATH'),
            ep = val['ID'],
            ip = val['CE_IP'],
            port = val['CE_PORT'],
        )

        print 'Will execute:', str_exec
        subprocess.call(str_exec, shell=True)
        print 'Ok!, %s launched in BG!' % val['ID']

#
