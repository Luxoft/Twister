#!/usr/bin/env python

# version: 2.003

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
if __dir__: chdir(__dir__)




def __main__():
    usage = 'Usage: %prog --of_port <port>'
    version = '%prog v1.0'
    parser = OptionParser(usage=usage, version=version)

    # script options
    parser.add_option('-i', '--eth_interface', action='store', default=None,
                        help='Ethernet interface: eth0 (default).')
    parser.add_option('-o', '--of_port', action='store', default=6633,
                        help='OpenFlow port: 6633 (default).')
    parser.add_option('-u', '--user', action='store', default=None,
                        help='user: None (default).')
    parser.add_option('-t', '--twister_path', action='store', default=None,
                        help='TWISTER_PATH: None (default).')
    (options, args) = parser.parse_args()

    if not options.user:
        print('Cannot guess user name for this Execution Process! Exiting!')

        exit(1)

    if not options.twister_path:
        print('TWISTER_PATH environment variable is not set! exiting!')

        exit(1)

    path.append(options.twister_path)

    from common.configobj import ConfigObj

    from services.PacketSniffer.PacketSniffer import PacketSniffer

    # load execution process configuration
    epConfig = ConfigObj(options.twister_path + '/config/epname.ini')

    snifferConfig = epConfig.pop('PACKETSNIFFERPLUGIN')

    epConfig = list(epConfig.itervalues())

    if not snifferConfig['ENABLED']:
        print 'Packet Sniffer not enabled. exiting..'
        exit(0)

    try:
        snifferIface = snifferConfig['ETH_INTERFACE']
    except Exception, e:
        snifferIface = 'eth0'

    if options.eth_interface:
        snifferIface = options.eth_interface

    # initiate and start sniffer
    sniffer = PacketSniffer(options.user, epConfig,
                        options.of_port, _iface=snifferIface)

    print 'Packet Sniffer start..'

    sniffer.run()

    return




__main__()
