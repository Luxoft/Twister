#!/usr/bin/python

# version: 2.001

# File: cli.py ; This file is part of Twister.

# Copyright (C) 2012 , Luxoft

# Authors:
#  Andrei Costachi <acostachi@luxoft.com>
#  Andrei Toma <atoma@luxoft.com>
#  Cristian Constantin <crconstantin@luxoft.com>
#  Daniel Cioata <dcioata@luxoft.com>

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import xmlrpclib
from optparse import OptionParser

#

usage = "Usage: %prog --server <ip:port> --status <start|stop|pause> --config <path> --project <path>"
version = "%prog v1.0"
parser = OptionParser(usage=usage, version=version)
user = os.getenv('USER')

parser.add_option("--server",        action="store", default="http://127.0.0.1:8000/", help="Central engine server IP and Port.")
parser.add_option("-s", "--status",  action="store", help="Status: start/ stop/ pause.")
parser.add_option("-c", "--config",  action="store", help="Path to FWMCONFIG.XML file.")
parser.add_option("-p", "--project", action="store", help="Path to PROJECT.XML file.")
(options, args) = parser.parse_args()

#

if not options.status:
	print('Must specify a status ! Exiting !')
	exit(1)
if options.status.lower() not in ['stop', 'start', 'pause']:
	print('Must specify a valid status ! Exiting !')
	exit(1)

if not options.config:
	print('Must specify a config path ! Exiting !')
	exit(1)
if not os.path.isfile(options.config):
	print('Must specify a valid config path ! Exiting !')
	exit(1)

if not options.project:
	print('Must specify a project path ! Exiting !')
	exit(1)
if not os.path.isfile(options.project):
	print('Must specify a valid project path ! Exiting !')
	exit(1)

try:
	proxy = xmlrpclib.ServerProxy(options.server)
except:
	print('Must specify a valid IP and PORT combination ! Exiting !')
	exit(1)

#

if options.status == 'start':
	print proxy.setExecStatusAll(user, 2, options.config + ',' + options.project)

elif options.status == 'stop':
	print proxy.setExecStatusAll(user, 0, options.config + ',' + options.project)

elif options.status == 'pause':
	print proxy.setExecStatusAll(user, 1, options.config + ',' + options.project)

#
