"""
<title>DirectPacketICMP</title>
<description>
    Send ICMP packet to single egress port

    Generate a ICMP packet
    Generate and install a matching flow
    Add action to direct the packet to an egress port
    Send the packet to ingress dataplane port
    Verify the packet is received at the egress port only
    Difference from DirectPacket test is that sent packet is ICMP
    
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

class DirectPacketICMP(SimpleDataPlane):
    """
    Send ICMP packet to single egress port

    Generate a ICMP packet
    Generate and install a matching flow
    Add action to direct the packet to an egress port
    Send the packet to ingress dataplane port
    Verify the packet is received at the egress port only
    Difference from DirectPacket test is that sent packet is ICMP
    """
    def runTest(self):

        self.logger.info("Running DirectPacketICMP test")
        of_ports = self.port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 0, "Not enough ports for test")

        pkt = testutils.simple_icmp_packet()
        pktmatch = parse.packet_to_flow_match(pkt)
        self.assertTrue(match is not None, "Could not generate flow match from pkt")
        act = action.action_output()

        for idx in range(len(of_ports)):
            self.logger.info("Clear the switch state")
            rc = testutils.delete_all_flows(self.controller, self.logger)
            self.assertEqual(rc, 0, "Failed to delete all flows")

            ingress_port = of_ports[idx]
            egress_port = of_ports[(idx + 1) % len(of_ports)]
            self.logger.info("Ingress " + str(ingress_port) +
                             " to egress " + str(egress_port))

            request = message.flow_mod()
            request.match_fields = pktmatch
            act.port = egress_port
            inst = instruction.instruction_apply_actions()
            inst.actions.add(act)
            request.instructions.add(inst)

            self.logger.info("Inserting flow")
            rv = self.controller.message_send(request)
            self.assertTrue(rv != -1, "Error installing flow mod")
            testutils.do_barrier(self.controller)

            self.logger.info("Sending packet to dp port " + str(ingress_port))
            self.dataplane.send(ingress_port, str(pkt))

            (rcv_port, rcv_pkt, _ ) = self.dataplane.poll(timeout=2)

            self.assertTrue(rcv_pkt is not None, "Did not receive packet")
            self.assertEqual(rcv_port, egress_port, "Unexpected receive port")
            self.assertEqual(str(pkt), str(rcv_pkt),
                             'Response packet does not match send packet')

    
tc = DirectPacketICMP()
_RESULT = tc.run()
