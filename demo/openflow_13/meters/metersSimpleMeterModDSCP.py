"""
<title>SimpleMeterModDSCP</title>
<description>
    Insert a simple meter_mod with mark DSCP band and verify there is no error returned
    
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

class SimpleMeterModDSCP(SimpleProtocol):
    """
    Insert a simple meter_mod with mark DSCP band and verify there is no error returned
    """
    def runTest(self):
        self.logger.info("Running SimpleMeterModDSCP test")
        self.logger.info("Sending meter_mod request")

        self.logger.info("Delete all meters")
        rc = testutils.delete_all_meters(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        self.logger.info("Insert metermod with DSCP remark band")
        msg = message.meter_mod()
        msg.command = ofp.OFPMC_ADD
        msg.meter_id = 1
        msg.flags = ofp.OFPMF_KBPS
        band1 = meter.meter_band_dscp_remark()
        band1.rate = 1024
        band1.burst_size = 12
        msg.bands.add(band1)
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',msg.show())
        response = self.controller.message_send(msg)

        #Verify meter is inserted
        self.logger.info("Verify meter is inserted")
        msg = message.meter_stats_request()
        msg.meter_id = ofp.OFPM_ALL
        rv, _ = self.controller.transact(msg, timeout= 2)
        self.assertEqual(str(len(rv.stats)), "1", "Switch should return one stats array")

    
tc = SimpleMeterModDSCP()
_RESULT = tc.run()
