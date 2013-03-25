"""
<title>ActiveCount</title>
<description>Verify that active_count counter in the Table_Stats reply , increments in accordance with the flows inserted in a table
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

class ActiveCount(SimpleDataPlane):

    """Verify that active_count counter in the Table_Stats reply , increments in accordance with the flows inserted in a table"""

    def runTest(self):

        self.logger.info("Running Table_Counter_1 test")

        of_ports = self.port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 1, "Not enough ports for test")

        #Clear switch State
        rc = testutils.delete_all_flows(self.controller, self.logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        self.logger.info("Insert any flow matching on in_port=ingress_port,action = output to egress_port T ")
        self.logger.info("Send Table_Stats, verify active_count counter is incremented in accordance")

        #Insert a flow with match on all ingress port
        (pkt, match ) = testutils.wildcard_all_except_ingress(self,of_ports)

        #Generate  Table_Stats
        testutils.verify_tablestats(self,expect_active=1)

    
tc = ActiveCount()
_RESULT = tc.run()
