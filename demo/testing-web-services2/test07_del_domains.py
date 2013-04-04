
# <title> Test 07 </title>

# version: 2.001
# <description> Create delete actions and test DomainNamesChangedNotification function. This test must pass. </description>

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

	printLog('Creating action to delete domain 1...') ; time.sleep(1)
	d1 = c.factory.create('domainNameChange')
	d1.domainName = None
	d1.oldDomainName = 'Google'
	d1.action = 'Delete'

	printLog('Creating action to delete domain 2...') ; time.sleep(1)
	d2 = c.factory.create('domainNameChange')
	d2.domainName = None
	d2.oldDomainName = 'Yahoo'
	d2.action = 'Delete'

	printLog('Creating action to delete domain 3...') ; time.sleep(1)
	d3 = c.factory.create('domainNameChange')
	d3.domainName = None
	d3.oldDomainName = 'Microsoft'
	d3.action = 'Delete'


	printLog('Creating array of domains...\n') ; time.sleep(1)
	arr = c.factory.create('ArrayOfDomainNameChange')

	printLog('Adding domains in the array...') ; time.sleep(1)
	arr.domainNameChange.append(d1)
	arr.domainNameChange.append(d2)
	arr.domainNameChange.append(d3)
	printLog('The array is: %s\n' % arr)

	printLog('Call change domain names function...')
	c.service.DomainNamesChangedNotification(arr)
	logMsg('logDebug', 'XML Request was:\n' + str(c.last_sent()) + '\n\n\n')


	print 'Testing if there are 0 domains registered...\n' ; time.sleep(1)
	result = c.service.GetDomainNames()

	if str(result) == '':
		print 'Test okay!'
		return 'PASS'
	else:
		print 'Test failed!'
		print 'The result was:', result
		return 'FAIL'

#

_RESULT = test()

#
