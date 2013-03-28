"""
<title>GroupModEmpty</title>
<description>
    A modification for existing group with no buckets should be accepted
    
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

class GroupModEmpty(GroupTest):
    """
    A modification for existing group with no buckets should be accepted
    """

    def runTest(self):
        self.clear_switch()

        group_add_msg = \
        testutils.create_group_mod_msg(ofp.OFPGC_ADD, ofp.OFPGT_ALL, group_id = 0, buckets = [
            testutils.create_bucket(0, 0, 0, [
                testutils.create_action(action= ofp.OFPAT_OUTPUT, port= 1)
            ])
        ])
        self.send_ctrl_exp_noerror(group_add_msg, 'group add')
        group_mod_msg = \
        testutils.create_group_mod_msg(ofp.OFPGC_MODIFY, ofp.OFPGT_ALL, group_id = 0, buckets = [
        ])
        self.send_ctrl_exp_noerror(group_mod_msg, 'group mod')

    
tc = GroupModEmpty()
_RESULT = tc.run()
