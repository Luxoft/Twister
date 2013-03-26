"""
<title>PacketOutLoad</title>
<description>
    Generate lots of packet-out messages

    Test packet-out function by sending lots of packet-out msgs
    to the switch.  This test tracks the number of packets received in
    the dataplane, but does not enforce any requirements about the
    number received.
    
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

class PacketOutLoad(SimpleDataPlane):
    """
    Generate lots of packet-out messages

    Test packet-out function by sending lots of packet-out msgs
    to the switch.  This test tracks the number of packets received in
    the dataplane, but does not enforce any requirements about the
    number received.
    """
    def runTest(self):
        self.logger.info("Running PacketOutLoad test")
        self.logger.info("Generate lots of packet-out messages")
        self.logger.info("This test tracks the number of packets received in the dataplane, but does not enforce any requirements about the number received")
        of_ports = self.port_map.keys()
        of_ports.sort()
        # Delete all flows
        self.assertTrue(len(of_ports) > 1, "Not enough ports for test")
        self.logger.info("Clear the switch state, delete all flows")
        rc = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        out_count = 0
        in_count = 0
        xid = 100
        for dp_port in of_ports:
            for outpkt, opt in [
               (testutils.simple_tcp_packet(), "simple TCP packet"),
               (testutils.simple_eth_packet(), "simple Ethernet packet"),
               (testutils.simple_eth_packet(pktlen=40), "tiny Ethernet packet")]:

               self.logger.info("PKT OUT test with %s, port %s" % (opt, dp_port))
               msg = message.packet_out()
               msg.data = str(outpkt)
               act = action.action_output()
               act.port = dp_port
               self.assertTrue(msg.actions.add(act), 'Could not add action to msg')

               self.logger.info("PacketOutLoad to: " + str(dp_port))
               for count in range(100):
                   msg.xid = xid
                   xid += 1
                   rv = self.controller.message_send(msg)
                   self.assertTrue(rv == 0, "Error sending out message")
                   out_count += 1

               exp_pkt_arg = None
               exp_port = None
        time.sleep(2)
        while True:
            (of_port, pkt, pkt_time) = self.dataplane.poll(timeout=0)
            if pkt is None:
                break
            in_count += 1
        self.logger.info("PacketOutLoad Sent %d. Got %d." % (out_count, in_count))

    
tc = PacketOutLoad()
_RESULT = tc.run()
