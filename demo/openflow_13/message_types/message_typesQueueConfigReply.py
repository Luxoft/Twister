"""
<title>QueueConfigReply</title>
<description>Verify Queue Configuration Reply message body 
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

class QueueConfigReply(SimpleProtocol):

    """Verify Queue Configuration Reply message body """

    def runTest(self):

        self.logger.info("Running QueueConfigRequest")

        of_ports = self.port_map.keys()
        of_ports.sort()

        self.logger.info("Sending Queue Config Request ...")
        request = message.queue_get_config_request()
        request.port = of_ports[0]
        response, pkt = self.controller.transact(request)
        self.assertTrue(response is not None,
                        "Did not get reply ")
        self.assertTrue(response.header.type == ofp.OFPT_QUEUE_GET_CONFIG_REPLY, "Reply is not Queue Config Reply")

        #Verify Reply Body
        self.assertEqual(response.header.xid, request.header.xid , "Transaction Id in reply is not same as request")
        self.assertEqual(response.port,request.port , "Port queried does not match ")
        queues = []
        queues = response.queues
        self.logger.info ("Queues Configured for port " + str(of_ports[0]) + str(queues))

    
tc = QueueConfigReply()
_RESULT = tc.run()
