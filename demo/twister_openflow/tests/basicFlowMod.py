
from ce_libs import *

try:
    basic.basic_config=getOpenflowConfig(globEpName)
    basic.basic_port_map=basic.basic_config['port_map']
except:
    print "Error: Invalid configuration for EPNAME: " + str(globEpName)

class FlowMod(SimpleProtocol):
    """
    Insert a flow

    Simple verification of a flow mod transaction
    """

    def runTest(self):
        basic_logger.info("Running " + str(self))
        request = message.flow_mod()
        request.match.wildcards = ofp.OFPFW_ALL
        request.buffer_id = 0xffffffff
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, "Error installing flow mod")


tc = FlowMod()
_RESULT = tc.run()
