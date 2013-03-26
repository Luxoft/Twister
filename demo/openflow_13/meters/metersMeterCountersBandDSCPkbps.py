"""
<title>MeterCountersBandDSCPkbps</title>
<description>
    Insert meter_mod, flow_mod, send packets, verify DSCP remark band counters are incremented
    
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

class MeterCountersBandDSCPkbps(SimpleDataPlane):
    """
    Insert meter_mod, flow_mod, send packets, verify DSCP remark band counters are incremented
    """
    def runTest(self):
        self.logger.info("Running MeterCounters test")

        #Delete all meters
        self.logger.info("Delete all meters")
        rc = testutils.delete_all_meters(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all meters")

        #Delete all flows
        self.logger.info("Delete all flows")
        rc = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        of_ports = self.port_map.keys()
        of_ports.sort()
        ingress_port = of_ports[0]

        #Insert meter_mod
        self.logger.info("Generate meter mod")
        msg = message.meter_mod()
        msg.command = ofp.OFPMC_ADD
        msg.meter_id = 1
        msg.flags = ofp.OFPMF_KBPS
        band1 = meter.meter_band_dscp_remark()
        band1.rate = 2
        band1.prec_level = 1
        msg.bands.add(band1)
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',msg.show())
        rv = self.controller.message_send(msg)
        self.assertTrue(rv != -1, "Failed to insert test meter")

        #Generate packet and match
        pkt = testutils.simple_tcp_packet()
        match = parse.packet_to_flow_match(pkt)

        #Insert Flowmod and assign meter
        request = message.flow_mod()
        inst = instruction.instruction_meter_table()
        inst.meter_id = 1
        request.buffer_id = 0xffffffff
        request.priority = 1000
        inst2 = instruction.instruction_apply_actions()
        act = action.action_output()
        act.port = of_ports[1]
        act.max_len = ofp.OFPCML_NO_BUFFER
        inst2.actions.add(act)
        request.instructions.add(inst2)
        request.instructions.add(inst)
        self.logger.info("Adding flow ")
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',request.show())
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, "Failed to insert test flow")
        testutils.do_barrier(self.controller)
        #Send packet to matching flow
        for pkt in range(120):
            self.dataplane.send(ingress_port, str(pkt))

        #Request meter stats
        self.logger.info("Verify meter stats")
        msg = message.meter_stats_request()
        msg.meter_id = 1
        rv, _ = self.controller.transact(msg, timeout= 2)
        self.assertTrue(rv is not None, "Switch did not reply")
        for item in rv.stats:
            self.assertTrue(item.bands.packet_band_count != 0, "Packet_count must be different than 0")
            self.assertTrue(item.bands.byte_band_count != 0, "Byte_count must be different than 0")

    
tc = MeterCountersBandDSCPkbps()
_RESULT = tc.run()
