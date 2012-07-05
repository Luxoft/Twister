
from Tkinter import *

import os,sys
__file__ = os.path.abspath(__file__)
DIR = os.path.split(__file__)[0]
UPPER_DIR = os.sep.join(DIR.split(os.sep)[:-2])+"/Sources/Python/XMLUtils"
sys.path.append(UPPER_DIR)

from BeautifulSoup import *

#dictionary structure
#[devicename:"DUT1",devicedesc="device description",properties:[{"propname":"propvalue"},]]

class TSConfigParser:
    def __init__(self):
        self.xmldoc=None
        self.devices=[]

    def parseConfigFile(self,cfgfile):
        f=open(cfgfile)
        self.xmldoc=BeautifulStoneSoup(f.read())
        dv_lst=self.xmldoc.findAll("device")
        for dv in dv_lst:
            dv_dict={}
            dv_dict[dv.devicename.name]=dv.devicename.text
            dv_dict[dv.devicedesc.name]=dv.devicedesc.text
            prop_lst=dv.findAll('property')
            proplist=[]
            for prop in prop_lst:
                prop_dict={}
                prop_dict[prop.propname.text]=prop.propvalue.text
                proplist.append(prop_dict)
            dv_dict['properties']=proplist
            self.devices.append(dv_dict)
        #print str(self.devices[0])

    def getDevicesNames(self):
        names=[]
        for dv in self.devices:
            names.append(dv['devicename'])
        return names

    def getProperty(self,dvname,prop):
       for dv in self.devices:
           if(dvname == dv['devicename']):
               for p in dv['properties']:
                   if(prop in p):
                       return p[prop]

#fname="/home/dancioata/tscproject/tscrepository/config/testsuite_config.xml"
fname="xmlcfg/testsuite_config.xml"
cfgparser=TSConfigParser()
cfgparser.parseConfigFile(fname)


def getDevicesNames(*args):
    return cfgparser.getDevicesNames()

def getProperty(devname,prop):
    return cfgparser.getProperty(devname,prop)

#register python functions to tcl
tcl=Tcl()
cmd = tcl.createcommand("getDevicesNames", getDevicesNames)
cmd1= tcl.createcommand("getProperty", getProperty)

# call it, and print the results:
#result = tcl.eval("getDevicesNames")
#result = tcl.eval("getProperty DUT1 TerminalServerIp")
#result = tcl.eval("getProperty DUT1 TerminalServerPort")
#result=tcl.evalfile("/home/dancioata/tscproject/tscrepository/pyexport.tcl")

def run_tcl_tests():
    tcl=Tcl()
    cmd = tcl.createcommand("getDevicesNames", getDevicesNames)
    cmd1= tcl.createcommand("getProperty", getProperty)

    fname="/home/dancioata/tscproject/tscrepository/config/testsuite_config.xml"
    cfgparser=TSConfigParser()
    cfgparser.parseConfigFile(fname)
    tcl.eval("source testcases/ceslib.tcl")
    tcl.eval("source testcases/setup.tcl")
    tcl.eval('setup_ace 0')
    tcl.eval("source testcases/t001.tcl")
    tcl.eval("T-001")
    tcl.eval("source testcases/t002.tcl")
    tcl.eval("T-002")
    tcl.eval("source testcases/t003.tcl")
    tcl.eval("T-003")
    tcl.eval("source testcases/t007.tcl")
    tcl.eval("T-007")
    tcl.eval("source testcases/t008.tcl")
    tcl.eval("T-008")
    tcl.eval("source testcases/t009.tcl")
    tcl.eval("T-009")
    tcl.eval("source testcases/t012.tcl")
    tcl.eval("T-012")
    tcl.eval("source testcases/t013.tcl")
    tcl.eval("source testcases/t014.tcl")
    tcl.eval("source testcases/t015.tcl")

def main():

    run_tcl_tests()
    #print cfgparser.getDevicesNames()
    #print cfgparser.getProperty('DUT1','TerminalServerIp')
    #print cfgparser.getProperty('DUT1','TerminalServerPort')
    #print cfgparser.getProperty('DUT2','TerminalServerIp')
    #print cfgparser.getProperty('DUT2','TerminalServerPort')


if __name__ == "__main__":
    main()
