
import os, sys, time
sys.path.append(os.getenv('TWISTER_PATH') + '/.twister_cache/')
from ce_libs import logMsg

#
# <title>test 001</title>
# <description>This test doesn't do anything spectacular, it just counts to 10, in 10 seconds.</description>
#

def test002():

	testName = 'test002.py'
	logMsg('logTest', "\nTestCase:%s starting\n" % testName)
	print "\nTestCase:%s starting\n" % testName
	error_code = "FAIL"

	timer_i = time.time()
	for i in range(10):
		# Exposed Python function
		logMsg('logDebug', "%s: working %i...\n" % (testName.upper(), i))
		print "%s: working %i..." % (testName.upper(), i)
		time.sleep(1)
	timer_f = time.time()
	logMsg('logDebug', "Working took %.2f seconds.\n" % (timer_f-timer_i))

	logMsg('logRunning', "TEST: working even more 222...\n")

	logMsg('logTest', "TestCase:%s %s\n" % (testName, error_code))
	return error_code

#

_RESULT = test002()
