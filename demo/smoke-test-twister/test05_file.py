
#
# <ver>version: 2.004</ver>
# <title>Test the Files</title>
# <description>This suite checks the most basic functionality of Twister.<br>
# It checks if the EPs are running the tests successfully and it calls all CE functions, to ensure they work as expected.</description>
#

import time
import random

STATUS_PENDING  = 10 # Not yet run, waiting to start
STATUS_WORKING  = 1  # Is running now
STATUS_PASS     = 2  # Test is finished successful
STATUS_FAIL     = 3  # Test failed
STATUS_SKIPPED  = 4  # When file doesn't exist, or test has flag `runnable = False`
STATUS_ABORTED  = 5  # When test is stopped while running
STATUS_NOT_EXEC = 6  # Not executed, is sent from TC when tests are paused, and then stopped instead of being resumed
STATUS_TIMEOUT  = 7  # When timer expired
STATUS_INVALID  = 8  # When timer expired, the next run
STATUS_WAITING  = 9  # Is waiting for another test


def test(PROXY, USER):

    ep_list = PROXY.listEPs()

    for epname in ep_list:

        print '\n:::', USER, '-', epname, ':::'
        time.sleep(0.5)

        # This is a list
        ep_files = PROXY.getEpFiles(epname)

        for file_id in ep_files:

            print 'File variable ?', PROXY.getFileVariable(epname, file_id, 'xyz')
            r = PROXY.setFileVariable(epname, file_id, 'xyz', random.randrange(1, 100))
            if not r:
                print('Failure! Cannot set file variable for `%s`!' % file_id)
                return 'Fail'

            print 'Set variable for `{}`: `{}`'.format(file_id, r)
            print 'File variable ?', PROXY.getFileVariable(epname, file_id, 'xyz')


        # Get all statuses for this EP. It's a string
        status_before = PROXY.getFileStatusAll(epname)
        if not status_before: continue

        if len(ep_files) != len(status_before):
            print('This is wrong! There are {} files, but {} statuses!'.format(len(ep_files), len(status_before)))
            print(ep_files)
            print(status_before)
            return 'Fail'

        print 'Status All for {} ?'.format(epname), status_before

        msg = 'WILL RESET ALL STATUSES TO [SKIP], FOR `{} - {}` !\n'.format(USER, epname)
        print(msg) ; logMsg('logRunning', msg) ; logMsg('logDebug', msg)

        r = PROXY.setFileStatusAll(epname, STATUS_SKIPPED)
        # If success, the return must be True
        if not r:
            print('Failure! Cannot set file variable for all files!')
            return 'Fail'
        print 'Status all SKIPPED:', epname, r

        time.sleep(0.5)
        print

        msg = 'RESTORING ALL STATUSES FOR `{} - {}` ...\n'.format(USER, epname)
        print(msg) ; logMsg('logRunning', msg) ; logMsg('logDebug', msg)

        # Restore all statuses
        for i in range(len(ep_files)):
            file_id = ep_files[i]
            file_status = status_before[i]
            if file_status == -1:
                file_status = STATUS_PENDING

            r = PROXY.setFileStatus(epname, file_id, int(file_status))
            # If success, the return must be True
            if r:
                print('setFileStatus for {} - {} success.'.format(epname, file_id))
            else:
                print('Failure! Cannot setFileStatus for {} - {}!'.format(epname, file_id))
                return 'Fail'

        msg = 'ALL STATUSES RESTORED SUCCESSFULLY.\n'
        print(msg) ; logMsg('logRunning', msg) ; logMsg('logDebug', msg)

        print 'Status All for {} ?'.format(epname), PROXY.getFileStatusAll(epname)

        print '\n----- -----'

    time.sleep(0.5)

    return 'Pass'


# Must have one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout'
_RESULT = test(PROXY, USER)

# Eof()
