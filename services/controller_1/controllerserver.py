

from gevent import monkey
monkey.patch_all()

import sys
import os
import signal
import pickle
import gevent
import base64
import struct

from gevent.server import StreamServer
from gevent.queue import Queue,Empty

import ConfigParser

#oftest13 modules
sys.path.insert(0,"../../lib/openflow")

import of_13.parse as parse_13
import of_13.cstruct as cstruct_13
import of_13.message as message_13

#loggig handlers
###
import logging



#xmlrpc
import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer

import SocketServer
from SimpleXMLRPCServer import SimpleXMLRPCServer,SimpleXMLRPCRequestHandler
class ThreadedXMLRPCServer(SocketServer.ThreadingMixIn,SimpleXMLRPCServer): pass

import urllib2

#constants
MAX_PACKET_LEN      = 65535
ID_PKT_TRANSACT     = 0
ID_SWICTH_CONNECTED = 1

OFP_VERSION_13 = cstruct_13.OFP_VERSION

#openflow controller logger
oflogger=None

class AgentHandler:
    def __init__(self,controller):
        self.logger=getLogger()
        self.controller=controller
        
    def echo (self,msg):
        return "Replay: "+msg
        
    def start_controller_server(self,host,port):
        rv=self.controller.start_controller_server(host,port)
        return rv
        
    def shutdown(self,channel_id):
        channel=self.controller.get_switch_channel(channel_id)
        if(channel==None):
            self.logger.warning("Invalid channel id: "+ str(channel_id))
        channel.shutdown()
        return True        
        
    def connect(self,channel_id):
        rv=False        
        timeout=10;
        channel=self.controller.get_switch_channel(channel_id)        
        if(channel==None):
            self.logger.info('Waiting %d for switch to connect' % timeout)   
            t_delta=0;
            while(t_delta<timeout):
                channel=self.controller.get_switch_channel(channel_id)
                if(channel):
                    self.logger.info('switch connected')
                    rv=True
                    break;
                gevent.sleep(1)
                t_delta+=1  
        else:
            rv=True           
        return rv
        
    def transact (self,channel_id,msg_xid,raw_msg):
        raw_msg=base64.b64decode(raw_msg)
        msg_xid=int(msg_xid)
        self.logger.debug('Transact message xid: %s'%hex(msg_xid))   
        channel=self.controller.get_switch_channel(channel_id)
        if(channel==None):
            self.logger.info('Switch channel not active')   
            return ''
        else:
            msg=channel.transact(msg_xid,raw_msg)            
            if(msg==None):
                return ''
            else:
                return base64.b64encode(msg)         
                
    def poll(self,channel_id,msg_type):
        msg=None
        self.logger.debug('Poll message type: %d' % msg_type)
        channel=self.controller.get_switch_channel(channel_id)
        if(channel==None):
            self.logger.info('Switch channel not active')   
            return ''
        else:
            msg=channel.poll(msg_type)            
        if(msg==None):
            return ''
        else:
            return base64.b64encode(msg) 
            
    def message_send(self,channel_id,msg):
        raw_msg=base64.b64decode(msg)
        self.logger.debug("Sending message to channel")
        channel=self.controller.get_switch_channel(channel_id)
        if(channel==None):
            self.logger.info('Switch channel not active')   
            return False
        else:
            msg=channel.message_send(raw_msg)
        return True
    

class SwitchChannel():

    def __init__ (self,controller):
        self.controller=controller
        self.logger=getLogger()
        self.local_queue=Queue(maxsize=20)       
        self.active=False
        self.switch_socket=None
        self.transact_raw_msg=None
        self.poll_msg_type=None
        self.packets=[]
        self.max_packets=1024
        #event = agent command for this channel id
        #only one event is set per agent call       
        self.event_wait={'event_id':None,'event_data':None}
        self.timeout=10
        self.of_version=None
        
    def start (self,socket):         
        self.logger.info('Starting switch channel')       
        self.switch_socket=socket
        gevent.spawn(self.handle_channel_message, socket)        
                       
    def stop():
        pass
        
    def shutdown(self):    
        self.packets=[]
        
    def connect(self,timeout=10):
        rv=False
        self.event_wait['event_id']='switch_connected'
        if(self.switch_socket==None):
            try:
                data=self.local_queue.get(timeout)
                rv=True
            except Empty:            
                print("Switch connection timeout") 
        else:
            rv=True
        self.event_wait['event_id']=None
        return rv
       
    def transact(self,msg_xid,raw_msg):
        msg=None
        self.event_wait['event_id']=ID_PKT_TRANSACT
        self.event_wait['event_data']={'msg_xid':msg_xid,'raw_msg':raw_msg}
        self.message_send(raw_msg)
        try:
            msg=self.local_queue.get(timeout=10)        
        except Empty:            
          self.logger.info("Transact message not found") 
           
        self.event_wait['event_id'] = None
        self.event_wait['event_data'] = None
        return msg
        
        #wait 2 seconds to before poll packet list"
    def poll(self,msg_type):
        print "Pool request"
        msg=None        
        for i in range(0,len(self.packets)):
            pkt=self.packets[i][0]
            if(pkt.header.type==msg_type):
                msg=self.packets.pop(i)
                self.logger.info("POLl message found,type:%d"%msg_type)  
                break
        if(msg):
            return msg[1]    
        else:
            self.logger.info("POLL message not found") 
            return None
            
    # msg - ofp_message_t
    # rawpkt - the binary openflow message       
    def process_message_10(self,msg,rawpkt):
        
        if(msg.header.type==cstruct_10.OFPT_HELLO):
            self.message_send(message_10.hello())                            
        if(msg.header.type==cstruct_10.OFPT_ECHO_REQUEST):
            self.message_send(message_10.echo_reply()) 
            
        if(msg.header.type!=cstruct_10.OFPT_ECHO_REQUEST):
            if(len(self.packets) >= self.max_packets):
                self.logger.warning("Packet list full")
                self.packets=[]                    
            self.packets.append((msg,rawpkt))      
            
    # msg - ofp_message_t
    # rawpkt - the binary openflow message       
    def process_message_13(self,msg,rawpkt):
        
        if(msg.header.type==cstruct_13.OFPT_HELLO):
            response=message_13.hello()
            response.header.xid=msg.header.xid
            print response.show()
            self.message_send(response)                            
        if(msg.header.type==cstruct_13.OFPT_ECHO_REQUEST):
            response=message_13.echo_reply()
            response.header.xid=msg.header.xid
            self.message_send(response) 
            
        if(msg.header.type!=cstruct_13.OFPT_ECHO_REQUEST):
            if(len(self.packets) >= self.max_packets):
                self.logger.warning("Packet list full")
                self.packets=[]                    
            self.packets.append((msg,rawpkt))      
                        
    def handle_channel_message(self,socket):        
    
        if(self.event_wait['event_id']=='switch_connected'):
            self.local_queue.put(True)    
            
        self.active=True
            
        while True:
            data = socket.recv(MAX_PACKET_LEN)                
            if( not data):
                self.logger.info('Closing switch channel')                
                self.active=False
                break;
            msg=self.controller.of_message_parse(data)
            if(msg==None):
                self.logger.warning("Invalid openflow message")
                continue
                
            if ( (self.event_wait['event_id']==ID_PKT_TRANSACT) and 
                (self.event_wait['event_data']['msg_xid']==msg.header.xid) ):
                print "Transact message found, xid: %s" % hex(msg.header.xid)
                self.local_queue.put(data)
                continue 
                                                           
            # set openflow version, should be on hello message
            # assume that OFPT_HELLO=0 in all openflow versions            
            if((self.of_version == None) and (msg.header.type==0)):
                self.of_version=msg.header.version
                self.logger.info("Setting switch openflow version to: %d" % self.of_version)
                
            #Process messages       
                       
            if( (self.of_version==msg.header.version) and (self.of_version==OFP_VERSION_13)):            
                self.logger.debug("Process message for OPENFLOW_VERSION: %d" % OFP_VERSION_13)
                self.process_message_13(msg,data)
                
            else:
                self.logger.warning("Openflow version not match")
                continue                
                 
        self.active=False
        
    def message_send(self,msg):
        if self.switch_socket==None:
            self.logger.warning("No socket connection")
            return False         
               
        if type(msg) != type(""):                        
            #msg.header.xid = gen_xid()                
            outpkt = msg.pack()    
            hdr = msg.header
            self.logger.info("MSG_OUT: version: %d type: %d length: %d xid: %s" % 
                (hdr.version,hdr.type, hdr.length, hex(hdr.xid)))
        else:
            outpkt = msg
        self.switch_socket.sendall(outpkt)        
        return True           

# Custom class for controller server to parse 
# any version of openflow header

class ofp_header_t():
    def __init__(self):
        self.version = 0
        self.type = 0
        self.length = 0
        self.xid = 0    
        
    def pack(self):
        packed = ""
        packed += struct.pack("!BBHL", self.version, self.type, self.length, self.xid)
        
    def unpack(self, binaryString):
        if (len(binaryString) < 8):
            return binaryString
        fmt = '!BBHL'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.version, self.type, self.length, self.xid) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[8:]
        
    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'version: ' + str(self.version) + ' '
        outstr += prefix + 'type: ' + str(self.type) + ' '
        outstr += prefix + 'length: ' + str(self.length) + ' '
        outstr += prefix + 'xid: ' + str(hex(self.xid)) + ' '
        return outstr
        
class of_message_t():
    def __init__(self):
        self.header = None 
        self.rawmsg = None
        
class Controller():

    def __init__(self):
        self.logger=getLogger()
        self.agent_channel_server=None
        self.switch_channel_server=None
        self.agent_channel=None
        self.switch_channel=None
        
    def start(self):
        pass
        
    def close(self):
        pass
                
    def start_controller_server(self,host,port):
        if(not self.switch_channel_server):
            self.logger.info("Starting openflow switch controller server %s:%d"%(host,port))
            self.switch_channel_server=StreamServer((host,port),self.start_switch_channel)    
            self.switch_channel_server.start()
            self.logger.info("Controller server waiting for switch connection")
        return True
                
    def start_switch_channel(self,socket,address):
        if(self.switch_channel==None):
            self.switch_channel=SwitchChannel(self)
            self.switch_channel.start(socket)     
        elif (not self.switch_channel.active):
            self.switch_channel.start(socket)
            
    def get_switch_channel(self,channel_id):
        return self.switch_channel          
        
    def of_message_parse(self,pkt):
        offset = 0
        while offset < len(pkt):
            # Parse the header to get type
            # TODO: Create a custom function to parse header
            hdr = ofp_header_t()
            hdr.unpack(pkt[offset:])
            self.logger.info("MSG_IN : " + hdr.show())
            if not hdr or hdr.length == 0:
                self.logger.error("Could not parse header")
                self.logger.error("pkt len %d." % len(pkt))
                if hdr:
                    self.logger.info("hdr len %d." % hdr.length)
                    self.logger.info("hdr len %d." % hdr.version)
                return None 
            
            rawmsg = pkt[offset : offset + hdr.length]        
            msg=of_message_t()
            msg.header=hdr
            msg.rawmsg=pkt[offset : offset + hdr.length]
            return msg                                    
        # Extract the raw message bytes here (not used for controller server):
            
def getLogger():
    global oflogger
    if(oflogger):
        return oflogger
    oflogger = logging.getLogger('ofcontroller')
    oflogger.setLevel(logging.DEBUG)
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # create console handler with a higher log level
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    oflogger.addHandler(ch)    
    #create file handler which logs even debug messages
    #fh = logging.FileHandler('controller_server.log')
    #fh.setLevel(logging.DEBUG)
    #create formatter and add it to the handlers
    #fh.setFormatter(formatter)
    #add the handlers to the logger
    #logger.addHandler(fh)
    return oflogger
    
                     
def main():

    #load configuration from file
    if(len(sys.argv)!=2):    
        print "Configuration file missing"
        print "Usage python controllerserver.py configfile"
        exit(0)
    else:    
        config_file=sys.argv[1];

    config = ConfigParser.SafeConfigParser()
    config.read(config_file)        
    as_host=config.get('CONTROLLER_CONFIG', 'agent_server_host')    
    as_port=config.getint('CONTROLLER_CONFIG', 'agent_server_port')
    
    #start openflow agent server
    server = ThreadedXMLRPCServer((as_host, as_port),logRequests = False)
    print "Listening for agent on port %d..." % as_port
    controller=Controller()
    xmlrpc_handler=AgentHandler(controller)
    server.register_instance(xmlrpc_handler)
    server.serve_forever()
     
    
if __name__ == '__main__':
    main()                        
        
