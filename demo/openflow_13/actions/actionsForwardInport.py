"""
<title>ForwardInport</title>
<description> ForwardInPort : Packet sent to virtual port IN_PORT
    If the output.port = OFPP.INPORT then the packet is sent to the input port itself
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

class ForwardInport(SimpleDataPlane):

    """ ForwardInPort : Packet sent to virtual port IN_PORT
    If the output.port = OFPP.INPORT then the packet is sent to the input port itself"""

    def runTest(self):

        self.logger.info("Running Forward_Inport test")
        of_ports = self.port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 1, "Not enough ports for test")

        #Clear switch state
        rc = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        self.logger.info("Insert a flow with output action port OFPP_INPORT")
        self.logger.info("Send packet matching the flow")
        self.logger.info("Expecting packet on the input port")

        #Create a packet
        pkt = testutils.simple_tcp_packet()
        match = parse.packet_to_flow_match(pkt)

        ingress_port=of_ports[0]
        # Create a flow mod message
        self.logger.info("Generate flow_mod message")
        request = message.flow_mod()
        request.match_fields = match
        act = action.action_output()
        act.port = ofp.OFPP_IN_PORT
        act.max_len = ofp.OFPCML_NO_BUFFER
        inst = instruction.instruction_apply_actions()
        inst.actions.add(act)
        request.instructions.add(inst)

        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',request.show())

        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, "Failed to insert test flow")

        #Send packet matching the flow
        self.logger.info("Sending packet to dp port " + str(ingress_port))
        self.dataplane.send(ingress_port, str(pkt))
        yes_ports = [ingress_port]
        #Verfying packet recieved on expected dataplane ports
        testutils.receive_pkt_check(self.dataplane, pkt, yes_ports,set(of_ports).difference([ingress_port]),
                          self, self.logger)

    
tc = ForwardInport()
_RESULT = tc.run()
