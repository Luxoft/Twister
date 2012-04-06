from oflib import *
import time
import pprint
import copy
switch_3="00:00:00:00:00:00:00:03"
switch_4="00:00:00:00:00:00:00:04"
switch_5="00:00:00:00:00:00:00:05"

counter_list=["transmitPackets","transmitBytes","receivePackets","receiveBytes"]
current_stats={}

def statsPerSecond(old_stats,new_stats):
    
    for new_s in new_stats:    
        for old_s in old_stats:
            if(new_s['portNumber']<0):
                continue
            elif(new_s['portNumber']==old_s['portNumber']):
                print "portNumber: %s" % new_s['portNumber']                        
                for key,val in new_s.items():              
                    if(key in counter_list):                
                        diff=new_s[key]-old_s[key]    
                        print "%s : %i  /s" % (key,  diff)                        
                        old_s[key]=val
                                        
                print "\n"          
def of_floodlight_3():
    global current_stats
    log_debug("Starting openflow controller test 3")
    statsType="port"
    #dictionary to keep all switch counters

    
    #Getting registered swiches
    fl_switches=restapi.get_switches()    
        
    if(statsType=="port"):
        log_debug("Getting port statistics from floodlight controller\n")
        for sw in fl_switches:
            switch_dpid=sw['dpid']
            print "Swich DPID: %s" % switch_dpid        
            of_dict=restapi.get_switch_statistics(switch_dpid,statsType)            
            #print of_dict
            if(of_dict!=None):
                new_stats=of_dict[switch_dpid]
                #print current_stats.get(switch_dpid)
                if(current_stats.get(switch_dpid)==None):
                    current_stats[switch_dpid]=copy.deepcopy(new_stats)
                    #print current_stats
                    print current_stats.get(switch_dpid)
                    #print new_stats                    
                else:    
                    print "enter here"
                    statsPerSecond(current_stats[switch_dpid],new_stats)
                """                    
                for ps in  port_stats:
                    if(ps['portNumber'] <0):
                        continue
                    if(False):
                        print "portNumber:      %s" % ps['portNumber']
                        print "transmitPackets: %s" % ps['transmitPackets']
                        print "transmitBytes:   %s" % ps['transmitBytes']
                        print "receivePackets:  %s" % ps['receivePackets']
                        print "receiveBytes:    %s" % ps['receiveBytes']                        
                    else:
                        statsPerSecond(switch_dpid,ps)

            else:
                return False  
            """                
    return True;

restapi= RestApiTest('10.9.6.220',8080)
while True:
    of_floodlight_3()
    time.sleep(1)
    
        
