
from LibOpenFlow import *

#

def openflow_test_4():
    '''
    <title>OpenFlow: 004</title>
    <description>This test shows topology lings for devices registered in the FloodLite controller.</description>
    '''

    log_debug('\n=== Starting openflow controller test 4 ===\n')
    restapi = FloodLiteControl('10.9.6.220', 8080)

    log_debug('~~ Topology links from floodlight controler ~~\n')
    topo_links = restapi.get_topology_links()

    for tl in topo_links:
        log_debug("src-swich: %s -> dst-switch: %s" %       (tl['src-switch'], tl['dst-switch']))
        log_debug("src-port: %s  -> dst-port:   %s\n" %     (tl['src-port'],   tl['dst-port']))

    show_switches()

    return 'PASS'

#

_RESULT = openflow_test_4()

#
