"""
<title>BadTableID</title>
<description>
    Verify flow_mod with bad table_id return error
    
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

class BadTableID(SimpleDataPlane):
    """
    Verify flow_mod with bad table id return error 
    """
    def runTest(self):
        self.logger.info("Running BadTableID test")
        of_ports = self.port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 0, "Not enough ports for test")

        self.logger.info("Clear the switch state, delete all flows")
        rv = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rv, 0, "Failed to delete all flows")

        request = message.flow_mod()
        request.buffer_id = 0xffffffff
        inst = instruction.instruction_goto_table()
	inst.table_id = ofp.OFPTT_ALL
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
        self.assertTrue(response.type==ofp.OFPET_BAD_INSTRUCTION,
                               'Error type is not OFPET_BAD_INSTRUCTION')
        self.assertTrue(response.code==ofp.OFPFMFC_BAD_TABLE_ID,
                               'Error code is not OFPFMFC_BAD_TABLE_ID')

tc = BadTableID()
_RESULT = tc.run()
