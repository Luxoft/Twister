"""
<title>RoleRequest</title>
<description>Check basic role request is implemented
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

class RoleRequest(SimpleProtocol):

    """Check basic role request is implemented"""

    def runTest(self):

        self.logger.info("Running role request test ")

        self.logger.info("Sending OFPT_ROLE_REQUEST ")
        self.logger.info("Expecting OFPT_ROLE_REPLY ")

        request = message.role_request()
        request.role = ofp.OFPCR_ROLE_NOCHANGE
        logMsg('logDebug',"Request to switch:")
        logMsg('logDebug',request.show())
        response, _ = self.controller.transact(request)

        self.assertTrue(response is not None,
                        'Did not receive OFPT_ROLE_REPLY')
        logMsg('logDebug',"Response from switch:")
        logMsg('logDebug',response.show())
        self.assertTrue(response.type == ofp.OFPT_ROLE_REPLY, "Role reply not received")

    
tc = RoleRequest()
_RESULT = tc.run()
