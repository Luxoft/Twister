#!/usr/bin/python

import os
import xmlrpclib

proxy = xmlrpclib.ServerProxy('http://11.126.32.9:8000/')	# Tsc Server
#proxy = xmlrpclib.ServerProxy('http://127.0.0.1:8000/')	# Virtualbox VM

print proxy.echo('i will reset all your logs!!!')
user_name = os.getenv('USER')
proxy.resetLogs(user_name)
print proxy.echo('all your logs clean!')
print
