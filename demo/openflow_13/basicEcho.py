
from basicSimpleProtocol import *


class Echo(SimpleProtocol):
    """
    Test echo response with no data
    """
    def runTest(self):
        testutils.do_echo_request_reply_test(self, self.controller)
        
tc=Echo()
_RESULT=tc.run()            
