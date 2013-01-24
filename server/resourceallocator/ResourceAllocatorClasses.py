
# File: ResourceAllocatorClasses.py ; This file is part of Twister.

# Copyright (C) 2012-2013 , Luxoft

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

import os
import sys
import json
import thread
import cherrypy

from binascii import hexlify
from cherrypy import _cptools

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print('TWISTER_PATH environment variable is not set! Exiting!')
    exit(1)
sys.path.append(TWISTER_PATH)

from common.tsclogging import *

RESOURCE_FREE     = 1
RESOURCE_BUSY     = 2
RESOURCE_RESERVED = 3

#

def _recursive_find_id(parent_node, node_id, path=[]):
    '''
    Parent Node is a dict of nodes with structure Name: {Id, Meta, Children}.
    Node ID is a unique ID.
    '''
    if not parent_node:
        return False
    if parent_node.get('id') == node_id:
        result = dict(parent_node)
        result['path'] = path
        return result
    if not parent_node.get('children'):
        return False

    try: path.pop(-1)
    except: pass

    for node in parent_node.get('children'):
        result = _recursive_find_id(parent_node['children'][node], node_id, path)
        if result:
            path.insert(0, node)
            result['path'] = path
            return result


def _find_pointer(parent_node, node_path=[]):
    '''
    Returns the pointer to a dictionary, following the path.
    '''
    pointer = parent_node

    for node in node_path:
        if not node:
            continue
        if node in pointer['children']:
            pointer = pointer['children'][node]
        else:
            return False

    return pointer

#

class ResourceAllocator(_cptools.XMLRPCController):

    def __init__(self):

        self.resources = {'name': '/', 'meta': {}, 'children': {}}
        self.acc_lock = thread.allocate_lock() # Task change lock
        self.cfg_file = '{0}/common/resources.json'.format(TWISTER_PATH)
        self._load(v=True)

#

    def _load(self, v=False):

        try:
            f = open(self.cfg_file, 'r')
            self.resources = json.load(f)
            f.close() ; del f
            if v:
                logDebug('RA: Resources loaded successfully.')
        except:
            if v:
                logDebug('RA: There are no resources to load.')


    def _save(self):

        # Write changes.
        with self.acc_lock:
            f = open(self.cfg_file, 'w')
            json.dump(self.resources, f, indent=4)
            f.close() ; del f


    @cherrypy.expose
    def echo(self, msg):
        '''
        Simple echo function, for testing connection.
        '''
        logDebug('Echo: %s' % str(msg))
        return 'RA reply: %s' % str(msg)

#

    @cherrypy.expose
    def getResource(self, query):
        '''
        Show all the properties, or just 1 property of a resource.
        Must provide a Resource ID or a Query.
        '''

        if not query:
            msg = 'Get Resource: Cannot get a null resource !'
            logError(msg)
            return '*ERROR* ' + msg

        query = str(query)

        if query.count(':') > 1:
            msg = 'Get Resource: Invalid query ! Cannot access more than 1 meta info !'
            logError(msg)
            return '*ERROR* ' + msg

        if ':' in query:
            resource = query.split(':')[1]
            query    = query.split(':')[0]
        else:
            resource = ''

        # If the query is and ID
        if '/' not in query:
            result = _recursive_find_id(self.resources, query)

        # If the query is a / string query
        else:
            parts = query.split('/')
            result = self.resources

            for part in parts:
                if not part:
                    continue
                result = result['children'].get(part)

            result['path'] = [p for p in parts if p]

        if not result:
            return False

        result = dict(result)

        if not resource:
            result['children'] = sorted([result['children'][node]['id'] for node in result.get('children') or []])
            result['path'] = '/'.join(result.get('path', ''))
            return result
        else:
            return result['meta'].get(resource, '')

#

    def _get_res_pointer(self, query):

        # If the query is a path
        if '/' in query:
            resource_p = _find_pointer(self.resources, query.split('/'))
        # If the query is an ID
        else:
            try:
                resource_path = _recursive_find_id(self.resources, query)['path']
                resource_p = _find_pointer(self.resources, resource_path)
                del resource_path
            except:
                resource_p = None

        return resource_p


    @cherrypy.expose
    def setResource(self, name, parent=None, props={}):
        '''
        Create or change a resource, using a name, a parent Path or ID and some properties.
        '''

        parent = str(parent)

        parent_p = self._get_res_pointer(parent)

        if not parent_p:
            msg = 'Set Resource: Cannot find parent path or ID `{0}` !'.format(parent)
            logError(msg)
            return '*ERROR* ' + msg

        if not 'children' in parent_p:
            parent_p['children'] = {}

        try: del parent_p['path']
        except: pass

        # If the resource exists, patch the new properties!
        if name in parent_p['children']:
            child_p = parent_p['children'][name]
            child_p['meta'].update(props)
            # Write changes.
            self._save()
            logDebug('Updated resource `{0}` : `{1}`.'.format(child_p['id'], props))
            return True

        # If the resource is new, create it.
        else:
            res_id = hexlify(os.urandom(4))
            parent_p['children'][name] = {'id': res_id, 'meta': props, 'children': {}}
            # Write changes.
            self._save()
            logDebug('Created resource `{0}` : `{1}`.'.format(res_id, props))
            return res_id


    @cherrypy.expose
    def deleteResource(self, res_query):
        '''
        Permanently delete a resource.
        '''

        # Find the resource.
        res_p = self.getResource(res_query)

        if not res_p:
            msg = 'Del Resource: Cannot find resource path or ID `{0}` !'.format(res_query)
            logError(msg)
            return '*ERROR* ' + msg

        # Correct node path
        node_path = [p for p in res_p['path'].split('/') if p]

        exec( 'del self.resources["children"]["{0}"]'.format('"]["children"]["'.join(node_path)) )

        # Write changes.
        self._save()

        return True

#

    @cherrypy.expose
    def getResourceStatus(self, res_query):
        '''
        Returns the status of a given resource.
        '''
        res_p = self.getResource(res_query)

        if not res_p:
            msg = 'Get Status: Cannot find resource path or ID `{0}` !'.format(res_query)
            logError(msg)
            return '*ERROR* ' + msg

        return res_p.get('status', RESOURCE_FREE)


    @cherrypy.expose
    def allocResource(self, res_query):

        res_p = self._get_res_pointer(res_query)

        if not res_p:
            msg = 'Alloc Resource: Cannot find resource path or ID `{0}` !'.format(res_query)
            logError(msg)
            return '*ERROR* ' + msg
        if res_p.get('status') == RESOURCE_BUSY:
            msg = 'Alloc Resource: Cannot allocate ! The resource is already busy !'
            logError(msg)
            return '*ERROR* ' + msg

        res_p['status'] = RESOURCE_BUSY
        # Write changes.
        self._save()
        return RESOURCE_BUSY


    @cherrypy.expose
    def reserveResource(self, res_query):

        res_p = self._get_res_pointer(res_query)

        if not res_p:
            msg = 'Reserve Resource: Cannot find resource path or ID `{0}` !'.format(res_query)
            logError(msg)
            return '*ERROR* ' + msg
        if res_p.get('status') == RESOURCE_BUSY:
            msg = 'Reserve Resource: Cannot allocate ! The resource is already busy !'
            logError(msg)
            return '*ERROR* ' + msg

        res_p['status'] = RESOURCE_RESERVED
        # Write changes.
        self._save()
        return RESOURCE_RESERVED


    @cherrypy.expose
    def freeResource(self, res_query):

        res_p = self._get_res_pointer(res_query)

        if not res_p:
            msg = 'Free Resource: Cannot find resource path or ID `{0}` !'.format(res_query)
            logError(msg)
            return '*ERROR* ' + msg

        res_p['status'] = RESOURCE_FREE
        # Write changes.
        self._save()
        return RESOURCE_FREE

#

# Eof()
