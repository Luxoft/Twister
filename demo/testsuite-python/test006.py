
import os, sys, time
sys.path.append(os.getenv('HOME') + '/.twister_cache/')

#

def test006():

	import pexpect
	from ce_libs import logMsg
	from ce_libs import queryResource, setPropertyLocal, getPropertyLocal
	from ce_libs import createEmptyResource, delResource

	testName = 'test006.py'
	logMsg('logTest', "\nTestCase:%s starting\n" % testName)

	error_code = "PASS"

	print 'Queried...', queryResource("devicevendor:Avaya&&devicetype:PBX,moduletype:?")
	print 'Queried...', queryResource("devicetype:Contivity&&devicefamily:27XX&&devicemodel:2750SY")

	resid = createEmptyResource(0)

	setPropertyLocal(resid, "prop_1", "value_1")
	setPropertyLocal(resid, "prop_2", "value_2")

	print 'Prop 1:', getPropertyLocal(resid, "prop_1")
	print 'Prop 2:', getPropertyLocal(resid, "prop_2")

	print 'Deleting resource %s... %s.' % (resid, str(delResource(resid)))

	logMsg('logTest', "TestCase:%s %s\n" % (testName, error_code))
	return error_code

#

_RESULT = test006()
