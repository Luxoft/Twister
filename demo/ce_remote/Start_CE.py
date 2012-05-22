#!/usr/bin/python

import xmlrpclib

proxy = xmlrpclib.ServerProxy('http://11.126.32.9:8000/')	# Tsc Server
#proxy = xmlrpclib.ServerProxy('http://11.126.32.12:8000/')	# Dan Ubuntu
#proxy = xmlrpclib.ServerProxy('http://11.126.32.14:8000/')	# Cro Windows
#proxy = xmlrpclib.ServerProxy('http://127.0.0.1:8000/')	# Virtualbox VM

print proxy.echo('hellooo!')
print 'Searching one EP:', proxy.searchEP('EP-1001')

print 'set status running (2):', proxy.setExecStatusAll(2)
print 'get status:', proxy.getExecStatusAll()
print
