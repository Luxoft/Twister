
# <title> Test 01 </title>
# <description> Calling inexistent functions. All exceptions must be caught. </description>

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

printLog('Calling inexistent function `Echo`:') ; time.sleep(1)
try:
	c.service.Echo()
except Exception, e:
	printLog('Exception:: %s\n' % str(e))

printLog('Calling inexistent function `GetMethod`:')
try:
	c.service.GetMethod()
except Exception, e:
	printLog('Exception:: %s\n' % str(e))

#

_RESULT = 'PASS'

#
