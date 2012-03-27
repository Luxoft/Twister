from oflib import *
import time

def of_floodlight_3():
    log_debug("Starting openflow controller test 3")
    statsType="port"
    #Getting registered swiches
    fl_switches=restapi.get_switches()    
    if(statsType=="port"):
        log_debug("Getting port statistics from floodlight controller\n")
        for sw in fl_switches:
            switch_dpid=sw['dpid']
            print "Swich DPID: %s" % switch_dpid        
            of_dict=restapi.get_switch_statistics(switch_dpid,statsType)
            if(of_dict!=None):
                port_stats=of_dict[switch_dpid]
                for ps in  port_stats:
                    if(ps['portNumber'] <0):
                        continue
                    if(True):
                        print "portNumber:      %s" % ps['portNumber']
                        print "transmitPackets: %s" % ps['transmitPackets']
                        print "transmitBytes:   %s" % ps['transmitBytes']
                        print "receivePackets:  %s" % ps['receivePackets']
                        print "receiveBytes:    %s" % ps['receiveBytes']
                    else:
                       print "portNumber:%s tx_pkt: %d tx_bytes: %d rx_pkt: %s rx_bytes: %i" % \
                       (ps['portNumber'],ps['transmitPackets'], ps['transmitBytes'],ps['receivePackets'], ps['receiveBytes'])
            else:
                return False  
    return True;

restapi= RestApiTest('11.126.32.12',8080)
while True:
    of_floodlight_3()
    time.sleep(2)
    
        
