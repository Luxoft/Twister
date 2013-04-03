"""
<title>MultipleCommandSourcesError<title>
<description>Errors and replies only to the initiating controller
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

class MultipleCommandSourcesError(MultipleController):
    """
    In equal state, the controller should receive Async messages
    """ 
    
    def runTest(self):

        self.logger.info("Running MultipleCommandSourcesError test ")

        #Send role change request
	self.logger.info("Generate role request message")
        request = message.role_request()
        request.role = ofp.OFPCR_ROLE_EQUAL
        logMsg('logDebug',"Request to switch: ")
        logMsg('logDebug',request.show())
	######################################################
	self.logger.info("Sending for controller 1")
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, " Not able to send role request.")
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ROLE_REPLY,
                                               timeout=2)
        self.assertTrue(response is not None, 'Did not receive OFPT_ROLE_REPLY')
        logMsg('logDebug',"Response from switch: ")
        logMsg('logDebug',response.show())
        self.assertTrue(response.role == ofp.OFPCR_ROLE_EQUAL, 'Role is not SLAVE')
	######################################################
	self.logger.info("Sending for controller 2")
        rv = self.controller2.message_send(request)
        self.assertTrue(rv != -1, " Not able to send role request.")
        (response, pkt) = self.controller2.poll(exp_msg=ofp.OFPT_ROLE_REPLY,
                                               timeout=2)
        self.assertTrue(response is not None, 'Did not receive OFPT_ROLE_REPLY')
        logMsg('logDebug',"Response from switch: ")
        logMsg('logDebug',response.show())
        self.assertTrue(response.role == ofp.OFPCR_ROLE_EQUAL, 'Role is not SLAVE')
	######################################################
	self.logger.info("Sending for controller 3")
        rv = self.controller3.message_send(request)
        self.assertTrue(rv != -1, " Not able to send role request.")
        (response, pkt) = self.controller3.poll(exp_msg=ofp.OFPT_ROLE_REPLY,
                                               timeout=2)
        self.assertTrue(response is not None, 'Did not receive OFPT_ROLE_REPLY')
        logMsg('logDebug',"Response from switch: ")
        logMsg('logDebug',response.show())
        self.assertTrue(response.role == ofp.OFPCR_ROLE_EQUAL, 'Role is not SLAVE')
	######################################################

        self.logger.info("Sending multipart request with invalid type")
        msg = message.meter_features_request()
        msg.type = 90
        rv = self.controller.message_send(msg)
	(response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ERROR,
                                               timeout=5)	
        self.assertTrue(response is not None, "Did not get response")
        logMsg('logDebug',"Response from switch:")
        logMsg('logDebug',response.show())
        self.assertTrue(response.type==ofp.OFPET_BAD_REQUEST, "Response is not OFPET_BAD_REQUEST")
        self.assertTrue(response.code==ofp.OFPBRC_BAD_MULTIPART, "Response is not BAD_MULTIPART")

	self.logger.info("Verify error message is not received on controller 2 & 3")
        (response2, pkt) = self.controller2.poll(exp_msg=ofp.OFPT_ERROR,
                                               timeout=5)
	self.assertTrue(response2 is None, 'Received error message from controller 2')

        (response3, pkt) = self.controller3.poll(exp_msg=ofp.OFPT_ERROR,
                                               timeout=5)
	self.assertTrue(response3 is None, 'Received error message form controller 3')

tc = MultipleCommandSourcesError(testbed=currentTB,ra_proxy=ra_service)
_RESULT = tc.run()
