"""
<title>IdenticalFlows</title>
<description>Verify that adding two identical flows overwrites the existing one and clears counters
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

class IdenticalFlows(SimpleDataPlane):

    """Verify that adding two identical flows overwrites the existing one and clears counters"""

    def runTest(self):

        self.logger.info("Running Identical_Flows test ")

        of_ports = self.port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 0, "Not enough ports for test")

        self.logger.info("Clear the switch state, delete all flows")
        rc = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        self.logger.info("Inserting two identical flows one by one")
        self.logger.info("Expecting switch to overwrite the first flow and clear the counters associated with it ")

        # Create and add flow-1, check on dataplane it is active.
        (pkt,match) = testutils.wildcard_all_except_ingress(self,of_ports)

        # Verify active_entries in table_stats_request =1
        testutils.verify_tablestats(self,expect_active=1)

        # Send Packet (to increment counters like byte_count and packet_count)
        #send_packet(self,pkt,of_ports[0],of_ports[1])
        num_sends = 5
        for pkt_cnt in range(num_sends):
            self.dataplane.send(of_ports[0],str(pkt))


        # Verify Flow counters have incremented
        testutils.verify_flowstats(self,match,byte_count=500,packet_count=5)

        #Send Identical flow
        (pkt1,match1) = testutils.wildcard_all_except_ingress(self,of_ports)
        # Verify active_entries in table_stats_request =1
        testutils.verify_tablestats(self,expect_active=1)

        # Verify Flow counters reset
        testutils.verify_flowstats(self,match,byte_count=0,packet_count=0)

    
tc = IdenticalFlows()
_RESULT = tc.run()
