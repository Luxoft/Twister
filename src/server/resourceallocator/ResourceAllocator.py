#!/usr/bin/env python

'''
Resource allocator server.
'''

import os
import sys
import socket
from SimpleXMLRPCServer import SimpleXMLRPCServer

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print('TWISTER_PATH environment variable  is not set! Exiting!')
    exit(1)
sys.path.append(TWISTER_PATH)

from ResourceAllocatorClasses import *

#

if __name__ == "__main__":

    # Read devices XML configuration file
    HW_PATH = TWISTER_PATH + '/config/hwconfig.xml'
    if not os.path.exists(HW_PATH):
        logCritical("RA: Invalid path for config file: `%s` !" % HW_PATH)
        exit(1)
    else:
        logDebug("RA: XML Config File: `%s`." % HW_PATH)

    # Server and Port
    serverIP = socket.gethostbyname(socket.gethostname())

    # ResourceAllocator port = CentralEngine port + 1
    serverPort = 8001

    # Start server
    server = SimpleXMLRPCServer((serverIP, serverPort), logRequests=False)
    logDebug("Started Resource allocator server on IP %s, port %s..." % (serverIP, serverPort))
    # IMPORTANT: Register function SHOULD return value to avoid exceptions on the client side
    server.register_instance(ResourceAllocator(HW_PATH))

    server.serve_forever()

#
