
#
# <ver>version: 3.001</ver>
# <title>Test EPs</title>
# <description>This suite checks the most basic functionality of Twister.<br>
# It checks if the EPs are running the tests successfully and it calls all CE functions, to ensure they work as expected.</description>
# <test>ep</test>
# <smoke>yes</smoke>
#

import time
import random

#

def test(PROXY, USER, EP):

    ep_list = PROXY.list_eps()
    if not ep_list:
        _REASON = 'Failure! Cannot get EP list!'
        print(_REASON)
        return 'Fail', _REASON
    print 'EPs list:', ep_list

    time.sleep(0.5)
    print

    print 'Status All ?', PROXY.get_ep_status_all()
    print 'Status All:', PROXY.set_ep_status_all(8) # STATUS INVALID
    print 'Status All ?', PROXY.get_ep_status_all()
    time.sleep(0.5)
    print

    for epname in ep_list:
        #
        if epname == EP: continue
        #
        print ':::', USER, '-', epname, ':::'
        suites = PROXY.list_suites(epname).split(',') or []
        print 'Suites:', suites
        #
        print 'EP files:', PROXY.get_ep_files(epname)
        if suites:
            print 'Suite files:', PROXY.get_suite_files(epname, suites[0])
        #
        print 'Exec status ?', PROXY.get_ep_status(epname)
        print 'Set status paused:', PROXY.set_ep_status(epname, 1, 'Smoke test suite')
        print 'Exec status ?', PROXY.get_ep_status(epname)
        print 'Set status invalid:', PROXY.set_ep_status(epname, 8, 'Smoke test suite')
        print 'Exec status ?', PROXY.get_ep_status(epname)
        print '-----\n'

    print 'EP variable', ep_list[1], ' ABC:', PROXY.get_ep_variable(ep_list[1], 'abc')
    r = PROXY.set_ep_variable(ep_list[1], 'abc', random.randrange(1, 100))
    if not r:
        _REASON = 'Failure! Cannot set EP variable ABC!'
        print(_REASON)
        return 'Fail', _REASON
    print 'EP variable', ep_list[1], ' ABC:', PROXY.get_ep_variable(ep_list[1], 'abc')

    time.sleep(0.5)

    print 'EP variable', ep_list[-1], ' XYZ:', PROXY.get_ep_variable(ep_list[-1], 'xyz')
    r = PROXY.set_ep_variable(ep_list[-1], 'xyz', random.randrange(1, 100))
    if not r:
        _REASON = 'Failure! Cannot set EP variable XYZ!'
        print(_REASON)
        return 'Fail', _REASON
    print 'EP variable', ep_list[-1], ' XYZ:', PROXY.get_ep_variable(ep_list[-1], 'xyz')

    time.sleep(0.25)

    return 'Pass', ''

# Must have one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout'
_RESULT, _REASON = test(PROXY, USER, EP)

# Eof()
