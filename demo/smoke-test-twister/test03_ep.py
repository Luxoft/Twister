
#
# version: 2.001
# <title>test 03</title>
# <description>Testing the EP.</description>
#

import time
import random

#

def test(PROXY, USER, EP):

    ep_list = PROXY.listEPs(USER).split(',')
    if not ep_list:
        print('Failure! Cannot get EP list!')
        return 'Fail'
    print 'EPs list:', ep_list

    r = PROXY.searchEP(USER, 'EP-1001')
    if not r:
        print('Failure! Cannot find EP-1001!')
        return 'Fail'
    print 'Search EP-1001:', r

    r = PROXY.searchEP(USER, 'EP-1999')
    if r:
        print('Failure! EP-1999 should not be here!')
        return 'Fail'
    print 'Search EP-1999:', r
    time.sleep(0.5)
    print

    print 'Status All ?', PROXY.getExecStatusAll(USER)
    print 'Status All:', PROXY.setExecStatusAll(USER, 8)
    print 'Status All ?', PROXY.getExecStatusAll(USER)
    time.sleep(0.5)
    print

    for epname in ep_list:
        #
        if epname == EP: continue
        #
        print ':::', USER, '-', epname, ':::'
        suites = PROXY.listSuites(USER, epname).split(',') or None
        print 'Suites:', suites
        #
        print 'EP files:', PROXY.getEpFiles(USER, epname)
        print 'Suite files:', PROXY.getSuiteFiles(USER, epname, suites[0])
        #
        print 'Exec status ?', PROXY.getExecStatus(USER, epname)
        print 'Set status paused:', PROXY.setExecStatus(USER, epname, 1)
        print 'Exec status ?', PROXY.getExecStatus(USER, epname)
        print 'Set status invalid:', PROXY.setExecStatus(USER, epname, 8)
        print 'Exec status ?', PROXY.getExecStatus(USER, epname)
        print '-----\n'

    print 'EP variable', ep_list[1], ' ABC:', PROXY.getEpVariable(USER, ep_list[1], 'abc')
    r = PROXY.setEpVariable(USER, ep_list[1], 'abc', random.randrange(1, 100))
    if not r:
        print('Failure! Cannot set EP variable!')
        return 'Fail'
    print 'EP variable', ep_list[1], ' ABC:', PROXY.getEpVariable(USER, ep_list[1], 'abc')

    time.sleep(0.5)

    print 'EP variable', ep_list[-1], ' XYZ:', PROXY.getEpVariable(USER, ep_list[-1], 'xyz')
    r = PROXY.setEpVariable(USER, ep_list[-1], 'xyz', random.randrange(1, 100))
    if not r:
        print('Failure! Cannot set EP variable!')
        return 'Fail'
    print 'EP variable', ep_list[-1], ' XYZ:', PROXY.getEpVariable(USER, ep_list[-1], 'xyz')

    time.sleep(0.5)

    return 'Pass'

#

_RESULT = test(PROXY, USER, EP)

# Eof()
