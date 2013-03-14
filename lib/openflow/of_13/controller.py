import xmlrpclib
import time
import base64
import logging

import message as message

from message import *
from parse import *
from ofutils import *

agent_config = {"agent_host":"127.0.0.1", "agent_port":7711}

class Controller():
    def __init__(self,host,port):    
        self.host=host
        self.port=port
        proxy_str="http://%s:%d/" % (agent_config["agent_host"],agent_config["agent_port"])        
        self.proxy = xmlrpclib.ServerProxy(proxy_str)
        self.channel_id=1
        self.logger = logging.getLogger("controller")
        
        #back compatibility with oftest 1.0
        self.switch_addr=None
        self.switch_socket="None"
        
    #back compatibility functions with oftest 1.0
    
    def shutdown(self):
        self.proxy.shutdown(self.channel_id)
        
        
    def join(self):
        pass
        
    def register(self, msg_type, handler):
        pass
                
    def start(self,timeout=20):
        try:
            self.proxy.start_controller_server('0.0.0.0',6633)
        except:
            self.logger.warning("Unable to connect to: %s:%d" % 
                (agent_config["agent_host"],agent_config["agent_port"]))
            
    def connect(self,timeout=20):
        rv=self.proxy.connect(self.channel_id)
        self.active=rv
        if(rv==True):
            self.logger.info("Switch connected")
            self.switch_addr=True
        else:
            self.logger.info("Switch not connected")
            self.switch_addr=None
            
    def transact(self,msg,timeout=20):
        if type(msg) != type(""):                        
            msg.header.xid = gen_xid()                
            outpkt = msg.pack()                            
        else:
            outpkt = msg     
        """
        Encode message as base64 to avoid xmlrpc exceptios
        msg_xid is a long int and excetion occured, convert to string
        """    
        request=base64.b64encode(outpkt)
        s_msg_xid=str(msg.header.xid)
        res_msg = self.proxy.transact(self.channel_id,s_msg_xid,request)
        #decode reply
        res_msg=base64.b64decode(res_msg)
        replay, pkt=self.of_message_parse(res_msg)
        #print replay.show()
        return (replay, pkt)
        
    def poll(self,exp_msg,timeout=20):
        self.logger.debug("Poll request")
        raw_msg=self.proxy.poll(self.channel_id, exp_msg)        
        if(raw_msg==''):
            return (None,None)
        msg=base64.b64decode(raw_msg)
        pkt,rmsg=self.of_message_parse(msg)        
        return (pkt,rmsg)
        
    def message_send(self,msg):
        if type(msg) != type(""):                        
            msg.header.xid = gen_xid()                
            outpkt = msg.pack()                            
        else:
            outpkt = msg     
            
        request=base64.b64encode(outpkt)
        self.proxy.message_send(self.channel_id, request)    
        return 0    
        
    def of_message_parse(self,pkt):
        offset = 0
        if(pkt==None):
            return (None,None)
        while offset < len(pkt):
            # Parse the header to get type
            hdr = of_header_parse(pkt[offset:])
            if not hdr or hdr.length == 0:
                self.logger.error("Could not parse header")
                self.logger.error("pkt len %d." % len(pkt))
                if hdr:
                    self.logger.error("hdr len %d." % hdr.length)                
                self.kill()
                return None,None

            # Extract the raw message bytes
            if (offset + hdr.length) > len(pkt):
                break
            rawmsg = pkt[offset : offset + hdr.length]
            offset += hdr.length
            if(hdr.type!=OFPT_PACKET_IN):
                self.logger.debug("Msg in: buf len %d. hdr.type %s. hdr.len %d" %
                              (len(pkt), ofp_type_map[hdr.type], hdr.length))
            if hdr.version != OFP_VERSION:
                self.logger.error("Version %d does not match OFTest version %d"
                                  % (hdr.version, OFP_VERSION))
                return (None,None)
                
            msg = of_message_parse(rawmsg)
            
            if not msg:
                self.parse_errors += 1
                self.logger.warn("Could not parse message")
                return (None,None)
                
            return (msg,rawmsg)            
            
