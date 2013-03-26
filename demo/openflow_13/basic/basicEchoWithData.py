"""
<title>EchoWithData</title>
<description>
    Test echo response with short string data
    
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

class EchoWithData(SimpleProtocol):
    """
    Test echo response with short string data
    """
    def runTest(self):
        self.logger.info("Running EchoWithData test")
        request = message.echo_request()
        request.data = 'OpenFlow Will Rule The World'
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',request.show())
        response, _ = self.controller.transact(request)
        logMsg('logDebug',"Response from switch:")
        logMsg('logDebug',response.show())
        self.assertEqual(response.header.type, ofp.OFPT_ECHO_REPLY,
                         'response is not echo_reply')
        self.assertEqual(request.header.xid, response.header.xid,
                         'response xid != request xid')
        self.assertEqual(request.data, response.data,
                         'response data does not match request')

    
tc = EchoWithData()
_RESULT = tc.run()
