"""
<title>BadActionBadOutPort</title>
<description>When the output to switch port action refers to a port that does not exit ,
    the switch generates an OFPT_ERROR msg , with type field OFPT_BAD_ACTION and code field OFPBAC_BAD_OUT_PORT
    
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

class BadActionBadOutPort(SimpleProtocol):

    """When the output to switch port action refers to a port that does not exit ,
    the switch generates an OFPT_ERROR msg , with type field OFPT_BAD_ACTION and code field OFPBAC_BAD_OUT_PORT
    """

    def runTest(self):

        self.logger.info("Running BadActionBadPort test")

        bad_port=ofp.OFPP_MAX
        pkt=testutils.simple_tcp_packet()

        #Send flow_mod message
        self.logger.info("Sending flow_mod message..")
        request = testutils.flow_msg_create(self, pkt, ing_port=1, egr_port=bad_port)
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',request.show())
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1 ,"Unable to send the message")
        # poll for error message
        self.logger.info("Waiting for OFPT_ERROR message...")
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ERROR,timeout=5)
        self.assertTrue(response is not None, "Switch did not reply")
        logMsg('logDebug',"Response from switch:")
        logMsg('logDebug',response.show())
        self.assertTrue(response.type == ofp.OFPET_BAD_ACTION, "Response type is not OFPET_BAD_ACTION")
        self.assertTrue(response.code == ofp.OFPBAC_BAD_OUT_PORT, "Response code is not OFPET_BAD_PORT")

    
tc = BadActionBadOutPort()
_RESULT = tc.run()
