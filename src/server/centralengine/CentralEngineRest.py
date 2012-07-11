
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
import datetime
import cherrypy

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print('$TWISTER_PATH environment variable is not set! Exiting!')
    exit(1)
sys.path.append(TWISTER_PATH)

from common.constants import *
from common.tsclogging import LOG_FILE

#

class CentralEngineRest:

    def __init__(self, project):

        self.project = project


    def _user_agent(self):
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

        host = cherrypy.request.headers['Host']

        return '<head><title>Central Engine REST</title></head>\n'\
               '<body>'\
               '<h3>Central Engine REST</h3>'\
               '<p>From here, you can access:<br><br>'\
               '<a href="http://{host}/rest/stats">Stats</a>  and  <a href="http://{host}/rest/logs">Logs</a>.</p>'\
               '</body>'.format(host=host)


    @cherrypy.expose
    def stats(self, user='', epname='', suite=''):
        """
        This function should be used in the browser.
        It prints a few statistics about the Central Engine.
        """
        if self._user_agent == 'x':
            return 0

        reversed = dict((v,k) for k,v in execStatus.iteritems())
        now = datetime.datetime.today()
        if now.second < 59:
            now_str = now.replace(second=now.second+1).strftime('%Y-%m-%d %H:%M:%S')
        else:
            now_str = now.replace(minute=now.minute+1, second=0).strftime('%Y-%m-%d %H:%M:%S')
        ce_host = cherrypy.config['server.socket_host']
        ce_port = cherrypy.config['server.socket_port']
        host = cherrypy.request.headers['Host']

        if not user:
            return '<head><title>Central Engine Statistics</title></head>\n'\
                   '<body>'\
                   '<h3>Central Engine statistics</h3>'\
                   '<h3>Registered users:</h3>\n'\
                   '{users}.'\
                   '</body>'.format(users=';<br>'.join(
                   ['&nbsp;&nbsp;<a href="http://{host}/stats?user={user}">{user}</a>'.format(host = host, user=k)
                    for k in self.project.users.keys()]
                    ) or 'None')

        status = reversed[self.project.getUserInfo(user, 'status')]

        if epname:
            if not epname in self.project.getUserInfo(user, 'eps'):
                return '<b>Execution Process `{0}` doesn\'t exist!</b>'.format(epname)

            # EP name only
            if not suite:
                data = self.project.getEpInfo(user, epname)
                ret = '<head><title>Central Engine Statistics</title></head>\n'\
                      '<body>'\
                      '<h3>Execution Process `{epname}`</h3>'\
                      '<b>Status</b>: {status}<br><br>'\
                      '<b>Ping</b>: {ping}<br><br>'\
                      '<b>Suites</b>: [<br>{suites}<br>]'\
                      '</body>'.format(
                    epname = epname,
                    status = reversed[data.get('status', STATUS_INVALID)],
                    ping = str( (now - datetime.datetime.strptime(data.get('last_seen_alive', now_str), '%Y-%m-%d %H:%M:%S')).seconds ) + 's',
                    suites = '<br>'.join(['&nbsp;&nbsp;<a href="http://{host}/stats?user={user}&epname={ep}&suite={s}">{s}</a>'.format(
                        host = host, user = user, ep = epname, s = k)
                                          for k in data['suites'].keys()])
                )

            # EP name and Suite name
            else:
                data = self.project.getSuiteInfo(user, epname, suite)
                reversed = dict((v,k) for k,v in testStatus.iteritems())
                ret = '<head><title>Central Engine Statistics</title></head>\n'\
                      '<body>'\
                      '<h3>EP `{epname}` -> Suite `{suite}`</h3>'\
                      '<b>Files</b>: [<br>{files}<br>]'\
                      '</body>'.format(
                    epname = epname,
                    suite = suite,
                    files = '<br>'.join(['&nbsp;&nbsp;{0}: {1}'.format(data['files'][k]['file'], reversed[data['files'][k]['status']] )
                                         for k in data['files']])
                )

        # General statistics
        else:
            eps = self.project.getUserInfo(user, 'eps').keys()
            ret = '<head><title>Central Engine Statistics</title></head>\n'\
                  '<body>'\
                  '<h3>Central Engine statistics for user `{user}`</h3>'\
                  '<b>Running on</b>: {host}:{port}<br><br>'\
                  '<b>Status</b>: {status}<br><br>'\
                  '<b>Processes</b>: [<br>{eps}<br>]'\
                  '</body>'.format(
                user = user,
                status = status,
                host = ce_host,
                port = ce_port,
                eps = '<br>'.join(
                    ['&nbsp;&nbsp;<a href="http://{host}/stats?user={user}&epname={ep}">{ep}</a>: {status}'.format(
                        user = user, ep=ep, host=host,
                        status=reversed[self.project.getEpInfo(user, ep).get('status', STATUS_INVALID)])
                     for ep in eps]
                )
            )

        return ret


    @cherrypy.expose
    def status(self, user, epname='', suite=''):
        return self.stats(user, epname, suite)


    @cherrypy.expose
    def log(self):
        """
        This function should be used in the browser.
        It prints the Central Engine log.
        """
        if self._user_agent == 'x':
            return 0

        log = open(LOG_FILE).read()
        return '<head><title>Central Engine Log</title></head>\n'\
               '<body>' + log.replace('\n', '<br>') + \
               '</body>'


    @cherrypy.expose
    def logs(self):
        return self.log()

#

# Eof()
