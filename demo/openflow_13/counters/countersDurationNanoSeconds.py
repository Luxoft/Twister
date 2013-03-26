"""
<title>DurationNanoSeconds</title>
<description>Verify that duration in nano secounds counter is available 
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

class DurationNanoSeconds(SimpleDataPlane):

    """Verify that duration in nano secounds counter is available """

    def runTest(self):

        self.logger.info("Running duration in nano seconds test")

        of_ports = self.port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 1, "Not enough ports for test")

        #Clear switch State
        rc = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        self.logger.info("Send Queue_Stats Request")
        self.logger.info("Verify reply has duration in nano seconds count ")

        # Send Port_Stats request for the ingress port (retrieve current counter state)
        (counter) = testutils.get_portstats(self,of_ports[0])
        self.assertTrue(counter is not None, "Switch did not reply")
        dr_nsec = counter[14]
        self.logger.info("Duration in nano seconds count is :" + str(dr_nsec))

    
tc = DurationNanoSeconds()
_RESULT = tc.run()
