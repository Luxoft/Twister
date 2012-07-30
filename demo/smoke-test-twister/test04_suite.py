
#
# <title>test 04</title>
# <description>Testing the Suites.</description>
#

import time

#

def test(proxy, userName):

    ep_list = proxy.listEPs(userName).split(',')

    for epname in ep_list:

        print '\n:::', userName, '-', epname, ':::'
        time.sleep(0.5)

        suites = proxy.listSuites(userName, epname).split(',') or None
        print 'Suites:', suites

        for suite in suites:

            if not suite: continue

            suite_id = suite.split(':')[0]
            suite_name = suite.split(':')[1]

            r = proxy.getSuiteVariable(userName, epname, suite_id, 'ep')
            if not r:
                print('Failure! Cannot get Suite variable `build_id` !')
                return 'Fail'
            print 'Suite variable %s `ep` ?' % suite, r

            r = proxy.getSuiteVariable(userName, epname, suite_id, 'build_id')
            if not r:
                print('Warning! Cannot get Suite variable `build_id` !')
            print 'Suite variable %s `build_id` ?' % suite, r

            r = proxy.getSuiteVariable(userName, epname, suite_id, 'suite_id')
            if not r:
                print('Warning! Cannot get Suite variable `suite_id` !')
            print 'Suite variable %s `suite_id` ?' % suite, r

    time.sleep(0.5)

    return 'Pass'

#

_RESULT = test(proxy, userName)

# Eof()
