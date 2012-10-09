
# File: CentralEngineRest.py ; This file is part of Twister.

# Copyright (C) 2012 , Luxoft

# Authors:
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
Central Engine REST functions
*****************************

All functions are exposed and can be accessed using the browser.
"""

import os, sys
import glob
import json
import time
import platform
import cherrypy
import mako
from mako.template import Template
from binascii import unhexlify as decode

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print('\n$TWISTER_PATH environment variable is not set! Exiting!\n')
    exit(1)
sys.path.append(TWISTER_PATH)

from common.constants import *
from common.tsclogging import *

if mako.__version__ < '0.7':
    logWarning('Warning! Mako-template version is old: `{0}`! Some pages might crash!\n'.format(mako.__version__))

# # # # #

def calcMemory():
    import subprocess
    memLine = subprocess.check_output(['free', '-o']).split('\n')[1]
    memUsed    = int(memLine.split()[2])
    mebBuffers = int(memLine.split()[-2])
    memCached  = int(memLine.split()[-1])
    Total      = float(memLine.split()[1])
    memPer = ((memUsed - mebBuffers - memCached) * 100.) / Total
    return float('%.2f' % memPer)

def getCpuData():
    statLine = open('/proc/stat', 'r').readline()
    timeList = statLine.split(' ')[2:6]
    for i in range(len(timeList)):
        timeList[i] = float(timeList[i])
    return timeList

def calcCpu():
    x = getCpuData()
    time.sleep(0.5)
    y = getCpuData()
    for i in range(len(x)):
        y[i] -= x[i]
    cpuPer = sum(y[:-1]) / sum(y) * 100.
    return float('%.2f' % cpuPer)

def prepareLog(log_file, pos=0):
    if not os.path.isfile(log_file):
        return 'File `{0}` does not exist!'.format(log_file)
    f = open(log_file, 'rb')
    f.seek(pos)
    log = f.read().rstrip()
    f.close() ; del f

    body = '''
    <style>
    .nfo {color:gray; text-shadow: 1px 1px 1px #aaa}
    .dbg {color:gray; text-shadow: 1px 1px 1px #aaa}
    .err {color:orange; text-shadow: 1px 1px 1px #aaa}
    .warn {color:orange; text-shadow: 1px 1px 1px #aaa}
    .crit {color:red; text-shadow: 1px 1px 1px #aaa}
    </style>
    '''
    body += log.replace('\n', '<br>\n').replace(' ', '&nbsp;')
    del log
    body = body.replace(';INFO&',   ';<b class="nfo">INFO</b>&')
    body = body.replace(';DEBUG&',  ';<b class="dbg">DEBUG</b>&')
    body = body.replace(';ERROR&',  ';<b class="err">ERROR</b>&')
    body = body.replace(';WARNING&',  ';<b class="warn">WARNING</b>&')
    body = body.replace(';CRITICAL&', ';<b class="crit">CRITICAL</b>&')
    body = body.replace(';debug:',    ';<b class="dbg">debug</b>:')
    body = body.replace(';error:',    ';<b class="err">error</b>:')
    body = body.replace(';warning:',  ';<b class="warn">warning</b>:')
    return body

def dirList(path, newdict):
    if os.path.isdir(path):
        dlist = []
        flist = []
        for fname in sorted(os.listdir(path), key=str.lower):
            nd = {'data': fname, 'children': []}
            if os.path.isdir(path + os.sep + fname):
                dlist.append(nd)
            else:
                flist.append(nd)
        newdict['children'] = dlist + flist
    for nitem in newdict['children']:
        newpath = path + os.sep + nitem['data']
        dirList(newpath, nitem)

# # # # #

class CentralEngineRest:

    def __init__(self, parent, project):

        self.project = project
        self.parent  = parent


    def user_agent(self):
        """
        User agent returns Browser or XML RPC client.
        This function is not exposed.
        """
        if  cherrypy.request.headers['User-Agent'].startswith('xmlrpclib.py') or\
            cherrypy.request.headers['User-Agent'].startswith('Apache XML RPC'):
            # XML RPC client
            return 'x'
        else:
            # Browser
            return 'b'


    @cherrypy.expose
    def index(self):
        if self.user_agent() == 'x':
            return 0

        ip_port = cherrypy.request.headers['Host']
        machine = platform.uname()[1]
        system  = ' '.join(platform.linux_distribution())
        users   = sorted([u.split('/')[2] for u in glob.glob('/home/*/twister')])
        # os.path.expanduser("~user")

        output = Template(filename=TWISTER_PATH + '/server/centralengine/template_main.htm')
        return output.render(ip_port=ip_port, machine=machine, system=system, users=users)


    @cherrypy.expose
    def users(self, user):
        if self.user_agent() == 'x':
            return 0

        host = cherrypy.request.headers['Host']
        reversed = dict((v,k) for k,v in execStatus.iteritems())
        status = reversed[self.project.getUserInfo(user, 'status')]
        master_config = self.project.getUserInfo(user, 'config_path')
        proj_config = self.project.getUserInfo(user, 'tests_path')
        logs_path = self.project.getUserInfo(user, 'logs_path')
        try: eps_file = self.project.parsers[user].xmlDict.root.epidsfile.text
        except: eps_file = ''
        eps = self.project.getUserInfo(user, 'eps')
        ep_statuses = [ reversed[eps[ep].get('status', STATUS_INVALID)] for ep in eps ]
        logs = self.project.getUserInfo(user, 'log_types')

        output = Template(filename=TWISTER_PATH + '/server/centralengine/template_user.htm')
        return output.render(host=host, user=user, status=status, master_config=master_config, proj_config=proj_config,
               exec_status=reversed, logs_path=logs_path, eps_file=eps_file, eps=eps, ep_statuses=ep_statuses, logs=logs)

#

    @cherrypy.expose
    def json_stats(self):
        if self.user_agent() == 'x':
            return 0

        cherrypy.response.headers['Content-Type']  = 'application/json; charset=utf-8'
        cherrypy.response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        cherrypy.response.headers['Pragma']  = 'no-cache'
        cherrypy.response.headers['Expires'] = 0
        data = {'mem': calcMemory(), 'cpu': calcCpu()}
        return json.dumps(data)


    @cherrypy.expose
    def json_all(self):
        if self.user_agent() == 'x':
            return 0

        cherrypy.response.headers['Content-Type']  = 'application/json; charset=utf-8'
        cherrypy.response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        cherrypy.response.headers['Pragma']  = 'no-cache'
        cherrypy.response.headers['Expires'] = 0
        return open(TWISTER_PATH + '/common/project_users.json', 'r').read()


    @cherrypy.expose
    def json_eps(self, user, epname):
        if self.user_agent() == 'x':
            return 0

        epname = decode(epname)
        cherrypy.response.headers['Content-Type']  = 'application/json; charset=utf-8'
        cherrypy.response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        cherrypy.response.headers['Pragma']  = 'no-cache'
        cherrypy.response.headers['Expires'] = 0

        data = []
        epinfo = self.project.getEpInfo(user, epname)

        for suite in epinfo['suites']:
            sdata = {
                'data': epinfo['suites'][suite]['name'],
                'attr': {'id': suite, 'rel': 'suite'},
                'children': [],
            }
            if epinfo['suites'][suite]['files']:
                sdata['children'] = [epinfo['suites'][suite]['files'][k]['file'] for k in epinfo['suites'][suite]['files'].keys()]
            data.append(sdata)

        return json.dumps(data)


    @cherrypy.expose
    def json_folders(self):
        if self.user_agent() == 'x':
            return 0

        newdict = {'data':'root','children':[]}
        dirpath = '/home/cro/twister'
        dirList(dirpath, newdict)

        return json.dumps(newdict)


    @cherrypy.expose
    def json_logs(self, user='', log=''):
        if self.user_agent() == 'x':
            return 0

        if user and log:
            logs = self.project.getUserInfo(user, 'log_types')
            logsPath = self.project.getUserInfo(user, 'logs_path')
            if log.startswith('logcli_'):
                epname = '_'.join(log.split('_')[1:])
                log = logsPath + os.sep + decode(epname) + '_CLI.log'
            else:
                log = logs.get(log)

        cherrypy.response.headers['Content-Type']  = 'application/json; charset=utf-8'
        cherrypy.response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        cherrypy.response.headers['Pragma']  = 'no-cache'
        cherrypy.response.headers['Expires'] = 0
        return json.dumps(prepareLog(log or LOG_FILE))

#

    @cherrypy.expose
    def resetUser(self, user):
        self.project.reset(user)
        self.parent.resetLogs(user)
        raise cherrypy.HTTPRedirect('http://{host}/rest/users/{user}'.format(
            host = cherrypy.request.headers['Host'], user = user
        ))


    @cherrypy.expose
    def setUserStatus(self, user, status):
        output = Template(filename=TWISTER_PATH + '/server/centralengine/template_error.htm')
        try: status = int(status)
        except: return output.render(title='Error!', body='<b>Status value `{0}` is invalid!</b>'.format(status))
        if status not in execStatus.values():
            return output.render(title='Error!', body='<b>Status value `{0}` is not in the list of valid statuses: {1}!</b>'\
                .format(status, execStatus.values()))
        self.parent.setExecStatusAll(user, status, 'User status changed from REST interface.')
        raise cherrypy.HTTPRedirect('http://{host}/rest/users/{user}#tab_home'.format(
            host = cherrypy.request.headers['Host'], user = user
        ))


    @cherrypy.expose
    def setEpStatus(self, user, epname, status):
        output = Template(filename=TWISTER_PATH + '/server/centralengine/template_error.htm')
        try: status = int(status)
        except: return output.render(title='Error!', body='<b>Status value `{0}` is invalid!</b>'.format(status))
        if status not in execStatus.values():
            return output.render(title='Error!', body='<b>Status value `{0}` is not in the list of valid statuses: {1}!</b>'\
                .format(status, execStatus.values()))
        self.parent.setExecStatus(user, epname, status, 'EP status changed from REST interface.')
        raise cherrypy.HTTPRedirect('http://{host}/rest/users/{user}#tab_proc'.format(
            host = cherrypy.request.headers['Host'], user = user, epname = epname
        ))

#

# Eof()
