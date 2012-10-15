
from ce_libs import *

try:
    errormsg.config=getOpenflowConfig(globEpName)
    errormsg.errormsg_port_map= pktact.pa_config['port_map']
except:
    print "Error: Invalid configuration for EPNAME: " + str(globEpName)

#class body
class BadType1(basic.SimpleProtocol):
    """
    When the controller sends a request message which 
    is not understood by the switch , it generates error 
    a OFPT_ERROR msg with Type Field OFPET_BAD_REQUEST
    Added OFPT_BAD_TYPE in cstruct.py
    """
    def runTest(self):
    
        msg=message.echo_request();
        msg.pack();     
        #use cstruct module for header to use pack with bool argument
        header=ofp.ofp_header() 
        header.length=msg.header.length;
        #change message header type to non existent type
        header.type = 45       
        packed = header.pack(False)        
        
        rv=self.controller.message_send(packed)
        
        self.assertTrue(rv==0,"Unable to send the message")
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ERROR,         
                                               timeout=5)
        self.assertTrue(response is not None, 
                               'Switch did not replay with error message')
        self.assertTrue(response.type==ofp.OFPET_BAD_REQUEST, 
                               'Message field type is not OFPET_BAD_REQUEST') 
        self.assertTrue(response.type==ofp.OFPET_BAD_REQUEST, 
                               'Message field type is not OFPBRC_BAD_TYPE')


tc = BadType1()
_RESULT = tc.run()
