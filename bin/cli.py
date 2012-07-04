#!/usr/bin/python

import xmlrpclib
import sys
import os


#proxy = xmlrpclib.ServerProxy('http://11.126.32.9:8000/')	# Tsc Server
proxy = xmlrpclib.ServerProxy('http://127.0.0.1:8000/')	# Virtualbox VM

user = os.getenv('USER')

status = sys.argv[1:2]
config = sys.argv[2:3]

if config and not os.path.exists(config[0]):
	print 'Please enter an existing config file!'
	exit(1)

if not status:
	print 'You must provide one of the following commands: start/stop/pause!'
	exit(1)

if sys.argv[1] == 'start':
	if config:
		print proxy.setExecStatusAll(user, 2, config[0])
	else:
		print proxy.setExecStatusAll(user, 2)
elif sys.argv[1] == 'stop':
	if config:
		print proxy.setExecStatusAll(user, 0, config[0])
	else:
		print proxy.setExecStatusAll(user, 0)
elif sys.argv[1] == 'pause':
	if config:
		print proxy.setExecStatusAll(user, 1, config[0])
	else:
		print proxy.setExecStatusAll(user, 1)
else:
	print 'Invalid status: ', sys.argv[1]