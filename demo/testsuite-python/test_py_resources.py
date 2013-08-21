
# version: 2.003

# getResource, setResource and *the rest* are now included in the interpreter !
# No need to import anything !

#
# <title>Test Resource Allocator</title>
# <description>This test is checking the Resource Allocator.</description>
# <tags>testbed, resources, devices, SUTSs</tags>
#

from os import urandom
from binascii import hexlify

def test():

	testName = 'test_py_resources.py'
	logMsg('logTest', "\nTestCase: `{}` starting\n".format(testName))

	error_code = "PASS"

	print 'Query Root...', getResource(1)
	print 'Query Root...', getResource('/')
	print

	py_res = 'tb_' + hexlify(urandom(4))
	print 'Create a tb `{}`...'.format(py_res)
	res_id = setResource(py_res, '/', {'meta1': 1, 'meta2': 2})
	print 'Ok.\n'

	if not res_id:
		return "FAIL"

	r = getResource('/' + py_res)
	print 'Find device by name::', r
	if not r: return "FAIL"

	r = getResource(res_id)
	print 'Find device by ID::', r
	if not r: return "FAIL"
	print

	r = getResource('/{}:meta1'.format(py_res))
	print 'Meta 1::', r
	if not r: return "FAIL"

	r = getResource('/{}:meta2'.format(py_res))
	print 'Meta 2::', r
	if not r: return "FAIL"
	print

	print 'Update resource::', setResource(py_res, '/', {'more-info': 'y'})
	r = getResource(res_id)
	print 'Check status::', r
	if 'more-info' not in r['meta']: return "FAIL"
	print

	for i in range(1, 4):
		tag = 'tag{}'.format(i)
		r = setResource(py_res, '/', {tag: str(i)})
		print 'Set tag `{}` = `{}` ... {}'.format(tag, i, r)
		if not r: return "FAIL"

		path = '/' + py_res + ':' + tag
		r = renameResource(path, 'tagx')
		print 'Rename tag `{}` = `tagx` ... {}'.format(path, r)
		if not r: return "FAIL"

		path = '/' + py_res + ':tagx'
		r = deleteResource(path)
		print 'Delete tag `{}` ... {}'.format(path, r)
		if not r: return "FAIL"
		print

	print 'Check status 1::', getResourceStatus(res_id)
	print 'Reserve resource::', reserveResource(res_id)
	print 'Check status 2::', getResourceStatus(res_id)
	print

	print 'Delete resource::', deleteResource(res_id)
	r = getResource(res_id)
	print 'Check info::', r
	if r: return "FAIL"
	print

	logMsg('logTest', "TestCase:%s %s\n" % (testName, error_code))

	# This return is used by the framework!
	return error_code

#

# Must have one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout', 'invalid'
_RESULT = test()
