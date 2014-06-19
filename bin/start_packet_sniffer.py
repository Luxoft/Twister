#!/usr/bin/env python2.7

# version: 3.000

# This file will start Packet Sniffer
# File: start_packet_sniffer.py ; This file is part of Twister.
#
# Copyright (C) 2012-2013 , Luxoft
#
# Authors:
#    Adrian Toader <adtoader@luxoft.com>
#
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from sys import path
from os import getuid, chdir
from os.path import split

from json import load
from optparse import OptionParser




if getuid() != 0:
    print('To run Packet Sniffer, must be ROOT! Exiting!\n')
    exit(1)


__dir__ = split(__file__)[0]
if __dir__:
    chdir(__dir__)




if __name__ == "__main__":
    USAGE = 'Usage: %prog --of_port <port>'
    VERSION = '%prog v1.0'
    PARSER = OptionParser(usage=USAGE, version=VERSION)

    # script options
    PARSER.add_option('-i', '--eth_interface', action='store', default=None,
                        help='Ethernet interface: eth0 (default).')
    PARSER.add_option('-o', '--of_port', action='store', default=6633,
                        help='OpenFlow port: 6633 (default).')
    PARSER.add_option('-u', '--user', action='store', default=None,
                        help='user: None (default).')
    PARSER.add_option('-t', '--twister_path', action='store', default=None,
                        help='TWISTER_PATH: None (default).')
    (OPTIONS, ARGS) = PARSER.parse_args()

    if not OPTIONS.user:
        print('Cannot guess user name for this Execution Process! Exiting!')

        exit(1)

    if not OPTIONS.twister_path:
        print('TWISTER_PATH environment variable is not set! exiting!')

        exit(1)

    path.append(OPTIONS.twister_path)

    from ConfigParser import SafeConfigParser

    from services.PacketSniffer.PacketSniffer import Sniffer

    # load execution process configuration
    _EP_CONFIG = dict()
    EP_CONFIG = SafeConfigParser()
    EP_CONFIG.read(OPTIONS.twister_path + '/config/epname.ini')
    for s in [_s for _s in EP_CONFIG.sections() if not _s == 'PACKETSNIFFERPLUGIN'
                                                    and EP_CONFIG.has_option(_s, 'ENABLED')
                                                    and EP_CONFIG.get(_s, 'ENABLED')]:
        _EP_CONFIG.update([(s, {'CE_IP': EP_CONFIG.get(s, 'CE_IP'), 'CE_PORT': EP_CONFIG.get(s, 'CE_PORT')}), ])

    EP_CONFIG = list(_EP_CONFIG.itervalues())

    # initiate and start SNIFFER
    SNIFFER = Sniffer(user=OPTIONS.user, epConfig=EP_CONFIG,
                        OFPort=OPTIONS.of_port, iface=OPTIONS.eth_interface)

    print 'Packet Sniffer start..'

    SNIFFER.run()

