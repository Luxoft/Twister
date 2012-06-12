
# <title> Test 13 - multiplication function </title>
# <description> Testing the XML-RPC server: running multiplication function 3 times </description>

import time
import xmlrpclib

proxy = xmlrpclib.ServerProxy('http://localhost:55001/')
print 'Connected to XML-RPC server:', proxy, '\n'

print proxy.echo('hellooo!')
print

print 'Testing XML-RPC mul:', proxy.mul(123, 765)
print 'Testing XML-RPC mul:', proxy.mul(345, 987)

try: print 'Testing XML-RPC mul:', proxy.dif(1, 'm')
except Exception, e: print 'Exception:', e

time.sleep(2)
_RETURN = 'PASS'
