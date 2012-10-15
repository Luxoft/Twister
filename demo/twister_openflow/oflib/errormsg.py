"""
Error messages

"""

import time
import signal
import sys
import logging

import unittest
import random

import oftest.controller as controller
import oftest.cstruct as ofp
import oftest.message as message
import oftest.dataplane as dataplane
import oftest.action as action

from testutils import *
import basic

from twistertc import *
import oftest.oflog as oflog
from of_config import openflow_config as config

#@var basic_port_map Local copy of the configuration map from OF port
# numbers to OS interfaces
errormsg_port_map = None
#@var basic_logger Local logger object
errormsg_logger = None
#@var basic_config Local copy of global configuration data
errormsg_config = None

test_prio = {}

errormsg_logger = logging.getLogger("basic")
errormsg_logger.info("Initializing test set")
errormsg_port_map = config["port_map"]
errormsg_config = config

def test_set_init(config):
    """
    Set up function for basic test classes

    @param config The configuration dictionary; see oft
    """
    
    basic.test_set_init(config)
    
    global errormsg_port_map
    global errormsg_logger
    global errormsg_config

    errormsg_logger = logging.getLogger("basic")
    errormsg_logger.info("Initializing test set")
    errormsg_port_map = config["port_map"]
    errormsg_config = config
#    print str(config)


class NoCompatibleVersion(basic.SimpleProtocol):
    """
    When the reason for a Hello failing , 
    is due to version incompatibility between switch and controller , 
    then switch generates OFPT_ERROR msg with Type Field OFPET_HELLO_FAILED and code field 
    OFPHFC_INCOMPATIBLE
    """
    def setUp(self):
        """
        setUp is almost identical with Simple protocol, only
        set initial_hello=False        
        """
        self.logger = errormsg_logger
        self.config = errormsg_config
        signal.signal(signal.SIGINT, self.sig_handler)
        errormsg_logger.info("** START TEST CASE " + str(self))
        self.controller = controller.Controller(
            host=errormsg_config["controller_host"],
            port=errormsg_config["controller_port"])
        # clean_shutdown should be set to False to force quit app
        self.clean_shutdown = True
        #set initial hello to False
        self.controller.initial_hello=False
        self.controller.start()
        #@todo Add an option to wait for a pkt transaction to ensure version
        # compatibilty?
        self.controller.connect(timeout=20)
        if not self.controller.active:
            raise Exception("Controller startup failed")
        if self.controller.switch_addr is None: 
            raise Exception("Controller startup failed (no switch addr)")
        errormsg_logger.info("Connected " + str(self.controller.switch_addr))
        
    def runTest(self):
        errormsg_logger.info("Running IncompatibleVersion ")                
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_HELLO,         
                                               timeout=5)
        request = message.hello()                                               
        errormsg_logger.info("Change hello message version to 0 and send it to control plane")
        request.header.version=0
        rv = self.controller.message_send(request)      
          
        errormsg_logger.info("Expecting OFPT_ERROR message")
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ERROR,         
                                               timeout=5)
                
        self.assertTrue(response is not None, 
                               'Switch did not replay with error message') 
        self.assertTrue(response.type==ofp.OFPET_HELLO_FAILED, 
                               'Message field type is not HELLO_FAILED') 
        self.assertTrue(response.code==ofp.OFPHFC_INCOMPATIBLE, 
                               'Message field code is not OFPHFC_INCOMPATIBLE') 
                               
class BadVersion(basic.SimpleProtocol):
    """
    When the header in the  request msg  
    contains a version field which is not supported by the switch , 
    it generates OFPT_ERROR_msg with Type field OFPET_BAD_REQUEST 
    and code field OFPBRC_BAD_VERSION
    """
    
    def runTest(self):
    
        request=message.echo_request();
        request.header.version=0        
        rv=self.controller.message_send(request)
        
        self.assertTrue(rv==0,"Unable to send the message")
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ERROR,         
                                               timeout=5)
        self.assertTrue(response is not None, 
                               'Switch did not replay with error message')
        self.assertTrue(response.type==ofp.OFPET_BAD_REQUEST, 
                               'Message field type is not OFPET_BAD_REQUEST') 
        self.assertTrue(response.type==ofp.OFPET_BAD_REQUEST, 
                               'Message field type is not OFPBRC_BAD_VERSION')

class BadType1(basic.SimpleProtocol):
    """
    When the controller sends a request message which 
    is not understood by the switch , it generates error 
    a OFPT_ERROR msg with Type Field OFPET_BAD_REQUEST
    Added OFPT_BAD_TYPE in cstruct.py
    """
    def runTest(self):
    
        msg=message.echo_request();
        msg.pack();     
        #use cstruct module for header to use pack with bool argument
        header=ofp.ofp_header() 
        header.length=msg.header.length;
        #change message header type to non existent type
        header.type = 45       
        packed = header.pack(False)        
        
        rv=self.controller.message_send(packed)
        
        self.assertTrue(rv==0,"Unable to send the message")
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ERROR,         
                                               timeout=5)
        self.assertTrue(response is not None, 
                               'Switch did not replay with error message')
        self.assertTrue(response.type==ofp.OFPET_BAD_REQUEST, 
                               'Message field type is not OFPET_BAD_REQUEST') 
        self.assertTrue(response.type==ofp.OFPET_BAD_REQUEST, 
                               'Message field type is not OFPBRC_BAD_TYPE')
        
class BadStats(basic.SimpleProtocol):
    """
    ofp_stats_request.type not supported.

    When the request type sent by the controller is not supported by switch 
    (e.g some switch do not support queue stats request) , 
    the switch generates OFPT_ERROR msg with type Field OFPET_BAD_REQUEST 
    and code field OFPBRC_BAD_STAT
    """
    def runTest(self):
        request = message.queue_stats_request()
        request.port_no  = ofp.OFPP_ALL
        request.queue_id = ofp.OFPQ_ALL
        rv=self.controller.message_send(request)
        
        self.assertTrue(rv==0,"Unable to send the message")
         
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ERROR,         
                                               timeout=5)
        self.assertTrue(response is not None, 
                               'Switch did not replay with error messge')
        self.assertTrue(response.type==ofp.OFPET_BAD_REQUEST, 
                               'Message field type is not OFPET_BAD_REQUEST') 
        self.assertTrue(response.type==ofp.OFPBRC_BAD_STAT, 
                               'Message field code is not OFPBRC_BAD_STAT')
                               
class BadLength1(basic.SimpleProtocol):    
    """
    Wrong request length for type. 
    
    When the length field in the header of the stats request is wrong , 
    switch generates an OFPT_ERROR msg with type field OFPET BAD_REQUEST 
    and code field OFPBRC_BAD_LEN
    """
    def runTest(self):
        #in the module message at pack time the length is computed
        #avoid this by using cstruct module
        stats_request = ofp.ofp_stats_request()
        header=ofp.ofp_header() 
        header.type = ofp.OFPT_STATS_REQUEST
        # normal the header length is 12 change it to 18
        header.length=18;
        packed=header.pack()+stats_request.pack()
        rv=self.controller.message_send(packed)
        self.assertTrue(rv==0,"Unable to send the message")
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ERROR,         
                                               timeout=5)
        self.assertTrue(response is not None, 
                               'Switch did not replay with error messge')
        self.assertTrue(response.type==ofp.OFPET_BAD_REQUEST, 
                               'Message field type is not OFPET_BAD_REQUEST') 
        self.assertTrue(response.type==ofp.OFPBRC_BAD_LEN, 
                               'Message field code is not OFPBRC_BAD_LEN')    
                               
class BadVendor2(basic.SimpleProtocol):
    """
    Unknown vendor id specified. 
    If a switch does not understand a vendor extension, it must send an OFPT_ERROR
    message with a OFPBRC_BAD_VENDOR error code and OFPET_BAD_REQUEST error
    type.
    """
    
    def runTest(self):        
        request = message.vendor()
        response, pkt = self.controller.transact(request, timeout=2)        
                
        
        rv = self.controller.message_send(request)
        self.assertTrue(rv==0,"Unable to send the message")
        
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ERROR,         
                                               timeout=5)
        self.assertTrue(response is not None, 
                                'Switch did not replay with error messge')
        self.assertTrue(response.type==ofp.OFPET_BAD_REQUEST, 
                               'Message field type is not OFPET_BAD_REQUEST') 
        self.assertTrue(response.code==ofp.OFPBAC_BAD_VENDOR, 
                               'Message field code is not OFPET_BAD_VENDOR')        
                               
class BadOutPort(basic.SimpleProtocol):   
    """
    Problem validating output action.
    Generate a flow_mod msg .Add an action OFPAT_OUTPUT such that out-put port is an invalid port . 
    Verify switch responds back with an error msg

    """
    def runTest(self):  
        
        pkt=simple_tcp_packet()
        act=action.action_output()        
        request = flow_msg_create(self, pkt, ing_port=1, egr_port=-1)
        
        rv = self.controller.message_send(request)
        self.assertTrue(rv==0,"Unable to send the message")
        
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ERROR,         
                                               timeout=5)
        self.assertTrue(response is not None, 
                                'Switch did not replay with error messge')                                       
        self.assertTrue(response.type==ofp.OFPET_BAD_ACTION, 
                               'Message field type is not OFPET_BAD_ACTION') 
        self.assertTrue(response.code==ofp.OFPET_OUT_PORT, 
                               'Message field code is not OFPET_OUT_PORT')
                               
class BadType2(basic.SimpleProtocol):   
    """
    Unknown action type. 
    Generate a flow_mod_msg .Add lot of actions such that switch 
    cannot handle them. Verify switch responds back with an error msg

    """
    def runTest(self):  
        
        pkt=simple_tcp_packet()
        act=action.action_output()       
        of_ports = errormsg_port_map.keys()
        self.assertTrue(len(of_ports)>1,"meeds 2 ports for testing")
        of_ports.sort() 
        request = flow_msg_create(self, pkt, ing_port=of_ports[0], egr_port=of_ports[1])
        request.actions.actions[0].type=67

        rv = self.controller.message_send(request)
        self.assertTrue(rv==0,"Unable to send the message")
        
        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ERROR,         
                                               timeout=5)
        self.assertTrue(response is not None, 
                                'Switch did not replay with error messge')                                       
        self.assertTrue(response.type==ofp.OFPET_BAD_ACTION, 
                               'Message field type is not OFPET_BAD_ACTION') 
        self.assertTrue(response.code==ofp.OFPBAC_BAD_TYPE, 
                               'Message field code is not OFPBAC_BAD_TYPE')

class BadLength2(basic.SimpleProtocol):
    """
    Length problem in actions.

    When the length field in the action header specified by the controller is
    wrong , the switch replies back with an OFPT_ERROR msg with Type Field
    OFPBAC_BAD_LEN

    """
    def runTest(self):

        pkt=simple_tcp_packet()
#        act=action.action_output()
        of_ports = errormsg_port_map.keys()
        self.assertTrue(len(of_ports)>1,"meeds 2 ports for testing")
        of_ports.sort()
        request = flow_msg_create(self, pkt, ing_port=of_ports[0], egr_port=of_ports[1])
#        request.actions.actions[0].type=67
        request.actions.actions[0].len=100

        print request.show()

        rv = self.controller.message_send(request)
        self.assertTrue(rv==0,"Unable to send the message")

        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ERROR,
                                               timeout=5)

        self.assertTrue(response is not None,
                                'Switch did not replay with error messge')      
        self.assertTrue(response.type==ofp.OFPET_BAD_ACTION,
                               'Message field type is not OFPET_BAD_ACTION')
        self.assertTrue(response.code==ofp.OFPBAC_BAD_LEN,
                               'Message field code is not OFPBAC_BAD_LEN')

class BufferUnknown(basic.SimpleProtocol):
    """
    Specified buffer does not exist. 

    When the buffer specified by the controller does not exit , the switch
    replies back with OFPT_ERROR msg with type fiels OFPET_BAD_REQUEST

    """
    def runTest(self):

        pkt=simple_tcp_packet()
#        act=action.action_output()
        of_ports = errormsg_port_map.keys()
        self.assertTrue(len(of_ports)>1,"meeds 2 ports for testing")
        of_ports.sort()
        request = flow_msg_create(self, pkt, ing_port=of_port[0], egr_port=of_ports[1])
        request.buffer_id=-1

        print request.show()

        rv = self.controller.message_send(request)
        self.assertTrue(rv==0,"Unable to send the message")

        (response, pkt) = self.controller.poll(exp_msg=ofp.OFPT_ERROR,
                                               timeout=5)
        print response.show()
        self.assertTrue(response is not None,
                                'Switch did not replay with error messge')
        self.assertTrue(response.type==ofp.OFPET_BAD_REQUEST,
                               'Message field type is not OFPET_BAD_REQUEST')
        self.assertTrue(response.code==ofp.OFPBRC_BUFFER_UNKNOWN,
                               'Message field code is not OFPBRC_BUFFER_UNKNOWN')


