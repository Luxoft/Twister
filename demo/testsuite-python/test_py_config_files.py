
# version: 2.001

"""
<title>Test Configuration Files</title>
<description>Function `getConfig` is included in the interpreter!<br>
This function should get a config, using the full path to config file and the full path to a config variable in that file.</description>
<tags>config files</tags>
"""

import os
from pprint import pformat

cfg_path = PROXY.getUserVariable(USER, 'tcfg_path')

# Consider that this EP is running on the same machine with the Central Engine...
cfg_files = [ (cfg_path +'/'+ p) for p in os.listdir(cfg_path) if os.path.isfile(cfg_path +'/'+ p) ]

for cfg in cfg_files:
	print 'All params for `{}`:'.format(cfg)
	print pformat(getConfig(cfg, ''), indent=4, width=60), '\n'

#

# Must have one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout', 'invalid'
_RESULT = 'pass'
