
# <title> Test 03 - a function with an error </title>

# version: 2.001
# <description> Testing a function with an error, on the SOAP server </description>

def func():

	import time
	from suds.client import Client

	c = Client('http://localhost:55000/?wsdl')

	print '\nConnected to SOAP Server:'
	print str(c)[80:-1]

	try:
		print 'Calling function with err: ', c.service.error_function()
	except Exception, e:
		print time.sleep(2)
		print 'Caught error:', e
		return 'FAIL'

	print time.sleep(2)
	return 'PASS'

#

_RESULT = func()
