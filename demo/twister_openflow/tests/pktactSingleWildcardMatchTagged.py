
from ce_libs import *

try:
    pktact.pa_config = getOpenflowConfig(globEpName)
    pktact.pa_port_map = pktact.pa_config['port_map']
except:
    print 'Error: Invalid configuration for EPNAME: ' + str(globEpName)

class SingleWildcardMatchTagged(BaseMatchCase):
    """
    SingleWildcardMatch with tagged packets
    """
    def runTest(self):
        vid = test_param_get(self.config, 'vid', default=TEST_VID_DEFAULT)
        for wc in WILDCARD_VALUES:
            flow_match_test(self, pa_port_map, wildcards=wc, dl_vlan=vid,
                            max_test=10)


tc = SingleWildcardMatchTagged()
_RESULT = tc.run()
