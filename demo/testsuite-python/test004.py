
import os, sys, time
sys.path.append(os.getenv('HOME') + '/.twister_cache/')

#

def test004():
	'''
	Testing Python Expect.
	'''

	import pexpect
	from ce_libs import logMsg

	testName = 'test004.py'
	logMsg('logTest', "\nTestCase:%s starting\n" % testName)

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

	logMsg('logTest', "TestCase:%s %s\n" % (testName, error_code))
	return error_code

#

_RESULT = test004()
