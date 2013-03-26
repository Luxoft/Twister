"""
<title>MeterFeatureRequest</title>
<description>
    Send meter feature request and verify that switch respond
    
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

class MeterFeatureRequest(SimpleProtocol):
    """
    Send meter feature request and verify that switch respond
    """
    def runTest(self):
        self.logger.info("Running MeterFeatureRequest test")
        self.logger.info("Sending meter feature request")
        msg = message.meter_features_request()
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',msg.show())
        response, _ = self.controller.transact(msg, timeout=2)
        self.assertTrue(response is not None, "Did not get response")
        logMsg('logDebug',"Response from switch:")
        logMsg('logDebug',response.show())
        self.assertTrue(response.type==ofp.OFPMP_METER_FEATURES, "Response is not OFPMP_METER_FEATURES")

    
tc = MeterFeatureRequest()
_RESULT = tc.run()
