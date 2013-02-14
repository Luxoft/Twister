
# File: Threads.py ; This file is part of Twister.

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

'''
This module contains Functions needed to communicate with Resource Allocator Server.
'''

import gevent
from gevent import *

from gevent import monkey
monkey.patch_all()

#

tasks = []

#

def tasks_reset():
    print 'Threads:: Reseting tasks...'
    global tasks
    tasks = []

#

def tasks_append(func, *args, **kwargs):
    if not callable(func):
        print 'Threads:: Cannot append object `{0}`, because it\'s not a function!'.format(func)
        return False
    print 'Threads:: Appending function', func, args, kwargs
    g = spawn(func, *args, **kwargs)
    tasks.append(g)
    return True

#

def tcl_tasks_append(string):
    # TODO ...
    return True

#

def tasks_start():
    global tasks
    print 'Threads:: Starting tasks...'
    gevent.joinall(tasks)
    print 'Threads:: Finished tasks!'
    return [t.get() for t in tasks]
