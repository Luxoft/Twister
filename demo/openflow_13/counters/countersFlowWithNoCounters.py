"""
<title>FlowWithNoCounters</title>
<description>Verify Byte counters per flow are
    set to maximum when NO_BYT_COUNTS and NO_PKT_COUNTS flags are set
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

class FlowWithNoCounters(SimpleDataPlane):

    """Verify Byte counters per flow are
    set to maximum when NO_BYT_COUNTS and NO_PKT_COUNTS flags are set"""

    def runTest(self):

        self.logger.info("Running BytePerFlow test")

        of_ports = self.port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 1, "Not enough ports for test")

        #Clear switch State
        rc = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        pkt = testutils.simple_tcp_packet()
        match = parse.packet_to_flow_match(pkt)

        ingress_port=of_ports[0]

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
        request.flags = ofp.OFPFF_NO_PKT_COUNTS + ofp.OFPFF_NO_BYT_COUNTS

        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',request.show())

        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, "Failed to insert test flow")
        self.dataplane.send(ingress_port, str(pkt))
        response = testutils.flow_stats_get(self,match)
        self.assertTrue(response is not None, "Switch did not reply")
        logMsg('logDebug',"Response from switch:")
        logMsg('logDebug',response.show())
        for item in response.stats:
            self.assertTrue(item.packet_count >= 18446744073709551615, "Packet count not returned at maximum value")
            self.assertTrue(item.byte_count >= 18446744073709551615, "Byte count not returned at maximum value")

    
tc = FlowWithNoCounters()
_RESULT = tc.run()
