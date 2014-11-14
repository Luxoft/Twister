
#
# <ver>version: 3.001</ver>
# <title>Test the Suites</title>
# <description>This suite checks the most basic functionality of Twister.<br>
# It checks if the EPs are running the tests successfully and it calls all CE functions, to ensure they work as expected.</description>
# <test>suite</test>
# <smoke>yes</smoke>
#

import time

#

def test(PROXY, USER):

    ep_list = PROXY.list_eps()

    for epname in ep_list:

        print '\n:::', USER, '-', epname, ':::'
        time.sleep(0.5)

        suites = PROXY.list_suites(epname).split(',') or []
        print 'Suites:', suites

        for suite in suites:

            if not suite: continue

            suite_id = suite.split(':')[0]
            suite_name = suite.split(':')[1]

            r = PROXY.get_suite_variable(epname, suite_id, 'ep')
            if not r:
                _REASON = 'Failure! Cannot get Suite variable `build_id` !'
                print(_REASON)
                return 'Fail', _REASON
            print 'Suite variable %s `ep` ?' % suite, r

            r = PROXY.get_suite_variable(epname, suite_id, 'build_id')
            if not r:
                print('Warning! Cannot get Suite variable `build_id` !')
            print 'Suite variable %s `build_id` ?' % suite, r

            r = PROXY.get_suite_variable(epname, suite_id, 'suite_id')
            if not r:
                print('Warning! Cannot get Suite variable `suite_id` !')
            print 'Suite variable %s `suite_id` ?' % suite, r

    time.sleep(0.5)

    return 'Pass', ''

# Must have one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout'
_RESULT, _REASON = test(PROXY, USER)

# Eof()
