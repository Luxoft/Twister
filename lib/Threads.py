
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
This module contains Threading Functions.\n
Use `tasks_append` to insert functions that take a long time to finish.\n
Use `tasks_start` to spawn all the functions from the queue.
'''

from threading import Thread

#

tasks = []

#

class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs, Verbose)
        self.daemon = False
        self._return = None

    def run(self):
        if self._Thread__target is not None:
            self._return = self._Thread__target(*self._Thread__args, **self._Thread__kwargs)

#

def tasks_reset():
    global tasks
    print 'Threads:: Reseting tasks...'
    del tasks
    tasks = []

#

def tasks_append(func, *args, **kwargs):
    global tasks
    print 'Threads:: Appending function', func, args, kwargs
    g = ThreadWithReturnValue(target=func, args=args, kwargs=kwargs)
    tasks.append(g)
    return True

#

def tasks_start(timeout=None):
    global tasks
    print 'Threads:: Starting tasks...'
    [t.start() for t in tasks]
    [t.join(timeout) for t in tasks]
    result = [t._return for t in tasks]
    print 'Threads:: Finished tasks!'
    return result
