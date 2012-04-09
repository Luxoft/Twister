
import time

from LibOpenFlow import *

#

def openflow_test():
    '''
    <title>OpenFlow: 008</title>
    <description>Testing Flow Pusher.
    Add changed flow path to controler (for 2 switches), then remove it.
    </description>
    '''

    log_debug('\n=== Starting openflow controller test 8 ===')
    log_debug('Descr: Add changed flow path to controler (for 2 switches), then remove it.')

    restapi = FloodLiteControl('10.9.6.220', 8080)
    flowpusher = StaticFlowPusher('10.9.6.220')
    fl_switches = restapi.get_switches()

    for s in fl_switches:
       print 'DPID: %s' % s['dpid']

    fl_nr = 0
    tm_wait = 30
    fl_list = []

    for ifp in changed_flow_path:
        fl_nr += 1
        fl_name='flow-mod-%i' % fl_nr
        fl_dict={'switch':ifp[0], 'name':fl_name, 'cookie':'0', 'priority':'32768',
            'ingress-port':str(ifp[1]), 'active':'true', 'actions':'output=%i' % ifp[2]}
        fl_list.append(fl_dict)

    log_debug('Done.\n')
    show_switches()
    log_debug('Push new flow to controler...')

    for fl in fl_list:
        flowpusher.set(fl)
        time.sleep(1)
        log_debug('Flow added:\n %s' % str(fl))

    show_switches()

    log_debug ('\nSleep %i seconds before removing the flows...\n' % tm_wait)
    time.sleep(tm_wait)
    log_debug('Removing datapath flows...\n')

    for fl in fl_list:
        flowpusher.remove(None, fl)
        time.sleep(1)
        log_debug('Flow removed:\n %s' % str(fl))

    show_switches()
    return 'PASS'

#

_RESULT = openflow_test()

#
