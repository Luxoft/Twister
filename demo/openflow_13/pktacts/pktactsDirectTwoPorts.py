"""
<title>DirectTwoPorts</title>
<description>
    Send packet to two egress ports

    Generate a packet
    Generate and install a matching flow
    Add action to direct the packet to two egress ports
    Send the packet to ingress dataplane port
    Verify the packet is received at the two egress ports
    
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

class DirectTwoPorts(SimpleDataPlane):
    """
    Send packet to two egress ports

    Generate a packet
    Generate and install a matching flow
    Add action to direct the packet to two egress ports
    Send the packet to ingress dataplane port
    Verify the packet is received at the two egress ports
    """
    def runTest(self):
        self.logger.info("Running DirectTwoPorts test")
        of_ports = self.port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 1, "Not enough ports for test")

        self.logger.info("Clear the switch state")
        rc = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        pkt = testutils.simple_tcp_packet()
        match = parse.packet_to_flow_match(pkt)

        for idx in range(len(of_ports)):
            rc = testutils.delete_all_flows(self.controller, self.logger)
            self.assertEqual(rc, 0, "Failed to delete all flows")
            ingress_port = of_ports[idx]
            egress_port1 = of_ports[(idx + 1) % len(of_ports)]
            egress_port2 = of_ports[(idx + 2) % len(of_ports)]
            self.logger.info("Ingress " + str(ingress_port) + " to egress " + str(egress_port1) + " and " + str(egress_port2))
            request = message.flow_mod()
            request.match_fields = match
            act = action.action_output()
            act.port = egress_port1
            inst = instruction.instruction_apply_actions()
            inst.actions.add(act)
            act.port = egress_port2
            act.max_len = ofp.OFPCML_NO_BUFFER
            inst.actions.add(act)
            request.instructions.add(inst)
            request.buffer_id = 0xffffffff

            request.priority = 1000
            self.logger.info("Adding flow ")
            logMsg('logDebug',"Request send to switch:")
            logMsg('logDebug',request.show())
            rv = self.controller.message_send(request)
            self.assertTrue(rv != -1, "Failed to insert test flow")

            self.dataplane.send(ingress_port, str(pkt))
            #Verifying packets recieved on expected dataplane ports
            self.logger.info("Verify packets are received")
            yes_ports = set([egress_port1, egress_port2])
            testutils.receive_pkt_check(self.dataplane, pkt, yes_ports, [ingress_port], self, self.logger)

    
tc = DirectTwoPorts()
_RESULT = tc.run()
