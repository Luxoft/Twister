
'''
This module contains all functions exposed to TCL and Python tests.
'''

import os, sys
import platform
import xmlrpclib

TWISTER_PATH=os.getenv('TWISTER_PATH')
if(not TWISTER_PATH):
    print 'TWISTER_PATH environment variable  is not set'
    exit(1)    
sys.path.append(TWISTER_PATH)

platform_sys = platform.system().lower()

#

# If this computer is Linux
if platform_sys=='linux' or platform_sys=='sunos':
    # This is executed in TEMP
    #sys.path.append(os.getenv('HOME') + '/twister/Sources/Python')
    
    from client.resourceallocator.ResourceAllocatorClient import *
    from __init__ import PROXY

    # Parse test suites devices configuration
    raClient = ResourceAllocatorClient(PROXY.replace('8000', '8001'))

    def queryResource(query):
        return raClient.queryResource(query)

    def createEmptyResource(lvl):
        return raClient.createEmptyResource(lvl)

    def delResource(resid):
        return raClient.delResourceLocal(resid)

    def setProperty(resid,prop,value):
        return raClient.setProperty(resid,prop,value)

    def getProperty(resid,prop):
        return raClient.getProperty(resid,prop)

    def setPropertyLocal(resid,prop,value):
        return raClient.setPropertyLocal(resid,prop,value)

    def getPropertyLocal(resid,prop):
        return raClient.getPropertyLocal(resid,prop)

elif platform_sys=='windows' or platform_sys=='java':
    # For Windows, the IP and PORT must be specified manually
    PROXY = 'http://11.126.32.9:8000/'   # Tsc Server
    #PROXY = 'http://11.126.32.12:8000/' # Dan Ubuntu
    #PROXY = 'http://11.126.32.14:8000/' # Cro Windows
    #PROXY = 'http://10.0.1.15:8000/'    # OpenSUSE VM

else:
    print('Exposed Libraries: PLATFORM UNSUPPORTED `{0}` !'.format(platform_sys))

    def queryResource(query):
        pass

    def createEmptyResource(lvl):
        pass

    def delResource(resid):
        pass

    def setProperty(resid,prop,value):
        pass

    def getProperty(resid,prop):
        pass

    def setPropertyLocal(resid,prop,value):
        pass

    def getPropertyLocal(resid,prop):
        pass

#

try:
    proxy = xmlrpclib.ServerProxy(PROXY)
    proxy.echo('exposed-libraries: checking connection...')
    logMsg = proxy.logMessage
except:
    def logMsg(logType, logMessage):
        print('[{0}]: {1}'.format(logType, logMessage))

#
