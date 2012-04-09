
from LibOpenFlow import *

#

def openflow_test_1():
    '''
    <title>OpenFlow: 001</title>
    <description>This test shows all the devices registered in the FloodLite controller.</description>
    '''

    log_debug('\n=== Starting openflow controller test 1 ===\n')

    restapi= FloodLiteControl('10.9.6.220', 8080)
    res = restapi.get_switches_info()

    log_debug('Found %i devices.' % len(res))

    for sid in res:
        print('\n~~ Switch ID: {0} ~~'.format(sid))
        for key, value in res[sid][0].items():
            print key.ljust(18), ':', value

    print
    return 'PASS'

#

_RESULT = openflow_test_1()

#
