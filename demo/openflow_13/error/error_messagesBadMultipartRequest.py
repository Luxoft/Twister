"""
<title>BadMultipartRequest</title>
<description>
    Send a bad multipart request, wait to OFPET_BAD_MULTIPART
    
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

class BadMultipartRequest(SimpleProtocol):
    """
    Send a bad multipart request, wait to OFPET_BAD_MULTIPART
    """
    def runTest(self):
        self.logger.info("Running BadMultipartRequest test")
        self.logger.info("Sending multipart request with invalid type")
        msg = message.meter_features_request()
        msg.type = 90
        response, _ = self.controller.transact(msg, timeout=2)
        self.assertTrue(response is not None, "Did not get response")
        logMsg('logDebug',"Response from switch:")
        logMsg('logDebug',response.show())
        self.assertTrue(response.type==ofp.OFPET_BAD_REQUEST, "Response is not OFPET_BAD_REQUEST")
        self.assertTrue(response.code==ofp.OFPBRC_BAD_MULTIPART, "Response is not BAD_MULTIPART")

    
tc = BadMultipartRequest()
_RESULT = tc.run()
