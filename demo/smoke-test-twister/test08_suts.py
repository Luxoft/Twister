
#
# <ver>version: 3.003</ver>
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

	sut_name = 'sut_' + hexlify(urandom(4)) + '.system'
	print 'Create a root SUT `{}`...'.format(sut_name)
	sut_id = set_sut(sut_name, '/', {'meta1': 1, 'meta2': 2})
	print 'Ok.\n'

	if not sut_id:
		_REASON = 'Cannot create sut!'
		return 'FAIL', _REASON

	r = get_sut('/' + sut_name)
	print 'Find SUT by name::', r
	if not r:
		_REASON = 'Cannot find sut by name!'
		return 'FAIL', _REASON

	r = get_sut(sut_id)
	print 'Find SUT by ID::', r
	if not r:
		_REASON = 'Cannot find sut by ID!'
		return 'FAIL', _REASON
	print

	r = get_info_sut('/{}:meta1'.format(sut_name))
	print 'Meta 1::', r
	if not r:
		_REASON = 'Cannot get meta1!'
		return 'FAIL', _REASON

	r = get_info_sut('{}:meta2'.format(sut_id))
	print 'Meta 2::', r
	if not r:
		_REASON = 'Cannot get meta2!'
		return 'FAIL', _REASON
	print

	print 'Reserving SUT...', reserve_sut(sut_id)
	print
	print 'Reserving SUT...', reserve_sut(sut_id)
	child_id = set_sut('child', sut_id, {'some-meta': 'y'})
	print 'Create child::', child_id
	print 'Find by name::', get_sut('/{}/child'.format(sut_name))
	print 'Find by ID::', get_sut(child_id)
	print 'Releasing SUT...', save_release_reserved_sut(sut_id)
	print


	for i in range(1, 4):
		print 'Reserving SUT...', reserve_sut(sut_id)

		tag = 'tag{}'.format(i)
		r = set_sut(sut_name, '/', {tag: str(i)})
		print 'Set tag `{}` = `{}` ... {}'.format(tag, i, r)
		if not r:
			_REASON = 'Cannot set tag!'
			return 'FAIL', _REASON

		path = '/' + sut_name + ':' + tag
		r = PROXY.rename_meta_sut(path, 'tagx')
		print 'Rename tag `{}` = `tagx` ... {}'.format(path, r)
		if not r:
			_REASON = 'Cannot rename tag!'
			return 'FAIL', _REASON

		print 'Renamed meta::', get_info_sut('{}:tagx'.format(sut_id))

		path = '/' + sut_name + ':tagx'
		r = delete_component_sut(path)
		print 'Delete tag `{}` ... {}'.format(path, r)
		if not r:
			_REASON = 'Cannot delete tag!'
			return 'FAIL', _REASON

		print 'Releasing SUT...\n', save_release_reserved_sut(sut_id)
		print


	r = rename_sut('/' + sut_name, 'test_sut')
	print 'Renaming SUT::', r
	if r.lower() != 'true':
		_REASON = 'Cannot rename sut!'
		return 'FAIL', _REASON
	r = rename_sut('/test_sut.system', sut_name)
	print 'Renaming SUT again::', r
	if r.lower() != 'true':
		_REASON = 'Cannot rename sut!'
		return 'FAIL', _REASON
	print

	print 'Delete SUT::', delete_sut('/' + sut_name)
	r = get_sut(sut_id)
	print 'Check info::', r
	if isinstance(r, dict):
		_REASON = 'Cannot delete sut!'
		return 'FAIL', _REASON
	print

	log_msg('logRunning', "TestCase: `{}` -  `{}`!\n".format(testName, error_code))
	log_msg('logTest', "TestCase: `{}` -  `{}`!\n".format(testName, error_code))

	# This return is used by the framework!
	return error_code, ''

#

# Must have one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout'
_RESULT, _REASON = test()
