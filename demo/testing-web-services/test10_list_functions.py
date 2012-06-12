
# <title> Test 10 - list all exposed functions </title>
# <description> Testing the XML-RPC server: listing all available functions </description>

import time
import xmlrpclib

proxy = xmlrpclib.ServerProxy('http://localhost:55001/')
print 'Connected to XML-RPC server:', proxy, '\n'

print 'Available functions:', dir(proxy)

time.sleep(2)
_RESULT = 'PASS'
