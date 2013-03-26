"""
<title>PacketInLoad</title>
<description>
    Generate lots of packet-in messages

    Test packet-in function by sending lots of packets to the dataplane.
    This test tracks the number of pkt-ins received but does not enforce
    any requirements about the number received.
    
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

class PacketInLoad(SimpleDataPlane):
    """
    Generate lots of packet-in messages

    Test packet-in function by sending lots of packets to the dataplane.
    This test tracks the number of pkt-ins received but does not enforce
    any requirements about the number received.
    """
    def runTest(self):
        # Construct packet to send to dataplane
        # Send packet to dataplane, once to each port
        # Poll controller with expect message type packet in
        self.logger.info("Running PacketInLoad test")
        self.logger.info("Generate lots of packet-in messages")
        self.logger.info("This test tracks the number of packets received, but does not enforce any requirements about the number received")

        of_ports = self.port_map.keys()
        of_ports.sort()
        # Delete all flows
        self.assertTrue(len(of_ports) > 1, "Not enough ports for test")
        self.logger.info("Clear the switch state, delete all flows")
        rc = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")
        out_count = 0
        in_count = 0

        for of_port in of_ports:
            for pkt, pt in [
               (testutils.simple_tcp_packet(), "simple TCP packet"),
               (testutils.simple_tcp_packet(payload_len=108),"simple tagged TCP packet"),
               (testutils.simple_eth_packet(), "simple Ethernet packet"),
               (testutils.simple_eth_packet(pktlen=40), "tiny Ethernet packet")]:
               self.logger.info("PKT IN test with %s, port %s" % (pt, of_port))
               for count in range(100):
                   out_count += 1
                   self.dataplane.send(of_port, str(pkt))
        time.sleep(2)
        while True:
            (response, raw) = self.controller.poll(ofp.OFPT_PACKET_IN,
                                                   timeout=0)
            if not response:
                break
            in_count += 1
        self.logger.info("PacketInLoad Sent %d. Got %d." % (out_count, in_count))

    
tc = PacketInLoad()
_RESULT = tc.run()
