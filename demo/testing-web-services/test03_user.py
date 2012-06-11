
from suds.client import Client

c = Client('http://localhost:8080/?wsdl')

print '\nConnected to SOAP Server.\n'

print 'Creating temporary user...'
u = c.factory.create("User")

u.user_name = 'John-Doe'
u.first_name = 'John'
u.last_name = 'Doe'
u.email = 'john-doe@site.com'
print '... Done.\n'

print 'The final user is:', u

print '\nOk!'

_RESULT = 'PASS'

#
