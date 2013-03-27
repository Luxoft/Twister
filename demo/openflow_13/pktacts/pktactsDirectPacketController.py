"""
<title>DirectPacketController</title>
<description>
    Send packet to the controller port

    Generate a packet
    Generate and install a matching flow
    Add action to direct the packet to the controller port
    Send the packet to ingress dataplane port
    Verify the packet is received at the controller port
    
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

class DirectPacketController(SimpleDataPlane):
    """
    Send packet to the controller port

    Generate a packet
    Generate and install a matching flow
    Add action to direct the packet to the controller port
    Send the packet to ingress dataplane port
    Verify the packet is received at the controller port
    """
    def runTest(self):
        self.handleFlow()

    def handleFlow(self, pkttype='TCP'):

        self.logger.info("Running DirectPacketController test")
        of_ports = self.port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 0, "Not enough ports for test")

        self.logger.info("Clear the switch state")
        rc = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        pkt = testutils.simple_tcp_packet()
        match = parse.packet_to_flow_match(pkt)

        ingress_port=of_ports[0]

        request = message.flow_mod()
        request.match_fields = match
        act = action.action_output()
        act.port = ofp.OFPP_CONTROLLER
        act.max_len = ofp.OFPCML_NO_BUFFER
        inst = instruction.instruction_apply_actions()
        inst.actions.add(act)
        request.instructions.add(inst)
        request.buffer_id = 0xffffffff
        request.priority = 1000
        self.logger.info("Adding flow ")
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',request.show())
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, "Failed to insert test flow")

        testutils.do_barrier(self.controller)

        self.logger.info("Sending packet to dp port " + str(ingress_port))
        self.dataplane.send(ingress_port, str(pkt))

        response,_ = self.controller.poll(ofp.OFPT_PACKET_IN, 2)
        self.assertTrue(response is not None, 'Packet in message not received by controller')

    
tc = DirectPacketController()
_RESULT = tc.run()
