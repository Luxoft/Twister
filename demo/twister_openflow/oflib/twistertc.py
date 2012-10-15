import oftest.oflog as oflog
import pprint

class TwisterTestCase():
    """
    Root class twister test case wapper
    """    
    def __init__(self):
        self.result='PASS'
        self.logger=oflog.OFLog()
        self.config=None
    def sig_handler(self, v1, v2):
        pass
        
    def setUp(self):
        pass
        
    def postSetup(self):
        
        print "### Dump Openflow configuration ###"
        if(self.config):
            pprint.pprint(self.config)
        else:
            print "None"
        print "###################################"
    def tearDown(self):
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
        self.setUp()
        self.postSetup()     
        try:   
            self.runTest()
        except Exception, e:
            print e
        self.tearDown()
        return self.result

            
