
# version: 3.001

"""
<title>Test Configuration Files</title>
<description>Function `get_config` is included in the interpreter!<br>
This function should get a config, using the full path to config file and the full path to a config variable in that file.</description>
<tags>config files</tags>
"""

import os
from pprint import pformat

cfg_path = PROXY.get_user_variable('tcfg_path')

# Consider that this EP is running on the same machine with the Central Engine...
for cfg in os.listdir(cfg_path):
	print 'All params for `{}`:'.format(cfg)
	print pformat(get_config(cfg, ''), indent=4, width=60), '\n'
        print 'ITERATION value is: ' + ITERATION
        print 'First iterator value is: ' + FIRST_ITERATOR_VAL
        print 'First iterator name is: ' + FIRST_ITERATOR_NAME
        print 'First iterator component is: ' + FIRST_ITERATOR_COMP

#

# Must have one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout', 'invalid'
_RESULT = 'pass'
