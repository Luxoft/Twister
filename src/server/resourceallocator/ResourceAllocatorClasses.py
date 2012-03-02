
import os
import sys
import re
import pickle

TWISTER_PATH=os.getenv('TWISTER_PATH')
if(not TWISTER_PATH):
    print 'TWISTER_PATH environment variable  is not set'
    exit(1)        
sys.path.append(TWISTER_PATH)


from trd_party.BeautifulSoup import *
from common.tsclogging import *

RESOURCE_FREE     = 0
RESOURCE_BUSY     = 1
RESOURCE_RESERVED = 2

lvl_1_pool = 0
lvl_2_pool = 0
lvl_3_pool = 0

#
# resid format is : xx_xx_xxx , Device_Module_Port
#

def genidLevel(lvl):
    global lvl_1_pool,lvl_2_pool,lvl_3_pool
    if lvl==0:
        lvl_1_pool += 1
        resid_str="%02d_00_000" % (lvl_1_pool)
        print 'Creating Device with id: %s' % resid_str
    elif lvl==1:
        lvl_2_pool += 1
        resid_str="%02d_%02d_000" % (lvl_1_pool,lvl_2_pool)
        print 'Creating Module with id: %s' % resid_str
    else:
        lvl_3_pool += 1
        resid_str="%02d_%02d_%03d" % (lvl_1_pool,lvl_2_pool,lvl_3_pool)
        print 'Creating Port with id: %s' % resid_str
    return resid_str

#

class ResourceAllocator:

    def __init__(self, cfgfile):
        self.xmldoc = None
        self.hwdevices = []
        self.residStr = 'resid'
        self.parseConfigFile(cfgfile)

    def echo(self, msg):
        '''
        Simple echo function, for testing connection.
        '''
        print('Echo: %s' % str(msg))
        return 'RA reply: %s' % str(msg)

    def getPropDict(self, node, ignoretag):
        '''
        Helper function.
        '''
        prop_list = node.findAll(recursive=False)
        propdict = {}
        for prop in prop_list:
            key = prop.name
            value = prop.text
            if key==ignoretag:
                continue
            propdict[key] = value
        return propdict

    def parseConfigFile(self, cfgfile):
        '''
        Parse the XML data and create lists of dictionaries to represent the devices.
        '''
        if os.path.exists(cfgfile):
            with open(cfgfile, 'r') as f :
                self.xmldoc = BeautifulStoneSoup(f.read())
        else:
            logCritical('Devices config file not found:', cfgfile)
            exit(1)

        global lvl_1_pool,lvl_2_pool,lvl_3_pool

        for dv_prop in self.xmldoc.findAll('device'):
            # Create a dictionary from device first level xml tags, ignore devicemodule tag
            # Generate lvl 1 resource id identifier
            # Create device module list
            hw_device = self.getPropDict(dv_prop, ignoretag='devicemodule')
            hw_device[self.residStr] = genidLevel(0)
            hw_device['status'] = RESOURCE_FREE
            hw_device['devicemodule'] = []
            lvl_2_pool = 0

            # Find all devicemodule
            for mod_prop in dv_prop.findAll('devicemodule'):

                hw_device_module = self.getPropDict(mod_prop, ignoretag='deviceport')
                hw_device_module[self.residStr] = genidLevel(1)
                hw_device_module['status'] = RESOURCE_FREE
                hw_device_module['deviceport'] = []
                lvl_3_pool = 0

                for port_prop in mod_prop.findAll('deviceport'):
                    hw_device_port = self.getPropDict(port_prop, ignoretag='')
                    hw_device_port[self.residStr] = genidLevel(2)
                    hw_device_port['status'] = RESOURCE_FREE
                    hw_device_module['deviceport'].append(hw_device_port)
                hw_device['devicemodule'].append(hw_device_module)

            self.hwdevices.append(hw_device)

    def deviceQuery(self, query):
        '''
        Find one device and return the Res ID.
        '''
        kv_list = query.split(',')
        keyval_list = []

        print('------------')
        for kv in kv_list:
            if len(kv.split(':')) != len(kv.split('&&'))+1:
                print('Invalid query => {0}'.format(kv))
                return None
            else:
                print('Query => {0}'.format(kv))
                keyval_list.append(kv)
        print('------------')

        query_len = len(keyval_list)


        def checkQuery(item, query):
            # Pairs of `&&` queries
            kv_pairs = query.split('&&')
            result = True

            for kv in kv_pairs:
                # Key and Value checking,
                key = kv.split(':')[0]
                value = kv.split(':')[1]
                # The `||` queries must become regex
                if '||' in query:
                    value = '|'.join( ['^'+elem+'$' for elem in value.split('||')] )
                # Regex compare
                if '||' in query and (re.match(value, item.get(key)) or \
                    (value=='?' and item.get('status')==RESOURCE_FREE)):
                    result = True
                # Value compare
                elif not '||' in query and (item.get(key)==value or \
                    (value=='?' and item.get('status')==RESOURCE_FREE)):
                    result = True
                # If the compare is False, return False, because all compares must be True
                else:
                    return False

            return result


        for device in self.hwdevices:
            if query_len>0:
                # Devices
                #key   = keyval_list[0][0]
                #value = keyval_list[0][1]
                if checkQuery(device, keyval_list[0]):
                    if(query_len==1):
                        return device[self.residStr]
                    else:
                        # Device modules
                        for devicemodule in device['devicemodule']:
                            #key   = keyval_list[1][0]
                            #value = keyval_list[1][1]
                            if checkQuery(devicemodule, keyval_list[1]):
                                if(query_len==2):
                                    return devicemodule[self.residStr]
                                else:
                                    # Device ports
                                    #key   = keyval_list[2][0]
                                    #value = keyval_list[2][1]
                                    for deviceport in devicemodule['deviceport']:
                                        if checkQuery(deviceport, keyval_list[2]):
                                            return deviceport[self.residStr]

        # If nothing is found...
        return None

    def getResourceById(self, resid):
        '''
        Returns the dictionary with this particular Res ID.
        '''
        d = int(resid.split('_')[0]) # Device
        m = int(resid.split('_')[1]) # Module
        p = int(resid.split('_')[2]) # Port
        dev = self.hwdevices[d-1]
        mod = None
        port = None

        if not m:
            return dev
        else:
            mod = dev['devicemodule'][m-1]
        if not p:
            return mod
        else:
            port = mod['deviceport'][p-1]
        return port

    def getResourceStatus(self, resid):
        '''
        Returns the status Integer: 0, 1, or 2.
        '''
        try: res = self.getResourceById(resid)
        except: print 'Cannot find Resource with Id `%s` !' % resid ; return -1
        return res.get('status', -1)

    def allocResource(self, resid, epid):
        if self.getResourceStatus(resid):
            print 'Cannot allocate! The resource is already busy!'
            return -1
        try: res = self.getResourceById(resid)
        except: print 'Cannot find Resource with Id `%s` !' % resid ; return False
        res['status'] = RESOURCE_BUSY
        return self.getResourceStatus(resid)

    def reserveResource(self, resid, epid):
        if self.getResourceStatus(resid):
            print 'Cannot allocate! The resource is already busy!'
            return -1
        try: res = self.getResourceById(resid)
        except: print 'Cannot find Resource with Id `%s` !' % resid ; return False
        res['status'] = RESOURCE_RESERVED
        return self.getResourceStatus(resid)

    def freeResource(self, resid):
        try: res = self.getResourceById(resid)
        except: print 'Cannot find Resource with Id `%s` !' % resid ; return False
        res['status'] = RESOURCE_FREE
        return self.getResourceStatus(resid)

    def dumpConfig(self):
        '''
        Used for debug.
        '''
        for dv in self.hwdevices:
            print '********************'
            print dv

#

if __name__ == '__main__':
    #ra = ResourceAllocator('/home/dancioata/tscproject/twister/Config/hwdevices.xml')
    ra = ResourceAllocator(r'd:\Projects\twister\Config\hwdevices.xml')
    ra.dumpConfig()

    query_list=[
    'devicename:DUT5||DUT6,moduletype:?',
    'devicetype:Contivity&&devicefamily:27XX&&devicemodel:2750SY',
    'devicevendor:Avaya&&devicetype:PBX,moduletype:?',
    'devicevendor:Avaya,moduletype:DS32',
    'devicename:?,moduletype:ATM',
    'devicefamily:?,moduletype:DS32',
    'devicefamily:ip500,moduletype:ETR||ATM||DS32,port:3',
    'devicetype:?,moduletype:?,port:103',
    'devicename:foo_PBX,moduletype:ETR,port:?',
    'devicetype:PBX,moduletype:ETR,port:201',
    'devicename:foo_PBX,moduletype:?,port:201',
    'devicetype:?,moduletype:?,port:207',
    'devicetype:?,moduletype:?,porttype:Phone',
    'devicetype:?,moduletype:?,hasspeaker:True',
    ]

    test = True
    for query in query_list:
        print '####################'
        res = ra.deviceQuery(query)
        zero = ra.freeResource(res)
        print 'ID:', res
        print 'Alocating:', ra.allocResource(res, '')
        print 'Releasing:', ra.freeResource(res)
        if not res or zero != 0: test = False

    if test: print '\nAll tests successful!'
    else: print '\nTests failed!'
