import twister_logger as oflog
import pprint
import xmlrpclib

from twister_config import ResourceManager

class TwisterTestCase():
    """
    Root class twister test case wapper
    """
    def __init__(self):
        self.result='PASS'
        self.logger=oflog.getLogger('tw_testcase')
        self.config=None
        #resource allocator configuration
        self.resourceManager=None
        
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
        
    def assertEqual(self, first, second, msg=None):
        if not first==second:
            self.logger.error("** FAILED ASSERTION: " + msg)
            self.result='FAIL'
    
    def run(self):
        self.init()
        #self.postSetup()
        try:
            self.runTest()
        except Exception, e:
            raise 
            self.result='FAIL'
        self.cleanUp()
        return self.result
    
    #RESOURCE ALLOCATOR API    
    def getPortMap(self,ra_proxy,testbed,switch_name):
        if(self.resourceManager==None):
            self.resourceManager=ResourceManager()
        port_map=self.resourceManager.getResources_ra(ra_proxy,testbed,switch_name)
        return port_map                 
        
       
        
def main():
    ttc=TwisterTestCase()
    ra=xmlrpclib.ServerProxy('http://127.0.0.1:8000/ra/')
    port_map=ttc.getPortMap(ra)
    print port_map
    
if __name__ == '__main__':
    main()
            
