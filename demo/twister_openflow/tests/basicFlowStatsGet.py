
from ce_libs import *

try:
    basic.basic_config=getOpenflowConfig(globEpName)
    basic.basic_port_map=basic.basic_config['port_map']
except:
    print "Error: Invalid configuration for EPNAME: " + str(globEpName)

class FlowStatsGet(SimpleProtocol):
    """
    Get stats

    Simply verify stats get transaction
    """
    def runTest(self):
        basic_logger.info("Running StatsGet")
        basic_logger.info("Inserting trial flow")
        request = message.flow_mod()
        request.match.wildcards = ofp.OFPFW_ALL
        request.buffer_id = 0xffffffff
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, "Failed to insert test flow")

        basic_logger.info("Sending flow request")
        request = message.flow_stats_request()
        request.out_port = ofp.OFPP_NONE
        request.table_id = 0xff
        request.match.wildcards = 0 # ofp.OFPFW_ALL
        response, pkt = self.controller.transact(request, timeout=2)
        self.assertTrue(response is not None, "Did not get response")
        basic_logger.debug(response.show())


tc = FlowStatsGet()
_RESULT = tc.run()
