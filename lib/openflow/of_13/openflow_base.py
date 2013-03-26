import sys
import logging
import trace
from xmlrpclib import ServerProxy
import random

import ce_libs.openflow.of_13.match as match
import ce_libs.openflow.of_13.controller as controller
import ce_libs.openflow.of_13.cstruct as ofp
import ce_libs.openflow.of_13.message as message
import ce_libs.openflow.of_13.action as action
import ce_libs.openflow.of_13.instruction as instruction
import ce_libs.openflow.of_13.parse as parse
import ce_libs.openflow.of_13.dataplane as dataplane
import ce_libs.openflow.of_13.testutils as testutils
import ce_libs.openflow.of_13.twister_testcase as testcase
import ce_libs.openflow.of_13.meter as meter

import ipaddr

TEST_VID_DEFAULT = 2
IPV6_ETHERTYPE = 0x86dd 
IPV4_ETHERTYPE = 0x0800
ETHERTYPE_VLAN = 0x8100
ETHERTYPE_MPLS = 0x8847
TCP_PROTOCOL = 0x6
UDP_PROTOCOL = 0x11
ICMPV6_PROTOCOL = 0x3a 

class SimpleProtocol(testcase.TwisterTestCase):
    """
    Root class for setting up the controller
    """
    def __init__(self,testbed=None,ra_proxy=None):
    
        print ra_proxy
        print testbed
        
        testcase.TwisterTestCase.__init__(self)
        if(testbed==None):
            self.testbed='openflow_testbed'
        else:
            self.testbed=testbed
       
        if (isinstance(ra_proxy, ServerProxy)):
            self.ra_proxy=ra_proxy
        else:            
            self.ra_proxy=ServerProxy('http://127.0.0.1:8000/ra/')
 
    def sig_handler(self, v1, v2):
        self.logger.critical("Received interrupt signal; exiting")
        print "Received interrupt signal; exiting"
        self.clean_shutdown = False
        self.cleanUp()
        sys.exit(1)

    def init(self):
            
        #signal.signal(signal.SIGINT, self.sig_handler)
        self.logger.info("** START TEST CASE " + str(self))
                    
        self.controller = controller.Controller(ra_proxy=self.ra_proxy,testbed=self.testbed,controller_name='controller_1')        
        self.port_map=self.getPortMap(self.ra_proxy,self.testbed,'switch')
        print "port_map: "+str(self.port_map) 
        
        # clean_shutdown should be set to False to force quit app
        self.clean_shutdown = True
        self.controller.start()
        #@todo Add an option to wait for a pkt transaction to ensure version
        # compatibilty?
        self.controller.connect(timeout=20)
        if not self.controller.active:
            print "Controller startup failed; exiting"
            sys.exit(1)
        self.logger.info("Connected " + str(self.controller.switch_addr))

    def cleanUp(self):
        self.logger.info("** END TEST CASE " + str(self))
        self.controller.shutdown()
        #@todo Review if join should be done on clean_shutdown
        if self.clean_shutdown:
            self.controller.join()

    def runTest(self):
        # Just a simple sanity check as illustration
        self.logger.info("Running simple proto test")
        self.assertTrue(self.controller.switch_socket is not None,
                        str(self) + 'No connection to switch')

    
class SimpleDataPlane(SimpleProtocol):
    """
    Root class that sets up the controller and dataplane
    """
    def init(self):
        SimpleProtocol.init(self)
        self.dataplane = dataplane.DataPlane()

        for of_port, ifname in self.port_map.items():
            self.dataplane.port_add(ifname, of_port)

    def cleanUp(self):
        self.logger.info("Cleanup for simple dataplane test")
        SimpleProtocol.cleanUp(self)
        self.dataplane.kill(join_threads=self.clean_shutdown)
        self.logger.info("Cleanup done")

    def runTest(self):
        self.assertTrue(self.controller.switch_socket is not None,
                        str(self) + 'No connection to switch')
        # self.dataplane.show()
        # Would like an assert that checks the data plane

def main():
    tc_1=SimpleProtocol()
    tc_1.run()
    tc_2=SimpleDataPlane()
    tc_2.run()
    
if __name__ == '__main__':
    main()
                    
