
from ce_libs import *

try:
    pktact.pa_config = getOpenflowConfig(globEpName)
    pktact.pa_port_map = pktact.pa_config['port_map']
except:
    print 'Error: Invalid configuration for EPNAME: ' + str(globEpName)

class AllWildcardMatchTagged(BaseMatchCase):
    """
    AllWildcardMatch with tagged packets
    """
    def runTest(self):
        vid = test_param_get(self.config, 'vid', default=TEST_VID_DEFAULT)
        flow_match_test(self, pa_port_map, wildcards=ofp.OFPFW_ALL,
                        dl_vlan=vid)


tc = AllWildcardMatchTagged()
_RESULT = tc.run()
