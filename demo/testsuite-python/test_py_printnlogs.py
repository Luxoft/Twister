
#
# version: 2.001
# <title>test print and logs</title>
# <description>This test doesn't do anything spectacular, prints and sends some logs.</description>
#

def test():

	testName = 'test_py_printnlogs.py'
	logMsg('logTest', "\nTestCase:%s starting\n" % testName)
	print "\nTestCase:%s starting\n" % testName
	error_code = "PASS"

	timer_i = time.time()
	for i in range(10):
		# Exposed Python function
		logMsg('logDebug', "Py %s: working %i...\n" % (testName.upper(), i))
		print "%s: working %i..." % (testName.upper(), i)
		time.sleep(1)
	timer_f = time.time()
	logMsg('logDebug', "Working took %.2f seconds.\n" % (timer_f-timer_i))

	logMsg('logRunning', "Py TEST: working even more 111...\n")

	logMsg('logTest', "TestCase:%s %s\n" % (testName, error_code))

	# This return is used by the framework!
	return error_code

#

# Must have one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout', 'invalid'
_RESULT = test()
