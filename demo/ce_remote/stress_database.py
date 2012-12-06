#!/usr/bin/python

#
# <title>Stress Database</title>
# <description>Testing the Database.</description>
#

import os, sys
import time
import xmlrpclib

user    = os.getenv('USER')
config  = os.getenv('HOME') + '/twister/config/fwmconfig.xml'
project = os.getenv('HOME') + '/twister/config/stress_database.xml'

xml_data = '''
<Root>
	<stoponfail>false</stoponfail>
	<dbautosave>false</dbautosave>
	<TestSuite>
		<tsName>Stress Test</tsName>
		<EpId>EP-1001</EpId>

		<UserDefined>
			<propName>release_id</propName>
			<propValue>1</propValue>
		</UserDefined>
		<UserDefined>
			<propName>build_id</propName>
			<propValue>1</propValue>
		</UserDefined>
		<UserDefined>
			<propName>suite_id</propName>
			<propValue>1</propValue>
		</UserDefined>
		<UserDefined>
			<propName>station_id</propName>
			<propValue>1</propValue>
		</UserDefined>
		<UserDefined>
			<propName>comments</propName>
			<propValue>some comment</propValue>
		</UserDefined>
		<UserDefined>
			<propName>release</propName>
			<propValue>2</propValue>
		</UserDefined>
		<UserDefined>
			<propName>build</propName>
			<propValue>2</propValue>
		</UserDefined>
		<UserDefined>
			<propName>Run_Number</propName>
			<propValue>99</propValue>
		</UserDefined>
%s

	</TestSuite>
</Root>''' % ( '''
		<TestCase>
			<tcName>%s/twister/demo/testsuite-python/init.py</tcName>
			<Property>
				<propName>Runnable</propName>
				<propValue>true</propValue>
			</Property>
		</TestCase>''' % os.getenv('HOME') * 5 )

open(project, 'w').write(xml_data)

print('Starting CE for `{0}`, with `{1}` and `{2}`.'.format(user, config, project))

proxy = xmlrpclib.ServerProxy('http://127.0.0.1:8000/')

proxy.setExecStatusAll(user, 2, config + ',' + project)
time.sleep(1)

print('Waiting for the tests to finish...\n')
while not proxy.getExecStatusAll(user).startswith('stopped'):
	time.sleep(1)
print('Starting to save into database...')

c = '/-\|' # Cursors

for i in range(5):
	proxy.commitToDatabase(user)
	txt = 'Save number %i... %s' % (i, c[i%4])
	sys.stdout.write(txt)
	sys.stdout.flush()
	time.sleep(3)
	sys.stdout.write('\b' * len(txt))

del proxy
print('\n') # Fix the backspace

print('Success !')

# Eof()
