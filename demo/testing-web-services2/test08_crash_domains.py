
# <title> Test 08 </title>

# version: 2.001
# <description> Negative testing DomainNamesChangedNotification. All exceptions must be caught, the test must pass. </description>

import time
from suds.client import Client
try: from ce_libs import logMsg
except:
	def logMsg(*args):
		print args

link = 'http://tsc-server:9090/axis2/services/AM_Server?wsdl'
c = Client(link)

print '\nConnected to SOAP Server at `%s`!\n' % link

#

def test():

	print 'Trying to add a changed notification without parameters:' ; time.sleep(1)
	try:
		c.service.DomainNamesChangedNotification()
		print 'This test should have failed! Error!'
		return 'FAIL'
	except Exception, e:
		print 'Exception:: `Zero parameters`!\n'


	print 'Creating domain with invalid action...' ; time.sleep(1)
	d1 = c.factory.create('domainNameChange')
	d1.domainName = 'Xxxxx'
	d1.action = 'Invalid'
	print d1, '\n'
	#
	print 'Creating array of domains without domains...' ; time.sleep(1)
	arr = c.factory.create('ArrayOfDomainNameChange')
	print 'The array:', arr, '\n'
	#
	print 'Trying to add a changed notification with empty array:' ; time.sleep(1)
	try:
		c.service.DomainNamesChangedNotification(arr)
		print 'This test should have failed! Error!'
		return 'FAIL'
	except Exception, e:
		print 'Exception:: `Empty array`!\n'


	print 'Adding domain to the array...'
	arr.domainNameChange.append(d1)
	print 'The array:', arr, '\n'
	#
	print 'Trying to add a changed notification with invalid action:' ; time.sleep(1)
	try:
		c.service.DomainNamesChangedNotification(arr)
		print 'This test should have failed! Error!'
		return 'FAIL'
	except Exception, e:
		print 'Exception:: `Invalid domain action`!\n'

	print 'Caught all exceptions !'
	return 'PASS'

#

_RESULT = test()

#
