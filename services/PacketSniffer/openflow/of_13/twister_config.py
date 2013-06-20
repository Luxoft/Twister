import ConfigParser
import xmlrpclib
import pprint

class ResourceManager():
    def __init__(self):
        self.defaultConfig={
            'ra_proxy':'http://127.0.0.1:8000/ra/',
            'testbed':'openflow_13_testbed',
            'controller':{
                # openflow switch connect to host:port
                'host':'127.0.0.1',
                'port':6633,
                #controller agent connect to agent_host,agent_port
                'agent_host':'127.0.0.1',
                'agent_port':7755,
            },
            'switch':{
                'port_map':{1:'veth1',2:'veth3',3:'veth5',4:'veth7'},
                'datapath_id':'100000000001'
            }
        }
    
    def getResources_ra(self,ra_proxy,testbed,device):                
        res="/"+testbed+"/"+device+"/"        
        print "testbed: %s\ndevice: %s" % (testbed,device)
        query=None
        try:            
            q=ra_proxy.getResource(res)
            #pprint.pprint(q['meta'],indent=4)        
            if(q==False):
                 print "Twister ResourceAllocator: *** items for :%s,%s not available ***" %(testbed,device)
                 return False
            query=q['meta']      
            print "*** Resource manager config: RESOURCE_ALLOCATOR SUCCESS***"        
        except:
            raise
            print "*** Resource manager config: RESOURCE_ALLOCATOR FAILURE ***"
            return None            
          
        #controller configuration
        if(device.startswith('controller')):
            retDict={
                     'host':query['host'],
                     'port':int(query['port']),
                     'agent_host':query['agent_host'],
                     'agent_port':int(query['agent_port'])
                    }            
            return retDict
        #switch configuration
        if(device.startswith('switch')):            
            port_map_s=query['port_map']
            port_map=self.string_to_portmap(port_map_s)
            dpid=query['datapath_id']
            resDict={
                     'port_map':port_map,
                     'datapath_id':query['datapath_id']
                    }
            return resDict
        
    def getResources_file(self,config_file):
        config = ConfigParser.SafeConfigParser()
        config.read(config_file)   
        cfg={}
        for item in config.options('CONTROLLER_CONFIG'):
            cfg[item]=config.get('CONTROLLER_CONFIG',item)
        return cfg
                            
    def getResources_default(self):
        print "*** Resource manager config : DEFAULT ***"
        return self.defaultConfig
    
    #local function 
    def string_to_portmap(self,port_map_str):
        pml=port_map_str.split(",")
        port_map={}
        for pm1 in pml:
            l=pm1.split(":")
            port_map[int(l[0])]=l[1].strip()        
        return port_map
                        
def main():
    cfg=ResourceManager()
    ra_proxy=xmlrpclib.ServerProxy(cfg.defaultConfig['ra_proxy'])
    c=cfg.getResources_ra(ra_proxy,'openflow_13_testbed','controller')
    print c
    s=cfg.getResources_ra(ra_proxy,'openflow_13_testbed','switch')
    print s
    print "Test default resources"
    d=cfg.getResources_default()
    print d
    
if __name__ == '__main__':
        main()                
