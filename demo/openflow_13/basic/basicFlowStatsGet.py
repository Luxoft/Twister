"""
<title>FlowStatsGet</title>
<description>
    Get stats
    Simply verify stats get transaction
    
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

class FlowStatsGet(SimpleProtocol):
    """
    Get stats
    Simply verify stats get transaction
    """
    def runTest(self):

        self.logger.info("Running StatsGet")
        self.logger.info("Inserting trial flow")
        request = message.flow_mod()
        request.buffer_id = 0xffffffff

        logMsg('logDebug',"Request to switch:")
        logMsg('logDebug',request.show())
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, "Failed to insert test flow")

        self.logger.info("Sending flow request")
        response = testutils.flow_stats_get(self)
        logMsg('logDebug',"Response from switch: ")
        logMsg('logDebug',response.show())

    
tc = FlowStatsGet()
_RESULT = tc.run()
