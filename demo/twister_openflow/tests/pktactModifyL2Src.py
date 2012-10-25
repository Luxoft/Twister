
from ce_libs import *

try:
    pktact.pa_config = getOpenflowConfig(globEpName)
    pktact.pa_port_map = pktact.pa_config['port_map']
except:
    print 'Error: Invalid configuration for EPNAME: ' + str(globEpName)

class ModifyL2Src(BaseMatchCase):
    """
    Modify the source MAC address (TP1)
    """
    def runTest(self):
        sup_acts = supported_actions_get(self)
        if not (sup_acts & 1 << ofp.OFPAT_SET_DL_SRC):
            skip_message_emit(self, "ModifyL2Src test")
            return

        (pkt, exp_pkt, acts) = pkt_action_setup(self, mod_fields=['dl_src'],
                                                check_test_params=True)
        flow_match_test(self, pa_port_map, pkt=pkt, exp_pkt=exp_pkt,
                        action_list=acts, max_test=2)


tc = ModifyL2Src()
_RESULT = tc.run()
