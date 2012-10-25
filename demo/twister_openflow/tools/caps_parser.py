
from oftest_parser import *

template="""
from ce_libs import *

try:
    caps.caps_config = getOpenflowConfig(EP)
    caps.caps_port_map = caps.caps_config['port_map']
except:
    print 'Error: Invalid configuration for EPNAME: ' + str(EP)

%s

tc = %s()
_RESULT = tc.run()
"""

config={
"tc_template":template,
"tc_suite":"../oflib/caps.py",
"tc_list_name":"caps_list",
"tc_ignore_list":[],
"tc_path":"../tests/"
}
parse_test_suite(config)
