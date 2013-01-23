#!/usr/bin/env python

# File: ResourceAllocator.py ; This file is part of Twister.

# Copyright (C) 2012-2013 , Luxoft

# Authors:
#    Andrei Costachi <acostachi@luxoft.com>
#    Andrei Toma <atoma@luxoft.com>
#    Cristian Constantin <crconstantin@luxoft.com>
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

'''
Resource allocator server.
'''

import os
import sys
import cherrypy

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print('TWISTER_PATH environment variable is not set! Exiting!')
    exit(1)
sys.path.append(TWISTER_PATH)

from common.tsclogging import *
from server.resourceallocator.ResourceAllocatorClasses import *

#

if __name__ == "__main__":

    serverPort = sys.argv[1:2]

    if not serverPort:
        logCritical('RA: Must start with parameter PORT number!')
        exit(1)
    else:
        try:
            serverPort = int(serverPort[0])
        except:
            logCritical('RA: Must start with parameter PORT number!')
            exit(1)

    # Root path
    root = ResourceAllocator()

    # Config
    conf = {'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': serverPort,
            'server.thread_pool': 30,
            'engine.autoreload.on': False,
            'log.screen': False,
            },
            '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': TWISTER_PATH + '/server/httpserver/static',
            },
        }

    # Start !
    cherrypy.quickstart(root, '/', config=conf)

#
