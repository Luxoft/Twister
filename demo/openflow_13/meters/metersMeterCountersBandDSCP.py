"""
<title>MeterCountersBandDSCP</title>
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

class MeterCountersBandDSCP(SimpleDataPlane):
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
        self.logger.info("Insert meter mod")
        msg = message.meter_mod()
        msg.command = ofp.OFPMC_ADD
        msg.meter_id = 1
        msg.flags = ofp.OFPMF_PKTPS
        band1 = meter.meter_band_dscp_remark()
        band1.rate = 2
        band1.burst_size = 2
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
        request.match_fields = match
        inst = instruction.instruction_meter_table()
        inst.meter_id = 1
        request.instructions.add(inst)
        request.buffer_id = 0xffffffff
        request.priority = 1000
        self.logger.info("Adding flow ")
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',request.show())
        rv = self.controller.message_send(request)
        self.assertTrue(rv != -1, "Failed to insert test flow")

        #Send packet to matching flow
        self.dataplane.send(ingress_port, str(pkt))

        #Request meter stats
        self.logger.info("Verify stats")
        msg = message.meter_stats_request()
        msg.meter_id = 1
        rv, _ = self.controller.transact(msg, timeout= 2)
        self.assertTrue(rv is not None, "Switch did not reply")
        for item in rv.stats:
            self.assertEqual(str(item.bands.packet_band_count), "1", "Packet_count must be 1")
            self.assertEqual(str(item.bands.byte_band_count), "100", "Bytecount_count must be 100")

    
tc = MeterCountersBandDSCP()
_RESULT = tc.run()
