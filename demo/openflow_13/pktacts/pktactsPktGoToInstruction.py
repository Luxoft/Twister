"""
<title>PktGoToInstruction</title>
<description>
    Generate pkt, insert matching flow, direct from table 0 to table 1 and output to port
    
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

class PktGoToInstruction(SimpleDataPlane):
    """
    Generate pkt, insert matching flow, direct from table 0 to table 1 and output to port
    """
    def runTest(self):
        self.logger.info("Running PktGoToInstruction multiple tables test")
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
        self.logger.info("Generate flow mod for table 0 to direct to table 1")
        portmatch = match.in_port(ingress_port)
        srcmatch = match.eth_src(parse.parse_mac("00:06:07:08:09:0a"))
        dstmatch = match.eth_dst(parse.parse_mac("00:01:02:03:04:05"))
        request = message.flow_mod()
        request.match_fields.tlvs.append(portmatch)
        request.match_fields.tlvs.append(srcmatch)
        request.match_fields.tlvs.append(dstmatch)
        request.buffer_id = 0xffffffff
        request.table_id = 0

        inst = instruction.instruction_goto_table()
        inst.table_id = 1
        request.instructions.add(inst)
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',request.show())
        self.logger.info("Inserting flow for table 0")
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, "Error installing flow mod")

        #Send a packet a verify that it is not received on any port
        self.dataplane.send(ingress_port, str(pkt))
        testutils.receive_pkt_check(self.dataplane, pkt, [], of_ports,
                              self,self.logger)

        #Insert flow_mod matching packet in table 1 and output to port
        self.logger.info("Insert second flow mod to table 1 and output to port")
        request = message.flow_mod()
        request.match_fields.tlvs.append(portmatch)
        request.match_fields.tlvs.append(srcmatch)
        request.match_fields.tlvs.append(dstmatch)
        request.buffer_id = 0xffffffff
        request.table_id = 1

        act = action.action_output()
        act.port = egress_port
        inst = instruction.instruction_apply_actions()
        inst.actions.add(act)
        request.instructions.add(inst)
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',request.show())
        self.logger.info("Inserting flow for table 1")
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, "Error installing flow mod")

        #Send packet to ingress_port and verify if it is received on egress_port
        self.dataplane.send(ingress_port, str(pkt))
        testutils.receive_pkt_check(self.dataplane, pkt, [egress_port], [],
                              self,self.logger)

    
tc = PktGoToInstruction()
_RESULT = tc.run()
