
import time

from LibOpenFlow import *

#

def openflow_test():
    '''
    <title>OpenFlow: 006</title>
    <description>Testing Flow Pusher.
    Add single flow to switch, then remove it.
    </description>
    '''

    log_debug('\n=== Starting openflow controller test 6 ===\n')
    log_debug('Descr: Add single flow to switch, then remove it.')

    restapi = FloodLiteControl('10.9.6.220', 8080)
    flowpusher = StaticFlowPusher('10.9.6.220')
    fl_switches = restapi.get_switches()

    for s in fl_switches:
       print 'DPID: %s' % s['dpid']

    fl_nr = 0
    fl_list = []

    for ifp in single_switch_flow:
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

    log_debug ('\nSleep a little, before removing the flows...\n')
    time.sleep(10)
    log_debug('Removing datapath flows...\n')

    for fl in fl_list:
        flowpusher.remove(fl)
        time.sleep(1)
        log_debug('Flow removed:\n %s' % str(fl))

    show_switches()
    return 'PASS'

#

_RESULT = openflow_test()

#
