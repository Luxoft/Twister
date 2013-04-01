"""
<title>MasterSlave</title>
<description>When a controller enters Master state all other Master controllers must move to Slave
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

class MasterSlave(MultipleController):

    """Check switch move a master to slave when other controller request to be master"""

    def runTest(self):

        self.logger.info("Running MasterSlave test")

	self.logger.info("Change all controllers to equal -- default")
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
	self.logger.info("Sending for controller 3 and get generation id")
        rv = self.controller3.message_send(request)
        self.assertTrue(rv != -1, " Not able to send role request.")
        (response, pkt) = self.controller3.poll(exp_msg=ofp.OFPT_ROLE_REPLY,
                                               timeout=2)
        self.assertTrue(response is not None, 'Did not receive OFPT_ROLE_REPLY')
        logMsg('logDebug',"Response from switch: ")
        logMsg('logDebug',response.show())
        self.assertTrue(response.role == ofp.OFPCR_ROLE_EQUAL, 'Role is not SLAVE')
	gen_id = response.generation_id
	######################################################
	
	new_gen_id = gen_id + 1	
	self.logger.info("Change controller 1 role to master")
        request = message.role_request()
        request.role = ofp.OFPCR_ROLE_MASTER
	request.generation_id = new_gen_id
        logMsg('logDebug',"Request to switch: ")
        logMsg('logDebug',request.show())
	self.logger.info("Sending for controller 1")
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, " Not able to send role request.")
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ROLE_REPLY,
                                               timeout=2)
        self.assertTrue(response is not None, 'Did not receive OFPT_ROLE_REPLY')
        logMsg('logDebug',"Response from switch: ")
        logMsg('logDebug',response.show())
        self.assertTrue(response.role == ofp.OFPCR_ROLE_MASTER, 'Role is not SLAVE')

	self.logger.info("Change controller 2 to master and verify controller 1 do not receive any message")
	new_gen_id += 1
        request = message.role_request()
        request.role = ofp.OFPCR_ROLE_MASTER
	request.generation_id = new_gen_id
        logMsg('logDebug',"Request to switch: ")
        logMsg('logDebug',request.show())
	self.logger.info("Sending for controller 2")
        rv = self.controller2.message_send(request)
        self.assertTrue(rv != -1, " Not able to send role request.")
        (response, pkt) = self.controller2.poll(exp_msg=ofp.OFPT_ROLE_REPLY,
                                               timeout=2)
        (response2, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ROLE_REPLY,
                                               timeout=2)
        self.assertTrue(response2 is None, 'Controller 1 recevied ROLE_REPLY')
        self.assertTrue(response is not None, 'Did not receive OFPT_ROLE_REPLY')
        logMsg('logDebug',"Response from switch: ")
        logMsg('logDebug',response.show())
        self.assertTrue(response.role == ofp.OFPCR_ROLE_MASTER, 'Role is not SLAVE')

	self.logger.info("Verify that controller 1 role is slave")
        request = message.role_request()
        request.role = ofp.OFPCR_ROLE_NOCHANGE
        logMsg('logDebug',"Request to switch: ")
        logMsg('logDebug',request.show())
	self.logger.info("Sending for controller 1")
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, " Not able to send role request.")
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ROLE_REPLY,
                                               timeout=2)
        self.assertTrue(response is not None, 'Did not receive OFPT_ROLE_REPLY')
        logMsg('logDebug',"Response from switch: ")
        logMsg('logDebug',response.show())
        self.assertTrue(response.role == ofp.OFPCR_ROLE_SLAVE, 'Role is not SLAVE')
	
tc = MasterSlave(testbed=currentTB,ra_proxy=ra_service)
_RESULT = tc.run()
