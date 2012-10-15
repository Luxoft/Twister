
from ce_libs import *

try:
    errormsg.config=getOpenflowConfig(globEpName)
    errormsg.errormsg_port_map= pktact.pa_config['port_map']
except:
    print "Error: Invalid configuration for EPNAME: " + str(globEpName)

#class body
class BadOutPort(basic.SimpleProtocol):   
    """
    Problem validating output action.
    Generate a flow_mod msg .Add an action OFPAT_OUTPUT such that out-put port is an invalid port . 
    Verify switch responds back with an error msg

    """
    def runTest(self):  
        
        pkt=simple_tcp_packet()
        act=action.action_output()        
        request = flow_msg_create(self, pkt, ing_port=1, egr_port=-1)
        
        rv = self.controller.message_send(request)
        self.assertTrue(rv==0,"Unable to send the message")
        
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ERROR,         
                                               timeout=5)
        self.assertTrue(response is not None, 
                                'Switch did not replay with error messge')                                       
        self.assertTrue(response.type==ofp.OFPET_BAD_ACTION, 
                               'Message field type is not OFPET_BAD_ACTION') 
        self.assertTrue(response.code==ofp.OFPET_OUT_PORT, 
                               'Message field code is not OFPET_OUT_PORT')


tc = BadOutPort()
_RESULT = tc.run()
