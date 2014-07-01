
#
# <ver>version: 2.006</ver>
# <title>Test the Logs</title>
# <description>This suite checks the most basic functionality of Twister.<br>
# It checks if the EPs are running the tests successfully and it calls all CE functions, to ensure they work as expected.</description>
# <test>logs</test>
# <smoke>yes</smoke>
#

import time
import binascii

#

def test(PROXY):

    logMsg('logRunning', 'Starting LOGS smoke-test...\n')

    r = PROXY.reset_log('log_debug.log')
    if not r:
        print('Failure! Cannot reset log_debug!')
        return 'Fail'
    print 'Reset log_debug:',  r

    r = True # PROXY.reset_logs(USER)
    if not r:
        print('Failure! Cannot reset logs!')
        return 'Fail'
    print 'Reset logs:', r

    print 'Logs path:', PROXY.get_user_variable('logs_path')
    print 'Log types:', PROXY.get_user_variable('logs_types')
    time.sleep(0.5)
    print

    print 'Writing in logRunning...'
    r = PROXY.log_message('logRunning', 'Run run run run run...\n')
    if not r:
        print('Failure! Cannot use log_message!')
        return 'Fail'
    print 'Reading from logRunning: ', binascii.a2b_base64( PROXY.get_log_file(1, 0, 'log_running.log') )
    time.sleep(0.5)
    print

    print 'Writing in logDebug...'
    r = PROXY.log_message('logDebug', 'Debug debug debug debug debug...\n')
    if not r:
        print('Failure! Cannot use logDebug!')
        return 'Fail'
    print 'Reading from logDebug: ', binascii.a2b_base64( PROXY.get_log_file(1, 0, 'log_debug.log') )
    time.sleep(0.5)
    print

    print 'Writing in logTest...'
    r = PROXY.log_message('logTest', 'Test test test test test...\n')
    if not r:
        print('Failure! Cannot use logTest!')
        return 'Fail'
    print 'Reading from logTest: ', binascii.a2b_base64( PROXY.get_log_file(1, 0, 'log_debug.log') )
    time.sleep(0.5)
    print

    print('EP NAMES: {}.\n\n'.format(PROXY.list_eps()))

    for epname in PROXY.list_eps():
        try: r = PROXY.log_live(epname, binascii.b2a_base64('Some log live message for `{}`...'.format(epname)))
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
