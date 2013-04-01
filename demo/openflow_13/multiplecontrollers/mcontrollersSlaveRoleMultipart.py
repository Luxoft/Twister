"""
<title>SlaveRoleMultipart</title>
<description>A slave controller should be able to send multipart request messages
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

class SlaveRoleMultipart(MultipleController):

    """A slave controller should be able to send multipart request messages"""

    def runTest(self):

        self.logger.info("Running slave controller multipart request test ")
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

        #Sending multipart request
        self.logger.info("Sending multipart request")
        msg = message.table_stats_request()
        response, _ = self.controller.transact(msg, timeout=2)
        self.assertTrue(response is not None, "Did not get response")
        logMsg('logDebug',"Response from switch: ")
        logMsg('logDebug',response.show())
        self.assertTrue(response.type == ofp.OFPMP_TABLE, "Response is not OFPMP_TABLE")

    
tc = SlaveRoleMultipart(testbed=currentTB,ra_proxy=ra_service)
_RESULT = tc.run()
