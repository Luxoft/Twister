"""
<title>OverlappingMeterMod</title>
<description>
    Insert a overlapping meter mod, switch must return error
    
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

class OverlappingMeterMod(SimpleProtocol):
    """
    Insert a overlapping meter mod, switch must return error
    """
    def runTest(self):
        self.logger.info("Running OverlappingMeterMod test")
        self.logger.info("Sending meter_mod request")

        self.logger.info("Delete all meters")
        rc = testutils.delete_all_meters(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")
        self.logger.info("Insert first meter_mod")
        msg = message.meter_mod()
        msg.command = ofp.OFPMC_ADD
        msg.meter_id = 1
        msg.flags = ofp.OFPMF_KBPS
        band1 = meter.meter_band_drop()
        band1.rate = 1024
        band1.burst_size = 12
        msg.bands.add(band1)
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',msg.show())
        rv = self.controller.message_send(msg)
        self.assertEqual(rv,0, "Meter_mod insert failed")

        #Second meter_mod, same meter_id
        self.logger.info("Insert second meter_mod with same meter_id")
        msg2 = message.meter_mod()
        msg2.command = ofp.OFPMC_ADD
        msg2.meter_id = 1
        msg2.flags = ofp.OFPMF_KBPS
        band2 = meter.meter_band_drop()
        band2.rate = 2048
        band2.burst_size = 14
        msg2.bands.add(band2)
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',msg2.show())
        rsp,_ = self.controller.transact(msg2, timeout=2)
        self.assertTrue(rsp is not None, "Switch did not reply")
        logMsg('logDebug',"Response from switch:")
        logMsg('logDebug',rsp.show())
        self.assertTrue(rsp.type == ofp.OFPET_METER_MOD_FAILED, "Switch must return METER_MOD_FAILED")
        self.assertTrue(rsp.code == ofp.OFPMMFC_METER_EXISTS, "Error is not OFPMMFC_METER_EXISTS")

    
tc = OverlappingMeterMod()
_RESULT = tc.run()
