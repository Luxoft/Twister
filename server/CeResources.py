
# File: CeResources.py ; This file is part of Twister.

# version: 2.012

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
Resource Allocator
******************

All functions are exposed and can be accessed using XML-RPC, or the browser.\n
Its role is to manage nodes that represent test-beds and real devices, or SUTs.
"""

import os
import sys
import ast
import copy
import thread

try: import simplejson as json
except: import json

import cherrypy
from lxml import etree
from binascii import hexlify
from cherrypy import _cptools
from mako.template import Template
import time

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print('TWISTER_PATH environment variable is not set! Exiting!')
    exit(1)
if TWISTER_PATH not in sys.path:
    sys.path.append(TWISTER_PATH)

from common.tsclogging import *

RESOURCE_FREE     = 1
RESOURCE_BUSY     = 2
RESOURCE_RESERVED = 3

ROOT_DEVICE = 1
ROOT_SUT    = 2

ROOT_NAMES = {
    ROOT_DEVICE: 'Device', ROOT_SUT: 'SUT'
}

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


def _recursive_refresh_id(node):
    """ refresh ids """

    res_id = False
    while not res_id:
        res_id = hexlify(os.urandom(5))
        # If by any chance, this ID already exists, generate another one!
        if _recursive_find_id(node, res_id, []):
            res_id = False

    node.update([('id', res_id), ])

    if node['children']:
        for c in node['children']:
            node['children'][c] = _recursive_refresh_id(node['children'][c])

    return node


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
            #resource_p.update('path', resource_path)
            del resource_path
        except:
            resource_p = None

    return resource_p


def _get_res_path(parent_node, query):
    '''
    Helper function.
    '''
    query = str(query)

    # If the query is a path
    if '/' in query:
        resource_path = query.split('/')
    # If the query is an ID
    else:
        try:
            resource_path = _recursive_find_id(parent_node, query, [])['path']
        except:
            resource_path = None

    result = None
    if resource_path:
        result = [p for p in resource_path if p]

    return result


def flattenNodes(parent_node, result):
    # The node is valid ?
    if not parent_node:
        return False
    # This node has children ?
    if not parent_node.get('children'):
        return False

    for node in sorted(parent_node['children'].keys()):
        nd = dict(parent_node['children'][node])
        nd['label'] = node
        ch = flattenNodes(parent_node['children'][node], [])
        nd['children'] = ch or []
        result.append(nd)
    return result


def xml_to_res(xml, gparams):
    for folder in xml.xpath('folder'):
        # Create empty resource node
        nd = {'meta': {}, 'id': '', 'children': {}}
        # Populate META properties
        nd['meta'] = {gparam.find('name').text: gparam.find('value').text or '' for gparam in folder.xpath('param')}
        # If the XML node contains an ID, use it; else, create a random ID
        if nd['meta'].get('id'):
            nd['id'] = nd['meta']['id']
            del nd['meta']['id']
        else:
            nd['id'] = hexlify(os.urandom(5))
        # Add children for this node
        nd['children'] = xml_to_res(folder, {})
        gparams[folder.find('fname').text] = nd
    return gparams


def res_to_xml(parent_node, xml):
    # The node is valid ?
    if not parent_node:
        return False
    # This node has children ?
    if not parent_node.get('children'):
        return False

    for node in sorted(parent_node['children'].keys()):
        nd = dict(parent_node['children'][node])

        # Create empty folder
        folder = etree.SubElement(xml, 'folder')
        # Folder fname
        fname = etree.SubElement(folder, 'fname')
        fname.text = node
        # Folder fdesc
        fdesc = etree.SubElement(folder, 'fdesc')

        # The ID is special
        if nd.get('id'):
            tag = etree.SubElement(folder, 'param')
            prop = etree.SubElement(tag, 'name')
            prop.text = 'id'
            val  = etree.SubElement(tag, 'value')
            val.text = nd['id']
            typ  = etree.SubElement(tag, 'type')
            typ.text = 'string'
            desc  = etree.SubElement(tag, 'desc')

        for k, v in nd['meta'].iteritems():
            tag = etree.SubElement(folder, 'param')
            prop = etree.SubElement(tag, 'name')
            prop.text = str(k)
            val  = etree.SubElement(tag, 'value')
            if v:
                val.text = str(v)
            else:
                val.text = ''
            typ  = etree.SubElement(tag, 'type')
            typ.text = 'string'
            desc  = etree.SubElement(tag, 'desc')

        ch = res_to_xml(nd, folder)

    return xml

#

class ResourceAllocator(_cptools.XMLRPCController):

    def __init__(self, project):

        self.project = project

        self.resources = {'version': 0, 'name': '/', 'meta': {}, 'children': {}}
        self.reservedResources = dict()
        self.systems   = {'version': 0, 'name': '/', 'meta': {}, 'children': {}}
        self.acc_lock = thread.allocate_lock() # Task change lock
        self.ren_lock = thread.allocate_lock() # Rename lock
        self.imp_lock = thread.allocate_lock() # Import lock
        self.res_file = '{}/config/resources.json'.format(TWISTER_PATH)
        self.sut_file = '{}/config/systems.json'.format(TWISTER_PATH)
        self._loadedUsers = dict()
        self._load(v=True)




    @cherrypy.expose
    def default(self, *vpath, **params):
        user_agent = cherrypy.request.headers['User-Agent'].lower()
        if 'xmlrpc' in user_agent or 'xml rpc' in user_agent:
            return super(ResourceAllocator, self).default(*vpath, **params)
        # If the connection is not XML-RPC, return the RA main
        output = Template(filename=TWISTER_PATH + '/server/template/ra_main.htm')
        return output.render()

#

    def _load(self, v=False, props={}, force=False):
        # import time
        # t0 = time.time()

        if not force:
            try:
                user_roles = self.userRoles(props)
                user = user_roles.get('user')
                if user in self._loadedUsers:
                    self.systems = self._loadedUsers[user]
                    return True
            except Exception as e:
                if v:
                    logError('RA: There are no devices to load! `{}`!'.format(e))

        deviceStatusChanged = False
        sutStatusChanged = False
        with self.acc_lock:

            if not self.resources['children']:
                self.resources = {'version': 0, 'name': '/', 'meta': {}, 'children': {}}
            if not self.systems['children']:
                self.systems = {'version': 0, 'name': '/', 'meta': {}, 'children': {}}

            try:
                f = open(self.res_file, 'r')
                self.resources = json.load(f)
                f.close() ; del f
                if v:
                    logDebug('RA: Devices loaded successfully.')

                # Check status
                reservedIds = list()
                for u in self.reservedResources:
                    for i in self.reservedResources[u]:
                        reservedIds.append(self.reservedResources[u][i])
                for r in self.resources['children']:
                    try:
                        if (self.resources['children'][r]['status'] == 3
                            and not self.resources['children'][r]['id'] in reservedIds):
                            self.resources['children'][r]['status'] = 1
                            deviceStatusChanged = True
                    except Exception as e:
                        pass
            except Exception as e:
                if v:
                    logError('RA: There are no devices to load! `{}`!'.format(e))
            try:
                f = open(self.sut_file, 'r')
                self.systems = json.load(f)
                f.close() ; del f

                if v:
                    logDebug('RA: Systems root loaded successfully.')

                try:
                    sutsPath = '{}/config/sut/'.format(TWISTER_PATH)
                    sutPaths = [p for p in os.listdir(sutsPath) if os.path.isfile(os.path.join(sutsPath, p))]
                    for sutPath in sutPaths:
                        sutName = '.'.join(['.'.join(sutPath.split('.')[:-1]  + ['system'])])
                        with open(os.path.join(sutsPath, sutPath), 'r') as f:
                            self.systems['children'].update([(sutName, json.load(f)), ])
                except Exception as e:
                    if v:
                        logError('_load ERROR:: {}'.format(e))

                # Get the user rpyc connection connection
                try:
                    user_roles = self.userRoles(props)
                    user = user_roles.get('user')
                    userConn = self.project.rsrv.service._findConnection(user,
                                                            ['127.0.0.1', 'localhost'], 'client')
                    userConn = self.project.rsrv.service.conns[userConn]['conn']
                    userSuts = copy.deepcopy(userConn.root.get_suts())
                    if userSuts:
                        self.systems['children'].update(userSuts)
                    self._loadedUsers.update([(user, self.systems), ])
                except Exception as e:
                    if v:
                        logError('_load ERROR:: {}'.format(e))

                # Check status
                reservedIds = list()
                for u in self.reservedResources:
                    for i in self.reservedResources[u]:
                        reservedIds.append(self.reservedResources[u][i])
                for r in self.systems['children']:
                    try:
                        if (self.systems['children'][r]['status'] == 3
                            and not self.systems['children'][r]['id'] in reservedIds):
                            self.systems['children'][r]['status'] = 1
                            sutStatusChanged = True
                    except Exception as e:
                        pass
                if v:
                    logDebug('RA: Systems loaded successfully.')
            except Exception as e:
                if v:
                    logError('RA: There are no SUTs to load! `{}`!'.format(e))
        if deviceStatusChanged:
            self._save(props=props)
        if sutStatusChanged:
            self._save(ROOT_SUT, props=props)
        # t1 = time.time()
        # logDebug('|||||||||||||_load time:: ', t1-t0)
        return True


    def _save(self, root_id=ROOT_DEVICE, props={}):
        '''
        Function used to write the changes on HDD.
        The save is separate for Devices and SUTs, so the version is not incremented
        for both, before saving.
        '''

        # Write changes, using the Access Lock.
        with self.acc_lock:

            if root_id == ROOT_DEVICE:
                v = self.resources.get('version', 0) + 1
                logDebug('Saving {} file, version `{}`.'.format(ROOT_NAMES[root_id], v))
                self.resources['version'] = v
                f = open(self.res_file, 'w')
                json.dump(self.resources, f, indent=4)
                f.close() ; del f

            else:
                try:
                    user_roles = self.userRoles(props)
                    user = user_roles.get('user')
                    if user in self._loadedUsers:
                        self.systems = self._loadedUsers[user]
                except Exception as e:
                    if v:
                        logError('Save ERROR: `{}`!'.format(e))

                v = self.systems.get('version', 0) + 1
                self.systems['version'] = v
                logDebug('Saving {} file, version `{}`.'.format(ROOT_NAMES[root_id], v))

                systemsChildren = copy.deepcopy(self.systems['children'])
                self.systems['children'] = dict()

                f = open(self.sut_file, 'w')
                json.dump(self.systems, f, indent=4)
                f.close() ; del f

                self.systems['children'] = copy.deepcopy(systemsChildren)
                del systemsChildren

                userSuts = list()
                for child in self.systems['children']:
                    # Check where to save (ce / user)
                    childPath = '{}/config/sut/{}.json'.format(TWISTER_PATH, '.'.join(child.split('.')[:-1]))
                    if child.split('.')[-1] == 'system':
                        with open(childPath, 'w') as f:
                            json.dump(self.systems['children'][child], f, indent=4)
                    else:
                        userSuts.append(('.'.join(child.split('.')[:-1]), self.systems['children'][child]))

                if userSuts:
                    # Get the user rpyc connection connection
                    try:
                        user_roles = self.userRoles(props)
                        user = user_roles.get('user')

                        # update loaded users systems
                        self._loadedUsers.update([(user, self.systems), ])

                        userConn = self.project.rsrv.service._findConnection(user,
                                                                    ['127.0.0.1', 'localhost'], 'client')
                        userConn = self.project.rsrv.service.conns[userConn]['conn']
                        userConn.root.save_suts(userSuts)
                    except Exception as e:
                        logError('Saving ERROR:: `{}`.'.format(e))

        return True


    @cherrypy.expose
    def echo(self, msg):
        '''
        Simple echo function, for testing connection.
        '''
        logDebug('Echo: {}'.format(msg))
        return 'RA reply: {}'.format(msg)


    @cherrypy.expose
    def tree(self, root_id=ROOT_DEVICE, props={}, *arg, **kw):
        '''
        Return the structure, list based.
        '''
        self._load(v=False, props=props)

        try: root_id = int(root_id)
        except: root_id=ROOT_DEVICE

        if root_id == ROOT_DEVICE:
            root = self.resources
        else:
            root = self.systems

        result = [{'name': '/', 'id': '1', 'meta': {}, 'children': flattenNodes(root, [])}]
        cherrypy.response.headers['Content-Type']  = 'application/json; charset=utf-8'
        cherrypy.response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        cherrypy.response.headers['Pragma']  = 'no-cache'
        cherrypy.response.headers['Expires'] = 0
        return json.dumps(result, indent=4, sort_keys=True)


    @cherrypy.expose
    def import_xml(self, xml_file, root_id=ROOT_DEVICE, props={}):
        '''
        Import one XML file.
        WARNING! This erases everything!
        '''
        self._load(v=False, props=props)

        if not os.path.isfile(xml_file):
            logError('Import XML: XML file `{}` does not exist!'.format(xml_file))
            return False

        params_xml = etree.parse(xml_file)

        with self.imp_lock:
            if root_id == ROOT_DEVICE:
                try:
                    self.resources = xml_to_res(params_xml, {})
                    # self.resources = {'version': 0, 'name': '/', 'id': '1', 'meta': {},
                    #                     'children': xml_to_res(params_xml, {})}
                except Exception as e:
                    logError('Import XML: Exception `{}`.'.format(e))
                    return False
            else:
                try:
                    # default save to user path
                    sutName = os.path.basename(xml_file).split('.')[:-1]
                    if not sutName:
                        sutName = [os.path.basename(xml_file)]
                    sutName = '.'.join(sutName + ['user'])
                    if sutName in self.systems['children']:
                        sutName = '{}{}'.format(sutName, time.time())
                    sutContent = xml_to_res(params_xml, {})
                    sutContent = sutContent.popitem()[1]
                    sutContent.update([('path', sutName), ])
                    sutContent = _recursive_refresh_id(sutContent)
                    self.systems['children'].update([(sutName, sutContent), ])
                except Exception as e:
                    logError('Import XML: Exception `{}`.'.format(e))
                    return False

        # Write changes for Device or SUT
        self._save(root_id, props)

        root_name = ROOT_NAMES[root_id]
        #logDebug('All {} are now overwritten! Created `{}` major nodes, with children.'.format(root_name, len(result['children'])))
        return True


    @cherrypy.expose
    def export_xml(self, xml_file, root_id=ROOT_DEVICE, root=None, props={}):
        '''
        Export as XML file.
        '''
        self._load(v=False, props=props)

        try:
            f = open(xml_file, 'w')
        except:
            logError('Export XML: XML file `{}` cannot be written!'.format(xml_file))
            return False

        if root_id == ROOT_DEVICE:
            _root = self.resources
        elif root_id == ROOT_SUT:
            _root = self.systems
        elif root:
            _root = root

        xml = etree.Element('root')
        result = res_to_xml(_root, xml)
        f.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n\n')
        f.write(etree.tostring(xml, pretty_print=True))
        f.close()

        return True


    @cherrypy.expose
    def import_sut_xml(self, xml_file, props={}):
        '''
        Import one sut XML file.
        '''
        return self.import_xml(xml_file, ROOT_SUT, props)


    @cherrypy.expose
    def export_sut_xml(self, xml_file, query, props={}):
        '''
        Export as XML file.
        '''
        res_path = _get_res_path(self.systems, query)
        res_pointer = _get_res_pointer(self.systems, ''.join('/' + res_path[0]))
        root = {'version': 0, 'name': '/', 'meta': {}, 'children': {res_path[0]: res_pointer}}
        return self.export_xml(xml_file, None, root, props)


    def userRoles(self, props={}):
        # Check the username from CherryPy connection
        try: user = cherrypy.session.get('username')
        except: user = ''

        # Fallback
        if not user:
            user = props.get('__user', '')

        user_roles = self.project.authenticate(user)
        default = {'user': user, 'roles': [], 'groups': []}
        if not user_roles: return default
        user_roles.update({'user': user})
        return user_roles

#

    @cherrypy.expose
    def getResource(self, query, root_id=ROOT_DEVICE, flatten=True, props={}):
        '''
        Show all the properties, or just 1 property of a resource.
        Must provide a Resource ID, or a Query.
        The function is used for both Devices and SUTs, by providing the ROOT ID.
        '''
        self._load(v=False, props=props)

        # If the root is not provided, use the default root
        if root_id == ROOT_DEVICE:
            resources = self.resources
        else:
            resources = self.systems

        root_name = ROOT_NAMES[root_id]

        # If no resources...
        if not resources['children']:
            # Return default structure for root
            if query == '/':
                return {'path': '', 'meta': resources.get('meta', {}), 'id': '1', 'children': []}

            msg = 'Get {}: There are no devices defined !'.format(root_name)
            logError(msg)
            return '*ERROR* ' + msg

        if not query:
            msg = 'Get {}: Cannot get a null resource !'.format(root_name)
            logError(msg)
            return '*ERROR* ' + msg

        query = str(query)

        # If the query asks for a specific Meta Tag
        if query.count(':') > 1:
            msg = 'Get {}: Invalid query ! Cannot access more than 1 meta info !'.format(root_name)
            logError(msg)
            return '*ERROR* ' + msg

        if ':' in query:
            meta  = query.split(':')[1]
            query = query.split(':')[0]
        else:
            meta = ''

        # If the query is an ID
        if '/' not in query:
            result = _recursive_find_id(resources, query, [])
            if not result:
                return False

        # If the query is a slash string query
        else:
            parts = [q for q in query.split('/') if q]
            result = resources

            # If this is a normal resource
            if root_id == ROOT_DEVICE:
                for part in parts:
                    if not result: return False
                    result = result['children'].get(part)
            # If this is a SUT
            else:
                for part in parts:
                    if not result: return False
                    res = result['children'].get(part)
                    if not res:
                        # Ok, this might be a Device path, instead of SUT path!
                        tb_id = result['meta'].get('_id')
                        # If this SUT doesn't have a Device ID assigned, bye bye!
                        if not tb_id: return False
                        res_data = _recursive_find_id(self.resources, tb_id, [])
                        # If the Device ID is invalid, bye bye!
                        if not res_data: return False
                        # Find out the Device path from Resources and add the rest of the parts
                        link_path = '/' + '/'.join(res_data.get('path', '')) + '/' + part
                        result = self.getResource(link_path, flatten=False)
                        # After this, scan the next PART from PARTS
                    else:
                        result = res

            if not result: return False
            # Delete empty node paths
            result['path'] = [p for p in parts if p]

        result = dict(result)

        if not meta:
            # Flatten the children ?
            if flatten:
                result['children'] = sorted([result['children'][node]['id'] for
                                     node in result.get('children') or []],
                                     key=lambda node: node.lower())
            result['path'] = '/'.join(result.get('path', ''))
            return result
        else:
            ret = result['meta'].get(meta, '')
            if ret:
                return ret
            # If this is a normal resource
            if root_id == ROOT_DEVICE:
                return ret
            else:
                # Ok, this might be a Device ID, instead of SUT ID!
                tb_id = result['meta'].get('_id')
                # If this SUT doesn't have a Device ID assigned, bye bye!
                if not tb_id: return ''
                return self.getResource(tb_id +':'+ meta)


    @cherrypy.expose
    def getSut(self, query, props={}):
        '''
        Show all the properties, or just 1 property of a SUT.
        Must provide a SUT ID, or a SUT Path.
        '''
        return self.getResource(query, ROOT_SUT, props=props)

#

    @cherrypy.expose
    def setResource(self, name, parent=None, props={}, root_id=ROOT_DEVICE):
        '''
        Create or change a resource, using a name, a parent Path or ID and some properties.
        The function is used for both Devices and SUTs, by providing the ROOT ID.
        '''
        self._load(v=False, props=props)

        user_roles = self.userRoles(props)

        # If the root is not provided, use the default root
        if root_id == ROOT_DEVICE:
            if 'CHANGE_TESTBED' not in user_roles.get('roles', []):
                logDebug('Privileges ERROR! Username `{user}` cannot use Set Resource!'.format(**user_roles))
                return False
            resources = self.resources
        else:
            if 'CHANGE_SUT' not in user_roles.get('roles', []):
                logDebug('Privileges ERROR! Username `{user}` cannot use Set SUT!'.format(**user_roles))
                return False
            resources = self.systems

        root_name = ROOT_NAMES[root_id]

        # If this is the root resource, update the properties
        if name == '/' and parent == '/':
            if isinstance(props, dict):
                pass
            elif (isinstance(props, str) or isinstance(props, unicode)):
                props = props.strip()
                try:
                    props = ast.literal_eval(props)
                except Exception as e:
                    msg = 'Set {}: Cannot parse properties: `{}`, `{}` !'.format(root_name, props, e)
                    logError(msg)
                    return '*ERROR* ' + msg
            else:
                msg = 'Set {}: Invalid properties `{}` !'.format(root_name, props)
                logError(msg)
                return '*ERROR* ' + msg

            resources['meta'].update(props)
            # Write changes for Device or SUT
            self._save(root_id, props)
            logDebug('Set {}: Updated ROOT with properties: `{}`.'.format(root_name, props))
            return True

        if parent == '/' or parent == '1': # can alsow be 1
            parent_p = _get_res_pointer(resources, parent)

            if (root_id == ROOT_SUT and
                    (not name.split('.')[-1] == 'user' and not name.split('.')[-1] == 'system')):
                name = '.'.join([name, 'user'])
        else:
            parent_p = self._getReservedResource(parent, props, root_id)

        if not parent_p:
            msg = 'Set {}: Cannot access parent path or ID `{}` !'.format(root_name, parent)
            logError(msg)
            return '*ERROR* ' + msg

        if '/' in name:
            logDebug('Set {}: Stripping slash characters from `{}`...'.format(root_name, name))
            name = name.replace('/', '')

        if isinstance(props, dict):
            pass
        elif (isinstance(props, str) or isinstance(props, unicode)):
            props = props.strip()
            try:
                props = ast.literal_eval(props)
            except Exception as e:
                msg = 'Set {}: Cannot parse properties: `{}`, `{}` !'.format(root_name, props, e)
                logError(msg)
                return '*ERROR* ' + msg
        else:
            msg = 'Set {}: Invalid properties `{}` !'.format(root_name, props)
            logError(msg)
            return '*ERROR* ' + msg

        if not 'children' in parent_p:
            parent_p['children'] = {}

        if '/' in parent:
            for c in [p for p in parent.split('/') if p][1:]:
                parent_p = parent_p['children'][c]
        else:
            resource_path = _recursive_find_id(parent_p, parent, [])['path']
            for c in resource_path:
                parent_p = parent_p['children'][c]

        # try: del parent_p['path']
        # except: pass

        # Make a copy, to compare the changes at the end
        #old_parent = copy.deepcopy(parent_p)

        # If the resource exists, patch the new properties!
        if name in parent_p['children']:
            if parent == '/' or parent == '1':
                child_p = self._getReservedResource('/' + name, props, root_id)
            else:
                child_p = parent_p['children'][name]

            if not child_p:
                return False

            old_child = copy.deepcopy(child_p)

            child_p['meta'].update(props)

            if old_child != child_p:
                self._save(root_id, props)

            # if old_parent != parent_p:
            #     #self._save(root_id)
            #     logDebug('Updated {} `{}`, id `{}` : `{}`.'.format(root_name, name, child_p['id'], props))
            # else:
            #     logDebug('No changes have been made to {} `{}`, id `{}`.'.format(root_name, name, child_p['id']))

            return True

        # If the resource is new, create it.
        else:
            #parent_p = _get_res_pointer(parent_p, parent)

            res_id = False
            while not res_id:
                res_id = hexlify(os.urandom(5))
                # If by any chance, this ID already exists, generate another one!
                if _recursive_find_id(resources, res_id, []):
                    res_id = False

            parent_p['children'][name] = {'id': res_id, 'meta': props, 'children': {}}

            # Write changes for Device or SUT
            self._save(root_id, props)
            logDebug('Created {} `{}`, id `{}` : `{}`.'.format(root_name, name, res_id, props))
            return res_id


    @cherrypy.expose
    def setSut(self, name, parent=None, props={}):
        '''
        Create or change a SUT, using a name, a parent Path or ID and some properties.
        '''
        return self.setResource(name, parent, props, ROOT_SUT)


    @cherrypy.expose
    def renameResource(self, res_query, new_name, props={}, root_id=ROOT_DEVICE):
        '''
        Rename a resource.
        '''
        self._load(v=False, props=props)

        user_roles = self.userRoles(props)

        # If the root is not provided, use the default root
        if root_id == ROOT_DEVICE:
            if 'CHANGE_TESTBED' not in user_roles.get('roles', []):
                logDebug('Privileges ERROR! Username `{user}` cannot use Rename Resource!'.format(**user_roles))
                return False
            resources = self.resources
        else:
            if 'CHANGE_SUT' not in user_roles.get('roles', []):
                logDebug('Privileges ERROR! Username `{user}` cannot use Rename SUT!'.format(**user_roles))
                return False
            resources = self.systems

        root_name = ROOT_NAMES[root_id]

        # If no resources...
        if not resources['children']:
            msg = 'Rename {}: There are no resources defined !'.format(root_name)
            logError(msg)
            return '*ERROR* ' + msg

        if '/' in new_name:
            msg = 'Rename {}: New resource name cannot contain `/` !'.format(root_name)
            logError(msg)
            return '*ERROR* ' + msg

        if ':' in new_name:
            msg = 'Rename {}: New resource name cannot contain `:` !'.format(root_name)
            logError(msg)
            return '*ERROR* ' + msg

        if ':' in res_query:
            meta      = res_query.split(':')[1]
            res_query = res_query.split(':')[0]
        else:
            meta = ''

        # Find the resource pointer.
        # if root_id == ROOT_DEVICE:
        #     res_p = self.getResource(res_query)
        # else:
        #     res_p = self.getSut(res_query)

        # if not res_p:
        #     msg = 'Rename {}: Cannot find resource path or ID `{}` !'.format(root_name, res_query)
        #     logError(msg)
        #     return '*ERROR* ' + msg

        res_p = self._getReservedResource(res_query, props, root_id)
        if not res_p:
            msg = 'Rename {}: Cannot access reserved resource, path or ID `{}` !'.format(root_name, res_query)
            logError(msg)
            return '*ERROR* ' + msg

        # Correct node path
        res_path = _get_res_path(resources, res_query)
        node_path = [p for p in res_path if p]
        # Renamed node path
        if (not meta and len(node_path) == 1 and root_id == ROOT_SUT and
                    (not new_name.split('.')[-1] == 'user' and not new_name.split('.')[-1] == 'system')):
            new_name = '.'.join([new_name, 'user'])
        new_path = list(node_path) ; new_path[-1] = new_name

        if not node_path:
            msg = 'Rename {}: Cannot find resource node path `{}` !'.format(root_name, node_path)
            logError(msg)
            return '*ERROR* ' + msg

        if node_path == new_path:
            logDebug('No changes have been made to {} `{}`.'.format(root_name, new_name))
            return True

        # Must use the real pointer instead of `resource` pointer in order to update the real data
        # if root_id == ROOT_DEVICE:
        #     exec_string = 'self.resources["children"]["{}"]'.format('"]["children"]["'.join(node_path))
        # else:
        #     exec_string = 'self.systems["children"]["{}"]'.format('"]["children"]["'.join(node_path))
        if node_path[1:]:
            exec_string = 'res_p["children"]["{}"]'.format('"]["children"]["'.join(node_path[1:]))
        else:
            exec_string = 'res_p'

        with self.ren_lock:

            # If must rename a Meta info
            if meta:
                exec( 'val = {}["meta"].get("{}")'.format(exec_string, meta) )

                if val is None:
                    msg = 'Rename {}: Cannot find resource meta info `{}` !'.format(root_name, meta)
                    logError(msg)
                    return '*ERROR* ' + msg

                exec( '{0}["meta"]["{1}"] = {0}["meta"]["{2}"]'.format(exec_string, new_name, meta) )
                exec( 'del {}["meta"]["{}"]'.format(exec_string, meta) )

                logDebug('Renamed {0} meta `{1}:{2}` to `{1}:{3}`.'.format(root_name, '/'.join(node_path), meta, new_name))

            # If must rename a normal node
            else:
                # Must use the real pointer instead of `resource` pointer in order to update the real data
                # if root_id == ROOT_DEVICE:
                #     new_string = 'self.resources["children"]["{}"]'.format('"]["children"]["'.join(new_path))
                # else:
                #     new_string = 'self.systems["children"]["{}"]'.format('"]["children"]["'.join(new_path))
                if new_path[1:]:
                    new_string = 'res_p["children"]["{}"]'.format('"]["children"]["'.join(new_path[1:]))
                    exec( new_string + ' = ' + exec_string )
                    exec( 'del ' + exec_string )
                else:
                    res_p['path'] = new_name

                logDebug('rename:: ', self.reservedResources)

                #exec( new_string + ' = ' + exec_string )
                #exec( 'del ' + exec_string )

                logDebug('Renamed {} path `{}` to `{}`.'.format(root_name, '/'.join(node_path), '/'.join(new_path)))

        # Write changes.
        #self._save(root_id, props)

        return True


    @cherrypy.expose
    def renameSut(self, res_query, new_name, props={}):
        '''
        Rename a SUT.
        '''
        return self.renameResource(res_query, new_name, props, ROOT_SUT)


    @cherrypy.expose
    def deleteResource(self, res_query, props={}, root_id=ROOT_DEVICE):
        '''
        Permanently delete a resource.
        '''
        self._load(v=False, props=props)

        user_roles = self.userRoles(props)

        # If the root is not provided, use the default root
        if root_id == ROOT_DEVICE:
            if 'CHANGE_TESTBED' not in user_roles.get('roles', []):
                logDebug('Privileges ERROR! Username `{user}` cannot use Delete Resource!'.format(**user_roles))
                return False
            resources = self.resources
        else:
            if 'CHANGE_SUT' not in user_roles.get('roles', []):
                logDebug('Privileges ERROR! Username `{user}` cannot use Delete SUT!'.format(**user_roles))
                return False
            resources = self.systems

        root_name = ROOT_NAMES[root_id]

        # If no resources...
        if not resources['children']:
            msg = 'Del {}: There are no resources defined !'.format(root_name)
            logError(msg)
            return '*ERROR* ' + msg

        if ':' in res_query:
            meta      = res_query.split(':')[1]
            res_query = res_query.split(':')[0]
        else:
            meta = ''

        # Check if is reserved
        res_path = _get_res_path(resources, res_query)
        res_pointer = _get_res_pointer(resources, ''.join('/' + res_path[0]))

        user = user_roles.get('user')
        isReservedForUser = [False, True][res_pointer.get('status', RESOURCE_FREE) == RESOURCE_RESERVED and
                                res_pointer['id'] in self.reservedResources[user]]
        if not isReservedForUser:
            reservedResourceIds = list()
            for userReservedResourceIds in [self.reservedResources[u].keys() for u in self.reservedResources]:
                reservedResourceIds += userReservedResourceIds
            isReserved = [False, True][res_pointer.get('status', RESOURCE_FREE) == RESOURCE_RESERVED and
                            res_pointer['id'] in reservedResourceIds]
            if isReserved:
                msg = 'Del {}: Resource reserved, path or ID `{}` !'.format(root_name, res_query)
                logError(msg)
                return '*ERROR* ' + msg

        # Find the resource pointer.
        if root_id == ROOT_DEVICE:
            res_p = self.getResource(res_query, props=props)
        else:
            res_p = self.getSut(res_query, props=props)

        if not res_p:
            msg = 'Del {}: Cannot find resource path or ID `{}` !'.format(root_name, res_query)
            logError(msg)
            return '*ERROR* ' + msg

        # Correct node path
        node_path = [p for p in res_p['path'].split('/') if p]

        if not node_path:
            msg = 'Del {}: Cannot find resource node path `{}` !'.format(root_name, node_path)
            logError(msg)
            return '*ERROR* ' + msg

        # Must use the real pointer instead of `resource` pointer in order to update the real data
        if root_id == ROOT_DEVICE:
            exec_string = 'self.resources["children"]["{}"]'.format('"]["children"]["'.join(node_path))
        else:
            exec_string = 'self.systems["children"]["{}"]'.format('"]["children"]["'.join(node_path))

        # If must delete a Meta info
        if meta:
            exec( 'val = {}["meta"].get("{}")'.format(exec_string, meta) )

            if val is None:
                msg = 'Del {}: Cannot find resource meta info `{}` !'.format(root_name, meta)
                logError(msg)
                return '*ERROR* ' + msg

            exec( 'del {}["meta"]["{}"]'.format(exec_string, meta) )
            logDebug('Deleted {} meta `{}:{}`.'.format(root_name, '/'.join(node_path), meta))

        # If must delete a normal node
        else:
            exec( 'del ' + exec_string )
            logDebug('Deleted {} path `{}`.'.format(root_name, '/'.join(node_path)))

        # Write changes.
        self._save(root_id, props)

        # Delete file
        if not meta and len(node_path) == 1 and root_id == ROOT_SUT:
            if node_path[0].split('.')[-1] == 'system':
                os.remove('{}/config/sut/{}.json'.format(TWISTER_PATH,
                                                            '.'.join(node_path[0].split('.')[:-1])))
            else:
                # Get the user rpyc connection connection
                try:
                    #user = user_roles.get('user')
                    userConn = self.project.rsrv.service._findConnection(user,
                                                                ['127.0.0.1', 'localhost'], 'client')
                    userConn = self.project.rsrv.service.conns[userConn]['conn']
                    userConn.root.delete_sut('.'.join(node_path[0].split('.')[:-1]))
                except Exception as e:
                    logError('Saving ERROR:: `{}`.'.format(e))

        return True


    @cherrypy.expose
    def deleteSut(self, res_query, props={}):
        '''
        Permanently delete a SUT.
        '''
        return self.deleteResource(res_query, props, ROOT_SUT)


    @cherrypy.expose
    def isSutReserved(self, res_query):
        """ returns the user or false """

        return self.isResourceReserved(res_query, ROOT_SUT)


    @cherrypy.expose
    def reserveSut(self, res_query, props={}):
        '''
        Reserve a SUT.
        '''
        return self.reserveResource(res_query, props, ROOT_SUT)


    @cherrypy.expose
    def saveReservedSutAs(self, name, res_query, props={}):
        '''
        Save a reserved SUT as.
        '''
        return self.saveReservedResourceAs(name, res_query, props, ROOT_SUT)


    @cherrypy.expose
    def saveReservedSut(self, res_query, props={}):
        '''
        Save a reserved SUT.
        '''
        return self.saveReservedResource(res_query, props, ROOT_SUT)


    @cherrypy.expose
    def saveAndReleaseReservedSut(self, res_query, props={}):
        '''
        Save a reserved SUT.
        '''
        return self.saveAndReleaseReservedResource(res_query, props, ROOT_SUT)


    @cherrypy.expose
    def discardAndReleaseReservedSut(self, res_query, props={}):
        '''
        Discard a reserved SUT.
        '''
        return self.discardAndReleaseReservedResource(res_query, props, ROOT_SUT)


# # # Allocation and reservation of resources # # #


    def _getReservedResource(self, res_query, props={}, root_id=ROOT_DEVICE):
        '''
        Returns the reserved resource.
        '''

        if root_id == ROOT_DEVICE:
            resources = self.resources
        else:
            resources = self.systems

        # If no resources...
        if not resources['children']:
            msg = 'Get reserved resource: There are no resources defined !'
            logError(msg)
            return False

        user_roles = self.userRoles(props)
        user = user_roles.get('user')

        if ':' in res_query:
            res_query = res_query.split(':')[0]

        res_path = _get_res_path(resources, res_query)
        if not res_path:
            if '/' in res_query:
                res_path = [p for p in res_path.split('/') if p]
            else:
                for p in self.reservedResources[user]:
                    res_path = _get_res_path(self.reservedResources[user][p], res_query)

                    if res_path:
                        self.reservedResources[user][p]['path'] = res_path
                        return self.reservedResources[user][p]

        res_pointer = _get_res_pointer(resources, ''.join('/' + res_path[0]))

        if not res_pointer:
            msg = 'Get reserved resource: Cannot find resource path or ID `{}` !'.format(res_query)
            logError(msg)
            return False

        res_pointer.update([('path', [res_path[0]]), ])

        isReservedForUser = [False, True][res_pointer.get('status', RESOURCE_FREE) == RESOURCE_RESERVED and
                                res_pointer['id'] in self.reservedResources[user]]
        if not isReservedForUser:
            msg = 'Get reserved resource: Cannot find reserved resource path or ID `{}` !'.format(res_query)
            logError(msg)
            return False

        self.reservedResources[user][res_pointer['id']]['path'] = '/'.join(self.reservedResources[user][res_pointer['id']].get('path', ''))

        return self.reservedResources[user][res_pointer['id']]


    @cherrypy.expose
    def isResourceReserved(self, res_query, root_id=ROOT_DEVICE):
        """ returns the user or false """

        if root_id == ROOT_DEVICE:
            resources = self.resources
        else:
            resources = self.systems

        # If no resources...
        if not resources['children']:
            msg = 'Is resource reserved: There are no resources defined !'
            logError(msg)
            return False

        if ':' in res_query:
            res_query = res_query.split(':')[0]

        res_path = _get_res_path(resources, res_query)
        res_pointer = _get_res_pointer(resources, ''.join('/' + res_path[0]))

        if not res_pointer:
            msg = 'Is resource reserved: Cannot find resource path or ID `{}` !'.format(res_query)
            logError(msg)
            return False

        res_pointer.update([('path', [res_path[0]]), ])

        reservedForUser = [u for u in self.reservedResources if res_pointer['id'] in self.reservedResources[u]]
        if len(reservedForUser) == 1:
            reservedForUser = reservedForUser[0]
        else:
            #msg = 'Is resource reserved: reserved for `{}` !'.format(reservedForUser)
            #logError(msg)
            return False

        if not reservedForUser:
            msg = 'Is resource reserved: Cannot find reserved resource path or ID `{}` !'.format(res_query)
            logError(msg)
            return False

        return reservedForUser


    @cherrypy.expose
    def reserveResource(self, res_query, props={}, root_id=ROOT_DEVICE):
        """  """
        self._load(v=False, props=props)

        if root_id == ROOT_DEVICE:
            resources = self.resources
        else:
            resources = self.systems

        # If no resources...
        if not resources['children']:
            msg = 'Reserve resource: There are no resources defined !'
            logError(msg)
            return False

        if ':' in res_query:
            res_query = res_query.split(':')[0]

        res_path = _get_res_path(resources, res_query)
        res_pointer = _get_res_pointer(resources, ''.join('/' + res_path[0]))

        if not res_pointer:
            msg = 'Reserve Resource: Cannot find resource path or ID `{}` !'.format(res_query)
            logError(msg)
            return False

        res_pointer.update([('path', [res_path[0]]), ])

        if res_pointer.get('status', None) == RESOURCE_RESERVED:
            msg = 'Reserve Resource: Cannot allocate ! The resource is already busy !'
            logError(msg)
            return False

        res_pointer.update([('status', RESOURCE_RESERVED), ])
        # Write changes.
        self._save(root_id, props)

        user_roles = self.userRoles(props)
        user = user_roles.get('user')
        if user in self.reservedResources:
            self.reservedResources[user].update([(res_pointer['id'], copy.deepcopy(res_pointer)), ])
        else:
            self.reservedResources.update([(user, {res_pointer['id']: copy.deepcopy(res_pointer)}), ])

        return RESOURCE_RESERVED


    @cherrypy.expose
    def saveAndReleaseReservedResource(self, res_query, props={}, root_id=ROOT_DEVICE):
        """  """
        self._load(v=False, props=props)

        if root_id == ROOT_DEVICE:
            resources = self.resources
        else:
            resources = self.systems

        # If no resources...
        if not resources['children']:
            msg = 'Save and release reserved resource: There are no resources defined !'
            logError(msg)
            return False

        if ':' in res_query:
            res_query = res_query.split(':')[0]

        res_path = _get_res_path(resources, res_query)
        res_pointer = _get_res_pointer(resources, ''.join('/' + res_path[0]))

        if not res_pointer:
            msg = 'Save and release resource: Cannot find resource path or ID `{}` !'.format(res_query)
            logError(msg)
            return False

        res_pointer.update([('path', [res_path[0]]), ])

        user_roles = self.userRoles(props)
        user = user_roles.get('user')

        try:
            _res_pointer = self.reservedResources[user].pop(res_pointer['id'])
            if not isinstance(_res_pointer['path'], list):
                _res_pointer['path'] = _res_pointer['path'].split('/')

            # Check for modifications
            if res_pointer != _res_pointer:
                child = None
                for c in resources['children']:
                    if resources['children'][c]['id'] == _res_pointer['id']:
                        child = c
                if not child == _res_pointer['path'][0]:
                    resources['children'].pop(child)

                    # Delete file
                    if child.split('.')[-1] == 'system':
                        os.remove('{}/config/sut/{}.json'.format(TWISTER_PATH,
                                                                    '.'.join(child.split('.')[:-1])))
                    else:
                        # Get the user rpyc connection connection
                        try:
                            #user = user_roles.get('user')
                            userConn = self.project.rsrv.service._findConnection(user,
                                                                        ['127.0.0.1', 'localhost'], 'client')
                            userConn = self.project.rsrv.service.conns[userConn]['conn']
                            userConn.root.delete_sut('.'.join(child.split('.')[:-1]))
                        except Exception as e:
                            logError('Save and release resource ERROR:: `{}`.'.format(e))

            _res_pointer.update([('status', RESOURCE_FREE), ])
            resources['children'].update([(_res_pointer['path'][0], _res_pointer), ])
            #resources['children'].update([(res_path[0], _res_pointer), ])

            # Check for modifications
            if res_pointer != _res_pointer:
                # Write changes.
                self._save(root_id, props)

            if not self.reservedResources[user]:
                self.reservedResources.pop(user)
        except Exception as e:
            msg = 'Save and release resource: `{}` !'.format(e)
            logError(msg)
            return False

        return RESOURCE_FREE


    @cherrypy.expose
    def saveReservedResource(self, res_query, props={}, root_id=ROOT_DEVICE):
        """  """
        self._load(v=False, props=props)

        if root_id == ROOT_DEVICE:
            resources = self.resources
        else:
            resources = self.systems

        # If no resources...
        if not resources['children']:
            msg = 'Save reserved resource: There are no resources defined !'
            logError(msg)
            return False

        if ':' in res_query:
            res_query = res_query.split(':')[0]

        res_path = _get_res_path(resources, res_query)
        res_pointer = _get_res_pointer(resources, ''.join('/' + res_path[0]))

        if not res_pointer:
            msg = 'Save reserved resource: Cannot find resource path or ID `{}` !'.format(res_query)
            logError(msg)
            return False

        res_pointer.update([('path', [res_path[0]]), ])

        user_roles = self.userRoles(props)
        user = user_roles.get('user')

        try:
            _res_pointer = copy.deepcopy(self.reservedResources[user][res_pointer['id']])
            if not isinstance(_res_pointer['path'], list):
                _res_pointer['path'] = _res_pointer['path'].split('/')

            # Check for modifications
            if res_pointer != _res_pointer:
                child = None
                for c in resources['children']:
                    if resources['children'][c]['id'] == _res_pointer['id']:
                        child = c
                if not child == _res_pointer['path'][0]:
                    resources['children'].pop(child)

                    # Delete file
                    if child.split('.')[-1] == 'system':
                        os.remove('{}/config/sut/{}.json'.format(TWISTER_PATH,
                                                                    '.'.join(child.split('.')[:-1])))
                    else:
                        # Get the user rpyc connection connection
                        try:
                            #user = user_roles.get('user')
                            userConn = self.project.rsrv.service._findConnection(user,
                                                                        ['127.0.0.1', 'localhost'], 'client')
                            userConn = self.project.rsrv.service.conns[userConn]['conn']
                            userConn.root.delete_sut('.'.join(child.split('.')[:-1]))
                        except Exception as e:
                            logError('Save resource ERROR:: `{}`.'.format(e))

            resources['children'].update([(_res_pointer['path'][0], _res_pointer), ])

            # Check for modifications
            if res_pointer != _res_pointer:
                # Write changes.
                self._save(root_id, props)
        except Exception as e:
            msg = 'Save reserved resource: `{}` !'.format(e)
            logError(msg)
            return False

        return RESOURCE_RESERVED


    @cherrypy.expose
    def saveReservedResourceAs(self, name, res_query, props={}, root_id=ROOT_DEVICE):
        """  """
        self._load(v=False, props=props)

        if root_id == ROOT_DEVICE:
            resources = self.resources
        else:
            resources = self.systems

        # If no resources...
        if not resources['children']:
            msg = 'Save reserved resource as: There are no resources defined !'
            logError(msg)
            return False

        if ':' in res_query:
            res_query = res_query.split(':')[0]

        res_path = _get_res_path(resources, res_query)
        res_pointer = _get_res_pointer(resources, ''.join('/' + res_path[0]))

        if not res_pointer:
            msg = 'Save reserved resource as: Cannot find resource path or ID `{}` !'.format(res_query)
            logError(msg)
            return False

        res_pointer.update([('path', [res_path[0]]), ])

        user_roles = self.userRoles(props)
        user = user_roles.get('user')

        try:
            name = '.'.join([name, 'user'])

            _res_pointer = copy.deepcopy(self.reservedResources[user][res_pointer['id']])
            if not isinstance(_res_pointer['path'], list):
                _res_pointer['path'] = _res_pointer['path'].split('/')

            res_id = False
            while not res_id:
                res_id = hexlify(os.urandom(5))
                # If by any chance, this ID already exists, generate another one!
                if _recursive_find_id(resources, res_id, []):
                    res_id = False
            _res_pointer = _recursive_refresh_id(_res_pointer)
            _res_pointer.update([('status', RESOURCE_FREE), ])
            _res_pointer.update([('path', [name]), ])

            resources['children'].update([(name, _res_pointer), ])

            # Write changes.
            self._save(root_id, props)
            return res_id
        except Exception as e:
            msg = 'Save reserved resource as: `{}` !'.format(e)
            logError(msg)
            return False

        #return True


    @cherrypy.expose
    def discardAndReleaseReservedResource(self, res_query, props={}, root_id=ROOT_DEVICE):
        """  """
        self._load(v=False, props=props)

        if root_id == ROOT_DEVICE:
            resources = self.resources
        else:
            resources = self.systems

        # If no resources...
        if not resources['children']:
            msg = 'Discard reserved resource: There are no resources defined !'
            logError(msg)
            return False

        if ':' in res_query:
            res_query = res_query.split(':')[0]

        res_path = _get_res_path(resources, res_query)
        res_pointer = _get_res_pointer(resources, ''.join('/' + res_path[0]))

        if not res_pointer:
            msg = 'Discard reserved resource: Cannot find resource path or ID `{}` !'.format(res_query)
            logError(msg)
            return False

        res_pointer.update([('path', [res_path[0]]), ])

        user_roles = self.userRoles(props)
        user = user_roles.get('user')

        try:
            self.reservedResources[user].pop(res_pointer['id'])
            res_pointer['status'] = RESOURCE_FREE
            # Write changes.
            self._save(root_id, props)

            if not self.reservedResources[user]:
                self.reservedResources.pop(user)
        except Exception as e:
            msg = 'Discard reserved resource: `{}` !'.format(e)
            logError(msg)
            return False

        return RESOURCE_FREE

#

# Eof()
