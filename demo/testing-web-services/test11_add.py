
# <title> Test 11 - add function </title>
# <description> Testing the XML-RPC server: running add function 3 times </description>

import time
import xmlrpclib

proxy = xmlrpclib.ServerProxy('http://localhost:55001/')
print 'Connected to XML-RPC server:', proxy, '\n'

print proxy.echo('hellooo!')
print

print 'Testing XML-RPC sum:', proxy.sum(123, 765)
print 'Testing XML-RPC sum:', proxy.sum(345, 987)

try: print 'Testing XML-RPC sum:', proxy.sum(1, 's')
except Exception, e: print 'Exception:', e

time.sleep(2)
_RESULT = 'PASS'
