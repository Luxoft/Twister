"""
<title>PacketIn</title>
<description>
    Test packet in function
    Send a packet to each dataplane port and verify that a packet
    in message is received from the controller for each
    
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

class PacketIn(SimpleDataPlane):
    """
    Test packet in function
    Send a packet to each dataplane port and verify that a packet
    in message is received from the controller for each
    """
    def runTest(self):
        # Construct packet to send to dataplane
        # Send packet to dataplane, once to each port
        # Poll controller with expect message type packet in

        self.logger.info("Running PacketIn test")
        self.logger.info("Clear the switch state -- delete all flows")
        rc = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        # Need to insert flow fowarding packets to the controller!!!
        request = message.flow_mod()
        request.match.type = 1
        eth_type = match.eth_type(IPV4_ETHERTYPE)
        eth_dst = match.eth_dst(parse.parse_mac("00:01:02:03:04:05"))
        ipv4_src = match.ipv4_src(ipaddr.IPv4Address('192.168.0.1'))
        request.match_fields.tlvs.append(eth_type)
        request.match_fields.tlvs.append(eth_dst)
        request.match_fields.tlvs.append(ipv4_src)

        act = action.action_output()
        act.port = ofp.OFPP_CONTROLLER
        act.max_len = ofp.OFPCML_NO_BUFFER
        inst = instruction.instruction_apply_actions()
        inst.actions.add(act)
        request.instructions.add(inst)
        request.buffer_id = 0xffffffff

        request.priority = 1000
        self.logger.info("Sending flowmod to switch")
        logMsg('logDebug',"Flowmod packet:")
        logMsg('logDebug',request.show())
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, "Failed to insert test flow")
        testutils.do_barrier(self.controller)

        for of_port in self.port_map.keys():
            self.logger.info("PKT IN test, port " + str(of_port))
            pkt = testutils.simple_tcp_packet(dl_dst='00:01:02:03:04:05',ip_src='192.168.0.1')
            self.dataplane.send(of_port, str(pkt))
            testutils.do_barrier(self.controller)
            response,_  = self.controller.poll(ofp.OFPT_PACKET_IN, 2)
            logMsg('logDebug',response.show())
            self.assertTrue(response is not None,
                            'Packet in message not received on port ' +
                            str(of_port))
            self.assertEqual(response.reason, ofp.OFPR_ACTION, 'PacketIn type not OFPR_ACTION')

    
tc = PacketIn()
_RESULT = tc.run()
