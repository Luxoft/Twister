from basicSimpleProtocol import *

class FeaturesRequest(SimpleProtocol):
    """
    Test features_request to make sure we get a response

    Does NOT test the contents; just that we get a response
    """
    def runTest(self):
        request = message.features_request()
        response,_ = self.controller.transact(request)
        self.assertTrue(response,"Got no features_reply to features_request")
        self.assertEqual(response.header.type, ofp.OFPT_FEATURES_REPLY,
                         'response is not features_reply')
        self.assertTrue(len(response) >= 32, "features_reply too short: %d < 32 " % len(response))
        
tc=FeaturesRequest()
_RESULT=tc.run()
