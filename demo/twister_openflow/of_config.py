
twister_openflow_config = [
    {
        'cfgtype':'virtual',
        'epname':'EP-1001',
        'config':{
            'bridge':'br1',
            'controller_host':'127.0.0.1',
            'controller_port': 8855,
            #peer_map -> are used for ovswitch ports
            'peer_map':{1: 'veth0', 2: 'veth2', 3: 'veth4', 4: 'veth6'},
            #port_map -> openflow datapath links to ovswitch ports
            'port_map':{1: 'veth1', 2: 'veth3', 3: 'veth5', 4: 'veth7'}
        }
    },
    {
        'cfgtype':'virtual',
        'epname':'EP-1002',
        'config':
        {
            'bridge':'br2',
            'controller_host':'127.0.0.1',
            'controller_port': 7744,
            #peer_map -> are used for ovswitch ports
            'peer_map':{1: 'veth8', 2: 'veth10', 3: 'veth12', 4: 'veth14'},
            #port_map -> openflow datapath links to ovswitch ports
            'port_map':{1: 'veth9', 2: 'veth11', 3: 'veth13', 4: 'veth15'},
        }
     },
     {
        'cfgtype':'phy',
        'epname':'EP-1003',
        'config':
        {
            'bridge':'',
            'controller_host':'127.0.0.1',
            'controller_port': 6633,
            #peer_map -> NOT USED FOR PHY INTERFACES
            #'peer_map':{1: 'veth8', 2: 'veth10', 3: 'veth12', 4: 'veth14'},
            #port_map -> CHANGE PORT 1-4 to switch port
            'port_map':{1: 'eth1', 2: 'eth2', 3: 'eth3', 4: 'eth4'},
        }
     }
]

# Default openflow config used by oftest is first entry in list
openflow_config = twister_openflow_config[0]['config']

# Call this in the twister openflow test to set a new config
def getOpenflowConfig(epid):
    for cfg in twister_openflow_config:
        if cfg['epname'] == epid:
            print "Found config for %s" % epid
            return cfg['config']
    print "Config not found, return default config"
    return twister_openflow_config[0]['config']
