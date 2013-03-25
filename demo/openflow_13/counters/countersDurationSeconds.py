"""
<title>DurationSeconds</title>
<description>Verify that duration in secounds counter is available 
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

class DurationSeconds(SimpleDataPlane):

    """Verify that duration in secounds counter is available """

    def runTest(self):

        self.logger.info("Running duration in seconds test")

        of_ports = self.port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 1, "Not enough ports for test")

        #Clear switch State
        rc = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        self.logger.info("Send Queue_Stats Request")
        self.logger.info("Verify reply has duration in seconds count ")

        # Send Port_Stats request for the ingress port (retrieve current counter state)
        (counter) = testutils.get_portstats(self,of_ports[0])
        self.assertTrue(counter is not None, "Switch did not reply")
        dr_sec = counter[13]
        self.logger.info("Duration in seconds count is :" + str(dr_sec))

    
tc = DurationSeconds()
_RESULT = tc.run()
