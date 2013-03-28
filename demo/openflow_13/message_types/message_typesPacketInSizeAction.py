"""
<title>PacketInSizeAction</title>
<description>When the packet is sent because of a "send to controller" action,
        verify the data sent in packet_in varies in accordance with the
        max_len field set in action_output
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

class PacketInSizeAction(SimpleDataPlane):

    """When the packet is sent because of a "send to controller" action,
        verify the data sent in packet_in varies in accordance with the
        max_len field set in action_output"""


    def runTest(self):

        self.logger.info("Running PacketInSizeAction Test")
        of_ports = self.port_map.keys()
        of_ports.sort()

        #Clear switch state
        rc = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        #Create a simple tcp packet
        pkt = testutils.simple_tcp_packet()
        match = parse.packet_to_flow_match(pkt)
        self.assertTrue(match is not None, "Could not generate flow match from pkt")
        match.in_port = of_ports[0]


        max_len = [0 ,32 ,64,100]

        for bytes in max_len :

            #Insert a flow entry with action --output to controller
            request = message.flow_mod()
            request.match_fields = match

            act = action.action_output()
            act.port = ofp.OFPP_CONTROLLER
            act.max_len = bytes
            inst = instruction.instruction_apply_actions()
            inst.actions.add(act)
            request.instructions.add(inst)

            self.logger.debug("Adding flow ")

            rv = self.controller.message_send(request)
            self.assertTrue(rv != -1, "Failed to insert test flow")

            #Send packet matching the flow
            logMsg('logDebug',"Sending packet to dp port " + str(of_ports[0]))
            self.dataplane.send(of_ports[0], str(pkt))

            #Verifying packet_in recieved on the control plane
            (response, raw) = self.controller.poll(ofp.OFPT_PACKET_IN, timeout=10)
            self.assertTrue(response is not None,
                        'Packet in message not received by controller')

            #Verify the reason field is OFPR_ACTION
            self.assertEqual(response.reason,ofp.OFPR_ACTION,"PacketIn reason field is incorrect")
            #Verify buffer_id field and data field
            if response.buffer_id != 0xFFFFFFFF :
                self.assertTrue(len(response)>=bytes,"Packet_in size is greater than max_len field")
            else:
                self.assertTrue(len(response)==bytes,"Buffer None here but packet_in is not a complete packet")

    
tc = PacketInSizeAction()
_RESULT = tc.run()
