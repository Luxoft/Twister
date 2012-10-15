
from ce_libs import *

try:
    pktact.pa_config=getOpenflowConfig(globEpName)
    pktact.pa_port_map= pktact.pa_config['port_map']
except:
    print "Error: Invalid configuration for EPNAME: " + str(globEpName)

class ExactMatchTagged(BaseMatchCase):
    """
    Exact match for all port pairs with tagged pkts
    """

    def runTest(self):
        vid = test_param_get(self.config, 'vid', default=TEST_VID_DEFAULT)
        flow_match_test(self, pa_port_map, dl_vlan=vid)


tc = ExactMatchTagged()
_RESULT = tc.run()
