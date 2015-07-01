#!/usr/bin/env python2.7

# version: 3.008

# File: CentralEngine.py ; This file is part of Twister.

# Copyright (C) 2012-2014 , Luxoft

# Authors:
#    Andrei Costachi <acostachi@luxoft.com>
#    Cristi Constantin <crconstantin@luxoft.com>
#    Daniel Cioata <dcioata@luxoft.com>
#    Mihai Tudoran <mtudoran@luxoft.com>

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

import cherrypy
cherrypy.log.access_log.propagate = False
cherrypy.log.error_log.setLevel(10)

import os
import sys
import thread
from rpyc.utils.server import ThreadPoolServer

if not sys.version.startswith('2.7'):
    print 'Python version error! Central Engine must run on Python 2.7!'
    exit(1)

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print 'TWISTER_PATH environment variable is not set! Exiting!'
    exit(1)
if TWISTER_PATH not in sys.path:
    sys.path.append(TWISTER_PATH)

from common.tsclogging import logDebug, logInfo, logWarning, logError, logCritical
from common.tsclogging import setLogLevel
from server.CeProject  import Project
from server.CeXmlRpc   import CeXmlRpc
from server.CeRpyc     import CeRpycService
from common import iniparser

#

if __name__ == "__main__":

    if os.getuid() != 0:
        logWarning('Twister Server should run as ROOT! If it doesn\'t, '
                   'it won\'t be able to read config files and write logs for all users!')

    SERVER_PORT = sys.argv[1:2]

    if not SERVER_PORT:
        logCritical('Twister Server: Must start with parameter PORT number!')
        exit(1)
    else:
        try:
            SERVER_PORT = int(SERVER_PORT[0])
        except Exception:
            logCritical('Twister Server: Must start with parameter PORT number!')
            exit(1)

    # Read verbosity from configuration
    CFG_PATH = '{}/config/server_init.ini'.format(TWISTER_PATH)
    VERBOSITY = 20
    if os.path.isfile(CFG_PATH):
        CFG = iniparser.ConfigObj(CFG_PATH)
        VERBOSITY = CFG.get('verbosity', 20)
        del CFG

    RET = setLogLevel(VERBOSITY)
    if not RET:
        logError('Log: The Log level will default to INFO.')

    # RPyc config
    CONFIG = {
        'allow_pickle': True,
        'allow_getattr': True,
        'allow_setattr': True,
        'allow_delattr': True,
        'allow_all_attrs': True,
        }

    # Diff RPyc port
    RPYC_PORT = SERVER_PORT + 10
    try:
        RPYC_SERVER = ThreadPoolServer(CeRpycService, port=RPYC_PORT, protocol_config=CONFIG)
        RPYC_SERVER.logger.setLevel(30)
    except Exception:
        logCritical('Twister Server: Cannot launch the RPyc server on port `{}`!'.format(RPYC_PORT))
        exit(1)

    # Project manager does everything
    PROJ = Project()
    PROJ.rsrv = RPYC_SERVER
    # CE is the XML-RPC interface
    CE = CeXmlRpc(PROJ)

    def close():
        """ Close server. """
        RPYC_SERVER.close()
        del PROJ.manager

    PROJ.ip_port = ('127.0.0.1', SERVER_PORT)
    CE.web = PROJ.web
    CE.tb = PROJ.testbeds
    CE.sut = PROJ.sut
    CE.report = PROJ.report

    # EE Manager is the helper for EPs and Clients
    # Inject the project as variable for EE
    RPYC_SERVER.service.inject_object('project', PROJ)
    RPYC_SERVER.service.inject_object('cherry', CE)

    # Start rpyc server
    thread.start_new_thread(RPYC_SERVER.start, ())
    logInfo('RPYC Serving on 0.0.0.0:{}'.format(RPYC_PORT))


    # CherryPy config
    CONF = {
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': SERVER_PORT,
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
            'tools.sessions.on': False,
            'tools.auth_basic.on': False,
            'tools.auth_digest.on': False,
            'tools.auth.on': False,
            'tools.staticdir.on': True,
            'tools.staticdir.dir': TWISTER_PATH + '/server/static',
        },
    }

    # Start !
    cherrypy.engine.signal_handler.handlers['SIGTERM'] = close
    cherrypy.quickstart(CE, '/', config=CONF)

#
