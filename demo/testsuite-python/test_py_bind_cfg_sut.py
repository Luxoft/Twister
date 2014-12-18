
# version: 3.002

"""
<title>Test a cfg -> SUT bindings</title>
<description>Function `get_binding` is included in the interpreter!<br>
This function should get a config, using the full path to config file and the full path to a config variable in that file.</description>
<tags>bindings</tags>
"""
import json

bindings = PROXY.get_user_variable('bindings')

print 'Bindings found :: {}\n'.format(json.dumps(bindings, indent=4))

for b in bindings:
	print 'Binding for `{}` ->'.format(b), get_binding(b), '...'

print '\nCONFIG FILES for this testcase :: {}\n'.format(CONFIG)

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
print

print get_bind_id('Component_2')
print get_bind_name('Component_2')
print

# Also gets the default
print get_bind_id('Component_1', 'c1.xml')
print get_bind_name('Component_1', 'c1.xml')
print

print 'CONFIG: ', CONFIG
config_name = CONFIG[0].strip()
component_name = get_config(config_name).keys()[0]


print 'Testing the API with valid configuration: {}/{} -> {}'.format(config_name, component_name, SUT)
print 'Get bind `{}/{}`: {}'.format(config_name, component_name,
	get_bind_name(component_name, config_name))

print 'Set bind `{}/{} -> {}`: {}'.format(config_name, component_name, SUT,
	set_binding(config_name, component_name, SUT))

print 'Get bind again `{}/{}`: {}'.format(config_name, component_name,
	get_bind_name(component_name, config_name))

print 'Del bind `{}/{}`: {}'.format(config_name, component_name,
	del_binding(config_name, component_name))

print 'Get bind again `{}/{}`: {}'.format(config_name, component_name,
	get_bind_name(component_name, config_name))
print


config_name_alter = 'mumu' + config_name
print 'Testing the API with invalid config_name: {}/{} -> {}'.format(config_name_alter, component_name, SUT)
print 'Get bind `{}/{}`: {}'.format(config_name_alter, component_name,
	get_bind_name(component_name, config_name_alter))

print 'Set bind again `{}/{} -> {}`: {}'.format(config_name_alter, component_name, SUT,
	set_binding(config_name_alter, component_name, SUT))

print 'Get bind `{}/{}`: {}'.format(config_name_alter, component_name,
	get_bind_name(component_name, config_name_alter))

print 'Del bind again `{}/{}`: {}'.format(config_name_alter, component_name,
	del_binding(config_name_alter, component_name))

print 'Get bind again `{}/{}`: {}'.format(config_name_alter, component_name,
	get_bind_name(component_name, config_name_alter))
print


SUT_alter = '12'+SUT+'.user'
print 'Testing the API with invalid sut: {}/{} -> {}'.format(config_name, component_name, SUT_alter)
print 'Get bind `{}/{}`: {}'.format(config_name, component_name,
	get_bind_name(component_name, config_name))

print 'Set bind `{}/{} -> {}`: {}'.format(config_name, component_name, SUT_alter,
	set_binding(config_name, component_name, SUT_alter))

print 'Get bind `{}/{}`: {}'.format(config_name, component_name,
	get_bind_name(component_name, config_name))
print


component_name_alter = 'mumu' + component_name
print 'Testing the API with invalid component_name: {}/{} -> {}'.format(config_name, component_name_alter, SUT)
print 'Get bind `{}/{}`: {}'.format(config_name, component_name_alter,
	get_bind_name(component_name_alter, config_name))

print 'Set bind `{}/{} -> {}`: {}'.format(config_name, component_name_alter, SUT,
	set_binding(config_name, component_name_alter, SUT))

print 'Get bind `{}/{}`: {}'.format(config_name, component_name_alter,
	get_bind_name('mumu'+component_name_alter, config_name))

print 'Del bind again `{}/{}`: {}'.format(config_name, component_name_alter,
	del_binding(config_name, component_name_alter))

print 'Get bind again `{}/{}`: {}'.format(config_name, component_name_alter,
	get_bind_name(component_name_alter, config_name))
print

#

# Must have one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout', 'invalid'
_RESULT = 'pass'
