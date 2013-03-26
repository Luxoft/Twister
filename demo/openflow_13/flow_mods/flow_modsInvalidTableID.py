"""
<title>InvalidTableID</title>
<description>
    Verify flow_mod matches on UDP dst port
    
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

class InvalidTableID(SimpleDataPlane):
    """
    Verify flow_mod matches on UDP dst port
    """
    def runTest(self):
        self.logger.info("Running InvalidTableID test")
        self.logger.info("Insert a flow to invalid table ID, wait for error")
        of_ports = self.port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 0, "Not enough ports for test")

        act = action.action_output()
        self.logger.info("Clear the switch state, delete all flows")
        rv = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rv, 0, "Failed to delete all flows")

        request = message.flow_mod()
        request.buffer_id = 0xffffffff
        request.table_id = ofp.OFPTT_ALL
        act.port = of_ports[1]
        inst = instruction.instruction_apply_actions()
        inst.actions.add(act)
        request.instructions.add(inst)
        self.logger.info("Inserting flow")
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',request.show())
        rv, _ = self.controller.transact(request, timeout=5)
        self.assertTrue(rv is not None, "Error installing flow mod")
        logMsg('logDebug',"Response from switch:")
        logMsg('logDebug',rv.show())
        self.assertEqual(rv.type, ofp.OFPET_FLOW_MOD_FAILED, "Error type not FLOW_MOD_FAILED")
        self.assertEqual(rv.code, ofp.OFPFMFC_BAD_TABLE_ID, "Error code not BAD_TABLE_ID")

    
tc = InvalidTableID()
_RESULT = tc.run()
