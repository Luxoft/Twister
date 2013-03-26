"""
<title>FlowMod_ModifyStrict</title>
<description> Simple FlowMod Modify test
    delete all flows in the table
    insert an exact match flow_mod sending to port[1]
    then swap the output action from port[1] to port[2]
    then get flow_stats
    assert that the new actions are in place ( send packet)
    
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

class FlowMod_ModifyStrict(SimpleDataPlane):
    """ Simple FlowMod Modify test
    delete all flows in the table
    insert an exact match flow_mod sending to port[1]
    then swap the output action from port[1] to port[2]
    then get flow_stats
    assert that the new actions are in place ( send packet)
    """
    def runTest(self):
        self.logger.info("Running FlowMod_ModifyStrict test")
        self.logger.info("Insert flow_mod then modify output port with modify strict command")
        of_ports = self.port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 2, "Not enough ports for test")
        self.logger.info("Clear the switch state, delete all flows")
        rc = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        pkt = testutils.simple_tcp_packet()
        match = parse.packet_to_flow_match(pkt)

        ingress_port=of_ports[0]
        egress_port1=of_ports[1]
        egress_port2=of_ports[2]

        #First Flowmod
        self.logger.info("Insert first flow_mod")
        request = message.flow_mod()
        request.match_fields = match
        act = action.action_output()
        act.port = egress_port1
        act.max_len = ofp.OFPCML_NO_BUFFER
        inst = instruction.instruction_apply_actions()
        inst.actions.add(act)
        request.instructions.add(inst)
        request.buffer_id = 0xffffffff
        request.priority = 1000
        self.logger.debug("Adding flow ")
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',request.show())
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, "Failed to insert test flow")

        #Second Flowmod
        self.logger.info("Modify the first flow using OFPFC_MODIFY_STRICT command")
        request = message.flow_mod()
        request.command = ofp.OFPFC_MODIFY_STRICT
        request.match_fields = match
        act = action.action_output()
        act.port = egress_port2
        act.max_len = ofp.OFPCML_NO_BUFFER
        inst = instruction.instruction_apply_actions()
        inst.actions.add(act)
        request.instructions.add(inst)
        request.buffer_id = 0xffffffff
        request.priority = 1000
        self.logger.debug("Adding flow ")
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',request.show())
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, "Failed to insert test flow")

        flow_stats = testutils.flow_stats_get(self)
        self.assertEqual(len(flow_stats.stats),1, "Expected only one flow_mod")

        self.dataplane.send(ingress_port, str(pkt))
        #Verifying packets recieved on expected dataplane ports
        testutils.receive_pkt_check(self.dataplane, pkt, [egress_port2], [ingress_port], self, self.logger)

    
tc = FlowMod_ModifyStrict()
_RESULT = tc.run()
