"""
<title>ConfigurationRequest</title>
<description>Check basic Get Config request is implemented
    a) Send OFPT_GET_CONFIG_REQUEST
    b) Verify OFPT_GET_CONFIG_REPLY is received without errors
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

class ConfigurationRequest(SimpleProtocol):

    """Check basic Get Config request is implemented
    a) Send OFPT_GET_CONFIG_REQUEST
    b) Verify OFPT_GET_CONFIG_REPLY is received without errors"""

    def runTest(self):

        self.logger.info("Running Configuration_Request test ")

        self.logger.info("Sending OFPT_GET_CONFIG_REQUEST ")
        self.logger.info("Expecting OFPT_GET_CONFIG_REPLY ")

        request = message.get_config_request()
        logMsg('logDebug',"Request to switch:")
        logMsg('logDebug',request.show())
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, " Not able to send get_config request.")

        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_GET_CONFIG_REPLY,
                                               timeout=2)
        self.assertTrue(response is not None,
                        'Did not receive OFPT_GET_CONFIG_REPLY')
        logMsg('logDebug',"Response from switch:")
        logMsg('logDebug',response.show())

    
tc = ConfigurationRequest()
_RESULT = tc.run()
