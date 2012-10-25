
from oftest_parser import *

template="""
from ce_libs import *

try:
    basic.basic_config = getOpenflowConfig(EP)
    basic.basic_port_map = basic.basic_config['port_map']
except:
    print 'Error: Invalid configuration for EPNAME: ' + str(EP)

%s

tc = %s()
_RESULT = tc.run()
"""

config={
"tc_template":template,
"tc_suite":"../oflib/basic.py",
"tc_list_name":"basic_list",
"tc_ignore_list":["DataPlaneOnly"],
"tc_path":"../tests/"
}
parse_test_suite(config)
