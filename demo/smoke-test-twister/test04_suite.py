
#
# <ver>version: 2.003</ver>
# <title>Test the Suites</title>
# <description>This suite checks the most basic functionality of Twister.<br>
# It checks if the EPs are running the tests successfully and it calls all CE functions, to ensure they work as expected.</description>
#

import time

#

def test(PROXY, USER):

    ep_list = PROXY.listEPs(USER).split(',')

    for epname in ep_list:

        print '\n:::', USER, '-', epname, ':::'
        time.sleep(0.5)

        suites = PROXY.listSuites(USER, epname).split(',') or None
        print 'Suites:', suites

        for suite in suites:

            if not suite: continue

            suite_id = suite.split(':')[0]
            suite_name = suite.split(':')[1]

            r = PROXY.getSuiteVariable(USER, epname, suite_id, 'ep')
            if not r:
                print('Failure! Cannot get Suite variable `build_id` !')
                return 'Fail'
            print 'Suite variable %s `ep` ?' % suite, r

            r = PROXY.getSuiteVariable(USER, epname, suite_id, 'build_id')
            if not r:
                print('Warning! Cannot get Suite variable `build_id` !')
            print 'Suite variable %s `build_id` ?' % suite, r

            r = PROXY.getSuiteVariable(USER, epname, suite_id, 'suite_id')
            if not r:
                print('Warning! Cannot get Suite variable `suite_id` !')
            print 'Suite variable %s `suite_id` ?' % suite, r

    time.sleep(0.5)

    return 'Pass'

# Must have one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout'
_RESULT = test(PROXY, USER)

# Eof()
