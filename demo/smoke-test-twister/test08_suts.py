
#
# <ver>version: 3.001</ver>
# <title>Test CommonLib and Resource Allocator / SUTs</title>
# <description>This suite checks the most basic functionality of Twister.<br>
# Functions `get_sut`, `set_sut` and *the rest* are included in the interpreter!</description>
# <tags>testbed, resources, SUTs</tags>
# <test>sut</test>
# <smoke>yes</smoke>
#

from os import urandom
from binascii import hexlify

def test():

	testName = 'test_py_suts.py'
	log_msg('logRunning', "\nTestCase: `{}` starting...\n".format(testName))
	log_msg('logTest', "\nTestCase: `{}` starting...\n".format(testName))

	error_code = "PASS"

	print 'Query SUTs...', get_sut(1)
	print 'Query SUTs...', get_sut('/')
	print

	py_res = 'sut_' + hexlify(urandom(4)) + '.system'
	print 'Create a root SUT `{}`...'.format(py_res)
	res_id = set_sut(py_res, '/', {'meta1': 1, 'meta2': 2})
	print 'Ok.\n'

	if not res_id:
		return "FAIL"

	r = get_sut('/' + py_res)
	print 'Find SUT by name::', r
	if not r: return "FAIL"

	r = get_sut(res_id)
	print 'Find SUT by ID::', r
	if not r: return "FAIL"
	print

	r = get_sut('/{}:meta1'.format(py_res))
	print 'Meta 1::', r
	if not r:
		delete_sut(res_id)
		print '\nCould not update meta!'
		return "FAIL"

	r = get_sut('/{}:meta2'.format(py_res))
	print 'Meta 2::', r
	if not r:
		delete_sut(res_id)
		print '\nCould not update meta!'
		return "FAIL"
	print

	# for i in range(1, 4):
	# 	tag = 'tag{}'.format(i)
	# 	r = set_sut(py_res, '/', {tag: str(i)})
	# 	print 'Set tag `{}` = `{}` ... {}'.format(tag, i, r)
	# 	if not r: return "FAIL"

	# 	path = '/' + py_res + ':' + tag
	# 	r = rename_sut(path, 'tagx')
	# 	print 'Rename tag `{}` = `tagx` ... {}'.format(path, r)
	# 	if not r: return "FAIL"

	# 	path = '/' + py_res + ':tagx'
	# 	r = delete_sut(path)
	# 	print 'Delete tag `{}` ... {}'.format(path, r)
	# 	if not r: return "FAIL"
	# 	print

	print 'Delete SUT::', delete_sut('/' + py_res)
	r = get_sut(res_id)
	print 'Check info::', r
	if r and '*ERROR*' not in r:
		return "FAIL"
	print

	log_msg('logRunning', "TestCase: `{}` -  `{}`!\n".format(testName, error_code))
	log_msg('logTest', "TestCase: `{}` -  `{}`!\n".format(testName, error_code))

	# This return is used by the framework!
	return error_code

#

# Must have one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout'
_RESULT = test()
