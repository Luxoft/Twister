
# version: 2.002

"""
<title>Test a cfg -> SUT bindings</title>
<description>Function `get_binding` is included in the interpreter!<br>
This function should get a config, using the full path to config file and the full path to a config variable in that file.</description>
<tags>bindings</tags>
"""

bindings = PROXY.get_user_variable('bindings')

print 'Bindings found :: {}\n'.format(bindings)

for b in bindings:
	print 'Binding for `{}` ->'.format(b), get_binding(b), '...'

print '\nConfig files for this testcase :: {}\n'.format(CONFIG)

# This must be binded in the applet, or it will be False
print get_bind_id('ro1/A', 'c1.xml')
print get_bind_name('ro1/A', 'c1.xml')

print get_bind_id('ro1/B', 'c1.xml')
print get_bind_name('ro1/B', 'c1.xml')
print '\n'

# This must also be binded in the applet
# Gets the default
print get_bind_id('Component_1')
print get_bind_name('Component_1')

print get_bind_id('Component_2')
print get_bind_name('Component_2')
print '\n'

# Also gets the default
print get_bind_id('Component_1', 'c1.xml')
print get_bind_name('Component_1', 'c1.xml')

#

# Must have one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout', 'invalid'
_RESULT = 'pass'
