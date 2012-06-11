
from suds.client import Client

c = Client('http://localhost:8080/?wsdl')

print '\nConnected to SOAP Server:'
print str(c)[80:-1]

#

print 'Calling HELLO with int:', c.service.say_hello('Echo', 3)
print 'Calling HELLO with str:', c.service.say_hello('Echo', '3')
try:
	print 'Calling HELLO with err: ', c.service.say_hello(1)
except Exception, e:
	print 'Caught error:', e

print '\nOk!'

_RESULT = 'PASS'

#
