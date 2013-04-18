"""
<title>BadPortModPort</title>
<description>
    Generate port_mod with invalid port, switch must generate error
    
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

class BadPortModPort(SimpleDataPlane):
    """
    Generate port_mod with invalid port, switch must generate error
    """
    def runTest(self):

        self.logger.info("Running BadPortModPort test")
        of_ports = self.port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 0, "Not enough ports for test")

        self.logger.info("Generate port_mod message - no fwd")
        req = message.port_mod()
        req.port_no = ofp.OFPP_MAX 
        req.config = ofp.OFPPC_NO_FWD
        req.mask = ofp.OFPPC_NO_FWD
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',req.show())
        rv = self.controller.message_send(req)
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ERROR,
                                               timeout=5)
	self.assertTrue(response is not None, 'Switch did not reply')
        self.assertTrue(response.type==ofp.OFPET_PORT_MOD_FAILED,
                               'Error type is not OFPET_PORT_MOD_FAILED')
        self.assertTrue(response.code==ofp.OFPPMFC_BAD_PORT,
                               'Error code is not OFPPMFC_BAD_PORT')
	
    
tc = BadPortModPort()
_RESULT = tc.run()
