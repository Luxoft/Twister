"""
<title>GroupProcSimple</title>
<description>
    A group should apply its actions on packets
    
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

class GroupProcSimple(GroupTest):
    """
    A group should apply its actions on packets
    """

    def runTest(self):
        self.clear_switch()

        group_add_msg = \
        testutils.create_group_mod_msg(ofp.OFPGC_ADD, ofp.OFPGT_ALL, group_id = 1, buckets = [
            testutils.create_bucket(0, 0, 0, [
                testutils.create_action(action = ofp.OFPAT_SET_FIELD, tcp_sport = 2000),
                testutils.create_action(action = ofp.OFPAT_OUTPUT, port = 2)
            ])
        ])

        self.send_ctrl_exp_noerror(group_add_msg, 'group add')

        packet_in  = testutils.simple_tcp_packet(tcp_sport=1000)
        packet_out = testutils.simple_tcp_packet(tcp_sport=2000)

        flow_add_msg = \
        testutils.flow_msg_create(self,packet_in,ing_port = 1,action_list = [
            testutils.create_action(action = ofp.OFPAT_GROUP, group_id = 1)
        ])

        self.send_ctrl_exp_noerror(flow_add_msg, 'flow add')

        self.send_data(packet_in, 1)

        self.recv_data(2, packet_out)

    
tc = GroupProcSimple()
_RESULT = tc.run()
