"""
<title>LookedUpTable</title>
<description>
    Get table stats and verify the lookup and and matched counters increment

    
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

class LookedUpTable(SimpleDataPlane):
    """
    Get table stats and verify the lookup and and matched counters increment

    """
    def runTest(self):
        self.logger.info("Running LookedUpTable")
        self.logger.info("Sending table stats request")

        of_ports = self.port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 1, "Not enough ports for test")

        #Clear switch State
        rc = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        self.logger.info("Insert any flow matching on in_port=ingress_port,action = output to egress_port")
        self.logger.info("Send N packets matching the flow, N' packets not matching the flow")
        self.logger.info("Send Table_Stats, verify lookup_count = N+N' & matched_count=N ")

        #Get Current Table Stats
        (current_lookedup,current_matched,current_active) = testutils.get_tablestats(self)

        #Create a Match on Ingress flow
        (pkt,match) = testutils.wildcard_all_except_ingress(self,of_ports)

        #send packet pkt N times (pkt matches the flow)
        num_sends = 5
        for pkt_cnt in range(num_sends):
            self.dataplane.send(of_ports[0],str(pkt))

        #send packet pkt N' (pkt does not match the flow)
        num_sends2 = 5
        pkt2 = testutils.simple_tcp_packet(ip_dst="10.0.0.254")
        for pkt_cnt in range(num_sends):
            self.dataplane.send(of_ports[1],str(pkt2))

        new_lookup = num_sends+num_sends2+current_lookedup
        new_matched = num_sends+current_matched

        #Verify lookup_count and matched_count counters.
        testutils.verify_tablestats(self,expect_lookup=new_lookup,expect_match=new_matched)

    
tc = LookedUpTable()
_RESULT = tc.run()
