#!/usr/bin/env python

"""
Tool for running ofdatapath1.3 openflow 1.3 soft switch

"""

import argparse
import sys
import os
import time
import signal
from subprocess import Popen,PIPE,call,check_call
from of_config import *

ofdatapath_pid="/usr/local/var/run/ofdatapath.pid"
ofprotocol_pid="/usr/local/var/run/ofprotocol.pid"

class OFwitch:
    def __init__(self,config):
        self.config=config

    def setLinks(self):
        idx=0
        intf_names=self.config['port_map'].values()
        for intf in intf_names:
            cmd = ["/sbin/ifconfig",intf,"192.168.1" + str(idx) + ".1",
               "netmask", "255.255.255.0"]
            runCommand(cmd)

            idx=idx+1
        intf_names=self.config['peer_map'].values()
        for intf in intf_names:
            cmd = ["/sbin/ifconfig",intf,"192.168.1" + str(idx) + ".1",
               "netmask", "255.255.255.0"]
            runCommand(cmd)
            idx=idx+1

    def createLinks(self):
        #create a list of ports
        port_map=sorted(self.config['port_map'].keys())
        #peer_map=sorted(self.config['peer_map'].keys())
        for port in port_map:
            cmd ='ip link add name '+self.config['port_map'][port]
            cmd+=' type veth peer name '+ self.config['peer_map'][port]
            runCommand(cmd)
        self.setLinks()

    def deleteLinks(self):
        #create a list of ports
        port_map=sorted(self.config['port_map'].keys())
        for port in port_map:
            cmd ='ip link del '+self.config['port_map'][port]
            runCommand(cmd)

    def stop(self):
        self.deleteLinks()
        print "Stoped"

    def start(self):
        self.createLinks()
        print "Links created"
        time.sleep(2)

def runCommand(cmd):
    print "Cmd: " + str(cmd)
    if(type(cmd)==type(" ")):
        cmd_args=cmd.split(' ')
        call(cmd_args)
    else:
        call(cmd)

def start_switch():
    for item in twister_openflow_config:
        if(item['cfgtype']=='virtual'):
            sw=OFwitch(item['config'])
            sw.start()
    print "Starting ofdatapath"
    cfg=getOpenflowConfig("")
    intf_names=cfg['peer_map'].values()
    ints = ','.join(intf_names)
    runCommand("ofdatapath -i " + ints + " punix:/tmp/oft -d 000000000001 -P " + ofdatapath_pid + " -D -v")
    time.sleep(2)
    print "Starting secure channel"
    runCommand("ofprotocol unix:/tmp/oft tcp:127.0.0.1:6633 --fail=closed --listen=ptcp:6634")

def stop_switch():
    runCommand("killall -9 ofdatapath")
    runCommand("killall -9 ofprotocol")
    for item in twister_openflow_config:
        if(item['cfgtype']=='virtual'):
            sw=OFwitch(item['config'])
            sw.stop()

def main():
    signal.signal(signal.SIGINT, signal_handler)
    print 'Press Ctrl+C'

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--start-sw',action='store_true',
        help='start the openflow 1.3 softswitch and add virtual links')
    parser.add_argument('--stop-sw',action='store_true',
        help='stop the openflow 1.3 softswitch and delete virtual links')
    if os.getuid() != 0:
        print "*** Must run as root."
        exit( 1 )

    args = parser.parse_args()

    if(args.start_sw):
        start_switch()
    elif(args.stop_sw):
        stop_switch()
    else:
        print "you must use ONLY one of the following options:"
        parser.print_help();

def signal_handler(signal, frame):
    print 'You pressed Ctrl+C - or killed me with -2'
    stop_switch()

if __name__ == "__main__":
    main()
