
#
# <ver>version: 2.004</ver>
# <title>Test CommonLib and Resource Allocator / TestBed and Resources</title>
# <description>This suite checks the most basic functionality of Twister.<br>
# Functions `get_resource`, `set_resource` and *the rest* are included in the interpreter!</description>
# <tags>testbed, resources, devices</tags>
# <test>resource</test>
# <smoke>yes</smoke>
#

from os import urandom
from binascii import hexlify

def test():

	testName = 'test_py_resources.py'
	log_msg('logRunning', "\nTestCase: `{}` starting...\n".format(testName))
	log_msg('logTest', "\nTestCase: `{}` starting...\n".format(testName))

	error_code = "PASS"

	print 'Query Root (1)...', get_resource(1)
	print 'Query Root (/)...', get_resource('/')
	print

	py_res = 'tb_' + hexlify(urandom(4))
	print 'Create a tb `{}`...'.format(py_res)
	res_id = set_resource(py_res, '/', {'meta1': 1, 'meta2': 2})
	print 'Ok.\n'

	if not res_id:
		print('Could not create TB! {}'.format(res_id))
		return "FAIL"

	r = get_resource('/' + py_res)
	print 'Find device by name::', r
	if not r: return "FAIL"

	r = get_resource(res_id)
	print 'Find device by ID::', r
	if not r: return "FAIL"
	print

	r = get_resource('/{}:meta1'.format(py_res))
	print 'Meta 1::', r
	if not r: return "FAIL"

	r = get_resource('/{}:meta2'.format(py_res))
	print 'Meta 2::', r
	if not r: return "FAIL"
	print

	print 'Reserving resource...', PROXY.reserve_resource(res_id)
	print 'Update resource::', set_resource(py_res, '/', {'more-info': 'y'})
	print 'Releasing resource...', PROXY.save_release_reserved_res(res_id)

	r = get_resource(res_id)
	print 'Check status::', r
	if 'more-info' not in r['meta']: return "FAIL"
	print

	for i in range(1, 4):

		print 'Reserving resource...', PROXY.reserve_resource(res_id)
		tag = 'tag{}'.format(i)
		r = set_resource(py_res, '/', {tag: str(i)})
		print 'Releasing resource...', PROXY.save_release_reserved_res(res_id)
		print 'Set tag `{}` = `{}` ... {}'.format(tag, i, r)
		if not r:
			print 'Could not save tag {}!'.format(tag)
			return "FAIL"

		path = '/' + py_res + ':' + tag
		r = rename_resource(path, 'tagx')
		print 'Rename tag `{}` = `tagx` ... {}'.format(path, r)
		if not r:
			print 'Could not rename tag {}!'.format(tag)
			return "FAIL"

		path = '/' + py_res + ':tagx'
		r = delete_resource(path)
		print 'Delete tag `{}` ... {}'.format(path, r)
		if not r:
			print 'Could not delete tag {}!'.format(tag)
			return "FAIL"
		print

	print 'Reserve resource::', reserve_resource(res_id)
	print

	print 'Delete resource::', delete_resource(res_id)
	r = get_resource(res_id)
	print 'Check info::', r
	if r: return "FAIL"
	print

	log_msg('logRunning', "TestCase: `{}` -  `{}`!\n".format(testName, error_code))
	log_msg('logTest', "TestCase: `{}` -  `{}`!\n".format(testName, error_code))

	# This return is used by the framework!
	return error_code

#

# Must have one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout'
_RESULT = test()
