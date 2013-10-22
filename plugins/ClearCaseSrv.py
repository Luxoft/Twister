
# File: ClearCaseSrv.py ; This file is part of Twister.

# version: 2.001

# Copyright (C) 2012-2013 , Luxoft

# Authors:
#    Adrian Toader <adtoader@luxoft.com>
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

from __future__ import print_function

import os
import sys
import re
import socket
socket.setdefaulttimeout(5)
import xmlrpclib

import cherrypy
from cherrypy import _cptools

try: import simplejson as json
except: import json

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print('TWISTER_PATH environment variable is not set! Exiting!')
    exit(1)
if TWISTER_PATH not in sys.path:
    sys.path.append(TWISTER_PATH)

try:
    import cleartool
except Exception as e:
    print('Cannot import ClearTool !'.format(e))

#

class CC(_cptools.XMLRPCController):


    @cherrypy.expose
    def hello(self):
        """
        Hello function, for testing connection.
        """
        return True


    @cherrypy.expose
    def cmd(self, args):
        """
        Send cleartool command.
        setview ... endview ... ls ...
        """
        if not isinstance(args, dict):
            return False

        args = {k: v[0] if isinstance(v, list) else v for k, v in args.iteritems()}

        if not args.has_key('command') or not isinstance(args['command'], str):
            return False

        if args['command'] == 'exit':
            print('Clearcase Plugin Srv: Shutting down...')
            cherrypy.engine.exit()
        elif args['command'].startswith('setview'):
            print('Clearcase Plugin Srv: Changing view: `{}`.'.format(args['command']))

        _r = cleartool.cmd(args['command'])

        response = {
            'status': _r[0],
            'data':   _r[1],
            'error':  _r[2],
        }

        return json.dumps(response)


    @cherrypy.expose
    def getTestDescription(self, user, fname):
        """
        Returns the title, description and all tags from a test file.
        """
        try: text = open(fname,'rb').read()
        except: return ''

        li_tags = re.findall('^[ ]*?[#]*?[ ]*?<(?P<tag>\w+)>([ -~\n]+?)</(?P=tag)>', text, re.MULTILINE)
        tags = '<br>\n'.join(['<b>' + title + '</b> : ' + descr.replace('<', '&lt;') for title, descr in li_tags])

        data = cleartool.cmd( 'ls {}'.format(fname) )[1]
        if data:
            data = data.split()[0].split('@@')[1]
            extra_info = '<b>ClearCase Version</b> : {}'.format(data)

        return tags + '<br>\n' + extra_info


    @cherrypy.expose
    def getTestFile(self, fname):
        """
        Send 1 ClearCase file.
        """
        try: open(fname,'r')
        except: return ''

        with open(fname, 'rb') as handle:
            return xmlrpclib.Binary(handle.read())

#

if __name__ == "__main__":

    serverPort = sys.argv[1:2]

    if not serverPort:
        print('Clearcase Plugin Srv: Must start with parameter PORT number!')
        exit(1)
    else:
        try:
            serverPort = int(serverPort[0])
        except:
            print('Clearcase Plugin Srv: Must start with parameter PORT number!')
            exit(1)

    # Config
    conf = {'global': {
            'server.socket_host': '127.0.0.1',
            'server.socket_port': serverPort,
            'server.thread_pool': 2,
            'engine.autoreload.on': False,
            'log.screen': False
            }
        }

    print('Starting Clearcase Plugin Srv on `{}`.'.format(serverPort))

    # Start !
    cherrypy.quickstart(CC(), '/', config=conf)

    print('Ending Clearcase Plugin Srv from `{}`.'.format(serverPort))
