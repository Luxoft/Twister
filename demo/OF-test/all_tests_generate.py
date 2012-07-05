
'''
This tests generates all Openflow Tests, using a list of tests
and the template.
'''

import os, sys
import json

tmpl = '''
import os, sys
import time
import unittest
sys.path.append(os.getenv('TWISTER_PATH') + '/.twister_cache/ce_libs')

from oft import *
init_all_tests()
build_test_name('{test_name}')

from oft import suite
runner = unittest.TextTestRunner(verbosity=1)
result = runner.run(suite)
time.sleep(2)

if result.wasSuccessful():
    _RESULT = "PASS"
else:
    _RESULT = "FAIL"
'''

try: os.mkdir('tests')
except: pass

all_tests = json.load(open('all_tests.txt', 'r'))

#
for suite in all_tests:
	#
	for test in suite['tests']:
		print 'Writing suite `%s`, file `%s`.' % (suite['name'], test)
		f = open('tests/' + suite['name'] + '_' + test + '.py', 'w')
		f.write(tmpl.format(test_name = test))
		f.close()
	#
#
print 'Done!'
#
