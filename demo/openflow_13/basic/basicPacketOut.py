"""
<title>PacketOut</title>
<description>
    Test packet out function
    Send packet out message to controller for each dataplane port and
    verify the packet appears on the appropriate dataplane port
    
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

class PacketOut(SimpleDataPlane):
    """
    Test packet out function
    Send packet out message to controller for each dataplane port and
    verify the packet appears on the appropriate dataplane port
    """
    def runTest(self):
        # Construct packet to send to dataplane
        # Send packet to dataplane
        # Poll controller with expect message type packet in

        self.logger.info("Running PacketOut test")
        self.logger.info("Clear the switch state -- delete all flows")
        rc = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        # These will get put into function
        outpkt = testutils.simple_tcp_packet()
        of_ports = self.port_map.keys()
        of_ports.sort()
        for dp_port in of_ports:
            msg = message.packet_out()
            msg.in_port = ofp.OFPP_CONTROLLER
            msg.data = str(outpkt)
            act = action.action_output()
            act.port = dp_port
            self.assertTrue(msg.actions.add(act), 'Could not add action to msg')
            self.logger.info("PacketOut to: " + str(dp_port))
            logMsg('logDebug',"Packet out:")
            logMsg('logDebug',msg.show())
            rv = self.controller.message_send(msg)
            self.assertTrue(rv == 0, "Error sending out message")

            (of_port, pkt, _) = self.dataplane.poll(timeout=1)
            self.assertTrue(pkt is not None, "Packet not received on port " + str(of_port) )
            self.logger.info("PacketOut: got pkt from " + str(of_port))
            if of_port is not None:
                self.assertEqual(of_port, dp_port, "Unexpected receive port")
            self.assertEqual(str(outpkt), str(pkt)[:len(str(outpkt))],
                             'Response packet does not match send packet')

    
tc = PacketOut()
_RESULT = tc.run()
