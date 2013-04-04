
# File: TestBed.py ; This file is part of Twister.

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

'''
This module contains Functions needed to communicate with Resource Allocator Server.
'''

import os, sys
import platform
import xmlrpclib

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print('TWISTER_PATH environment variable is not set! Exiting!')
    exit(1)
sys.path.append(TWISTER_PATH)

platform_sys = platform.system().lower()

#

# If this computer is Linux
if platform_sys=='linux' or platform_sys=='sunos':

    # This is executed in TEMP
    from __init__ import PROXY

    ra_proxy = xmlrpclib.ServerProxy(PROXY.rstrip('/') + '/ra/')

    try: ra_proxy.echo('TestBed: Checking connection...')
    except: pass

    def getResource(query):
        try: return ra_proxy.getResource(query)
        except: return None

    def setResource(name, parent=None, props={}):
        try: return ra_proxy.setResource(name, parent, props)
        except: return None

    def renameResource(res_query, new_name):
        try: return ra_proxy.renameResource(es_query, new_name)
        except: return None

    def deleteResource(query):
        try: return ra_proxy.deleteResource(query)
        except: return None

    def getResourceStatus(query):
        try: return ra_proxy.getResourceStatus(query)
        except: return None

    def allocResource(query):
        try: return ra_proxy.allocResource(query)
        except: return None

    def reserveResource(query):
        try: return ra_proxy.reserveResource(query)
        except: return None

    def freeResource(query):
        try: return ra_proxy.freeResource(query)
        except: return None


elif platform_sys=='windows' or platform_sys=='java':
    # For Windows, the IP and PORT must be specified manually
    PROXY = 'http://127.0.0.1:8000/'


else:
    print('TestBed: PLATFORM UNSUPPORTED `{0}` !'.format(platform_sys))

    def getResource(query):
        pass

    def setResource(name, parent=None, props={}):
        pass

    def renameResource(res_query, new_name):
        pass

    def deleteResource(query):
        pass

    def getResourceStatus(query):
        pass

    def allocResource(query):
        pass

    def reserveResource(query):
        pass

    def freeResource(query):
        pass

#
