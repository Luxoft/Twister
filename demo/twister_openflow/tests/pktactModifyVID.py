
from ce_libs import *

try:
    pktact.pa_config=getOpenflowConfig(globEpName)
    pktact.pa_port_map= pktact.pa_config['port_map']
except:
    print "Error: Invalid configuration for EPNAME: " + str(globEpName)

class ModifyVID(BaseMatchCase):
    """
    Modify the VLAN ID in the VLAN tag of a tagged packet
    """
    def runTest(self):
        old_vid = 2
        new_vid = 3
        sup_acts = supported_actions_get(self)
        if not (sup_acts & 1 << ofp.OFPAT_SET_VLAN_VID):
            skip_message_emit(self, "Modify VLAN tag test")
            return

        pkt = simple_tcp_packet(dl_vlan_enable=True, dl_vlan=old_vid)
        exp_pkt = simple_tcp_packet(dl_vlan_enable=True, dl_vlan=new_vid)
        vid_act = action.action_set_vlan_vid()
        vid_act.vlan_vid = new_vid

        flow_match_test(self, pa_port_map, pkt=pkt, exp_pkt=exp_pkt,
                        action_list=[vid_act])


tc = ModifyVID()
_RESULT = tc.run()
