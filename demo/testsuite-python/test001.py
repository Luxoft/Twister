
import os, sys, time
sys.path.append(os.getenv('HOME') + '/.twister_cache/')

#

def test001():
	from ce_libs import logMsg

	testName = 'test001.py'
	logMsg('logTest', "\nTestCase:%s starting\n" % testName)
	print "\nTestCase:%s starting\n" % testName
	error_code = "PASS"

	timer_i = time.time()
	for i in range(10):
		# Exposed Python function
		logMsg('logDebug', "%s: working %i...\n" % (testName.upper(), i))
		print "%s: working %i..." % (testName.upper(), i)
		time.sleep(1)
	timer_f = time.time()
	logMsg('logDebug', "Working took %.2f seconds.\n" % (timer_f-timer_i))

	logMsg('logRunning', "TEST: working even more 111...\n")

	logMsg('logTest', "TestCase:%s %s\n" % (testName, error_code))
	return error_code

#

_RESULT = test001()
