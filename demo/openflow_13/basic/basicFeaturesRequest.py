"""
<title>FeaturesRequest</title>
<description>
    Test features_request to make sure we get a response
    Does NOT test the contents; just that we get a response
    
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

class FeaturesRequest(SimpleProtocol):
    """
    Test features_request to make sure we get a response
    Does NOT test the contents; just that we get a response
    """
    def runTest(self):
        self.logger.info("Running FeaturesRequest test")
        request = message.features_request()
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',request.show())
        response,_ = self.controller.transact(request)
        self.assertTrue(response,"Got no features_reply to features_request")
        logMsg('logDebug',"Response from switch:")
        logMsg('logDebug',response.show())
        self.assertEqual(response.header.type, ofp.OFPT_FEATURES_REPLY,
                         'response is not echo_reply')
        self.assertTrue(len(response) >= 32, "features_reply too short: %d < 32 " % len(response))

    
tc = FeaturesRequest()
_RESULT = tc.run()
