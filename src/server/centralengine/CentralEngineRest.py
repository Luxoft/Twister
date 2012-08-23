
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
import datetime
import platform
import cherrypy
from mako.template import Template

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print('$TWISTER_PATH environment variable is not set! Exiting!')
    exit(1)
sys.path.append(TWISTER_PATH)

from common.constants import *
from common.tsclogging import LOG_FILE

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
    body = log.replace('\n', '<br>\n').replace(' ', '&nbsp;')
    del log
    body = body.replace(';INFO&',   ';<b style="color:gray">INFO</b>&')
    body = body.replace(';DEBUG&',  ';<b style="color:gray">DEBUG</b>&')
    body = body.replace(';ERROR&',  ';<b style="color:orange">ERROR</b>&')
    body = body.replace(';WARNING&',  ';<b style="color:orange">WARNING</b>&')
    body = body.replace(';CRITICAL&', ';<b style="color:red"L>CRITICAL</b>&')
    return body

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
        statuses = [ reversed[eps[ep].get('status', STATUS_INVALID)] for ep in eps ]
        logs = self.project.getUserInfo(user, 'log_types')

        output = Template(filename=TWISTER_PATH + '/server/centralengine/template_user.htm')
        return output.render(host=host, user=user, status=status, master_config=master_config, proj_config=proj_config,
                             logs_path=logs_path, eps_file=eps_file, eps=eps, statuses=statuses, logs=logs)


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
    def json_logs(self, user='', log=''):
        if self.user_agent() == 'x':
            return 0

        if user and log:
            logs = self.project.getUserInfo(user, 'log_types')
            log = logs.get(log)

        cherrypy.response.headers['Content-Type']  = 'application/json; charset=utf-8'
        cherrypy.response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        cherrypy.response.headers['Pragma']  = 'no-cache'
        cherrypy.response.headers['Expires'] = 0
        return json.dumps(prepareLog(log or LOG_FILE))


    @cherrypy.expose
    def resetUser(self, user):
        self.project.reset(user)
        self.parent.resetLogs(user)
        raise cherrypy.HTTPRedirect('http://{host}/rest/users/{user}'.format(
            host = cherrypy.request.headers['Host'], user = user
        ))


    @cherrypy.expose
    def setUserStatus(self, user, status):
        output = Template(text=TMPL_DATA)
        try: status = int(status)
        except: return output.render(title='Error!', body='<b>Status value `%s` is invalid!</b>' % str(status))
        self.parent.setExecStatusAll(user, status, 'Status changed from REST interface.')
        raise cherrypy.HTTPRedirect('http://{host}/rest/users/{user}'.format(
            host = cherrypy.request.headers['Host'], user = user
        ))


    @cherrypy.expose
    def setEpStatus(self, user, epname, status):
        output = Template(text=TMPL_DATA)
        try: status = int(status)
        except: return output.render(title='Error!', body='<b>Status value `%s` is invalid!</b>' % str(status))
        self.parent.setExecStatus(user, epname, status, 'Status changed from REST interface.')
        raise cherrypy.HTTPRedirect('http://{host}/rest/users/{user}/{epname}'.format(
            host = cherrypy.request.headers['Host'], user = user, epname = epname
        ))

#

# Eof()
