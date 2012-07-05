
# <title> Test 12 - diff function </title>
# <description> Testing the XML-RPC server: running diff function 3 times </description>

import time
import xmlrpclib

proxy = xmlrpclib.ServerProxy('http://localhost:55001/')
print 'Connected to XML-RPC server:', proxy, '\n'

print proxy.echo('hellooo!')
print

print 'Testing XML-RPC dif:', proxy.dif(1230, 765)
print 'Testing XML-RPC dif:', proxy.dif(345, 9870)

try: print 'Testing XML-RPC dif:', proxy.dif(1, 'a')
except Exception, e: print 'Exception:', e

time.sleep(2)
_RESULT = 'PASS'
