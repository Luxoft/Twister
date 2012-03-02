#!/usr/bin/python

import xmlrpclib

proxy = xmlrpclib.ServerProxy('http://11.126.32.9:8000/')	# Tsc Server
#proxy = xmlrpclib.ServerProxy('http://11.126.32.12:8000/')	# Dan Ubuntu
#proxy = xmlrpclib.ServerProxy('http://11.126.32.14:8000/')	# Cro Windows
#proxy = xmlrpclib.ServerProxy('http://10.0.2.15:8000/')	# OpenSUSE VM

print proxy.echo('i will reset all your logs!!!')
proxy.resetLogs()
print proxy.echo('all your logs clean!')
