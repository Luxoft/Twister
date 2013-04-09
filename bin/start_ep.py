#!/usr/bin/python

# version: 2.002

# This file will start ALL Execution Processes that are enabled,
# from file `twister/config/epname.ini`.
# This should run as ROOT, to be able to start the packets sniffer.

import os, sys
import xmlrpclib
import subprocess

from datetime import datetime
from ConfigParser import SafeConfigParser

if not sys.version.startswith('2.7'):
    print('Python version error! Execution Process must run on Python 2.7!')
    exit(1)

try:
    user_name = os.getenv('USER')
    if user_name=='root':
        user_name = os.getenv('SUDO_USER')
except:
    print('Cannot guess user name for this Execution Process! Exiting!')
    exit(1)

pipe = subprocess.Popen('ps ax | grep start_packets_twist.py', shell=True, stdout=subprocess.PIPE)
for line in pipe.stdout.read().splitlines():
    try:
        kill(int(line.split()[0]), 9)
    except Exception, e:
        pass
del pipe

# Twister path environment
os.environ['TWISTER_PATH'] = os.getenv('HOME') + '/twister'

os.chdir(os.getenv('TWISTER_PATH') + '/bin')

cfg = SafeConfigParser()
cfg.read(os.getenv('TWISTER_PATH') + '/config/epname.ini')
eps = cfg.sections()
eps.pop(eps.index('SNIFF'))
print('Found `{}` EPs: `{}`.\n'.format(len(eps), ', '.join(eps)))

#

snifferEth = None
if cfg.get('SNIFF', 'ENABLED') == '1':
    snifferEth = cfg.get('SNIFF', 'ETH_INTERFACE')

#

for val in eps:

    # Only if the EP is enabled
    if cfg.getint(val, 'ENABLED'):

        ce_ip   = cfg.get(val, 'CE_IP')
        ce_port = cfg.get(val, 'CE_PORT')

        proxy = xmlrpclib.ServerProxy("http://{0}:{1}/".format(ce_ip, ce_port))

        try:
            last_seen_alive = proxy.getEpVariable(user_name, val, 'last_seen_alive')
        except:
            print('Error: Cannot connect to Central Engine to check the EP! Exiting!\n')
            exit(1)

        now_dtime = datetime.today()

        if last_seen_alive:
            diff = now_dtime - datetime.strptime(last_seen_alive, '%Y-%m-%d %H:%M:%S')
            if diff.seconds < 5:
                print('Error: Process {0} is already started for user {1}! (ping={2} sec)\n'\
                    .format(val, user_name, diff.seconds))
                del proxy
                continue

        del proxy

        str_exec = 'nohup python -u {twister_path}/client/executionprocess/ExecutionProcess.py '\
            '{user} {ep} "{ip}:{port}" {sniff} > "{twister_path}/.twister_cache/{ep}_LIVE.log" &'.format(
            twister_path = os.getenv('TWISTER_PATH'),
            user = user_name,
            ep = val,
            ip = ce_ip,
            port = ce_port,
            sniff = snifferEth,
        )

        print 'Will execute:', str_exec
        subprocess.call(str_exec, shell=True)
        print 'Ok! `%s` for user `%s` launched in background!\n' % (val, user_name)

#
