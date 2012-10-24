
#
# <title>test 04</title>
# <description>Testing the Suites.</description>
#

import time
import random

#

def test(PROXY, USER):

    ep_list = PROXY.listEPs(USER).split(',')

    for epname in ep_list:

        print '\n:::', USER, '-', epname, ':::'
        time.sleep(0.5)

        for file_id in PROXY.getEpFiles(USER, epname):

            suite = PROXY.getFileVariable(USER, file_id, 'suite')
            print 'File variable ?', PROXY.getFileVariable(USER, file_id, 'xyz')
            r = PROXY.setFileVariable(USER, epname, suite, file_id, 'xyz', random.randrange(1, 100))
            if not r:
                print('Failure! Cannot set file variable for `%s`!' % file_id)
                return 'Fail'

            print 'Set variable for `%s`:' % file_id, r
            print 'File variable ?', PROXY.getFileVariable(USER, file_id, 'xyz')

        r = PROXY.setFileStatusAll(USER, epname, 4)
        if not r:
            print('Failure! Cannot set file variable for all files!')
            return 'Fail'

        print 'Status all 4:', epname, r
        print 'Status all ?', epname, PROXY.getFileStatusAll(USER, epname)

    time.sleep(0.5)

    return 'Pass'

#

_RESULT = test(PROXY, USER)

# Eof()
