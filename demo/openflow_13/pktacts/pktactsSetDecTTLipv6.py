"""
<title>SetNewTTLipv6</title>
<description>
    Set decrement TTL to ipv6 packet
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

class SetDecTTLipv6(SimpleDataPlane):
    """
    Decrement TTL to ipv6 packet
    """
    def runTest(self):
        self.logger.info("Running SetDecTTLipv6 test")
        of_ports = self.port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 0, "Not enough ports for test")

        #Clear the switch state
        self.logger.info("Clear the switch state")
        rv = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rv, 0, "Failed to delete all flows")

        ingress_port = of_ports[0]
        egress_port = of_ports[1]
	pkt = testutils.simple_ipv6_packet(dl_dst='00:01:02:03:04:05',ip_src='fe80::2420:52ff:fe8f:5189',ip_dst='fe80::2420:52ff:fe8f:5190')
        port = match.in_port(ingress_port)
        eth_type = match.eth_type(IPV6_ETHERTYPE)
        eth_dst = match.eth_dst(parse.parse_mac("00:01:02:03:04:05"))
        ipv6_src = match.ipv6_src(ipaddr.IPv6Address('fe80::2420:52ff:fe8f:5189'))
        ipv6_dst = match.ipv6_dst(ipaddr.IPv6Address('fe80::2420:52ff:fe8f:5190'))
	self.logger.info("Generate and send flow_mod with dec_ttl action, initial packet have ttl 64")
        request = message.flow_mod()
        request.match_fields.tlvs.append(port)
        request.match_fields.tlvs.append(eth_type)
        request.match_fields.tlvs.append(eth_dst)
        request.match_fields.tlvs.append(ipv6_src)
        request.match_fields.tlvs.append(ipv6_dst)
       	request.buffer_id = 0xffffffff
        request.priority = 1
        inst = instruction.instruction_apply_actions()
        vid_act = action.action_dec_nw_ttl()
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
        p = scapy.all.Ether(str(rcv_pkt))
	self.logger.info("Verify incoming packet have hop_count set to 63")
	self.assertEqual(p.hlim, 63, "Incoming packet do not have hlim 63")
 
tc = SetDecTTLipv6()
_RESULT = tc.run()
