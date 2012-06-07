#!/usr/bin/python

import time
import random
import xmlrpclib

#proxy = xmlrpclib.ServerProxy('http://11.126.32.9:8000/')	# Tsc Server
proxy = xmlrpclib.ServerProxy('http://127.0.0.1:8000/')	# VirtualBox VM

proxy.echo('Hello CE !')

print 'Cfg path:', proxy.getConfigPath()
print 'Logs path:', proxy.getLogsPath()
print 'Log types:', proxy.getLogTypes()

print 'Search EP:', proxy.searchEP('EP-1001')
print '-----\n'


proxy.setStartedBy('cro')


for epname in proxy.listEPs().split(','):
	print '::::', epname, '::::'
	print 'Exec status ?', proxy.getExecStatus(epname)
	print 'Set status paused:', proxy.setExecStatus(epname, 1)
	print 'Exec status ?', proxy.getExecStatus(epname)
	print 'Set status stop:', proxy.setExecStatus(epname, 0)
	print 'Exec status ?', proxy.getExecStatus(epname)
	print '-----\n'


print 'Set status All:', proxy.setExecStatusAll(1, 'test msg')


print 'Exec status All 1 ?', proxy.getExecStatusAll()
time.sleep(1)
print 'Exec status All 2 ?', proxy.getExecStatusAll()
time.sleep(1)
print 'Exec status All 3 ?', proxy.getExecStatusAll()
print '-----\n'


print 'Reset logs ?', proxy.resetLogs()
print 'Reset debug ?', proxy.resetLog('log_debug.log')
print '-----\n'


for epname in proxy.listEPs().split(','):
	for file_id in proxy.getEpFiles(epname):
		print '::::', epname, file_id, '::::'
		print 'Set F Status:', proxy.setFileStatus(epname, file_id, random.choice([2,3,5]))

	print 'Status EP ?', proxy.getFileStatusAll(epname)
	print '-----\n'

print 'Status all ?', proxy.getFileStatusAll()
print '-----\n'


print proxy.getLibrariesList()
print proxy.getEpFiles('EP-1001')
print proxy.getSuiteFiles('EP-1001', 'demo 1')
print '-----\n'


print 'logrunning:', proxy.logMessage('logrunning', 'Writing some logrunning message!')
print 'logdebug:', proxy.logMessage('logdebug', 'Writing some logdebug message!')
print 'logtest:', proxy.logMessage('logtest', 'Writing some logtest message!')
print '-----\n'


print 'Sending e-mail:', proxy.sendMail()
