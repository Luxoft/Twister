"""
<title>FlowExpireBoth</title>
<description>
    Verify flow expire messages are properly generated.

    Generate a packet
    Generate and install a matching flow with hard timeout = 2 sec
    and idle timeout = 10 sec. Verify the flow expiration message is received
    and the hard timeout respected ( we send packets to the matching flow )
    
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

class FlowExpireBoth(SimpleDataPlane):
    """
    Verify flow expire messages are properly generated.

    Generate a packet
    Generate and install a matching flow with hard timeout = 2 sec
    and idle timeout = 10 sec. Verify the flow expiration message is received
    and the hard timeout respected ( we send packets to the matching flow )
    """
    def runTest(self):
        # TODO: set from command-line parameter
        self.logger.info("Running FlowExpireBoth test")
        self.logger.info("Insert flowmod with both idle and hard timeout set")
        self.logger.info("Verify that hard timeout is respected and flow remove message received")
        test_timeout = 60

        of_ports = self.port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 1, "Not enough ports for test")

        self.logger.info("Clear the switch state, delete all flows")
        rc = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        pkt = testutils.simple_tcp_packet()
        match = parse.packet_to_flow_match(pkt)
        self.assertTrue(match is not None,"Could not generate flow match from pkt")
        act = action.action_output()

        ingress_port = of_ports[0]
        egress_port  = of_ports[1]
        self.logger.info("Ingress " + str(ingress_port) + " to egress " + str(egress_port))

        request = message.flow_mod()
        request.match_fields = match
        request.cookie = random.randint(0,9007199254740992)
        request.buffer_id = 0xffffffff
        request.hard_timeout = 2
        request.idle_timeout = 20
        request.flags |= ofp.OFPFF_SEND_FLOW_REM
        act.port = egress_port
        inst = instruction.instruction_apply_actions()
        inst.actions.add(act)
        request.instructions.add(inst)

        self.logger.info("Inserting flow")
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',request.show())
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, "Error installing flow mod")
        for i in range(0,60):
            self.dataplane.send(ingress_port, str(pkt))

        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_FLOW_REMOVED,
                                               timeout=test_timeout)
        self.assertTrue(response is not None,
                        'Did not receive flow removed message ')
        logMsg('logDebug',"Response from switch:")
        logMsg('logDebug',response.show())
        self.assertEqual(request.cookie, response.cookie,
                         'Cookies do not match')
        self.assertEqual(ofp.OFPRR_HARD_TIMEOUT, response.reason,
                         'Flow table entry removal reason is not idle_timeout')

    
tc = FlowExpireBoth()
_RESULT = tc.run()
