
# <title> Test 06 </title>
# <description> Create domains and test function DomainNamesChangedNotification. This test must pass. </description>

import time
from suds.client import Client
try: from ce_libs import logMsg
except:
	def logMsg(*args):
		print args

def printLog(args):
	print args
	logMsg('logDebug', args)

link = 'http://tsc-server:9090/axis2/services/AM_Server?wsdl'
c = Client(link)

print '\nConnected to SOAP Server at `%s`!\n' % link

#

def test():

	printLog('Creating domain 1...') ; time.sleep(1)
	d1 = c.factory.create('domainNameChange')
	d1.domainName = 'Google'
	d1.action = 'Add'
	printLog(str(d1) + '\n')

	printLog('Creating domain 2...') ; time.sleep(1)
	d2 = c.factory.create('domainNameChange')
	d2.domainName = 'Yahoo'
	d2.action = 'Add'
	printLog(str(d2) + '\n')

	printLog('Creating domain 3...') ; time.sleep(1)
	d3 = c.factory.create('domainNameChange')
	d3.domainName = 'Microsoft'
	d3.action = 'Add'
	printLog(str(d3) + '\n')


	printLog('Creating array of domains...\n') ; time.sleep(1)
	arr = c.factory.create('ArrayOfDomainNameChange')

	printLog('Adding domains in the array...') ; time.sleep(1)
	arr.domainNameChange.append(d1)
	arr.domainNameChange.append(d2)
	arr.domainNameChange.append(d3)
	printLog('The array is: %s\n' % str(arr))

	printLog('Call change domain names function...')
	c.service.DomainNamesChangedNotification(arr)
	logMsg('logDebug', 'XML Request was:\n' + str(c.last_sent()) + '\n\n\n')


	print 'Testing if there are 3 domains registered...\n' ; time.sleep(1)
	result = c.service.GetDomainNames()
	expected = c.factory.create('ArrayOfString')
	expected.string = ['Google', 'Yahoo', 'Microsoft']

	if str(result) == str(expected):
		print 'Test okay!'
		return 'PASS'
	else:
		print 'Test failed!'
		print 'The result was:', result
		return 'FAIL'

#

_RESULT = test()

#
