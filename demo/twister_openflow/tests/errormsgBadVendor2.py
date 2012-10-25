
from ce_libs import *

try:
    errormsg.config = getOpenflowConfig(globEpName)
    errormsg.errormsg_port_map = pktact.pa_config['port_map']
except:
    print 'Error: Invalid configuration for EPNAME: ' + str(globEpName)

class BadVendor2(basic.SimpleProtocol):
    """
    Unknown vendor id specified. 
    If a switch does not understand a vendor extension, it must send an OFPT_ERROR
    message with a OFPBRC_BAD_VENDOR error code and OFPET_BAD_REQUEST error
    type.
    """
    
    def runTest(self):        
        request = message.vendor()
        response, pkt = self.controller.transact(request, timeout=2)        
                
        
        rv = self.controller.message_send(request)
        self.assertTrue(rv==0,"Unable to send the message")
        
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ERROR,         
                                               timeout=5)
        self.assertTrue(response is not None, 
                                'Switch did not replay with error messge')
        self.assertTrue(response.type==ofp.OFPET_BAD_REQUEST, 
                               'Message field type is not OFPET_BAD_REQUEST') 
        self.assertTrue(response.code==ofp.OFPBAC_BAD_VENDOR, 
                               'Message field code is not OFPET_BAD_VENDOR')        


tc = BadVendor2()
_RESULT = tc.run()
