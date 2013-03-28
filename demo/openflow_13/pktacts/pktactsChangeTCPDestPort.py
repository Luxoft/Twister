"""
<title>ChangeTCPDestPort</title>
<description>
    Change dst port of packet
    
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

class ChangeTCPDestPort(SimpleDataPlane):
    """
    Change dst port of packet
    """
    def runTest(self):
        self.logger.info("Running ChangeTCPDestPort")
        of_ports = self.port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 0, "Not enough ports for test")

        #Clear the switch state
        self.logger.info("Clear the switch state")
        rv = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rv, 0, "Failed to delete all flows")

        ingress_port = of_ports[0]
        egress_port = of_ports[1]
        pkt = testutils.simple_tcp_packet()
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
        vid_act = action.action_set_field()
        field_2b_set = match.tcp_dst(8881)
        vid_act.field = field_2b_set
        inst.actions.add(vid_act)
        act_out = action.action_output()
        act_out.port = egress_port
        inst.actions.add(act_out)
        request.instructions.add(inst)
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',request.show())
        self.logger.info("Inserting flow ")
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, "Error installing flow mod")
        self.dataplane.send(ingress_port, str(pkt))

        (rcv_port, rcv_pkt, _) = self.dataplane.poll(port_number=egress_port, timeout=1)
        p = scapy.all.Ether(rcv_pkt)
        self.assertEqual(str(p.payload.dport), "8881", "Destionation port set do not match")

    
tc = ChangeTCPDestPort()
_RESULT = tc.run()
