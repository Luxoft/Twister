"""
<title>MatchICMPv6Simple</title>
<description>
    Match on an ICMPv6 packet
    
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

class MatchICMPv6Simple(SimpleDataPlane):
    """
    Match on an ICMPv6 packet
    """
    def runTest(self):
        self.logger.info("Running MatchICMPv6Simple test")
        self.logger.info("Send ICMPv6 packet to matching flow and verify it is received")
        of_ports = self.port_map.keys()
        of_ports.sort()
        ing_port = of_ports[0]
        egr_port = of_ports[3]

        # Remove all entries Add entry match all
        self.logger.info("Clear the switch state, delete all flows")
        rc = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        # Add entry match
        request = message.flow_mod()
        request.match.type = ofp.OFPMT_OXM
        port = match.in_port(of_ports[0])
        eth_type = match.eth_type(IPV6_ETHERTYPE)
        ipv6_src = match.ipv6_src(ipaddr.IPv6Address('fe80::2420:52ff:fe8f:5189'))
        ip_proto = match.ip_proto(ICMPV6_PROTOCOL)
        icmpv6_type = match.icmpv6_type(128)
        request.match_fields.tlvs.append(port)
        request.match_fields.tlvs.append(eth_type)
        request.match_fields.tlvs.append(ipv6_src)
        request.match_fields.tlvs.append(ip_proto)
        request.match_fields.tlvs.append(icmpv6_type)
        act = action.action_output()
        act.port = of_ports[3]
        inst = instruction.instruction_apply_actions()
        inst.actions.add(act)
        request.instructions.add(inst)
        request.buffer_id = 0xffffffff

        request.priority = 1000
        self.logger.info("Adding flow ")
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',request.show())
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, "Failed to insert test flow")

        #Send packet
        pkt = testutils.simple_icmpv6_packet()
        self.logger.info("Sending IPv6 packet to " + str(ing_port))
        self.dataplane.send(ing_port, str(pkt))
        #Receive packet
        exp_pkt = testutils.simple_icmpv6_packet()
        testutils.receive_pkt_verify(self, egr_port, exp_pkt)
        #Remove flows
        rc = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

    
tc = MatchICMPv6Simple()
_RESULT = tc.run()
