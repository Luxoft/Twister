
import pexpect

from ce_libs import logMsg
from ce_libs import getResource, setResource, deleteResource, getResourceStatus
from ce_libs import allocResource, reserveResource, freeResource

#
# <title>test 006</title>
# <description>This test is checking the Resource Allocator.</description>
#

def test006():

	testName = 'test006.py'
	logMsg('logTest', "\nTestCase:%s starting\n" % testName)

	error_code = "PASS"

	print 'Query Root...', getResource(1)
	print 'Query Root...', getResource('/')
	print

	print 'Device 1::', getResource('/dev1')
	print 'Device 1::', getResource(101)
	print

	print 'Meta 1::', getResource('dev3/mod12:meta1')
	print 'Meta 2::', getResource('dev3/mod12:meta2')
	print

	id1 = setResource('test1', 'dev3/mod12', {'extra-info': 'yes'})
	print 'Create resource::', id1
	print 'Check info::', getResource(id1)
	print

	print 'Update resource::', setResource('test1', 'dev3/mod12', {'more-info': 'y'})
	print 'Check status::', getResource(id1)
	print

	print 'Check status 1::', getResourceStatus(id1)
	print 'Reserve resource::', reserveResource(id1)
	print 'Check status 2::', getResourceStatus(id1)
	print

	print 'Delete resource::', deleteResource(id1)
	print 'Check info::', getResource(id1)
	print

	logMsg('logTest', "TestCase:%s %s\n" % (testName, error_code))
	return error_code

#

_RESULT = test006()
