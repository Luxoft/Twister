
# <title> Test 03 </title>
# <description> Testing service GetMethods. This should fail. </description>

import time
from suds.client import Client
try: from ce_libs import logMsg
except:
	def logMsg(*args):
		print args

def printLog(args):
	print args
	logMsg('logDebug', args)

link = 'http://tsc-server:9090/axis2/services/AM_Server?wsdl'
c = Client(link)

print '\nConnected to SOAP Server at `%s`!\n' % link

expected = c.factory.create('ArrayOfString')
expected.string = [
	"MeterInstalledNotification",
	"GetPublishMethods",
	"ServiceOrderClosedNotification",
	"MeterRetireNotification",
	"DomainMembersChangedNotification",
	"StreetLightChangedNotification",
	"GetMethods",
	"GetMeterTestByMeterID",
	"ServiceOrderOpenedNotification",
	"GetAttachmentList",
	"CDDeviceRemoveNotification",
	"MeterBaseRemoveNotification",
	"PPMMeterExchangeNotification",
	"CDDeviceRetireNotification",
	"MeterRemoveNotification",
	"InHomeDisplayRetireNotification",
	"LMDeviceAddNotification",
	"MeterBaseAddNotification",
	"MeterBaseExchangeNotification",
	"MeterChangedNotification",
	"MeterBaseRetireNotification",
	"MeterBaseInstalledNotification",
	"InHomeDisplayInstalledNotification",
	"SecurityLightChangedNotification",
	"CDDeviceChangedNotification",
	"LMDeviceExchangeNotification",
	"MeterEventNotification",
	"MeterAddNotification",
	"MeterExchangeNotification",
	"MeterBaseChangedNotification",
	"EndDeviceShipmentNotification",
	"PoleChangedNotification",
	"TrafficLightChangedNotification",
	"LMDeviceInstalledNotification",
	"InHomeDisplayRemoveNotification",
	"TransformerBankChangedNotification",
	"LMDeviceRetireNotification",
	"InHomeDisplayAddNotification",
	"DomainNamesChangedNotification",
	"WorkOrderChangedNotificationToGIS",
	"LMDeviceChangedNotification",
	"AddAttachmentToWorkOrder",
	"InHomeDisplayChangedNotification",
	"UnregisterForService",
	"MeterTestNotification",
	"GetDomainNames",
	"GetRegistrationInfoByID",
	"ODDeviceChangedNotification",
	"CDDeviceExchangeNotification",
	"CDDeviceInstalledNotification",
	"InHomeDisplayExchangeNotification",
	"CDDeviceAddNotification",
	"GetDomainMembers",
	"RegisterForService",
	"RequestRegistrationID",
	"GetAttachment",
	"LMDeviceRemoveNotification",
	"ServiceOrderChangedNotification",
	"DeleteAttachmentFromWorkOrder",
	"PMChangedNotification",
	"InspectionNotification",
	#"PingURL"
	]

result = c.service.GetMethods()

printLog('Methods: %s\n' % result) ; time.sleep(1)
logMsg('logDebug', 'XML Request was:\n' + str(c.last_sent()) + '\n\n\n')
print

if str(result) == str(expected):
	printLog('The result is correct!\n\n')
	_RESULT = 'PASS'
else:
	printLog('The result is incorrect!\n\n')
	_RESULT = 'FAIL'

#
