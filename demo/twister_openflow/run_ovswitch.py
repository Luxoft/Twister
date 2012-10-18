#!/usr/bin/env python
#
# Create veth pairs and start up switch daemons
#
import argparse
import os
import time
from subprocess import Popen,PIPE,call,check_call
from of_config import *

openvswitch_mod="path/to/openvswitch/datapath/linux/openvswitch_mod.ko"
ovsdb_pid="/usr/local/var/run/openvswitch/ovsdb-server.pid"
ovsdb_sock="punix:/usr/local/var/run/openvswitch/db.sock"
vswitchd_pid="/usr/local/var/run/openvswitch/ovs-vswitchd.pid"
#sudo ip link add name veth10 type veth peer name veth16

class OVSwitch:
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

    def configureBridge(self,mode):
        if(mode=='delete'):
            print "Delete  bridge if exists:  "+self.config['bridge']
            cmd="ovs-vsctl --no-wait del-br "+self.config['bridge']
            runCommand(cmd)
        elif(mode=='add'):
            print "Adding bridge "+self.config['bridge']
            cmd="ovs-vsctl --no-wait add-br "+self.config['bridge']
            runCommand(cmd)

    def configurePorts(self):
        print "Adding virtual links to OVSwitch"
        port_map=sorted(self.config['port_map'].keys())
        for port in port_map:
            cmd = "ovs-vsctl --no-wait add-port "+self.config['bridge']+" "+ self.config['peer_map'][port]
            runCommand(cmd)

    def addController(self):
        print "Adding controller"
        chost=self.config['controller_host']
        cport=self.config['controller_port']
        cmd="ovs-vsctl --no-wait set-controller %s tcp:%s:%d" % (self.config['bridge'], chost, cport)
        runCommand(cmd)
        cmd="ovs-vsctl --no-wait set-fail-mode "+self.config['bridge']+" secure"
        runCommand(cmd)

    def stop(self):
        self.configureBridge('delete')
        self.deleteLinks()
        print "Show switch configuration"
        time.sleep(2)
        runCommand("ovs-vsctl show")

    def start(self):
        self.createLinks()
        self.configureBridge('add')
        self.configurePorts()
        self.addController()
        print "Show switch configuration"
        time.sleep(2)
        runCommand("ovs-vsctl show")


def start_ovswitch():
    print "Inserting openvswitch kernel module %s" % openvswitch_mod
    runCommand("/sbin/insmod "+openvswitch_mod)
    #start ovs database server
    print "Starting ovs database server"
    if os.path.isfile(ovsdb_pid) :
        print "ovsdb-server is already started"
    else:
        runCommand("ovsdb-server --remote="+ovsdb_sock+" --remote=db:Open_vSwitch,manager_options --pidfile --detach")
    #start ovs daemon
    if os.path.isfile(vswitchd_pid) :
        print "ovs-vswitchd is already started"
    else:
        runCommand("ovs-vswitchd --pidfile --detach")

def stop_ovswitch():
    if os.path.isfile(vswitchd_pid):
        print "Stopping ovs-vswitchd"
        with open(vswitchd_pid) as db_pid:
            pid=db_pid.read().strip()
            runCommand("kill "+ pid)
        #remove pid file to avoid hidden problems
        try:
            os.remove(vswitchd_pid)
        except:
            pass
    else:
        print "ovs-vswitchd is not started"

    if os.path.isfile(ovsdb_pid):
        print "Stopping ovsdb-server"
        with open(ovsdb_pid) as d_pid:
            pid=d_pid.read().strip()
            runCommand(["kill", pid])
        try:
            os.remove(ovsdb_pid)
        except:
            pass
    else:
       print "ovsdb-server is not started"

def runCommand(cmd):
    print "Cmd: " + str(cmd)
    if(type(cmd)==type(" ")):
        cmd_args=cmd.split(' ')
        call(cmd_args)
    else:
        call(cmd)

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--start-ovs',action='store_true',
        help='try to load kernel module, start openvswitch database and demon')
    parser.add_argument('--stop-ovs',action='store_true',
        help='stop openvswitch database and demon')

    parser.add_argument('--start-dp',action='store_true',
        help='create ovswitch datapath')
    parser.add_argument('--stop-dp',action='store_true',
        help='delete ovswitch datapath')


    if os.getuid() != 0:
        print "*** Must run as root."
        exit( 1 )

    args = parser.parse_args()

    if(args.start_ovs):
        start_ovswitch()
    elif(args.stop_ovs):
        stop_ovswitch()
    elif(args.start_dp):
        for item in twister_openflow_config:
            if(item['cfgtype']=='virtual'):
                sw=OVSwitch(item['config'])
                sw.start()
            else:
                print "Skip physical interface configuration."

    elif (args.stop_dp):
        for item in twister_openflow_config:
            if(item['cfgtype']=='virtual'):
                sw=OVSwitch(item['config'])
                sw.stop()
            else:
                print "Skip physical interface configuration."
    else:
        print "you must use ONLY one of the following options:"
        parser.print_help();

if __name__ == "__main__":
    main()
