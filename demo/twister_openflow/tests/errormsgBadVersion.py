
from ce_libs import *

try:
    errormsg.config=getOpenflowConfig(globEpName)
    errormsg.errormsg_port_map= pktact.pa_config['port_map']
except:
    print "Error: Invalid configuration for EPNAME: " + str(globEpName)

#class body
class BadVersion(basic.SimpleProtocol):
    """
    When the header in the  request msg  
    contains a version field which is not supported by the switch , 
    it generates OFPT_ERROR_msg with Type field OFPET_BAD_REQUEST 
    and code field OFPBRC_BAD_VERSION
    """
    
    def runTest(self):
    
        request=message.echo_request();
        request.header.version=0        
        rv=self.controller.message_send(request)
        
        self.assertTrue(rv==0,"Unable to send the message")
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ERROR,         
                                               timeout=5)
        self.assertTrue(response is not None, 
                               'Switch did not replay with error message')
        self.assertTrue(response.type==ofp.OFPET_BAD_REQUEST, 
                               'Message field type is not OFPET_BAD_REQUEST') 
        self.assertTrue(response.type==ofp.OFPET_BAD_REQUEST, 
                               'Message field type is not OFPBRC_BAD_VERSION')


tc = BadVersion()
_RESULT = tc.run()
