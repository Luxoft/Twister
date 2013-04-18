"""
<title>BadMatchDuplicated</title>
<description>
    Verify a flow_mod with duplicated match generate error
    
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

class BadMatchDuplicated(SimpleDataPlane):
    """
    Verify flow_mod with a bad match duplicated generate error
    """
    def runTest(self):
        self.logger.info("Running BadMatchDuplicated test")
        self.logger.info("Insert flowmod and verify a duplicated match field generate error")
        of_ports = self.port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 0, "Not enough ports for test")

        act = action.action_output()
        ingress_port = of_ports[0]
        egress_port = of_ports[1]
        self.logger.info("Clear the switch state, delete all flows")
        rv = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rv, 0, "Failed to delete all flows")
        self.logger.info("Insert flow_mod")
        dstmatch = match.eth_dst(parse.parse_mac("00:01:02:03:04:05"))
        request = message.flow_mod()
        request.match_fields.tlvs.append(dstmatch)
	request.match_fields.tlvs.append(dstmatch)
        request.buffer_id = 0xffffffff
        act.port = of_ports[1]
        inst = instruction.instruction_apply_actions()
        inst.actions.add(act)
        request.instructions.add(inst)
        self.logger.info("Inserting flow")
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',request.show())
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, "Error installing flow mod")
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ERROR,
                                               timeout=5)
        self.assertTrue(response is not None,
                                'Switch did not reply with error messge')
        logMsg('logDebug',"Response from switch:")
        logMsg('logDebug',response.show())
        self.assertTrue(response.type==ofp.OFPET_BAD_MATCH,
                               'Error type is not OFPET_BAD_MATCH')
        self.assertTrue(response.code==ofp.OFPBMC_DUP_FIELD,
                               'Error code is not OFPBMC_DUP_FIELD')

    
tc = BadMatchDuplicated()
_RESULT = tc.run()
