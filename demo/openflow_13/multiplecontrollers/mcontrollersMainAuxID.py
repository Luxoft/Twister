"""
<title>MainAuxID</title>
<description>Check the main connection have aux_id = 0
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

class MainAuxID(SimpleProtocol):

    """Check the main connection have aux_id = 0"""

    def runTest(self):

        self.logger.info("Running main connection aux_id test")
        self.logger.info("Sending FEATURES_REQUEST ")
        self.logger.info("Expecting FEATURES_REPLY ")

        request = message.features_request()
        logMsg('logDebug',"Request to switch: ")
        logMsg('logDebug',request.show())
        response,_ = self.controller.transact(request)
        self.assertTrue(response,"Got no features_reply to features_request")
        logMsg('logDebug',"Response from switch: ")
        logMsg('logDebug',response.show())
        self.assertEqual(response.header.type, ofp.OFPT_FEATURES_REPLY,'response is not echo_reply')
        self.assertTrue(len(response) >= 32, "features_reply too short: %d < 32 " % len(response))
        self.assertTrue(response.auxiliary_id == 0, "Connection aux_id is not 0")

    
tc = MainAuxID()
_RESULT = tc.run()
