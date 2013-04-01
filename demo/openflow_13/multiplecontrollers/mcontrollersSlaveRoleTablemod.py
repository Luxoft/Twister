"""
<title>SlaveRoleTablemod</title>
<description>A slave controller should not be able to send TableMod messages
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

class SlaveRoleTablemod(MultipleController):

    """A slave controller should not be able to send TableMod messages"""

    def runTest(self):

        self.logger.info("Running slave controller tablemod test ")
        self.logger.info("First send RoleRequest nochange in order to get generation_id")
        self.logger.info("Second send RoleRequest with role SLAVE")

        #Get the current generation_id
        request = message.role_request()
        request.role = ofp.OFPCR_ROLE_NOCHANGE
        logMsg('logDebug',"Request to switch: ")
        logMsg('logDebug',request.show())
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, "Not able to send role request.")
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ROLE_REPLY,
                                               timeout=2)
        self.assertTrue(response is not None, 'Did not receive OFPT_ROLE_REPLY')
        logMsg('logDebug',"Response from switch: ")
        logMsg('logDebug',response.show())
        new_genid = response.generation_id + 1

        #Send role change request
        request = message.role_request()
        request.role = ofp.OFPCR_ROLE_SLAVE
        request.generation_id = new_genid
        logMsg('logDebug',"Request to switch: ")
        logMsg('logDebug',request.show())
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, " Not able to send role request.")
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ROLE_REPLY,
                                               timeout=2)
        self.assertTrue(response is not None, 'Did not receive OFPT_ROLE_REPLY')
        logMsg('logDebug',"Response from switch: ")
        logMsg('logDebug',response.show())
        self.assertTrue(response.role == ofp.OFPCR_ROLE_SLAVE, 'Role is not SLAVE')

        #Send tablemod message
        self.logger.info("Sending tablemod message to switch")
        msg = message.table_mod()
        msg.table_id = 0 # first table should always exist
        msg.config = ofp.OFPTFPT_NEXT_TABLES_MISS
        logMsg('logDebug',"Request to switch: ")
        logMsg('logDebug',request.show())
        rv = self.controller.message_send(msg)
        self.assertTrue(rv != -1, " Not able to sent tablemod request.")
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ERROR,timeout=2)
        self.assertTrue(response is not None, 'Did not receive OFPT_ERROR')
        logMsg('logDebug',"Response from switch: ")
        logMsg('logDebug',response.show())
        self.assertTrue(response.type == ofp.OFPET_BAD_REQUEST, 'Erorr is not OFPET_BAD_REQUEST')
        self.assertTrue(response.code == ofp.OFPBRC_IS_SLAVE, 'Error is not OFPBRC_IS_SLAVE')

    
tc = SlaveRoleTablemod(testbed=currentTB,ra_proxy=ra_service)
_RESULT = tc.run()
