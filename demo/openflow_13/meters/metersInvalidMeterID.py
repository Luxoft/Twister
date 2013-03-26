"""
<title>InvalidMeterID</title>
<description>
    Insert a meter mod with meter_id=0, switch must return error
    
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

class InvalidMeterID(SimpleProtocol):
    """
    Insert a meter mod with meter_id=0, switch must return error
    """
    def runTest(self):
        self.logger.info("Running InvalidMeterID test")
        self.logger.info("Sending meter_mod request")

        self.logger.info("Delete all meters")
        rc = testutils.delete_all_meters(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        msg = message.meter_mod()
        msg.command = ofp.OFPMC_ADD
        msg.meter_id = 0
        msg.flags = ofp.OFPMF_KBPS
        band1 = meter.meter_band_drop()
        band1.rate = 1024
        band1.burst_size = 12
        msg.bands.add(band1)
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',msg.show())
        rsp,_ = self.controller.transact(msg, timeout=2)
        self.assertTrue(rsp is not None, "Switch must return error since meter_id is 0")
        logMsg('logDebug',"Response from switch:")
        logMsg('logDebug',rsp.show())
        self.assertTrue(rsp.type == ofp.OFPET_METER_MOD_FAILED, "Switch must return METER_MOD_FAILED, meter_id 0 must be invalid")

    
tc = InvalidMeterID()
_RESULT = tc.run()
