"""
<title>FullTableError</title>
<description>
    Insert flow's to table 1 till it's full and wait for error message OFPMFC_TABLE_FULL
    
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

class FullTableError(SimpleDataPlane):
    """
    Insert flow's to table 1 till it's full and wait for error message OFPMFC_TABLE_FULL
    """
    def runTest(self):
        self.logger.info("Running FullTableError test")
        self.logger.info("Insert flows to table 1 untill TABLE FULL error is received")
        of_ports = self.port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 0, "Not enough ports for test")
        self.logger.info("Clear the switch state, delete all flows")
        rc = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        for i in range(1, 10):
            for j in range(1, 10):
                for k in range(1, 10):
                    for l in range(1,10):
                        portmatch = match.in_port(of_ports[0])
                        dstmatch = match.eth_dst(parse.parse_mac("00:01:" + str(l) + ":" +str(k) + ":" +str(j)+ ":" + str(i)))
                        request = message.flow_mod()
                        request.match_fields.tlvs.append(dstmatch)
                        request.buffer_id = 0xffffffff
                        request.priority = 1
                        inst = instruction.instruction_apply_actions()
                        vid_act = action.action_set_field()
                        field_2b_set = match.ipv4_src(ipaddr.IPv4Address('10.' + str(i) + '.10.10'))
                        vid_act.field = field_2b_set
                        inst.actions.add(vid_act)

                        act_out = action.action_output()
                        act_out.port = of_ports[1]
                        inst.actions.add(act_out)
                        request.instructions.add(inst)
                        rv = self.controller.message_send(request)
                        self.assertTrue(rv != -1, "Error installing flow mod")

                        response,_ = self.controller.poll(ofp.OFPT_ERROR, 0.02 )
                        if response is not None:
                            logMsg('logDebug',"Response from switch:")
                            logMsg('logDebug',response.show())
                            rc = testutils.delete_all_flows(self.controller, self.logger)
                            self.assertEqual(str(response.code), "1", 'Switch did not return TABLE_FULL')
                            self.assertEqual(rc, 0, "Failed to delete all flows")
                            return
        self.assertEqual(1,0,"Table did not get full or switch did not return error")

    
tc = FullTableError()
_RESULT = tc.run()
