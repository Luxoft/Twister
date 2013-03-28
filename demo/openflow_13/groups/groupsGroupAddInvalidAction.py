"""
<title>GroupAddInvalidAction</title>
<description>
    If any action in the buckets is invalid, OFPET_BAD_ACTION/<code> should be returned
    
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

class GroupAddInvalidAction(GroupTest):
    """
    If any action in the buckets is invalid, OFPET_BAD_ACTION/<code> should be returned
    """

    def runTest(self):
        self.logger.info("Running GroupAddInvalidAction test")
        self.clear_switch()
        group_add_msg = \
        testutils.create_group_mod_msg(ofp.OFPGC_ADD, ofp.OFPGT_ALL, group_id = 0, buckets = [
            testutils.create_bucket(0, 0, 0, [
                testutils.create_action(action= ofp.OFPAT_OUTPUT, port= ofp.OFPP_ANY)
            ])
        ])

        self.send_ctrl_exp_error(group_add_msg, 'group add',
                                 ofp.OFPET_BAD_ACTION,
                                 ofp.OFPBAC_BAD_OUT_PORT)

    
tc = GroupAddInvalidAction()
_RESULT = tc.run()
