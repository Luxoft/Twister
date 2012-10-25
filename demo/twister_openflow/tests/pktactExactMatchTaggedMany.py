
from ce_libs import *

try:
    pktact.pa_config = getOpenflowConfig(globEpName)
    pktact.pa_port_map = pktact.pa_config['port_map']
except:
    print 'Error: Invalid configuration for EPNAME: ' + str(globEpName)

class ExactMatchTaggedMany(BaseMatchCase):
    """
    ExactMatchTagged with many VLANS
    """

    def runTest(self):
        for vid in range(2,100,10):
            flow_match_test(self, pa_port_map, dl_vlan=vid, max_test=5)
        for vid in range(100,4000,389):
            flow_match_test(self, pa_port_map, dl_vlan=vid, max_test=5)
        flow_match_test(self, pa_port_map, dl_vlan=4094, max_test=5)


tc = ExactMatchTaggedMany()
_RESULT = tc.run()
