"""
<title>InvalidMeterConfigRequest</title>
<description>
    Request configuration for a meter that do not exist, switch must return error
    
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

class InvalidMeterConfigRequest(SimpleDataPlane):
    """
    Request configuration for a meter that do not exist, switch must return error
    """
    def runTest(self):
        self.logger.info("Running InvalidMeterConfigRequest test")
        self.logger.info("Sending meter_config_request")

        self.logger.info("Delete all meters")
        rc = testutils.delete_all_meters(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        msg = message.meter_config_request()
        msg.meter_id = 1
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',msg.show())
        rv, _ = self.controller.transact(msg, timeout= 2)
        logMsg('logDebug',"Response from switch:")
        logMsg('logDebug',rv.show())
        self.assertTrue(rv is not None, "Switch did not reply")
        self.assertTrue(rv.type == ofp.OFPET_METER_MOD_FAILED, "Switch must return METER_MOD_FAILED")
        self.assertTrue(rv.code == ofp.OFPMMFC_UNKNOWN_METER, "Error is not OFPMMFC_UNKNOWN_METER")

    
tc = InvalidMeterConfigRequest()
_RESULT = tc.run()
