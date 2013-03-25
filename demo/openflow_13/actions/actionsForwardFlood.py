"""
<title>ForwardFlood</title>
<description>Forward:Flood : Packet is sent to all dataplane ports
    except ingress port when output action.port = OFPP_FLOOD 
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

class ForwardFlood(SimpleDataPlane):

    """Forward:Flood : Packet is sent to all dataplane ports
    except ingress port when output action.port = OFPP_FLOOD """

    def runTest(self):

        self.logger.info("Running Forward_Flood test")
        of_ports = self.port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 1, "Not enough ports for test")

        #Clear switch state
        rc = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        self.logger.info("Insert a flow with output action port OFPP_FORWARD")
        self.logger.info("Send packet matching the flow")
        self.logger.info("Expecting packet on all the ports except the input port")

        #Create a packet
        pkt = testutils.simple_tcp_packet()
        match = parse.packet_to_flow_match(pkt)

        self.logger.info("Generate flow_mod message")
        ingress_port=of_ports[0]
        request = message.flow_mod()
        request.match_fields = match
        act = action.action_output()
        act.port = ofp.OFPP_FLOOD
        act.max_len = ofp.OFPCML_NO_BUFFER
        inst = instruction.instruction_apply_actions()
        inst.actions.add(act)
        request.instructions.add(inst)

        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',request.show())

        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, "Failed to insert test flow")

        #Send Packet matching the flow
        self.logger.info("Sending packet to dp port " + str(ingress_port))
        self.dataplane.send(ingress_port, str(pkt))
        #Verifying packets recieved on expected dataplane ports
        yes_ports = set(of_ports).difference([ingress_port])
        testutils.receive_pkt_check(self.dataplane, pkt, yes_ports, [ingress_port], self, self.logger)

    
tc = ForwardFlood()
_RESULT = tc.run()
