
# version: 2.001

import time
import pexpect

#
# <title>Test pExpect FTP</title>
# <description>This test is connecting to a FTP host, using pExpect.</description>
#

def test():
	'''
	Testing Python Expect.
	'''

	testName = 'test_pexpect_ftp.py'
	log_msg('logTest', "\nTestCase:%s starting\n" % testName)

	error_code = "PASS"

	child = pexpect.spawn('ftp ftp.openbsd.org')
	time.sleep(1)

	child.expect('Name .*: ')
	child.sendline('anonymous')
	print child.before
	time.sleep(1)

	child.expect('Password:')
	child.sendline('noah@example.com')
	print child.before
	time.sleep(1)

	child.expect('ftp> ')
	child.sendline('cd /pub/OpenBSD/')
	print child.before
	time.sleep(1)

	child.expect('ftp> ')
	child.sendline('ls')
	print child.before
	time.sleep(1)

	child.expect('ftp> ')
	child.sendline('bye')
	print child.before
	time.sleep(1)

	log_msg('logTest', "TestCase:%s %s\n" % (testName, error_code))

	# This return is used by the framework!
	return error_code

#

# Must have one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout', 'invalid'
_RESULT = test()
