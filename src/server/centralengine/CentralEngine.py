#!/usr/bin/python

'''
This file contains configurations for Central Engine:
  - Base path
  - Config path
If the file is executed with Python, it will start the Engine.
'''

import os
import sys
import socket
import struct

from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler

TWISTER_PATH=os.getenv('TWISTER_PATH')
if(not TWISTER_PATH):
    print 'TWISTER_PATH environment variable  is not set'
    exit(1)    
sys.path.append(TWISTER_PATH)

from server.centralengine.CentralEngineClasses import *
from common.tsclogging import *
from common.xmlparser import *
CLIENTS_IP = []

#

def get_ip_address(ifname):
    try: import fcntl
    except: print('Fatal Error get IP adress!') ; exit(1)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(), 0x8915, struct.pack('256s', ifname[:15]) )[20:24])

class rpcRequestHandler(SimpleXMLRPCRequestHandler):
    def __init__(self, request, client_address, server):
        global CLIENTS_IP
        if not client_address[0] in CLIENTS_IP:
            CLIENTS_IP.append(client_address[0])
            logDebug('CE: New client connected : [ IP {0} ]'.format(client_address[0]))
        SimpleXMLRPCRequestHandler.__init__(self, request, client_address, server)

#

if __name__ == "__main__":

    # Initialization    
    logDebug("CE: TWISTER_PATH: `%s`." % TWISTER_PATH)

    # Read XML configuration file
    FMW_PATH = TWISTER_PATH + os.sep + "config/fwmconfig.xml"
    if not os.path.exists(FMW_PATH):
        logCritical("CE: Invalid path for config file: `%s` !" % FMW_PATH)
        exit(1)
    else:
        logDebug("CE: XML Config File: `%s`." % FMW_PATH)

    # Server and Port
    try:
        serverIP = socket.gethostbyname(socket.gethostname())
    except:
        serverIP = get_ip_address('eth0')
    serverPort = 8000

    # Start server
    server = SimpleXMLRPCServer((serverIP, serverPort), requestHandler=rpcRequestHandler, logRequests=False)
    logDebug("Started server on IP %s, port %s..." % (serverIP, serverPort))

    # IMPORTANT: Register function SHOULD return value to avoid exceptions on the client side
    server.register_instance(CentralEngine(FMW_PATH))
    server.serve_forever()

#
