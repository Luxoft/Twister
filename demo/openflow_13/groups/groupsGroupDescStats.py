"""
<title>GroupDescStats</title>
<description>
    Desc stats of a group should work
    
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

class GroupDescStats(GroupTest):
    """
    Desc stats of a group should work
    """

    def runTest(self):
        self.clear_switch()

        b1 = testutils.create_bucket(0, 0, 0, [
                 testutils.create_action(action = ofp.OFPAT_OUTPUT, port = 2)
            ])
        b2 =  testutils.create_bucket(0, 0, 0, [
                  testutils.create_action(action = ofp.OFPAT_OUTPUT, port = 3)
            ])
        b3 = testutils.create_bucket(0, 0, 0, [
                 testutils.create_action(action = ofp.OFPAT_OUTPUT, port = 4)
            ])

        group_add_msg = \
        testutils.create_group_mod_msg(ofp.OFPGC_ADD, ofp.OFPGT_ALL, group_id = 10, buckets = [b1, b2, b3])
        self.send_ctrl_exp_noerror(group_add_msg, 'group add')
        group_desc_stats_req = \
        testutils.create_group_desc_stats_req()

        response = \
        self.send_ctrl_exp_reply(group_desc_stats_req,
                                 ofp.OFPT_MULTIPART_REPLY, 'group desc stat')
        exp_len = ofp.OFP_HEADER_BYTES + \
                  ofp.OFP_MULTIPART_REPLY_BYTES + \
                  ofp.OFP_GROUP_DESC_STATS_BYTES + \
                  len(b1) + len(b2) + len(b3)

        self.assertEqual(len(response), exp_len,
                         'Received packet length does not equal expected length')

    
tc = GroupDescStats()
_RESULT = tc.run()
