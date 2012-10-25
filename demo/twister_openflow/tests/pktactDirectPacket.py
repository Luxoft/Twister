
from ce_libs import *

try:
    pktact.pa_config = getOpenflowConfig(globEpName)
    pktact.pa_port_map = pktact.pa_config['port_map']
except:
    print 'Error: Invalid configuration for EPNAME: ' + str(globEpName)

class DirectPacket(basic.SimpleDataPlane):
    """
    Send packet to single egress port

    Generate a packet
    Generate and install a matching flow
    Add action to direct the packet to an egress port
    Send the packet to ingress dataplane port
    Verify the packet is received at the egress port only
    """
    def runTest(self):
        self.handleFlow()

    def handleFlow(self, pkttype='TCP'):
        of_ports = pa_port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 1, "Not enough ports for test")

        if (pkttype == 'ICMP'):
            pkt = simple_icmp_packet()
        else:
            pkt = simple_tcp_packet()
        match = parse.packet_to_flow_match(pkt)
        match.wildcards &= ~ofp.OFPFW_IN_PORT
        self.assertTrue(match is not None,
                        "Could not generate flow match from pkt")
        act = action.action_output()

        for idx in range(len(of_ports)):
            rv = delete_all_flows(self.controller, pa_logger)
            self.assertEqual(rv, 0, "Failed to delete all flows")

            ingress_port = of_ports[idx]
            egress_port = of_ports[(idx + 1) % len(of_ports)]
            pa_logger.info("Ingress " + str(ingress_port) +
                             " to egress " + str(egress_port))

            match.in_port = ingress_port

            request = message.flow_mod()
            request.match = match
            request.buffer_id = 0xffffffff
            act.port = egress_port
            self.assertTrue(request.actions.add(act), "Could not add action")

            pa_logger.info("Inserting flow")
            rv = self.controller.message_send(request)
            self.assertTrue(rv != -1, "Error installing flow mod")
            do_barrier(self.controller)

            pa_logger.info("Sending packet to dp port " +
                           str(ingress_port))
            self.dataplane.send(ingress_port, str(pkt))
            (rcv_port, rcv_pkt, pkt_time) = self.dataplane.poll(timeout=1)
            self.assertTrue(rcv_pkt is not None, "Did not receive packet")
            pa_logger.debug("Packet len " + str(len(rcv_pkt)) + " in on " +
                         str(rcv_port))
            self.assertEqual(rcv_port, egress_port, "Unexpected receive port")
            self.assertEqual(str(pkt), str(rcv_pkt),
                             'Response packet does not match send packet')


tc = DirectPacket()
_RESULT = tc.run()
