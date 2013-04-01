"""
<title>EqualChangeSwitchState</title>
<description>In equal state, the controller has full read / write access to the Switch
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

class EqualChangeSwitchState(MultipleController):
    """
    In equal state, the controller has full read / write access to the Switch
    """ 
    
    def runTest(self):

        self.logger.info("Running EqualChangeSwitchState test ")
        self.logger.info("Controllers in EQUAL state should be able to change switch state")

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

	self.logger.info("Insert a flow from each controller")

	self.logger.info("Sending flow_mod from controller 1")
        request = message.flow_mod()
        request.buffer_id = 0xffffffff
	request.priority = 1
        logMsg('logDebug',"Request to switch:")
        logMsg('logDebug',request.show())
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, "Error installing flow mod")

	self.logger.info("Sending flow_mod for controller 2")
        request = message.flow_mod()
        request.buffer_id = 0xffffffff
	request.priority = 2
        logMsg('logDebug',"Request to switch:")
        logMsg('logDebug',request.show())
        rv = self.controller2.message_send(request)
        self.assertTrue(rv != -1, "Error installing flow mod")

	self.logger.info("Sending flow_mod for controller 3")
        request = message.flow_mod()
        request.buffer_id = 0xffffffff
	request.priority = 3
        logMsg('logDebug',"Request to switch:")
        logMsg('logDebug',request.show())
        rv = self.controller3.message_send(request)
        self.assertTrue(rv != -1, "Error installing flow mod")

	self.logger.info("Sending stats request in order to verify 3 flow's are active")
        response = testutils.ag_flow_stats_get(self)
	self.assertTrue(response is not None, 'Did not receive stats reply')
	self.assertTrue(response.flow_count == 3, 'Flowcount is not 3')
        logMsg('logDebug',"Response from switch: ")
        logMsg('logDebug',response.show())

    
tc = EqualChangeSwitchState()
_RESULT = tc.run()
