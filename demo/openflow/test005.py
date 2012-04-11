
import os, sys, time

sys.path.append(os.getenv('TWISTER_PATH') + '/.twister_cache/ce_libs/')

#

def openflow_test_5():
    '''
    <title>OpenFlow: 005</title>
    <description>Testing Flow Pusher.
    Disable one port.</description>
    '''

    from LibOpenFlow import log_debug, show_switches, FloodLiteControl, StaticFlowPusher

    log_debug('\n=== Starting openflow controller test 5 ===\n')
    restapi = FloodLiteControl('10.9.6.220', 8080)
    flowpusher = StaticFlowPusher('10.9.6.220')
    switches = restapi.get_switches()

    log_debug('Found %i devices.' % len(switches))

    PORT = '34'

    for s in switches:
        DPID = s['dpid']
        log_debug('Will disable port %s for switch `%s`.' % (PORT, DPID))

        # Specifying no actions will cause the packets to be dropped
        fl_dict = {'switch':DPID,'ingress-port':PORT,'name':'disable-34','cookie':'0','priority':'32768','actions':''}

        flowpusher.set(fl_dict)
        log_debug('Port `%s` is now disabled.' % PORT)

    show_switches()

    log_debug ('\nSleep a little before enabling the port back...\n')
    time.sleep(25)

    for s in switches:
        DPID = s['dpid']
        fl_dict = {'switch':DPID,'ingress-port':PORT,'name':'disable-34','cookie':'0','priority':'32768','actions':''}

        flowpusher.remove(fl_dict)
        log_debug('Port `%s` for switch `%s` is now enabled.' % (PORT, DPID))

    show_switches()

    return 'PASS'

#

_RESULT = openflow_test_5()

#
