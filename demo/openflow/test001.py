
from LibOpenFlow import *

#

def openflow_test_1():
    '''
    <title>OpenFlow: 001</title>
    <description>This test shows all the devices registered in the FloodLite controller.</description>
    '''

    log_debug('\n=== Starting openflow controller test 1 ===\n')

    restapi= FloodLiteControl('10.9.6.220', 8080)
    switches = restapi.get_switches_info()

    log_debug('Found %i devices.' % len(switches))

    if len(switches) != 2:
        print('Error! Must have 2 switches! Exiting!')
        return 'FAIL'

    for sid in switches:
        print('\n~~ Switch ID: {0} ~~'.format(sid))
        for key, value in switches[sid][0].items():
            print key.ljust(18), ':', value

    print
    return 'PASS'

#

_RESULT = openflow_test_1()

#
