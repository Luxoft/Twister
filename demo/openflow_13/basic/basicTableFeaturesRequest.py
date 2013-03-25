"""
<title>TableFeaturesRequest</title>
<description>Check basic table features request is implemented
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

class TableFeaturesRequest(SimpleProtocol):

    """Check basic table features request is implemented"""

    def runTest(self):

        self.logger.info("Running table features request test ")

        request = message.table_features_request()
        request.table_id = 1
        logMsg('logDebug',"Request to switch:")
        logMsg('logDebug',request.show())
        rv, _ = self.controller.transact(request, timeout=5)
        self.assertTrue(rv is not None, "Switch did not reply")
        self.assertTrue(rv.type == ofp.OFPMP_TABLE_FEATURES, "Reply type not TABLE_FEATURES")

    
tc = TableFeaturesRequest()
_RESULT = tc.run()
