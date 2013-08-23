
#
# version: 2.003
# <title>test 02</title>
# <description>Testing the logs.</description>
#

import time
import binascii

#

def test(PROXY, USER):

    logMsg('logRunning', 'Starting LOGS smoke-test...\n')

    PROXY.setStartedBy(USER, 'gigi')
    time.sleep(0.5)

    r = PROXY.resetLog(USER, 'log_debug.log')
    if not r:
        print('Failure! Cannot reset log_debug!')
        return 'Fail'
    print 'Reset log_debug:',  r

    r = True #PROXY.resetLogs(USER)
    if not r:
        print('Failure! Cannot reset logs!')
        return 'Fail'
    print 'Reset logs:', r

    print 'Logs path:', PROXY.getUserVariable(USER, 'logs_path')
    print 'Log types:', PROXY.getUserVariable(USER, 'logs_types')
    time.sleep(0.5)
    print

    print 'Writing in logRunning...'
    r = PROXY.logMessage(USER, 'logRunning', 'Run run run run run...\n')
    if not r:
        print('Failure! Cannot use logMessage!')
        return 'Fail'
    print 'Reading from logRunning: ', binascii.a2b_base64( PROXY.getLogFile(USER, 1, 0, 'log_running.log') )
    time.sleep(0.5)
    print

    print 'Writing in logDebug...'
    r = PROXY.logMessage(USER, 'logDebug', 'Debug debug debug debug debug...\n')
    if not r:
        print('Failure! Cannot use logDebug!')
        return 'Fail'
    print 'Reading from logDebug: ', binascii.a2b_base64( PROXY.getLogFile(USER, 1, 0, 'log_debug.log') )
    time.sleep(0.5)
    print

    print 'Writing in logTest...'
    r = PROXY.logMessage(USER, 'logTest', 'Test test test test test...\n')
    if not r:
        print('Failure! Cannot use logTest!')
        return 'Fail'
    print 'Reading from logTest: ', binascii.a2b_base64( PROXY.getLogFile(USER, 1, 0, 'log_debug.log') )
    time.sleep(0.5)
    print

    for epname in PROXY.listEPs(USER).split(','):
        try: r = PROXY.logLIVE(USER, epname, binascii.b2a_base64('Some log live message for `%s`...' % epname))
        except: r = False
        if not r:
            print('Failure! Cannot use log Live!')
            return 'Fail'

    logMsg('logRunning', 'LOGS smoke-test passed.\n')

    return 'Pass'

# Must have one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout', 'invalid'
_RESULT = test(PROXY, USER)

# Eof()
