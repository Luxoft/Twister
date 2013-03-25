"""
<title>BarrierRequestReply</title>
<description> Check basic Barrier request is implemented
    a) Send OFPT_BARRIER_REQUEST
    c) Verify OFPT_BARRIER_REPLY is recieved
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

class BarrierRequestReply(SimpleProtocol):

    """ Check basic Barrier request is implemented
    a) Send OFPT_BARRIER_REQUEST
    c) Verify OFPT_BARRIER_REPLY is recieved"""

    def runTest(self):

        self.logger.info("Running Barrier_Request_Reply test")

        self.logger.info("Sending Barrier Request")
        self.logger.info("Expecting a Barrier Reply with same xid")

        #Send Barrier Request
        request = message.barrier_request()
        logMsg('logDebug',"Request to switch:")
        logMsg('logDebug',request.show())
        (response,pkt) = self.controller.transact(request)
        logMsg('logDebug',"Response from switch:")
        logMsg('logDebug',response.show())
        self.assertEqual(response.header.type, ofp.OFPT_BARRIER_REPLY,'response is not barrier_reply')
        self.assertEqual(request.header.xid, response.header.xid,
                         'response xid != request xid')

    
tc = BarrierRequestReply()
_RESULT = tc.run()
