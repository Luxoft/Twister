"""
<title>QueueStatsRequest</title>
<description>Verify Queue Stats is available 
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

class QueueStatsRequest(SimpleProtocol):

    """Verify Queue stats message body """

    def runTest(self):

        self.logger.info("Running QueueStatsRequest")

        of_ports = self.port_map.keys()
        of_ports.sort()

        self.logger.info("Sending Queue stats Request ...")
        request = message.queue_stats_request()
        request.port_no = of_ports[0]
        logMsg('logDebug',"Request to switch:")
        logMsg('logDebug',request.show())
        response, pkt = self.controller.transact(request)
        self.assertTrue(response is not None,
                        "Did not get reply ")
        logMsg('logDebug',"Response from switch:")
        logMsg('logDebug',response.show())
        self.assertTrue(response.header.type == 19, "Reply is not multipart Reply")
    
tc = QueueStatsRequest()
_RESULT = tc.run()
