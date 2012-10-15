
from ce_libs import *

try:
    pktact.pa_config=getOpenflowConfig(globEpName)
    pktact.pa_port_map= pktact.pa_config['port_map']
except:
    print "Error: Invalid configuration for EPNAME: " + str(globEpName)

class AllWildcardMatch(BaseMatchCase):
    """
    Create Wildcard-all flow and exercise for all ports

    Generate a packet
    Generate and install a matching flow with wildcard-all
    Add action to forward to a port
    Send the packet to the port
    Verify the packet is received at all other ports (one port at a time)
    Verify flow_expiration message is correct when command option is set
    """
    def runTest(self):
        flow_match_test(self, pa_port_map, wildcards=ofp.OFPFW_ALL)


tc = AllWildcardMatch()
_RESULT = tc.run()
