"""
<title>AllplusNONforward</title>
<description>
    Send to OFPP_ALL port

    Generate a packet
    Generate and install a matching flow
    Add action to forward to OFPP_ALL
    Send the packet to ingress dataplane port
    Verify the packet is received at all other ports
    
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

class AllplusNONforward(SimpleDataPlane):
    """
    Send to OFPP_ALL port

    Generate a packet
    Generate and install a matching flow
    Add action to forward to OFPP_ALL
    Send the packet to ingress dataplane port
    Verify the packet is received at all other ports
    """
    def runTest(self):
        self.logger.info("Running All test")
        of_ports = self.port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 0, "Not enough ports for test")

        pkt = testutils.simple_tcp_packet()
        act = action.action_output()

        self.logger.info("Clear the switch state")
        rv = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rv, 0, "Failed to delete all flows")
	ingress_port = of_ports[1]
        self.logger.info("Ingress " + str(ingress_port) + " to all ports")

        portmatch = match.in_port(ingress_port)
        srcmatch = match.eth_src(parse.parse_mac("00:06:07:08:09:0a"))
        dstmatch = match.eth_dst(parse.parse_mac("00:01:02:03:04:05"))
        request = message.flow_mod()
        request.match_fields.tlvs.append(portmatch)
        request.match_fields.tlvs.append(srcmatch)
        request.match_fields.tlvs.append(dstmatch)
        request.buffer_id = 0xffffffff
        act.port = ofp.OFPP_ALL
        inst = instruction.instruction_apply_actions()
        inst.actions.add(act)
        request.instructions.add(inst)
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',request.show())
        self.logger.info("Inserting flow")
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, "Error installing flow mod")

	self.logger.info("Send port_mod no forward for port 1")
        #Retrieve Port Configuration
        self.logger.info("Sends Features Request and retrieve Port Configuration from reply")
        (hw_addr, port_config, advert) = \
            testutils.port_config_get(self.controller, of_ports[0], self.logger)
        self.assertTrue(port_config is not None, "Did not get port config")
        logMsg('logDebug',"No flood bit port " + str(of_ports[0]) + " is now " +
                           str(port_config & ofp.OFPPC_NO_FWD))

        #Modify Port Configuration
        self.logger.info("Modify Port Configuration using Port Modification Message:OFPT_PORT_MOD")
        rv = testutils.port_config_set(self.controller, of_ports[0],
                             port_config ^ ofp.OFPPC_NO_FWD, ofp.OFPPC_NO_FWD, self.logger)
        self.assertTrue(rv != -1, "Error sending port mod")

        # Verify change took place with features request
        self.logger.info("Verify the change and then set it back")
        (hw_addr, port_config2, advert) = testutils.port_config_get(self.controller, of_ports[0], self.logger)

        logMsg('logDebug',"No flood bit port " + str(of_ports[0]) + " is now " +
                           str(port_config2 & ofp.OFPPC_NO_FWD))

        self.assertTrue(port_config2 is not None, "Did not get port config2")
        self.assertTrue(port_config2 & ofp.OFPPC_NO_FWD !=
                        port_config & ofp.OFPPC_NO_FWD,
                        "Bit change did not take")

	testutils.do_barrier(self.controller)	
        self.logger.info("Sending packet to dp port " + str(ingress_port))
        self.dataplane.send(ingress_port, str(pkt))
        yes_ports = set(of_ports).difference([ingress_port,of_ports[0]])
        testutils.receive_pkt_check(self.dataplane, pkt, yes_ports, [ingress_port,of_ports[0]],
                          self,self.logger)
	
        # Set it back
        rv = testutils.port_config_set(self.controller, of_ports[0],port_config,
                             ofp.OFPPC_NO_FWD, self.logger)
        self.assertTrue(rv != -1, "Error sending port mod")
    
tc = AllplusNONforward()
_RESULT = tc.run()
