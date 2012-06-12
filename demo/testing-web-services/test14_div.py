
# <title> Test 14 - division function </title>
# <description> Testing the XML-RPC server: running division function 3 times </description>

import time
import xmlrpclib

proxy = xmlrpclib.ServerProxy('http://localhost:55001/')
print 'Connected to XML-RPC server:', proxy, '\n'

print proxy.echo('hellooo!')
print

print 'Testing XML-RPC div:', proxy.div(1230, 5)
print 'Testing XML-RPC div:', proxy.div(3456, 9)

try: print 'Testing XML-RPC div:', proxy.div(1, 'd')
except Exception, e: print 'Exception:', e

time.sleep(2)
_RETURN = 'PASS'
