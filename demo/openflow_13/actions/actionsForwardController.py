"""
<title>ForwardController</title>
<description>ForwardController : Packet is sent to controller
    output.port = OFPP_CONTROLLER
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

class ForwardController(SimpleDataPlane):

    """ForwardController : Packet is sent to controller
    output.port = OFPP_CONTROLLER"""

    def runTest(self):

        self.logger.info("Running Forward_Controller test")

        of_ports = self.port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 1, "Not enough ports for test")

        #Clear switch state
        rc = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        self.logger.info("Insert a flow with output action port OFPP_CONTROLLER")
        self.logger.info("Send packet matching the flow")
        self.logger.info("Expecting packet on the control plane")

        #Create packet
        pkt = testutils.simple_tcp_packet()
        match = parse.packet_to_flow_match(pkt)

        self.logger.info("Generate flow_mod message")
        #Create a flow mod message
        request = message.flow_mod()
        request.match_fields = match
        act = action.action_output()
        act.port = ofp.OFPP_CONTROLLER
        act.max_len = ofp.OFPCML_NO_BUFFER
        inst = instruction.instruction_apply_actions()
        inst.actions.add(act)
        request.instructions.add(inst)

        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',request.show())

        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, "Failed to insert test flow")

        for ingress_port in of_ports:
            #Send packet matching the flow
            self.logger.info("Sending packet to dp port " + str(ingress_port))
            self.dataplane.send(ingress_port, str(pkt))
            testutils.do_barrier(self.controller)
            #Verifying packet recieved on the control plane port
            (response, raw) = self.controller.poll(ofp.OFPT_PACKET_IN, timeout=10)
            self.assertTrue(response is not None,
                        'Packet in message not received by controller')

    
tc = ForwardController()
_RESULT = tc.run()
