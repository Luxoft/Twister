
# version: 2.001

import time
import telnetlib

"""
<title>Testing Telnet Lib</title>
<description>This test is connecting to a TELNET host, using the default Pythin lib.
If you need something more advanced, use Twister Telnet library.</description>
"""

def test():
	'''
	Testing Python standard Telnet library.
	'''

	testName = 'test_py_telnet.py'
	logMsg('logTest', "\nTestCase:%s starting\n" % testName)
	error_code = "PASS"

	tn = telnetlib.Telnet('134.117.136.48', 23, 60)
	print 'Connected:', tn
	time.sleep(1)

	print tn.read_until('login:', 30)
	tn.write('guest\n')
	time.sleep(1)

	print tn.read_until('any key to continue...', 10)
	tn.write('\n\n')
	time.sleep(1)

	print tn.read_until("'q' to quit", 10)
	tn.write('q\n')
	time.sleep(1)

	print tn.read_until('About the National Capital FreeNet', 10)
	tn.write('1\n')
	time.sleep(1)

	print tn.read_until('Your Choice ==>', 10)
	tn.write('x\n')
	tn.write('y\n')
	time.sleep(1)

	print tn.read_very_eager()

	logMsg('logTest', "TestCase:%s %s\n" % (testName, error_code))

	# This return is used by the framework!
	return error_code

#

# Must have one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout'
_RESULT = test()
