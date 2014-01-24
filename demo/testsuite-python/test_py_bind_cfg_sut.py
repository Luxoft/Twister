
# version: 2.001

"""
<title>Test a cfg -> SUT bindings</title>
<description>Function `getBinding` is included in the interpreter!<br>
This function should get a config, using the full path to config file and the full path to a config variable in that file.</description>
<tags>bindings</tags>
"""

bindings = PROXY.getUserVariable('bindings')

for b in bindings:
	print 'Binding for `{}` ->'.format(b), getBinding(b), '...'

#

# Must have one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout', 'invalid'
_RESULT = 'pass'
