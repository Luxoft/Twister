"""
<title>InvalidMeterStats</title>
<description>
    Request stats for a meter_id that do not exist, switch must return error
    
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

class InvalidMeterStats(SimpleProtocol):
    """
    Request stats for a meter_id that do not exist, switch must return error
    """
    def runTest(self):
        self.logger.info("Running InvalidMeterStats test")
        self.logger.info("Sending meter_stats request")

        self.logger.info("Delete all meters")
        rc = testutils.delete_all_meters(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        msg = message.meter_mod()
        msg.command = ofp.OFPMC_ADD
        msg.meter_id = 1
        msg.flags = ofp.OFPMF_KBPS
        band1 = meter.meter_band_drop()
        band1.rate = 1024
        band1.burst_size = 12
        msg.bands.add(band1)
        band5 = meter.meter_band_drop()
        band5.rate = 2048
        band5.burst_size = 18
        msg.bands.add(band5)
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',msg.show())
        rv = self.controller.message_send(msg)

        #Request stats for meter_id 2 that do not exist
        self.logger.info("Request meters stats for invalid meter_id")
        msg3 = message.meter_stats_request()
        msg3.meter_id = 2
        logMsg('logDebug',"Request from switch:")
        logMsg('logDebug',msg3.show())
        rv, _ = self.controller.transact(msg3, timeout=2)
        self.assertTrue(rv is not None, "Switch did not reply")
        logMsg('logDebug',"Response from switch:")
        logMsg('logDebug',rv.show())
        self.assertTrue(rv.type == ofp.OFPET_METER_MOD_FAILED, "Switch must return METER_MOD_FAILED")
        self.assertTrue(rv.code == ofp.OFPMMFC_UNKNOWN_METER, "Error is not OFPMMFC_METER_EXISTS")

    
tc = InvalidMeterStats()
_RESULT = tc.run()
