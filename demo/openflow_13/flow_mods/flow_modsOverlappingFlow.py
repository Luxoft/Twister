"""
<title>OverlappingFlow</title>
<description>
    Insert two identical flows, second flow has overlapping flag enabled so the switch must return a overlapping flow error code.
    
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

class OverlappingFlow(SimpleDataPlane):
    """
    Insert two identical flows, second flow has overlapping flag enabled so the switch must return a overlapping flow error code.
    """
    def runTest(self):
        self.logger.info("Running OverlappingFlow test")
        self.logger.info("Insert two identical flows, verify overlapping error is returned")
        of_ports = self.port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 0, "Not enough ports for test")
        self.logger.info("Clear the switch state,delete all flows")
        rc = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        #Insert first flowmod
        self.logger.info("Insert first flow_mod")
        portmatch = match.in_port(of_ports[0])
        request = message.flow_mod()
        request.match_fields.tlvs.append(portmatch)
        request.buffer_id = 0xffffffff
        request.priority = 1
        inst = instruction.instruction_apply_actions()

        act_out = action.action_output()
        act_out.port = of_ports[1]
        inst.actions.add(act_out)
        request.instructions.add(inst)
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',request.show())
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, "Error installing flow mod")

        #Insert second flowmod but with overlap checking flag enabled
        self.logger.info("Insert second identical flow_mod")
        portmatch = match.in_port(of_ports[0])
        request = message.flow_mod()
        request.match_fields.tlvs.append(portmatch)
        request.buffer_id = 0xffffffff
        request.flags = ofp.OFPFF_CHECK_OVERLAP
        request.priority = 1
        inst = instruction.instruction_apply_actions()
        act_out = action.action_output()
        act_out.port = of_ports[1]
        inst.actions.add(act_out)
        request.instructions.add(inst)
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',request.show())
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, "Error installing flow mod")

        response,_ = self.controller.poll(ofp.OFPT_ERROR, 2 )
        self.assertTrue(response is not None,
                               'Switch did not reply with expected error messge')
        logMsg('logDebug',"Response from switch:")
        logMsg('logDebug',response.show())
        self.assertTrue(response.code==3,
                               'Error type is not OVERLAPPING FLOW')

    
tc = OverlappingFlow()
_RESULT = tc.run()
