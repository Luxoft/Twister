
from ce_libs import *

try:
    basic.basic_config = getOpenflowConfig(EP)
    basic.basic_port_map = basic.basic_config['port_map']
except:
    print 'Error: Invalid configuration for EPNAME: ' + str(EP)

class EchoWithData(SimpleProtocol):
    """
    Test echo response with short string data
    """
    def runTest(self):
        request = message.echo_request()
        request.data = 'OpenFlow Will Rule The World'
        response, pkt = self.controller.transact(request)
        self.assertEqual(response.header.type, ofp.OFPT_ECHO_REPLY,
                         'response is not echo_reply')
        self.assertEqual(request.header.xid, response.header.xid,
                         'response xid != request xid')
        self.assertEqual(request.data, response.data,
                         'response data does not match request')


tc = EchoWithData()
_RESULT = tc.run()
