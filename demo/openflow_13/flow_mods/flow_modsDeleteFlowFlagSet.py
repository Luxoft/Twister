"""
<title>DeleteFlowFlagSet</title>
<description>Request deletion of flow and set OFPFF_SEND_FLOW_REM flag, wait for flow removed message
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

class DeleteFlowFlagSet(SimpleDataPlane):

    """Request deletion of flow and set OFPFF_SEND_FLOW_REM flag, wait for flow removed message"""

    def runTest(self):
        self.logger.info("Running DeleteFlowFlagSet test")
        self.logger.info("Delete a flow with OFPFF_SEND_FLOW_REM flag set and wait to message")
        of_ports = self.port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 0, "Not enough ports for test")
        self.logger.info("Clear the switch state, delete all flows")
        rc = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        request = message.flow_mod()
        request.buffer_id = 0xffffffff
        request.out_port = of_ports[1]
        request.flags = ofp.OFPFF_SEND_FLOW_REM

        self.logger.info("Inserting flow ")
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, "Error installing flow mod")

        # Issue a delete command
        msg = message.flow_mod()
        msg.out_port = of_ports[1]
        msg.command = ofp.OFPFC_DELETE
        msg.buffer_id = 0xffffffff
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',request.show())
        self.controller.message_send(msg)

        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_FLOW_REMOVED,
                                               timeout=2)
        self.assertTrue(response is not None, 'Did not receive flow removed message ')
        logMsg('logDebug',"Response from switch:")
        logMsg('logDebug',response.show())
        self.assertEqual(str(response.reason), "2", "Reason not flow deleted")

    
tc = DeleteFlowFlagSet()
_RESULT = tc.run()
