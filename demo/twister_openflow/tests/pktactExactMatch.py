
from ce_libs import *

try:
    pktact.pa_config=getOpenflowConfig(globEpName)
    pktact.pa_port_map= pktact.pa_config['port_map']
except:
    print "Error: Invalid configuration for EPNAME: " + str(globEpName)

class ExactMatch(BaseMatchCase):
    """
    Exercise exact matching for all port pairs

    Generate a packet
    Generate and install a matching flow without wildcard mask
    Add action to forward to a port
    Send the packet to the port
    Verify the packet is received at all other ports (one port at a time)
    """

    def runTest(self):
        flow_match_test(self, pa_port_map)


tc = ExactMatch()
_RESULT = tc.run()
