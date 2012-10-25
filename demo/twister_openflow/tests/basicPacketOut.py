
from ce_libs import *

try:
    basic.basic_config = getOpenflowConfig(EP)
    basic.basic_port_map = basic.basic_config['port_map']
except:
    print 'Error: Invalid configuration for EPNAME: ' + str(EP)

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

        rc = delete_all_flows(self.controller, basic_logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        # These will get put into function
        outpkt = simple_tcp_packet()
        of_ports = basic_port_map.keys()
        of_ports.sort()
        for dp_port in of_ports:
            msg = message.packet_out()
            msg.data = str(outpkt)
            act = action.action_output()
            act.port = dp_port
            self.assertTrue(msg.actions.add(act), 'Could not add action to msg')

            basic_logger.info("PacketOut to: " + str(dp_port))
            rv = self.controller.message_send(msg)
            self.assertTrue(rv == 0, "Error sending out message")

            (of_port, pkt, pkt_time) = self.dataplane.poll(timeout=1)

            self.assertTrue(pkt is not None, 'Packet not received')
            basic_logger.info("PacketOut: got pkt from " + str(of_port))
            if of_port is not None:
                self.assertEqual(of_port, dp_port, "Unexpected receive port")
            self.assertEqual(str(outpkt), str(pkt),
                             'Response packet does not match send packet')


tc = PacketOut()
_RESULT = tc.run()
