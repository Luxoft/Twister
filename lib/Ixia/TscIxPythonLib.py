# File: TscIxPythonLib.py ; This file is part of Twister.

# version: 2.002

# Copyright (C) 2013 , Luxoft

# Authors:
#    Adrian Toader <adtoader@luxoft.com>
#    Andrei Costachi <acostachi@luxoft.com>
#    Andrei Toma <atoma@luxoft.com>
#    Cristi Constantin <crconstantin@luxoft.com>
#    Daniel Cioata <dcioata@luxoft.com>
#    Mihail Tudoran <mtudoran@luxoft.com>

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''
This module contains wrapper functions for Ixia traffic generator TCL library
'''
from Tkinter import Tcl

t = Tcl()

t.eval('package req IxTclHal')

true  = True
false = False
yes   = True
no    = False
none  = None


def ixDapConfigPort(chassis, card, port, macAddress, ipAddress, gateway, mask, enableVlan=False, vlanId=0):
    # TCL cmd :: ixDapConfigPort chassis card port macAddress ipAddress gateway mask enableVlan {false} vlanId {0}
    r = t.eval("ixDapConfigPort {} {} {} {} {} {} {} {} {} ".format(chassis, card, port, macAddress, ipAddress, gateway, mask, enableVlan, vlanId))
    return r


def ixDapAddPortInterface(args):
    # TCL cmd :: ixDapAddPortInterface args
    r = t.eval("ixDapAddPortInterface {} ".format(args))
    return r


def ixDapAddRouteTable(args):
    # TCL cmd :: ixDapAddRouteTable args
    r = t.eval("ixDapAddRouteTable {} ".format(args))
    return r


def ixDapAddPortFilter(args):
    # TCL cmd :: ixDapAddPortFilter args
    r = t.eval("ixDapAddPortFilter {} ".format(args))
    return r


def ixDapBaseIpAddresses(args):
    # TCL cmd :: ixDapBaseIpAddresses args
    r = t.eval("ixDapBaseIpAddresses {} ".format(args))
    return r


def ixDapCleanUp():
    # TCL cmd :: ixDapCleanUp
    r = t.eval("ixDapCleanUp ".format())
    return r


def ixDapSetBaseIp(chassisName, ipAddress, mask="255.255.0.0"):
    # TCL cmd :: ixDapSetBaseIp chassisName ipAddress mask {255.255.0.0}
    r = t.eval("ixDapSetBaseIp {} {} {} ".format(chassisName, ipAddress, mask))
    return r


def ixDapAddRoute(destination, mask, interface):
    # TCL cmd :: ixDapAddRoute destination mask interface
    r = t.eval("ixDapAddRoute {} {} {} ".format(destination, mask, interface))
    return r


def ixDapDelRoute(destination):
    # TCL cmd :: ixDapDelRoute destination
    r = t.eval("ixDapDelRoute {} ".format(destination))
    return r


def ixDapLogin(userName):
    # TCL cmd :: ixDapLogin userName
    r = t.eval("ixDapLogin {} ".format(userName))
    return r


def clearStatsAndTransmit(TxRxArray, duration, staggeredStart="notStaggeredStart", calcAvgRates=False, AvgRateArray=None, calcQosRates=False, QosRateArray=None, calcTxRxRates=False, delay="delay"):
    # TCL cmd :: clearStatsAndTransmit TxRxArray duration staggeredStart {notStaggeredStart} calcAvgRates {no} AvgRateArray calcQosRates {no} QosRateArray calcTxRxRates {no} delay {delay}
    if AvgRateArray is None: print "TCL argument `AvgRateArray` cannot be empty!"; return False
    if QosRateArray is None: print "TCL argument `QosRateArray` cannot be empty!"; return False
    r = t.eval("clearStatsAndTransmit {} {} {} {} {} {} {} {} {} ".format(TxRxArray, duration, staggeredStart, calcAvgRates, AvgRateArray, calcQosRates, QosRateArray, calcTxRxRates, delay))
    return r


def transmitAndCollectRxRatesPerSecond(TxRxArray, RxRateArray, rxRateArgs, duration, staggeredStart="notStaggeredStart"):
    # TCL cmd :: transmitAndCollectRxRatesPerSecond TxRxArray RxRateArray rxRateArgs duration staggeredStart {notStaggeredStart}
    r = t.eval("transmitAndCollectRxRatesPerSecond {} {} {} {} {} ".format(TxRxArray, RxRateArray, rxRateArgs, duration, staggeredStart))
    return r


def collectRxRatesPerSecond(TxRxArray, RxRateArray, rxRateArgs, duration):
    # TCL cmd :: collectRxRatesPerSecond TxRxArray RxRateArray rxRateArgs duration
    r = t.eval("collectRxRatesPerSecond {} {} {} {} ".format(TxRxArray, RxRateArray, rxRateArgs, duration))
    return r


def prepareToTransmit(TxRxArray):
    # TCL cmd :: prepareToTransmit TxRxArray
    r = t.eval("prepareToTransmit {} ".format(TxRxArray))
    return r


def writeWaitForTransmit(duration, destroy="destroy"):
    # TCL cmd :: writeWaitForTransmit duration destroy {destroy}
    r = t.eval("writeWaitForTransmit {} {} ".format(duration, destroy))
    return r


def writeWaitForPause(dialogName, duration, destroy="destroy"):
    # TCL cmd :: writeWaitForPause dialogName duration destroy {destroy}
    r = t.eval("writeWaitForPause {} {} {} ".format(dialogName, duration, destroy))
    return r


def writeWaitMessage(dialogName, messageType, duration, destroy="destroy"):
    # TCL cmd :: writeWaitMessage dialogName messageType duration destroy {destroy}
    r = t.eval("writeWaitMessage {} {} {} {} ".format(dialogName, messageType, duration, destroy))
    return r


def issuePortGroupCommand(command, TxRxList, verbose="noVerbose", LastTimestamp=None, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: issuePortGroupCommand command TxRxList verbose {noVerbose} LastTimestamp groupId {710} create {create} destroy {destroy}
    if LastTimestamp is None: print "TCL argument `LastTimestamp` cannot be empty!"; return False
    r = t.eval("issuePortGroupCommand {} {} {} {} {} {} {} ".format(command, TxRxList, verbose, LastTimestamp, groupId, create, destroy))
    return r


def getPortGroupObject(ix_object, TxRxList, verbose="noVerbose", groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: getPortGroupObject object TxRxList verbose {noVerbose} groupId {710} create {create} destroy {destroy}
    r = t.eval("getPortGroupObject {} {} {} {} {} {} ".format(ix_object, TxRxList, verbose, groupId, create, destroy))
    return r


def issuePortGroupMethod(PortArray, LastTimestamp, args):
    # TCL cmd :: issuePortGroupMethod PortArray LastTimestamp args
    r = t.eval("issuePortGroupMethod {} {} {} ".format(PortArray, LastTimestamp, args))
    return r


def startTx(TxRxArray, staggeredStart="notStaggeredStart", FirstTimestamp=None, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: startTx TxRxArray staggeredStart {notStaggeredStart} FirstTimestamp groupId {710} create {create} destroy {destroy}
    if FirstTimestamp is None: print "TCL argument `FirstTimestamp` cannot be empty!"; return False
    r = t.eval("startTx {} {} {} {} {} {} ".format(TxRxArray, staggeredStart, FirstTimestamp, groupId, create, destroy))
    return r


def startStaggeredTx(TxRxArray, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: startStaggeredTx TxRxArray groupId {710} create {create} destroy {destroy}
    r = t.eval("startStaggeredTx {} {} {} {} ".format(TxRxArray, groupId, create, destroy))
    return r


def stopTx(TxRxArray, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: stopTx TxRxArray groupId {710} create {create} destroy {destroy}
    r = t.eval("stopTx {} {} {} {} ".format(TxRxArray, groupId, create, destroy))
    return r


def startPortTx(chassis, lm, port, FirstTimestamp, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: startPortTx chassis lm port FirstTimestamp groupId {710} create {create} destroy {destroy}
    r = t.eval("startPortTx {} {} {} {} {} {} {} ".format(chassis, lm, port, FirstTimestamp, groupId, create, destroy))
    return r


def stopPortTx(chassis, lm, port, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: stopPortTx chassis lm port groupId {710} create {create} destroy {destroy}
    r = t.eval("stopPortTx {} {} {} {} {} {} ".format(chassis, lm, port, groupId, create, destroy))
    return r


def startCapture(TxRxArray, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: startCapture TxRxArray groupId {710} create {create} destroy {destroy}
    r = t.eval("startCapture {} {} {} {} ".format(TxRxArray, groupId, create, destroy))
    return r


def startPrbsCapture(TxRxArray, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: startPrbsCapture TxRxArray groupId {710} create {create} destroy {destroy}
    r = t.eval("startPrbsCapture {} {} {} {} ".format(TxRxArray, groupId, create, destroy))
    return r


def stopCapture(TxRxArray, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: stopCapture TxRxArray groupId {710} create {create} destroy {destroy}
    r = t.eval("stopCapture {} {} {} {} ".format(TxRxArray, groupId, create, destroy))
    return r


def stopPrbsCapture(TxRxArray, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: stopPrbsCapture TxRxArray groupId {710} create {create} destroy {destroy}
    r = t.eval("stopPrbsCapture {} {} {} {} ".format(TxRxArray, groupId, create, destroy))
    return r


def clearPrbsCapture(TxRxArray, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: clearPrbsCapture TxRxArray groupId {710} create {create} destroy {destroy}
    r = t.eval("clearPrbsCapture {} {} {} {} ".format(TxRxArray, groupId, create, destroy))
    return r


def startPortCapture(chassis, lm, port, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: startPortCapture chassis lm port groupId {710} create {create} destroy {destroy}
    r = t.eval("startPortCapture {} {} {} {} {} {} ".format(chassis, lm, port, groupId, create, destroy))
    return r


def startPortPrbsCapture(chassis, lm, port, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: startPortPrbsCapture chassis lm port groupId {710} create {create} destroy {destroy}
    r = t.eval("startPortPrbsCapture {} {} {} {} {} {} ".format(chassis, lm, port, groupId, create, destroy))
    return r


def stopPortCapture(chassis, lm, port, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: stopPortCapture chassis lm port groupId {710} create {create} destroy {destroy}
    r = t.eval("stopPortCapture {} {} {} {} {} {} ".format(chassis, lm, port, groupId, create, destroy))
    return r


def stopPortPrbsCapture(chassis, lm, port, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: stopPortPrbsCapture chassis lm port groupId {710} create {create} destroy {destroy}
    r = t.eval("stopPortPrbsCapture {} {} {} {} {} {} ".format(chassis, lm, port, groupId, create, destroy))
    return r


def clearPortPrbsCapture(chassis, lm, port, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: clearPortPrbsCapture chassis lm port groupId {710} create {create} destroy {destroy}
    r = t.eval("clearPortPrbsCapture {} {} {} {} {} {} ".format(chassis, lm, port, groupId, create, destroy))
    return r


def startPacketGroups(TxRxArray, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: startPacketGroups TxRxArray groupId {710} create {create} destroy {destroy}
    r = t.eval("startPacketGroups {} {} {} {} ".format(TxRxArray, groupId, create, destroy))
    return r


def stopPacketGroups(TxRxArray, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: stopPacketGroups TxRxArray groupId {710} create {create} destroy {destroy}
    r = t.eval("stopPacketGroups {} {} {} {} ".format(TxRxArray, groupId, create, destroy))
    return r


def startPortPacketGroups(chassis, lm, port, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: startPortPacketGroups chassis lm port groupId {710} create {create} destroy {destroy}
    r = t.eval("startPortPacketGroups {} {} {} {} {} {} ".format(chassis, lm, port, groupId, create, destroy))
    return r


def stopPortPacketGroups(chassis, lm, port, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: stopPortPacketGroups chassis lm port groupId {710} create {create} destroy {destroy}
    r = t.eval("stopPortPacketGroups {} {} {} {} {} {} ".format(chassis, lm, port, groupId, create, destroy))
    return r


def clearPacketGroups(TxRxArray, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: clearPacketGroups TxRxArray groupId {710} create {create} destroy {destroy}
    r = t.eval("clearPacketGroups {} {} {} {} ".format(TxRxArray, groupId, create, destroy))
    return r


def clearPortPacketGroups(chassis, lm, port, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: clearPortPacketGroups chassis lm port groupId {710} create {create} destroy {destroy}
    r = t.eval("clearPortPacketGroups {} {} {} {} {} {} ".format(chassis, lm, port, groupId, create, destroy))
    return r


def startCollisions(TxRxArray, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: startCollisions TxRxArray groupId {710} create {create} destroy {destroy}
    r = t.eval("startCollisions {} {} {} {} ".format(TxRxArray, groupId, create, destroy))
    return r


def stopCollisions(TxRxArray, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: stopCollisions TxRxArray groupId {710} create {create} destroy {destroy}
    r = t.eval("stopCollisions {} {} {} {} ".format(TxRxArray, groupId, create, destroy))
    return r


def startPortCollisions(c, l, p, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: startPortCollisions c l p groupId {710} create {create} destroy {destroy}
    r = t.eval("startPortCollisions {} {} {} {} {} {} ".format(c, l, p, groupId, create, destroy))
    return r


def stopPortCollisions(c, l, p, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: stopPortCollisions c l p groupId {710} create {create} destroy {destroy}
    r = t.eval("stopPortCollisions {} {} {} {} {} {} ".format(c, l, p, groupId, create, destroy))
    return r


def zeroStats(TxRxArray, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: zeroStats TxRxArray groupId {710} create {create} destroy {destroy}
    r = t.eval("zeroStats {} {} {} {} ".format(TxRxArray, groupId, create, destroy))
    return r


def zeroPortStats(chassis, lm, port, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: zeroPortStats chassis lm port groupId {710} create {create} destroy {destroy}
    r = t.eval("zeroPortStats {} {} {} {} {} {} ".format(chassis, lm, port, groupId, create, destroy))
    return r


def clearPerStreamTxStats(TxRxArray, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: clearPerStreamTxStats TxRxArray groupId {710} create {create} destroy {destroy}
    r = t.eval("clearPerStreamTxStats {} {} {} {} ".format(TxRxArray, groupId, create, destroy))
    return r


def clearPerStreamTxPortStats(chassis, lm, port, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: clearPerStreamTxPortStats chassis lm port groupId {710} create {create} destroy {destroy}
    r = t.eval("clearPerStreamTxPortStats {} {} {} {} {} {} ".format(chassis, lm, port, groupId, create, destroy))
    return r


def clearPcsLaneStatistics(TxRxArray, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: clearPcsLaneStatistics TxRxArray groupId {710} create {create} destroy {destroy}
    r = t.eval("clearPcsLaneStatistics {} {} {} {} ".format(TxRxArray, groupId, create, destroy))
    return r


def clearPcsLanePortStatistics(chassis, lm, port, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: clearPcsLanePortStatistics chassis lm port groupId {710} create {create} destroy {destroy}
    r = t.eval("clearPcsLanePortStatistics {} {} {} {} {} {} ".format(chassis, lm, port, groupId, create, destroy))
    return r


def clearTimeStamp(TxRxArray, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: clearTimeStamp TxRxArray groupId {710} create {create} destroy {destroy}
    r = t.eval("clearTimeStamp {} {} {} {} ".format(TxRxArray, groupId, create, destroy))
    return r


def flushAddressTable(PortMap, checkLink=yes):
    # TCL cmd :: flushAddressTable PortMap checkLink {yes}
    r = t.eval("flushAddressTable {} {} ".format(PortMap, checkLink))
    return r


def enableArpResponse(mapType, PortMap, write="nowrite"):
    # TCL cmd :: enableArpResponse mapType PortMap write {nowrite}
    r = t.eval("enableArpResponse {} {} {} ".format(mapType, PortMap, write))
    return r


def enablePortArpResponse(mapType, chassis, lm, port, write="write"):
    # TCL cmd :: enablePortArpResponse mapType chassis lm port write {write}
    r = t.eval("enablePortArpResponse {} {} {} {} {} ".format(mapType, chassis, lm, port, write))
    return r


def disableArpResponse(PortMap, write="nowrite"):
    # TCL cmd :: disableArpResponse PortMap write {nowrite}
    r = t.eval("disableArpResponse {} {} ".format(PortMap, write))
    return r


def disablePortArpResponse(chassis, lm, port, write="write"):
    # TCL cmd :: disablePortArpResponse chassis lm port write {write}
    r = t.eval("disablePortArpResponse {} {} {} {} ".format(chassis, lm, port, write))
    return r


def transmitArpRequest(TxRxArray, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: transmitArpRequest TxRxArray groupId {710} create {create} destroy {destroy}
    r = t.eval("transmitArpRequest {} {} {} {} ".format(TxRxArray, groupId, create, destroy))
    return r


def transmitPortArpRequest(chassis, lm, port):
    # TCL cmd :: transmitPortArpRequest chassis lm port
    r = t.eval("transmitPortArpRequest {} {} {} ".format(chassis, lm, port))
    return r


def clearArpTable(TxRxArray, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: clearArpTable TxRxArray groupId {710} create {create} destroy {destroy}
    r = t.eval("clearArpTable {} {} {} {} ".format(TxRxArray, groupId, create, destroy))
    return r


def clearPortArpTable(chassis, lm, port):
    # TCL cmd :: clearPortArpTable chassis lm port
    r = t.eval("clearPortArpTable {} {} {} ".format(chassis, lm, port))
    return r


def setDataIntegrityMode(TxRxArray, write="nowrite"):
    # TCL cmd :: setDataIntegrityMode TxRxArray write {nowrite}
    r = t.eval("setDataIntegrityMode {} {} ".format(TxRxArray, write))
    return r


def setPrbsMode(TxRxArray, write="nowrite"):
    # TCL cmd :: setPrbsMode TxRxArray write {nowrite}
    r = t.eval("setPrbsMode {} {} ".format(TxRxArray, write))
    return r


def setPacketGroupMode(TxRxArray, write="nowrite"):
    # TCL cmd :: setPacketGroupMode TxRxArray write {nowrite}
    r = t.eval("setPacketGroupMode {} {} ".format(TxRxArray, write))
    return r


def setWidePacketGroupMode(TxRxArray, write="nowrite"):
    # TCL cmd :: setWidePacketGroupMode TxRxArray write {nowrite}
    r = t.eval("setWidePacketGroupMode {} {} ".format(TxRxArray, write))
    return r


def setCaptureMode(TxRxArray, write="nowrite"):
    # TCL cmd :: setCaptureMode TxRxArray write {nowrite}
    r = t.eval("setCaptureMode {} {} ".format(TxRxArray, write))
    return r


def setTcpRoundTripFlowMode(TxRxArray, write="nowrite"):
    # TCL cmd :: setTcpRoundTripFlowMode TxRxArray write {nowrite}
    r = t.eval("setTcpRoundTripFlowMode {} {} ".format(TxRxArray, write))
    return r


def setPacketStreamMode(TxRxArray, write="nowrite"):
    # TCL cmd :: setPacketStreamMode TxRxArray write {nowrite}
    r = t.eval("setPacketStreamMode {} {} ".format(TxRxArray, write))
    return r


def setPacketFlowMode(TxRxArray, write="nowrite"):
    # TCL cmd :: setPacketFlowMode TxRxArray write {nowrite}
    r = t.eval("setPacketFlowMode {} {} ".format(TxRxArray, write))
    return r


def setAdvancedStreamSchedulerMode(TxRxArray, write="nowrite"):
    # TCL cmd :: setAdvancedStreamSchedulerMode TxRxArray write {nowrite}
    r = t.eval("setAdvancedStreamSchedulerMode {} {} ".format(TxRxArray, write))
    return r


def setFirstLastTimestampMode(TxRxArray, write="nowrite"):
    # TCL cmd :: setFirstLastTimestampMode TxRxArray write {nowrite}
    r = t.eval("setFirstLastTimestampMode {} {} ".format(TxRxArray, write))
    return r


def setDataIntegrityMode(TxRxArray, write="nowrite"):
    # TCL cmd :: setDataIntegrityMode TxRxArray write {nowrite}
    r = t.eval("setDataIntegrityMode {} {} ".format(TxRxArray, write))
    return r


def setSequenceCheckingMode(TxRxArray, write="nowrite"):
    # TCL cmd :: setSequenceCheckingMode TxRxArray write {nowrite}
    r = t.eval("setSequenceCheckingMode {} {} ".format(TxRxArray, write))
    return r


def changePortTransmitMode(TxRxArray, transmitMode, write="nowrite"):
    # TCL cmd :: changePortTransmitMode TxRxArray transmitMode write {nowrite}
    r = t.eval("changePortTransmitMode {} {} {} ".format(TxRxArray, transmitMode, write))
    return r


def changePortReceiveMode(TxRxArray, receiveMode, write="nowrite", verbose=yes):
    # TCL cmd :: changePortReceiveMode TxRxArray receiveMode write {nowrite} verbose {yes}
    r = t.eval("changePortReceiveMode {} {} {} {} ".format(TxRxArray, receiveMode, write, verbose))
    return r


def writeToHardware(PortArray, args):
    # TCL cmd :: writeToHardware PortArray args
    r = t.eval("writeToHardware {} {} ".format(PortArray, args))
    return r


def writeToHardwareAsChunks(PortArray, action, args):
    # TCL cmd :: writeToHardwareAsChunks PortArray action args
    r = t.eval("writeToHardwareAsChunks {} {} {} ".format(PortArray, action, args))
    return r


def writePortsToHardware(PortArray, args):
    # TCL cmd :: writePortsToHardware PortArray args
    r = t.eval("writePortsToHardware {} {} ".format(PortArray, args))
    return r


def writeConfigToHardware(PortArray, args):
    # TCL cmd :: writeConfigToHardware PortArray args
    r = t.eval("writeConfigToHardware {} {} ".format(PortArray, args))
    return r


def resetSequenceIndex(TxRxArray, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: resetSequenceIndex TxRxArray groupId {710} create {create} destroy {destroy}
    r = t.eval("resetSequenceIndex {} {} {} {} ".format(TxRxArray, groupId, create, destroy))
    return r


def resetPortSequenceIndex(chassis, lm, port, FirstTimestamp, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: resetPortSequenceIndex chassis lm port FirstTimestamp groupId {710} create {create} destroy {destroy}
    r = t.eval("resetPortSequenceIndex {} {} {} {} {} {} {} ".format(chassis, lm, port, FirstTimestamp, groupId, create, destroy))
    return r


def loadPoePulse(TxRxArray, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: loadPoePulse TxRxArray groupId {710} create {create} destroy {destroy}
    r = t.eval("loadPoePulse {} {} {} {} ".format(TxRxArray, groupId, create, destroy))
    return r


def loadPortPoePulse(chassis, lm, port):
    # TCL cmd :: loadPortPoePulse chassis lm port
    r = t.eval("loadPortPoePulse {} {} {} ".format(chassis, lm, port))
    return r


def armPoeTrigger(TxRxArray, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: armPoeTrigger TxRxArray groupId {710} create {create} destroy {destroy}
    r = t.eval("armPoeTrigger {} {} {} {} ".format(TxRxArray, groupId, create, destroy))
    return r


def armPortPoeTrigger(chassis, lm, port):
    # TCL cmd :: armPortPoeTrigger chassis lm port
    r = t.eval("armPortPoeTrigger {} {} {} ".format(chassis, lm, port))
    return r


def abortPoeArm(TxRxArray, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: abortPoeArm TxRxArray groupId {710} create {create} destroy {destroy}
    r = t.eval("abortPoeArm {} {} {} {} ".format(TxRxArray, groupId, create, destroy))
    return r


def abortPortPoeArm(chassis, lm, port):
    # TCL cmd :: abortPortPoeArm chassis lm port
    r = t.eval("abortPortPoeArm {} {} {} ".format(chassis, lm, port))
    return r


def resetSequenceIndex(TxRxArray, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: resetSequenceIndex TxRxArray groupId {710} create {create} destroy {destroy}
    r = t.eval("resetSequenceIndex {} {} {} {} ".format(TxRxArray, groupId, create, destroy))
    return r


def resetPortSequenceIndex(chassis, lm, port, FirstTimestamp, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: resetPortSequenceIndex chassis lm port FirstTimestamp groupId {710} create {create} destroy {destroy}
    r = t.eval("resetPortSequenceIndex {} {} {} {} {} {} {} ".format(chassis, lm, port, FirstTimestamp, groupId, create, destroy))
    return r


def loadPoEPulse(TxRxArray, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: loadPoEPulse TxRxArray groupId {710} create {create} destroy {destroy}
    r = t.eval("loadPoEPulse {} {} {} {} ".format(TxRxArray, groupId, create, destroy))
    return r


def loadPortPoEPulse(chassis, lm, port, FirstTimestamp, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: loadPortPoEPulse chassis lm port FirstTimestamp groupId {710} create {create} destroy {destroy}
    r = t.eval("loadPortPoEPulse {} {} {} {} {} {} {} ".format(chassis, lm, port, FirstTimestamp, groupId, create, destroy))
    return r


def restartAutoNegotiation(TxRxArray, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: restartAutoNegotiation TxRxArray groupId {710} create {create} destroy {destroy}
    r = t.eval("restartAutoNegotiation {} {} {} {} ".format(TxRxArray, groupId, create, destroy))
    return r


def rebootLocalCpu(TxRxArray, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: rebootLocalCpu TxRxArray groupId {710} create {create} destroy {destroy}
    r = t.eval("rebootLocalCpu {} {} {} {} ".format(TxRxArray, groupId, create, destroy))
    return r


def rebootPortLocalCpu(chassis, lm, port, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: rebootPortLocalCpu chassis lm port groupId {710} create {create} destroy {destroy}
    r = t.eval("rebootPortLocalCpu {} {} {} {} {} {} ".format(chassis, lm, port, groupId, create, destroy))
    return r


def simulatePhysicalInterfaceDown(TxRxArray, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: simulatePhysicalInterfaceDown TxRxArray groupId {710} create {create} destroy {destroy}
    r = t.eval("simulatePhysicalInterfaceDown {} {} {} {} ".format(TxRxArray, groupId, create, destroy))
    return r


def simulatePortPhysicalInterfaceDown(chassis, lm, port, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: simulatePortPhysicalInterfaceDown chassis lm port groupId {710} create {create} destroy {destroy}
    r = t.eval("simulatePortPhysicalInterfaceDown {} {} {} {} {} {} ".format(chassis, lm, port, groupId, create, destroy))
    return r


def simulatePhysicalInterfaceUp(TxRxArray, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: simulatePhysicalInterfaceUp TxRxArray groupId {710} create {create} destroy {destroy}
    r = t.eval("simulatePhysicalInterfaceUp {} {} {} {} ".format(TxRxArray, groupId, create, destroy))
    return r


def simulatePortPhysicalInterfaceUp(chassis, lm, port, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: simulatePortPhysicalInterfaceUp chassis lm port groupId {710} create {create} destroy {destroy}
    r = t.eval("simulatePortPhysicalInterfaceUp {} {} {} {} {} {} ".format(chassis, lm, port, groupId, create, destroy))
    return r


def startAtmOamTransmit(TxRxArray, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: startAtmOamTransmit TxRxArray groupId {710} create {create} destroy {destroy}
    r = t.eval("startAtmOamTransmit {} {} {} {} ".format(TxRxArray, groupId, create, destroy))
    return r


def startPortAtmOamTransmit(chassis, lm, port):
    # TCL cmd :: startPortAtmOamTransmit chassis lm port
    r = t.eval("startPortAtmOamTransmit {} {} {} ".format(chassis, lm, port))
    return r


def stopAtmOamTransmit(TxRxArray, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: stopAtmOamTransmit TxRxArray groupId {710} create {create} destroy {destroy}
    r = t.eval("stopAtmOamTransmit {} {} {} {} ".format(TxRxArray, groupId, create, destroy))
    return r


def stopPortAtmOamTransmit(chassis, lm, port):
    # TCL cmd :: stopPortAtmOamTransmit chassis lm port
    r = t.eval("stopPortAtmOamTransmit {} {} {} ".format(chassis, lm, port))
    return r


def setScheduledTransmitTime(TxRxArray, duration, groupId=710):
    # TCL cmd :: setScheduledTransmitTime TxRxArray duration groupId {710}
    r = t.eval("setScheduledTransmitTime {} {} {} ".format(TxRxArray, duration, groupId))
    return r


def setAutoDetectInstrumentationMode(TxRxArray, write="nowrite"):
    # TCL cmd :: setAutoDetectInstrumentationMode TxRxArray write {nowrite}
    r = t.eval("setAutoDetectInstrumentationMode {} {} ".format(TxRxArray, write))
    return r


def enablePortIntrinsicLatencyAdjustment(chassId, cardId, portId, enable, write="nowrite"):
    # TCL cmd :: enablePortIntrinsicLatencyAdjustment chassId cardId portId enable write {nowrite}
    r = t.eval("enablePortIntrinsicLatencyAdjustment {} {} {} {} {} ".format(chassId, cardId, portId, enable, write))
    return r


def enableIntrinsicLatencyAdjustment(TxRxArray, enable, write="nowrite"):
    # TCL cmd :: enableIntrinsicLatencyAdjustment TxRxArray enable write {nowrite}
    r = t.eval("enableIntrinsicLatencyAdjustment {} {} {} ".format(TxRxArray, enable, write))
    return r


def isIntrinsicLatencyAdjustmentEnabled(chassId, cardId, portId):
    # TCL cmd :: isIntrinsicLatencyAdjustmentEnabled chassId cardId portId
    r = t.eval("isIntrinsicLatencyAdjustmentEnabled {} {} {} ".format(chassId, cardId, portId))
    return r


def ipAddressSetDefault():
    # TCL cmd :: ipAddressSetDefault
    r = t.eval("ipAddressSetDefault ".format())
    return r


def updateIpAddressTable(chassis, card, port, write="nowrite"):
    # TCL cmd :: updateIpAddressTable chassis card port write {nowrite}
    r = t.eval("updateIpAddressTable {} {} {} {} ".format(chassis, card, port, write))
    return r


def mpincr(args):
    # TCL cmd :: mpincr args
    r = t.eval("mpincr {} ".format(args))
    return r


def calculatePercentLossExact(txFrames, rxFrames):
    # TCL cmd :: calculatePercentLossExact txFrames rxFrames
    r = t.eval("calculatePercentLossExact {} {} ".format(txFrames, rxFrames))
    return r


def calculatePercentLoss(txFrames, rxFrames):
    # TCL cmd :: calculatePercentLoss txFrames rxFrames
    r = t.eval("calculatePercentLoss {} {} ".format(txFrames, rxFrames))
    return r


def calculatePercentThroughput(tputRate, maxRate):
    # TCL cmd :: calculatePercentThroughput tputRate maxRate
    r = t.eval("calculatePercentThroughput {} {} ".format(tputRate, maxRate))
    return r


def calculateDuration(numTxFrames, frameRate, numFrames=1, loopcount=1):
    # TCL cmd :: calculateDuration numTxFrames frameRate numFrames {1} loopcount {1}
    r = t.eval("calculateDuration {} {} {} {} ".format(numTxFrames, frameRate, numFrames, loopcount))
    return r


def calculateTotalBursts(framerate, ifg, burstsize, ibg, duration=1):
    # TCL cmd :: calculateTotalBursts framerate ifg burstsize ibg duration {1}
    r = t.eval("calculateTotalBursts {} {} {} {} {} ".format(framerate, ifg, burstsize, ibg, duration))
    return r


def calculateAvgLatency(LatencyArray):
    # TCL cmd :: calculateAvgLatency LatencyArray
    r = t.eval("calculateAvgLatency {} ".format(LatencyArray))
    return r


def calculateLoopCounterFromTxFrames(totalFrames):
    # TCL cmd :: calculateLoopCounterFromTxFrames totalFrames
    r = t.eval("calculateLoopCounterFromTxFrames {} ".format(totalFrames))
    return r


def calculateStreamNumFrames(framerate, Duration, maxNumFrames=0xffffffff):
    # TCL cmd :: calculateStreamNumFrames framerate Duration maxNumFrames {0xffffffff}
    r = t.eval("calculateStreamNumFrames {} {} {} ".format(framerate, Duration, maxNumFrames))
    return r


def getTransmitTime(PortArray, originalDuration, DurationArray, Warnings):
    # TCL cmd :: getTransmitTime PortArray originalDuration DurationArray Warnings
    r = t.eval("getTransmitTime {} {} {} {} ".format(PortArray, originalDuration, DurationArray, Warnings))
    return r


def getDurationFromCapture(PortArray, tx_c, tx_l, tx_p, originalDuration):
    # TCL cmd :: getDurationFromCapture PortArray tx_c tx_l tx_p originalDuration
    r = t.eval("getDurationFromCapture {} {} {} {} {} ".format(PortArray, tx_c, tx_l, tx_p, originalDuration))
    return r


def maxArray(NumArray):
    # TCL cmd :: maxArray NumArray
    r = t.eval("maxArray {} ".format(NumArray))
    return r


def connectToChassis(chassisList, cableLengthList="cable3feet", chassisIdList=None, chassisSeqList=None):
    # TCL cmd :: connectToChassis chassisList cableLengthList {cable3feet} chassisIdList chassisSeqList
    if chassisIdList is None: print "TCL argument `chassisIdList` cannot be empty!"; return False
    if chassisSeqList is None: print "TCL argument `chassisSeqList` cannot be empty!"; return False
    r = t.eval("connectToChassis {} {} {} {} ".format(chassisList, cableLengthList, chassisIdList, chassisSeqList))
    return r


def setConnectChassisFlag(value):
    # TCL cmd :: setConnectChassisFlag value
    r = t.eval("setConnectChassisFlag {} ".format(value))
    return r


def getConnectChassisFlag():
    # TCL cmd :: getConnectChassisFlag
    r = t.eval("getConnectChassisFlag ".format())
    return r


def clientOpen(host, port):
    # TCL cmd :: clientOpen host port
    r = t.eval("clientOpen {} {} ".format(host, port))
    return r


def clientClose(socketId):
    # TCL cmd :: clientClose socketId
    r = t.eval("clientClose {} ".format(socketId))
    return r


def clientSend(socketId, args):
    # TCL cmd :: clientSend socketId args
    r = t.eval("clientSend {} {} ".format(socketId, args))
    return r


def remoteDefine(commandList):
    # TCL cmd :: remoteDefine commandList
    r = t.eval("remoteDefine {} ".format(commandList))
    return r


def getConstantsValue(serverSocket):
    # TCL cmd :: getConstantsValue serverSocket
    r = t.eval("getConstantsValue {} ".format(serverSocket))
    return r


def ixMasterSet(name, element, op):
    # TCL cmd :: ixMasterSet name element op
    r = t.eval("ixMasterSet {} {} {} ".format(name, element, op))
    return r


def redefineCommand(command):
    # TCL cmd :: redefineCommand command
    r = t.eval("redefineCommand {} ".format(command))
    return r


def doFileTransfer(action, filename1, filename2, port=4500):
    # TCL cmd :: doFileTransfer action filename1 filename2 port {4500}
    r = t.eval("doFileTransfer {} {} {} {} ".format(action, filename1, filename2, port))
    return r


def getPercentMaxRate(chassis, card, port, framesize, rateType, rate, preambleSize=8):
    # TCL cmd :: getPercentMaxRate chassis card port framesize rateType rate preambleSize {8}
    r = t.eval("getPercentMaxRate {} {} {} {} {} {} {} ".format(chassis, card, port, framesize, rateType, rate, preambleSize))
    return r


def getMaxFPS(speed, framesize, preambleSize=8):
    # TCL cmd :: getMaxFPS speed framesize preambleSize {8}
    r = t.eval("getMaxFPS {} {} {} ".format(speed, framesize, preambleSize))
    return r


def convertPercentMaxRate(framesize, rateType, rate, speed, preambleSize=8):
    # TCL cmd :: convertPercentMaxRate framesize rateType rate speed preambleSize {8}
    r = t.eval("convertPercentMaxRate {} {} {} {} {} ".format(framesize, rateType, rate, speed, preambleSize))
    return r


def convertKbpsRate(framesize, rateType, rate, speed, preambleSize=8):
    # TCL cmd :: convertKbpsRate framesize rateType rate speed preambleSize {8}
    r = t.eval("convertKbpsRate {} {} {} {} {} ".format(framesize, rateType, rate, speed, preambleSize))
    return r


def convertFpsRate(framesize, rateType, rate, speed, preambleSize=8):
    # TCL cmd :: convertFpsRate framesize rateType rate speed preambleSize {8}
    r = t.eval("convertFpsRate {} {} {} {} {} ".format(framesize, rateType, rate, speed, preambleSize))
    return r


def generateFullList(originalList, burstsize=10):
    # TCL cmd :: generateFullList originalList burstsize {10}
    r = t.eval("generateFullList {} {} ".format(originalList, burstsize))
    return r


def initializeDefineCommand():
    # TCL cmd :: initializeDefineCommand
    r = t.eval("initializeDefineCommand ".format())
    return r


def initializeDefineTest():
    # TCL cmd :: initializeDefineTest
    r = t.eval("initializeDefineTest ".format())
    return r


def dhcpSetState(chassis, card, port, newState):
    # TCL cmd :: dhcpSetState chassis card port newState
    r = t.eval("dhcpSetState {} {} {} {} ".format(chassis, card, port, newState))
    return r


def dhcpGetState(chassis, card, port):
    # TCL cmd :: dhcpGetState chassis card port
    r = t.eval("dhcpGetState {} {} {} ".format(chassis, card, port))
    return r


def dhcpSetLease(chassis, card, port, lease):
    # TCL cmd :: dhcpSetLease chassis card port lease
    r = t.eval("dhcpSetLease {} {} {} {} ".format(chassis, card, port, lease))
    return r


def dhcpGetLease(chassis, card, port):
    # TCL cmd :: dhcpGetLease chassis card port
    r = t.eval("dhcpGetLease {} {} {} ".format(chassis, card, port))
    return r


def dhcpSetIP(chassis, card, port, ip):
    # TCL cmd :: dhcpSetIP chassis card port ip
    r = t.eval("dhcpSetIP {} {} {} {} ".format(chassis, card, port, ip))
    return r


def dhcpGetIP(chassis, card, port):
    # TCL cmd :: dhcpGetIP chassis card port
    r = t.eval("dhcpGetIP {} {} {} ".format(chassis, card, port))
    return r


def dhcpSetServer(chassis, card, port, server):
    # TCL cmd :: dhcpSetServer chassis card port server
    r = t.eval("dhcpSetServer {} {} {} {} ".format(chassis, card, port, server))
    return r


def dhcpGetServer(chassis, card, port):
    # TCL cmd :: dhcpGetServer chassis card port
    r = t.eval("dhcpGetServer {} {} {} ".format(chassis, card, port))
    return r


def dhcpGetTimer(timer):
    # TCL cmd :: dhcpGetTimer timer
    r = t.eval("dhcpGetTimer {} ".format(timer))
    return r


def dhcpStartTimers(lease, timer1=0, timer2=0):
    # TCL cmd :: dhcpStartTimers lease timer1 {0} timer2 {0}
    r = t.eval("dhcpStartTimers {} {} {} ".format(lease, timer1, timer2))
    return r


def dhcpStartTimer(timer, lease):
    # TCL cmd :: dhcpStartTimer timer lease
    r = t.eval("dhcpStartTimer {} {} ".format(timer, lease))
    return r


def dhcpStopTimers():
    # TCL cmd :: dhcpStopTimers
    r = t.eval("dhcpStopTimers ".format())
    return r


def dhcpStopTimer(timer):
    # TCL cmd :: dhcpStopTimer timer
    r = t.eval("dhcpStopTimer {} ".format(timer))
    return r


def dhcpSetStreamRegion(region):
    # TCL cmd :: dhcpSetStreamRegion region
    r = t.eval("dhcpSetStreamRegion {} ".format(region))
    return r


def dhcpGetStreamRegion():
    # TCL cmd :: dhcpGetStreamRegion
    r = t.eval("dhcpGetStreamRegion ".format())
    return r


def dhcpSetPortList(portList):
    # TCL cmd :: dhcpSetPortList portList
    r = t.eval("dhcpSetPortList {} ".format(portList))
    return r


def dhcpGetPortList():
    # TCL cmd :: dhcpGetPortList
    r = t.eval("dhcpGetPortList ".format())
    return r


def dhcpStop():
    # TCL cmd :: dhcpStop
    r = t.eval("dhcpStop ".format())
    return r


def dhcpStopPort(chassis, card, port, release=False):
    # TCL cmd :: dhcpStopPort chassis card port release {false}
    r = t.eval("dhcpStopPort {} {} {} {} ".format(chassis, card, port, release))
    return r


def dhcpEnableStateMachine(stateList="dhcpClient::stateList", eventList="dhcpClient::eventList", actionList="dhcpClient::actionList"):
    # TCL cmd :: dhcpEnableStateMachine stateList {dhcpClient::stateList} eventList {dhcpClient::eventList} actionList {dhcpClient::actionList}
    r = t.eval("dhcpEnableStateMachine {} {} {} ".format(stateList, eventList, actionList))
    return r


def dhcpDisableStateMachine(stateList="dhcpClient::stateList", eventList="dhcpClient::eventList", actionList=None):
    # TCL cmd :: dhcpDisableStateMachine stateList {dhcpClient::stateList} eventList {dhcpClient::eventList} actionList
    if actionList is None: print "TCL argument `actionList` cannot be empty!"; return False
    r = t.eval("dhcpDisableStateMachine {} {} {} ".format(stateList, eventList, actionList))
    return r


def DHCPdiscoverIP(PortList, startState=0, stateMachine="disable"):
    # TCL cmd :: DHCPdiscoverIP PortList startState {0} stateMachine {disable}
    r = t.eval("DHCPdiscoverIP {} {} {} ".format(PortList, startState, stateMachine))
    return r


def send_DHCP_discover(portList):
    # TCL cmd :: send_DHCP_discover portList
    r = t.eval("send_DHCP_discover {} ".format(portList))
    return r


def get_DHCP_offer(PortList):
    # TCL cmd :: get_DHCP_offer PortList
    r = t.eval("get_DHCP_offer {} ".format(PortList))
    return r


def send_DHCP_request(portList):
    # TCL cmd :: send_DHCP_request portList
    r = t.eval("send_DHCP_request {} ".format(portList))
    return r


def get_DHCP_ack(portList, command):
    # TCL cmd :: get_DHCP_ack portList command
    r = t.eval("get_DHCP_ack {} {} ".format(portList, command))
    return r


def send_DHCP_release(portList):
    # TCL cmd :: send_DHCP_release portList
    r = t.eval("send_DHCP_release {} ".format(portList))
    return r


def setupUDPbootp(chassis, lm, port):
    # TCL cmd :: setupUDPbootp chassis lm port
    r = t.eval("setupUDPbootp {} {} {} ".format(chassis, lm, port))
    return r


def setupDhcpBroadcastIP(chassis, lm, port):
    # TCL cmd :: setupDhcpBroadcastIP chassis lm port
    r = t.eval("setupDhcpBroadcastIP {} {} {} ".format(chassis, lm, port))
    return r


def setupDhcpUnicastIP(chassis, lm, port, sourceIpAddr, destIpAddr):
    # TCL cmd :: setupDhcpUnicastIP chassis lm port sourceIpAddr destIpAddr
    r = t.eval("setupDhcpUnicastIP {} {} {} {} {} ".format(chassis, lm, port, sourceIpAddr, destIpAddr))
    return r


def setupDefaultDhcpParameters(chassis, lm, port, transactionID, txSA, clientIpAddr="0.0.0.0"):
    # TCL cmd :: setupDefaultDhcpParameters chassis lm port transactionID txSA clientIpAddr {0.0.0.0}
    r = t.eval("setupDefaultDhcpParameters {} {} {} {} {} {} ".format(chassis, lm, port, transactionID, txSA, clientIpAddr))
    return r


def setDhcpOptions(OptionList):
    # TCL cmd :: setDhcpOptions OptionList
    r = t.eval("setDhcpOptions {} ".format(OptionList))
    return r


def sendDhcpPacket(portList, opcode):
    # TCL cmd :: sendDhcpPacket portList opcode
    r = t.eval("sendDhcpPacket {} {} ".format(portList, opcode))
    return r


def buildDhcpPacket(chassis, lm, port, opcode):
    # TCL cmd :: buildDhcpPacket chassis lm port opcode
    r = t.eval("buildDhcpPacket {} {} {} {} ".format(chassis, lm, port, opcode))
    return r


def get_DHCP_packet(chassis, lm, port, messageType, wait=0):
    # TCL cmd :: get_DHCP_packet chassis lm port messageType wait {0}
    r = t.eval("get_DHCP_packet {} {} {} {} {} ".format(chassis, lm, port, messageType, wait))
    return r


def createDialog(dialogName, window="textDialog"):
    # TCL cmd :: createDialog dialogName window {textDialog}
    r = t.eval("createDialog {} {} ".format(dialogName, window))
    return r


def writeDialog(dialogText, window="textDialog"):
    # TCL cmd :: writeDialog dialogText window {textDialog}
    r = t.eval("writeDialog {} {} ".format(dialogText, window))
    return r


def destroyDialog(window="textDialog"):
    # TCL cmd :: destroyDialog window {textDialog}
    r = t.eval("destroyDialog {} ".format(window))
    return r


def setStopTestFlag(value):
    # TCL cmd :: setStopTestFlag value
    r = t.eval("setStopTestFlag {} ".format(value))
    return r


def stopTest():
    # TCL cmd :: stopTest
    r = t.eval("stopTest ".format())
    return r


def isTestStopped():
    # TCL cmd :: isTestStopped
    r = t.eval("isTestStopped ".format())
    return r


def informServerCurrentTestStopped():
    # TCL cmd :: informServerCurrentTestStopped
    r = t.eval("informServerCurrentTestStopped ".format())
    return r


def IsPOSPort(c, l, p):
    # TCL cmd :: IsPOSPort c l p
    r = t.eval("IsPOSPort {} {} {} ".format(c, l, p))
    return r


def Is10GigEPort(c, l, p):
    # TCL cmd :: Is10GigEPort c l p
    r = t.eval("Is10GigEPort {} {} {} ".format(c, l, p))
    return r


def IsGigabitPort(c, l, p):
    # TCL cmd :: IsGigabitPort c l p
    r = t.eval("IsGigabitPort {} {} {} ".format(c, l, p))
    return r


def any10100Ports(TxRxArray):
    # TCL cmd :: any10100Ports TxRxArray
    r = t.eval("any10100Ports {} ".format(TxRxArray))
    return r


def anyGigPorts(TxRxArray):
    # TCL cmd :: anyGigPorts TxRxArray
    r = t.eval("anyGigPorts {} ".format(TxRxArray))
    return r


def anyOc48Ports(TxRxArray):
    # TCL cmd :: anyOc48Ports TxRxArray
    r = t.eval("anyOc48Ports {} ".format(TxRxArray))
    return r


def anyOc192Ports(TxRxArray):
    # TCL cmd :: anyOc192Ports TxRxArray
    r = t.eval("anyOc192Ports {} ".format(TxRxArray))
    return r


def anyPortsByInterface(TxRxArray, interface):
    # TCL cmd :: anyPortsByInterface TxRxArray interface
    r = t.eval("anyPortsByInterface {} {} ".format(TxRxArray, interface))
    return r


def anyPortsBySpeed(TxRxArray, speed):
    # TCL cmd :: anyPortsBySpeed TxRxArray speed
    r = t.eval("anyPortsBySpeed {} {} ".format(TxRxArray, speed))
    return r


def supportsProtocolServer(TxRxArray):
    # TCL cmd :: supportsProtocolServer TxRxArray
    r = t.eval("supportsProtocolServer {} ".format(TxRxArray))
    return r


def supportsPortCPU(TxRxArray):
    # TCL cmd :: supportsPortCPU TxRxArray
    r = t.eval("supportsPortCPU {} ".format(TxRxArray))
    return r


def isValidFeature(PortArray, featureList):
    # TCL cmd :: isValidFeature PortArray featureList
    r = t.eval("isValidFeature {} {} ".format(PortArray, featureList))
    return r


def isPacketFlowMode(c, l, p):
    # TCL cmd :: isPacketFlowMode c l p
    r = t.eval("isPacketFlowMode {} {} {} ".format(c, l, p))
    return r


def isAdvancedStreamSchedulerMode(c, l, p):
    # TCL cmd :: isAdvancedStreamSchedulerMode c l p
    r = t.eval("isAdvancedStreamSchedulerMode {} {} {} ".format(c, l, p))
    return r


def ixInitialize(chassisList, cableLen="cable3feet", logfilename=None, client="local"):
    # TCL cmd :: ixInitialize chassisList cableLen {cable3feet} logfilename client {local}
    if logfilename is None: print "TCL argument `logfilename` cannot be empty!"; return False
    r = t.eval("ixInitialize {} {} {} {} ".format(chassisList, cableLen, logfilename, client))
    return r


def ixConnectToChassis(chassisList, cableLength="('cable3feet',)"):
    # TCL cmd :: ixConnectToChassis chassisList cableLength {('cable3feet',)}
    r = t.eval("ixConnectToChassis {} {} ".format(chassisList, cableLength))
    return r


def ixConnectToTclServer(serverName):
    # TCL cmd :: ixConnectToTclServer serverName
    r = t.eval("ixConnectToTclServer {} ".format(serverName))
    return r


def ixDisconnectTclServer(serverName):
    # TCL cmd :: ixDisconnectTclServer serverName
    r = t.eval("ixDisconnectTclServer {} ".format(serverName))
    return r


def ixGetChassisID(chassisName):
    # TCL cmd :: ixGetChassisID chassisName
    r = t.eval("ixGetChassisID {} ".format(chassisName))
    return r


def ixDisconnectFromChassis(args):
    # TCL cmd :: ixDisconnectFromChassis args
    r = t.eval("ixDisconnectFromChassis {} ".format(args))
    return r


def ixGlobalSetDefault():
    # TCL cmd :: ixGlobalSetDefault
    r = t.eval("ixGlobalSetDefault ".format())
    return r


def ixStartTransmit(PortList):
    # TCL cmd :: ixStartTransmit PortList
    r = t.eval("ixStartTransmit {} ".format(PortList))
    return r


def ixStartPortTransmit(chassis, lm, port):
    # TCL cmd :: ixStartPortTransmit chassis lm port
    r = t.eval("ixStartPortTransmit {} {} {} ".format(chassis, lm, port))
    return r


def ixStartStaggeredTransmit(PortList):
    # TCL cmd :: ixStartStaggeredTransmit PortList
    r = t.eval("ixStartStaggeredTransmit {} ".format(PortList))
    return r


def ixStopTransmit(PortList):
    # TCL cmd :: ixStopTransmit PortList
    r = t.eval("ixStopTransmit {} ".format(PortList))
    return r


def ixStopPortTransmit(chassis, lm, port):
    # TCL cmd :: ixStopPortTransmit chassis lm port
    r = t.eval("ixStopPortTransmit {} {} {} ".format(chassis, lm, port))
    return r


def ixStartCapture(PortList):
    # TCL cmd :: ixStartCapture PortList
    r = t.eval("ixStartCapture {} ".format(PortList))
    return r


def ixStartPrbsCapture(PortList):
    # TCL cmd :: ixStartPrbsCapture PortList
    r = t.eval("ixStartPrbsCapture {} ".format(PortList))
    return r


def ixStopCapture(PortList):
    # TCL cmd :: ixStopCapture PortList
    r = t.eval("ixStopCapture {} ".format(PortList))
    return r


def ixStopPrbsCapture(PortList):
    # TCL cmd :: ixStopPrbsCapture PortList
    r = t.eval("ixStopPrbsCapture {} ".format(PortList))
    return r


def ixClearPrbsCapture(PortList):
    # TCL cmd :: ixClearPrbsCapture PortList
    r = t.eval("ixClearPrbsCapture {} ".format(PortList))
    return r


def ixStartPortCapture(chassis, lm, port):
    # TCL cmd :: ixStartPortCapture chassis lm port
    r = t.eval("ixStartPortCapture {} {} {} ".format(chassis, lm, port))
    return r


def ixStartPortPrbsCapture(chassis, lm, port):
    # TCL cmd :: ixStartPortPrbsCapture chassis lm port
    r = t.eval("ixStartPortPrbsCapture {} {} {} ".format(chassis, lm, port))
    return r


def ixStopPortCapture(chassis, lm, port, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: ixStopPortCapture chassis lm port groupId {710} create {create} destroy {destroy}
    r = t.eval("ixStopPortCapture {} {} {} {} {} {} ".format(chassis, lm, port, groupId, create, destroy))
    return r


def ixStopPortPrbsCapture(chassis, lm, port, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: ixStopPortPrbsCapture chassis lm port groupId {710} create {create} destroy {destroy}
    r = t.eval("ixStopPortPrbsCapture {} {} {} {} {} {} ".format(chassis, lm, port, groupId, create, destroy))
    return r


def ixClearPortPrbsCapture(chassis, lm, port, groupId=710, create="create", destroy="destroy"):
    # TCL cmd :: ixClearPortPrbsCapture chassis lm port groupId {710} create {create} destroy {destroy}
    r = t.eval("ixClearPortPrbsCapture {} {} {} {} {} {} ".format(chassis, lm, port, groupId, create, destroy))
    return r


def ixClearStats(PortList):
    # TCL cmd :: ixClearStats PortList
    r = t.eval("ixClearStats {} ".format(PortList))
    return r


def ixClearPortStats(chassis, lm, port):
    # TCL cmd :: ixClearPortStats chassis lm port
    r = t.eval("ixClearPortStats {} {} {} ".format(chassis, lm, port))
    return r


def ixClearPerStreamTxStats(PortList):
    # TCL cmd :: ixClearPerStreamTxStats PortList
    r = t.eval("ixClearPerStreamTxStats {} ".format(PortList))
    return r


def ixClearPerStreamTxPortStats(chassis, lm, port):
    # TCL cmd :: ixClearPerStreamTxPortStats chassis lm port
    r = t.eval("ixClearPerStreamTxPortStats {} {} {} ".format(chassis, lm, port))
    return r


def ixRequestStats(TxRxArray):
    # TCL cmd :: ixRequestStats TxRxArray
    r = t.eval("ixRequestStats {} ".format(TxRxArray))
    return r


def ixClearTimeStamp(PortList):
    # TCL cmd :: ixClearTimeStamp PortList
    r = t.eval("ixClearTimeStamp {} ".format(PortList))
    return r


def ixStartPacketGroups(PortList):
    # TCL cmd :: ixStartPacketGroups PortList
    r = t.eval("ixStartPacketGroups {} ".format(PortList))
    return r


def ixStartPortPacketGroups(chassis, lm, port):
    # TCL cmd :: ixStartPortPacketGroups chassis lm port
    r = t.eval("ixStartPortPacketGroups {} {} {} ".format(chassis, lm, port))
    return r


def ixStopPacketGroups(PortList):
    # TCL cmd :: ixStopPacketGroups PortList
    r = t.eval("ixStopPacketGroups {} ".format(PortList))
    return r


def ixClearPacketGroups(PortList):
    # TCL cmd :: ixClearPacketGroups PortList
    r = t.eval("ixClearPacketGroups {} ".format(PortList))
    return r


def ixClearPortPacketGroups(chassis, lm, port):
    # TCL cmd :: ixClearPortPacketGroups chassis lm port
    r = t.eval("ixClearPortPacketGroups {} {} {} ".format(chassis, lm, port))
    return r


def ixSetScheduledTransmitTime(PortList, duration):
    # TCL cmd :: ixSetScheduledTransmitTime PortList duration
    r = t.eval("ixSetScheduledTransmitTime {} {} ".format(PortList, duration))
    return r


def ixClearScheduledTransmitTime(PortList):
    # TCL cmd :: ixClearScheduledTransmitTime PortList
    r = t.eval("ixClearScheduledTransmitTime {} ".format(PortList))
    return r


def ixStopPortPacketGroups(chassis, lm, port):
    # TCL cmd :: ixStopPortPacketGroups chassis lm port
    r = t.eval("ixStopPortPacketGroups {} {} {} ".format(chassis, lm, port))
    return r


def ixStartCollisions(PortList):
    # TCL cmd :: ixStartCollisions PortList
    r = t.eval("ixStartCollisions {} ".format(PortList))
    return r


def ixStartPortCollisions(chassis, lm, port):
    # TCL cmd :: ixStartPortCollisions chassis lm port
    r = t.eval("ixStartPortCollisions {} {} {} ".format(chassis, lm, port))
    return r


def ixStopCollisions(PortList):
    # TCL cmd :: ixStopCollisions PortList
    r = t.eval("ixStopCollisions {} ".format(PortList))
    return r


def ixStopPortCollisions(chassis, lm, port):
    # TCL cmd :: ixStopPortCollisions chassis lm port
    r = t.eval("ixStopPortCollisions {} {} {} ".format(chassis, lm, port))
    return r


def ixLoadPoePulse(PortList):
    # TCL cmd :: ixLoadPoePulse PortList
    r = t.eval("ixLoadPoePulse {} ".format(PortList))
    return r


def ixLoadPortPoePulse(chassis, lm, port):
    # TCL cmd :: ixLoadPortPoePulse chassis lm port
    r = t.eval("ixLoadPortPoePulse {} {} {} ".format(chassis, lm, port))
    return r


def ixArmPoeTrigger(PortList):
    # TCL cmd :: ixArmPoeTrigger PortList
    r = t.eval("ixArmPoeTrigger {} ".format(PortList))
    return r


def ixArmPortPoeTrigger(chassis, lm, port):
    # TCL cmd :: ixArmPortPoeTrigger chassis lm port
    r = t.eval("ixArmPortPoeTrigger {} {} {} ".format(chassis, lm, port))
    return r


def ixAbortPoeArm(PortList):
    # TCL cmd :: ixAbortPoeArm PortList
    r = t.eval("ixAbortPoeArm {} ".format(PortList))
    return r


def ixAbortPortPoeArm(chassis, lm, port):
    # TCL cmd :: ixAbortPortPoeArm chassis lm port
    r = t.eval("ixAbortPortPoeArm {} {} {} ".format(chassis, lm, port))
    return r


def ixStartAtmOamTransmit(PortList):
    # TCL cmd :: ixStartAtmOamTransmit PortList
    r = t.eval("ixStartAtmOamTransmit {} ".format(PortList))
    return r


def ixStartPortAtmOamTransmit(chassis, lm, port):
    # TCL cmd :: ixStartPortAtmOamTransmit chassis lm port
    r = t.eval("ixStartPortAtmOamTransmit {} {} {} ".format(chassis, lm, port))
    return r


def ixStopAtmOamTransmit(PortList):
    # TCL cmd :: ixStopAtmOamTransmit PortList
    r = t.eval("ixStopAtmOamTransmit {} ".format(PortList))
    return r


def ixStopPortAtmOamTransmit(chassis, lm, port):
    # TCL cmd :: ixStopPortAtmOamTransmit chassis lm port
    r = t.eval("ixStopPortAtmOamTransmit {} {} {} ".format(chassis, lm, port))
    return r


def ixCreatePortListWildCard(portList, excludePorts):
    # TCL cmd :: ixCreatePortListWildCard portList excludePorts
    r = t.eval("ixCreatePortListWildCard {} {} ".format(portList, excludePorts))
    return r


def ixCreateSortedPortList(portListFrom, portListTo, excludePortList):
    # TCL cmd :: ixCreateSortedPortList portListFrom portListTo excludePortList
    r = t.eval("ixCreateSortedPortList {} {} {} ".format(portListFrom, portListTo, excludePortList))
    return r


def ixPuts(args):
    # TCL cmd :: ixPuts args
    r = t.eval("ixPuts {} ".format(args))
    return r


def ixiaPortSetParms(chassis, card, port, parm, value):
    # TCL cmd :: ixiaPortSetParms chassis card port parm value
    r = t.eval("ixiaPortSetParms {} {} {} {} {} ".format(chassis, card, port, parm, value))
    return r


def ixiaReadWriteMII(ports, action, register, code):
    # TCL cmd :: ixiaReadWriteMII ports action register code
    r = t.eval("ixiaReadWriteMII {} {} {} {} ".format(ports, action, register, code))
    return r


def ixTclSvrConnect(serverName):
    # TCL cmd :: ixTclSvrConnect serverName
    r = t.eval("ixTclSvrConnect {} ".format(serverName))
    return r


def ixTclSvrDisconnect():
    # TCL cmd :: ixTclSvrDisconnect
    r = t.eval("ixTclSvrDisconnect ".format())
    return r


def ixEnableArpResponse(mapType, PortMap):
    # TCL cmd :: ixEnableArpResponse mapType PortMap
    r = t.eval("ixEnableArpResponse {} {} ".format(mapType, PortMap))
    return r


def ixEnablePortArpResponse(mapType, chassis, lm, port, write="write"):
    # TCL cmd :: ixEnablePortArpResponse mapType chassis lm port write {write}
    r = t.eval("ixEnablePortArpResponse {} {} {} {} {} ".format(mapType, chassis, lm, port, write))
    return r


def ixDisableArpResponse(PortMap):
    # TCL cmd :: ixDisableArpResponse PortMap
    r = t.eval("ixDisableArpResponse {} ".format(PortMap))
    return r


def ixTransmitArpRequest(TxRxArray):
    # TCL cmd :: ixTransmitArpRequest TxRxArray
    r = t.eval("ixTransmitArpRequest {} ".format(TxRxArray))
    return r


def ixClearArpTable(TxRxArray):
    # TCL cmd :: ixClearArpTable TxRxArray
    r = t.eval("ixClearArpTable {} ".format(TxRxArray))
    return r


def ixDisablePortArpResponse(chassis, lm, port, write="write"):
    # TCL cmd :: ixDisablePortArpResponse chassis lm port write {write}
    r = t.eval("ixDisablePortArpResponse {} {} {} {} ".format(chassis, lm, port, write))
    return r


def ixTransmitPortArpRequest(chassis, lm, port):
    # TCL cmd :: ixTransmitPortArpRequest chassis lm port
    r = t.eval("ixTransmitPortArpRequest {} {} {} ".format(chassis, lm, port))
    return r


def ixClearPortArpTable(chassis, lm, port):
    # TCL cmd :: ixClearPortArpTable chassis lm port
    r = t.eval("ixClearPortArpTable {} {} {} ".format(chassis, lm, port))
    return r


def ixSetPacketGroupMode(TxRxArray, write="nowrite"):
    # TCL cmd :: ixSetPacketGroupMode TxRxArray write {nowrite}
    r = t.eval("ixSetPacketGroupMode {} {} ".format(TxRxArray, write))
    return r


def ixSetPortPacketGroupMode(chassis, lm, port, write="nowrite"):
    # TCL cmd :: ixSetPortPacketGroupMode chassis lm port write {nowrite}
    r = t.eval("ixSetPortPacketGroupMode {} {} {} {} ".format(chassis, lm, port, write))
    return r


def ixSetAutoDetectInstrumentationMode(TxRxArray, write="nowrite"):
    # TCL cmd :: ixSetAutoDetectInstrumentationMode TxRxArray write {nowrite}
    r = t.eval("ixSetAutoDetectInstrumentationMode {} {} ".format(TxRxArray, write))
    return r


def ixSetPortAutoDetectInstrumentationMode(chassis, lm, port, write="nowrite"):
    # TCL cmd :: ixSetPortAutoDetectInstrumentationMode chassis lm port write {nowrite}
    r = t.eval("ixSetPortAutoDetectInstrumentationMode {} {} {} {} ".format(chassis, lm, port, write))
    return r


def ixSetWidePacketGroupMode(TxRxArray, write="nowrite"):
    # TCL cmd :: ixSetWidePacketGroupMode TxRxArray write {nowrite}
    r = t.eval("ixSetWidePacketGroupMode {} {} ".format(TxRxArray, write))
    return r


def ixSetPortWidePacketGroupMode(chassis, lm, port, write="nowrite"):
    # TCL cmd :: ixSetPortWidePacketGroupMode chassis lm port write {nowrite}
    r = t.eval("ixSetPortWidePacketGroupMode {} {} {} {} ".format(chassis, lm, port, write))
    return r


def ixSetCaptureMode(TxRxArray, write="nowrite"):
    # TCL cmd :: ixSetCaptureMode TxRxArray write {nowrite}
    r = t.eval("ixSetCaptureMode {} {} ".format(TxRxArray, write))
    return r


def ixSetPortCaptureMode(chassis, lm, port, write="nowrite"):
    # TCL cmd :: ixSetPortCaptureMode chassis lm port write {nowrite}
    r = t.eval("ixSetPortCaptureMode {} {} {} {} ".format(chassis, lm, port, write))
    return r


def ixSetTcpRoundTripFlowMode(TxRxArray, write="nowrite"):
    # TCL cmd :: ixSetTcpRoundTripFlowMode TxRxArray write {nowrite}
    r = t.eval("ixSetTcpRoundTripFlowMode {} {} ".format(TxRxArray, write))
    return r


def ixSetPortTcpRoundTripFlowMode(c, l, p, write="nowrite"):
    # TCL cmd :: ixSetPortTcpRoundTripFlowMode c l p write {nowrite}
    r = t.eval("ixSetPortTcpRoundTripFlowMode {} {} {} {} ".format(c, l, p, write))
    return r


def ixSetDataIntegrityMode(TxRxArray, write="nowrite"):
    # TCL cmd :: ixSetDataIntegrityMode TxRxArray write {nowrite}
    r = t.eval("ixSetDataIntegrityMode {} {} ".format(TxRxArray, write))
    return r


def ixSetPortDataIntegrityMode(c, l, p, write="nowrite"):
    # TCL cmd :: ixSetPortDataIntegrityMode c l p write {nowrite}
    r = t.eval("ixSetPortDataIntegrityMode {} {} {} {} ".format(c, l, p, write))
    return r


def ixSetPrbsMode(TxRxArray, write="nowrite"):
    # TCL cmd :: ixSetPrbsMode TxRxArray write {nowrite}
    r = t.eval("ixSetPrbsMode {} {} ".format(TxRxArray, write))
    return r


def ixSetPortPrbsMode(c, l, p, write="nowrite"):
    # TCL cmd :: ixSetPortPrbsMode c l p write {nowrite}
    r = t.eval("ixSetPortPrbsMode {} {} {} {} ".format(c, l, p, write))
    return r


def ixSetSequenceCheckingMode(TxRxArray, write="nowrite"):
    # TCL cmd :: ixSetSequenceCheckingMode TxRxArray write {nowrite}
    r = t.eval("ixSetSequenceCheckingMode {} {} ".format(TxRxArray, write))
    return r


def ixSetPortSequenceCheckingMode(c, l, p, write="nowrite"):
    # TCL cmd :: ixSetPortSequenceCheckingMode c l p write {nowrite}
    r = t.eval("ixSetPortSequenceCheckingMode {} {} {} {} ".format(c, l, p, write))
    return r


def ixSetPacketFlowMode(TxRxArray, write="nowrite"):
    # TCL cmd :: ixSetPacketFlowMode TxRxArray write {nowrite}
    r = t.eval("ixSetPacketFlowMode {} {} ".format(TxRxArray, write))
    return r


def ixSetPortPacketFlowMode(c, l, p, write="nowrite"):
    # TCL cmd :: ixSetPortPacketFlowMode c l p write {nowrite}
    r = t.eval("ixSetPortPacketFlowMode {} {} {} {} ".format(c, l, p, write))
    return r


def ixSetPacketStreamMode(TxRxArray, write="nowrite"):
    # TCL cmd :: ixSetPacketStreamMode TxRxArray write {nowrite}
    r = t.eval("ixSetPacketStreamMode {} {} ".format(TxRxArray, write))
    return r


def ixSetPortPacketStreamMode(chassis, lm, port, write="nowrite"):
    # TCL cmd :: ixSetPortPacketStreamMode chassis lm port write {nowrite}
    r = t.eval("ixSetPortPacketStreamMode {} {} {} {} ".format(chassis, lm, port, write))
    return r


def ixSetAdvancedStreamSchedulerMode(TxRxArray, write="nowrite"):
    # TCL cmd :: ixSetAdvancedStreamSchedulerMode TxRxArray write {nowrite}
    r = t.eval("ixSetAdvancedStreamSchedulerMode {} {} ".format(TxRxArray, write))
    return r


def ixSetPortAdvancedStreamSchedulerMode(c, l, p, write="nowrite"):
    # TCL cmd :: ixSetPortAdvancedStreamSchedulerMode c l p write {nowrite}
    r = t.eval("ixSetPortAdvancedStreamSchedulerMode {} {} {} {} ".format(c, l, p, write))
    return r


def ixWritePortsToHardware(PortArray, args):
    # TCL cmd :: ixWritePortsToHardware PortArray args
    r = t.eval("ixWritePortsToHardware {} {} ".format(PortArray, args))
    return r


def ixWriteConfigToHardware(PortArray, args):
    # TCL cmd :: ixWriteConfigToHardware PortArray args
    r = t.eval("ixWriteConfigToHardware {} {} ".format(PortArray, args))
    return r


def ixCheckTransmitDone(PortArray):
    # TCL cmd :: ixCheckTransmitDone PortArray
    r = t.eval("ixCheckTransmitDone {} ".format(PortArray))
    return r


def ixCheckPortTransmitDone(chassis, lm, port):
    # TCL cmd :: ixCheckPortTransmitDone chassis lm port
    r = t.eval("ixCheckPortTransmitDone {} {} {} ".format(chassis, lm, port))
    return r


def ixCheckLinkState(PortArray, message="messageOn"):
    # TCL cmd :: ixCheckLinkState PortArray message {messageOn}
    r = t.eval("ixCheckLinkState {} {} ".format(PortArray, message))
    return r


def ixCheckPPPState(PortArray, message="messageOn"):
    # TCL cmd :: ixCheckPPPState PortArray message {messageOn}
    r = t.eval("ixCheckPPPState {} {} ".format(PortArray, message))
    return r


def ixCollectStats(rxList, statName, RxNumFrames, TotalRxFrames):
    # TCL cmd :: ixCollectStats rxList statName RxNumFrames TotalRxFrames
    r = t.eval("ixCollectStats {} {} {} {} ".format(rxList, statName, RxNumFrames, TotalRxFrames))
    return r


def ixProxyConnect(tclServer, chassisList, cableLen="cable3feet", logFilename=None):
    # TCL cmd :: ixProxyConnect tclServer chassisList cableLen {cable3feet} logFilename
    if logFilename is None: print "TCL argument `logFilename` cannot be empty!"; return False
    r = t.eval("ixProxyConnect {} {} {} {} ".format(tclServer, chassisList, cableLen, logFilename))
    return r


def ixResetSequenceIndex(PortArray):
    # TCL cmd :: ixResetSequenceIndex PortArray
    r = t.eval("ixResetSequenceIndex {} ".format(PortArray))
    return r


def ixResetPortSequenceIndex(chassis, lm, port):
    # TCL cmd :: ixResetPortSequenceIndex chassis lm port
    r = t.eval("ixResetPortSequenceIndex {} {} {} ".format(chassis, lm, port))
    return r


def ixRestartAutoNegotiation(TxRxArray):
    # TCL cmd :: ixRestartAutoNegotiation TxRxArray
    r = t.eval("ixRestartAutoNegotiation {} ".format(TxRxArray))
    return r


def ixRestartPortAutoNegotiation(chassis, lm, port):
    # TCL cmd :: ixRestartPortAutoNegotiation chassis lm port
    r = t.eval("ixRestartPortAutoNegotiation {} {} {} ".format(chassis, lm, port))
    return r


def ixRestartPPPNegotiation(TxRxArray):
    # TCL cmd :: ixRestartPPPNegotiation TxRxArray
    r = t.eval("ixRestartPPPNegotiation {} ".format(TxRxArray))
    return r


def ixRestartPortPPPNegotiation(chassis, lm, port):
    # TCL cmd :: ixRestartPortPPPNegotiation chassis lm port
    r = t.eval("ixRestartPortPPPNegotiation {} {} {} ".format(chassis, lm, port))
    return r


def ixSimulatePhysicalInterfaceUp(TxRxArray):
    # TCL cmd :: ixSimulatePhysicalInterfaceUp TxRxArray
    r = t.eval("ixSimulatePhysicalInterfaceUp {} ".format(TxRxArray))
    return r


def ixSimulatePortPhysicalInterfaceUp(chassis, lm, port):
    # TCL cmd :: ixSimulatePortPhysicalInterfaceUp chassis lm port
    r = t.eval("ixSimulatePortPhysicalInterfaceUp {} {} {} ".format(chassis, lm, port))
    return r


def ixSimulatePhysicalInterfaceDown(TxRxArray):
    # TCL cmd :: ixSimulatePhysicalInterfaceDown TxRxArray
    r = t.eval("ixSimulatePhysicalInterfaceDown {} ".format(TxRxArray))
    return r


def ixSimulatePortPhysicalInterfaceDown(chassis, lm, port):
    # TCL cmd :: ixSimulatePortPhysicalInterfaceDown chassis lm port
    r = t.eval("ixSimulatePortPhysicalInterfaceDown {} {} {} ".format(chassis, lm, port))
    return r


def ixIsOverlappingIpAddress(ipAddress1, count1, ipAddress2, count2):
    # TCL cmd :: ixIsOverlappingIpAddress ipAddress1 count1 ipAddress2 count2
    r = t.eval("ixIsOverlappingIpAddress {} {} {} {} ".format(ipAddress1, count1, ipAddress2, count2))
    return r


def ixIsSameSubnet(ipAddr1, mask1, ipAddr2, mask2):
    # TCL cmd :: ixIsSameSubnet ipAddr1 mask1 ipAddr2 mask2
    r = t.eval("ixIsSameSubnet {} {} {} {} ".format(ipAddr1, mask1, ipAddr2, mask2))
    return r


def ixIsValidHost(ipAddr, mask):
    # TCL cmd :: ixIsValidHost ipAddr mask
    r = t.eval("ixIsValidHost {} {} ".format(ipAddr, mask))
    return r


def ixIsValidNetMask(mask):
    # TCL cmd :: ixIsValidNetMask mask
    r = t.eval("ixIsValidNetMask {} ".format(mask))
    return r


def ixIsValidUnicastIp(ipAddr):
    # TCL cmd :: ixIsValidUnicastIp ipAddr
    r = t.eval("ixIsValidUnicastIp {} ".format(ipAddr))
    return r


def ixConvertFromSeconds(time, Hours, Minutes, Seconds):
    # TCL cmd :: ixConvertFromSeconds time Hours Minutes Seconds
    r = t.eval("ixConvertFromSeconds {} {} {} {} ".format(time, Hours, Minutes, Seconds))
    return r


def ixConvertToSeconds(hours, minutes, seconds):
    # TCL cmd :: ixConvertToSeconds hours minutes seconds
    r = t.eval("ixConvertToSeconds {} {} {} ".format(hours, minutes, seconds))
    return r


def ixEnablePortIntrinsicLatencyAdjustment(chassId, cardId, portId, enable, write="nowrite"):
    # TCL cmd :: ixEnablePortIntrinsicLatencyAdjustment chassId cardId portId enable write {nowrite}
    r = t.eval("ixEnablePortIntrinsicLatencyAdjustment {} {} {} {} {} ".format(chassId, cardId, portId, enable, write))
    return r


def ixEnableIntrinsicLatencyAdjustment(TxRxArray, enable, write="nowrite"):
    # TCL cmd :: ixEnableIntrinsicLatencyAdjustment TxRxArray enable write {nowrite}
    r = t.eval("ixEnableIntrinsicLatencyAdjustment {} {} {} ".format(TxRxArray, enable, write))
    return r


def ixIsIntrinsicLatencyAdjustmentEnabled(chassId, cardId, portId):
    # TCL cmd :: ixIsIntrinsicLatencyAdjustmentEnabled chassId cardId portId
    r = t.eval("ixIsIntrinsicLatencyAdjustmentEnabled {} {} {} ".format(chassId, cardId, portId))
    return r


def initCommand_zz_advancedTestParameter():
    # TCL cmd :: initCommand_zz_advancedTestParameter
    r = t.eval("initCommand_zz_advancedTestParameter ".format())
    return r


def initCommand_zz_fastpath():
    # TCL cmd :: initCommand_zz_fastpath
    r = t.eval("initCommand_zz_fastpath ".format())
    return r


def initCommand_zz_ipfastpath():
    # TCL cmd :: initCommand_zz_ipfastpath
    r = t.eval("initCommand_zz_ipfastpath ".format())
    return r


def initCommand_zz_learn():
    # TCL cmd :: initCommand_zz_learn
    r = t.eval("initCommand_zz_learn ".format())
    return r


def initCommand_zz_logger():
    # TCL cmd :: initCommand_zz_logger
    r = t.eval("initCommand_zz_logger ".format())
    return r


def initCommand_zz_map():
    # TCL cmd :: initCommand_zz_map
    r = t.eval("initCommand_zz_map ".format())
    return r


def initCommand_zz_tclClient():
    # TCL cmd :: initCommand_zz_tclClient
    r = t.eval("initCommand_zz_tclClient ".format())
    return r


def initCommand_zz_testProfile():
    # TCL cmd :: initCommand_zz_testProfile
    r = t.eval("initCommand_zz_testProfile ".format())
    return r


def ixCollectAndSendLogs(args):
    # TCL cmd :: ixCollectAndSendLogs args
    r = t.eval("ixCollectAndSendLogs {} ".format(args))
    return r


def showmaps():
    # TCL cmd :: showmaps
    r = t.eval("showmaps ".format())
    return r


def ixMiiConfigPreEmphasis(chassis, card, port, peSetting):
    # TCL cmd :: ixMiiConfigPreEmphasis chassis card port peSetting
    r = t.eval("ixMiiConfigPreEmphasis {} {} {} {} ".format(chassis, card, port, peSetting))
    return r


def ixMiiConfigLossOfSignalThreshold(chassis, card, port, threshold):
    # TCL cmd :: ixMiiConfigLossOfSignalThreshold chassis card port threshold
    r = t.eval("ixMiiConfigLossOfSignalThreshold {} {} {} {} ".format(chassis, card, port, threshold))
    return r


def ixMiiConfigXgxsLinkMonitoring(chassis, card, port, enable):
    # TCL cmd :: ixMiiConfigXgxsLinkMonitoring chassis card port enable
    r = t.eval("ixMiiConfigXgxsLinkMonitoring {} {} {} {} ".format(chassis, card, port, enable))
    return r


def ixMiiConfigAlignRxDataClock(chassis, card, port, clock):
    # TCL cmd :: ixMiiConfigAlignRxDataClock chassis card port clock
    r = t.eval("ixMiiConfigAlignRxDataClock {} {} {} {} ".format(chassis, card, port, clock))
    return r


def ixMiiConfigReceiveEqualization(chassis, card, port, value):
    # TCL cmd :: ixMiiConfigReceiveEqualization chassis card port value
    r = t.eval("ixMiiConfigReceiveEqualization {} {} {} {} ".format(chassis, card, port, value))
    return r


def ixMiiConfigXauiOutput(chassis, card, port, enable):
    # TCL cmd :: ixMiiConfigXauiOutput chassis card port enable
    r = t.eval("ixMiiConfigXauiOutput {} {} {} {} ".format(chassis, card, port, enable))
    return r


def ixMiiConfigXauiSerialLoopback(chassis, card, port, enable):
    # TCL cmd :: ixMiiConfigXauiSerialLoopback chassis card port enable
    r = t.eval("ixMiiConfigXauiSerialLoopback {} {} {} {} ".format(chassis, card, port, enable))
    return r


def ixMiiConfigXgmiiParallelLoopback(chassis, card, port, enable):
    # TCL cmd :: ixMiiConfigXgmiiParallelLoopback chassis card port enable
    r = t.eval("ixMiiConfigXgmiiParallelLoopback {} {} {} {} ".format(chassis, card, port, enable))
    return r


def logOn(ix_file):
    # TCL cmd :: logOn file
    r = t.eval("logOn {} ".format(ix_file))
    return r


def logOff():
    # TCL cmd :: logOff
    r = t.eval("logOff ".format())
    return r


def logMsg(args):
    # TCL cmd :: logMsg args
    r = t.eval("logMsg {} ".format(args))
    return r


def errorMsg(args):
    # TCL cmd :: errorMsg args
    r = t.eval("errorMsg {} ".format(args))
    return r


def debugOn(ix_file):
    # TCL cmd :: debugOn file
    r = t.eval("debugOn {} ".format(ix_file))
    return r


def debugOff():
    # TCL cmd :: debugOff
    r = t.eval("debugOff ".format())
    return r


def debugMsg(args):
    # TCL cmd :: debugMsg args
    r = t.eval("debugMsg {} ".format(args))
    return r


def showCmd(cmd, method="cget"):
    # TCL cmd :: showCmd cmd method {cget}
    r = t.eval("showCmd {} {} ".format(cmd, method))
    return r


def openMyFile(filename, fileAccess="w", command="logger"):
    # TCL cmd :: openMyFile filename fileAccess {w} command {logger}
    r = t.eval("openMyFile {} {} {} ".format(filename, fileAccess, command))
    return r


def closeMyFile(fileId):
    # TCL cmd :: closeMyFile fileId
    r = t.eval("closeMyFile {} ".format(fileId))
    return r


def callTraceMsg(arg):
    # TCL cmd :: callTraceMsg arg
    r = t.eval("callTraceMsg {} ".format(arg))
    return r


def traceVariableMsg(name1, name2, op):
    # TCL cmd :: traceVariableMsg name1 name2 op
    r = t.eval("traceVariableMsg {} {} {} ".format(name1, name2, op))
    return r


def isDigit(arg):
    # TCL cmd :: isDigit arg
    r = t.eval("isDigit {} ".format(arg))
    return r


def isNegative(arg):
    # TCL cmd :: isNegative arg
    r = t.eval("isNegative {} ".format(arg))
    return r


def isValidExponentialFloat(valueToCheck):
    # TCL cmd :: isValidExponentialFloat valueToCheck
    r = t.eval("isValidExponentialFloat {} ".format(valueToCheck))
    return r


def isValidPositiveExponentialFloat(valueToCheck):
    # TCL cmd :: isValidPositiveExponentialFloat valueToCheck
    r = t.eval("isValidPositiveExponentialFloat {} ".format(valueToCheck))
    return r


def isValidPartialFloat(valueToCheck):
    # TCL cmd :: isValidPartialFloat valueToCheck
    r = t.eval("isValidPartialFloat {} ".format(valueToCheck))
    return r


def isValidPositivePartialFloat(valueToCheck):
    # TCL cmd :: isValidPositivePartialFloat valueToCheck
    r = t.eval("isValidPositivePartialFloat {} ".format(valueToCheck))
    return r


def isValidPositiveFloat(valueToCheck):
    # TCL cmd :: isValidPositiveFloat valueToCheck
    r = t.eval("isValidPositiveFloat {} ".format(valueToCheck))
    return r


def isValidInteger(valueToCheck):
    # TCL cmd :: isValidInteger valueToCheck
    r = t.eval("isValidInteger {} ".format(valueToCheck))
    return r


def isValidPositiveInteger(valueToCheck):
    # TCL cmd :: isValidPositiveInteger valueToCheck
    r = t.eval("isValidPositiveInteger {} ".format(valueToCheck))
    return r


def getProcList(fileName, sortOn="procName", ProcList=None, verbose="verbose"):
    # TCL cmd :: getProcList fileName sortOn {procName} ProcList verbose {verbose}
    if ProcList is None: print "TCL argument `ProcList` cannot be empty!"; return False
    r = t.eval("getProcList {} {} {} {} ".format(fileName, sortOn, ProcList, verbose))
    return r


def getTxBasedOnRx(TxRxArray, c, l, p):
    # TCL cmd :: getTxBasedOnRx TxRxArray c l p
    r = t.eval("getTxBasedOnRx {} {} {} {} ".format(TxRxArray, c, l, p))
    return r


def convertFromSeconds(time, Hours, Minutes, Seconds):
    # TCL cmd :: convertFromSeconds time Hours Minutes Seconds
    r = t.eval("convertFromSeconds {} {} {} {} ".format(time, Hours, Minutes, Seconds))
    return r


def convertToSeconds(hours, minutes, seconds):
    # TCL cmd :: convertToSeconds hours minutes seconds
    r = t.eval("convertToSeconds {} {} {} ".format(hours, minutes, seconds))
    return r


def formatDurationTime(duration):
    # TCL cmd :: formatDurationTime duration
    r = t.eval("formatDurationTime {} ".format(duration))
    return r


def formatNumber(number, formatTemplete):
    # TCL cmd :: formatNumber number formatTemplete
    r = t.eval("formatNumber {} {} ".format(number, formatTemplete))
    return r


def unixCludgeGetExpr():
    # TCL cmd :: unixCludgeGetExpr
    r = t.eval("unixCludgeGetExpr ".format())
    return r


def useProfile(use):
    # TCL cmd :: useProfile use
    r = t.eval("useProfile {} ".format(use))
    return r


def CountGlobalMemory(memory):
    # TCL cmd :: CountGlobalMemory memory
    r = t.eval("CountGlobalMemory {} ".format(memory))
    return r


def createNamedFont(name, family, size):
    # TCL cmd :: createNamedFont name family size
    r = t.eval("createNamedFont {} {} {} ".format(name, family, size))
    return r


def buildFileName(fileName, type):
    # TCL cmd :: buildFileName fileName type
    r = t.eval("buildFileName {} {} ".format(fileName, type))
    return r


def ixSource(dirFileName):
    # TCL cmd :: ixSource dirFileName
    r = t.eval("ixSource {} ".format(dirFileName))
    return r


def sourceRecursively(dirName):
    # TCL cmd :: sourceRecursively dirName
    r = t.eval("sourceRecursively {} ".format(dirName))
    return r


def ixLogin(userName):
    # TCL cmd :: ixLogin userName
    r = t.eval("ixLogin {} ".format(userName))
    return r


def ixLogout():
    # TCL cmd :: ixLogout
    r = t.eval("ixLogout ".format())
    return r


def ixTakeOwnership(txRxList, takeType):
    # TCL cmd :: ixTakeOwnership txRxList takeType
    r = t.eval("ixTakeOwnership {} {} ".format(txRxList, takeType))
    return r


def ixPortTakeOwnership(chassis, lm, port, takeType):
    # TCL cmd :: ixPortTakeOwnership chassis lm port takeType
    r = t.eval("ixPortTakeOwnership {} {} {} {} ".format(chassis, lm, port, takeType))
    return r


def ixClearOwnership(txRxList, takeType):
    # TCL cmd :: ixClearOwnership txRxList takeType
    r = t.eval("ixClearOwnership {} {} ".format(txRxList, takeType))
    return r


def ixPortClearOwnership(chassis, lm, port, takeType):
    # TCL cmd :: ixPortClearOwnership chassis lm port takeType
    r = t.eval("ixPortClearOwnership {} {} {} {} ".format(chassis, lm, port, takeType))
    return r


def ixCheckOwnership(txRxList):
    # TCL cmd :: ixCheckOwnership txRxList
    r = t.eval("ixCheckOwnership {} ".format(txRxList))
    return r


def canUse(c, l, p):
    # TCL cmd :: canUse c l p
    r = t.eval("canUse {} {} {} ".format(c, l, p))
    return r


def isMine(chassis, card, port):
    # TCL cmd :: isMine chassis card port
    r = t.eval("isMine {} {} {} ".format(chassis, card, port))
    return r


def calculateChecksum(data):
    # TCL cmd :: calculateChecksum data
    r = t.eval("calculateChecksum {} ".format(data))
    return r


def oid2octet(oid):
    # TCL cmd :: oid2octet oid
    r = t.eval("oid2octet {} ".format(oid))
    return r


def buildLLCHeader():
    # TCL cmd :: buildLLCHeader
    r = t.eval("buildLLCHeader ".format())
    return r


def buildIpHeader(sourceIP, destinationIP, dataLength, TOS, TTL, protocol, flags, options):
    # TCL cmd :: buildIpHeader sourceIP destinationIP dataLength TOS TTL protocol flags options
    r = t.eval("buildIpHeader {} {} {} {} {} {} {} {} ".format(sourceIP, destinationIP, dataLength, TOS, TTL, protocol, flags, options))
    return r


def buildRipBlock(ipAddress, Metric, familyId="00 02"):
    # TCL cmd :: buildRipBlock ipAddress Metric familyId {00 02}
    r = t.eval("buildRipBlock {} {} {} ".format(ipAddress, Metric, familyId))
    return r


def buildVidHeader(userPriority, CFIformat, VID):
    # TCL cmd :: buildVidHeader userPriority CFIformat VID
    r = t.eval("buildVidHeader {} {} {} ".format(userPriority, CFIformat, VID))
    return r


def buildIPXPacket(packetType, destNetwork, destNode, destSocket, sourceNetwork, sourceNode, sourceSocket, dataLength, data):
    # TCL cmd :: buildIPXPacket packetType destNetwork destNode destSocket sourceNetwork sourceNode sourceSocket dataLength data
    r = t.eval("buildIPXPacket {} {} {} {} {} {} {} {} {} ".format(packetType, destNetwork, destNode, destSocket, sourceNetwork, sourceNode, sourceSocket, dataLength, data))
    return r


def buildIPXData(frameSize):
    # TCL cmd :: buildIPXData frameSize
    r = t.eval("buildIPXData {} ".format(frameSize))
    return r


def buildServerEntry(operation, serviceType, serverName, netAddress, nodeAddress, socketNum, hops):
    # TCL cmd :: buildServerEntry operation serviceType serverName netAddress nodeAddress socketNum hops
    r = t.eval("buildServerEntry {} {} {} {} {} {} {} ".format(operation, serviceType, serverName, netAddress, nodeAddress, socketNum, hops))
    return r


def buildSapPacket(operation, serviceType, serverName, netAddress, nodeAddress, socketNum, hops):
    # TCL cmd :: buildSapPacket operation serviceType serverName netAddress nodeAddress socketNum hops
    r = t.eval("buildSapPacket {} {} {} {} {} {} {} ".format(operation, serviceType, serverName, netAddress, nodeAddress, socketNum, hops))
    return r


def buildNetworkEntry(networkNumber, hops, ticks):
    # TCL cmd :: buildNetworkEntry networkNumber hops ticks
    r = t.eval("buildNetworkEntry {} {} {} ".format(networkNumber, hops, ticks))
    return r


def buildRipxPacket(operation, networkNumber, hops, ticks):
    # TCL cmd :: buildRipxPacket operation networkNumber hops ticks
    r = t.eval("buildRipxPacket {} {} {} {} ".format(operation, networkNumber, hops, ticks))
    return r


def buildArpPacket(sourceMAC, sourceIP, dutIP):
    # TCL cmd :: buildArpPacket sourceMAC sourceIP dutIP
    r = t.eval("buildArpPacket {} {} {} ".format(sourceMAC, sourceIP, dutIP))
    return r


def buildRipPacket(sourceMAC, sourceIP, destinationIP, RipCommand, IpList, ttl=64, ripVersion=2):
    # TCL cmd :: buildRipPacket sourceMAC sourceIP destinationIP RipCommand IpList ttl {0x40} ripVersion {02}
    r = t.eval("buildRipPacket {} {} {} {} {} {} {} ".format(sourceMAC, sourceIP, destinationIP, RipCommand, IpList, ttl, ripVersion))
    return r


def buildUdpEchoPacket(sourceIP, destIP, frameLength):
    # TCL cmd :: buildUdpEchoPacket sourceIP destIP frameLength
    r = t.eval("buildUdpEchoPacket {} {} {} ".format(sourceIP, destIP, frameLength))
    return r


def buildIgmpPacket(sourceIP, destIP, version, type, respTime, groupAddr):
    # TCL cmd :: buildIgmpPacket sourceIP destIP version type respTime groupAddr
    r = t.eval("buildIgmpPacket {} {} {} {} {} {} ".format(sourceIP, destIP, version, type, respTime, groupAddr))
    return r


def buildIpPriorityPacket(sourceIP, destIP, frameLength, TOS):
    # TCL cmd :: buildIpPriorityPacket sourceIP destIP frameLength TOS
    r = t.eval("buildIpPriorityPacket {} {} {} {} ".format(sourceIP, destIP, frameLength, TOS))
    return r


def buildVlanTagPacket(userPriority, CFIformat, VID, data):
    # TCL cmd :: buildVlanTagPacket userPriority CFIformat VID data
    r = t.eval("buildVlanTagPacket {} {} {} {} ".format(userPriority, CFIformat, VID, data))
    return r


def buildSnmpPacket(sourceIP, destIP, sourcePort, communityName, oid):
    # TCL cmd :: buildSnmpPacket sourceIP destIP sourcePort communityName oid
    r = t.eval("buildSnmpPacket {} {} {} {} {} ".format(sourceIP, destIP, sourcePort, communityName, oid))
    return r


def buildIcmpPacket(sourceIP, destIP, dataLength, icmpEcho, icmpSequence):
    # TCL cmd :: buildIcmpPacket sourceIP destIP dataLength icmpEcho icmpSequence
    r = t.eval("buildIcmpPacket {} {} {} {} {} ".format(sourceIP, destIP, dataLength, icmpEcho, icmpSequence))
    return r


def buildBpduPacket(rootID="00 10 FF E4 1C 0D", bridgeID="00 10 FF E4 1C 0D", protocolID=None, versionID=None, bpduType=None, bitField=None, rootPriority=None, rootPathCost=None, bridgePriority=32768, portID=128, messageAge=17920, maxAge=20, helloTime=2, forwardDelay=15):
    # TCL cmd :: buildBpduPacket rootID {00 10 FF E4 1C 0D} bridgeID {00 10 FF E4 1C 0D} protocolID versionID bpduType bitField rootPriority rootPathCost bridgePriority {32768} portID {128} messageAge {17920} maxAge {20} helloTime {2} forwardDelay {15}
    if protocolID is None: print "TCL argument `protocolID` cannot be empty!"; return False
    if versionID is None: print "TCL argument `versionID` cannot be empty!"; return False
    if bpduType is None: print "TCL argument `bpduType` cannot be empty!"; return False
    if bitField is None: print "TCL argument `bitField` cannot be empty!"; return False
    if rootPriority is None: print "TCL argument `rootPriority` cannot be empty!"; return False
    if rootPathCost is None: print "TCL argument `rootPathCost` cannot be empty!"; return False
    r = t.eval("buildBpduPacket {} {} {} {} {} {} {} {} {} {} {} {} {} {} ".format(rootID, bridgeID, protocolID, versionID, bpduType, bitField, rootPriority, rootPathCost, bridgePriority, portID, messageAge, maxAge, helloTime, forwardDelay))
    return r


def ixGetArgument(argList, argToFind):
    # TCL cmd :: ixGetArgument argList argToFind
    r = t.eval("ixGetArgument {} {} ".format(argList, argToFind))
    return r


def isUNIX():
    # TCL cmd :: isUNIX
    r = t.eval("isUNIX ".format())
    return r


def isWindows():
    # TCL cmd :: isWindows
    r = t.eval("isWindows ".format())
    return r


def RandomRange(ix_range):
    # TCL cmd :: RandomRange range
    r = t.eval("RandomRange {} ".format(ix_range))
    return r


def Random():
    # TCL cmd :: Random
    r = t.eval("Random ".format())
    return r


def RandomInit():
    # TCL cmd :: RandomInit
    r = t.eval("RandomInit ".format())
    return r


def RandomFromTo(ix_from, to):
    # TCL cmd :: RandomFromTo from to
    r = t.eval("RandomFromTo {} {} ".format(ix_from, to))
    return r


def serverSocketAccept(socket, addr, port):
    # TCL cmd :: serverSocketAccept socket addr port
    r = t.eval("serverSocketAccept {} {} {} ".format(socket, addr, port))
    return r


def readsocket(socket):
    # TCL cmd :: readsocket socket
    r = t.eval("readsocket {} ".format(socket))
    return r


def handleEvent(socket, line):
    # TCL cmd :: handleEvent socket line
    r = t.eval("handleEvent {} {} ".format(socket, line))
    return r


def generatePort():
    # TCL cmd :: generatePort
    r = t.eval("generatePort ".format())
    return r


def putsClient(line):
    # TCL cmd :: putsClient line
    r = t.eval("putsClient {} ".format(line))
    return r


def createServerSocket(port=-1, retry=true):
    # TCL cmd :: createServerSocket port {-1} retry {true}
    r = t.eval("createServerSocket {} {} ".format(port, retry))
    return r


def closeSocket(socket):
    # TCL cmd :: closeSocket socket
    r = t.eval("closeSocket {} ".format(socket))
    return r


def closeServerSocket():
    # TCL cmd :: closeServerSocket
    r = t.eval("closeServerSocket ".format())
    return r


def isTestCommandSocket(socket):
    # TCL cmd :: isTestCommandSocket socket
    r = t.eval("isTestCommandSocket {} ".format(socket))
    return r


def isLogSocket(socket):
    # TCL cmd :: isLogSocket socket
    r = t.eval("isLogSocket {} ".format(socket))
    return r


def isCommandSocket(socket):
    # TCL cmd :: isCommandSocket socket
    r = t.eval("isCommandSocket {} ".format(socket))
    return r


def isDataSocket(socket):
    # TCL cmd :: isDataSocket socket
    r = t.eval("isDataSocket {} ".format(socket))
    return r


def createClientSocket(port=-1):
    # TCL cmd :: createClientSocket port {-1}
    r = t.eval("createClientSocket {} ".format(port))
    return r


def closeClientSocket(socket=-1):
    # TCL cmd :: closeClientSocket socket {-1}
    r = t.eval("closeClientSocket {} ".format(socket))
    return r


def closeAllSockets():
    # TCL cmd :: closeAllSockets
    r = t.eval("closeAllSockets ".format())
    return r


def readClientSocket(socket):
    # TCL cmd :: readClientSocket socket
    r = t.eval("readClientSocket {} ".format(socket))
    return r


def createClientSocketCreate(host, port):
    # TCL cmd :: createClientSocketCreate host port
    r = t.eval("createClientSocketCreate {} {} ".format(host, port))
    return r


def putsServer(line):
    # TCL cmd :: putsServer line
    r = t.eval("putsServer {} ".format(line))
    return r


def handleCommand(line):
    # TCL cmd :: handleCommand line
    r = t.eval("handleCommand {} ".format(line))
    return r


def checkTransmitDone(chassis, lm, port):
    # TCL cmd :: checkTransmitDone chassis lm port
    r = t.eval("checkTransmitDone {} {} {} ".format(chassis, lm, port))
    return r


def checkAllTransmitDone(TxRxArray, duration=0):
    # TCL cmd :: checkAllTransmitDone TxRxArray duration {0}
    r = t.eval("checkAllTransmitDone {} {} ".format(TxRxArray, duration))
    return r


def requestStats(TxRxArray):
    # TCL cmd :: requestStats TxRxArray
    r = t.eval("requestStats {} ".format(TxRxArray))
    return r


def collectTxStats(txList, TxNumFrames, TxActualFrames, TotalTxFrames, verbose=true):
    # TCL cmd :: collectTxStats txList TxNumFrames TxActualFrames TotalTxFrames verbose {true}
    r = t.eval("collectTxStats {} {} {} {} {} ".format(txList, TxNumFrames, TxActualFrames, TotalTxFrames, verbose))
    return r


def collectRxStats(rxList, RxNumFrames, TotalRxFrames, printError=yes, receiveCounter="userDefinedStat2"):
    # TCL cmd :: collectRxStats rxList RxNumFrames TotalRxFrames printError {yes} receiveCounter {userDefinedStat2}
    r = t.eval("collectRxStats {} {} {} {} {} ".format(rxList, RxNumFrames, TotalRxFrames, printError, receiveCounter))
    return r


def collectVlanStats(vlanList, VlanNumFrames, TotalVlanFrames):
    # TCL cmd :: collectVlanStats vlanList VlanNumFrames TotalVlanFrames
    r = t.eval("collectVlanStats {} {} {} ".format(vlanList, VlanNumFrames, TotalVlanFrames))
    return r


def collectDataIntegrityStats(rxPortList, Errors, RxFrames, TotalRxFrames, TotalErrorFrames):
    # TCL cmd :: collectDataIntegrityStats rxPortList Errors RxFrames TotalRxFrames TotalErrorFrames
    r = t.eval("collectDataIntegrityStats {} {} {} {} {} ".format(rxPortList, Errors, RxFrames, TotalRxFrames, TotalErrorFrames))
    return r


def collectSequenceStats(rxPortList, Errors, RxFrames, TotalRxFrames, TotalErrorFrames):
    # TCL cmd :: collectSequenceStats rxPortList Errors RxFrames TotalRxFrames TotalErrorFrames
    r = t.eval("collectSequenceStats {} {} {} {} {} ".format(rxPortList, Errors, RxFrames, TotalRxFrames, TotalErrorFrames))
    return r


def collectErroredFramesStats(rxPortList, ErrorredFrames, errorList):
    # TCL cmd :: collectErroredFramesStats rxPortList ErrorredFrames errorList
    r = t.eval("collectErroredFramesStats {} {} {} ".format(rxPortList, ErrorredFrames, errorList))
    return r


def collectQosStats(rxList, RxQosNumFrames, TotalQosFrames, TotalRxFrames, printError=yes):
    # TCL cmd :: collectQosStats rxList RxQosNumFrames TotalQosFrames TotalRxFrames printError {yes}
    r = t.eval("collectQosStats {} {} {} {} {} ".format(rxList, RxQosNumFrames, TotalQosFrames, TotalRxFrames, printError))
    return r


def collectStats(rxList, statNameList, RxNumFrames, TotalRxFrames, verbose="verbose"):
    # TCL cmd :: collectStats rxList statNameList RxNumFrames TotalRxFrames verbose {verbose}
    r = t.eval("collectStats {} {} {} {} {} ".format(rxList, statNameList, RxNumFrames, TotalRxFrames, verbose))
    return r


def getNumErroredFrames(chassis, lm, port, error="allErrors"):
    # TCL cmd :: getNumErroredFrames chassis lm port error {allErrors}
    r = t.eval("getNumErroredFrames {} {} {} {} ".format(chassis, lm, port, error))
    return r


def checkLinkState(PortArray, PortsToRemove, message="messageOn"):
    # TCL cmd :: checkLinkState PortArray PortsToRemove message {messageOn}
    r = t.eval("checkLinkState {} {} {} ".format(PortArray, PortsToRemove, message))
    return r


def checkPPPState(PortArray, message="messageOn"):
    # TCL cmd :: checkPPPState PortArray message {messageOn}
    r = t.eval("checkPPPState {} {} ".format(PortArray, message))
    return r


def getRunningRate(portList, RunningRate, args, sampleNum=1):
    # TCL cmd :: getRunningRate portList RunningRate args sampleNum {1}
    r = t.eval("getRunningRate {} {} {} {} ".format(portList, RunningRate, args, sampleNum))
    return r


def getRunRatePerSecond(TxRxArray, TxRateArray, RxRateArray, duration):
    # TCL cmd :: getRunRatePerSecond TxRxArray TxRateArray RxRateArray duration
    r = t.eval("getRunRatePerSecond {} {} {} {} ".format(TxRxArray, TxRateArray, RxRateArray, duration))
    return r


def collectRates(TxRxArray, AvgRateArray, duration, rateType="rxRate", RxRateArray=None):
    # TCL cmd :: collectRates TxRxArray AvgRateArray duration rateType {rxRate} RxRateArray
    if RxRateArray is None: print "TCL argument `RxRateArray` cannot be empty!"; return False
    r = t.eval("collectRates {} {} {} {} {} ".format(TxRxArray, AvgRateArray, duration, rateType, RxRateArray))
    return r


def capitalizeString(str):
    # TCL cmd :: capitalizeString str
    r = t.eval("capitalizeString {} ".format(str))
    return r


def stringRepeat(string, repeatCount):
    # TCL cmd :: stringRepeat string repeatCount
    r = t.eval("stringRepeat {} {} ".format(string, repeatCount))
    return r


def stringIsInteger(string):
    # TCL cmd :: stringIsInteger string
    r = t.eval("stringIsInteger {} ".format(string))
    return r


def stringIsDouble(string):
    # TCL cmd :: stringIsDouble string
    r = t.eval("stringIsDouble {} ".format(string))
    return r


def stringSubstitute(string1, old, new):
    # TCL cmd :: stringSubstitute string1 old new
    r = t.eval("stringSubstitute {} {} {} ".format(string1, old, new))
    return r


def stringUnderscore(theString, underscore="=", tabs="observe"):
    # TCL cmd :: stringUnderscore theString underscore {=} tabs {observe}
    r = t.eval("stringUnderscore {} {} {} ".format(theString, underscore, tabs))
    return r


def stringTitle(theString, whichWords="significant"):
    # TCL cmd :: stringTitle theString whichWords {significant}
    r = t.eval("stringTitle {} {} ".format(theString, whichWords))
    return r


def stringSplitToTitle(theString):
    # TCL cmd :: stringSplitToTitle theString
    r = t.eval("stringSplitToTitle {} ".format(theString))
    return r


def stringJoinFromTitle(theString):
    # TCL cmd :: stringJoinFromTitle theString
    r = t.eval("stringJoinFromTitle {} ".format(theString))
    return r


def stringToUpper(theString, index1=-1, index2=-1):
    # TCL cmd :: stringToUpper theString index1 {-1} index2 {-1}
    r = t.eval("stringToUpper {} {} {} ".format(theString, index1, index2))
    return r


def stringMap(ix_map, value):
    # TCL cmd :: stringMap map value
    r = t.eval("stringMap {} {} ".format(ix_map, value))
    return r


def stringCompare(args):
    # TCL cmd :: stringCompare args
    r = t.eval("stringCompare {} ".format(args))
    return r


def stringFormatNumber(value, args):
    # TCL cmd :: stringFormatNumber value args
    r = t.eval("stringFormatNumber {} {} ".format(value, args))
    return r


def stringReplace(oldString, first, last, newString):
    # TCL cmd :: stringReplace oldString first last newString
    r = t.eval("stringReplace {} {} {} {} ".format(oldString, first, last, newString))
    return r


def send_learn_frames(PortArray, RemovedPorts, staggeredStart=true):
    # TCL cmd :: send_learn_frames PortArray RemovedPorts staggeredStart {true}
    r = t.eval("send_learn_frames {} {} {} ".format(PortArray, RemovedPorts, staggeredStart))
    return r


def OLDsend_arp_frames(PortArray, RemovedPorts):
    # TCL cmd :: OLDsend_arp_frames PortArray RemovedPorts
    r = t.eval("OLDsend_arp_frames {} {} ".format(PortArray, RemovedPorts))
    return r


def send_arp_frames(PortArray, RemovedPorts, resetInterfaces=true):
    # TCL cmd :: send_arp_frames PortArray RemovedPorts resetInterfaces {true}
    r = t.eval("send_arp_frames {} {} {} ".format(PortArray, RemovedPorts, resetInterfaces))
    return r


def configureArp(PortArray, ArpList, write="write", numInterfaces=1, resetInterfaces=true):
    # TCL cmd :: configureArp PortArray ArpList write {write} numInterfaces {1} resetInterfaces {true}
    r = t.eval("configureArp {} {} {} {} {} ".format(PortArray, ArpList, write, numInterfaces, resetInterfaces))
    return r


def sendArp(PortArray, arpList, RemovedPorts):
    # TCL cmd :: sendArp PortArray arpList RemovedPorts
    r = t.eval("sendArp {} {} {} ".format(PortArray, arpList, RemovedPorts))
    return r


def verifyAllArpFramesSent(portList):
    # TCL cmd :: verifyAllArpFramesSent portList
    r = t.eval("verifyAllArpFramesSent {} ".format(portList))
    return r


def verifyArpReply(portList):
    # TCL cmd :: verifyArpReply portList
    r = t.eval("verifyArpReply {} ".format(portList))
    return r


def send_neighborDiscovery_frames(PortArray, RemovedPorts, resetInterfaces=true):
    # TCL cmd :: send_neighborDiscovery_frames PortArray RemovedPorts resetInterfaces {true}
    r = t.eval("send_neighborDiscovery_frames {} {} {} ".format(PortArray, RemovedPorts, resetInterfaces))
    return r


def performNeighborDiscovery(PortArray, RemovedPorts, resetInterfaces=true):
    # TCL cmd :: performNeighborDiscovery PortArray RemovedPorts resetInterfaces {true}
    r = t.eval("performNeighborDiscovery {} {} {} ".format(PortArray, RemovedPorts, resetInterfaces))
    return r


def sendRouterSolicitation(PortList):
    # TCL cmd :: sendRouterSolicitation PortList
    r = t.eval("sendRouterSolicitation {} ".format(PortList))
    return r


def getNeighborDiscovery(PortList, MacAddrArray, verbose=False):
    # TCL cmd :: getNeighborDiscovery PortList MacAddrArray verbose {false}
    r = t.eval("getNeighborDiscovery {} {} {} ".format(PortList, MacAddrArray, verbose))
    return r


def getNeighborDiscoveryPort(chassId, cardId, portId, verbose=False):
    # TCL cmd :: getNeighborDiscoveryPort chassId cardId portId verbose {false}
    r = t.eval("getNeighborDiscoveryPort {} {} {} {} ".format(chassId, cardId, portId, verbose))
    return r


def sapStr2Asc(strName):
    # TCL cmd :: sapStr2Asc strName
    r = t.eval("sapStr2Asc {} ".format(strName))
    return r


def send_ripx_frames(PortArray, RemovedPorts):
    # TCL cmd :: send_ripx_frames PortArray RemovedPorts
    r = t.eval("send_ripx_frames {} {} ".format(PortArray, RemovedPorts))
    return r


def send_sap_server_frames(PortArray):
    # TCL cmd :: send_sap_server_frames PortArray
    r = t.eval("send_sap_server_frames {} ".format(PortArray))
    return r


def send_sapgns_frames(PortArray):
    # TCL cmd :: send_sapgns_frames PortArray
    r = t.eval("send_sapgns_frames {} ".format(PortArray))
    return r


def parseCmd(testName, method_name, Args):
    # TCL cmd :: parseCmd testName method_name Args
    r = t.eval("parseCmd {} {} {} ".format(testName, method_name, Args))
    return r


def configureOptions(testName, arguments):
    # TCL cmd :: configureOptions testName arguments
    r = t.eval("configureOptions {} {} ".format(testName, arguments))
    return r


def cgetOptions(testName, arguments):
    # TCL cmd :: cgetOptions testName arguments
    r = t.eval("cgetOptions {} {} ".format(testName, arguments))
    return r


def getParmProperty(testName, property, parmName):
    # TCL cmd :: getParmProperty testName property parmName
    r = t.eval("getParmProperty {} {} {} ".format(testName, property, parmName))
    return r


def startOptions(testName, arguments):
    # TCL cmd :: startOptions testName arguments
    r = t.eval("startOptions {} {} ".format(testName, arguments))
    return r


def registerResultVarsOptions(testName, arguments):
    # TCL cmd :: registerResultVarsOptions testName arguments
    r = t.eval("registerResultVarsOptions {} {} ".format(testName, arguments))
    return r


def existsOptions(testName, arguments):
    # TCL cmd :: existsOptions testName arguments
    r = t.eval("existsOptions {} {} ".format(testName, arguments))
    return r


def calcTrafficMix(StreamArray, BurstArray, percentUtilization=100):
    # TCL cmd :: calcTrafficMix StreamArray BurstArray percentUtilization {100}
    r = t.eval("calcTrafficMix {} {} {} ".format(StreamArray, BurstArray, percentUtilization))
    return r


def calcAggregateDataRate(frameSizeList, bitRate, speed, preambleSize=8):
    # TCL cmd :: calcAggregateDataRate frameSizeList bitRate speed preambleSize {8}
    r = t.eval("calcAggregateDataRate {} {} {} {} ".format(frameSizeList, bitRate, speed, preambleSize))
    return r


def calcAggregateFrameRate(frameSizeList, bitRate, speed, preambleSize=8):
    # TCL cmd :: calcAggregateFrameRate frameSizeList bitRate speed preambleSize {8}
    r = t.eval("calcAggregateFrameRate {} {} {} {} ".format(frameSizeList, bitRate, speed, preambleSize))
    return r


def calcAggregateTotalRate(frameSizeList, bitRate, speed, preambleSize=8):
    # TCL cmd :: calcAggregateTotalRate frameSizeList bitRate speed preambleSize {8}
    r = t.eval("calcAggregateTotalRate {} {} {} {} ".format(frameSizeList, bitRate, speed, preambleSize))
    return r


def calcAggregateBitRate(frameSizeList, bitRate, speed, includeCRC=true, includePreamble=true, preambleSize=8):
    # TCL cmd :: calcAggregateBitRate frameSizeList bitRate speed includeCRC {true} includePreamble {true} preambleSize {8}
    r = t.eval("calcAggregateBitRate {} {} {} {} {} {} ".format(frameSizeList, bitRate, speed, includeCRC, includePreamble, preambleSize))
    return r


def calcAggregatePPS(frameSizeList, pps, speed, preambleSize=8):
    # TCL cmd :: calcAggregatePPS frameSizeList pps speed preambleSize {8}
    r = t.eval("calcAggregatePPS {} {} {} {} ".format(frameSizeList, pps, speed, preambleSize))
    return r


def calcTotalBits(frameSizeList, includeCRC=true, includePreamble=true, preambleSize=8):
    # TCL cmd :: calcTotalBits frameSizeList includeCRC {true} includePreamble {true} preambleSize {8}
    r = t.eval("calcTotalBits {} {} {} {} ".format(frameSizeList, includeCRC, includePreamble, preambleSize))
    return r


def calcTotalStreamTime(TxRxArray, StreamArray, BurstArray, Loopcount, duration, percentUtilization=100, numRxAddresses=1, preambleSize=8):
    # TCL cmd :: calcTotalStreamTime TxRxArray StreamArray BurstArray Loopcount duration percentUtilization {100} numRxAddresses {1} preambleSize {8}
    r = t.eval("calcTotalStreamTime {} {} {} {} {} {} {} {} ".format(TxRxArray, StreamArray, BurstArray, Loopcount, duration, percentUtilization, numRxAddresses, preambleSize))
    return r


def globalSetDefault():
    # TCL cmd :: globalSetDefault
    r = t.eval("globalSetDefault ".format())
    return r


def protocolStackSetDefault():
    # TCL cmd :: protocolStackSetDefault
    r = t.eval("protocolStackSetDefault ".format())
    return r


def streamSet(chasId, cardId, portId, streamId):
    # TCL cmd :: streamSet chasId cardId portId streamId
    r = t.eval("streamSet {} {} {} {} ".format(chasId, cardId, portId, streamId))
    return r


def validateFramesize(framesize):
    # TCL cmd :: validateFramesize framesize
    r = t.eval("validateFramesize {} ".format(framesize))
    return r


def validateFramesizeList(framesizeList):
    # TCL cmd :: validateFramesizeList framesizeList
    r = t.eval("validateFramesizeList {} ".format(framesizeList))
    return r


def validatePreamblesize(preambleSize):
    # TCL cmd :: validatePreamblesize preambleSize
    r = t.eval("validatePreamblesize {} ".format(preambleSize))
    return r


def getLearnProc(portArray):
    # TCL cmd :: getLearnProc portArray
    r = t.eval("getLearnProc {} ".format(portArray))
    return r


def validateProtocol(protocols):
    # TCL cmd :: validateProtocol protocols
    r = t.eval("validateProtocol {} ".format(protocols))
    return r


def initMaxRate(PortArray, maxRateArray, framesize, userRateArray, percentRate=100, preambleSize=8):
    # TCL cmd :: initMaxRate PortArray maxRateArray framesize userRateArray percentRate {100} preambleSize {8}
    r = t.eval("initMaxRate {} {} {} {} {} {} ".format(PortArray, maxRateArray, framesize, userRateArray, percentRate, preambleSize))
    return r


def buildIpMcastMacAddress(groupAddress):
    # TCL cmd :: buildIpMcastMacAddress groupAddress
    r = t.eval("buildIpMcastMacAddress {} ".format(groupAddress))
    return r


def setPortName(portName, chassis, card, pt):
    # TCL cmd :: setPortName portName chassis card pt
    r = t.eval("setPortName {} {} {} {} ".format(portName, chassis, card, pt))
    return r


def getPortString(c, l, p, testCmd="results"):
    # TCL cmd :: getPortString c l p testCmd {results}
    r = t.eval("getPortString {} {} {} {} ".format(c, l, p, testCmd))
    return r


def getPortId(c, l, p):
    # TCL cmd :: getPortId c l p
    r = t.eval("getPortId {} {} {} ".format(c, l, p))
    return r


def getPortName(chassis, card, port, default="default"):
    # TCL cmd :: getPortName chassis card port default {default}
    r = t.eval("getPortName {} {} {} {} ".format(chassis, card, port, default))
    return r


def setPortFactoryDefaults(chassis, card, port):
    # TCL cmd :: setPortFactoryDefaults chassis card port
    r = t.eval("setPortFactoryDefaults {} {} {} ".format(chassis, card, port))
    return r


def setFactoryDefaults(portList, write="nowrite"):
    # TCL cmd :: setFactoryDefaults portList write {nowrite}
    r = t.eval("setFactoryDefaults {} {} ".format(portList, write))
    return r


def getProtocolName(protocol):
    # TCL cmd :: getProtocolName protocol
    r = t.eval("getProtocolName {} ".format(protocol))
    return r


def getDuplexModeString(duplex):
    # TCL cmd :: getDuplexModeString duplex
    r = t.eval("getDuplexModeString {} ".format(duplex))
    return r


def disableUdfs(udfList):
    # TCL cmd :: disableUdfs udfList
    r = t.eval("disableUdfs {} ".format(udfList))
    return r


def getIpClassName(classNum):
    # TCL cmd :: getIpClassName classNum
    r = t.eval("getIpClassName {} ".format(classNum))
    return r


def getMinimum(ValArray):
    # TCL cmd :: getMinimum ValArray
    r = t.eval("getMinimum {} ".format(ValArray))
    return r


def swapPortList(portList, newList):
    # TCL cmd :: swapPortList portList newList
    r = t.eval("swapPortList {} {} ".format(portList, newList))
    return r


def copyPortList(SourceList, DestList):
    # TCL cmd :: copyPortList SourceList DestList
    r = t.eval("copyPortList {} {} ".format(SourceList, DestList))
    return r


def removePorts(PortList, removePortList):
    # TCL cmd :: removePorts PortList removePortList
    r = t.eval("removePorts {} {} ".format(PortList, removePortList))
    return r


def lnumsort(option, MyList):
    # TCL cmd :: lnumsort option MyList
    r = t.eval("lnumsort {} {} ".format(option, MyList))
    return r


def mergeLists(MergedList, args):
    # TCL cmd :: mergeLists MergedList args
    r = t.eval("mergeLists {} {} ".format(MergedList, args))
    return r


def host2addr(ipAddr):
    # TCL cmd :: host2addr ipAddr
    r = t.eval("host2addr {} ".format(ipAddr))
    return r


def long2IpAddr(value):
    # TCL cmd :: long2IpAddr value
    r = t.eval("long2IpAddr {} ".format(value))
    return r


def byte2IpAddr(hexBytes):
    # TCL cmd :: byte2IpAddr hexBytes
    r = t.eval("byte2IpAddr {} ".format(hexBytes))
    return r


def num2ip(num):
    # TCL cmd :: num2ip num
    r = t.eval("num2ip {} ".format(num))
    return r


def ip2num(ipAddr):
    # TCL cmd :: ip2num ipAddr
    r = t.eval("ip2num {} ".format(ipAddr))
    return r


def long2octet(value, sizeInBytes=2):
    # TCL cmd :: long2octet value sizeInBytes {2}
    r = t.eval("long2octet {} {} ".format(value, sizeInBytes))
    return r


def list2word(mylist):
    # TCL cmd :: list2word mylist
    r = t.eval("list2word {} ".format(mylist))
    return r


def value2Hexlist(value, width):
    # TCL cmd :: value2Hexlist value width
    r = t.eval("value2Hexlist {} {} ".format(value, width))
    return r


def hexlist2Value(hexlist):
    # TCL cmd :: hexlist2Value hexlist
    r = t.eval("hexlist2Value {} ".format(hexlist))
    return r


def expandHexString(byteList, delimiter=":"):
    # TCL cmd :: expandHexString byteList delimiter {:}
    r = t.eval("expandHexString {} {} ".format(byteList, delimiter))
    return r


def getMultipleNumbers(number, maxAllowedNum, numA, numB):
    # TCL cmd :: getMultipleNumbers number maxAllowedNum numA numB
    r = t.eval("getMultipleNumbers {} {} {} {} ".format(number, maxAllowedNum, numA, numB))
    return r


def hextodec(number):
    # TCL cmd :: hextodec number
    r = t.eval("hextodec {} ".format(number))
    return r


def dectohex(number):
    # TCL cmd :: dectohex number
    r = t.eval("dectohex {} ".format(number))
    return r


def incrMacAddress(macaddr, amt):
    # TCL cmd :: incrMacAddress macaddr amt
    r = t.eval("incrMacAddress {} {} ".format(macaddr, amt))
    return r


def incrIpField(ipAddress, byteNum=4, amount=1):
    # TCL cmd :: incrIpField ipAddress byteNum {4} amount {1}
    r = t.eval("incrIpField {} {} {} ".format(ipAddress, byteNum, amount))
    return r


def incrIpFieldHexFormat(ipAddress, byteNum=4, amount=1):
    # TCL cmd :: incrIpFieldHexFormat ipAddress byteNum {4} amount {1}
    r = t.eval("incrIpFieldHexFormat {} {} {} ".format(ipAddress, byteNum, amount))
    return r


def assignIncrMacAddresses(portList):
    # TCL cmd :: assignIncrMacAddresses portList
    r = t.eval("assignIncrMacAddresses {} ".format(portList))
    return r


def incrHostIpAddr(ipAddress, amount=1):
    # TCL cmd :: incrHostIpAddr ipAddress amount {1}
    r = t.eval("incrHostIpAddr {} {} ".format(ipAddress, amount))
    return r


def waitForResidualFrames(time):
    # TCL cmd :: waitForResidualFrames time
    r = t.eval("waitForResidualFrames {} ".format(time))
    return r


def getPerTxArray(TxRxArray, PerTxArray, txPort):
    # TCL cmd :: getPerTxArray TxRxArray PerTxArray txPort
    r = t.eval("getPerTxArray {} {} {} ".format(TxRxArray, PerTxArray, txPort))
    return r


def getTxPorts(MapArray):
    # TCL cmd :: getTxPorts MapArray
    r = t.eval("getTxPorts {} ".format(MapArray))
    return r


def getRxPorts(MapArray):
    # TCL cmd :: getRxPorts MapArray
    r = t.eval("getRxPorts {} ".format(MapArray))
    return r


def getAllPorts(MapArray):
    # TCL cmd :: getAllPorts MapArray
    r = t.eval("getAllPorts {} ".format(MapArray))
    return r


def comparePortArray(KeepArray, CompareArray, removePorts="remove"):
    # TCL cmd :: comparePortArray KeepArray CompareArray removePorts {remove}
    r = t.eval("comparePortArray {} {} {} ".format(KeepArray, CompareArray, removePorts))
    return r


def mergePortArray(TxRxArray, MapArray):
    # TCL cmd :: mergePortArray TxRxArray MapArray
    r = t.eval("mergePortArray {} {} ".format(TxRxArray, MapArray))
    return r


def getAdvancedSchedulerArray(TxRxArray, AdvancedSchedulerArray, OtherArray):
    # TCL cmd :: getAdvancedSchedulerArray TxRxArray AdvancedSchedulerArray OtherArray
    r = t.eval("getAdvancedSchedulerArray {} {} {} ".format(TxRxArray, AdvancedSchedulerArray, OtherArray))
    return r


def cleanUpMultiuser():
    # TCL cmd :: cleanUpMultiuser
    r = t.eval("cleanUpMultiuser ".format())
    return r


def cleanUp():
    # TCL cmd :: cleanUp
    r = t.eval("cleanUp ".format())
    return r


def isIpAddressValid(ipAddress):
    # TCL cmd :: isIpAddressValid ipAddress
    r = t.eval("isIpAddressValid {} ".format(ipAddress))
    return r


def isMacAddressValid(macAddress):
    # TCL cmd :: isMacAddressValid macAddress
    r = t.eval("isMacAddressValid {} ".format(macAddress))
    return r


def isPartialMacAddressValid(macAddress):
    # TCL cmd :: isPartialMacAddressValid macAddress
    r = t.eval("isPartialMacAddressValid {} ".format(macAddress))
    return r


def getCommandParameters(command):
    # TCL cmd :: getCommandParameters command
    r = t.eval("getCommandParameters {} ".format(command))
    return r


def changePortLoopback(TxRxArray, enabled=true, verbose="noVerbose"):
    # TCL cmd :: changePortLoopback TxRxArray enabled {true} verbose {noVerbose}
    r = t.eval("changePortLoopback {} {} {} ".format(TxRxArray, enabled, verbose))
    return r


def validateUnidirectionalMap(TxRxArray):
    # TCL cmd :: validateUnidirectionalMap TxRxArray
    r = t.eval("validateUnidirectionalMap {} ".format(TxRxArray))
    return r


def getTxRxModeString(value, modeType="TX"):
    # TCL cmd :: getTxRxModeString value modeType {TX}
    r = t.eval("getTxRxModeString {} {} ".format(value, modeType))
    return r


def removeStreams(TxRxPortList, verbose="verbose"):
    # TCL cmd :: removeStreams TxRxPortList verbose {verbose}
    r = t.eval("removeStreams {} {} ".format(TxRxPortList, verbose))
    return r


def getIpV4MaskWidth(ipV4Mask):
    # TCL cmd :: getIpV4MaskWidth ipV4Mask
    r = t.eval("getIpV4MaskWidth {} ".format(ipV4Mask))
    return r


def getIpV4MaskFromWidth(maskWidth):
    # TCL cmd :: getIpV4MaskFromWidth maskWidth
    r = t.eval("getIpV4MaskFromWidth {} ".format(maskWidth))
    return r


def ixIsBgpInstalled():
    # TCL cmd :: ixIsBgpInstalled
    r = t.eval("ixIsBgpInstalled ".format())
    return r


def ixIsIsisInstalled():
    # TCL cmd :: ixIsIsisInstalled
    r = t.eval("ixIsIsisInstalled ".format())
    return r


def ixIsRsvpInstalled():
    # TCL cmd :: ixIsRsvpInstalled
    r = t.eval("ixIsRsvpInstalled ".format())
    return r


def ixIsOspfInstalled():
    # TCL cmd :: ixIsOspfInstalled
    r = t.eval("ixIsOspfInstalled ".format())
    return r


def ixIsRipInstalled():
    # TCL cmd :: ixIsRipInstalled
    r = t.eval("ixIsRipInstalled ".format())
    return r


def ixIsArpInstalled():
    # TCL cmd :: ixIsArpInstalled
    r = t.eval("ixIsArpInstalled ".format())
    return r


def ixIsIgmpInstalled():
    # TCL cmd :: ixIsIgmpInstalled
    r = t.eval("ixIsIgmpInstalled ".format())
    return r


def ixIsVpnL2Installed():
    # TCL cmd :: ixIsVpnL2Installed
    r = t.eval("ixIsVpnL2Installed ".format())
    return r


def ixIsVpnL3Installed():
    # TCL cmd :: ixIsVpnL3Installed
    r = t.eval("ixIsVpnL3Installed ".format())
    return r


def ixIsMldInstalled():
    # TCL cmd :: ixIsMldInstalled
    r = t.eval("ixIsMldInstalled ".format())
    return r


def ixIsOspfV3Installed():
    # TCL cmd :: ixIsOspfV3Installed
    r = t.eval("ixIsOspfV3Installed ".format())
    return r


def ixIsPimsmInstalled():
    # TCL cmd :: ixIsPimsmInstalled
    r = t.eval("ixIsPimsmInstalled ".format())
    return r


def ixGetLineUtilization(chassis, card, port, rateType="typePercentMaxRate"):
    # TCL cmd :: ixGetLineUtilization chassis card port rateType {typePercentMaxRate}
    r = t.eval("ixGetLineUtilization {} {} {} {} ".format(chassis, card, port, rateType))
    return r


def ixIsLdpInstalled():
    # TCL cmd :: ixIsLdpInstalled
    r = t.eval("ixIsLdpInstalled ".format())
    return r


def ixIsRipngInstalled():
    # TCL cmd :: ixIsRipngInstalled
    r = t.eval("ixIsRipngInstalled ".format())
    return r


def calculateMaxRate(chassis, card, port, framesize=64, preambleOrAtmEncap=8):
    # TCL cmd :: calculateMaxRate chassis card port framesize {64} preambleOrAtmEncap {8}
    r = t.eval("calculateMaxRate {} {} {} {} {} ".format(chassis, card, port, framesize, preambleOrAtmEncap))
    return r


def calculateGapBytes(chassis, card, port, framerate, framesize=64, preambleSize=8):
    # TCL cmd :: calculateGapBytes chassis card port framerate framesize {64} preambleSize {8}
    r = t.eval("calculateGapBytes {} {} {} {} {} {} ".format(chassis, card, port, framerate, framesize, preambleSize))
    return r


def calculateFPS(chassis, card, port, percentLineRate=100, framesize=64, preambleOrAtmEncap=8):
    # TCL cmd :: calculateFPS chassis card port percentLineRate {100} framesize {64} preambleOrAtmEncap {8}
    r = t.eval("calculateFPS {} {} {} {} {} {} ".format(chassis, card, port, percentLineRate, framesize, preambleOrAtmEncap))
    return r


def calculatePercentMaxRate(chassis, card, port, framerate, framesize, preambleOrAtmEncap=8):
    # TCL cmd :: calculatePercentMaxRate chassis card port framerate framesize preambleOrAtmEncap {8}
    r = t.eval("calculatePercentMaxRate {} {} {} {} {} {} ".format(chassis, card, port, framerate, framesize, preambleOrAtmEncap))
    return r


def vlanUtilsSetDefault():
    # TCL cmd :: vlanUtilsSetDefault
    r = t.eval("vlanUtilsSetDefault ".format())
    return r


def setPortTagged(chassis, card, port):
    # TCL cmd :: setPortTagged chassis card port
    r = t.eval("setPortTagged {} {} {} ".format(chassis, card, port))
    return r


def setTagged(portList):
    # TCL cmd :: setTagged portList
    r = t.eval("setTagged {} ".format(portList))
    return r


def setPortUntagged(chassis, card, port):
    # TCL cmd :: setPortUntagged chassis card port
    r = t.eval("setPortUntagged {} {} {} ".format(chassis, card, port))
    return r


def setUntagged(portList):
    # TCL cmd :: setUntagged portList
    r = t.eval("setUntagged {} ".format(portList))
    return r


def isPortTagged(chassis, card, port):
    # TCL cmd :: isPortTagged chassis card port
    r = t.eval("isPortTagged {} {} {} ".format(chassis, card, port))
    return r


def getUntaggedPortList():
    # TCL cmd :: getUntaggedPortList
    r = t.eval("getUntaggedPortList ".format())
    return r


def emptyUntaggedPortList():
    # TCL cmd :: emptyUntaggedPortList
    r = t.eval("emptyUntaggedPortList ".format())
    return r


def chassis(args):
    # TCL cmd :: chassis args
    r = t.eval("chassis {} ".format(args))
    return r


def card(args):
    # TCL cmd :: card args
    r = t.eval("card {} ".format(args))
    return r


def port(args):
    # TCL cmd :: port args
    r = t.eval("port {} ".format(args))
    return r


def stat(args):
    # TCL cmd :: stat args
    r = t.eval("stat {} ".format(args))
    return r


def ix_filter(args):
    # TCL cmd :: filter args
    r = t.eval("filter {} ".format(args))
    return r


def flexibleTimestamp(args):
    # TCL cmd :: flexibleTimestamp args
    r = t.eval("flexibleTimestamp {} ".format(args))
    return r


def filterPallette(args):
    # TCL cmd :: filterPallette args
    r = t.eval("filterPallette {} ".format(args))
    return r


def capture(args):
    # TCL cmd :: capture args
    r = t.eval("capture {} ".format(args))
    return r


def ipAddressTable(args):
    # TCL cmd :: ipAddressTable args
    r = t.eval("ipAddressTable {} ".format(args))
    return r


def arpServer(args):
    # TCL cmd :: arpServer args
    r = t.eval("arpServer {} ".format(args))
    return r


def interfaceTable(args):
    # TCL cmd :: interfaceTable args
    r = t.eval("interfaceTable {} ".format(args))
    return r


def protocol(args):
    # TCL cmd :: protocol args
    r = t.eval("protocol {} ".format(args))
    return r


def protocolServer(args):
    # TCL cmd :: protocolServer args
    r = t.eval("protocolServer {} ".format(args))
    return r


def oamPort(args):
    # TCL cmd :: oamPort args
    r = t.eval("oamPort {} ".format(args))
    return r


def stream(args):
    # TCL cmd :: stream args
    r = t.eval("stream {} ".format(args))
    return r


def streamRegion(args):
    # TCL cmd :: streamRegion args
    r = t.eval("streamRegion {} ".format(args))
    return r


def arp(args):
    # TCL cmd :: arp args
    r = t.eval("arp {} ".format(args))
    return r


def ix_exec(cmd):
    r = t.eval(cmd)
    return r


if __name__ == "__main__":
    funcs = [x[0] for x in locals().items() if callable( x[1] )]
    # print sorted(funcs)
    print 'Found {} functions!'.format(len(funcs))

    print isUNIX()
    print 'Connect to TCL Server:', ixConnectToTclServer("10.144.31.91")
    print 'Connect to Chassis', ixConnectToChassis("10.144.31.91")

    print 'Config chassis...'
    portList = ''
    chassis('get 10.144.31.91')
    py_chassis = chassis('cget -id')
    print py_chassis

    print 'Config card...'
    py_card = 1
    card('setDefault')
    card('config -txFrequencyDeviation 0')
    print py_card

    print 'Config port...'
    py_port = 1
    port('setFactoryDefaults {} {} {}'.format(py_chassis, py_card, py_port))
    port('config -speed                     100')
    port('config -duplex                    full')
    port('config -flowControl               false')
    print py_port

    print 'Config stat...'
    stat('setDefault')
    stat('config -mode                      statNormal')
    stat('config -enableValidStats          false')
    stat('config -enableProtocolServerStats true')
    stat('config -enableArpStats            true')
    stat('config -enablePosExtendedStats    true')
    stat('config -enableDhcpStats           false')
    stat('config -enableDhcpV6Stats         false')
    stat('config -enableEthernetOamStats    false')
    print 'Done.'

    print 'Config flexibleTimestamp...'
    flexibleTimestamp('setDefault')
    flexibleTimestamp('config -type          timestampBeforeCrc')
    flexibleTimestamp('config -offset        23')
    print 'Done.'

    print 'Config filter...'
    filter('setDefault')
    filter('config -captureTriggerDA         anyAddr')
    filter('config -captureTriggerSA         anyAddr')
    filter('config -captureTriggerPattern    anyPattern')
    filter('config -captureTriggerError      errAnyFrame')
    print 'Done.'

    print 'Config filterPallette...'
    filterPallette('setDefault')
    filterPallette('config -DA1              "00 00 00 00 00 00"')
    filterPallette('config -DAMask1          "00 00 00 00 00 00"')
    filterPallette('config -DA2              "00 00 00 00 00 00"')
    filterPallette('config -DAMask2          "00 00 00 00 00 00"')
    filterPallette('config -SA1              "00 00 00 00 00 00"')
    filterPallette('config -SAMask1          "00 00 00 00 00 00"')
    filterPallette('config -SA2              "00 00 00 00 00 00"')
    filterPallette('config -SAMask2          "00 00 00 00 00 00"')
    filterPallette('config -pattern1         "DE ED EF FE AC CA"')
    filterPallette('config -patternMask1     "00 00 00 00 00 00"')
    print 'Done.'

    print 'Config capture...'
    capture('setDefault')
    capture('config -fullAction              lock')
    capture('config -sliceSize               8191')
    print 'Done.'

    print 'Config ipAddressTable...'
    ipAddressTable('setDefault')
    ipAddressTable('config -defaultGateway   "0.0.0.0"')
    print 'Done.'

    print 'Config arpServer...'
    arpServer('setDefault')
    arpServer('config -retries               3')
    arpServer('config -mode                  arpGatewayOnly')
    arpServer('config -rate                  208333')
    arpServer('config -requestRepeatCount    3')
    print 'Done.'

    print 'Config interfaceTable...'
    interfaceTable('setDefault')
    interfaceTable('config -dhcpV4RequestRate                0')
    interfaceTable('config -dhcpV6RequestRate                0')
    interfaceTable('config -dhcpV4MaximumOutstandingRequests 100')
    interfaceTable('config -dhcpV6MaximumOutstandingRequests 100')
    interfaceTable('config -fcoeRequestRate                  500')
    print 'Done.'

    print 'clearAllInterfaces ...'
    interfaceTable('clearAllInterfaces')
    print 'Done.'

    print 'Config protocolServer...'
    protocolServer('setDefault')
    protocolServer('config -enableArpResponse                true')
    protocolServer('config -enablePingResponse               false')
    print 'Done.'

    print 'Config oamPort...'
    oamPort('setDefault')
    oamPort('config -enable                  false')
    oamPort('config -macAddress              "00 00 AB BA DE AD"')
    oamPort('config -enableLoopback          false')
    oamPort('config -enableLinkEvents        false')
    print 'Done.'

    print 'ixWritePortsToHardware and ixCheckLinkState ...'
    # lappend portList [list $chassis $card $port] # ???
    ixWritePortsToHardware(portList)
    ixCheckLinkState(portList)
    print 'Done.'

#
