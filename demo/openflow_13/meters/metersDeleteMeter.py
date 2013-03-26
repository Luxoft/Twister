"""
<title>DeleteMeter</title>
<description>
    Insert meter, verify stats, delete meter, verify stats.
    
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

class DeleteMeter(SimpleDataPlane):
    """
    Insert meter, verify stats, delete meter, verify stats.
    """
    def runTest(self):
        self.logger.info("Running Delete test")

        #Delete all meters
        self.logger.info("Delete all meters")
        rc = testutils.delete_all_meters(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all meters")

        #Insert meter_mod
        self.logger.info("Insert metermod")
        msg = message.meter_mod()
        msg.command = ofp.OFPMC_ADD
        msg.meter_id = 1
        msg.flags = ofp.OFPMF_PKTPS
        band1 = meter.meter_band_drop()
        band1.rate = 2
        band1.burst_size = 2
        msg.bands.add(band1)
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',msg.show())
        rv = self.controller.message_send(msg)

        #Request stats and verify meter is inserted
        self.logger.info("Request stats and verify meter is inserted")
        msg = message.meter_stats_request()
        msg.meter_id = ofp.OFPM_ALL
        rv, _ = self.controller.transact(msg, timeout= 2)
        self.assertEqual(str(len(rv.stats)), "1", "Switch should return one stats array")

        #Delete the meter
        self.logger.info("Delete the meter")
        msg = message.meter_mod()
        msg.command = ofp.OFPMC_DELETE
        msg.meter_id = 1
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',msg.show())
        rv = self.controller.message_send(msg)

        #Request meter stats and verify there is no meter present
        self.logger.info("Verify stats to see if meter was deleted")
        msg = message.meter_stats_request()
        msg.meter_id = ofp.OFPM_ALL
        rv, _ = self.controller.transact(msg, timeout= 2)
        self.assertEqual(str(len(rv.stats)), "0", "Switch should return empty stats array")

    
tc = DeleteMeter()
_RESULT = tc.run()
