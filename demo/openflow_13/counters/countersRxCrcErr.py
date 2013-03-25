"""
<title>RxCrcErr</title>
<description>Log the rx_crc_error stats fiels, this test do not verify the value
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

class RxCrcErr(SimpleDataPlane):

    """Log the rx_crc_error stats fiels, this test do not verify the value"""

    def runTest(self):

        self.logger.info("Running Port_Counter_9 test")

        of_ports = self.port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 1, "Not enough ports for test")

        #Clear switch State
        rc = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        self.logger.info("Send Port_Stats Request")
        self.logger.info("Verify reply has rx_crc_err count ")

        # Send Port_Stats request for the ingress port (retrieve current counter state)
        (counter) = testutils.get_portstats(self,of_ports[0])
        self.assertTrue(counter is not None, "Switch did not reply")
        rx_crc_err = counter[10]
        self.logger.info("Recieve CRC Errors  count is :" + str(rx_crc_err))

    
tc = RxCrcErr()
_RESULT = tc.run()
