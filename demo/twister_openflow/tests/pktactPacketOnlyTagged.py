
from ce_libs import *

try:
    pktact.pa_config = getOpenflowConfig(globEpName)
    pktact.pa_port_map = pktact.pa_config['port_map']
except:
    print 'Error: Invalid configuration for EPNAME: ' + str(globEpName)

class PacketOnlyTagged(basic.DataPlaneOnly):
    """
    Just send a packet thru the switch
    """
    def runTest(self):
        vid = test_param_get(self.config, 'vid', default=TEST_VID_DEFAULT)
        pkt = simple_tcp_packet(dl_vlan_enable=True, dl_vlan=vid)
        of_ports = pa_port_map.keys()
        of_ports.sort()
        ing_port = of_ports[0]
        pa_logger.info("Sending packet to " + str(ing_port))
        pa_logger.debug("Data: " + str(pkt).encode('hex'))
        self.dataplane.send(ing_port, str(pkt))


tc = PacketOnlyTagged()
_RESULT = tc.run()
