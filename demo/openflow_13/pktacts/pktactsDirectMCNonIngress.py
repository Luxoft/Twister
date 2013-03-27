"""
<title>DirectMCNonIngress</title>
<description>
    Multicast to all non-ingress ports

    Generate a packet
    Generate and install a matching flow
    Add action to direct the packet to all non-ingress ports
    Send the packet to ingress dataplane port
    Verify the packet is received at all non-ingress ports

    Does not use the flood action
    
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

class DirectMCNonIngress(SimpleDataPlane):
    """
    Multicast to all non-ingress ports

    Generate a packet
    Generate and install a matching flow
    Add action to direct the packet to all non-ingress ports
    Send the packet to ingress dataplane port
    Verify the packet is received at all non-ingress ports

    Does not use the flood action
    """
    def runTest(self):
        self.logger.info("Running DirectMCNonIngress")
        of_ports = self.port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 1, "Not enough ports for test")

        self.logger.info("Clear the switch state")
        rc = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        pkt = testutils.simple_tcp_packet()
        match = parse.packet_to_flow_match(pkt)
        act = action.action_output()

        for ingress_port in of_ports:
            self.logger.info("Clear the switch state")
            rc = testutils.delete_all_flows(self.controller, self.logger)
            self.assertEqual(rc, 0, "Failed to delete all flows")

            self.logger.info("Ingress " + str(ingress_port) + " all non-ingress ports")
            inst = instruction.instruction_apply_actions()
            request = message.flow_mod()
            request.match_fields = match
            request.buffer_id = 0xffffffff
            for egress_port in of_ports:
                if egress_port == ingress_port:
                    continue
                act.port = egress_port
                inst.actions.add(act)
                request.instructions.add(inst)

            logMsg('logDebug',"Request send to switch:")
            logMsg('logDebug',request.show())

            self.logger.info("Inserting flow")
            rv = self.controller.message_send(request)
            self.assertTrue(rv != -1, "Error installing flow mod")

            self.logger.info("Sending packet to dp port " + str(ingress_port))
            self.dataplane.send(ingress_port, str(pkt))
            yes_ports = set(of_ports).difference([ingress_port])
            testutils.receive_pkt_check(self.dataplane, pkt, yes_ports, [], self, self.logger)

    
tc = DirectMCNonIngress()
_RESULT = tc.run()
