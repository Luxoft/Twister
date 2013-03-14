
from basicSimpleProtocol import *

class SimpleDataPlane(SimpleProtocol):
    """
    Root class that sets up the controller and dataplane
    """
    def init(self):
        SimpleProtocol.init(self)
        self.dataplane = dataplane.DataPlane()

        for of_port, ifname in self.port_map.items():
            self.dataplane.port_add(ifname, of_port)

    def cleanUp(self):
        self.logger.info("Cleanup for simple dataplane test")
        SimpleProtocol.cleanUp(self)
        self.dataplane.kill(join_threads=self.clean_shutdown)
        self.logger.info("Cleanup done")

    def runTest(self):
        self.assertTrue(self.controller.switch_socket is not None,
                        str(self) + 'No connection to switch')
        # self.dataplane.show()
        # Would like an assert that checks the data plane

tc=SimpleDataPlane()
_RESULT=tc.run()        
