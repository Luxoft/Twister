"""
<title>PortModPacketIn</title>
<description>
    Modify the behavior of physical port using Port Modification Messages
    Change OFPPC_NO_PACKET_IN flag and verify change took place with Features Request
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

class PortModPacketIn(SimpleDataPlane):
    """
    Modify the behavior of physical port using Port Modification Messages
    Change OFPPC_NO_PACKET_IN flag and verify change took place with Features Request"""

    def runTest(self):

        self.logger.info("Running PortModPacketIn Test")
        of_ports = self.port_map.keys()
        of_ports.sort()

        #Retrieve Port Configuration
        self.logger.info("Sends Features Request and retrieve Port Configuration from reply")
        (hw_addr, port_config, advert) = \
            testutils.port_config_get(self.controller, of_ports[0], self.logger)
        self.assertTrue(port_config is not None, "Did not get port config")
        logMsg('logDebug',"No flood bit port " + str(of_ports[0]) + " is now " +
                           str(port_config & ofp.OFPPC_NO_PACKET_IN))

        #Modify Port Configuration
        self.logger.info("Modify Port Configuration using Port Modification Message:OFPT_PORT_MOD")
        rv = testutils.port_config_set(self.controller, of_ports[0],
                             port_config ^ ofp.OFPPC_NO_PACKET_IN, ofp.OFPPC_NO_PACKET_IN, self.logger)
        self.assertTrue(rv != -1, "Error sending port mod")

        # Verify change took place with features request
        self.logger.info("Verify the change and then set it back")
        (hw_addr, port_config2, advert) = testutils.port_config_get(self.controller, of_ports[0], self.logger)

        logMsg('logDebug',"No flood bit port " + str(of_ports[0]) + " is now " +
                           str(port_config2 & ofp.OFPPC_NO_PACKET_IN))

        self.assertTrue(port_config2 is not None, "Did not get port config2")
        self.assertTrue(port_config2 & ofp.OFPPC_NO_PACKET_IN !=
                        port_config & ofp.OFPPC_NO_PACKET_IN,
                        "Bit change did not take")
        # Set it back
        rv = testutils.port_config_set(self.controller, of_ports[0],port_config,
                             ofp.OFPPC_NO_PACKET_IN, self.logger)
        self.assertTrue(rv != -1, "Error sending port mod")

    
tc = PortModPacketIn()
_RESULT = tc.run()
