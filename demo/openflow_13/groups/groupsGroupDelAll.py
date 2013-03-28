"""
<title>GroupDelAll</title>
<description>
    #@todo: A deletion for OFGP_ALL should remove all groups
    
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

class GroupDelAll(GroupTest):
    """
    #@todo: A deletion for OFGP_ALL should remove all groups
    """

    def runTest(self):
        self.clear_switch()

        group_add_msg1 = \
        testutils.create_group_mod_msg(ofp.OFPGC_ADD, ofp.OFPGT_ALL, group_id = 1, buckets = [
            testutils.create_bucket(0, 0, 0, [
                testutils.create_action(action= ofp.OFPAT_OUTPUT, port= 1)
            ])
        ])

        self.send_ctrl_exp_noerror(group_add_msg1, 'group add 1')

        group_add_msg2 = \
        testutils.create_group_mod_msg(ofp.OFPGC_ADD, ofp.OFPGT_ALL, group_id = 2, buckets = [
            testutils.create_bucket(0, 0, 0, [
                testutils.create_action(action= ofp.OFPAT_OUTPUT, port= 1)
            ])
        ])

        self.send_ctrl_exp_noerror(group_add_msg2, 'group add 2')

        group_del_msg = \
        testutils.create_group_mod_msg(ofp.OFPGC_DELETE, group_id = ofp.OFPG_ALL)

        self.send_ctrl_exp_noerror(group_del_msg, 'group del')

    
tc = GroupDelAll()
_RESULT = tc.run()
