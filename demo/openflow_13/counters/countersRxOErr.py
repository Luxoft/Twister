"""
<title>RxOErr</title>
<description>Log the tx_o_err stats fiels, this test do not verify the value
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

class RxOErr(SimpleDataPlane):

    """Log the tx_o_err stats fiels, this test do not verify the value"""

    def runTest(self):

        self.logger.info("Running Rx_O_Err test")

        of_ports = self.port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 1, "Not enough ports for test")

        #Clear switch State
        rc = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        self.logger.info("Send Port_Stats Request")
        self.logger.info("Verify reply has rx_over_err count ")

        # Send Port_Stats request for the ingress port (retrieve current counter state)
        (counter) = testutils.get_portstats(self,of_ports[0])
        self.assertTrue(counter is not None, "Switch did not reply")
        rx_over_err = counter[9]
        self.logger.info("Recieve Overrun Errors  count is :" + str(rx_over_err))

    
tc = RxOErr()
_RESULT = tc.run()
