"""
<title>BadRequestBadLength</title>
<description>When the length field in the header of the stats request is wrong ,
    switch generates an OFPT_ERROR msg with type field OFPET BAD_REQUEST
    and code field OFPBRC_BAD_LEN
    
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

class BadRequestBadLength(SimpleProtocol):

    """When the length field in the header of the stats request is wrong ,
    switch generates an OFPT_ERROR msg with type field OFPET BAD_REQUEST
    and code field OFPBRC_BAD_LEN
    """
    def runTest(self):

        self.logger.info("Running BadRequestBadLength test")
        #In Message module at pack time the length is computed
        #avoid this by using cstruct module
        self.logger.info("Sending stats_request message..")
        stats_request = ofp.ofp_port_stats_request()
        header=ofp.ofp_header()
        header.type = ofp.OFPMP_PORT_STATS
        # normal the header length is 12bytes changed it to 18bytes
        header.length=13;
        packed=header.pack()+stats_request.pack()
        rv=self.controller.message_send(packed)
        self.assertTrue(rv != -1,"Unable to send the message")
        self.logger.info("Waiting for OFPT_ERROR message..")
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ERROR,
                                               timeout=5)

        self.assertTrue(response is not None,
                               'Switch did not reply with expected error messge')
        logMsg('logDebug',"Response from switch:")
        logMsg('logDebug',response.show())
        self.assertTrue(response.type==ofp.OFPET_BAD_REQUEST,
                               'Error type is not OFPET_BAD_REQUEST')
        self.assertTrue(response.code==ofp.OFPBRC_BAD_LEN,
                               'Error code is not OFPBRC_BAD_LEN')

    
tc = BadRequestBadLength()
_RESULT = tc.run()
