
import os, sys
sys.path.append(os.getenv('TWISTER_PATH') + '/.twister_cache/')
from ce_libs import *

import message
import cstruct
import controller
import oflog

#

class BasicEcho():

    def __init__(self):
        self.logger=oflog.OFLog()
        self.config=open_flow_config
        self.statusType=self.config['test_status']
        self.status=self.statusType['NOTEXEC']

    def testInit(self):
        self.logger.info("***  %s start ***\n" % (self.__class__.__name__))
        self.status='STARTED'
        host=open_flow_config['controller']['host']
        port=open_flow_config['controller']['port']
        self.controller = controller.Controller(host,port)
        self.controller.start()
        self.controller.connect(timeout=20)

    def testEnd(self):
        self.controller.kill()
        self.logger.info("*** %s done with status: %s ***\n" % (self.__class__.__name__,self.status))

    def testStart(self):
        self.testInit()
        self.status=self.runTest()
        self.testEnd()
        return self.status

    def runTest(self):
        request = message.echo_request()
        response, pkt = self.controller.transact(request)
        self.logger.debug(request.show())
        self.logger.debug(response.show())

        if(response.header.type!=cstruct.OFPT_ECHO_REPLY):
            self.logger.info('Response is not echo_reply')
            return self.statusType['FAIL']
        if(len(response.data)> 0):
            self.logger.info('response data non-empty')
            return self.statusType['FAIL']
        return self.statusType['PASS']

# Run!
test = BasicEcho()
_RESULT = test.testStart()
print _RESULT

#
