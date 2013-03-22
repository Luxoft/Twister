import sys
#remove sys.path.append before running in twister
sys.path.append("/home/dancioata/twister/.twister_cache/EP-1001")
import logging

import trace

import unittest

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


import ipaddr

class SimpleProtocol(testcase.TwisterTestCase):
    """
    Root class for setting up the controller
    """

    def sig_handler(self, v1, v2):
        self.logger.critical("Received interrupt signal; exiting")
        print "Received interrupt signal; exiting"
        self.clean_shutdown = False
        self.cleanUp()
        sys.exit(1)

    def init(self):
            
        #signal.signal(signal.SIGINT, self.sig_handler)
        self.logger.info("** START TEST CASE " + str(self))
        #create or use existing proxy
        try:            
            from ce_libs import ce_proxy
            self.ra_proxy=ce_proxy
        except:
            import xmlrpclib
            self.ra_proxy=xmlrpclib.ServerProxy('http://127.0.0.1:8000/ra/')
            
        #replace here the testbed with currenttestbed                     
        self.controller = controller.Controller(ra_proxy=self.ra_proxy,testbed='openflow_testbed',controller_name='controller_1')
        
        self.port_map=self.getPortMap(self.ra_proxy,'openflow_testbed','switch')
        
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

    def assertTrue(self, cond, msg):
        if not cond:
            self.logger.error("** FAILED ASSERTION: " + msg)        

#tc=SimpleProtocol()
#_RESULT=tc.run()
