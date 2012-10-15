
from ce_libs import *

try:
    pktact.pa_config=getOpenflowConfig(globEpName)
    pktact.pa_port_map= pktact.pa_config['port_map']
except:
    print "Error: Invalid configuration for EPNAME: " + str(globEpName)

class FloodPlusIngress(basic.SimpleDataPlane):
    """
    Flood to all ports plus send to ingress port

    Generate a packet
    Generate and install a matching flow
    Add action to flood the packet
    Add action to send to ingress port
    Send the packet to ingress dataplane port
    Verify the packet is received at all other ports
    """
    def runTest(self):
        of_ports = pa_port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 1, "Not enough ports for test")

        pkt = simple_tcp_packet()
        match = parse.packet_to_flow_match(pkt)
        match.wildcards &= ~ofp.OFPFW_IN_PORT
        self.assertTrue(match is not None,
                        "Could not generate flow match from pkt")
        act = action.action_output()

        for ingress_port in of_ports:
            rv = delete_all_flows(self.controller, pa_logger)
            self.assertEqual(rv, 0, "Failed to delete all flows")

            pa_logger.info("Ingress " + str(ingress_port) + " to all ports")
            match.in_port = ingress_port

            request = message.flow_mod()
            request.match = match
            request.buffer_id = 0xffffffff
            act.port = ofp.OFPP_FLOOD
            self.assertTrue(request.actions.add(act),
                            "Could not add flood port action")
            act.port = ofp.OFPP_IN_PORT
            self.assertTrue(request.actions.add(act),
                            "Could not add ingress port for output")
            pa_logger.info(request.show())

            pa_logger.info("Inserting flow")
            rv = self.controller.message_send(request)
            self.assertTrue(rv != -1, "Error installing flow mod")
            do_barrier(self.controller)

            pa_logger.info("Sending packet to dp port " + str(ingress_port))
            self.dataplane.send(ingress_port, str(pkt))
            receive_pkt_check(self.dataplane, pkt, of_ports, [], self,
                              pa_logger)


tc = FloodPlusIngress()
_RESULT = tc.run()
