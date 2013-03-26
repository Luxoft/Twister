"""
<title>PortConfigMod</title>
<description>
    Modify a bit in port config and verify changed
    Get the switch configuration, modify the port configuration
    and write it back; get the config again and verify changed.
    Then set it back to the way it was.
    
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

class PortConfigMod(SimpleProtocol):
    """
    Modify a bit in port config and verify changed
    Get the switch configuration, modify the port configuration
    and write it back; get the config again and verify changed.
    Then set it back to the way it was.
    """

    def runTest(self):
        self.logger.info("Running " + str(self))
        for of_port, _ in self.port_map.items(): # Grab first port
            break

        (_, config, _) = \
            testutils.port_config_get(self.controller, of_port, self.logger)
        self.assertTrue(config is not None, "Did not get port config")

        logMsg('logDebug',"No flood bit port " + str(of_port) + " is now " + str(config & ofp.OFPPC_NO_PACKET_IN))

        rv = testutils.port_config_set(self.controller, of_port,
                             config ^ ofp.OFPPC_NO_PACKET_IN, ofp.OFPPC_NO_PACKET_IN,
                             self.logger)
        self.assertTrue(rv != -1, "Error sending port mod")

        # Verify change took place with same feature request
        (_, config2, _) = \
            testutils.port_config_get(self.controller, of_port, self.logger)
        self.assertTrue(config2 is not None, "Did not get port config2")
        logMsg('logDebug',"No packet_in bit port " + str(of_port) + " is now " +
                            str(config2 & ofp.OFPPC_NO_PACKET_IN))
        self.assertTrue(config2 & ofp.OFPPC_NO_PACKET_IN !=
                        config & ofp.OFPPC_NO_PACKET_IN,
                        "Bit change did not take")
        # Set it back
        rv = testutils.port_config_set(self.controller, of_port, config,
                             ofp.OFPPC_NO_PACKET_IN, self.logger)
        self.assertTrue(rv != -1, "Error sending port mod")

    
tc = PortConfigMod()
_RESULT = tc.run()
