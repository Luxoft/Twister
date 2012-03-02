#!/usr/bin/python

import xmlrpclib

proxy = xmlrpclib.ServerProxy('http://11.126.32.9:8000/')	# Tsc Server
#proxy = xmlrpclib.ServerProxy('http://11.126.32.12:8000/')	# Dan Ubuntu
#proxy = xmlrpclib.ServerProxy('http://11.126.32.14:8000/')	# Cro Windows
#proxy = xmlrpclib.ServerProxy('http://10.0.2.15:8000/')	# OpenSUSE VM

print proxy.echo('hellooo!')

query = """
        select suts.id, app.name, ipo.name, os.name_vers from suts,app,ipo,os where
        (suts.app_id = app.id and suts.app_id = ipo.id and suts.os_id = os.id)
        """

print proxy.runDBSelect(query)
