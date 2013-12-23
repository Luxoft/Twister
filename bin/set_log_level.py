#!/usr/bin/env python2.7

# File: set_log_level.py ; This file is part of Twister.

# version: 3.001

# Copyright (C) 2012-2013 , Luxoft

# Authors:
#    Adrian Toader <adtoader@luxoft.com>
#    Andrei Costachi <acostachi@luxoft.com>
#    Andrei Toma <atoma@luxoft.com>
#    Cristi Constantin <crconstantin@luxoft.com>
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

import sys
import rpyc

try:
    c = rpyc.connect('127.0.0.1', 8010)
except Exception as e:
    print('\nCannot connect to CE! Exception: `{}`!\n'.format(e))
    exit(1)

try:
    level = int(sys.argv[1])
except:
    level = c.root.getLogLevel()
    print('\nThe log level is `{}`.\n'.format(level))
    exit(1)

if level <= 0 or level > 5:
    print('\nInvalid log level `{}` ! Must give an integer between 1-5 !\n'.format(level))
    exit(1)

c.root.setLogLevel( level )

if level == 1:
    print('\nLog level set to `{}`.\nWARNING! This should only be used for development and debugging!\n'.format(level))
else:
    print('\nLog level set to `{}`.\n'.format(level))
