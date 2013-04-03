"""
<title>MultipleCommandSources<title>
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

class MultipleCommandSources(MultipleController):
    """
    In equal state, the controller should receive Async messages
    """ 
    
    def runTest(self):

        self.logger.info("Running MultipleCommandSources test ")

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

        request = message.role_request()
        request.role = ofp.OFPCR_ROLE_NOCHANGE

	self.logger.info("Send a role_request from controller 1 and expect answer only on controller 1")
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, "Error sending role_request from controller 1")
	self.logger.info("Polling message on controller 1")
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ROLE_REPLY,
                                               timeout=5)
	self.assertTrue(response is not None, 'Did not receive OFPT_ROLE_REPLY from controller 1')

	self.logger.info("Verify role_reply is not received on controller 2 & 3")
        (response2, pkt) = self.controller2.poll(exp_msg=ofp.OFPT_ROLE_REPLY,
                                               timeout=5)
	self.assertTrue(response2 is None, 'Received role_reply from controller 2')

        (response3, pkt) = self.controller3.poll(exp_msg=ofp.OFPT_ROLE_REPLY,
                                               timeout=5)
	self.assertTrue(response3 is None, 'Received role_reply form controller 3')

tc = MultipleCommandSources(testbed=currentTB,ra_proxy=ra_service)
_RESULT = tc.run()
