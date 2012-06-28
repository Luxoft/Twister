
import time
import pexpect
from ce_libs import logMsg

#
# <title>test 005</title>
# <description>This test is connecting to a SSH server.</description>
#

def test005():

	testName = 'test005.py'
	logMsg('logTest', "\nTestCase:%s starting\n" % testName)

	error_code = "PASS"

	print '=== Connecting to SSH ==='
	child = pexpect.spawn('ssh user@11.126.32.9')

	child.expect('.+assword:', timeout=60)
	child.sendline("password")
	print child.before[:-4]
	time.sleep(1)

	child.expect('user@tsc-server:', timeout=10)
	child.sendline("cd twister")
	print child.before[:-4]
	print child.after
	time.sleep(1)

	child.expect('user@tsc-server:', timeout=10)
	child.sendline("ls -la")
	print child.before[:-4]
	print child.after
	time.sleep(1)

	child.expect('user@tsc-server:', timeout=10)
	child.sendline("exit")
	print child.before[:-4]
	print child.after
	time.sleep(1)

	logMsg('logTest', "TestCase:%s %s\n" % (testName, error_code))
	return error_code

#

_RESULT = test005()
