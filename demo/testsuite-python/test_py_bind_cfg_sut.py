
# version: 2.002

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
print getBindId('ro1/A', 'c1.xml')
print getBindName('ro1/A', 'c1.xml')

print getBindId('ro1/B', 'c1.xml')
print getBindName('ro1/B', 'c1.xml')
print '\n'

# This must also be binded in the applet
# Gets the default
print getBindId('Component_1')
print getBindName('Component_1')

print getBindId('Component_2')
print getBindName('Component_2')
print '\n'

# Also gets the default
print getBindId('Component_1', 'c1.xml')
print getBindName('Component_1', 'c1.xml')

#

# Must have one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout', 'invalid'
_RESULT = 'pass'
