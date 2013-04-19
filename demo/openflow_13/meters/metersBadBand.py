"""
<title>BadBand</title>
<description>
    Insert meter_mod with bad band type set, switch must return error
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

class BadBand(SimpleDataPlane):
    """
    Insert meter_mod with bad band type, switch must return error
    """
    def runTest(self):
        self.logger.info("Running Delete test")

        self.logger.info("Insert metermod with bad band type")
        msg = message.meter_mod()
        msg.command = ofp.OFPMC_ADD
        msg.meter_id = 1
	band1 = meter.meter_band_drop()
	band1.type = 5
        band1.rate = 2
        band1.burst_size = 2
        msg.bands.add(band1)
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',msg.show())
        rv = self.controller.message_send(msg)
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ERROR,
                                               timeout=5)
	self.assertTrue(response is not None, 'Switch did not reply')
        self.assertTrue(response.type==ofp.OFPET_METER_MOD_FAILED,
                               'Error type is not OFPET_METER_MOD_FAILED')
        self.assertTrue(response.code==ofp.OFPMMFC_BAD_BAND,
                               'Error code is not OFPMMFC_BAD_BAND')

tc = BadBand()
_RESULT = tc.run()
