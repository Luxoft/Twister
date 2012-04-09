
from LibOpenFlow import *

#

def openflow_test_2():
    '''
    <title>OpenFlow: 002</title>
    <description>This test shows all the devices registered in the FloodLite controller.</description>
    '''

    log_debug('\n=== Starting openflow controller test 2 ===\n')

    restapi= FloodLiteControl('10.9.6.220', 8080)
    res = restapi.get_aggregate_stats('flow')
    log_debug('Found %i devices.' % len(res))
    log_debug('\n~~ Aggregates ~~')

    for sid in res:
        if not res[sid]:
            print '\n  None!'
            break
        print '\n~~ Switch ID:', sid, '~~'
        for key,value in res[sid][0].items():
            print ' ', key.ljust(18), ':', value

    res = restapi.get_aggregate_stats('table')
    log_debug('\n~~ Tables ~~')

    for sid in res:
        if not res[sid]:
            print '\n  None!'
            break
        print '\n~~ Switch ID:', sid, '~~'
        for key,value in res[sid][0].items():
            print ' ', key.ljust(18), ':', value

    print
    return 'PASS'

#

_RESULT = openflow_test_2()

#
