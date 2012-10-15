
from ce_libs import *

try:
    basic.basic_config=getOpenflowConfig(globEpName)
    basic.basic_port_map=basic.basic_config['port_map']
except:
    print "Error: Invalid configuration for EPNAME: " + str(globEpName)

class PortConfigMod(SimpleProtocol):
    """
    Modify a bit in port config and verify changed

    Get the switch configuration, modify the port configuration
    and write it back; get the config again and verify changed.
    Then set it back to the way it was.
    """

    def runTest(self):
        basic_logger.info("Running " + str(self))
        for of_port, ifname in basic_port_map.items(): # Grab first port
            break

        (hw_addr, config, advert) = \
            port_config_get(self.controller, of_port, basic_logger)
        self.assertTrue(config is not None, "Did not get port config")

        basic_logger.debug("No flood bit port " + str(of_port) + " is now " +
                           str(config & ofp.OFPPC_NO_FLOOD))

        rv = port_config_set(self.controller, of_port,
                             config ^ ofp.OFPPC_NO_FLOOD, ofp.OFPPC_NO_FLOOD,
                             basic_logger)
        self.assertTrue(rv != -1, "Error sending port mod")

        # Verify change took place with same feature request
        (hw_addr, config2, advert) = \
            port_config_get(self.controller, of_port, basic_logger)
        basic_logger.debug("No flood bit port " + str(of_port) + " is now " +
                           str(config2 & ofp.OFPPC_NO_FLOOD))
        self.assertTrue(config2 is not None, "Did not get port config2")
        self.assertTrue(config2 & ofp.OFPPC_NO_FLOOD !=
                        config & ofp.OFPPC_NO_FLOOD,
                        "Bit change did not take")
        # Set it back
        rv = port_config_set(self.controller, of_port, config,
                             ofp.OFPPC_NO_FLOOD, basic_logger)
        self.assertTrue(rv != -1, "Error sending port mod")


tc = PortConfigMod()
_RESULT = tc.run()
