
from ce_libs import *

try:
    pktact.pa_config=getOpenflowConfig(globEpName)
    pktact.pa_port_map= pktact.pa_config['port_map']
except:
    print "Error: Invalid configuration for EPNAME: " + str(globEpName)

class AllExceptOneWildcardMatchTagged(BaseMatchCase):
    """
    Match one field with tagged packets
    """
    def runTest(self):
        vid = test_param_get(self.config, 'vid', default=TEST_VID_DEFAULT)
        for wc in WILDCARD_VALUES:
            all_exp_one_wildcard = ofp.OFPFW_ALL ^ wc
            flow_match_test(self, pa_port_map, wildcards=all_exp_one_wildcard,
                            dl_vlan=vid)


tc = AllExceptOneWildcardMatchTagged()
_RESULT = tc.run()
