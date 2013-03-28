"""
<title>GroupAddExisting</title>
<description>
    An addition with existing group id should result in OFPET_GROUP_MOD_FAILED/OFPGMFC_GROUP_EXISTS
    
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

class GroupAddExisting(GroupTest):
    """
    An addition with existing group id should result in OFPET_GROUP_MOD_FAILED/OFPGMFC_GROUP_EXISTS
    """

    def runTest(self):
        self.clear_switch()

        group_add_msg = \
        testutils.create_group_mod_msg(ofp.OFPGC_ADD, ofp.OFPGT_ALL, group_id = 0, buckets = [
            testutils.create_bucket(0, 0, 0, [
                testutils.create_action(action= ofp.OFPAT_OUTPUT, port= 1)
            ])
        ])
        self.send_ctrl_exp_noerror(group_add_msg, 'group add 1')
        group_mod_msg2 = \
        testutils.create_group_mod_msg(ofp.OFPGC_ADD, ofp.OFPGT_ALL, group_id = 0, buckets = [
            testutils.create_bucket(0, 0, 0, [
                testutils.create_action(action= ofp.OFPAT_OUTPUT, port= 1)
            ])
        ])
        self.send_ctrl_exp_error(group_add_msg, 'group add 2',
                                 ofp.OFPET_GROUP_MOD_FAILED,
                                 ofp.OFPGMFC_GROUP_EXISTS)

    
tc = GroupAddExisting()
_RESULT = tc.run()
