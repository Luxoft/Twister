"""
<title>DurationPerFlow</title>
<description>Verify duration in seconds counters per flow are
    incremented
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

class DurationPerFlow(SimpleDataPlane):

    """Verify duration in seconds counters per flow are
    incremented"""

    def runTest(self):

        self.logger.info("Running DurationPerFlow test")

        of_ports = self.port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 1, "Not enough ports for test")

        #Clear switch State
        rc = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        self.logger.info("Insert any flow")
        self.logger.info("Sending N Packets matching the flow")
        self.logger.info("After sleep verify duration counters increment in accordance")

        #Create a Match on Ingress flow
        (pkt,match) = testutils.wildcard_all_except_ingress(self,of_ports)

        #Send Packets matching the flow
        num_pkts = 5
        for pkt_cnt in range(num_pkts):
            self.dataplane.send(of_ports[0],str(pkt))
        time.sleep(2)
        #Verify Recieved Packets/Bytes Per Flow
        response = testutils.flow_stats_get(self,match)
        self.assertTrue(response is not None, "Switch did not reply")
        logMsg('logDebug',"Response from switch:")
        logMsg('logDebug',response.show())
        for item in response.stats:
            self.assertTrue(str(item.duration_sec) != 0, "Duration should more than 0 second")

    
tc = DurationPerFlow()
_RESULT = tc.run()
