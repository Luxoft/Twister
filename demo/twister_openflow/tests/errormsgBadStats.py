
from ce_libs import *

try:
    errormsg.config=getOpenflowConfig(globEpName)
    errormsg.errormsg_port_map= pktact.pa_config['port_map']
except:
    print "Error: Invalid configuration for EPNAME: " + str(globEpName)

#class body
class BadStats(basic.SimpleProtocol):
    """
    ofp_stats_request.type not supported.

    When the request type sent by the controller is not supported by switch 
    (e.g some switch do not support queue stats request) , 
    the switch generates OFPT_ERROR msg with type Field OFPET_BAD_REQUEST 
    and code field OFPBRC_BAD_STAT
    """
    def runTest(self):
        request = message.queue_stats_request()
        request.port_no  = ofp.OFPP_ALL
        request.queue_id = ofp.OFPQ_ALL
        rv=self.controller.message_send(request)
        
        self.assertTrue(rv==0,"Unable to send the message")
         
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ERROR,         
                                               timeout=5)
        self.assertTrue(response is not None, 
                               'Switch did not replay with error messge')
        self.assertTrue(response.type==ofp.OFPET_BAD_REQUEST, 
                               'Message field type is not OFPET_BAD_REQUEST') 
        self.assertTrue(response.type==ofp.OFPBRC_BAD_STAT, 
                               'Message field code is not OFPBRC_BAD_STAT')


tc = BadStats()
_RESULT = tc.run()
