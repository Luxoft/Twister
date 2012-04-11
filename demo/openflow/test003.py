
import sys

sys.path.append(os.getenv('TWISTER_PATH') + '/.twister_cache/')

from LibOpenFlow import *

#

def openflow_test_3():
    '''
    <title>OpenFlow: 003</title>
    <description>StatType possible values: port, queue, flow, aggregate, desc, table, features, host.
    This test displays all port statistics.
    </description>
    '''

    log_debug('\n=== Starting openflow controller test 3 ===\n')

    restapi= FloodLiteControl('10.9.6.220', 8080)
    fl_switches = restapi.get_switches()
    log_debug('Getting port statistics from floodlight controller...\n')

    for sw in fl_switches:
        switch_dpid = sw['dpid']
        log_debug("\nSwich DPID: %s" % switch_dpid)
        of_dict = restapi.get_switch_statistics(switch_dpid, 'port')
        #print 'debug:', of_dict

        if of_dict:
            for ps in of_dict[switch_dpid]:
                if ps['portNumber'] < 0:
                    continue

                print "portNumber:      %s" % ps['portNumber']
                print "transmitPackets: %s" % ps['transmitPackets']
                print "transmitBytes:   %s" % ps['transmitBytes']
                print "receivePackets:  %s" % ps['receivePackets']
                print "receiveBytes:    %s" % ps['receiveBytes']
                print "\n"
        else:
            return 'FAIL'

    return 'PASS'

#

_RESULT = openflow_test_3()

#
