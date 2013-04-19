"""
<title>BadCommand</title>
<description>
    Send meter_mod with bad command, switch must return error
    
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

class BadCommand(SimpleDataPlane):
    """
    Send meter_mod with bad command, switch must return error
    """
    def runTest(self):
        self.logger.info("Running Delete test")

        #Delete all meters
        self.logger.info("Delete all meters")
        rc = testutils.delete_all_meters(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all meters")

        #Insert meter_mod
        self.logger.info("Insert metermod with bad command set")
        msg = message.meter_mod()
        msg.command = 8
        msg.meter_id = 1
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',msg.show())
        rv = self.controller.message_send(msg)
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ERROR,
                                               timeout=5)
	self.assertTrue(response is not None, 'Switch did not reply')
        self.assertTrue(response.type==ofp.OFPET_METER_MOD_FAILED,
                               'Error type is not OFPET_METER_MOD_FAILED')
        self.assertTrue(response.code==ofp.OFPMMFC_BAD_COMMAND,
                               'Error code is not OFPMMFC_BAD_COMMAND')
    
tc = BadCommand()
_RESULT = tc.run()
