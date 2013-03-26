"""
<title>MeterCounters</title>
<description>
    Insert meter_mod, flow_mod, send packets, verify counters are incremented
    
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

class MeterCounters(SimpleDataPlane):
    """
    Insert meter_mod, flow_mod, send packets, verify counters are incremented
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
        msg.flags = ofp.OFPMF_KBPS
        band1 = meter.meter_band_drop()
        band1.rate = 1024
        band1.burst_size = 12
        msg.bands.add(band1)
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',msg.show())
        rv = self.controller.message_send(msg)
        self.assertTrue(rv != -1, "Failed to insert test meter")

        #Generate packet and match
        pkt = testutils.simple_tcp_packet()
        match = parse.packet_to_flow_match(pkt)

        #Insert Flowmod and assign meter
        self.logger.info("Insert flowmod for meter")
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
        self.logger.info("Request meter stats")
        msg = message.meter_stats_request()
        msg.meter_id = 1
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',msg.show())
        rv, _ = self.controller.transact(msg, timeout= 2)
        self.assertTrue(rv is not None, "Switch did not reply")
        logMsg('logDebug',"Response from switch:")
        logMsg('logDebug',rv.show())
        for item in rv.stats:
            self.assertEqual(str(item.packet_in_count), "1", "Flow_count must be 1")
            self.assertEqual(str(item.byte_in_count), "100", "Flow_count must be 1")

    
tc = MeterCounters()
_RESULT = tc.run()
