"""
<title>GroupProcAllChain</title>
<description>
    An ALL group should use all of its buckets, modifying the resulting packet(s)
    
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

class GroupProcAllChain(GroupTest):
    """
    An ALL group should use all of its buckets, modifying the resulting packet(s)
    """

    def runTest(self):
        self.clear_switch()

        group_add_msg2 = \
        testutils.create_group_mod_msg(ofp.OFPGC_ADD, ofp.OFPGT_ALL, group_id = 2, buckets = [
            testutils.create_bucket(0, 0, 0, [
                testutils.create_action(action = ofp.OFPAT_SET_FIELD, tcp_sport = 2000),
                testutils.create_action(action = ofp.OFPAT_OUTPUT, port = 2)
            ])
        ])

        self.send_ctrl_exp_noerror(group_add_msg2, 'group add 2')

        group_add_msg3 = \
        testutils.create_group_mod_msg(ofp.OFPGC_ADD, ofp.OFPGT_ALL, group_id = 3, buckets = [
            testutils.create_bucket(0, 0, 0, [
                testutils.create_action(action = ofp.OFPAT_SET_FIELD, tcp_sport = 3000),
                testutils.create_action(action = ofp.OFPAT_OUTPUT, port = 3)
            ]),
            testutils.create_bucket(0, 0, 0, [
                testutils.create_action(action = ofp.OFPAT_SET_FIELD, tcp_sport = 4000),
                testutils.create_action(action = ofp.OFPAT_OUTPUT, port = 4)
            ])
        ])

        self.send_ctrl_exp_noerror(group_add_msg3, 'group add 3')

        group_add_msg1 = \
        testutils.create_group_mod_msg(ofp.OFPGC_ADD, ofp.OFPGT_ALL, group_id = 1, buckets = [
            testutils.create_bucket(0, 0, 0, [
                testutils.create_action(action = ofp.OFPAT_GROUP, group_id = 2),
            ]),
            testutils.create_bucket(0, 0, 0, [
                testutils.create_action(action = ofp.OFPAT_GROUP, group_id = 3),
            ])
        ])

        self.send_ctrl_exp_noerror(group_add_msg1, 'group add 1')

        packet_in  = testutils.simple_tcp_packet(tcp_sport=1000)
        packet_out1 = testutils.simple_tcp_packet(tcp_sport=2000)
        packet_out2 = testutils.simple_tcp_packet(tcp_sport=3000)
        packet_out3 = testutils.simple_tcp_packet(tcp_sport=4000)

        flow_add_msg = \
        testutils.flow_msg_create(self,packet_in,ing_port = 1,action_list = [
            testutils.create_action(action = ofp.OFPAT_GROUP, group_id = 1)
        ])

        self.send_ctrl_exp_noerror(flow_add_msg, 'flow add')

        self.send_data(packet_in, 1)

        self.recv_data(2, packet_out1)
        self.recv_data(3, packet_out2)
        self.recv_data(4, packet_out3)

    
tc = GroupProcAllChain()
_RESULT = tc.run()
