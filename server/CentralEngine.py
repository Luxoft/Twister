#!/usr/bin/env python2.7

# version: 2.009

# File: CentralEngine.py ; This file is part of Twister.

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

"""
This file starts the Twister Server.
"""

# Patch for _DummyThread __stop error
import threading
threading._DummyThread._Thread__stop = lambda x: 1

import os
import sys
import thread
import cherrypy
from rpyc.utils.server import ThreadPoolServer

if not sys.version.startswith('2.7'):
    print('Python version error! Central Engine must run on Python 2.7!')
    exit(1)

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print('TWISTER_PATH environment variable is not set! Exiting!')
    exit(1)
if TWISTER_PATH not in sys.path:
    sys.path.append(TWISTER_PATH)


from common.tsclogging import *
from server.CeProject  import Project
from server.CeXmlRpc   import CeXmlRpc
from server.CeRpyc     import CeRpycService

#

if __name__ == "__main__":

    if os.getuid() != 0:
        logWarning('Twister Server should run as ROOT! If it doesn\'t, '
                   'it won\'t be able to read config files and write logs for all users!')

    serverPort = sys.argv[1:2]

    if not serverPort:
        logCritical('Twister Server: Must start with parameter PORT number!')
        exit(1)
    else:
        try:
            serverPort = int(serverPort[0])
        except:
            logCritical('Twister Server: Must start with parameter PORT number!')
            exit(1)

    # RPyc config
    config = {
        'allow_pickle': True,
        'allow_getattr': True,
        'allow_setattr': True,
        'allow_delattr': True,
        'allow_all_attrs': True,
        }

    # Diff RPyc port
    rpycPort = serverPort + 10
    try:
        rpycServer = ThreadPoolServer(CeRpycService, port=rpycPort, protocol_config=config)
    except:
        logCritical('Twister Server: Cannot launch the RPyc server on port `{}`!'.format(rpycPort))
        exit(1)

    # Project manager does everything
    proj = Project()
    proj.rsrv = rpycServer
    # CE is the XML-RPC interface
    ce = CeXmlRpc(proj)

    def close():
        global proj, rpycServer
        rpycServer.close()
        del proj.manager

    proj.ip_port = ('127.0.0.1', serverPort)
    ce.web = proj.web
    ce.ra  = proj.ra
    ce.report = proj.report

    # EE Manager is the helper for EPs and Clients
    # Inject the project as variable for EE
    rpycServer.service.inject_object('project', proj)
    rpycServer.service.inject_object('cherry', ce)
    # Less spam please !
    rpycServer.logger.setLevel(30)

    # Start rpyc server
    thread.start_new_thread(rpycServer.start, ())
    logInfo('RPYC Serving on 0.0.0.0:{}'.format(rpycPort))


    # CherryPy config
    conf = {'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': serverPort,
            'server.thread_pool': 90,
            'engine.autoreload.on': False,
            'log.screen': False,

            'tools.sessions.on': True,
            'tools.sessions.timeout': 60*24*365,
            'tools.auth_basic.on': True,
            'tools.auth_basic.realm': 'Twister Server',
            'tools.auth_basic.checkpassword': Project.check_passwd,
            },
            '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': TWISTER_PATH + '/server/static',
            },
        }

    # Start !
    cherrypy.engine.signal_handler.handlers['SIGTERM'] = close
    cherrypy.quickstart(ce, '/', config=conf)

#
