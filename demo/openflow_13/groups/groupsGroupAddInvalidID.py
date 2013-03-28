"""
<title>GroupAddInvalidID</title>
<description>
    An addition with invalid group id (reserved) should result in OFPET_GROUP_MOD_FAILED/OFPGMFC_INVALID_GROUP
    
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

class GroupAddInvalidID(GroupTest):
    """
    An addition with invalid group id (reserved) should result in OFPET_GROUP_MOD_FAILED/OFPGMFC_INVALID_GROUP
    """

    def runTest(self):
        self.clear_switch()
        group_add_msg = \
        testutils.create_group_mod_msg(ofp.OFPGC_ADD, ofp.OFPGT_ALL, group_id = ofp.OFPG_ALL, buckets = [
            testutils.create_bucket(0, 0, 0, [
                testutils.create_action(action= ofp.OFPAT_OUTPUT, port= 1)
            ])
        ])
        self.send_ctrl_exp_error(group_add_msg, 'group add',
                                 ofp.OFPET_GROUP_MOD_FAILED,
                                 ofp.OFPGMFC_INVALID_GROUP)

    
tc = GroupAddInvalidID()
_RESULT = tc.run()
