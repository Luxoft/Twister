"""
<title>PortDown</title>
<description>
    Generate port_mod OFPPC_PORT_DOWN message and send
    
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

class PortDown(SimpleDataPlane):
    """
    Generate port_mod OFPPC_PORT_DOWN message and send
    """
    def runTest(self):

        self.logger.info("Running PortDown test")
        of_ports = self.port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 0, "Not enough ports for test")

        #Clear the switch state
        self.logger.info("Clear the switch state")
        testutils.clear_switch(self,of_ports,self.logger)
        testutils.do_barrier(self.controller)

        #Get hw_addr of port 0
        self.logger.info("Get hw_addr of port 0")
        req = message.port_desc_stats_request()
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',req.show())
        response,pkt = self.controller.transact(req)
        self.assertTrue(response is not None,"No response received for port stats request")
        logMsg('logDebug',"Response from switch:")
        logMsg('logDebug',response.show())

        self.logger.info("Generate port_mod message - port down")
        req = message.port_mod()
        req.port_no = of_ports[0]
        req.hw_addr = response.ports[0].hw_addr
        req.config = ofp.OFPPC_PORT_DOWN
        req.mask = ofp.OFPPC_PORT_DOWN
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',req.show())
        rv = self.controller.message_send(req)

        self.logger.info("Request port desc stats")
        req = message.port_desc_stats_request()
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',req.show())
        response,pkt = self.controller.transact(req)
        self.assertTrue(response is not None,"No response received for port stats request")
        logMsg('logDebug',"Response from switch:")
        logMsg('logDebug',response.show())
        self.assertEqual(ofp.OFPPC_PORT_DOWN, response.ports[0].config, "Config do not match OFPPC_PORT_DOWN")

    
tc = PortDown()
_RESULT = tc.run()
