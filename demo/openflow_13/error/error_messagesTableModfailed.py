"""
<title>TableModFailed</title>
<description>Send table_mod with invalid table_id 
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

class TableModFailed(SimpleProtocol):

    """Send table_mod with invalid table_id , switch must return error"""

    def runTest(self):

        self.logger.info("Running table_mod failed test ")

        self.logger.info("Sending table_mod request ")
        self.logger.info("Expecting error ")

        request = message.table_mod()
        request.table_id = ofp.OFPTT_MAX 
        rv = self.controller.message_send(request)
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',request.show())
        self.assertTrue(rv != -1, " Not able to send queue config request.")

        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ERROR,
                                               timeout=5)
        self.assertTrue(response is not None, "Switch did not reply")
        logMsg('logDebug',"Response from switch:")
        logMsg('logDebug',response.show())
        self.assertTrue(response.type == ofp.OFPET_TABLE_MOD_FAILED, "Response type is not OFPET_TABLE_MOD_FAILED")

tc = TableModFailed()
_RESULT = tc.run()
