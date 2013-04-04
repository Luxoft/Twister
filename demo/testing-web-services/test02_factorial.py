
# <title> Test 02 - factorial </title>

# version: 2.001
# <description> Testing the SOAP server: running Factorial function 3 times, the last time with wrong parameters </description>

import time
from suds.client import Client

c = Client('http://localhost:55000/?wsdl')

print '\nConnected to SOAP Server:'
print str(c)[80:-1]

#

print 'Calling FACTORIAL with int:', c.service.factorial(9)
print 'Calling FACTORIAL with str:', c.service.factorial('9')
try:
	print 'Calling HELLO with err: ', c.service.factorial('a')
except Exception, e:
	print 'Caught error:', e

print time.sleep(2)
print '\nFactorial function OK!'

_RESULT = 'PASS'

#
