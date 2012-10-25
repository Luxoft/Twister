
from ce_libs import *

try:
    pktact.pa_config = getOpenflowConfig(globEpName)
    pktact.pa_port_map = pktact.pa_config['port_map']
except:
    print 'Error: Invalid configuration for EPNAME: ' + str(globEpName)

class StripVLANTag(BaseMatchCase):
    """
    Strip the VLAN tag from a tagged packet
    """
    def runTest(self):
        old_vid = 2
        sup_acts = supported_actions_get(self)
        if not (sup_acts & 1 << ofp.OFPAT_STRIP_VLAN):
            skip_message_emit(self, "Strip VLAN tag test")
            return

        len_w_vid = 104
        len = 100
        pkt = simple_tcp_packet(pktlen=len_w_vid, dl_vlan_enable=True,
                                dl_vlan=old_vid)
        exp_pkt = simple_tcp_packet(pktlen=len)
        vid_act = action.action_strip_vlan()

        flow_match_test(self, pa_port_map, pkt=pkt, exp_pkt=exp_pkt,
                        action_list=[vid_act])


tc = StripVLANTag()
_RESULT = tc.run()
