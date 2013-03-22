
# File: ResourceAllocator.py ; This file is part of Twister.

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

"""
Resource Allocator functions
****************************

All functions are exposed and can be accessed using the browser.
"""

import os, sys
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
    Node ID must be a unique ID.
    '''
    # The node is valid ?
    if not parent_node:
        return False
    # Found the node with the correct id !
    if parent_node.get('id') == node_id:
        result = dict(parent_node)
        result['path'] = path
        return result
    # This node has children ?
    if not parent_node.get('children'):
        return False
    # Check depth
    if len(path) > 25:
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
    The pointer can be used to add meta tags, or add/ delete children.
    '''
    for node in node_path:
        if not node:
            continue
        if node in parent_node['children']:
            parent_node = parent_node['children'][node]
        else:
            return False

    return parent_node


def _get_res_pointer(parent_node, query):
    '''
    Helper function.
    '''
    query = str(query)

    # If the query is a path
    if '/' in query:
        resource_p = _find_pointer(parent_node, query.split('/'))
    # If the query is an ID
    else:
        try:
            resource_path = _recursive_find_id(parent_node, query, [])['path']
            resource_p = _find_pointer(parent_node, resource_path)
            del resource_path
        except:
            resource_p = None

    return resource_p

#

class ResourceAllocator(_cptools.XMLRPCController):

    def __init__(self):

        self.resources = {'name': '/', 'meta': {}, 'children': {}}
        self.acc_lock = thread.allocate_lock() # Task change lock
        self.ren_lock = thread.allocate_lock() # Rename lock
        self.cfg_file = '{0}/config/resources.json'.format(TWISTER_PATH)
        self._load(v=True)

#

    def _load(self, v=False):

        with self.acc_lock:
            try:
                f = open(self.cfg_file, 'r')
                self.resources = json.load(f)
                f.close() ; del f
                if v:
                    logDebug('RA: Resources loaded successfully.')
            except:
                if v:
                    logDebug('RA: There are no resources to load! Invalid path `{0}`!'.format(self.cfg_file))

        return True


    def _save(self):

        # Write changes, using the Access Lock.
        with self.acc_lock:
            f = open(self.cfg_file, 'w')
            json.dump(self.resources, f, indent=4)
            f.close() ; del f

        return True


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
        Must provide a Resource ID, or a Query.
        '''
        self._load(v=False)
        # If no resources...
        if not self.resources['children']:
            msg = 'Get Resource: There are no resources defined !'
            logError(msg)
            return '*ERROR* ' + msg

        if not query:
            msg = 'Get Resource: Cannot get a null resource !'
            logError(msg)
            return '*ERROR* ' + msg

        query = str(query)

        # If the query asks for a specific Meta Tag
        if query.count(':') > 1:
            msg = 'Get Resource: Invalid query ! Cannot access more than 1 meta info !'
            logError(msg)
            return '*ERROR* ' + msg

        if ':' in query:
            meta  = query.split(':')[1]
            query = query.split(':')[0]
        else:
            meta = ''

        # If the query is an ID
        if '/' not in query:
            result = _recursive_find_id(self.resources, query, [])
            if not result:
                return False

        # If the query is a slash string query
        else:
            parts = [q for q in query.split('/') if q]
            result = self.resources

            for part in parts:
                if not result: return False
                result = result['children'].get(part)

            if not result: return False

            result['path'] = [p for p in parts if p]

        result = dict(result)

        if not meta:
            result['children'] = sorted([result['children'][node]['id'] for node in result.get('children') or []])
            result['path'] = '/'.join(result.get('path', ''))
            return result
        else:
            return result['meta'].get(meta, '')

#

    @cherrypy.expose
    def setResource(self, name, parent=None, props={}):
        '''
        Create or change a resource, using a name, a parent Path or ID and some properties.
        '''
        self._load(v=False)

        parent_p = _get_res_pointer(self.resources, parent)

        if not parent_p:
            msg = 'Set Resource: Cannot find parent path or ID `{0}` !'.format(parent)
            logError(msg)
            return '*ERROR* ' + msg

        if isinstance(props, dict):
            pass
        elif (isinstance(props, str) or isinstance(props, unicode)):
            props = props.replace("'", '"')
            try:
                props = json.loads(props)
            except:
                msg = 'Set Resource: Cannot parse properties: `{0}` !'.format(props)
                logError(msg)
                return '*ERROR* ' + msg
        else:
            msg = 'Set Resource: Invalid properties `{0}` !'.format(props)
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
            res_id = False

            while not res_id:
                res_id = hexlify(os.urandom(5))
                # If by any chance, this ID already exists, generate another one!
                if _recursive_find_id(self.resources, res_id, []):
                    res_id = False

            parent_p['children'][name] = {'id': res_id, 'meta': props, 'children': {}}
            # Write changes.
            self._save()
            logDebug('Created resource `{0}` : `{1}`.'.format(res_id, props))
            return res_id


    @cherrypy.expose
    def renameResource(self, res_query, new_name):
        '''
        Rename a resource.
        '''
        self._load(v=False)

        # If no resources...
        if not self.resources['children']:
            msg = 'Rename Resource: There are no resources defined !'
            logError(msg)
            return '*ERROR* ' + msg

        if '/' in new_name:
            msg = 'Rename Resource: New resource name cannot contain `/` !'
            logError(msg)
            return '*ERROR* ' + msg

        if ':' in new_name:
            msg = 'Rename Resource: New resource name cannot contain `:` !'
            logError(msg)
            return '*ERROR* ' + msg

        if ':' in res_query:
            meta      = res_query.split(':')[1]
            res_query = res_query.split(':')[0]
        else:
            meta = ''

        # Find the resource pointer.
        res_p = self.getResource(res_query)

        if not res_p:
            msg = 'Rename Resource: Cannot find resource path or ID `{0}` !'.format(res_query)
            logError(msg)
            return '*ERROR* ' + msg

        # Correct node path
        node_path = [p for p in res_p['path'].split('/') if p]
        # Renamed node path
        new_path = list(node_path) ; new_path[-1] = new_name

        if not node_path:
            msg = 'Rename Resource: Cannot find resource node path `{0}` !'.format(node_path)
            logError(msg)
            return '*ERROR* ' + msg

        exec_string = 'self.resources["children"]["{0}"]'.format('"]["children"]["'.join(node_path))

        with self.ren_lock:

            # If must rename a Meta info
            if meta:
                exec( 'val = {0}["meta"].get("{1}")'.format(exec_string, meta) )

                if val is None:
                    msg = 'Rename Resource: Cannot find resource meta info `{0}` !'.format(meta)
                    logError(msg)
                    return '*ERROR* ' + msg

                exec( '{0}["meta"]["{1}"] = {0}["meta"]["{2}"]'.format(exec_string, new_name, meta) )
                exec( 'del {0}["meta"]["{1}"]'.format(exec_string, meta) )

                logDebug('Renamed resource meta `{0}:{1}` to `{0}:{2}`.'.format('/'.join(node_path), meta, new_name))

            # If must rename a normal node
            else:
                new_string = 'self.resources["children"]["{0}"]'.format('"]["children"]["'.join(new_path))

                exec( new_string + ' = ' + exec_string )
                exec( 'del ' + exec_string )

                logDebug('Renamed resource path `{0}` to `{1}`.'.format('/'.join(node_path), '/'.join(new_path)))

            # # Write changes.
            self._save()

        return True


    @cherrypy.expose
    def deleteResource(self, res_query):
        '''
        Permanently delete a resource.
        '''
        self._load(v=False)

        # If no resources...
        if not self.resources['children']:
            msg = 'Del Resource: There are no resources defined !'
            logError(msg)
            return '*ERROR* ' + msg

        if ':' in res_query:
            meta      = res_query.split(':')[1]
            res_query = res_query.split(':')[0]
        else:
            meta = ''

        # Find the resource pointer.
        res_p = self.getResource(res_query)

        if not res_p:
            msg = 'Del Resource: Cannot find resource path or ID `{0}` !'.format(res_query)
            logError(msg)
            return '*ERROR* ' + msg

        # Correct node path
        node_path = [p for p in res_p['path'].split('/') if p]

        if not node_path:
            msg = 'Del Resource: Cannot find resource node path `{0}` !'.format(node_path)
            logError(msg)
            return '*ERROR* ' + msg

        exec_string = 'self.resources["children"]["{0}"]'.format('"]["children"]["'.join(node_path))

        # If must delete a Meta info
        if meta:
            exec( 'val = {0}["meta"].get("{1}")'.format(exec_string, meta) )

            if val is None:
                msg = 'Del Resource: Cannot find resource meta info `{0}` !'.format(meta)
                logError(msg)
                return '*ERROR* ' + msg

            exec( 'del {0}["meta"]["{1}"]'.format(exec_string, meta) )
            logDebug('Deleted resource meta `{0}:{1}`.'.format('/'.join(node_path), meta))

        # If must delete a normal node
        else:
            exec( 'del ' + exec_string )
            logDebug('Deleted resource path `{0}`.'.format('/'.join(node_path)))

        # Write changes.
        self._save()

        return True


    @cherrypy.expose
    def findEpname(self, tbname):
        '''
        Calculate EP Name, based on test bed.
        '''
        self._load(v=False)
        # If no resources...
        if not self.resources['children']:
            msg = 'Find Epname: There are no resources defined !'
            logError(msg)
            return '*ERROR* ' + msg

        tbvalue = self.resources['children'].get(tbname)

        if not tbvalue:
            msg = 'Find Epname: Cannot find TestBed `{0}` !'.format(tbname)
            logError(msg)
            return '*ERROR* ' + msg

        ep = tbvalue['meta'].get('epnames')

        if not ep:
            msg = 'Find Epname: TestBed `{0}` does not have any EPs !'.format(tbname)
            logError(msg)
            return '*ERROR* ' + msg

        return ep


# # # Allocation and reservation of resources # # #


    @cherrypy.expose
    def getResourceStatus(self, res_query):
        '''
        Returns the status of a given resource.
        '''
        self._load(v=False)
        # If no resources...
        if not self.resources['children']:
            msg = 'Get Resource: There are no resources defined !'
            logError(msg)
            return '*ERROR* ' + msg

        res_p = self.getResource(res_query)

        if not res_p:
            msg = 'Get Status: Cannot find resource path or ID `{0}` !'.format(res_query)
            logError(msg)
            return '*ERROR* ' + msg

        return res_p.get('status', RESOURCE_FREE)


    @cherrypy.expose
    def allocResource(self, res_query):

        self._load(v=False)
        res_p = _get_res_pointer(self.resources, res_query)

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

        self._load(v=False)
        res_p = _get_res_pointer(self.resources, res_query)

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

        self._load(v=False)
        res_p = _get_res_pointer(self.resources, res_query)

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
