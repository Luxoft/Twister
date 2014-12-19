
#
# <ver>version: 3.002</ver>
# <title>Test CommonLib and Resource Allocator / TestBed and Resources</title>
# <description>This suite checks the most basic functionality of Twister.<br>
# Functions `get_tb`, `set_tb` and *the rest* are included in the interpreter!</description>
# <tags>testbed, resources, devices</tags>
# <test>resource</test>
# <smoke>yes</smoke>
#

from os import urandom
from binascii import hexlify

def test():

	testName = 'test_resources.py'
	log_msg('logRunning', "\nTestCase: `{}` starting...\n".format(testName))
	log_msg('logTest', "\nTestCase: `{}` starting...\n".format(testName))

	error_code = "PASS"

	print 'Query Root (1)...', get_tb(1)
	print 'Query Root (/)...', get_tb('/')
	print

	print is_tb_reserved('/tb1')
	print get_tb_user('/tb1')
	print is_sut_reserved('/SUT1.user')
	print get_sut_user('/SUT1.user')
	print

	tb_name = 'tb_' + hexlify(urandom(4))
	print 'Create a tb `{}`...'.format(tb_name)
	tb_id = set_tb(tb_name, '/', {'meta1': 1, 'meta2': 2})
	print 'Ok.\n'

	if not tb_id:
		print('Could not create TB! {}'.format(tb_id))
		return 'FAIL'

	r = get_tb('/' + tb_name)
	print 'Find device by name::', r
	if not r: return 'FAIL'

	r = get_tb(tb_id)
	print 'Find device by ID::', r
	if not r: return 'FAIL'
	print

	r = get_tb('/{}:meta1'.format(tb_name))
	print 'Meta 1::', r
	if not r: return 'FAIL'

	r = get_tb('/{}:meta2'.format(tb_name))
	print 'Meta 2::', r
	if not r: return 'FAIL'
	print

	print 'Reserving resource...', reserve_tb(tb_id)
	print 'Update resource::', set_tb(tb_name, '/', {'more-info': 'y'})
	print 'Saving resource...', save_reserved_tb(tb_id)
	print

	print 'Reserving resource...', reserve_tb(tb_id)
	print 'Update resource::', set_tb(tb_name, '/', {'more-info': 'y'})
	print 'Saving resource...', save_reserved_tb(tb_id)
	print

	child_id = set_tb('child', tb_id, {'some-meta': 'y'})
	print 'Create child::', child_id
	print 'Releasing resource...', save_release_reserved_tb(tb_id)
	print 'Child by name::', get_tb('/{}/child'.format(tb_name))
	print 'Child by ID::', get_tb(child_id)
	print

	r = get_tb(tb_id)
	print 'Check status::', r
	if 'more-info' not in r['meta']:
		print 'The meta was not updated!'
		return 'FAIL'
	print

	for i in range(1, 4):

		print 'Reserving resource...', reserve_tb(tb_id)
		tag = 'tag{}'.format(i)
		r = update_meta_tb(tb_name, '/', {tag: str(i)})

		print 'Set tag `{}` = `{}` ... {}'.format(tag, i, r)
		if not r:
			print 'Could not save tag {}!'.format(tag)
			return 'FAIL'

		path = tb_id + ':' + tag
		r = rename_tb(path, 'tagx')
		print 'Rename tag `{}` = `tagx` ... {}'.format(path, r)
		if not r:
			print 'Could not rename tag {}!'.format(tag)
			return 'FAIL'

		path = tb_id + ':tagx'
		r = delete_tb(path)
		print 'Delete tag `{}` ... {}'.format(path, r)
		if not r:
			print 'Could not delete tag `tagx`!'
			return 'FAIL'

		print 'Creating tag again...'
		r = update_meta_tb(tb_name, '/', {tag: str(i)})

		print 'Set tag `{}` = `{}` ... {}'.format(tag, i, r)
		if not r:
			print 'Could not save tag {}!'.format(tag)
			return 'FAIL'

		path = '/' + tb_name + ':' + tag
		r = rename_tb(path, 'tagx')
		print 'Rename tag `{}` = `tagx` ... {}'.format(path, r)
		if not r:
			print 'Could not rename tag {}!'.format(tag)
			return 'FAIL'

		path = '/' + tb_name + ':tagx'
		r = delete_tb(path)
		print 'Delete tag `{}` ... {}'.format(path, r)
		if not r:
			print 'Could not delete tag `tagx`!'
			return 'FAIL'

		print 'Releasing resource...', save_release_reserved_tb(tb_id)
		print


	print 'Reserving resource...', reserve_tb(tb_id)
	r = rename_tb(tb_id, 'test_resource')
	print 'Renaming resource by ID::', r
	if not r: return 'FAIL'
	print 'Releasing resource...', save_release_reserved_tb(tb_id)
	print

	print 'Reserving resource...', reserve_tb(tb_id)
	r = rename_tb('/test_resource', tb_name)
	print 'Renaming resource by name::', r
	if not r: return 'FAIL'
	print 'Releasing resource...', save_release_reserved_tb(tb_id)
	print


	print 'Delete resource::', delete_tb(tb_id)
	r = get_tb(tb_id)
	print 'Check info::', r
	if isinstance(r, dict):
		return 'FAIL'
	print

	print 'Everything is ok.'

	log_msg('logRunning', "TestCase: `{}` -  `{}`!\n".format(testName, error_code))
	log_msg('logTest', "TestCase: `{}` -  `{}`!\n".format(testName, error_code))

	# This return is used by the framework!
	return error_code

#

# Must have one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout'
_RESULT = test()
