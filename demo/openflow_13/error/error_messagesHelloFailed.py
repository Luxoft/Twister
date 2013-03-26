"""
<title>HelloFailed</title>
<description>
    When the switch fails a successful hello-exchange with the controller ,
    it generates an OFPT_ERROR msg with Type Field OFPET_HELLO_FAILED
    code field OFPHFC_INCOMPATIBLE
    
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

class HelloFailed(SimpleProtocol):
    """
    When the switch fails a successful hello-exchange with the controller ,
    it generates an OFPT_ERROR msg with Type Field OFPET_HELLO_FAILED
    code field OFPHFC_INCOMPATIBLE
    """
    def setUp(self):

        #This is almost same as setUp in SimpleProtocol except that intial hello is set to false
        self.controller = controller.Controller(
            host=basic_config["controller_host"],
            port=basic_config["controller_port"])
        # clean_shutdown should be set to False to force quit app
        self.clean_shutdown = True
        #set initial hello to False
        self.controller.initial_hello=False
        self.controller.start()
        self.controller.connect(timeout=20)
        # By default, respond to echo requests
        self.controller.keep_alive = True
        if not self.controller.active:
            raise Exception("Controller startup failed")
        if self.controller.switch_addr is None:
            raise Exception("Controller startup failed (no switch addr)")
        self.logger.info("Connected " + str(self.controller.switch_addr))

    def runTest(self):

        self.logger.info("Running HelloFailed Test")

        #Send a hello message with incorrect version
        self.logger.info("Sending Hello message with incorrect version..")
        request = message.hello()
        self.logger.info("Change hello message version to 0 and send it to control plane")
        request.header.version=0
        logMsg('logDebug',"Request send to switch:")
        logMsg('logDebug',request.show())
        rv = self.controller.message_send(request)

        self.logger.info("Waiting for OFPT_ERROR message..")
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ERROR,
                                               timeout=5)
        self.assertTrue(response is not None,
                               'Switch did not reply with error message')
        logMsg('logDebug',"Response from switch:")
        logMsg('logDebug',response.show())
        self.assertTrue(response.type==ofp.OFPET_HELLO_FAILED,
                               'Error type is not HELLO_FAILED')
        self.assertTrue(response.code==ofp.OFPHFC_INCOMPATIBLE,
                               'Error code is not OFPHFC_INCOMPATIBLE')

    
tc = HelloFailed()
_RESULT = tc.run()
