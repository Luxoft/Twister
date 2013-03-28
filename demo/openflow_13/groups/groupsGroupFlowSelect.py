"""
<title>GroupFlowSelect</title>
<description>
    A group action select with group id should select the correct flows only
    
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

class GroupFlowSelect(GroupTest):
    """
    A group action select with group id should select the correct flows only
    """

    def runTest(self):
        self.clear_switch()

        group_add_msg1 = \
        testutils.create_group_mod_msg(ofp.OFPGC_ADD, ofp.OFPGT_ALL, group_id = 1, buckets = [])

        self.send_ctrl_exp_noerror(group_add_msg1, 'group add 1')

        group_add_msg2 = \
        testutils.create_group_mod_msg(ofp.OFPGC_ADD, ofp.OFPGT_ALL, group_id = 2, buckets = [])

        self.send_ctrl_exp_noerror(group_add_msg2, 'group add 2')

        packet_in1 = testutils.simple_tcp_packet(tcp_sport=1000)

        flow_add_msg1 = \
        testutils.flow_msg_create(self,packet_in1,ing_port = 1,action_list = [
            testutils.create_action(action = ofp.OFPAT_GROUP, group_id = 1),
            testutils.create_action(action = ofp.OFPAT_OUTPUT, port = 2)
        ])

        self.send_ctrl_exp_noerror(flow_add_msg1, 'flow add 1')

        packet_in2 = testutils.simple_tcp_packet(tcp_sport=2000)

        flow_add_msg2 = \
        testutils.flow_msg_create(self,packet_in2,ing_port = 1,action_list = [
            testutils.create_action(action = ofp.OFPAT_GROUP, group_id = 2),
            testutils.create_action(action = ofp.OFPAT_OUTPUT, port = 2)
        ])

        self.send_ctrl_exp_noerror(flow_add_msg2, 'flow add 2')

        packet_in3 = testutils.simple_tcp_packet(tcp_sport=3000)

        flow_add_msg3 = \
        testutils.flow_msg_create(self,packet_in3,ing_port = 1,action_list = [
            testutils.create_action(action = ofp.OFPAT_GROUP, group_id = 2),
            testutils.create_action(action = ofp.OFPAT_OUTPUT, port = 2)
        ])

        self.send_ctrl_exp_noerror(flow_add_msg3, 'flow add 3')

        packet_in4 = testutils.simple_tcp_packet(tcp_sport=4000)

        flow_add_msg4 = \
        testutils.flow_msg_create(self,packet_in4,ing_port = 1,action_list = [
            testutils.create_action(action = ofp.OFPAT_OUTPUT, port = 2)
        ])

        self.send_ctrl_exp_noerror(flow_add_msg4, 'flow add 4')

        aggr_stat_req = message.aggregate_stats_request()
        aggr_stat_req.table_id = 0xff
        aggr_stat_req.out_port = ofp.OFPP_ANY
        aggr_stat_req.out_group = 2
        aggr_stat_req.match.type = 1
        response = \
        self.send_ctrl_exp_reply(aggr_stat_req,
                                 ofp.OFPT_MULTIPART_REPLY, 'aggr stat')
        self.assertEqual(response.stats[0].flow_count, 2,
                         'Did not match expected flow count')

    
tc = GroupFlowSelect()
_RESULT = tc.run()
