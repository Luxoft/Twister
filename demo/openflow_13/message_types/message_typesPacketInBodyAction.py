"""
<title>PacketInBodyAction</title>
<description>Verify the packet_in message body, when packet_in is generated due to action output to controller
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

class PacketInBodyAction(SimpleDataPlane):

    """Verify the packet_in message body, when packet_in is generated due to action output to controller"""

    def runTest(self):

        self.logger.info("Running PacketInBodyAction Test")
        of_ports = self.port_map.keys()
        of_ports.sort()

        #Clear switch state
        rc = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        # Create a simple tcp packet
        pkt = testutils.simple_tcp_packet()
        match = parse.packet_to_flow_match(pkt)
        self.assertTrue(match is not None, "Could not generate flow match from pkt")

        #Insert a flow entry with action output to controller
        request = message.flow_mod()
        request.match_fields = match

        act = action.action_output()
        act.port = ofp.OFPP_CONTROLLER
        act.max_len = ofp.OFPCML_NO_BUFFER
        inst = instruction.instruction_apply_actions()
        inst.actions.add(act)
        request.instructions.add(inst)

        self.logger.info("Inserting flow....")
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, "Error installing flow mod")

        #Send packet matching the flow
        logMsg('logDebug',"Sending packet to dp port " + str(of_ports[0]))
        self.dataplane.send(of_ports[0], str(pkt))

        #Verifying packet_in recieved on the control plane
        (response, raw) = self.controller.poll(ofp.OFPT_PACKET_IN, timeout=10)
        self.assertTrue(response is not None,
                    'Packet in message not received by controller')

        #Verify the reason field is OFPR_ACTION
        self.assertEqual(response.reason,ofp.OFPR_ACTION,"PacketIn reason field is incorrect")

        #Verify Frame Total Length Field in Packet_in
        self.assertEqual(response.total_len,len(str(pkt)), "PacketIn total_len field is incorrect")

    
tc = PacketInBodyAction()
_RESULT = tc.run()
