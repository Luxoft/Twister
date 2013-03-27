"""
<title>ErrorMsg</title>
<description>
    Verify OFPT_ERROR msg is implemented

    When the header in the  request msg
    contains a version field which is not supported by the switch ,
    it generates OFPT_ERROR_msg with Type field OFPET_BAD_REQUEST
    and code field OFPBRC_BAD_VERSION
    
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

class ErrorMsg(SimpleProtocol):

    """
    Verify OFPT_ERROR msg is implemented

    When the header in the  request msg
    contains a version field which is not supported by the switch ,
    it generates OFPT_ERROR_msg with Type field OFPET_BAD_REQUEST
    and code field OFPBRC_BAD_VERSION
    """

    def runTest(self):

        self.logger.info("Running Error Msg test")

        #Send Echo Request
        self.logger.info("Sending a Echo request with a version which is not supported by the switch")
        request=message.echo_request()
        request.header.version=0
        rv=self.controller.message_send(request)
        self.assertTrue(rv is not None,"Unable to send the message")

        self.logger.info("Waiting for a OFPT_ERROR msg on the control plane...")
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ERROR,
                                               timeout=5)
        self.assertTrue(response is not None,
                               'Switch did not reply with error message')
        self.assertTrue(response.type==ofp.OFPHFC_INCOMPATIBLE,
                               'Message field type is not OFPET_BAD_REQUEST')
        self.assertTrue(response.type==ofp.OFPET_HELLO_FAILED,
                               'Message field code is not OFPBRC_BAD_VERSION')

    
tc = ErrorMsg()
_RESULT = tc.run()
