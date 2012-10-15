
from ce_libs import *

try:
    pktact.pa_config=getOpenflowConfig(globEpName)
    pktact.pa_port_map= pktact.pa_config['port_map']
except:
    print "Error: Invalid configuration for EPNAME: " + str(globEpName)

class AddVLANTag(BaseMatchCase):
    """
    Add a VLAN tag to an untagged packet
    """
    def runTest(self):
        new_vid = 2
        sup_acts = supported_actions_get(self)
        if not(sup_acts & 1<<ofp.OFPAT_SET_VLAN_VID):
            skip_message_emit(self, "Add VLAN tag test")
            return

        len = 100
        len_w_vid = 104
        pkt = simple_tcp_packet(pktlen=len)
        exp_pkt = simple_tcp_packet(pktlen=len_w_vid, dl_vlan_enable=True,
                                    dl_vlan=new_vid)
        vid_act = action.action_set_vlan_vid()
        vid_act.vlan_vid = new_vid

        flow_match_test(self, pa_port_map, pkt=pkt,
                        exp_pkt=exp_pkt, action_list=[vid_act])


tc = AddVLANTag()
_RESULT = tc.run()
