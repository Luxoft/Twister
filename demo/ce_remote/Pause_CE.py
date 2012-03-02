#!/usr/bin/python

import xmlrpclib

proxy = xmlrpclib.ServerProxy('http://11.126.32.9:8000/')	# Tsc Server
#proxy = xmlrpclib.ServerProxy('http://11.126.32.12:8000/')	# Dan Ubuntu
#proxy = xmlrpclib.ServerProxy('http://11.126.32.14:8000/')	# Cro Windows
#proxy = xmlrpclib.ServerProxy('http://10.0.2.15:8000/')	# OpenSUSE VM

print proxy.echo('hellooo!')
print 'Searching one EP:', proxy.searchEP('EPId-1001')

print 'set status paused (1):', proxy.setExecStatusAll(1)
print 'get status:', proxy.getExecStatusAll()
print
