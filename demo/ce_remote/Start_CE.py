#!/usr/bin/python

import os
import xmlrpclib

proxy = xmlrpclib.ServerProxy('http://11.126.32.9:8000/')	# Tsc Server
#proxy = xmlrpclib.ServerProxy('http://127.0.0.1:8000/')	# Virtualbox VM

user_name = os.getenv('USER')
print proxy.echo('hellooo! i will start the processes!')

print 'set status running (2):', proxy.setExecStatusAll(user_name, 2)
print 'get status:', proxy.getExecStatusAll(user_name)
print
