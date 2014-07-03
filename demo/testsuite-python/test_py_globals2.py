
# version: 2.001

"""
<title>Testing Globals</title>
<description>This test is setting some complex global variables, that will be used in the next tests.
The variables can be accessed both from Python and TCL.</description>
"""

def func1():
	print 'Some function #1'
	return 1

def func2():
	print 'Some function #2'
	return 2

class Class1:
	pass

class Class2(object):
	x = 1

#

print 'Setting 2 functions, 2 classes and 2 instances, for using in the next tests!'

set_global('func1', func1)
set_global('func2', func2)
set_global('Class1', Class1)
set_global('Class2', Class2)
set_global('Class1i', Class1())
set_global('Class2i', Class2())

#

# Must have one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout', 'invalid'
_RESULT = 'pass'
