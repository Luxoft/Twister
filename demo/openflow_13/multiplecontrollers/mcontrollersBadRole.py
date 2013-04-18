"""
<title>BadRole</title>
<description>Send role request with invalid role, switch must return error 
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

class BadRole(MultipleController):

    """Send role request with invalid role id, switch must return error """

    def runTest(self):

        self.logger.info("Sending OFPT_ROLE_REQUEST ")
        self.logger.info("Expecting error ")

        #Get the current generation_id
        request = message.role_request()
        request.role = ofp.OFPCR_ROLE_SLAVE
        request.generation_id = 1
        logMsg('logDebug',"Request to switch: ")
        logMsg('logDebug',request.show())
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, " Not able to send role request.")
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ROLE_REPLY,
                                               timeout=2)
        self.assertTrue(response is not None, 'Did not receive OFPT_ROLE_REPLY')
        logMsg('logDebug',"Response from switch: ")
        logMsg('logDebug',response.show())
        #Decrease generation_id by 1
        new_genid = response.generation_id - 1

        #Send role change request
        request = message.role_request()
        request.role = 5 
        request.generation_id = new_genid
        logMsg('logDebug',"Request to switch: ")
        logMsg('logDebug',request.show())
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, "Not able to send role request.")
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ERROR,
                                               timeout=2)
        self.assertTrue(response is not None, 'Did not receive OFPT_ROLE_REPLY')
        logMsg('logDebug',"Response from switch: ")
        logMsg('logDebug',response.show())
        self.assertTrue(response.type == ofp.OFPET_ROLE_REQUEST_FAILED, 'Error is not RoleRequestFailed')
        self.assertTrue(response.code == ofp.OFPRRFC_BAD_ROLE, 'Error is not OFPRRFC_BAD_ROLE')

    
tc = BadRole(testbed=currentTB,ra_proxy=ra_service)
_RESULT = tc.run()
