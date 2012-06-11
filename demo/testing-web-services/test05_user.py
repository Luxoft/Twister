
def func():

	import time
	from suds.client import Client

	c = Client('http://localhost:55000/?wsdl')

	print '\nConnected to SOAP Server.\n'

	print 'Creating new user...'
	u = c.factory.create('User')

	u.user_name = 'John-Doe'
	u.first_name = 'John'
	u.last_name = 'Doe'
	print '... Done.\n'

	print 'The final user is:', u

	print 'Adding user to the service...'
	try:
		uid = c.service.add_user(u)
		print 'User ID:', uid
	except Exception, e:
		print 'Cannot add user!'
		return 'FAIL'
	print '... Done.\n'

	print 'All users: ', c.service.get_all_users()

	print 'Deleting user from the service...'
	try:
		c.service.del_user(uid)
	except Exception, e:
		print 'Cannot delete user!'
		return 'FAIL'
	print '... Done.\n'

	print 'All users: ', c.service.get_all_users()

	print time.sleep(1)
	print '\nAdding and deleting users OK!'
	return 'PASS'

#

_RESULT = func()
