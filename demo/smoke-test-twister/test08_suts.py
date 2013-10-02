
#
# <ver>version: 2.002</ver>
# <title>Test CommonLib and Resource Allocator / SUTs</title>
# <description>This suite checks the most basic functionality of Twister.<br>
# Functions `getSut`, `setSut` and *the rest* are included in the interpreter!</description>
# <tags>testbed, resources, SUTs</tags>
#

from os import urandom
from binascii import hexlify

def test():

	testName = 'test_py_suts.py'
	logMsg('logRunning', "\nTestCase: `{}` starting...\n".format(testName))
	logMsg('logTest', "\nTestCase: `{}` starting...\n".format(testName))

	error_code = "PASS"

	print 'Query SUTs...', getSut(1)
	print 'Query SUTs...', getSut('/')
	print

	py_res = 'tb_' + hexlify(urandom(4))
	print 'Create a root SUT `{}`...'.format(py_res)
	res_id = setSut(py_res, '/', {'meta1': 1, 'meta2': 2})
	print 'Ok.\n'

	if not res_id:
		return "FAIL"

	r = getSut('/' + py_res)
	print 'Find SUT by name::', r
	if not r: return "FAIL"

	r = getSut(res_id)
	print 'Find SUT by ID::', r
	if not r: return "FAIL"
	print

	r = getSut('/{}:meta1'.format(py_res))
	print 'Meta 1::', r
	if not r: return "FAIL"

	r = getSut('/{}:meta2'.format(py_res))
	print 'Meta 2::', r
	if not r: return "FAIL"
	print

	print 'Update SUT::', setSut(py_res, '/', {'more-info': 'y'})
	r = getSut(res_id)
	print 'Check status::', r
	if 'more-info' not in r['meta']: return "FAIL"
	print

	for i in range(1, 4):
		tag = 'tag{}'.format(i)
		r = setSut(py_res, '/', {tag: str(i)})
		print 'Set tag `{}` = `{}` ... {}'.format(tag, i, r)
		if not r: return "FAIL"

		path = '/' + py_res + ':' + tag
		r = renameSut(path, 'tagx')
		print 'Rename tag `{}` = `tagx` ... {}'.format(path, r)
		if not r: return "FAIL"

		path = '/' + py_res + ':tagx'
		r = deleteSut(path)
		print 'Delete tag `{}` ... {}'.format(path, r)
		if not r: return "FAIL"
		print

	print 'Delete SUT::', deleteSut(res_id)
	r = getSut(res_id)
	print 'Check info::', r
	if r: return "FAIL"
	print

	logMsg('logRunning', "TestCase: `{}` -  `{}`!\n".format(testName, error_code))
	logMsg('logTest', "TestCase: `{}` -  `{}`!\n".format(testName, error_code))

	# This return is used by the framework!
	return error_code

#

# Must have one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout'
_RESULT = test()
