#!/usr/bin/env python

'''
Resource allocator server.
'''

import os
import sys
import socket
from SimpleXMLRPCServer import SimpleXMLRPCServer

TWISTER_PATH=os.getenv('TWISTER_PATH')

if(not TWISTER_PATH):
    print 'TWISTER_PATH environment variable  is not set'
    exit(1)        
sys.path.append(TWISTER_PATH)

from ResourceAllocatorClasses import *

if __name__ == "__main__":

    # Initialization
    """
    if not os.getenv('TSCBASE_PATH'):
        TSCBASE_PATH = os.getenv('HOME') + '/twister/'
        logWarning('TSCBASE_PATH is not set, using `%s`!' % TSCBASE_PATH)
        if not os.path.exists(TSCBASE_PATH):
            logCritical("RA: Invalid base path: `%s` !" % TSCBASE_PATH)
            exit(1)
    else:
        TSCBASE_PATH = os.getenv('TSCBASE_PATH')

    logDebug("RA: TSC Base Path: `%s`." % TSCBASE_PATH)
    """
    
    # Read devices XML configuration file
    devices_config = TWISTER_PATH + os.sep + "config/hwdevices.xml"
    if not os.path.exists(devices_config):
        logCritical("RA: Invalid path for config file: `%s` !" % devices_config)
        exit(1)
    else:
        logDebug("RA: XML Config File: `%s`." % devices_config)

    # Server and Port
    serverIP = socket.gethostbyname(socket.gethostname())

    # ResourceAllocator server port = CentralEngine port + 1
    serverPort = 8001

    # Start server
    server = SimpleXMLRPCServer((serverIP, serverPort), logRequests=False)
    logDebug("Started Resource allocator server on IP %s, port %s..." % (serverIP, serverPort))
    # IMPORTANT: Register function SHOULD return value to avoid exceptions on the client side
    server.register_instance(ResourceAllocator(devices_config))

    server.serve_forever()

#
