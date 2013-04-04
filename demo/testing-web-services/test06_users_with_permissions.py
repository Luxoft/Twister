
# <title> Test 06 - create users with permissions </title>

# version: 2.001
# <description> Testing the SOAP server: create many complex data structures and submit them to the server (users with permissions) </description>

def func():

	import time
	from suds.client import Client

	c = Client('http://localhost:55000/?wsdl')

	print '\nConnected to SOAP Server.\n'

	print 'Creating new user...'
	u = c.factory.create('User')

	u.user_name = 'John-Permissions'
	u.first_name = 'John'
	u.last_name = 'Doe'
	print '... Done.\n'

	print 'Creating permissions array for user...'
	u.permissions = c.factory.create("PermissionArray")
	print '... Done.\n'

	print 'Creating first permission for user...'
	permission = c.factory.create("Permission")
	permission.application = 'table'
	permission.operation = 'write'
	print permission
	try:
		u.permissions.Permission.append(permission)
	except Exception, e:
		print 'Cannot add permission!'
		return 'FAIL'
	print '... Done.\n'

	print 'Creating second permission for user...'
	permission = c.factory.create("Permission")
	permission.application = 'table'
	permission.operation = 'read'
	print permission
	try:
		u.permissions.Permission.append(permission)
	except Exception, e:
		print 'Cannot add permission!'
		return 'FAIL'
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

	print 'All users:', c.service.get_all_users()

	print time.sleep(1)
	print '\nAdding permissions OK!'
	return 'PASS'

#

_RESULT = func()
