"""
<title>SimpleMeterMod</title>
<description>
    Insert a simple meter_mod and verify there is no error returned
    
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

class SimpleMeterMod(SimpleProtocol):
    """
    Insert a simple meter_mod and verify there is no error returned
    """
    def runTest(self):
        self.logger.info("Running SimpleMeterMod test")
        self.logger.info("Sending meter_mod request")

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
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',msg.show())
        response = self.controller.message_send(msg)

        #Verify meter is inserted
        self.logger.info("Sending meter_stats_request")
        msg = message.meter_stats_request()
        msg.meter_id = ofp.OFPM_ALL
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',msg.show())
        rv, _ = self.controller.transact(msg, timeout= 2)
        logMsg('logDebug',"Response from switch:")
        logMsg('logDebug',rv.show())
        self.assertEqual(str(len(rv.stats)), "1", "Switch should return one stats array")

    
tc = SimpleMeterMod()
_RESULT = tc.run()
