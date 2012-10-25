
from oftest_parser import *

template="""
from ce_libs import *

try:
    errormsg.config = getOpenflowConfig(globEpName)
    errormsg.errormsg_port_map = pktact.pa_config['port_map']
except:
    print 'Error: Invalid configuration for EPNAME: ' + str(globEpName)

%s

tc = %s()
_RESULT = tc.run()
"""

config={
"tc_template":template,
"tc_suite":"../oflib/errormsg.py",
"tc_list_name":"errormsg_list",
"tc_ignore_list":[],
"tc_path":"../tests/"
}
parse_test_suite(config)
