"""
<title>SetConfigRequest</title>
<description>Verify OFPT_SET_CONFIG is implemented
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

class SetConfigRequest(SimpleProtocol):

    """Verify OFPT_SET_CONFIG is implemented"""

    def runTest(self):

        self.logger.info("Running SetConfigRequest Test")
        of_ports = self.port_map.keys()
        of_ports.sort()

        #Send get_config_request -- retrive miss_send_len field
        self.logger.info("Sending Get Config Request ")
        request = message.get_config_request()
        (reply, pkt) = self.controller.transact(request)
        self.assertTrue(reply is not None, "Failed to get any reply")
        self.assertEqual(reply.header.type, ofp.OFPT_GET_CONFIG_REPLY,'Response is not Config Reply')

        miss_send_len = 0
        miss_send_len = reply.miss_send_len
        old_flags = 0
        old_flags = reply.flags

        #Send set_config_request --- set a different miss_sen_len field and flag
        self.logger.info("Sending Set Config Request...")
        req = message.set_config()

        if miss_send_len < 65400 :# Max miss_send len is 65535
            req.miss_send_len = miss_send_len + 100
            new_miss_send_len = req.miss_send_len
        else :
            req.miss_send_len = miss_send_len - 100
            new_miss_send_len = req.miss_send_len

        if old_flags > 0 :
            req.flags = old_flags-1
            new_flags = req.flags
        else :
            req.flags = old_flags+1
            new_flags = req.flags

        rv=self.controller.message_send(req)
        self.assertTrue(rv is not None,"Unable to send the message")

        #Send get_config_request -- verify change came into effect
        self.logger.info("Sending Get Config Request...")
        request = message.get_config_request()

        (rep, pkt) = self.controller.transact(request)
        self.assertTrue(rep is not None, "Failed to get any reply")
        self.assertEqual(rep.header.type, ofp.OFPT_GET_CONFIG_REPLY,'Response is not Config Reply')
        self.assertEqual(rep.miss_send_len,new_miss_send_len, "miss_send_len configuration parameter could not be set")
        self.assertEqual(rep.flags,new_flags, "frag flags could not be set")

    
tc = SetConfigRequest()
_RESULT = tc.run()
