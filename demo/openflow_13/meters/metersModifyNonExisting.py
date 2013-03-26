"""
<title>ModifyNonExisting</title>
<description>
    Try to modify a non existing meter, switch must return error
    
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

class ModifyNonExisting(SimpleDataPlane):
    """
    Try to modify a non existing meter, switch must return error
    """
    def runTest(self):
        self.logger.info("Running ModifyNonExisting test")

        #Delete all meters
        self.logger.info("Delete all meters")
        rc = testutils.delete_all_meters(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all meters")

        #Insert meter_mod
        self.logger.info("Try to modify a non existing meter")
        msg = message.meter_mod()
        msg.command = ofp.OFPMC_MODIFY
        msg.meter_id = 1
        msg.flags = ofp.OFPMF_KBPS
        band1 = meter.meter_band_drop()
        band1.rate = 1024
        band1.burst_size = 12
        msg.bands.add(band1)
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',msg.show())
        rv, _ = self.controller.transact(msg, timeout= 2)
        self.assertTrue(rv is not None, "Switch did not reply")
        logMsg('logDebug',"Response from switch:")
        logMsg('logDebug',rv.show())
        self.assertTrue(rv.type == ofp.OFPET_METER_MOD_FAILED, "Switch must return METER_MOD_FAILED")
        self.assertTrue(rv.code == ofp.OFPMMFC_UNKNOWN_METER, "Error is not OFPMMFC_UNKNOWN_METER")

    
tc = ModifyNonExisting()
_RESULT = tc.run()
