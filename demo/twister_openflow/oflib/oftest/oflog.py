
import logging

class OFLog:
    def __init__(self):
        self.level=logging.NOTSET
        self.oflogger=logging.getLogger('openflow_log')
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.oflogger.addHandler(ch)
        self.oflogger.setLevel(logging.DEBUG)  
                
    def setLevel(self,level):
        self.level=level
        self.oflogger.setLevel(level)
                
    def debug(self,msg):         
        self.logMsg(msg,logging.DEBUG)           

    def info(self,msg):
        self.logMsg(msg,logging.INFO)
            
    def warning(self,msg):        
        self.logMsg(msg,logging.WARNING)

    def warn(self,msg):
        self.logMsg(msg,logging.WARNING)
        
    def error(self,msg):        
        self.logMsg(msg,logging.ERROR)
            
    def critical(self,msg):        
        self.logMsg(msg,logging.CRITICAL)
            
    def logMsg(self,msg,level):
        #self.oflogger.debug(msg)
        print msg
        
if __name__ == "__main__":
    log=OFLog()
    log.debug("Hello")
    
    
