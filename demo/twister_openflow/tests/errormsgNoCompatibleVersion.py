
from ce_libs import *

try:
    errormsg.config=getOpenflowConfig(globEpName)
    errormsg.errormsg_port_map= pktact.pa_config['port_map']
except:
    print "Error: Invalid configuration for EPNAME: " + str(globEpName)

#class body
class NoCompatibleVersion(basic.SimpleProtocol):
    """
    When the reason for a Hello failing , 
    is due to version incompatibility between switch and controller , 
    then switch generates OFPT_ERROR msg with Type Field OFPET_HELLO_FAILED and code field 
    OFPHFC_INCOMPATIBLE
    """
    def setUp(self):
        """
        setUp is almost identical with Simple protocol, only
        set initial_hello=False        
        """
        self.logger = errormsg_logger
        self.config = errormsg_config
        signal.signal(signal.SIGINT, self.sig_handler)
        errormsg_logger.info("** START TEST CASE " + str(self))
        self.controller = controller.Controller(
            host=errormsg_config["controller_host"],
            port=errormsg_config["controller_port"])
        # clean_shutdown should be set to False to force quit app
        self.clean_shutdown = True
        #set initial hello to False
        self.controller.initial_hello=False
        self.controller.start()
        #@todo Add an option to wait for a pkt transaction to ensure version
        # compatibilty?
        self.controller.connect(timeout=20)
        if not self.controller.active:
            raise Exception("Controller startup failed")
        if self.controller.switch_addr is None: 
            raise Exception("Controller startup failed (no switch addr)")
        errormsg_logger.info("Connected " + str(self.controller.switch_addr))
        
    def runTest(self):
        errormsg_logger.info("Running IncompatibleVersion ")                
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_HELLO,         
                                               timeout=5)
        request = message.hello()                                               
        errormsg_logger.info("Change hello message version to 0 and send it to control plane")
        request.header.version=0
        rv = self.controller.message_send(request)      
          
        errormsg_logger.info("Expecting OFPT_ERROR message")
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ERROR,         
                                               timeout=5)
                
        self.assertTrue(response is not None, 
                               'Switch did not replay with error message') 
        self.assertTrue(response.type==ofp.OFPET_HELLO_FAILED, 
                               'Message field type is not HELLO_FAILED') 
        self.assertTrue(response.code==ofp.OFPHFC_INCOMPATIBLE, 
                               'Message field code is not OFPHFC_INCOMPATIBLE') 


tc = NoCompatibleVersion()
_RESULT = tc.run()
