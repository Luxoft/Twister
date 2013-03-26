"""
<title>EmptyFlowStats</title>
<description>
    Verify the switch replies to a flow stats request when
    the query doesn't match any flows.
    
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

class EmptyFlowStats(SimpleDataPlane):
    """
    Verify the switch replies to a flow stats request when
    the query doesn't match any flows.
    """
    def runTest(self):
        self.logger.info("Running EmptyFlowStats test")
        self.logger.info("Verify switch reply to flow_stats command")
        self.logger.info("Clear the switch state, delete all flows")
        rc = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")
        match = ofp.ofp_match()
        match.wildcards = 0
        stat_req = message.flow_stats_request()
        stat_req.match = match
        stat_req.table_id = 0xff
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',stat_req.show())
        response, pkt = self.controller.transact(stat_req)
        self.assertTrue(response is not None,
                        "No response to stats request")
        logMsg('logDebug',"Response from switch:")
        logMsg('logDebug',response.show())
        self.assertEqual(len(response.stats), 0)
        self.assertEqual(response.flags, 0)

    
tc = EmptyFlowStats()
_RESULT = tc.run()
