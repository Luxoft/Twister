"""
<title>DeleteNonExisting</title>
<description>
    When trying to delete a non existing meter, switch do not have to return anything
    
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

class DeleteNonExisting(SimpleDataPlane):
    """
    When trying to delete a non existing meter, switch do not have to return anything
    """
    def runTest(self):
        self.logger.info("Running DeleteNonExisting test")

        #Delete all meters
        self.logger.info("Delete all meters")
        rc = testutils.delete_all_meters(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all meters")

        #Insert meter_mod
        self.logger.info("Try to delete a non existing meter, switch must not return error")
        msg = message.meter_mod()
        msg.command = ofp.OFPMC_DELETE
        msg.meter_id = 1
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',msg.show())
        rv = self.controller.message_send(msg)
        response,_  = self.controller.poll(ofp.OFPT_ERROR, 2)
        
        self.assertTrue(response is None, "Switch not reply")
       

    
tc = DeleteNonExisting()
_RESULT = tc.run()
