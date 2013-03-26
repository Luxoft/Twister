"""
<title>AggregatedStats</title>
<description>Verify counters in aggregate stats reply
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

class AggregatedStats(SimpleDataPlane):

    """Verify counters in aggregate stats reply"""

    def runTest(self):

        self.logger.info("Running AggregatedStats test")

        of_ports = self.port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 1, "Not enough ports for test")

        #Clear switch State
        rc = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        #Create a Match on Ingress flow
        (pkt,match) = testutils.wildcard_all_except_ingress(self,of_ports)

        #Send Packets matching the flow
        num_pkts = 5
        for pkt_cnt in range(num_pkts):
            self.dataplane.send(of_ports[0],str(pkt))
        time.sleep(2)
        #Verify Recieved Packets/Bytes Per Flow

        response = testutils.ag_flow_stats_get(self,match)
        self.assertTrue(response is not None, "Switch did not reply")
        logMsg('logDebug',"Response from switch:")
        logMsg('logDebug',response.show())
        for item in response.stats:
            self.assertEqual(str(item.packet_count), "5", "Packet count should be 5")
            self.assertEqual(str(item.byte_count), "500", "Byte count should be 500")
            self.assertEqual(str(item.flow_count), "1", "Flow count should be 1")

    
tc = AggregatedStats()
_RESULT = tc.run()
