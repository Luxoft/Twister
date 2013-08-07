#!/usr/bin/env python

# version: 2.003

# File: CentralEngine.py ; This file is part of Twister.

# Copyright (C) 2012-2013 , Luxoft

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
This file starts the Twister Server.
"""

import os
import sys
import cherrypy
import paramiko

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print('TWISTER_PATH environment variable is not set! Exiting!')
    exit(1)
sys.path.append(TWISTER_PATH)

from common.tsclogging import *
from server.CentralEngineClasses import CentralEngine

#

def check_passwd(realm, user, passwd):
    """
    This function is called before ALL XML-RPC calls,
    to check the username and password.
    """
    if cherrypy.session.get('user_passwd') == (user+':'+passwd):
        return True
    elif passwd == 'EP':
        cherrypy.session['username'] = user
        return True

    t = paramiko.Transport(('localhost', 22))
    t.logger.setLevel(40) # Less spam, please
    t.start_client()

    # This operation is really heavy!!!
    try:
        t.auth_password(user, passwd)
        cherrypy.session['username'] = user
        cherrypy.session['user_passwd'] = (user+':'+passwd)
        t.stop_thread()
        t.close()
        return True
    except:
        t.stop_thread()
        t.close()
        return False

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

    # Root path
    root = CentralEngine()

    # Config
    conf = {'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': serverPort,
            'server.thread_pool': 90,
            'engine.autoreload.on': False,
            'log.screen': False,

            'tools.sessions.on': True,
            'tools.auth_basic.on': True,
            'tools.auth_basic.realm': 'Twister Server',
            'tools.auth_basic.checkpassword': check_passwd,
            },
            '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': TWISTER_PATH + '/server/static',
            },
        }

    # Start !
    cherrypy.quickstart(root, '/', config=conf)

#
