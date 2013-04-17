"""
<title>BadQueueConfigPort</title>
<description>Send queue config request with invalid port
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

class BadQueuePort(SimpleProtocol):

    """Send queue config with bad port , switch must return error"""

    def runTest(self):

        self.logger.info("Running queue config bad port test ")

        self.logger.info("Sending queue_get_config_request ")
        self.logger.info("Expecting queue_get_config_reply ")

        request = message.queue_get_config_request()
        request.port = ofp.OFPP_MAX
        rv = self.controller.message_send(request)
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',request.show())
        self.assertTrue(rv != -1, " Not able to send queue config request.")

        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ERROR,
                                               timeout=5)
        self.assertTrue(response is not None, "Switch did not reply")
        logMsg('logDebug',"Response from switch:")
        logMsg('logDebug',response.show())
        self.assertTrue(response.type == ofp.OFPET_QUEUE_OP_FAILED, "Response type is not OFPET_QUEUE_OP_FAILED")

tc = BadQueuePort()
_RESULT = tc.run()
