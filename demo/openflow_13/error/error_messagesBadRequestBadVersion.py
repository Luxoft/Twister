"""
<title>BadRequestBadVersion</title>
<description>When the header in the request msg
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

class BadRequestBadVersion(SimpleProtocol):
    """When the header in the request msg
    contains a version field which is not supported by the switch ,
    it generates OFPT_ERROR_msg with Type field OFPET_BAD_REQUEST
    and code field OFPBRC_BAD_VERSION
    """

    def runTest(self):

        self.logger.info("Running BadRequestBadVersion Test")

        #Send a flow_stats request , with incorrect version
        self.logger.info("Sending flow_mod request.. ")
        request=message.flow_stats_request()
        request.table_id = ofp.OFPTT_ALL
        request.out_port = ofp.OFPP_ANY
        request.out_group = ofp.OFPG_ANY
        request.header.version=0
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',request.show())
        rv = self.controller.message_send(request)

        self.logger.info("Waiting for OFPT_ERROR message..")
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ERROR,
                                               timeout=5)
        self.assertTrue(response is not None,
                               'Switch did not reply with error message')
        logMsg('logDebug',"Response from switch:")
        logMsg('logDebug',response.show())
        self.assertTrue(response.type==ofp.OFPET_BAD_REQUEST,
                               'Error type is not OFPET_BAD_REQUEST')
        self.assertTrue(response.code==ofp.OFPBRC_BAD_VERSION,
                               'Error code is not OFPBRC_BAD_VERSION')

    
tc = BadRequestBadVersion()
_RESULT = tc.run()
