
from ce_libs import TelnetManager

#
# <title>Testing Twister Telnet library</title>
# <description>This test is connecting to a TELNET host.</description>
#

def test():
	'''
	Testing Twister Telnet library.
	'''

	conn = {
		'host': '11.126.32.16',
		'port': 23,
		'user': 'user',
		'passwd': 'password',
		'loging_prompt': 'login:',
		'passwd_prompt': 'Password',
	}

	tm = TelnetManager()

	print 'begin test'
	print '||||||||||||||||||||||||||||||||||||||||||||||'
	print 'open_connection'
	tm.open_connection('test', conn['host'], conn['port'], conn['user'], conn['passwd'],
							conn['loging_prompt'], conn['passwd_prompt'])
	tm.open_connection('test1', conn['host'], conn['port'], conn['user'], conn['passwd'],
							conn['loging_prompt'], conn['passwd_prompt'])
	tm.open_connection('test2', conn['host'], conn['port'], conn['user'], conn['passwd'],
							conn['loging_prompt'], conn['passwd_prompt'])
	tm.open_connection('test3', conn['host'], conn['port'], conn['user'], conn['passwd'],
							conn['loging_prompt'], conn['passwd_prompt'])

	print '||||||||||||||||||||||||||||||||||||||||||||||'
	print 'list_connections'
	print tm.list_connections()

	print '||||||||||||||||||||||||||||||||||||||||||||||'
	print 'get_connection'
	print tm.get_connection()

	print '||||||||||||||||||||||||||||||||||||||||||||||'
	print 'set_active_connection'
	print tm.set_active_connection('test')

	print '||||||||||||||||||||||||||||||||||||||||||||||'
	print 'get_connection'
	print tm.get_connection()

	print '||||||||||||||||||||||||||||||||||||||||||||||'
	print 'set_timeout'
	print tm.set_timeout(4)

	print '||||||||||||||||||||||||||||||||||||||||||||||'
	print 'set_newline'
	print tm.set_newline('\r\n')

	print '||||||||||||||||||||||||||||||||||||||||||||||'
	print 'write'
	print tm.write('ls')

	print '||||||||||||||||||||||||||||||||||||||||||||||'
	print 'read'
	print tm.read()

	print '||||||||||||||||||||||||||||||||||||||||||||||'
	print 'read_until'
	print tm.read_until('test')

	print '||||||||||||||||||||||||||||||||||||||||||||||'
	print 'close_connection default'
	print tm.close_connection()

	print '||||||||||||||||||||||||||||||||||||||||||||||'
	print 'list_connections'
	print tm.list_connections()

	print '||||||||||||||||||||||||||||||||||||||||||||||'
	print 'close_connection'
	print tm.close_connection('test3')

	print '||||||||||||||||||||||||||||||||||||||||||||||'
	print 'list_connections'
	print tm.list_connections()

	print '||||||||||||||||||||||||||||||||||||||||||||||'
	print 'close_all_connections'
	print tm.close_all_connections()

	print '||||||||||||||||||||||||||||||||||||||||||||||'
	print 'list_connections'
	print tm.list_connections()

	logMsg('Twister Telnet test done.')
	# This return is used by the framework!
	return "PASS"

#

# Must have one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout', 'invalid'
_RESULT = test()
