"""
<title>GroupModLoop</title>
<description>
    A modification causing loop should result in OFPET_GROUP_MOD_FAILED/OFPGMFC_LOOP
    
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

class GroupModLoop(GroupTest):
    """
    A modification causing loop should result in OFPET_GROUP_MOD_FAILED/OFPGMFC_LOOP
    """

    def runTest(self):
        self.clear_switch()

        group_add_msg1 = \
        testutils.create_group_mod_msg(ofp.OFPGC_ADD, ofp.OFPGT_ALL, group_id = 0, buckets = [
            testutils.create_bucket(0, 0, 0, [
                testutils.create_action(action= ofp.OFPAT_OUTPUT, port= 1)
            ])
        ])
        self.send_ctrl_exp_noerror(group_add_msg1, 'group add 1')
        group_add_msg2 = \
        testutils.create_group_mod_msg(ofp.OFPGC_ADD, ofp.OFPGT_ALL, group_id = 1, buckets = [
            testutils.create_bucket(0, 0, 0, [
                testutils.create_action(action= ofp.OFPAT_GROUP, group_id= 0)
            ])
        ])
        self.send_ctrl_exp_noerror(group_add_msg2, 'group add 2')
        group_add_msg3 = \
        testutils.create_group_mod_msg(ofp.OFPGC_ADD, ofp.OFPGT_ALL, group_id = 2, buckets = [
            testutils.create_bucket(0, 0, 0, [
                testutils.create_action(action= ofp.OFPAT_GROUP, group_id= 0)
            ])
        ])
        self.send_ctrl_exp_noerror(group_add_msg3, 'group add 3')
        group_mod_msg = \
        testutils.create_group_mod_msg(ofp.OFPGC_MODIFY, ofp.OFPGT_ALL, group_id = 0, buckets = [
            testutils.create_bucket(0, 0, 0, [
                testutils.create_action(action= ofp.OFPAT_GROUP, group_id= 2)
            ])
        ])
        self.send_ctrl_exp_error(group_mod_msg, 'group mod',
                                 ofp.OFPET_GROUP_MOD_FAILED,
                                 ofp.OFPGMFC_LOOP)

    
tc = GroupModLoop()
_RESULT = tc.run()
