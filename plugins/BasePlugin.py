
# File: BasePlugin.py ; This file is part of Twister.

# Copyright (C) 2012 , Luxoft

# Authors:
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

#

class BasePlugin(object):

    """
    Basic plugin class.
    """

    def __init__(self, user, data):

        self.user = user
        self.data = data


    def run(self, args):
        """
        This function is called from the Java GUI.
        """
        pass


    def onStart(self):
        """
        This function is called from the Central Engine,
        every time it Starts the execution, from status Stop or Invalid.
        On Start, you can implement actions like:
        reseting the logs, or send an e-mail alert.
        """
        pass


    def onPause(self):
        """
        This function is called from the Central Engine,
        every time it Pauses the execution of all EPs.
        """
        pass


    def onStop(self):
        """
        This function is called from the Central Engine,
        every time it Stops the execution of all EPs.
        On Stop, you can implement actions like:
        sending a report, or saving some results to database.
        """
        pass

#

# Eof()
