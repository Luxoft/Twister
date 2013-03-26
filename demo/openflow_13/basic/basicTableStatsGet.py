"""
<title>TableStatsGet</title>
<description>
    Get table stats
    Natively verify that we get a reply
    do better sanity check of data in stats.TableStats test
    
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

class TableStatsGet(SimpleProtocol):
    """
    Get table stats
    Natively verify that we get a reply
    do better sanity check of data in stats.TableStats test
    """
    def runTest(self):
        self.logger.info("Running TableStatsGet test")
        self.logger.info("Sending table stats request")
        request = message.table_stats_request()
        logMsg('logDebug',"Request to switch:")
        logMsg('logDebug',request.show())
        response, _ = self.controller.transact(request, timeout=2)
        self.assertTrue(response is not None, "Did not get response")
        logMsg('logDebug',"Response from switch")
        logMsg('logDebug',response.show())

    
tc = TableStatsGet()
_RESULT = tc.run()
