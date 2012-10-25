
from ce_libs import *

try:
    basic.basic_config = getOpenflowConfig(EP)
    basic.basic_port_map = basic.basic_config['port_map']
except:
    print 'Error: Invalid configuration for EPNAME: ' + str(EP)

class TableStatsGet(SimpleProtocol):
    """
    Get table stats

    Simply verify table stats get transaction
    """
    def runTest(self):
        basic_logger.info("Running TableStatsGet")
        basic_logger.info("Inserting trial flow")
        request = message.flow_mod()
        request.match.wildcards = ofp.OFPFW_ALL
        request.buffer_id = 0xffffffff
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, "Failed to insert test flow")

        basic_logger.info("Sending table stats request")
        request = message.table_stats_request()
        response, pkt = self.controller.transact(request, timeout=2)
        self.assertTrue(response is not None, "Did not get response")
        basic_logger.debug(response.show())


tc = TableStatsGet()
_RESULT = tc.run()
