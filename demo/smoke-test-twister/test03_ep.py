
#
# <title>test 03</title>
# <description>Testing the EP.</description>
#

import time
import random

#

def test(proxy, userName, globEpName):

    ep_list = proxy.listEPs(userName).split(',')
    if not ep_list:
        print('Failure! Cannot get EP list!')
        return 'Fail'
    print 'EPs list:', ep_list

    r = proxy.searchEP(userName, 'EP-1001')
    if not r:
        print('Failure! Cannot find EP-1001!')
        return 'Fail'
    print 'Search EP-1001:', r

    r = proxy.searchEP(userName, 'EP-1999')
    if r:
        print('Failure! EP-1999 should not be here!')
        return 'Fail'
    print 'Search EP-1999:', r
    time.sleep(0.5)
    print

    print 'Status All ?', proxy.getExecStatusAll(userName)
    print 'Status All:', proxy.setExecStatusAll(userName, 8)
    print 'Status All ?', proxy.getExecStatusAll(userName)
    time.sleep(0.5)
    print

    for epname in ep_list:
        #
        if epname == globEpName: continue
        #
        print ':::', userName, '-', epname, ':::'
        suites = proxy.listSuites(userName, epname).split(',') or None
        print 'Suites:', suites
        #
        print 'EP files:', proxy.getEpFiles(userName, epname)
        print 'Suite files:', proxy.getSuiteFiles(userName, epname, suites[0])
        #
        print 'Exec status ?', proxy.getExecStatus(userName, epname)
        print 'Set status paused:', proxy.setExecStatus(userName, epname, 1)
        print 'Exec status ?', proxy.getExecStatus(userName, epname)
        print 'Set status invalid:', proxy.setExecStatus(userName, epname, 8)
        print 'Exec status ?', proxy.getExecStatus(userName, epname)
        print '-----\n'

    print 'EP variable', ep_list[1], ' ABC:', proxy.getEpVariable(userName, ep_list[1], 'abc')
    r = proxy.setEpVariable(userName, ep_list[1], 'abc', random.randrange(1, 100))
    if not r:
        print('Failure! Cannot set EP variable!')
        return 'Fail'
    print 'EP variable', ep_list[1], ' ABC:', proxy.getEpVariable(userName, ep_list[1], 'abc')

    time.sleep(0.5)

    print 'EP variable', ep_list[-1], ' XYZ:', proxy.getEpVariable(userName, ep_list[-1], 'xyz')
    r = proxy.setEpVariable(userName, ep_list[-1], 'xyz', random.randrange(1, 100))
    if not r:
        print('Failure! Cannot set EP variable!')
        return 'Fail'
    print 'EP variable', ep_list[-1], ' XYZ:', proxy.getEpVariable(userName, ep_list[-1], 'xyz')

    time.sleep(0.5)

    return 'Pass'

#

_RESULT = test(proxy, userName, globEpName)

# Eof()
