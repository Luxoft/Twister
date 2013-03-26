"""
<title>ModifyMeterMod</title>
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

class ModifyMeterMod(SimpleProtocol):
    """
    Insert a simple meter_mod and verify there is no error returned
    """
    def runTest(self):
        self.logger.info("Running ModifyMeterMod test")
        self.logger.info("Sending meter_mod request")

        self.logger.info("Delete all meters")
        rc = testutils.delete_all_meters(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        #Insert meter_mod
        self.logger.info("Insert meter mod")
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

        #Modify meter_mod 1
        self.logger.info("Modify meter 1")
        msg = message.meter_mod()
        msg.command = ofp.OFPMC_MODIFY
        msg.meter_id = 1
        msg.flags = ofp.OFPMF_KBPS
        band1 = meter.meter_band_drop()
        band1.rate = 2024
        band1.burst_size = 12
        msg.bands.add(band1)
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',msg.show())
        response = self.controller.message_send(msg)

        #Request meter config for meter 1
        self.logger.info("Verify stats")
        msg = message.meter_config_request()
        msg.meter_id = 1
        rv, _ = self.controller.transact(msg, timeout= 2)
        for item in rv.bands:
            for item2 in item.bands.meters:
                self.assertEqual(item2.rate, 2024, "Meter_mod not modifyed")

    
tc = ModifyMeterMod()
_RESULT = tc.run()
