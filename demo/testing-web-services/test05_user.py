
from suds.client import Client

c = Client('http://localhost:8080/?wsdl')

print '\nConnected to SOAP Server.\n'

print 'Creating new user...'
u = c.factory.create("User")

u.user_name = 'John-Doe'
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
u.permissions.Permission.append(permission)
print '... Done.\n'

print 'Creating second permission for user...'
permission = c.factory.create("Permission")
permission.application = 'table'
permission.operation = 'read'
print permission
u.permissions.Permission.append(permission)
print '... Done.\n'

print 'The final user is:', u

print 'Adding user to the service...'
uid = c.service.add_user(u)
print 'User ID:', uid
print '... Done.\n'

print 'All users:', c.service.get_all_users()

print '\nOk!'

_RESULT = 'PASS'

#
