"""
<title>GroupDelExisting</title>
<description>
    A deletion for existing group should remove the group
    
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

class GroupDelExisting(GroupTest):
    """
    A deletion for existing group should remove the group
    """

    def runTest(self):

        group_add_msg = \
        testutils.create_group_mod_msg(ofp.OFPGC_ADD, ofp.OFPGT_ALL, group_id = 10, buckets = [
            testutils.create_bucket(0, 0, 0, [
                testutils.create_action(action= ofp.OFPAT_OUTPUT, port= 1)
            ])
        ])

        self.send_ctrl_exp_noerror(group_add_msg, 'group add')

        group_del_msg = \
        testutils.create_group_mod_msg(ofp.OFPGC_DELETE, ofp.OFPGT_ALL, group_id = 10, buckets = [
        ])

        self.send_ctrl_exp_noerror(group_del_msg, 'group del')

    
tc = GroupDelExisting()
_RESULT = tc.run()
