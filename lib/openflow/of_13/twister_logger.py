import logging

tw_openflow_logger=None

def getLogger(logger_name,filehandler=None):
    global tw_openflow_logger
    
    if(tw_openflow_logger): 
        return tw_openflow_logger
        
    logger = logging.getLogger('openflow 1.3')
    logger.setLevel(logging.DEBUG)
        
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')    
    # create file handler which logs even debug messages
    if(filehandler):        
        fh = logging.FileHandler('controller_server.log')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)    
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(ch)
    tw_openflow_logger=logger
    
    return tw_openflow_logger
    

