"""
<title>MultipleConnections</title>
<description>Connections to all (multiple) controllers must be kept in parallel
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

class MultipleConnections(MultipleController):
    """
    Connections to all (multiple) controllers must be kept in parallel
    """

    def runTest(self):

        self.logger.info("Running MultipleConnections test")
        self.logger.info("Connect 3 controllers and verify the connections are kept in parallel")
	self.logger.info("Send ROLE_REQUEST_NOCHANGE from each controller and verify it is active")

	self.logger.info("Sleep for 10 seconds ...")
	time.sleep(10)

	self.logger.info("Request role for controller 1")
        request = message.role_request()
        request.role = ofp.OFPCR_ROLE_NOCHANGE
        logMsg('logDebug',"Request to switch: ")
        logMsg('logDebug',request.show())
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, "Not able to send role request.")
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ROLE_REPLY,timeout=2)
        self.assertTrue(response is not None, 'Did not receive OFPT_ROLE_REPLY')
        logMsg('logDebug',"Response from switch: ")
        logMsg('logDebug',response.show())

	self.logger.info("Request role for controller 2")
        request = message.role_request()
        request.role = ofp.OFPCR_ROLE_NOCHANGE
        logMsg('logDebug',"Request to switch: ")
        logMsg('logDebug',request.show())
        rv = self.controller2.message_send(request)
        self.assertTrue(rv != -1, "Not able to send role request.")
        (response, pkt) = self.controller2.poll(exp_msg=ofp.OFPT_ROLE_REPLY,timeout=2)
        self.assertTrue(response is not None, 'Did not receive OFPT_ROLE_REPLY')
        logMsg('logDebug',"Response from switch: ")
        logMsg('logDebug',response.show())

	self.logger.info("Request role for controller 3")
        request = message.role_request()
        request.role = ofp.OFPCR_ROLE_NOCHANGE
        logMsg('logDebug',"Request to switch: ")
        logMsg('logDebug',request.show())
        rv = self.controller3.message_send(request)
        self.assertTrue(rv != -1, "Not able to send role request.")
        (response, pkt) = self.controller3.poll(exp_msg=ofp.OFPT_ROLE_REPLY,timeout=2)
        self.assertTrue(response is not None, 'Did not receive OFPT_ROLE_REPLY')
        logMsg('logDebug',"Response from switch: ")
        logMsg('logDebug',response.show())

tc = MultipleConnections()
_RESULT = tc.run()
