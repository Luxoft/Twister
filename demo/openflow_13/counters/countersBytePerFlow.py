"""
<title>BytePerFlow</title>
<description>Verify Byte counters per flow are
    incremented by no. of packets received for that flow
</description>
"""

try:
    if('TWISTER_ENV' in globals()):
        from ce_libs.openflow.of_13.openflow_base import *
        testbed=currentTB
        from ce_libs import ra_proxy
        ra_service=ra_proxy                        
except:
    raise

class BytePerFlow(SimpleDataPlane):

    """Verify Byte counters per flow are
    incremented by no. of packets received for that flow"""

    def runTest(self):

        self.logger.info("Running BytePerFlow test")

        of_ports = self.port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 1, "Not enough ports for test")

        #Clear switch State
        rc = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        self.logger.info("Insert any flow")
        self.logger.info("Sending N Packets matching the flow")
        self.logger.info("Verify byte counters increment in accordance")

        #Create a Match on Ingress flow
        (pkt,match) = testutils.wildcard_all_except_ingress(self,of_ports)

        #Send Packets matching the flow
        num_pkts = 5
        for pkt_cnt in range(num_pkts):
            self.dataplane.send(of_ports[0],str(pkt))

        #Verify Recieved Packets/Bytes Per Flow
        testutils.verify_flowstats(self,match,byte_count=500)

    
tc = BytePerFlow()
_RESULT = tc.run()
