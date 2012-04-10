
import time

from LibOpenFlow import *

#

def openflow_test_5():
    '''
    <title>OpenFlow: 005</title>
    <description>Testing Flow Pusher.
    Disable one port.</description>
    '''

    log_debug('\n=== Starting openflow controller test 5 ===\n')
    restapi = FloodLiteControl('10.9.6.220', 8080)
    flowpusher = StaticFlowPusher('10.9.6.220')
    switches = restapi.get_switches()

    DPID = switches[0]['dpid']
    PORT = '18'

    log_debug('Found %i devices. Will disable port %s for switch `%s`.' %
        ( len(switches), PORT, DPID))

    # Specifying no actions will cause the packets to be dropped
    fl_dict = {'switch':DPID, 'name':'flow-mod-1', 'cookie':'0', 'priority':'32768',
            'ingress-port':PORT, 'active':'true', 'actions':''}

    flowpusher.set(fl_dict)
    log_debug('Port `%s` is now disabled.' % PORT)

    show_switches()

    log_debug ('\nSleep a little before enabling the port back...\n')
    time.sleep(10)

    flowpusher.remove(fl_dict)

    show_switches()

    return 'PASS'

#

_RESULT = openflow_test_5()

#
