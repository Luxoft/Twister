
from ce_libs import *

try:
    errormsg.config = getOpenflowConfig(globEpName)
    errormsg.errormsg_port_map = pktact.pa_config['port_map']
except:
    print 'Error: Invalid configuration for EPNAME: ' + str(globEpName)

class BufferUnknown(basic.SimpleProtocol):
    """
    Specified buffer does not exist. 

    When the buffer specified by the controller does not exit , the switch
    replies back with OFPT_ERROR msg with type fiels OFPET_BAD_REQUEST

    """
    def runTest(self):

        pkt=simple_tcp_packet()
#        act=action.action_output()
        of_ports = errormsg_port_map.keys()
        self.assertTrue(len(of_ports)>1,"meeds 2 ports for testing")
        of_ports.sort()
        request = flow_msg_create(self, pkt, ing_port=of_port[0], egr_port=of_ports[1])
        request.buffer_id=-1

        print request.show()

        rv = self.controller.message_send(request)
        self.assertTrue(rv==0,"Unable to send the message")

        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ERROR,
                                               timeout=5)
        print response.show()
        self.assertTrue(response is not None,
                                'Switch did not replay with error messge')
        self.assertTrue(response.type==ofp.OFPET_BAD_REQUEST,
                               'Message field type is not OFPET_BAD_REQUEST')
        self.assertTrue(response.code==ofp.OFPBRC_BUFFER_UNKNOWN,
                               'Message field code is not OFPBRC_BUFFER_UNKNOWN')


tc = BufferUnknown()
_RESULT = tc.run()
