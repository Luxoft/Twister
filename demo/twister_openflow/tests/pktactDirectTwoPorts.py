
from ce_libs import *

try:
    pktact.pa_config=getOpenflowConfig(globEpName)
    pktact.pa_port_map= pktact.pa_config['port_map']
except:
    print "Error: Invalid configuration for EPNAME: " + str(globEpName)

class DirectTwoPorts(basic.SimpleDataPlane):
    """
    Send packet to two egress ports

    Generate a packet
    Generate and install a matching flow
    Add action to direct the packet to two egress ports
    Send the packet to ingress dataplane port
    Verify the packet is received at the two egress ports
    """
    def runTest(self):
        of_ports = pa_port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 2, "Not enough ports for test")

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
            egress_port1 = of_ports[(idx + 1) % len(of_ports)]
            egress_port2 = of_ports[(idx + 2) % len(of_ports)]
            pa_logger.info("Ingress " + str(ingress_port) +
                           " to egress " + str(egress_port1) + " and " +
                           str(egress_port2))

            match.in_port = ingress_port

            request = message.flow_mod()
            request.match = match
            request.buffer_id = 0xffffffff
            act.port = egress_port1
            self.assertTrue(request.actions.add(act), "Could not add action1")
            act.port = egress_port2
            self.assertTrue(request.actions.add(act), "Could not add action2")
            # pa_logger.info(request.show())

            pa_logger.info("Inserting flow")
            rv = self.controller.message_send(request)
            self.assertTrue(rv != -1, "Error installing flow mod")
            do_barrier(self.controller)

            pa_logger.info("Sending packet to dp port " +
                           str(ingress_port))
            self.dataplane.send(ingress_port, str(pkt))
            yes_ports = set([egress_port1, egress_port2])
            no_ports = set(of_ports).difference(yes_ports)

            receive_pkt_check(self.dataplane, pkt, yes_ports, no_ports,
                              self, pa_logger)


tc = DirectTwoPorts()
_RESULT = tc.run()
