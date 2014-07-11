
# File: TscThreadsLib.py ; This file is part of Twister.

# version: 3.001

# Copyright (C) 2012-2014 , Luxoft

# Authors:
#    Andrei Costachi <acostachi@luxoft.com>
#    Cristi Constantin <crconstantin@luxoft.com>
#    Daniel Cioata <dcioata@luxoft.com>
#    Mihail Tudoran <mtudoran@luxoft.com>

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This module contains Threading Functions.\n
Use `tasks_reset` before running anything, to cleanup the previous queue!\n
Use `tasks_append` to insert functions that take a long time to finish.\n
Use `tasks_start` to spawn all the functions from the queue.
"""

from __future__ import print_function
import traceback
from threading import Thread

#

tasks = []

#

class ThreadWithReturnValue(Thread):
    """
    Helper class.
    """
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs, Verbose)
        self.daemon = False
        self.result = None

    def run(self):
        """
        Main function.
        """
        if self._Thread__target is not None:
            try:
                self.result = self._Thread__target(*self._Thread__args, **self._Thread__kwargs)
            except Exception:
                trace = traceback.format_exc()[34:].strip()
                print('Exception:: {}'.format(trace))
                self.result = False

#

def tasks_reset():
    """
    Reset tasks.
    """
    global tasks
    print('Threads:: Reseting tasks...')
    tasks = []

#

def tasks_append(func, *args, **kwargs):
    """
    Add a task.
    """
    print('Threads:: Appending function', func, args, kwargs)
    g = ThreadWithReturnValue(target=func, args=args, kwargs=kwargs)
    tasks.append(g)
    return True

#

def tasks_start(timeout=None):
    """
    Spawn tasks.
    """
    print('Threads:: Starting tasks...')
    for t in tasks:
        t.start()
    for t in tasks:
        t.join(timeout)
    print('Threads:: Finished tasks!')
    result = [t.result for t in tasks]
    return result
