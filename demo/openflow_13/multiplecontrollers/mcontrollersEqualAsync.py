"""
<title>EqualAsync<title>
<description>In equal state, the controller should receive Async messages
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

class EqualAsync(MultipleController):
    """
    In equal state, the controller should receive Async messages
    """ 
    
    def runTest(self):

        self.logger.info("Running EqualAsync test ")

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

	self.logger.info("Insert a flow with hard expire set to 2 sec")
        request = message.flow_mod()
        request.buffer_id = 0xffffffff
	request.hard_timeout = 2
        logMsg('logDebug',"Request to switch:")
        logMsg('logDebug',request.show())
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, "Error installing flow mod")

	self.logger.info("Waiting for async flow_removed message")
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_FLOW_REMOVED,
                                               timeout=5)
	self.assertTrue(response is not None, 'Did not receive OFPT_FLOW_REMOVED async from switch')

        (response2, pkt) = self.controller2.poll(exp_msg=ofp.OFPT_FLOW_REMOVED,
                                               timeout=5)
	self.assertTrue(response2 is not None, 'Did not receive OFPT_FLOW_REMOVED async from switch')

        (response3, pkt) = self.controller3.poll(exp_msg=ofp.OFPT_FLOW_REMOVED,
                                               timeout=5)
	self.assertTrue(response3 is not None, 'Did not receive OFPT_FLOW_REMOVED async from switch')

tc = EqualAsync(testbed=currentTB,ra_proxy=ra_service)
_RESULT = tc.run()
