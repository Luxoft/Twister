
import time
import json
import pprint

from oflib import *

switch_3 = "00:0a:08:17:f4:32:a5:00"
switch_4 = "00:0a:08:17:f4:5c:ac:00"
switch_5 = "00:00:00:00:00:00:00:05"

single_switch_flow = [(switch_3,1,2),(switch_3,2,1)]
initial_flow_path  = [(switch_3,1,2),(switch_3,2,1), (switch_4,1,2),(switch_4,2,1)]
changed_flow_path  = [(switch_3,1,3),(switch_3,3,1), (switch_5,1,2),(switch_5,2,1), (switch_4,1,3),(switch_4,3,1)]

#

def of_floodlight_1():
    log_debug("\n=== Starting openflow controller test 1 ===")
    res = restapi.get_switches_info()

    for sid in res:
        print '\n~~ Switch ID:', sid, '~~'
        for key,value in res[sid][0].items():
            print key.ljust(18), ':', value

    print
    return True

#

def of_floodlight_2():
    log_debug("\n=== Starting openflow controller test 2 ===")

    res = restapi.get_aggregate_stats('flow')
    log_debug('\n~~ Aggregates ~~')
    for sid in res:
        if not res[sid]:
            print '\n  None!'
            break
        print '\n~~ Switch ID:', sid, '~~'
        for key,value in res[sid][0].items():
            print ' ', key.ljust(18), ':', value

    res = restapi.get_aggregate_stats('table')
    log_debug('\n~~ Tables ~~')
    for sid in res:
        if not res[sid]:
            print '\n  None!'
            break
        print '\n~~ Switch ID:', sid, '~~'
        for key,value in res[sid][0].items():
            print ' ', key.ljust(18), ':', value

    print
    return True

#

# StatType: port, queue, flow, aggregate, desc, table, features, host
# Get port statistics
def of_floodlight_3():

    log_debug("\n=== Starting openflow controller test 3 ===")
    fl_switches = restapi.get_switches() # Getting registered swiches
    statsType="port"

    if statsType=="port":
        log_debug("Getting port statistics from floodlight controller...\n")

        for sw in fl_switches:
            switch_dpid = sw['dpid']
            log_debug("\nSwich DPID: %s" % switch_dpid)
            of_dict = restapi.get_switch_statistics(switch_dpid,statsType)
            print 'debug:', of_dict

            if of_dict:
                port_stats = of_dict[switch_dpid]
                for ps in  port_stats:
                    if ps['portNumber'] < 0:
                        continue

                    print "portNumber:      %s" % ps['portNumber']
                    print "transmitPackets: %s" % ps['transmitPackets']
                    print "transmitBytes:   %s" % ps['transmitBytes']
                    print "receivePackets:  %s" % ps['receivePackets']
                    print "receiveBytes:    %s" % ps['receiveBytes']
                    print "\n"
                    # print "portNumber:%s tx_pkt: %d tx_bytes: %d rx_pkt: %s rx_bytes: %i" % \
                    # (ps['portNumber'],ps['transmitPackets'], ps['transmitBytes'],ps['receivePackets'], ps['receiveBytes'])
            else:
                return False

    return True

#

# Get flows from floodlight controller
def of_floodlight_4():

    log_debug("\n=== Starting openflow controller test 4 ===")
    fl_switches = restapi.get_switches() # Getting registered swiches
    statsType = "flow"

    if statsType=="flow":
        log_debug("Getting flows from floodlight controller...\n")

        for sw in fl_switches:
            switch_dpid = sw['dpid']
            log_debug("\nSwich DPID: %s" % switch_dpid)
            fl_dict = restapi.get_switch_statistics(switch_dpid, statsType)
            print 'debug:', fl_dict

            if fl_dict:
                flows = fl_dict[switch_dpid]
                for fl in flows:
                    print "\nMatch:"
                    for key,value in fl['match'].items():
                        print "  %s : %s" % (key.ljust(24), value)

                    for act in fl['actions']:
                        print "\nAction:"
                        for key,value in act.items():
                            print "  %s : %s" % (key.ljust(24), value)
            else:
                return False

    return True

#

def of_floodlight_5():
    log_debug("\n=== Starting openflow controller test 5 ===")
    log_debug("Getting topology links from floodlight controler...\n")
    topo_links = restapi.get_topology_links()
    #print 'Topo links:', topo_links, '\n'

    for tl in topo_links:
        log_debug("src-swich: %s -> dst-switch: %s" %   (tl['src-switch'], tl['dst-switch']))
        log_debug("src-port: %s  -> dst-port:   %s\n" % (tl['src-port'],   tl['dst-port']))

#

# Adding flow path to controler, wait 10 secons
# then remove flow path, the flow path should be added on both swiches
# Assume that the topology is known
def of_floodlight_6():

    log_debug("\n=== Starting openflow controller test 6 ===")
    log_debug("Adding initial flows path")
    fl_switches = restapi.get_switches()

    for s in fl_switches:
       print "DPID: %s" % s['dpid']

    fl_list=[]
    fl_nr=0
    tm_wait=30

    for ifp in initial_flow_path:
        fl_nr+=1
        fl_name="flow-mod-%i" % fl_nr
        fl_dict={"switch":ifp[0], "name":fl_name, "cookie":"0", "priority":"32768",
            "ingress-port":str(ifp[1]), "active":"true", "actions":"output=%i" % ifp[2]}
        fl_list.append(fl_dict)

    log_debug("Done.\n")
    log_debug("Getting flows from controller...")
    of_floodlight_4()
    log_debug("Push new flow to controler...")

    for fl in fl_list:
        flowpusher.set(fl)
        time.sleep(1)
        log_debug("Flow added:\n %s" % str(fl))

    log_debug("Getting flows from controller...")
    of_floodlight_4()

    log_debug ("\nSleep %i seconds before removing the flows...\n" % tm_wait)
    time.sleep(tm_wait)
    log_debug ("Removing datapath flows...\n")

    for fl in fl_list:
        flowpusher.remove(None,fl)
        time.sleep(1)
        log_debug("Flow removed:\n %s" % str(fl))

    log_debug("Getting flows from controller...")
    of_floodlight_4()

#

def of_floodlight_7():
    log_debug("\n=== Starting openflow controller test 7 ===")
    log_debug("Change flows path")
    fl_switches = restapi.get_switches()

    for s in fl_switches:
       print "DPID: %s" % s['dpid']

    fl_list=[]
    fl_nr=0
    tm_wait=30

    for ifp in changed_flow_path:
        fl_nr+=1
        fl_name="flow-mod-%i" % fl_nr
        fl_dict={"switch":ifp[0], "name":fl_name, "cookie":"0", "priority":"32768",
            "ingress-port":str(ifp[1]), "active":"true", "actions":"output=%i" % ifp[2]}
        fl_list.append(fl_dict)

    log_debug("Done.\n")
    log_debug("Getting flows from controller...")
    of_floodlight_4()
    log_debug("Push new flow to controler...")

    for fl in fl_list:
        flowpusher.set(fl)
        log_debug("Flow added:\n %s" % str(fl))

    log_debug("Getting flows from controller...")
    of_floodlight_4()

    log_debug ("\nSleep %i seconds before removing the flows...\n" % tm_wait)
    time.sleep(tm_wait)
    log_debug ("Removing datapath flows...\n")

    for fl in fl_list:
        flowpusher.remove(None,fl)
        log_debug("Flow removed:\n %s" % str(fl))

    log_debug("Getting flows from controller...")
    of_floodlight_4()

#

# Add single flow to switch
def of_floodlight_8():
    log_debug("Starting openflow controller test 8")
    log_debug("Add flows to single switch")
    fl_switches = restapi.get_switches()

    for s in fl_switches:
       print "DPID: %s" % s['dpid']

    fl_list=[]
    fl_nr=0
    tm_wait=30

    for ifp in single_switch_flow:
        fl_nr+=1
        fl_name="flow-mod-%i" % fl_nr
        fl_dict={"switch":ifp[0], "name":fl_name, "cookie":"0", "priority":"32768",
            "ingress-port":str(ifp[1]), "active":"true", "actions":"output=%i" % ifp[2]}
        fl_list.append(fl_dict)

    log_debug("Done.\n")
    log_debug("Getting flows from controller...")
    of_floodlight_4()
    log_debug("Push new flow to controler...")

    for fl in fl_list:
        flowpusher.set(fl)
        log_debug("Flow added:\n %s" % str(fl))

    log_debug("Getting flows from controller...")
    of_floodlight_4()

    log_debug ("\nSleep %i seconds before removing the flows...\n" % tm_wait)
    time.sleep(tm_wait)
    log_debug("Removing datapath flows \n")

    for fl in fl_list:
        flowpusher.remove(None,fl)
        log_debug("Flow removed:\n %s" % str(fl))

    log_debug("Getting flows from controller...")
    of_floodlight_4()

#

restapi= RestApiTest('10.9.6.220', 8080)
flowpusher = StaticFlowPusher('10.9.6.220')

#

of_floodlight_1()
of_floodlight_2()
#of_floodlight_3()
#of_floodlight_4()
#of_floodlight_5()
#of_floodlight_6()
#of_floodlight_7()
#of_floodlight_8()
