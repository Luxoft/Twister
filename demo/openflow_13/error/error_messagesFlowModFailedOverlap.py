"""
<title>FlowModFailedOverlap</title>
<description>Verify that if overlap check flag is set in the flow entry and an
        overlapping flow is inserted then an error
        type OFPET_FLOW_MOD_FAILED code OFPFMFC_OVERLAP
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

class FlowModFailedOverlap(SimpleDataPlane):

    """Verify that if overlap check flag is set in the flow entry and an
        overlapping flow is inserted then an error
        type OFPET_FLOW_MOD_FAILED code OFPFMFC_OVERLAP"""

    def runTest(self):

        self.logger.info("Running FlowModFailedOverlap test")

        of_ports = self.port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 1, "Not enough ports for test")

        #Clear Switch State
        rc = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")
        testutils.do_barrier(self.controller)

        self.logger.info("Insert first flow_mod")
        #Insert a flow F with wildcarded all fields
        (pkt,match) = testutils.wildcard_all_except_ingress(self,of_ports)
        testutils.do_barrier(self.controller)

        #Verify flow is active
        testutils.verify_tablestats(self,expect_active=1)
        testutils.do_barrier(self.controller)
        # Build a overlapping flow F'-- Wildcard All except ingress with check overlap bit set
        self.logger.info("Build and insert the second flow_mod that overlaps the first one")
        pkt_matchingress = testutils.simple_tcp_packet()
        match3 = parse.packet_to_flow_match(pkt_matchingress)
        self.assertTrue(match3 is not None, "Could not generate flow match from pkt")

        request = message.flow_mod()
        request.flags = ofp.OFPFF_CHECK_OVERLAP
        request.cookie = random.randint(0,9007199254740992)
        request.buffer_id = 0xffffffff
        request.match_fields = match3
        act = action.action_output()
        act.port = ofp.OFPP_ALL
        inst = instruction.instruction_apply_actions()
        inst.actions.add(act)
        request.instructions.add(inst)
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',request.show())
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, "Error installing flow mod")

        self.logger.info("Verify table stats in order to expect active flow count 1")
        # Verify Flow does not get inserted
        testutils.verify_tablestats(self,expect_active=1)

        #Verify OFPET_FLOW_MOD_FAILED/OFPFMFC_OVERLAP error is recieved on the control plane
        self.logger.info("Waiting for OFPT_ERROR message...")
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ERROR,
                                               timeout=5)
        self.assertTrue(response is not None,
                               'Switch did not reply with error message')
        logMsg('logDebug',"Response from switch:")
        logMsg('logDebug',response.show())
        self.assertTrue(response.type==ofp.OFPET_FLOW_MOD_FAILED,
                               'Error type is not flow mod failed ')
        self.assertTrue(response.code==ofp.OFPFMFC_OVERLAP,
                               'Error code is not overlap')

    
tc = FlowModFailedOverlap()
_RESULT = tc.run()
