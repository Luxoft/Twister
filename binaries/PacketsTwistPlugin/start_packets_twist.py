#!/usr/bin/env python

# This file will start Packets Twists


from os import getuid, chdir, getenv, environ
from os.path import split

from json import load
from optparse import OptionParser

from PacketsTwist import PacketsTwist




if getuid() != 0:
    print('To run Packets Twist, must be ROOT! Exiting!\n')
    exit(1)


__dir__ = split(__file__)[0]
if __dir__: chdir(__dir__)


# # # #

def __main__():
    usage = 'Usage: %prog --of_port <port>'
    version = '%prog v1.0'
    parser = OptionParser(usage=usage, version=version)

    # script options
    parser.add_option('-o', '--of_port', action='store', default=6633,
                        help='OpenFlow port: 6633 (default).')
    parser.add_option('-u', '--user', action='store', default=None,
                        help='user: None (default).')
    (options, args) = parser.parse_args()

    if not options.user:
        print('Cannot guess user name for this Execution Process! Exiting!')

        exit(1)

    environ['TWISTER_PATH'] = getenv('HOME') + '/twister'

    # load execution process configuration
    epConfig = load(open(getenv('TWISTER_PATH') + '/bin/config_ep.json'))

    # initiate and start sniffer
    pt = PacketsTwist(options.user, epConfig, options.of_port)

    pt.run()

    return

# # # #


__main__()
