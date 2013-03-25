"""
<title>ForwardAll</title>
<description>ForwardAll : Packet is sent to all dataplane ports
    except ingress port when output action.port = OFPP_ALL
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

class ForwardAll(SimpleDataPlane):

    """ForwardAll : Packet is sent to all dataplane ports
    except ingress port when output action.port = OFPP_ALL"""

    def runTest(self):
        self.logger.info("Running ForwardAll except ingress test")
        of_ports = self.port_map.keys()
        of_ports.sort()

        self.assertTrue(len(of_ports) > 1, "Not enough ports for test")

        self.logger.info("Clear the switch state")

        rc = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        pkt = testutils.simple_tcp_packet()
        match = parse.packet_to_flow_match(pkt)

        ingress_port=of_ports[0]

        # Need to insert flow fowarding packets to the controller!!!
        self.logger.info("Generate flow_mod message")
        request = message.flow_mod()
        request.match_fields = match
        act = action.action_output()
        act.port = ofp.OFPP_ALL
        act.max_len = ofp.OFPCML_NO_BUFFER
        inst = instruction.instruction_apply_actions()
        inst.actions.add(act)
        request.instructions.add(inst)
        request.buffer_id = 0xffffffff
        request.priority = 1000
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',request.show())
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, "Failed to insert test flow")
        self.logger.info("Sending packets to matching flow")
        self.dataplane.send(ingress_port, str(pkt))
        #Verifying packets recieved on expected dataplane ports
        yes_ports = set(of_ports).difference([ingress_port])
        testutils.receive_pkt_check(self.dataplane, pkt, yes_ports, [ingress_port], self, self.logger)

    
tc = ForwardAll()
_RESULT = tc.run()
