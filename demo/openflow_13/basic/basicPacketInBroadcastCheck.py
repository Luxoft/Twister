"""
<title>PacketInBroadcastCheck</title>
<description>
    Check if bcast pkts leak when no flows are present
    Clear the flow table
    Send in a broadcast pkt
    Look for the packet on other dataplane ports.
    
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

class PacketInBroadcastCheck(SimpleDataPlane):
    """
    Check if bcast pkts leak when no flows are present
    Clear the flow table
    Send in a broadcast pkt
    Look for the packet on other dataplane ports.
    """

    def runTest(self):
        self.logger.info("Running broadcast leak test")
        # Need at least two ports
        self.assertTrue(len(self.port_map.items()) > 1, "Too few ports for test")

        self.logger.info("Clear the switch state -- delete all flows")
        rc = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        of_ports = self.port_map.keys()
        d_port = of_ports[0]
        egr_port= of_ports[1]
        pkt = testutils.simple_tcp_packet(dl_dst='ff:ff:ff:ff:ff:ff')

        self.logger.info("BCast Leak Test, send to port %s" % d_port)
        self.dataplane.send(d_port, str(pkt))

        r_pkt = testutils.receive_pkt_verify(self, egr_port, None)
        self.assertTrue(r_pkt is None,
                        'BCast packet received on port ')

    
tc = PacketInBroadcastCheck()
_RESULT = tc.run()
