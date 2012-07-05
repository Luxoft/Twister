
# <title> Test 04 - create user </title>
# <description> Testing the SOAP server: receive a complex data atructure from the server (user object) and create an instance of that structure </description>

def func():

	import time
	from suds.client import Client

	c = Client('http://localhost:55000/?wsdl')

	print '\nConnected to SOAP Server.\n'

	print 'Creating temporary user...'
	u = c.factory.create('User')

	u.user_name = 'John-Doe'
	u.first_name = 'John'
	u.last_name = 'Doe'
	u.email = 'john-doe@site.com'
	print '... Done.\n'

	print 'The final user is:', u

	print time.sleep(2)
	print '\nCreating new user OK!'
	return 'PASS'

#

_RESULT = func()
