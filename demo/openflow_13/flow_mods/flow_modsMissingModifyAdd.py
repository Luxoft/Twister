"""
<title>MissingModifyAdd</title>
<description>If a modify does not match an existing flow, the flow do not get added 
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

class MissingModifyAdd(SimpleDataPlane):

    """If a modify does not match an existing flow, the flow do not get added """

    def runTest(self):

        self.logger.info("Running Missing_Modify_Add test")
        self.logger.info("If a modify does not match an existing flow, the flow do not get added")

        of_ports = self.port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 0, "Not enough ports for test")

        self.logger.info("Clear the switch state, delete all flows")
        rc = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        #Generate a flow-mod,command OFPC_MODIFY
        self.logger.info("Insert flow_mod with OFPFC_MODIFY command")
        ingress_port = of_ports[0]
        egress_port = of_ports[1]
        portmatch = match.in_port(ingress_port)
        request = message.flow_mod()
        request.match_fields.tlvs.append(portmatch)
        request.buffer_id = 0xffffffff
        request.command = ofp.OFPFC_MODIFY
        inst = instruction.instruction_apply_actions()
        act = action.action_output()
        act.port = egress_port
        inst.actions.add(act)
        request.instructions.add(inst)
        self.logger.info("Inserting flow ")
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',request.show())
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, "Error installing flow mod")

        #Verify the flow gets added i.e. active_count= 0
        testutils.verify_tablestats(self,expect_active=0)

    
tc = MissingModifyAdd()
_RESULT = tc.run()
