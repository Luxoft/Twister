
import time
from suds.client import Client

c = Client('http://localhost:55000/?wsdl')

print '\nConnected to SOAP Server:'
print str(c)[80:-1]

#

try:
	print 'Calling function with err: ', c.service.error_function()
except Exception, e:
	print 'Caught error:', e
	_RESULT = 'FAIL'
	exit(1)

print time.sleep(2)

_RESULT = 'PASS'

#
