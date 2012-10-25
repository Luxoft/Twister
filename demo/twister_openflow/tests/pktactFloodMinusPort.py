
from ce_libs import *

try:
    pktact.pa_config = getOpenflowConfig(globEpName)
    pktact.pa_port_map = pktact.pa_config['port_map']
except:
    print 'Error: Invalid configuration for EPNAME: ' + str(globEpName)

class FloodMinusPort(basic.SimpleDataPlane):
    """
    Config port with No_Flood and test Flood action

    Generate a packet
    Generate a matching flow
    Add action to forward to OFPP_ALL
    Set port to no-flood
    Send the packet to ingress dataplane port
    Verify the packet is received at all other ports except
    the ingress port and the no_flood port
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
            no_flood_idx = (idx + 1) % len(of_ports)
            no_flood_port = of_ports[no_flood_idx]
            rv = port_config_set(self.controller, no_flood_port,
                                 ofp.OFPPC_NO_FLOOD, ofp.OFPPC_NO_FLOOD,
                                 pa_logger)
            self.assertEqual(rv, 0, "Failed to set port config to no-flood")

            match.in_port = ingress_port

            request = message.flow_mod()
            request.match = match
            request.buffer_id = 0xffffffff
            act.port = ofp.OFPP_FLOOD
            self.assertTrue(request.actions.add(act),
                            "Could not add flood port action")
            pa_logger.info(request.show())

            pa_logger.info("Inserting flow")
            rv = self.controller.message_send(request)
            self.assertTrue(rv != -1, "Error installing flow mod")
            do_barrier(self.controller)

            pa_logger.info("Sending packet to dp port " + str(ingress_port))
            pa_logger.info("No flood port is " + str(no_flood_port))
            self.dataplane.send(ingress_port, str(pkt))
            no_ports = set([ingress_port, no_flood_port])
            yes_ports = set(of_ports).difference(no_ports)
            receive_pkt_check(self.dataplane, pkt, yes_ports, no_ports, self,
                              pa_logger)

            # Turn no flood off again
            rv = port_config_set(self.controller, no_flood_port,
                                 0, ofp.OFPPC_NO_FLOOD, pa_logger)
            self.assertEqual(rv, 0, "Failed to reset port config")


tc = FloodMinusPort()
_RESULT = tc.run()
