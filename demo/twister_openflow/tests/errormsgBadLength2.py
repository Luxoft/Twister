
from ce_libs import *

try:
    errormsg.config = getOpenflowConfig(globEpName)
    errormsg.errormsg_port_map = pktact.pa_config['port_map']
except:
    print 'Error: Invalid configuration for EPNAME: ' + str(globEpName)

class BadLength2(basic.SimpleProtocol):
    """
    Length problem in actions.

    When the length field in the action header specified by the controller is
    wrong , the switch replies back with an OFPT_ERROR msg with Type Field
    OFPBAC_BAD_LEN

    """
    def runTest(self):

        pkt=simple_tcp_packet()
#        act=action.action_output()
        of_ports = errormsg_port_map.keys()
        self.assertTrue(len(of_ports)>1,"meeds 2 ports for testing")
        of_ports.sort()
        request = flow_msg_create(self, pkt, ing_port=of_ports[0], egr_port=of_ports[1])
#        request.actions.actions[0].type=67
        request.actions.actions[0].len=100

        print request.show()

        rv = self.controller.message_send(request)
        self.assertTrue(rv==0,"Unable to send the message")

        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ERROR,
                                               timeout=5)

        self.assertTrue(response is not None,
                                'Switch did not replay with error messge')      
        self.assertTrue(response.type==ofp.OFPET_BAD_ACTION,
                               'Message field type is not OFPET_BAD_ACTION')
        self.assertTrue(response.code==ofp.OFPBAC_BAD_LEN,
                               'Message field code is not OFPBAC_BAD_LEN')


tc = BadLength2()
_RESULT = tc.run()
