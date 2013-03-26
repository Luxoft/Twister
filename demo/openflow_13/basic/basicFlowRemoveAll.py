"""
<title>FlowRemoveAll</title>
<description>
    Remove all flows; required for almost all tests
    Add a bunch of flows, remove them, and then make sure there are no flows left
    This is an intentionally naive test to see if the baseline functionality works
    and should be a precondition to any more complicated deletion test (e.g.,
    delete_strict vs. delete)    
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

class FlowRemoveAll(SimpleProtocol):
    """
    Remove all flows; required for almost all tests
    Add a bunch of flows, remove them, and then make sure there are no flows left
    This is an intentionally naive test to see if the baseline functionality works
    and should be a precondition to any more complicated deletion test (e.g.,
    delete_strict vs. delete)
    """
    def runTest(self):
        self.logger.info("Running StatsGet")
        self.logger.info("Inserting trial flow")

        for i in range(1,5):
            request = message.flow_mod()
            request.buffer_id = 0xffffffff
            request.match.type = ofp.OFPMT_OXM
            eth_type = match.eth_type(IPV4_ETHERTYPE)
            request.match_fields.tlvs.append(eth_type)

            act = action.action_output()
            act.port = ofp.OFPP_CONTROLLER
            act.max_len = ofp.OFPCML_NO_BUFFER
            inst = instruction.instruction_apply_actions()
            inst.actions.add(act)
            request.instructions.add(inst)
            request.priority = i*1000
            self.logger.info("Adding flow %d" % i)
            logMsg('logDebug',request.show())
            rv = self.controller.message_send(request)
            self.assertTrue(rv != -1, "Failed to insert test flow %d" % i)

        self.logger.info("Removing all flows")
        testutils.delete_all_flows(self.controller, self.logger)
        self.logger.info("Sending flow request")
        request = message.flow_stats_request()
        request.out_port = ofp.OFPP_ANY
        request.out_group = ofp.OFPG_ANY
        request.table_id = 0xff
        response, _ = self.controller.transact(request, timeout=2)
        self.assertTrue(response is not None, "Did not get response")
        logMsg('logDebug',"Response from switch:")
        logMsg('logDebug',response.show())
        self.assertTrue(isinstance(response,message.flow_stats_reply),"Not a flow_stats_reply")
        self.assertEqual(len(response.stats),0)

    
tc = FlowRemoveAll()
_RESULT = tc.run()
