
import os, sys, time

sys.path.append(os.getenv('TWISTER_PATH') + '/.twister_cache/ce_libs/')

from LibOpenFlow import *

#

def openflow_test():
    '''
    <title>OpenFlow: 009</title>
    <description>Testing Flow Pusher.
    Add changed path to floodlight controller.
    </description>
    '''

    log_debug('\n=== Starting openflow controller test 9 ===')
    log_debug('Descr: Add changed path to floodlight controller.')

    restapi = FloodLiteControl('10.9.6.220', 8080)
    flowpusher = StaticFlowPusher('10.9.6.220')
    fl_switches = restapi.get_switches()

    for s in fl_switches:
       print 'DPID: %s' % s['dpid']

    # ----------------------------------------------------------------------------------------------
    # Add settings for CHANGED DATAPATH
    # ----------------------------------------------------------------------------------------------
    fl_nr = 0
    tm_wait = 30
    fl_list = []

    for ifp in changed_flow_path:
        fl_nr += 1
        fl_name='flow-mod-%i' % fl_nr
        if ifp[2]:
            fl_dict={'switch':ifp[0], 'name':fl_name, 'cookie':'0', 'priority':'32768',
                'ingress-port':str(ifp[1]), 'active':'true', 'actions':'output=%i' % ifp[2]}
        else:
            fl_dict={'switch':ifp[0], 'name':fl_name, 'cookie':'0', 'priority':'32768',
                'ingress-port':str(ifp[1]), 'active':'true', 'actions':''}
        fl_list.append(fl_dict)

    log_debug('\nAdding changed datapath settings...\n')

    for fl in fl_list:
        flowpusher.set(fl)
        time.sleep(1)
        log_debug('Flow added:\n %s' % str(fl))

    show_switches()

    print 'Waiting a little before moving to the next test...\n'
    time.sleep(60)

    return 'PASS'

#

_RESULT = openflow_test()

#
