"""
<title>FlowMod</title>
<description>
    Insert a flow
    Simple verification of a flow mod transaction
    
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

class FlowMod(SimpleProtocol):
    """
    Insert a flow
    Simple verification of a flow mod transaction
    """

    def runTest(self):
        self.logger.info("Running simple flow_mod test")
        request = message.flow_mod()
        request.buffer_id = 0xffffffff
        logMsg('logDebug',"Request to switch:")
        logMsg('logDebug',request.show())
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, "Error installing flow mod")

    
tc = FlowMod()
_RESULT = tc.run()
