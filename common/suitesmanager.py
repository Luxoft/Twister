
# File: suitesmanager.py ; This file is part of Twister.

# version: 2.001

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

import os
import sys

from collections import OrderedDict

__all__ = ['SuitesManager']

#

class SuitesManager(OrderedDict):

    """
    This class controls the suites and files structure.
    The structure can become very complex when dealing with
    a lot of suites with subsuites that contain other subsuites.
    All this structure must allow files execution in order.
    This class is common for Central Engine and Execution Process!
    """

    def _recursive_find_suites(self, nodes, result=[]):
        # Nodes are Ordered Dicts
        for id, node in nodes.iteritems():
            if node['type'] != 'suite':
                continue
            result.append(id)
            ids = self._recursive_find_suites(node['children'], [])
            result.extend(ids)
        return result


    def getSuites(self):
        """
        Returns a list of suite IDs.
        """
        # Must pass a null result as default parameter!
        result = self._recursive_find_suites(self, [])
        return result


    def _recursive_find_files(self, nodes, result=[]):
        # Nodes are Ordered Dicts
        for id, node in nodes.iteritems():
            # This is a file
            if node['type'] == 'file':
                result.append(id)
            # This is a suite
            else:
                self._recursive_find_files(node['children'], result)
        return result


    def getFiles(self, suite_id=None):
        """
        Returns a list of file IDs. Can filter for one suite.
        """
        if suite_id:
            suite = self.findId(suite_id, self)
            if not suite: return []
            # Must pass a null result as default parameter!
            ids = self._recursive_find_files(suite['children'], [])
            return ids
        else:
            # Must pass a null result as default parameter!
            return self._recursive_find_files(self, [])


    def iterNodes(self, nodes=None, result=[]):
        """
        Depth iterate through suites and files.
        This is used by the Execution Runner.
        """
        if not nodes:
            nodes = self
        for id, node in nodes.iteritems():
            result.append([id, node])
            if node['type'] == 'suite':
                self.iterNodes(node['children'], result)
        return result


    def findId(self, node_id, nodes=None, _found=None):
        """
        Find a node, using the ID.
        """
        if not nodes:
            nodes = self
        if _found:
            return _found
        for id, node in nodes.iteritems():
            # The ID is found!
            if id == node_id:
                return node
            if node['type'] == 'suite':
                _found = self.findId(node_id, node['children'], _found)
        return _found

#
