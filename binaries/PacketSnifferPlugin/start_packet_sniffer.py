#!/usr/bin/env python

# version: 2.002

# This file will start Packet Sniffer


from sys import path
from os import getuid, chdir
from os.path import split

from json import load
from optparse import OptionParser

#

if getuid() != 0:
    print('To run Packet Sniffer, must be ROOT! Exiting!\n')
    exit(1)


__dir__ = split(__file__)[0]
if __dir__: chdir(__dir__)


# # # #

def __main__():
    usage = 'Usage: %prog --of_port <port>'
    version = '%prog v1.0'
    parser = OptionParser(usage=usage, version=version)

    # script options
    parser.add_option('-i', '--eth_interface', action='store', default='eth0',
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
    epConfig.pop('PACKETSNIFFERPLUGIN')
    epConfig = list(epConfig.itervalues())

    # initiate and start sniffer
    pt = PacketSniffer(options.user, epConfig, options.of_port, filters={'-i': options.eth_interface})

    pt.run()

    print 'Packet Sniffer started'

    return

# # # #

__main__()
