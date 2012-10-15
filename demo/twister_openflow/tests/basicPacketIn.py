
from ce_libs import *

try:
    basic.basic_config=getOpenflowConfig(globEpName)
    basic.basic_port_map=basic.basic_config['port_map']
except:
    print "Error: Invalid configuration for EPNAME: " + str(globEpName)

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
        rc = delete_all_flows(self.controller, basic_logger)
        self.assertEqual(rc, 0, "Failed to delete all flows")

        for of_port in basic_port_map.keys():
            basic_logger.info("PKT IN test, port " + str(of_port))
            pkt = simple_tcp_packet()
            self.dataplane.send(of_port, str(pkt))
            #@todo Check for unexpected messages?
            (response, raw) = self.controller.poll(ofp.OFPT_PACKET_IN, 2)

            self.assertTrue(response is not None,
                            'Packet in message not received on port ' +
                            str(of_port))
            if str(pkt) != response.data:
                basic_logger.debug("pkt  len " + str(len(str(pkt))) +
                                   ": " + str(pkt))
                basic_logger.debug("resp len " +
                                   str(len(str(response.data))) +
                                   ": " + str(response.data))

            self.assertEqual(str(pkt), response.data,
                             'Response packet does not match send packet' +
                             ' for port ' + str(of_port))


tc = PacketIn()
_RESULT = tc.run()
