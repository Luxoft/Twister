#!/usr/bin/env python

# version: 2.001

# File: installer.py ; This file is part of Twister.

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

import os, sys

# Install option.
TO_INSTALL = ''

while 1:
    print('\nPlease select what you wish to install:')
    print('[1] the Twister dependencies (must be ROOT)')
    print('[2] the Twister clients')
    print('[3] the Twister servers')
    print('[q] e[x]it, don\'t install anything')

    selected = raw_input('Your choice: ')
    if selected == '1':
        print('Will install dependencies.\n')
        TO_INSTALL = 'dependencies'
        break
    elif selected == '2':
        print('Will install clients.\n')
        TO_INSTALL = 'client'
        break
    elif selected == '3':
        print('Will install servers.\n')
        TO_INSTALL = 'server'
        break
    elif selected in ['0', 'q', 'x']:
        print('Ok, exiting!\n')
        exit(0)
    else:
        print('`%s` is not a valid choice! try again!' % selected)
    del selected


# Import options

if TO_INSTALL == 'client':
    import installer_client

elif TO_INSTALL == 'server':
    import installer_server

elif TO_INSTALL == 'dependencies':
    import install_dependencies

else:
    print('\nOption error!\n')
