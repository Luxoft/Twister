"""
<title>GroupProcEmpty</title>
<description>
    A group with no buckets should not alter the action set of the packet
    
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

class GroupProcEmpty(GroupTest):
    """
    A group with no buckets should not alter the action set of the packet
    """

    def runTest(self):

        self.clear_switch()

        group_add_msg = \
        testutils.create_group_mod_msg(ofp.OFPGC_ADD, ofp.OFPGT_ALL, group_id = 1, buckets = [
        ])

        self.send_ctrl_exp_noerror(group_add_msg, 'group add')

        packet_in  = testutils.simple_tcp_packet()

        flow_add_msg = \
        testutils.create_flow_msg(packet = packet_in, in_port = 1, apply_action_list = [
            testutils.create_action(action = ofp.OFPAT_GROUP, group_id = 1)
        ])

        self.send_ctrl_exp_noerror(flow_add_msg, 'flow add')

        self.send_data(packet_in, 1)

        self.recv_data(2, None)

    
tc = GroupProcEmpty()
_RESULT = tc.run()
