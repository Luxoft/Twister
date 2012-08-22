
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

TMPL_DATA = """
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	% if title is not UNDEFINED:
	<title>${title}</title>
	% else:
	<title>Central Engine REST</title>
	% endif
	<link type="text/css" rel="stylesheet" href="/static/css/bootstrap.css" />
	<!--[if lt IE 9]><script src="/static/js/html5.js"></script><![endif]-->
	<style>
	* {font-family:DejaVu Sans Mono, Monospace, Courier New, Courier}
	.INFO {color:gray} .DEBUG {color:gray} .ERROR {color:orange} .WARNING {} .CRITICAL {color:red}
	</style>
</head>
<body>

<div class="row-fluid" style="margin-top:10px;">
<div class="span1"></div>
<div class="span11">
<div class="hero-unit">

% if title is not UNDEFINED:
<h1>${title}</h1>
% else:
<h1>Central Engine REST</h1>
% endif
<br>

${body}

</div>
</div>
</div>

<script language="javascript" type="text/javascript" src="/static/js/jquery.min.js"></script>
</body>
</html>
"""
#

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

def prepareLog(log_file):
    if not os.path.isfile(log_file):
        return 'File `{0}` does not exist!'.format(log_file)
    log = open(log_file).read().rstrip()
    body = log.replace('\n', '<br>\n').replace(' ', '&nbsp;')
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

        output = Template(text=TMPL_DATA)
        host = cherrypy.request.headers['Host']
        body = '<p>From here, you can access:<br><br>\n'\
               '<i class="icon-user" style="margin-top:5px;"></i> <a href="http://{host}/rest/stats">User stats</a>&nbsp;  '\
               'and&nbsp;  <i class="icon-list-alt" style="margin-top:5px;"></i> <a href="http://{host}/rest/logs">Logs</a>.</p>'.format(host=host)

        return output.render(body=body)



    @cherrypy.expose
    def new(self):
        ip_port = cherrypy.request.headers['Host']
        machine = platform.uname()[1]
        system  = ' '.join(platform.linux_distribution())
        users   = ['cro', 'jorj', 'bubu'] # self.project.users.keys()

        output = Template(filename=TWISTER_PATH + '/server/centralengine/template_main.htm')
        return output.render(ip_port=ip_port, machine=machine, system=system, users=users)

    @cherrypy.expose
    def users(self, user):
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
        cherrypy.response.headers['Content-Type']  = 'application/json; charset=utf-8'
        cherrypy.response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        cherrypy.response.headers['Pragma']  = 'no-cache'
        cherrypy.response.headers['Expires'] = 0
        data = {'mem': calcMemory(), 'cpu': calcCpu()}
        return json.dumps(data)

    @cherrypy.expose
    def json_logs(self, user='', log=''):
        if user and log:
            logs = self.project.getUserInfo(user, 'log_types')
            log = logs.get(log)
        cherrypy.response.headers['Content-Type']  = 'application/json; charset=utf-8'
        cherrypy.response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        cherrypy.response.headers['Pragma']  = 'no-cache'
        cherrypy.response.headers['Expires'] = 0
        return json.dumps(prepareLog(log or LOG_FILE))



    @cherrypy.expose
    def stats(self, user='', epname='', suite=''):
        """
        This function should be used in the browser.
        It prints a few statistics about the Central Engine.
        """
        if self.user_agent() == 'x':
            return 0

        output = Template(text=TMPL_DATA)
        reversed = dict((v,k) for k,v in execStatus.iteritems())
        now = datetime.datetime.today()
        if now.second < 59:
            now_str = now.replace(second=now.second+1).strftime('%Y-%m-%d %H:%M:%S')
        else:
            now_str = now.replace(minute=now.minute+1, second=0).strftime('%Y-%m-%d %H:%M:%S')
        ce_host = cherrypy.config['server.socket_host']
        ce_port = cherrypy.config['server.socket_port']
        host = cherrypy.request.headers['Host']

        # -- This is before selecting a User
        if not user:
            body = '<p><strong>Running on</strong>: {ce_host}:{ce_port}</p><br>\n'\
                   '<h2>Registered users:</h2>\n'\
                   '<p>{users}.</p>'.format(ce_host=ce_host, ce_port=ce_port, users=';<br>'.join(
                   ['&nbsp;<i class="icon-user" style="margin-top:5px;"></i>&nbsp;user <a href="http://{host}/rest/stats/{user}">{user}</a>\n'
                        .format(host=host, user=k)
                        for k in self.project.users.keys()]
                        ) or 'None')
            return output.render(title='Central Engine', body=body)
        else:
            if user not in self.project.users.keys():
                body = '<b>User name `{0}` doesn\'t exist!</b>'.format(user)
                return output.render(title='Error!', body=body)

        status = reversed[self.project.getUserInfo(user, 'status')]

        if epname:
            if not epname in self.project.getUserInfo(user, 'eps'):
                body = '<b>Execution Process `{0}` doesn\'t exist!</b>'.format(epname)
                return output.render(title='Error!', body=body)

            # -- After selecting a User. EP statistics
            if not suite:
                data = self.project.getEpInfo(user, epname)
                ret = '<h2>Execution Process `<i>{epname}</i>`</h2><br>\n'\
                      '<b>Status</b>: {status}<br><br>\n'\
                      '<b>Ping</b>: {ping}<br><br>\n'\
                      '<b>Suites</b>: [<br>{suites}<br>]\n'.format(
                    epname = epname,
                    status = reversed[data.get('status', STATUS_INVALID)],
                    ping = str( (now - datetime.datetime.strptime(data.get('last_seen_alive', now_str), '%Y-%m-%d %H:%M:%S')).seconds ) + 's',
                    suites = '<br>'.join(['&nbsp;&nbsp;<a href="http://{host}/rest/stats/{user}/{ep}/{id}">{name}</a>'.format(
                        host = host, user = user, ep = epname, id = k, name = v['name'])
                                          for k, v in data['suites'].items()])
                )

            # -- After selecting a User. Suite statistics
            else:
                data = self.project.getSuiteInfo(user, epname, suite)
                reversed = dict((v,k) for k,v in testStatus.iteritems())
                ret = '<h2>Suite `<i>{name}</i>` (id `<i>{suite}</i>`)</h2><br>\n'\
                      '<b>Files</b>: [<br>{files}<br>]'.format(
                    epname = epname,
                    suite = suite,
                    name = data['name'],
                    files = '<br>'.join(['&nbsp;&nbsp;{0}: {1}'.format(data['files'][k]['file'],
                                        reversed[data['files'][k].get('status', STATUS_INVALID)] )
                                        for k in data['files']])
                )

        # -- This is after selecting a User. General user statistics
        else:
            eps = self.project.getUserInfo(user, 'eps').keys()
            try: eps_file = self.project.parsers[user].xmlDict.root.epidsfile.text
            except: eps_file = ''

            ret = '<h2>User `<i>{user}</i>`</h2><br>\n'\
                  '<table class="table">\n'\
                  '<tr><td><b>Status</b></td><td>{status} '\
                  '<small>(<a href="http://{host}/rest/setUserStatus/{user}/2"><i class="icon-play"></i> start</a> | '\
                  '<a href="http://{host}/rest/setUserStatus/{user}/0"><i class="icon-stop"></i> stop</a> | '\
                  '<a href="http://{host}/rest/resetUser/{user}"><i class="icon-warning-sign"></i> reset!</a>)</small>\n'\
                  '<tr><td><b>Master Config</b></td><td><small>{big_config}</small></td></tr>\n'\
                  '<tr><td><b>Tests Config</b></td><td><small>{config}</small></td></tr>\n'\
                  '<tr><td><b>Logs Path</b></td><td><small>{logs_path}</small></td></tr>\n'\
                  '<tr><td><b>EP files</b></td><td><small>{eps_file}</small></td></tr>\n</table><br>\n\n'\
                  '<h3>Processes:</h3><br>\n<ol>{eps}</ol>\n'.format(
                host = host,
                user = user,
                status = status,
                big_config = self.project.getUserInfo(user, 'config_path'),
                config = self.project.getUserInfo(user, 'tests_path'),
                logs_path = self.project.getUserInfo(user, 'logs_path'),
                eps_file = eps_file,
                eps = '\n'.join(
                    ['<li>&nbsp;<a href="http://{host}/rest/stats/{user}/{ep}">{ep}</a>: {status}</li>'.format(
                        user = user, ep=ep, host=host,
                        status=reversed[self.project.getEpInfo(user, ep).get('status', STATUS_INVALID)])
                     for ep in eps]
                )
            )

        return output.render(title='Central Engine Statistics', body=ret)


    @cherrypy.expose
    def status(self, user, epname='', suite=''):
        return self.stats(user, epname, suite)


    @cherrypy.expose
    def resetUser(self, user):
        self.project.reset(user)
        self.parent.resetLogs(user)
        raise cherrypy.HTTPRedirect('http://{host}/rest/stats/{user}'.format(
            host = cherrypy.request.headers['Host'], user = user
        ))


    @cherrypy.expose
    def setUserStatus(self, user, status):
        output = Template(text=TMPL_DATA)
        try: status = int(status)
        except: return output.render(title='Error!', body='<b>Status value `%s` is invalid!</b>' % str(status))
        self.parent.setExecStatusAll(user, status, 'Status changed from REST interface.')
        raise cherrypy.HTTPRedirect('http://{host}/rest/stats/{user}'.format(
            host = cherrypy.request.headers['Host'], user = user
        ))


    @cherrypy.expose
    def setEpStatus(self, user, epname, status):
        output = Template(text=TMPL_DATA)
        try: status = int(status)
        except: return output.render(title='Error!', body='<b>Status value `%s` is invalid!</b>' % str(status))
        self.parent.setExecStatus(user, epname, status, 'Status changed from REST interface.')
        raise cherrypy.HTTPRedirect('http://{host}/rest/stats/{user}/{epname}'.format(
            host = cherrypy.request.headers['Host'], user = user, epname = epname
        ))


    @cherrypy.expose
    def log(self):
        """
        This function should be used in the browser.
        It prints the Central Engine log.
        """
        if self.user_agent() == 'x':
            return 0

        output = Template(text=TMPL_DATA)
        log_body = '<p style="font-family:DejaVu Sans Mono, Monospace, Courier New">' + prepareLog(LOG_FILE) + '</p>'
        return output.render(title='Central Engine Log', body=log_body)


    @cherrypy.expose
    def logs(self):
        return self.log()

#

# Eof()
