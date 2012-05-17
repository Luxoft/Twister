#!/usr/bin/python

# File: CentralEngine.py ; This file is part of Twister.

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

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print('TWISTER_PATH environment variable is not set! Exiting!')
    exit(1)
sys.path.append(TWISTER_PATH)

from trd_party.BeautifulSoup import BeautifulStoneSoup
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

    # Read XML configuration file
    FMW_PATH = TWISTER_PATH + '/config/fwmconfig.xml'
    if not os.path.exists(FMW_PATH):
        logCritical("CE: Invalid path for config file: `%s` !" % FMW_PATH)
        exit(1)
    else:
        logDebug("CE: XML Config File: `%s`." % FMW_PATH)
        soup = BeautifulStoneSoup(open(FMW_PATH))

    # Server and Port
    try:
        serverIP = socket.gethostbyname(socket.gethostname())
    except:
        serverIP = get_ip_address('eth0')

    serverPort = int(soup.centralengineport.text)
    del soup

    # Start server
    server = SimpleXMLRPCServer((serverIP, serverPort), requestHandler=rpcRequestHandler, logRequests=False)
    logDebug("Started server on IP %s, port %s..." % (serverIP, serverPort))

    # IMPORTANT: Register function SHOULD return value to avoid exceptions on the client side
    server.register_instance(CentralEngine(FMW_PATH))
    server.serve_forever()

#
