"""
<title>PktFlowmodPriority</title>
<description>
    Generate pkt, insert two flowmod with priority set
    then verify that priority is respected.
    
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

class PktFlowmodPriority(SimpleDataPlane):
    """
    Generate pkt, insert two flowmod with priority set
    then verify that priority is respected.
    """
    def runTest(self):
        self.logger.info("Running PktFlowmodPriority test")
        of_ports = self.port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 0, "Not enough ports for test")

        #Clear the switch state
        self.logger.info("Clear the switch state")
        rv = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rv, 0, "Failed to delete all flows")

        #Generate a packet
        pkt = testutils.simple_tcp_packet()
        ingress_port = of_ports[0]
        egress_port = of_ports[1]
        egress_prio = of_ports[2]

        #Insert flow_mod with priority 0
        portmatch = match.in_port(ingress_port)
        srcmatch = match.eth_src(parse.parse_mac("00:06:07:08:09:0a"))
        dstmatch = match.eth_dst(parse.parse_mac("00:01:02:03:04:05"))
        request = message.flow_mod()
        request.match_fields.tlvs.append(portmatch)
        request.match_fields.tlvs.append(srcmatch)
        request.match_fields.tlvs.append(dstmatch)
        request.buffer_id = 0xffffffff
        request.priority = 0

        inst = instruction.instruction_apply_actions()
        act = action.action_output()
        act.port = egress_port
        inst.actions.add(act)
        request.instructions.add(inst)
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',request.show())
        self.logger.info("Inserting flow ")
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, "Error installing flow mod")

        #Send a packet a verify that it is received on egress_port
        self.dataplane.send(ingress_port, str(pkt))
        testutils.receive_pkt_check(self.dataplane, pkt, [egress_port], [],
                              self,self.logger)

        #Insert flow_mod with priority 1
        portmatch = match.in_port(ingress_port)
        srcmatch = match.eth_src(parse.parse_mac("00:06:07:08:09:0a"))
        dstmatch = match.eth_dst(parse.parse_mac("00:01:02:03:04:05"))
        request = message.flow_mod()
        request.match_fields.tlvs.append(portmatch)
        request.match_fields.tlvs.append(srcmatch)
        request.match_fields.tlvs.append(dstmatch)
        request.buffer_id = 0xffffffff
        request.priority = 1

        inst = instruction.instruction_apply_actions()
        act = action.action_output()
        act.port = egress_prio
        inst.actions.add(act)
        request.instructions.add(inst)
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',request.show())
        self.logger.info("Inserting flow ")
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, "Error installing flow mod")

        #Send a packet a verify that it is received on egress_port
        self.dataplane.send(ingress_port, str(pkt))
        testutils.receive_pkt_check(self.dataplane, pkt, [egress_prio], [egress_port],
                              self,self.logger)

    
tc = PktFlowmodPriority()
_RESULT = tc.run()
