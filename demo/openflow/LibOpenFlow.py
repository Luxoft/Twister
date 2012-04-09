
import time
import json
import httplib

#

switch_1 = "00:0a:08:17:f4:32:a5:00"
switch_2 = "00:0a:08:17:f4:5c:ac:00"
switch_3 = "00:00:00:00:00:00:00:05"

single_switch_flow = [(switch_2,1,2),(switch_2,2,1)]
initial_flow_path  = [(switch_1,1,2),(switch_1,2,1), (switch_2,1,2),(switch_2,2,1)]
changed_flow_path  = [(switch_1,1,3),(switch_1,3,1), (switch_3,1,2),(switch_3,2,1), (switch_2,1,3),(switch_2,3,1)]

#

def log_debug(msg):
    print(msg)
    time.sleep(0.5)

#

class FloodLiteControl():

    '''
    This is a helper for connecting the the FloodLite controller.
    '''

    def __init__(self, server, port):
        self.server = server
        self.port = port


    def get_switches(self):
        '''
        List of all switch DPIDs connected to the controller
        '''
        fl_uri = "http://"+self.server+":"+str(self.port)+"/wm/core/controller/switches/json"
        ret = self.rest_call(fl_uri)
        return ret


    def get_switches_info(self):
        '''
        List of all switches connected to the controller, with details
        '''
        fl_uri = "http://"+self.server+":"+str(self.port)+"/wm/core/switch/all/desc/json"
        ret = self.rest_call(fl_uri)
        return ret


    def get_aggregate_stats(self, statType):
        '''
        Compose aggregate stats
        statType : port, queue, flow, aggregate, desc, table, features, host
        '''
        fl_uri = "http://"+self.server+":"+str(self.port)+"/wm/core/switch/all/"+statType+"/json"
        ret = self.rest_call(fl_uri)
        return ret


    def get_switch_statistics(self, switchId, statType):
        '''
        Retrieve per switch stats
        switchId: Valid Switch DPID (XX:XX:XX:XX:XX:XX:XX:XX)
        statType : port, queue, flow, aggregate, desc, table, features, host
        '''
        fl_uri = "http://"+self.server+":"+str(self.port)+"/wm/core/switch/"+switchId+"/"+statType+"/json"
        ret = self.rest_call(fl_uri)
        return ret


    def get_global_traffic_counters(self, counterTitle):
        '''
        List of globat traffic counters in the controler
        All or, counter in form DPID_Port#OFEventL3/4_Type
        '''
        fl_uri = "http://"+self.server+":"+str(self.port)+"/wm/core/counter/"+counterTitle+"/json"
        ret = self.rest_call(fl_uri)
        return ret


    def get_switch_traffic_counters(self, switchId, counterName):
        '''
        List of traffic counters per switch
        '''
        fl_uri = "http://"+self.server+":"+str(self.port)+"/wm/core/counter/"+switchId+"/"+counterName+"/json"
        ret = self.rest_call(fl_uri)
        return ret


    def get_topology_links(self):
        '''
        List all the inter-switch links connected to the same controller
        '''
        fl_uri = "http://"+self.server+":"+str(self.port)+"/wm/topology/links/json"
        ret = self.rest_call(fl_uri)
        return ret


    def rest_call(self, path):
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        conn = httplib.HTTPConnection(self.server, self.port)
        conn.request('GET', path, "", headers)
        response = conn.getresponse()
        res = (response.status, response.reason, response.read())
        conn.close()

        if res[0] == 200:
            response_dict = json.loads(res[2])
            return response_dict
        else:
            print "Rest API invalid call, status: %d, reason: %s" % (res[0], res[1])
            return None

#

class StaticFlowPusher(object):

    def __init__(self, server):
        self.server = server

    def get(self, data):
        ret = self.rest_call({}, 'GET')
        return json.loads(ret[2])

    def set(self, data):
        ret = self.rest_call(data, 'POST')
        return ret[0] == 200

    def remove(self, objtype, data):
        ret = self.rest_call(data, 'DELETE')
        return ret[0] == 200

    def rest_call(self, data, action):
        path = '/wm/staticflowentrypusher/json'
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        body = json.dumps(data)
        conn = httplib.HTTPConnection(self.server, 8080)
        conn.request(action, path, body, headers)
        response = conn.getresponse()
        ret = (response.status, response.reason, response.read())
        conn.close()
        return ret

#

def show_switches():

    restapi= FloodLiteControl('10.9.6.220', 8080)
    fl_switches = restapi.get_switches()
    log_debug('\n~~ Getting flows from floodlight controller ~~\n')

    for sw in fl_switches:
        switch_dpid = sw['dpid']
        log_debug('Swich DPID: %s' % switch_dpid)
        fl_dict = restapi.get_switch_statistics(switch_dpid, 'flow')

        if not fl_dict[switch_dpid]:
            print '\nMatch:  None!\n'
            return False

        if fl_dict:
            for fl in fl_dict[switch_dpid]:
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
