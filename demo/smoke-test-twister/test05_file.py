
#
# <title>test 04</title>
# <description>Testing the Suites.</description>
#

import time
import random

#

def test(proxy, userName):

    ep_list = proxy.listEPs(userName).split(',')

    for epname in ep_list:

        print '\n:::', userName, '-', epname, ':::'
        time.sleep(0.5)

        for file_id in proxy.getEpFiles(userName, epname):

            suite = proxy.getFileVariable(userName, file_id, 'suite')
            print 'File variable ?', proxy.getFileVariable(userName, file_id, 'xyz')
            r = proxy.setFileVariable(userName, epname, suite, file_id, 'xyz', random.randrange(1, 100))
            if not r:
                print('Failure! Cannot set file variable for `%s`!' % file_id)
                return 'Fail'

            print 'Set variable for `%s`:' % file_id, r
            print 'File variable ?', proxy.getFileVariable(userName, file_id, 'xyz')

        r = proxy.setFileStatusAll(userName, epname, 4)
        if not r:
            print('Failure! Cannot set file variable for all files!')
            return 'Fail'

        print 'Status all 4:', epname, r
        print 'Status all ?', epname, proxy.getFileStatusAll(userName, epname)

    time.sleep(0.5)

    return 'Pass'

#

_RESULT = test(proxy, userName)

# Eof()
