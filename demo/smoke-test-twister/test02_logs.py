
#
# <ver>version: 2.005</ver>
# <title>Test the Logs</title>
# <description>This suite checks the most basic functionality of Twister.<br>
# It checks if the EPs are running the tests successfully and it calls all CE functions, to ensure they work as expected.</description>
#

import time
import binascii

#

def test(PROXY):

    logMsg('logRunning', 'Starting LOGS smoke-test...\n')

    r = PROXY.resetLog('log_debug.log')
    if not r:
        print('Failure! Cannot reset log_debug!')
        return 'Fail'
    print 'Reset log_debug:',  r

    r = True # PROXY.resetLogs(USER)
    if not r:
        print('Failure! Cannot reset logs!')
        return 'Fail'
    print 'Reset logs:', r

    print 'Logs path:', PROXY.getUserVariable('logs_path')
    print 'Log types:', PROXY.getUserVariable('logs_types')
    time.sleep(0.5)
    print

    print 'Writing in logRunning...'
    r = PROXY.logMessage('logRunning', 'Run run run run run...\n')
    if not r:
        print('Failure! Cannot use logMessage!')
        return 'Fail'
    print 'Reading from logRunning: ', binascii.a2b_base64( PROXY.getLogFile(1, 0, 'log_running.log') )
    time.sleep(0.5)
    print

    print 'Writing in logDebug...'
    r = PROXY.logMessage('logDebug', 'Debug debug debug debug debug...\n')
    if not r:
        print('Failure! Cannot use logDebug!')
        return 'Fail'
    print 'Reading from logDebug: ', binascii.a2b_base64( PROXY.getLogFile(1, 0, 'log_debug.log') )
    time.sleep(0.5)
    print

    print 'Writing in logTest...'
    r = PROXY.logMessage('logTest', 'Test test test test test...\n')
    if not r:
        print('Failure! Cannot use logTest!')
        return 'Fail'
    print 'Reading from logTest: ', binascii.a2b_base64( PROXY.getLogFile(1, 0, 'log_debug.log') )
    time.sleep(0.5)
    print

    print('EP NAMES: {}.\n\n'.format(PROXY.listEPs()))

    for epname in PROXY.listEPs():
        try: r = PROXY.logLIVE(epname, binascii.b2a_base64('Some log live message for `{}`...'.format(epname)))
        except: r = False
        if not r:
            print('Failure! Cannot use log Live!')
            return 'Fail'

    logMsg('logRunning', 'LOGS smoke-test passed.\n')

    return 'Pass'

# Must have one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout'
_RESULT = test(PROXY)

# Eof()
