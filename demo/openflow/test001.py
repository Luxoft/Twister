
import os, sys

if os.getenv('TWISTER_PATH'):
    sys.path.append(os.getenv('TWISTER_PATH') + '/.twister_cache/ce_libs/')

#

def openflow_test_1():
    '''
    <title>OpenFlow: 001</title>
    <description>This test shows all the devices registered in the FloodLite controller.</description>
    '''

    from LibOpenFlow import log_debug, show_switches, FloodLiteControl

    log_debug('\n=== Starting openflow controller test 1 ===\n')

    restapi= FloodLiteControl('10.9.6.220', 8080)
    switches = restapi.get_switches_info()
    result = 'PASS'

    log_debug('Found %i devices.' % len(switches))

    if len(switches) != 2:
        print('Error! Must have 2 switches!')
        result = 'FAIL'

    for sid in switches:
        print('\n~~ Switch ID: {0} ~~'.format(sid))
        for key, value in switches[sid][0].items():
            print key.ljust(18), ':', value

    return result

#

_RESULT = openflow_test_1()

#
