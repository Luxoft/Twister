"""
<title>TableModConfig</title>
<description> Simple table modification
    Mostly to make sure the switch correctly responds to these messages.
    More complicated tests in the multi-tables.py tests
    
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

class TableModConfig(SimpleProtocol):
    """ Simple table modification
    Mostly to make sure the switch correctly responds to these messages.
    More complicated tests in the multi-tables.py tests
    """
    def runTest(self):
        self.logger.info("Running " + str(self))
        table_mod = message.table_mod()
        table_mod.table_id = 0 # first table should always exist
        table_mod.config = ofp.OFPTFPT_NEXT_TABLES_MISS
        logMsg('logDebug',"Request to switch:")
        logMsg('logDebug',table_mod.show())
        rv = self.controller.message_send(table_mod)
        self.assertTrue(rv != -1, "Error sending table_mod")
        testutils.do_echo_request_reply_test(self, self.controller)

    
tc = TableModConfig()
_RESULT = tc.run()
