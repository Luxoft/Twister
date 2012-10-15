
from ce_libs import *

try:
    basic.basic_config=getOpenflowConfig(globEpName)
    basic.basic_port_map=basic.basic_config['port_map']
except:
    print "Error: Invalid configuration for EPNAME: " + str(globEpName)

class SimpleDataPlane(SimpleProtocol):
    """
    Root class that sets up the controller and dataplane
    """
    def setUp(self):
        SimpleProtocol.setUp(self)
        self.dataplane = dataplane.DataPlane()
        for of_port, ifname in basic_port_map.items():
            self.dataplane.port_add(ifname, of_port)

    def tearDown(self):
        basic_logger.info("Teardown for simple dataplane test")
        SimpleProtocol.tearDown(self)
        self.dataplane.kill(join_threads=self.clean_shutdown)
        basic_logger.info("Teardown done")

    def runTest(self):
        self.assertTrue(self.controller.switch_socket is not None,
                        str(self) + 'No connection to switch')


tc = SimpleDataPlane()
_RESULT = tc.run()
