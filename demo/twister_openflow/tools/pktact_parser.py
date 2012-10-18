
from oftest_parser import *

template="""
from ce_libs import *

try:
    pktact.pa_config=getOpenflowConfig(globEpName)
    pktact.pa_port_map= pktact.pa_config[\'port_map\']
except:
    print \"Error: Invalid configuration for EPNAME: \" + str(globEpName)

%s

tc = %s()
_RESULT = tc.run()
"""

config={
"tc_template":template,
"tc_suite":"../oflib/pktact.py",
"tc_list_name":"pktact_list",
"tc_ignore_list":[],
"tc_path":"../tests/"
}
parse_test_suite(config)
