import twister_logger as oflog
import pprint
import xmlrpclib


class TwisterTestCase():
    """
    Root class twister test case wapper
    """
    def __init__(self):
        self.result='PASS'
        self.logger=oflog.getLogger('tw_testcase')
        self.config=None
        #resource allocator configuration
        self.raConfig={
            "RA_TESTBED":"/openflow_tb1", 
            "RA_SWITCH_PORT_MAP":"/of_switch:port_map",
            "RA_CONTROLLER_HOST":"/of_controller_1:host",
            "RA_CONTROLLER_PORT":"/of_controller_1:port",
            "RA_CONTROLLER_AGENT_HOST":"/of_controller_1:agent_host",
            "RA_CONTROLLER_AGENT_PORT":"/of_controller_1:agent_port"
        }
        
    def sig_handler(self, v1, v2):
        pass

    def init(self):
        pass
        
    def postSetup(self):

        print "### Dump Openflow configuration ###"
        if(self.config):
            pprint.pprint(self.config)
        else:
            print "None"
        print "###################################"
        
    def cleanUp(self):
        pass

    def runTest(self):
        pass

    def assertTrue(self, cond, msg):
        if not cond:
            self.logger.error("** FAILED ASSERTION: " + msg)
            self.result='FAIL'

    def assertEqual(self, first, second, msg):
        if not first==second:
            self.logger.error("** FAILED ASSERTION: " + msg)
            self.result='FAIL'

    def run(self):
        self.init()
        self.postSetup()
        try:
            self.runTest()
        except Exception, e:
            print e
        self.cleanUp()
        return self.result
        
    #RESOURCE ALLOCATOR API
    def getPortMap(self,ra_proxy):
        self.logger.warning("REVIEW THIS BEFORE RUNNING WITH TWISTER")       
        res=self.raConfig["RA_TESTBED"]+self.raConfig["RA_SWITCH_PORT_MAP"]
        pm=ra_proxy.getResource(res)
        port_map_l=pm.split(",")
        port_map={}
        for pm1 in port_map_l:
            l=pm1.split(":")
            port_map[int(l[0])]=l[1]
        return port_map
        
    def getControllerHost(self,ra_proxy):        
        self.logger.warning("REVIEW THIS BEFORE RUNNING WITH TWISTER")
        res=self.raConfig["RA_TESTBED"]+self.raConfig["RA_CONTROLLER_HOST"]
        host=ra_proxy.getResource(res)
        return host
        
    def getControllerPort(self,ra_proxy):           
        self.logger.warning("REVIEW THIS BEFORE RUNNING WITH TWISTER")
        res=self.raConfig["RA_TESTBED"]+self.raConfig["RA_CONTROLLER_PORT"]
        port=ra_proxy.getResource(res)
        return int(port)
     
    def getControllerAgentHost(self,ra_proxy):   
        self.logger.warning("REVIEW THIS BEFORE RUNNING WITH TWISTER")
        res=self.raConfig["RA_TESTBED"]+self.raConfig["RA_CONTROLLER_AGENT_HOST"]
        host=ra_proxy.getResource(res)
        return host
        
    def getControllerAgentPort(self,ra_proxy):   
        self.logger.warning("REVIEW THIS BEFORE RUNNING WITH TWISTER")
        res=self.raConfig["RA_TESTBED"]+self.raConfig["RA_CONTROLLER_AGENT_PORT"]
        port=ra_proxy.getResource(res)
        return int(port)
           
def main():
    ttc=TwisterTestCase()
    ra=xmlrpclib.ServerProxy('http://127.0.0.1:8000/ra/')
    port_map=ttc.getPortMap(ra)
    host=ttc.getControllerHost(ra)
    port=ttc.getControllerPort(ra)
    agent_host=ttc.getControllerAgentHost(ra)
    agent_port=ttc.getControllerAgentPort(ra)
    print port_map
    print host
    print port
    print agent_host
    print agent_port
    
if __name__ == '__main__':
    main()
            
