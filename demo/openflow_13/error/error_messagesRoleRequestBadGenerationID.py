"""
<title>RoleRequestBadGenerationID</title>
<description>Send role request with invalid generation_id, switch must return error
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

class RoleRequestBadGenerationID(SimpleProtocol):

    """Send role request with invalid generation_id, switch must return error"""

    def runTest(self):

        self.logger.info("Running role request test ")

        self.logger.info("Sending OFPT_ROLE_REQUEST ")
        self.logger.info("Expecting OFPT_ROLE_REPLY ")

        request = message.role_request()
        request.role = ofp.OFPCR_ROLE_MASTER
        request.generation_id = 0
        rv = self.controller.message_send(request)
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',request.show())
        self.assertTrue(rv != -1, " Not able to send role request.")

        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ERROR,
                                               timeout=5)
        self.assertTrue(response is not None, "Switch did not reply")
        logMsg('logDebug',"Response from switch:")
        logMsg('logDebug',response.show())
        self.assertTrue(response.type == ofp.OFPET_ROLE_REQUEST_FAILED, "Response type is not OFPET_ROLE_REQUEST_FAILED")
        self.assertTrue(response.code == ofp.OFPRRFC_STALE, "Response code is not OFPRRFC_STALE")

    
tc = RoleRequestBadGenerationID()
_RESULT = tc.run()
