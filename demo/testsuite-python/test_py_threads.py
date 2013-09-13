
# version: 2.001

import re
import time
from TscThreadsLib import tasks_reset, tasks_append, tasks_start

#
# <title>Testing Threads Library</title>
# <description>This test is checking the Threads library.</description>
#

def isPrime(n):
	return re.match(r'^1?$|^(11+?)\1+$', '1' * n) == None

def primesList(n):
	time.sleep(0.1)
	return [nr for nr in range(2, n) if isPrime(nr)]

def long_task(n):
	print 'Calculating some long task... {0}.'.format(n)
	time.sleep(5)
	print 'Exiting long task {0}.'.format(n)
	return n ** 2

#

def test():

	testName = 'test_py_threads.py'
	logMsg('logTest', "\nTestCase:%s starting\n" % testName)

	error_code = "PASS"

	# _________________________________________________________________________
	tasks_reset()

	for i in range(5, 90):
		tasks_append(primesList, i)

	# Short tasks...
	short_tasks_res = tasks_start()

	print 'Result for short tasks:'
	for t in short_tasks_res:
		if t: print t
	print()

	# _________________________________________________________________________
	tasks_reset()

	for i in range(1, 10):
		tasks_append(long_task, i)

	# Long tasks...
	long_tasks_res = tasks_start()

	print 'Result for long tasks:'
	for t in long_tasks_res:
		print 'Result:', t

	# _________________________________________________________________________
	logMsg('logTest', "TestCase:%s %s\n" % (testName, error_code))

	# This return is used by the framework!
	return error_code

#

# Must have one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout'
_RESULT = test()
