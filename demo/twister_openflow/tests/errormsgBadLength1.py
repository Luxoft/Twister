
from ce_libs import *

try:
    errormsg.config=getOpenflowConfig(globEpName)
    errormsg.errormsg_port_map= pktact.pa_config['port_map']
except:
    print "Error: Invalid configuration for EPNAME: " + str(globEpName)

#class body
class BadLength1(basic.SimpleProtocol):    
    """
    Wrong request length for type. 
    
    When the length field in the header of the stats request is wrong , 
    switch generates an OFPT_ERROR msg with type field OFPET BAD_REQUEST 
    and code field OFPBRC_BAD_LEN
    """
    def runTest(self):
        #in the module message at pack time the length is computed
        #avoid this by using cstruct module
        stats_request = ofp.ofp_stats_request()
        header=ofp.ofp_header() 
        header.type = ofp.OFPT_STATS_REQUEST
        # normal the header length is 12 change it to 18
        header.length=18;
        packed=header.pack()+stats_request.pack()
        rv=self.controller.message_send(packed)
        self.assertTrue(rv==0,"Unable to send the message")
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ERROR,         
                                               timeout=5)
        self.assertTrue(response is not None, 
                               'Switch did not replay with error messge')
        self.assertTrue(response.type==ofp.OFPET_BAD_REQUEST, 
                               'Message field type is not OFPET_BAD_REQUEST') 
        self.assertTrue(response.type==ofp.OFPBRC_BAD_LEN, 
                               'Message field code is not OFPBRC_BAD_LEN')    


tc = BadLength1()
_RESULT = tc.run()
