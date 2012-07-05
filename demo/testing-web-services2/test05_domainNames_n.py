
# <title> Test 05 </title>
# <description> Testing service GetDomainNames with wrong parameters. All exceptions must be caught, the test must pass. </description>

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

	printLog('Calling GetDomainNames with parameter 1...') ; time.sleep(1)
	try:
		c.service.GetDomainNames('x')
	except:
		printLog('Exception: The function does not accept parameters!\n')
	logMsg('logDebug', 'XML Request was:\n' + str(c.last_sent()) + '\n\n\n')

	s = c.factory.create('ArrayOfString')


	printLog('Calling GetDomainNames with parameter 2...') ; time.sleep(1)
	try:
		c.service.GetDomainNames(s)
	except:
		printLog('Exception: The function does not accept parameters!\n')
	logMsg('logDebug', 'XML Request was:\n' + str(c.last_sent()) + '\n\n\n')

	return 'PASS'

#

_RESULT = test()

#
