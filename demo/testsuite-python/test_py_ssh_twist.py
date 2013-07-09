
# version: 2.002

from TscSshLib import SshManager

#
# <title>Testing Twister Ssh library</title>
# <description>This test is connecting to a Ssh host.</description>
#

def test():
	'''
	Testing Twister Ssh library.
	'''

	conn = {
		'host': 'host',
		'port': 22,
		'user': 'username',
		'passwd': 'password',
	}

	sm = SshManager()

	print 'begin test'
	print '||||||||||||||||||||||||||||||||||||||||||||||'
	print 'open_connection'
	sm.open_connection('test', conn['host'], conn['user'],
						conn['passwd'], conn['port'])
	sm.open_connection('test1', conn['host'], conn['user'],
						conn['passwd'], conn['port'])
	sm.open_connection('test2', conn['host'], conn['user'],
						conn['passwd'], conn['port'])
	sm.open_connection('test3', conn['host'], conn['user'],
						conn['passwd'], conn['port'])

	print '||||||||||||||||||||||||||||||||||||||||||||||'
	print 'list_connections'
	print sm.list_connections()

	print '||||||||||||||||||||||||||||||||||||||||||||||'
	print 'get_connection'
	print sm.get_connection()

	print '||||||||||||||||||||||||||||||||||||||||||||||'
	print 'set_active_connection'
	print sm.set_active_connection('test')

	print '||||||||||||||||||||||||||||||||||||||||||||||'
	print 'get_connection'
	print sm.get_connection()

	print '||||||||||||||||||||||||||||||||||||||||||||||'
	print 'set_timeout'
	print sm.set_timeout(4)

	print '||||||||||||||||||||||||||||||||||||||||||||||'
	print 'write'
	print sm.write('ls')

	print '||||||||||||||||||||||||||||||||||||||||||||||'
	print 'read'
	print sm.read()

	print '||||||||||||||||||||||||||||||||||||||||||||||'
	print 'close_connection default'
	print sm.close_connection()

	print '||||||||||||||||||||||||||||||||||||||||||||||'
	print 'list_connections'
	print sm.list_connections()

	print '||||||||||||||||||||||||||||||||||||||||||||||'
	print 'close_connection'
	print sm.close_connection('test3')

	print '||||||||||||||||||||||||||||||||||||||||||||||'
	print 'list_connections'
	print sm.list_connections()

	print '||||||||||||||||||||||||||||||||||||||||||||||'
	print 'close_all_connections'
	print sm.close_all_connections()

	print '||||||||||||||||||||||||||||||||||||||||||||||'
	print 'list_connections'
	print sm.list_connections()

	logMsg('Twister Ssh test done.')
	# This return is used by the framework!
	return "PASS"

#

# Must have one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout', 'invalid'
_RESULT = test()
