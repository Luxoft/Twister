
# <title> Test 04 </title>

# version: 2.001
# <description> Testing service GetDomainNames. This should pass. </description>

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

result = c.service.GetDomainNames()

printLog('Methods: %s\n' % result) ; time.sleep(1)
logMsg('logDebug', 'XML Request was:\n' + str(c.last_sent()) + '\n\n\n')

if str(result) == '':
	printLog('The result is correct!\n\n')
	_RESULT = 'PASS'
else:
	printLog('The result is incorrect!\n\n')
	_RESULT = 'FAIL'

#
