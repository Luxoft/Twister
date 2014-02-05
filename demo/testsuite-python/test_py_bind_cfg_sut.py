
# version: 2.001

"""
<title>Test a cfg -> SUT bindings</title>
<description>Function `getBinding` is included in the interpreter!<br>
This function should get a config, using the full path to config file and the full path to a config variable in that file.</description>
<tags>bindings</tags>
"""

bindings = PROXY.getUserVariable('bindings')

print 'Bindings found :: {}\n'.format(bindings)

for b in bindings:
	print 'Binding for `{}` ->'.format(b), getBinding(b), '...'

print '\nConfig files for this testcase :: {}\n'.format(CONFIG)

# This must be binded in the applet, or it will be False
print getBind('ro1/A', 'c1.xml')
print getBind('ro1/B', 'c1.xml')

# This must also be binded in the applet
print getBind('Component_1') # Gets the default
print getBind('Component_2')

#

# Must have one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout', 'invalid'
_RESULT = 'pass'
