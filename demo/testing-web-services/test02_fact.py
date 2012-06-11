
from suds.client import Client

c = Client('http://localhost:8080/?wsdl')

print '\nConnected to SOAP Server:'
print str(c)[80:-1]

#

print 'Calling FACTORIAL with int:', c.service.factorial(9)
print 'Calling FACTORIAL with str:', c.service.factorial('9')
try:
	print 'Calling HELLO with err: ', c.service.factorial('a')
except Exception, e:
	print 'Caught error:', e

print '\nOk!'

_RESULT = 'PASS'

#
