
#
# <ver>version: 2.001</ver>
# <title>Test long sleep</title>
# <description>This suite checks the most basic functionality of Twister.<br>
# </description>
# <tags>test, delay, sleep</tags>
# <test>sleep</test>
# <smoke>yes</smoke>
#

import time

#

def test():

    logMsg('logRunning', '\nStarting long sleep...\n')

    mins = 1
    times = 30

    for i in range(1, times+1):
        print('[{0}] Sleeping `{1}` min...'.format(i, mins))
        st = mins * 60
        time.sleep(st)

    logMsg('logRunning', 'Finished long sleep.\n')

    return 'Pass'

#

# Must have one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout'
_RESULT = test()

# Eof()
