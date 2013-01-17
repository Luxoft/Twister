
# File: ExposedLibraries.py ; This file is part of Twister.

# Copyright (C) 2012 , Luxoft

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
This module contains all functions exposed to TCL, Python and Perl tests.
'''

import os, sys
import platform
import xmlrpclib
from xml.dom.minidom import parse

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print('TWISTER_PATH environment variable is not set! Exiting!')
    exit(1)
sys.path.append(TWISTER_PATH)

try:
    user_name = os.getenv('USER')
except:
    print('Cannot guess user name for this Execution Process! Exiting!')
    exit(1)

platform_sys = platform.system().lower()

fwmconfig_data = parse( open(TWISTER_PATH + '/config/fwmconfig.xml') )
centralEngPort = fwmconfig_data.getElementsByTagName('CentralEnginePort')[0].childNodes[0].data
resAllocPort = fwmconfig_data.getElementsByTagName('ResourceAllocatorPort')[0].childNodes[0].data
del fwmconfig_data

#

# If this computer is Linux
if platform_sys=='linux' or platform_sys=='sunos':

    # This is executed in TEMP
    from __init__ import PROXY

    # # Parse test suites devices configuration
    # raClient = ResourceAllocatorClient(PROXY.replace(centralEngPort, resAllocPort))

    # def queryResource(query):
    #     return raClient.queryResource(query)

    # def createEmptyResource(lvl):
    #     return raClient.createEmptyResource(lvl)

    # def delResource(resid):
    #     return raClient.delResourceLocal(resid)

    # def setProperty(resid,prop,value):
    #     return raClient.setProperty(resid,prop,value)

    # def getProperty(resid,prop):
    #     return raClient.getProperty(resid,prop)

    # def setPropertyLocal(resid,prop,value):
    #     return raClient.setPropertyLocal(resid,prop,value)

    # def getPropertyLocal(resid,prop):
    #     return raClient.getPropertyLocal(resid,prop)

elif platform_sys=='windows' or platform_sys=='java':
    # For Windows, the IP and PORT must be specified manually
    PROXY = 'http://127.0.0.1:{0}/'.format(centralEngPort)

else:
    print('Exposed Libraries: PLATFORM UNSUPPORTED `{0}` !'.format(platform_sys))

    # def queryResource(query):
    #     pass

    # def createEmptyResource(lvl):
    #     pass

    # def delResource(resid):
    #     pass

    # def setProperty(resid,prop,value):
    #     pass

    # def getProperty(resid,prop):
    #     pass

    # def setPropertyLocal(resid,prop,value):
    #     pass

    # def getPropertyLocal(resid,prop):
    #     pass

#
def logMessage(logType, logMessage):
    proxy.logMessage(user_name, logType, logMessage)
#

try:
    proxy = xmlrpclib.ServerProxy(PROXY)
    proxy.echo('exposed-libraries: checking connection...')
    logMsg = logMessage
except:
    def logMsg(logType, logMessage):
        print('[{0}]: {1}'.format(logType, logMessage))

#
