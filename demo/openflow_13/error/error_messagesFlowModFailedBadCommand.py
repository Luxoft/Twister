"""
<title>FlowModFailedBadCommand</title>
<description>
    Unknown command.
    When the flow_mod msg request is sent by the controller with
    some invalid command , the switch responds with an OFPT_ERROR msg ,
    type field OFPET_FLOW_MOD_FAILED and code field OFPFMFC_BAD_COMMAND 
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

class FlowModFailedBadCommand(SimpleProtocol):
    """
    Unknown command.
    When the flow_mod msg request is sent by the controller with
    some invalid command , the switch responds with an OFPT_ERROR msg ,
    type field OFPET_FLOW_MOD_FAILED and code field OFPFMFC_BAD_COMMAND """

    def runTest(self):
        msg = message.flow_mod()
        msg.command = 8

        packed=msg.pack()

        rv=self.controller.message_send(packed)
        self.assertTrue(rv==0,"Unable to send the message")
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ERROR,
                                               timeout=5)
        self.assertTrue(response is not None,
                                'Switch did not reply with error messge')
        logMsg('logDebug',"Response from switch:")
        logMsg('logDebug',response.show())
        self.assertTrue(response.type==ofp.OFPET_FLOW_MOD_FAILED,
                               'Error type is not OFPET_FLOW_MOD_FAILED')
        self.assertTrue(response.code==ofp.OFPFMFC_BAD_COMMAND,
                               'Error code is not OFPFMFC_BAD_COMMAND')

    
tc = FlowModFailedBadCommand()
_RESULT = tc.run()
