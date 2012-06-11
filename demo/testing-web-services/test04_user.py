
import time
from suds.client import Client

c = Client('http://localhost:55000/?wsdl')

print '\nConnected to SOAP Server.\n'

print 'Creating new user...'
u = c.factory.create("User")

u.user_name = 'John-Doe'
u.first_name = 'John'
u.last_name = 'Doe'
print '... Done.\n'

print 'The final user is:', u

print 'Adding user to the service...'
uid = c.service.add_user(u)
print 'User ID:', uid
print '... Done.\n'

print 'All users: ', c.service.get_all_users()

print 'Deleting user from the service...'
c.service.del_user(uid)
print '... Done.\n'

print 'All users: ', c.service.get_all_users()

print time.sleep(1)
print '\nOk!'

_RESULT = 'PASS'

#
