"""
<title>NoAction</title>
<description>
Clear switch, send packet and verify it is droped
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

class NoAction(SimpleDataPlane):
    """
    Clear switch, send packet and verify it is droped
    """
    def runTest(self):
        self.logger.info("Running NoAction test")
        of_ports = self.port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 0, "Not enough ports for test")

        pkt = testutils.simple_tcp_packet()

        self.logger.info("Clear the switch state")
        rv = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rv, 0, "Failed to delete all flows")

        for ingress_port in of_ports:
            self.logger.info("Sending packet to dp port " + str(ingress_port))
            self.dataplane.send(ingress_port, str(pkt))
            testutils.receive_pkt_check(self.dataplane, pkt, [], of_ports,
                              self,self.logger)

    
tc = NoAction()
_RESULT = tc.run()
