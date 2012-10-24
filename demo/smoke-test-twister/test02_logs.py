
#
# <title>test 02</title>
# <description>Testing the logs.</description>
#

import time
import binascii

#

def test(PROXY, USER):

    PROXY.setStartedBy(USER, 'gigi')
    time.sleep(0.5)

    r = PROXY.resetLog(USER, 'log_debug.log')
    if not r:
        print('Failure! Cannot reset log_debug!')
        return 'Fail'
    print 'Reset log:',  r

    r = PROXY.resetLogs(USER)
    if not r:
        print('Failure! Cannot reset logs!')
        return 'Fail'
    print 'Reset logs:', r

    print 'Logs path:', PROXY.getLogsPath(USER)
    print 'Log types:', PROXY.getLogTypes(USER)
    time.sleep(0.5)
    print

    print 'Writing in logRunning...'
    r = PROXY.logMessage(USER, 'logRunning', 'Run run run run run...')
    if not r:
        print('Failure! Cannot use logMessage!')
        return 'Fail'
    print 'Reading from logRunning: ', binascii.a2b_base64( PROXY.getLogFile(USER, 1, 0, 'log_running.log') )
    time.sleep(0.5)
    print

    print 'Writing in logDebug...'
    r = PROXY.logMessage(USER, 'logDebug', 'Debug debug debug debug debug...')
    if not r:
        print('Failure! Cannot use logDebug!')
        return 'Fail'
    print 'Reading from logDebug: ', binascii.a2b_base64( PROXY.getLogFile(USER, 1, 0, 'log_debug.log') )
    time.sleep(0.5)
    print

    for epname in PROXY.listEPs(USER).split(','):
        r = PROXY.logLIVE(USER, epname, binascii.b2a_base64('Some log live message for `%s`...' % epname))
        if not r:
            print('Failure! Cannot use log Live!')
            return 'Fail'

    return 'Pass'

#

_RESULT = test(PROXY, USER)

# Eof()
