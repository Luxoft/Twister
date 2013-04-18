"""
<title>GetAsyncRequest</title>
<description> Query the switch about what async messages should send to controller
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

class GetAsyncRequest(SimpleProtocol):

    """ Verify get_async_request works"""
    def runTest(self):

        self.logger.info("Running GetAsyncRequest test")

        self.logger.info("Sending Async Request")
        self.logger.info("Expecting a OPPT_GET_ASYNC_REPLY")

        #Send Barrier Request
        request = message.get_async_request()
        logMsg('logDebug',"Request to switch:")
        logMsg('logDebug',request.show())
        (response,pkt) = self.controller.transact(request)
        logMsg('logDebug',"Response from switch:")
        logMsg('logDebug',response.show())
        self.assertEqual(response.header.type, ofp.OFPT_GET_ASYNC_REPLY,'response is not OFPT_GET_ASYNC_REPLY')
    
tc = GetAsyncRequest()
_RESULT = tc.run()
