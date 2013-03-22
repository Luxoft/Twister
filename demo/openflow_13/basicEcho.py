
try:
    if('TWISTER_ENV' in globals()):
        from ce_libs.openflow.of_13.openflow_base import *
        testbed=currentTB
        from ce_libs import ra_proxy
        ra_service=ra_proxy    
except:
    raise


class Echo(SimpleProtocol):
    """
    Test echo response with no data
    """
    def runTest(self):
        testutils.do_echo_request_reply_test(self, self.controller)
        logMsg('logDebug',"message")
        
tc=Echo(testbed=currentTB,ra_proxy=ra_service)
_RESULT=tc.run()            
