
#
# <title>test 02</title>
# <description>Testing the logs.</description>
#

import time
import binascii

#

def test(proxy, userName):

    proxy.setStartedBy(userName, 'gigi')
    time.sleep(0.5)

    r = proxy.resetLog(userName, 'log_debug.log')
    if not r:
        print('Failure! Cannot reset log_debug!')
        return 'Fail'
    print 'Reset log:',  r

    r = proxy.resetLogs(userName)
    if not r:
        print('Failure! Cannot reset logs!')
        return 'Fail'
    print 'Reset logs:', r

    print 'Logs path:', proxy.getLogsPath(userName)
    print 'Log types:', proxy.getLogTypes(userName)
    time.sleep(0.5)
    print

    print 'Writing in logRunning...'
    r = proxy.logMessage(userName, 'logRunning', 'Run run run run run...')
    if not r:
        print('Failure! Cannot use logMessage!')
        return 'Fail'
    print 'Reading from logRunning: ', binascii.a2b_base64( proxy.getLogFile(userName, 1, 0, 'log_running.log') )
    time.sleep(0.5)
    print

    print 'Writing in logDebug...'
    r = proxy.logMessage(userName, 'logDebug', 'Debug debug debug debug debug...')
    if not r:
        print('Failure! Cannot use logDebug!')
        return 'Fail'
    print 'Reading from logDebug: ', binascii.a2b_base64( proxy.getLogFile(userName, 1, 0, 'log_debug.log') )
    time.sleep(0.5)
    print

    for epname in proxy.listEPs(userName).split(','):
        r = proxy.logLIVE(userName, epname, binascii.b2a_base64('Some log live message for `%s`...' % epname))
        if not r:
            print('Failure! Cannot use log Live!')
            return 'Fail'

    return 'Pass'

#

_RESULT = test(proxy, userName)

# Eof()
