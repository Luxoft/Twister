"""
<title>PktClearActionInstrunction</title>
<description>
    Generate pkt, insert matching flow, send to ingress_port, verify that it is received on egress_port
    then clear actions and send again verifying that it is droped.
    
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

class PktClearActionInstrunction(SimpleDataPlane):
    """
    Generate pkt, insert matching flow, send to ingress_port, verify that it is received on egress_port
    then clear actions and send again verifying that it is droped.
    """
    def runTest(self):
        self.logger.info("Running PktClearActionInstrion test")
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

        #Insert flow_mod to table 0 and direct the matching packet to table 1
        portmatch = match.in_port(ingress_port)
        srcmatch = match.eth_src(parse.parse_mac("00:06:07:08:09:0a"))
        dstmatch = match.eth_dst(parse.parse_mac("00:01:02:03:04:05"))
        request = message.flow_mod()
        request.match_fields.tlvs.append(portmatch)
        request.match_fields.tlvs.append(srcmatch)
        request.match_fields.tlvs.append(dstmatch)
        request.buffer_id = 0xffffffff

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

        #Clear the actions
        portmatch = match.in_port(ingress_port)
        srcmatch = match.eth_src(parse.parse_mac("00:06:07:08:09:0a"))
        dstmatch = match.eth_dst(parse.parse_mac("00:01:02:03:04:05"))
        request = message.flow_mod()
        request.match_fields.tlvs.append(portmatch)
        request.match_fields.tlvs.append(srcmatch)
        request.match_fields.tlvs.append(dstmatch)
        request.buffer_id = 0xffffffff
        request.table_id = 0
        inst = instruction.instruction_clear_actions()
        request.instructions.add(inst)
        self.logger.info("Inserting flow ")
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',request.show())
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, "Error installing flow mod")

        #Send again
        self.dataplane.send(ingress_port, str(pkt))
        testutils.receive_pkt_check(self.dataplane, pkt, [], of_ports,
                              self,self.logger)

    
tc = PktClearActionInstrunction()
_RESULT = tc.run()
