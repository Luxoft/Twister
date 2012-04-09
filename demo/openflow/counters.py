
import os
import time
import copy
import pprint

from LibOpenFlow import *

switch_3 = "00:0a:08:17:f4:32:a5:00"
switch_4 = "00:0a:08:17:f4:5c:ac:00"
switch_5 = "00:00:00:00:00:00:00:05"

counter_list=["transmitPackets","transmitBytes","receivePackets","receiveBytes"]
current_stats = {}


def statsPerSecond(old_stats, new_stats):

    for new_s in new_stats:

        for old_s in old_stats:

            if new_s['portNumber'] < 0:
                continue
            if new_s['portNumber'] not in [8, 18, 28]:
                continue

            elif new_s['portNumber'] == old_s['portNumber']:
                print "Port Nr %s" % new_s['portNumber']

                for key, val in new_s.items():
                    if key in counter_list:
                        diff = new_s[key] - old_s[key]
                        print "%s : %s /s" % (key.ljust(16), str(diff).ljust(9))
                        old_s[key] = val

                print "\n"


def of_floodlight_3():

    global current_stats

    # Dictionary to keep all switch counters
    # Getting registered swiches
    fl_switches = restapi.get_switches()

    for sw in fl_switches:

        switch_dpid = sw['dpid']
        print '\n=== Swich DPID: %s ===\n' % switch_dpid
        of_dict = restapi.get_switch_statistics(switch_dpid, 'port')

        if of_dict:
            new_stats = of_dict[switch_dpid]

            if not current_stats.get(switch_dpid):
                current_stats[switch_dpid] = copy.deepcopy(new_stats)
                fo = open(switch_dpid.replace(':','_') + '_ports.json', 'w')
                json.dump( current_stats.get(switch_dpid), fo, indent=2 )
            else:
                statsPerSecond(current_stats[switch_dpid],new_stats)

    return True

#

restapi= RestApiTest('10.9.6.220',8080)

#

while True:
    os.system('cls')
    of_floodlight_3()
    time.sleep(1)
