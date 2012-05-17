
# File: ResourceAllocatorClasses.py ; This file is part of Twister.

# Copyright (C) 2012 , Luxoft

# Authors:
#    Andrei Costachi <acostachi@luxoft.com>
#    Andrei Toma <atoma@luxoft.com>
#    Cristian Constantin <crconstantin@luxoft.com>
#    Daniel Cioata <dcioata@luxoft.com>

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import re
import pickle

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print('TWISTER_PATH environment variable is not set! Exiting!')
    exit(1)
sys.path.append(TWISTER_PATH)

from trd_party.BeautifulSoup import BeautifulStoneSoup
from common.tsclogging import *

RESOURCE_FREE     = 0
RESOURCE_BUSY     = 1
RESOURCE_RESERVED = 2

lvl_1_pool = 0
lvl_2_pool = 0
lvl_3_pool = 0
lvl_4_pool = 0

#
# resid format is : xx_xx_xx_xxx = TestBed_Device_Module_Port
#

def genidLevel(lvl):
    global lvl_1_pool, lvl_2_pool, lvl_3_pool, lvl_4_pool

    if not lvl:
        lvl_1_pool += 1
        resid_str="%02d_00_00_000" % (lvl_1_pool)
        logDebug('\nCreating TestBed with id: %s' % resid_str)
    elif lvl==1:
        lvl_2_pool += 1
        resid_str="%02d_%02d_00_000" % (lvl_1_pool,lvl_2_pool)
        logDebug('Creating Device with id: %s' % resid_str)
    elif lvl==2:
        lvl_3_pool += 1
        resid_str="%02d_%02d_%02d_000" % (lvl_1_pool,lvl_2_pool,lvl_3_pool)
        logDebug('Creating Module with id: %s' % resid_str)
    else:
        lvl_4_pool += 1
        resid_str="%02d_%02d_%02d_%03d" % (lvl_1_pool,lvl_2_pool,lvl_3_pool,lvl_4_pool)
        logDebug('Creating Port with id: %s' % resid_str)

    return resid_str

#

class ResourceAllocator:

    def __init__(self, cfgfile):
        self.xmldoc = None
        self.testbeds = []
        self.residStr = 'resid'
        self.parseConfigFile(cfgfile)


    def echo(self, msg):
        '''
        Simple echo function, for testing connection.
        '''
        logDebug('Echo: %s' % str(msg))
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
                txt = re.sub('<(?P<m>[\S]+)/>\n', '<\g<m>></\g<m>>', f.read())
                self.xmldoc = BeautifulStoneSoup(txt)
                del txt
        else:
            logCritical('Devices config file not found:', cfgfile)
            exit(1)

        global lvl_1_pool, lvl_2_pool, lvl_3_pool, lvl_4_pool

        for tb_prop in self.xmldoc.findAll('testbed'):
            test_bed = self.getPropDict(tb_prop, ignoretag='device')
            test_bed[self.residStr] = genidLevel(0)
            test_bed['status'] = RESOURCE_FREE
            test_bed['device'] = []
            lvl_2_pool = 0

            for dv_prop in self.xmldoc.findAll('device'):
                # Create a dictionary from device first level xml tags, ignore devicemodule tag
                # Generate lvl 1 resource id identifier
                # Create device module list
                hw_device = self.getPropDict(dv_prop, ignoretag='devicemodule')
                hw_device[self.residStr] = genidLevel(1)
                hw_device['status'] = RESOURCE_FREE
                hw_device['devicemodule'] = []
                lvl_3_pool = 0

                # Find all devicemodule
                for mod_prop in dv_prop.findAll('devicemodule'):

                    hw_device_module = self.getPropDict(mod_prop, ignoretag='deviceport')
                    hw_device_module[self.residStr] = genidLevel(2)
                    hw_device_module['status'] = RESOURCE_FREE
                    hw_device_module['deviceport'] = []
                    lvl_4_pool = 0

                    for port_prop in mod_prop.findAll('deviceport'):
                        hw_device_port = self.getPropDict(port_prop, ignoretag='')
                        hw_device_port[self.residStr] = genidLevel(3)
                        hw_device_port['status'] = RESOURCE_FREE

                        hw_device_module['deviceport'].append(hw_device_port)
                    hw_device['devicemodule'].append(hw_device_module)
                test_bed['device'].append(hw_device)

            self.testbeds.append(test_bed)


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

        if not query_len:
            logError('Null query!')

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


        for testbed in self.testbeds:

            # Testbeds
            if checkQuery(testbed, keyval_list[0]):
                if query_len==1:
                    return testbed[self.residStr]
                else:

                    # Devices
                    for device in testbed['device']:
                        if checkQuery(device, keyval_list[1]):
                            if query_len==2:
                                return device[self.residStr]
                            else:

                                # Device modules
                                for devicemodule in device['devicemodule']:
                                    if checkQuery(devicemodule, keyval_list[2]):
                                        if query_len==3:
                                            return devicemodule[self.residStr]
                                        else:

                                            # Device ports
                                            for deviceport in devicemodule['deviceport']:
                                                if checkQuery(deviceport, keyval_list[3]):
                                                    return deviceport[self.residStr]

        # If nothing is found...
        return None


    def getResourceById(self, resid):
        '''
        Returns the dictionary with this particular Res ID.
        '''
        t = int(resid.split('_')[0]) # Test bed
        d = int(resid.split('_')[1]) # Device
        m = int(resid.split('_')[2]) # Module
        p = int(resid.split('_')[3]) # Port

        tb = self.testbeds[t-1]
        dev = None
        mod = None
        port = None

        if not d:
            return tb
        else:
            dev = tb['device'][d-1]
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
        except: print 'Cannot free! Cannot find Resource with Id `%s` !' % resid ; return False
        res['status'] = RESOURCE_FREE
        return self.getResourceStatus(resid)


    def dumpConfig(self):
        '''
        Used for debug.
        '''
        for dv in self.testbeds:
            print '\n********** Test Bed **********'
            print dv

#

if __name__ == '__main__':

    #ra = ResourceAllocator(r'd:\Projects\twister_rel1\src\config\hwconfig_x.xml')
    ra = ResourceAllocator('/home/cro/twister_rel1/src/config/hwconfig_x.xml')
    ra.dumpConfig()
    test = True

    query_list = [
    'testbedname:TB-001,devicename:DUT3||DUT2||DUT1',
    'testbedname:?,devicename:DUT5||DUT6,moduletype:?',
    'testbedname:?,devicetype:Contivity&&devicefamily:27XX&&devicemodel:2750SY',
    'testbedname:?,devicevendor:Avaya&&devicetype:PBX,moduletype:?',
    'testbedname:?,devicevendor:Avaya,moduletype:DS32',

    'testbedid:?,devicename:?,moduletype:ATM',
    'testbedid:?,devicefamily:?,moduletype:DS32',
    'testbedid:?,devicefamily:ip500,moduletype:ETR||ATM||DS32,port:3',
    'testbedid:?,devicetype:?,moduletype:?,port:103',
    'testbedid:?,devicename:foo_PBX,moduletype:ETR,port:?',
    'testbedid:?,devicetype:PBX,moduletype:ETR,port:201',
    'testbedid:?,devicename:foo_PBX,moduletype:?,port:201',
    'testbedid:?,devicetype:?,moduletype:?,port:207',
    'testbedid:?,devicetype:?,moduletype:?,porttype:Phone',
    'testbedid:?,devicetype:?,moduletype:?,hasspeaker:True',
    ]

    query_list_x = [
    'testbedname:TB-001,devicename:Dev 003||Dev 002||Dev 001',
    'testbedid:002,devicename:?,moduletype:m',
    'testbedname:?,devicetype:C&&devicefamily:C&&devicemodel:C',
    'testbedname:?,devicetype:C&&devicefamily:C,moduletype:?',
    'testbedname:?,devicemodel:C,moduletype:m',
    ]

    for query in query_list_x:

        print('\n####################')
        res = ra.deviceQuery(query)
        print 'ID:', res
        zero = ra.freeResource(res)
        print 'Alocating:', ra.allocResource(res, '')
        print 'Releasing:', ra.freeResource(res)
        if not res or zero != 0: test = False

    if test: print '\nAll tests successful!'
    else: print '\nTests failed!'
