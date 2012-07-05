#!/usr/bin/python

# File: httpserver.py ; This file is part of Twister.

# Copyright (C) 2012 , Luxoft

# Authors:
#    Andrei Costachi <acostachi@luxoft.com>
#    Andrei Toma <atoma@luxoft.com>
#    Cristian Constantin <crconstantin@luxoft.com>
#    Daniel Cioata <dcioata@luxoft.com>

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
