"""
<title>DecNewMPLSttlInvalid</title>
<description>
    Decrement ttl of MPLS tag to packet
    
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

class DecNewMPLSttlInvalid(SimpleDataPlane):
    """
    Decrement new ttl to mpls packet	
    """
    def runTest(self):
        self.logger.info("Running DecNewMPLSttlInvalid test")
        of_ports = self.port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 0, "Not enough ports for test")

        #Clear the switch state
        self.logger.info("Clear the switch state")
        rv = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rv, 0, "Failed to delete all flows")

        ingress_port = of_ports[0]
        egress_port = of_ports[1]
	self.logger.info("Insert flow_mod with action decrement MPLS ttl to -1, switch must drop")
        pkt = testutils.simple_tcp_packet(mpls_tags=[{'label': 50, 'ttl': 0}])
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
        vid_act = action.action_dec_mpls_ttl()
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
	self.logger.info("Waiting for packet, switch must drop since it have ttl -1")
        (rcv_port, rcv_pkt, _) = self.dataplane.poll(port_number=egress_port, timeout=1)
        self.assertTrue(rcv_pkt == None, "Packet recevied, switch must drop it since should have ttl -1")

    
tc = DecNewMPLSttlInvalid()
_RESULT = tc.run()
