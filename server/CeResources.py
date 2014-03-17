
# File: CeResources.py ; This file is part of Twister.

# version: 2.034

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
import errno

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
from common.helpers    import *

RESOURCE_FREE     = 1
RESOURCE_BUSY     = 2
RESOURCE_RESERVED = 3

ROOT_DEVICE = 1
ROOT_SUT    = 2

ROOT_NAMES = {
    ROOT_DEVICE: 'Device', ROOT_SUT: 'SUT'
}

constant_dictionary = {'version': 0, 'name': '/', 'meta': {}, 'children': {}}

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


def _recursive_build_comp(parent, old_path, appendList=[]):
    '''
    parent - pointer in dictionary
    old_path - string with the parent component name
    appendList - list to append the sub-components
    '''
    if len(parent) == 0:
        # there are no sub-components; return empty list
        return []
    else:
        # there are sub-components

        # loop through all of them
        for child in parent:
            new_dict = parent[child]
            # build path name and add path, meta, id and children
            new_path = old_path + '/' + child
            add_dic = dict()
            add_dic['path'] = new_path
            add_dic['meta'] = new_dict['meta']
            add_dic['id'] = new_dict['id']

            if len(new_dict['children']) > 0:
                # component has children, add them recursively
                childList = list()
                _recursive_build_comp(new_dict['children'], new_path, childList)
                # append the list of sub-components
                add_dic['children'] = childList
            else:
                # no children, just add an empy list
                add_dic['children'] = []

            appendList.append(add_dic)

        return appendList


def _recursive_search_string(parent, query_string):
    '''
    parent - pointer in dictionary
    query_string - the string to search
    '''
    if len(parent) == 0:
        # there are no sub-components; return empty list
        return False
    else:
        # check if we got the string
        if parent['path'] == query_string:
            return True
        else:
            # deep search for every child
            for child in parent['children']:
                result =  _recursive_search_string(child,query_string)
                if result is True:
                    return True
    return False

#

class ResourceAllocator(_cptools.XMLRPCController):

    def __init__(self, project):

        logInfo('Starting Resource Allocator...')
        ti = time.time()

        self.project = project

        self.resources = constant_dictionary
        self.reservedResources = dict()
        self.lockedResources = dict()
        self.systems = constant_dictionary
        self.acc_lock = thread.allocate_lock() # Task change lock
        self.ren_lock = thread.allocate_lock() # Rename lock
        self.imp_lock = thread.allocate_lock() # Import lock
        self.save_lock = thread.allocate_lock() # Save lock
        self.load_lock = thread.allocate_lock() # Save lock
        self.res_file = '{}/config/resources.json'.format(TWISTER_PATH)
        self._loadedUsers = dict()
        self._load(v=True)

        logInfo('Resource Allocator initialization took `{:.4f}` sec.'.format(time.time()-ti))


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
        logFull('CeResources:_load {} {} {}'.format(v,props,force))

        if not force:
            try:
                user_roles = self.userRoles(props)
                user = user_roles.get('user')
                if user in self._loadedUsers:
                    # Get the user rpyc connection suts and count
                    try:
                        userConn = self.project._find_local_client(user)
                        userSutsLen = copy.deepcopy(userConn.root.exposed_get_suts_len())
                        loadedLen = 0
                        for c in self._loadedUsers[user]['children']:
                            if c.split('.')[-1] == 'user':
                                loadedLen += 1
                        if not userSutsLen == loadedLen:
                            userSuts = copy.deepcopy(userConn.root.get_suts())
                            if userSuts:
                                self.systems['children'].update(userSuts)

                                userSystems = constant_dictionary
                                userSystems['children'].update(userSuts)
                                self._loadedUsers.update([(user, userSystems), ])
                    except Exception as e:
                        if v:
                            logError('_load ERROR:: {}'.format(e))

                    self.systems = self._loadedUsers[user]
                    try:
                        sutsPath = self.project.getUserInfo(user, 'sys_sut_path')
                        if not sutsPath:
                            sutsPath = '{}/config/sut/'.format(TWISTER_PATH)
                        sutPaths = [p for p in os.listdir(sutsPath) if os.path.isfile(os.path.join(sutsPath, p)) and p.split('.')[-1] == 'json']
                        for sutPath in sutPaths:
                            sutName = '.'.join(['.'.join(sutPath.split('.')[:-1]  + ['system'])])
                            with open(os.path.join(sutsPath, sutPath), 'r') as f:
                                self.systems['children'].update([(sutName, json.load(f)), ])
                    except Exception as e:
                        if v:
                            logError('_load ERROR:: {}'.format(e))
                    return True
            except Exception as e:
                if v:
                    logError('RA: There are no devices to load! `{}`!'.format(e))

        with self.load_lock:

            if not self.resources.get('children'):
                self.resources = constant_dictionary
            if not self.systems.get('children'):
                self.systems = constant_dictionary

            # try to load test bed resources file
            try:
                f = open(self.res_file, 'r')
                self.resources = json.load(f)
                f.close() ; del f
                if v:
                    logDebug('RA: Devices loaded successfully.')

            except Exception as e:
                if v:
                    logError('RA: There are no devices to load! `{}`!'.format(e))
            # try to load SUT file
            try:
                self.systems   = constant_dictionary

                if v:
                    logDebug('RA: Systems root loaded successfully.')

                try:
                    user_roles = self.userRoles(props)
                    user = user_roles.get('user')
                    sutsPath = self.project.getUserInfo(user, 'sys_sut_path')
                    if not sutsPath:
                        sutsPath = '{}/config/sut/'.format(TWISTER_PATH)
                    sutPaths = [p for p in os.listdir(sutsPath) if os.path.isfile(os.path.join(sutsPath, p)) and p.split('.')[-1] == 'json']
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
                    userConn = self.project._find_local_client(user)
                    userSuts = copy.deepcopy(userConn.root.get_suts())
                    if userSuts:
                        self.systems['children'].update(userSuts)

                    userSystems  = constant_dictionary
                    if userSuts:
                        userSystems['children'].update(userSuts)
                    self._loadedUsers.update([(user, userSystems), ])
                except Exception as e:
                    if v:
                        logError('_load ERROR:: {}'.format(e))

                if v:
                    logDebug('RA: Systems loaded successfully.')
            except Exception as e:
                if v:
                    logError('RA: There are no SUTs to load! `{}`!'.format(e))
        r = None
        if not r == True and not r == None:
            logDebug('_load ERROR: {}'.format(r))
        # t1 = time.time()
        # logDebug('|||||||||||||_load time:: ', t1-t0)
        return True


    def _save(self, root_id=ROOT_DEVICE, props={}, resource_name = None, username = None):
        '''
        Function used to write the changes on HDD.
        The save is separate for Devices and SUTs, so the version is not incremented
        for both, before saving.
        '''
        logFull('CeResources:_save {} {} {} {}'.format(root_id,props,resource_name,username))
        log = list()
        # Write changes, using the Access Lock.
        with self.save_lock:

            if root_id == ROOT_DEVICE:
                try:
                    v = self.resources.get('version', 0) + 1
                    logDebug('Saving {} file, version `{}`.'.format(ROOT_NAMES[root_id], v))
                    self.resources['version'] = v
                    f = open(self.res_file, 'w')
                    json.dump(self.resources, f, indent=4)
                    f.close() ; del f
                except Exception as e:
                    log.append(e)
                    if v:
                        logError('Save ERROR: `{}`!'.format(e))

            else:
                try:
                    user_roles = self.userRoles(props)
                    user = user_roles.get('user')
                    if user in self._loadedUsers:
                        self.systems = self._loadedUsers[user]
                except Exception as e:
                    log.append(e)
                    if v:
                        logError('Save ERROR: `{}`!'.format(e))

                v = self.systems.get('version', 0) + 1
                self.systems['version'] = v

                systemsChildren = copy.deepcopy(self.systems['children'])
                self.systems['children'] = dict()

                self.systems = constant_dictionary

                self.systems['children'] = copy.deepcopy(systemsChildren)
                del systemsChildren

                userSuts = list()
                systemSuts = list()
                #logError('||||save sys', user, self.systems)
                for child in self.systems.get('children'):
                    if resource_name and child != resource_name :
                        continue

                    # Check where to save (ce / user)
                    user_roles = self.userRoles(props)
                    user = user_roles.get('user')
                    logDebug('Trying to save SUT file {} {} {}'.format(child, user, username))
                    if username and user != username:
                        # different user; dont't save it
                        logDebug('SUT file not saved; different users {} vs {}'.format(user,username))
                        continue
                    sutsPath = self.project.getUserInfo(user, 'sys_sut_path')
                    if not sutsPath:
                        sutsPath = '{}/config/sut/'.format(TWISTER_PATH)
                    childPath = os.path.join(sutsPath, '.'.join(child.split('.')[:-1] + ['json']))
                    if child.split('.')[-1] == 'system':
                        systemSuts.append((childPath, self.systems['children'][child]))
                    else:
                        userSuts.append(('.'.join(child.split('.')[:-1] + ['json']), self.systems['children'][child]))

                if userSuts:
                    # Get the user rpyc connection connection
                    user_roles = self.userRoles(props)
                    user = user_roles.get('user')
                    try:
                        userConn = self.project._find_local_client(user)
                        r = userConn.root.save_suts(userSuts)
                        if r is not True:
                            log.append(r)
                    except Exception as e:
                        log.append(e)
                        logError('Saving ERROR user:: `{}`.'.format(e))

                if systemSuts and not log:
                    for sys_sut in systemSuts:
                        try:
                            with open(sys_sut[0], 'w') as f:
                                json.dump(sys_sut[1], f, indent=4)
                        except Exception as e:
                            log.append(e)
                            logError('Saving ERROR system:: `{}`.'.format(e))

                    # update loaded users systems
                    self._loadedUsers.update([(user, self.systems), ])

                # else:
                #     self.reservedResources = dict()
                #     self.lockedResources = dict()

        if log:
            return '*ERROR* ' + str(log)

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
        logFull('CeResources:tree')
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
    def import_xml(self, xml_file, sutType='user', root_id=ROOT_DEVICE, props={}, username = None):
        '''
        Import one XML file.
        WARNING! This erases everything!
        '''
        self._load(v=False, props=props)

        if not os.path.isfile(xml_file):
            msg = 'Import XML: XML file `{}` does not exist!'.format(xml_file)
            logError(msg)
            return '*ERROR* ' + msg

        logDebug('Preparing to import XML file `{}`...'.format(xml_file))
        params_xml = etree.parse(xml_file)
        sutName = ""

        with self.imp_lock:
            if root_id == ROOT_DEVICE:
                try:
                    self.resources = xml_to_res(params_xml, {})
                    # self.resources = {'version': 0, 'name': '/', 'id': '1', 'meta': {},
                    #                     'children': xml_to_res(params_xml, {})}
                except Exception as e:
                    msg = 'Import XML: Exception `{}`.'.format(e)
                    logError(msg)
                    return '*ERROR* ' + msg
            else:
                try:
                    # default save to user path
                    sutName = os.path.basename(xml_file).split('.')[:-1]
                    if not sutName:
                        sutName = [os.path.basename(xml_file)]

                    # sut name is a list; make it string
                    sutName = ''.join(sutName)
                    # if we already have same SUT name, add timestamp to
                    # differentiate
                    tmpSutName = sutName + '.' + sutType
                    if tmpSutName in self.systems.get('children'):
                        actual_time = time.localtime()
                        sutName = '{}_{}'.format(sutName, time.strftime('%Y_%m_%d_%H_%M_%S',actual_time))

                    # Add SUT type ( user/system )
                    sutName = sutName + '.' + sutType

                    sutContent = xml_to_res(params_xml, {})
                    sutContent = sutContent.popitem()[1]
                    sutContent.update([('path', sutName.split()), ])
                    sutContent = _recursive_refresh_id(sutContent)
                    self.systems['children'].update([(sutName, sutContent), ])
                except Exception as e:
                    msg = 'Import XML: Exception `{}`.'.format(e)
                    logError(msg)
                    return'*ERROR* ' + msg

        # Write changes for Device or SUT
        if username:
            if '/' in sutName:
                name_to_save = sutName.split('/')[-1]
                r = self._save(root_id, props, name_to_save, username)
            else:
                r = self._save(root_id, props, sutName, username)
        else:
            r = self._save(root_id, props)
        if not r == True:
            return r

        #root_name = ROOT_NAMES[root_id]
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
            msg = 'Export XML: XML file `{}` cannot be written!'.format(xml_file)
            logError(msg)
            return '*ERROR* ' + msg

        logDebug('Preparing to export into XML file `{}`...'.format(xml_file))

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
    def import_sut_xml(self, xml_file, sutType='user', username = None):
        '''
        Import one sut XML file.
        '''
        logDebug('CeResources:import_sut_xml {} {} {}'.format(xml_file,sutType,username))
        props = {}
        return self.import_xml(xml_file, sutType, ROOT_SUT, props, username)


    @cherrypy.expose
    def export_sut_xml(self, xml_file, query, username = None):
        '''
        Export as XML file.
        '''
        res_path = _get_res_path(self.systems, query)
        res_pointer = _get_res_pointer(self.systems, ''.join('/' + res_path[0]))
        root = {'version': 0, 'name': '/', 'meta': {}, 'children': {res_path[0]: res_pointer}}
        return self.export_xml(xml_file, None, root, '{}')


    @cherrypy.expose
    def export_glob_sut_xml(self, xml_file, props={}):
        '''
        Export all suts as XML file.
        '''
        return self.export_xml(xml_file, ROOT_SUT, props)


    def userRoles(self, props={}):
        logFull('CeResources:userRoles')
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
    def getResource(self, query, root_id=ROOT_DEVICE, flatten=True, props={}, username=None):
        '''
        Show all the properties, or just 1 property of a resource.
        Must provide a Resource ID, or a Query.
        The function is used for both Devices and SUTs, by providing the ROOT ID.
        '''
        logFull('CeResources:getResource')
        self._load(v=False, props=props)

        # If the root is not provided, use the default root
        if root_id == ROOT_DEVICE:
            resources = self.resources
        else:
            resources = self.systems

        root_name = ROOT_NAMES[root_id]

        # If no resources...
        if not resources.get('children'):
            # Return default structure for root
            if query == '/':
                return {'name': '/', 'path': '', 'meta': resources.get('meta', {}), 'id': '1', 'children': []}

            msg = 'Get {}: There are no devices defined !'.format(root_name)
            logError(msg)
            return '*ERROR* ' + msg

        if not query:
            msg = 'Get {}: Cannot get a null resource !'.format(root_name)
            logError(msg)
            return '*ERROR* ' + msg

        logDebug('Get {} `{}`.'.format(root_name, query))

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
                return '*ERROR* no result'

        # If the query is a slash string query
        else:
            parts = [q for q in query.split('/') if q]
            result = resources

            # If this is a normal resource
            if root_id == ROOT_DEVICE:
                for part in parts:
                    if not result: return '*ERROR* no result'
                    result = result['children'].get(part)
            # If this is a SUT
            else:
                for part in parts:
                    if not result: return '*ERROR* no result'
                    res = result['children'].get(part)
                    if not res:
                        # Ok, this might be a Device path, instead of SUT path!
                        tb_id = result['meta'].get('_id')
                        # If this SUT doesn't have a Device ID assigned, bye bye!
                        if not tb_id: return '*ERROR* no result'
                        res_data = _recursive_find_id(self.resources, tb_id, [])
                        # If the Device ID is invalid, bye bye!
                        if not res_data: return '*ERROR* no result'
                        # Find out the Device path from Resources and add the rest of the parts
                        link_path = '/' + '/'.join(res_data.get('path', '')) + '/' + part
                        result = self.getResource(link_path, flatten=False)
                        # After this, scan the next PART from PARTS
                    else:
                        result = res

            if not result: return '*ERROR* no result'
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
                if not tb_id: return '*ERROR* no device id'
                return self.getResource(tb_id +':'+ meta)


    @cherrypy.expose
    def getSut(self, query, props={}, username = None):
        '''
        Show all the properties, or just 1 property of a SUT.
        Must provide a SUT ID, or a SUT Path.
        '''
        logDebug('CeResources: Get SUT for: `{}` `{}`!'.format(query,username))
        # query, root_id, flatten, props, username
        ret = self.getResource(query, ROOT_SUT, True, props, username)
        return ret

    @cherrypy.expose
    def getSutByName(self, query, username):
        '''
        Get the contant of one SUT file using it's name
        Must provide a SUT name.<type> ( type = user/system) and username
        '''
        logDebug('CeResources: GetSutByName {} {}'.format(query,username))
        suts = []
        usrHome = userHome(username)

        sutPath = None
        sutType = query.split('.')[-1]
        if sutType == 'system':
            # System SUT path
            sutPath = self.project.getUserInfo(username, 'sys_sut_path')
            if not sutPath:
                sutPath = '{}/config/sut/'.format(TWISTER_PATH)
        else:
            # User SUT path
            sutPath = self.project.getUserInfo(username, 'sut_path')
            if not sutPath:
                sutPath = '{}/twister/config/sut/'.format(usrHome)

        # if sut path doesn't end with '/' character, we have to add it
        if sutPath[-1] != '/':
            sutPath += '/'
        sutFile = sutPath + query.split('.')[0] + '.json'

        sutContent = False
        if os.path.isdir(sutPath):
            try:
                f = open(sutFile, 'r')
                sutContent = json.load(f)
                f.close() ; del f
            except IOError, e:
                if e.errno == errno.EACCES:
                    # permission denied error, try using the client
                    userConn = False
                    userConn = self.project._find_local_client(username)
                    if userConn:
                        fileContent = False
                        fileContent = userConn.root.exposed_read_file(sutFile)
                        if fileContent and not fileContent.startswith('*ERROR*'):
                            sutContent = json.loads(fileContent)

            if sutContent is False or (isinstance(sutContent, str) and sutContent.startswith('*ERROR*')):
                return sutContent

            if isinstance(sutContent, dict):
                # Now we have the SUT content; we need to format it for GUI
                recursiveList = list()
                retDict = dict()
                if sutContent.get('path'):
                    retDict['path'] = sutContent['path'][0]
                else:
                    retDict['path'] = query
                retDict['meta'] = sutContent['meta']
                retDict['id'] = sutContent['id']
                retDict['children'] = _recursive_build_comp(sutContent.get('children'),retDict['path'],recursiveList)
                return retDict

        # if we get here, we cannot get read access to the SUT directory
        return '*ERROR* Cannot get access to SUT path'


#

    @cherrypy.expose
    def setResource(self, name, parent=None, props={}, root_id=ROOT_DEVICE, username=None):
        '''
        Create or change a resource, using a name, a parent Path or ID and some properties.
        The function is used for both Devices and SUTs, by providing the ROOT ID.
        '''
        logFull('CeResources:setResource {} {} {} {} {}'.format(name,parent,props,root_id,username))
        self._load(v=False, props=props)

        user_roles = self.userRoles(props)

        # If the root is not provided, use the default root
        if root_id == ROOT_DEVICE:
            if 'CHANGE_TESTBED' not in user_roles.get('roles', []):
                msg = 'Privileges ERROR! Username `{user}` cannot use Set Resource!'.format(**user_roles)
                logDebug('Privileges ERROR! Username `{user}` cannot use Set Resource!'.format(**user_roles))
                return '*ERROR* ' + msg
            resources = self.resources
        else:
            if 'CHANGE_SUT' not in user_roles.get('roles', []):
                msg = 'Privileges ERROR! Username `{user}` cannot use Set SUT!'.format(**user_roles)
                logDebug(msg)
                return '*ERROR* ' + msg
            resources = self.systems

        root_name = ROOT_NAMES[root_id]

        if parent == '/' or parent == '1':
            _isResourceLocked = self.isResourceLocked(parent, root_id)
            if _isResourceLocked and _isResourceLocked != username:
                msg = 'Reserve resource: The resource is locked for {} !'.format(_isResourceLocked)
                logError(msg)
                return '*ERROR* ' + msg

        with self.acc_lock:
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

                epnames_tag = '_epnames_{}'.format(username)

                resources['meta'].update(props)
                # if _id key is present in meta and it has no value, we have
                # to remove it from meta dictionary
                if '_id' in resources['meta'].keys() and not resources['meta'].get('_id',False):
                    resources['meta'].pop('_id')

                # If the epnames tag exists in resources
                if epnames_tag in resources['meta']:
                    # And the tag is empty
                    if not resources['meta'][epnames_tag]:
                        logDebug('Deleting `{}` tag from resources.'.format(epnames_tag))
                        del resources['meta'][epnames_tag]

                # Write changes for Device or SUT
                if username:
                    if '/' in name:
                        name_to_save = name.split('/')[-1]
                        r = self._save(root_id, props, name_to_save, username)
                    else:
                        r = self._save(root_id, props, name, username)
                else:
                    r = self._save(root_id, props)
                logInfo('Set {}: Updated ROOT with properties: `{}`.'.format(root_name, props))
                if not r == True:
                    return r
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

            if not isinstance(parent_p.get('path'), list):
                parent_p['path'] = parent_p.get('path', '').split('/')

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

            # If the resource exists, patch the new properties!
            if name in parent_p['children']:
                if parent == '/' or parent == '1':
                    child_p = self._getReservedResource('/' + name, props, root_id)
                else:
                    child_p = parent_p['children'][name]

                if not child_p:
                    return '*ERROR* no found'

                old_child = copy.deepcopy(child_p)

                logDebug('Set Resource update props:: {} for child {}'.format(props,child_p))

                epnames_tag = '_epnames_{}'.format(username)

                child_p['meta'].update(props)
                # if _id key is present in meta and it has no value, we have
                # to remove it from meta dictionary
                if '_id' in child_p['meta'].keys() and not child_p['meta'].get('_id',False):
                    child_p['meta'].pop('_id')

                # If the epnames tag exists in resources
                if epnames_tag in child_p['meta']:
                    # And the tag is empty
                    if not child_p['meta'][epnames_tag]:
                        logDebug('Deleting `{}` tag from resources.'.format(epnames_tag))
                        del child_p['meta'][epnames_tag]

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

                epnames_tag = '_epnames_{}'.format(username)

                # If the epnames tag exists in resources
                if epnames_tag in parent_p['children'][name]['meta']:
                    # And the tag is empty
                    if not parent_p['children'][name]['meta'][epnames_tag]:
                        logDebug('Deleting `{}` tag from new resource.'.format(epnames_tag))
                        del parent_p['children'][name]['meta'][epnames_tag]

                r = None
                if parent == '/' or parent == '1':
                    # Write changes for Device or SUT
                    r = self._save(root_id, props, name, username)
                    if isinstance(r,str):
                         if '*ERROR*' in r:
                             # do clean up
                             parent_p['children'].pop(name)
                    else:
                        logDebug('Created {} `{}`, id `{}` : `{}` .'.format(root_name, name, res_id, props))

                if not r == True and not r == None:
                    return r
                return res_id


    @cherrypy.expose
    def setSut(self, name, parent=None, props={}, username=None):
        '''
        Create or change a SUT, using a name, a parent Path or ID and some properties.
        '''
        logDebug('CeResources:setSut {} {} {} {}'.format(name,parent,props,username))
        if not props:
            props = {}
        if not parent:
            parent = '/'
        return self.setResource(name, parent, props, ROOT_SUT, username)


    @cherrypy.expose
    def renameResource(self, res_query, new_name, props={}, root_id=ROOT_DEVICE):
        '''
        Rename a resource.
        '''
        logDebug('CeResources:renameResource {} {} {}'.format(res_query, new_name, props))
        self._load(v=False, props=props)

        user_roles = self.userRoles(props)
        user = user_roles['user']


        # If the root is not provided, use the default root
        if root_id == ROOT_DEVICE:
            if 'CHANGE_TESTBED' not in user_roles.get('roles', []):
                msg = 'Privileges ERROR! Username `{user}` cannot use Rename Resource!'.format(user)
                logDebug(msg)
                return '*ERROR* ' + msg
            resources = self.resources
        else:
            if 'CHANGE_SUT' not in user_roles.get('roles', []):
                msg = 'Privileges ERROR! Username `{user}` cannot use Rename SUT!'.format(user)
                logDebug(msg)
                return '*ERROR* ' + msg
            resources = self.systems

        root_name = ROOT_NAMES[root_id]

        # If no resources...
        if not resources.get('children'):
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

        _isResourceLocked = self.isResourceLocked(res_query, root_id)
        if _isResourceLocked and _isResourceLocked != user:
            msg = 'Reserve resource: The resource is locked for {} !'.format(_isResourceLocked)
            logError(msg)
            return '*ERROR* ' + msg

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
                if new_path[1:]:
                    new_string = 'res_p["children"]["{}"]'.format('"]["children"]["'.join(new_path[1:]))
                    exec( new_string + ' = ' + exec_string )
                    exec( 'del ' + exec_string )
                else:
                    #res_p['path'] = new_name
                    res_p.update([('path', [new_name]), ])

                logDebug('Renamed {} path `{}` to `{}`.'.format(root_name, '/'.join(node_path), '/'.join(new_path)))

        return True


    @cherrypy.expose
    def renameSut(self, res_query, new_name, username = None):
        '''
        Rename a SUT.
        '''
        logDebug('CeResources:renameSut {} {} {}'.format(res_query, new_name, username))

        return self.copySutFile(res_query, new_name, username, True)


    @cherrypy.expose
    def deleteResource(self, res_query, props={}, root_id=ROOT_DEVICE, username = None):
        '''
        Permanently delete a resource.
        '''
        logDebug('CeResources:deleteResource {} {} {} {}'.format(res_query,props,root_id,username))
        self._load(v=False, props=props)

        user_roles = self.userRoles(props)

        # If the root is not provided, use the default root
        if root_id == ROOT_DEVICE:
            if 'CHANGE_TESTBED' not in user_roles.get('roles', []):
                msg = 'Privileges ERROR! Username `{user}` cannot use Delete Resource!'.format(**user_roles)
                logDebug(msg)
                return '*ERROR* ' + msg
            resources = self.resources
        else:
            if 'CHANGE_SUT' not in user_roles.get('roles', []):
                msg = 'Privileges ERROR! Username `{user}` cannot use Delete SUT!'.format(**user_roles)
                logDebug(msg)
                return '*ERROR* ' + msg
            resources = self.systems

        root_name = ROOT_NAMES[root_id]

        # If no resources...
        if not resources.get('children'):
            msg = 'Del {}: There are no resources defined !'.format(root_name)
            logError(msg)
            return '*ERROR* ' + msg

        if ':' in res_query:
            meta      = res_query.split(':')[1]
            res_query = res_query.split(':')[0]
        else:
            meta = ''

        user = user_roles.get('user')

        # Check if resource is locked; if so, it cannot be deleted
        _isResourceLocked = self.isResourceLocked(res_query, root_id)
        if _isResourceLocked and _isResourceLocked != user:
            msg = 'Reserve resource: The resource is locked for {} !'.format(_isResourceLocked)
            logError(msg)
            return '*ERROR* ' + msg

        # Check if resource is reserved; if so, it cannot be deleted
        _isResourceLocked = self.isResourceReserved(res_query, root_id)
        if _isResourceLocked and _isResourceLocked != user:
            msg = 'Cannot delete: The resource is reserved for {} !'.format(_isResourceLocked)
            logError(msg)
            return '*ERROR* ' + msg


        # Check if is reserved
        try:
            for res in self.reservedResources[user]:
                res_path = _get_res_path(self.reservedResources[user][res], res_query)
                if res_path:
                    res_pointer = self.reservedResources[user][res]
                    break

                # it can be a meta parameter for the TB; we need to check this
                # case because get_res_path doesn't return correct in this case
                if res == res_query:
                    res_pointer = self.reservedResources[user][res]
                    res_path = [res_pointer.get('path')]
                    break;
        except Exception, e:
            res_path = None

        if res_path:
            # resource can be at test bed level or at children of test bed
            # level; we have to differentiate
            if res_pointer.get('path') == res_path[0]:
                # test bed level
                exec_string = 'res_pointer'
            else:
                # child of test bed level
                exec_string = 'res_pointer["children"]["{}"]'.format('"]["children"]["'.join(res_path))

            # If must delete a Meta info
            if meta:
                logDebug('Executing `{}` ...'.format( 'val = {}["meta"].get("{}")'.format(exec_string, meta) ))
                exec( 'val = {}["meta"].get("{}")'.format(exec_string, meta) )

                if val is None:
                    msg = 'Del {}: Cannot find resource meta info `{}` !'.format(root_name, meta)
                    logError(msg)
                    return '*ERROR* ' + msg

                logDebug('Executing `{}` ...'.format( 'del {}["meta"]["{}"]'.format(exec_string, meta) ))
                exec( 'del {}["meta"]["{}"]'.format(exec_string, meta) )
                logDebug('Deleted {} meta `{}:{}`.'.format(root_name, '/'.join(res_path), meta))

            # If must delete a normal node
            else:
                logDebug('Executing `{}` ...'.format( 'del ' + exec_string ))
                exec( 'del ' + exec_string )
                logDebug('Deleted {} path `{}`.'.format(root_name, '/'.join(res_path)))

            return True

        res_path = _get_res_path(resources, res_query)
        res_pointer = _get_res_pointer(resources, ''.join('/' + res_path[0]))

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
        if username:
            if '/' in res_query:
                name_to_save = res_query.split('/')[-1]
                r = self._save(root_id, props, name_to_save, username)
            else:
                r = self._save(root_id, props, res_query, username)
        else:
            r = self._save(root_id, props)

        # Delete file if it's SUT file
        if not meta and len(node_path) == 1 and root_id == ROOT_SUT:
            if node_path[0].split('.')[-1] == 'system':
                sutsPath = self.project.getUserInfo(user, 'sys_sut_path')
                if not sutsPath:
                    sutsPath = '{}/config/sut/'.format(TWISTER_PATH)
                file_name = node_path[0].split('.')[:-1][0]
                file_name += '.json'

                os.remove(sutsPath+file_name)
            else:
                # Get the user rpyc connection connection
                try:
                    userConn = self.project._find_local_client(user)
                    userConn.root.delete_sut('.'.join(node_path[0].split('.')[:-1]))
                except Exception as e:
                    logError('Saving ERROR:: `{}`.'.format(e))

        if not r == True:
            return r

        return True


    @cherrypy.expose
    def deleteSut(self, res_query, username = None):
        '''
        Permanently delete a SUT.
        '''
        logFull('CeResources:deleteSut')
        return self.deleteResource(res_query, '{}', ROOT_SUT, username)


    @cherrypy.expose
    def isSutReserved(self, res_query):
        """ returns the user or false """

        logFull('CeResources:isSutReserved')
        return self.isResourceReserved(res_query, ROOT_SUT)


    @cherrypy.expose
    def reserveSut(self, res_query, username = None):
        '''
        Reserve a SUT.
        '''
        logFull('CeResources:reserveSut')
        return self.reserveResource(res_query, '{}', ROOT_SUT, username)


    @cherrypy.expose
    def saveReservedSutAs(self, name, res_query, username = None):
        '''
        Save a reserved SUT as.
        '''
        logDebug('CeResources:saveReservedSutAs {} {} {}'.format(name,res_query,username))

        # we need to create the SUT file first
        props = {}
        #p_key = '_epnames_' + username
        #parent = {p_key:''}
        self.setResource(name, '/', props, ROOT_SUT, username)

        return self.saveReservedResourceAs(name, res_query, props, ROOT_SUT, username)


    @cherrypy.expose
    def saveReservedSut(self, res_query, username = None):
        '''
        Save a reserved SUT.
        '''
        logFull('CeResources:saveReservedSut')
        props = {}
        return self.saveReservedResource(res_query, props, ROOT_SUT, username)


    @cherrypy.expose
    def saveAndReleaseReservedSut(self, res_query, username = None):
        '''
        Save a reserved SUT.
        '''
        logFull('CeResources:saveAndReleaseReservedSut')
        return self.saveAndReleaseReservedResource(res_query, '{}', ROOT_SUT, username)


    @cherrypy.expose
    def discardAndReleaseReservedSut(self, res_query, username = None):
        '''
        Discard a reserved SUT.
        '''
        logFull('CeResources:discardAndReleaseReservedSut')
        props = {}
        return self.discardAndReleaseReservedResource(res_query, props, ROOT_SUT, username)


    @cherrypy.expose
    def isSutLocked(self, res_query):
        """ returns the user or false """

        logFull('CeResources:isSutLocked')
        return self.isResourceLocked(res_query, ROOT_SUT)


    @cherrypy.expose
    def lockSut(self, res_query, props={}, username = None):
        '''
        Lock a SUT.
        '''
        logFull('CeResources:lockSut')
        return self.lockResource(res_query, props, ROOT_SUT, username)


    @cherrypy.expose
    def unlockSut(self, res_query, props={}, username = None):
        '''
        Unlock a SUT.
        '''
        logFull('CeResources:unlockSut')
        return self.unlockResource(res_query, props, ROOT_SUT, username)


# # # Allocation and reservation of resources # # #


    def _getReservedResource(self, res_query, props={}, root_id=ROOT_DEVICE):
        '''
        Returns the reserved resource.
        '''
        logFull('CeResources:_getReservedResource')
        if root_id == ROOT_DEVICE:
            resources = self.resources
        else:
            resources = self.systems

        # If no resources...
        if not resources.get('children'):
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
                        return self.reservedResources[user][p]

        res_pointer = _get_res_pointer(resources, ''.join('/' + res_path[0]))

        if not res_pointer:
            msg = 'Get reserved resource: Cannot find resource path or ID `{}` !'.format(res_query)
            logError(msg)
            return False

        if not self.reservedResources.get(user):
            msg = 'Get reserved resource: Resource `{}` is not reserved !'.format(res_query)
            logError(msg)
            return False

        res_pointer.update([('path', [res_path[0]]), ])
        join_path = self.reservedResources[user][res_pointer['id']].get('path', '')
        if isinstance(join_path, str):
            join_path = [join_path]

        self.reservedResources[user][res_pointer['id']]['path'] = '/'.join(join_path)

        return self.reservedResources[user][res_pointer['id']]


    @cherrypy.expose
    def isResourceReserved(self, res_query, root_id=ROOT_DEVICE):
        """ returns the user or false """
        logFull('CeResources:isResourceReserved')
        if root_id == ROOT_DEVICE:
            resources = self.resources
        else:
            resources = self.systems

        # If no resources...
        if not resources.get('children'):
            msg = 'Is resource reserved: There are no resources defined !'
            logError(msg)
            return '*ERROR* ' + msg

        if ':' in res_query:
            res_query = res_query.split(':')[0]

        res_path = _get_res_path(resources, res_query)
        if not res_path:
            # return '*ERROR* not found'
            return False
        res_pointer = _get_res_pointer(resources, ''.join('/' + res_path[0]))

        if not res_pointer:
            msg = 'Is resource reserved: Cannot find resource path or ID `{}` !'.format(res_query)
            logError(msg)
            return '*ERROR* ' + msg

        res_pointer.update([('path', [res_path[0]]), ])

        reservedForUser = [u for u in self.reservedResources if res_pointer['id'] in self.reservedResources[u]]

        if not reservedForUser:
            return False

        if len(reservedForUser) == 1:
            reservedForUser = reservedForUser[0]
        else:
            logDebug('Wrong length for reservedForUser: {}'.format(len(reservedForUser)))
            return False

        return reservedForUser


    @cherrypy.expose
    def reserveResource(self, res_query, props={}, root_id=ROOT_DEVICE, username = None):
        """  """
        logDebug('CeResources:reserveResource {} {} {} {}'.format(res_query, props, root_id, username))
        self._load(v=False, props=props)

        if root_id == ROOT_DEVICE:
            resources = self.resources
        else:
            resources = self.systems

        # If no resources...
        if not resources.get('children'):
            msg = 'Reserve resource: There are no resources defined !'
            logError(msg)
            return '*ERROR* ' + msg

        if ':' in res_query:
            res_query = res_query.split(':')[0]

        user_roles = self.userRoles(props)
        user = user_roles.get('user')

        with self.acc_lock:
            _isResourceLocked = self.isResourceLocked(res_query, root_id)
            if _isResourceLocked and _isResourceLocked != user:
                msg = 'Reserve resource: The resource is locked for {} !'.format(_isResourceLocked)
                logError(msg)
                return '*ERROR* ' + msg

            _isResourceReserved = self.isResourceReserved(res_query, root_id)
            if _isResourceReserved and _isResourceReserved != user:
                msg = 'Reserve resource: The resource is reserved for {} !'.format(_isResourceReserved)
                logError(msg)
                return '*ERROR* ' + msg

            res_path = _get_res_path(resources, res_query)
            res_pointer = _get_res_pointer(resources, ''.join('/' + res_path[0]))

            if not res_pointer:
                msg = 'Reserve Resource: Cannot find resource path or ID `{}` !'.format(res_query)
                logError(msg)
                return '*ERROR* ' + msg

            res_pointer.update([('path', [res_path[0]]), ])

            if user in self.reservedResources:
                self.reservedResources[user].update([(res_pointer['id'], copy.deepcopy(res_pointer)), ])
            else:
                self.reservedResources.update([(user, {res_pointer['id']: copy.deepcopy(res_pointer)}), ])

        return True #RESOURCE_RESERVED


    @cherrypy.expose
    def saveAndReleaseReservedResource(self, res_query, props={}, root_id=ROOT_DEVICE, username = None):
        """  """
        logDebug('CeResources:saveAndReleaseReservedResource {} {} {} {}'.format(res_query, props, root_id, username))
        self._load(v=False, props=props)

        if root_id == ROOT_DEVICE:
            resources = self.resources
        else:
            resources = self.systems

        # If no resources...
        if not resources.get('children'):
            msg = 'Save and release reserved resource: There are no resources defined !'
            logError(msg)
            return '*ERROR* ' + msg

        if ':' in res_query:
            res_query = res_query.split(':')[0]

        res_path = _get_res_path(resources, res_query)
        res_pointer = _get_res_pointer(resources, ''.join('/' + res_path[0]))

        if '/' in res_query:
            res_query = res_query.split('/')[-1]

        if not res_pointer:
            msg = 'Save and release resource: Cannot find resource path or ID `{}` !'.format(res_query)
            logError(msg)
            return '*ERROR* ' + msg

        res_pointer.update([('path', [res_path[0]]), ])

        user_roles = self.userRoles(props)
        user = user_roles.get('user')

        #if not the same user, we have an error
        if username and user != username:
            msg = 'Save reserved resource: Cannot find resource path or ID `{}` for user {} !'.format(res_query, user)
            logError(msg)
            return '*ERROR* ' + msg

        save_result = None
        try:
            _res_pointer = self.reservedResources[user].pop(res_pointer['id'])
            if not isinstance(_res_pointer['path'], list):
                _res_pointer['path'] = _res_pointer['path'].split('/')

            # Check for modifications
            if res_pointer != _res_pointer:
                child = None
                for c in resources.get('children'):
                    if resources['children'][c]['id'] == _res_pointer['id']:
                        child = c
                if not child == _res_pointer['path'][0]:
                    resources['children'].pop(child)

                    # Delete file
                    if child.split('.')[-1] == 'system':
                        sutsPath = self.project.getUserInfo(user, 'sys_sut_path')
                        if not sutsPath:
                            sutsPath = '{}/config/sut/'.format(TWISTER_PATH)
                        os.remove(os.path.join(sutsPath, '.'.join(child.split('.')[:-1] + ['json'])))
                    else:
                        # Get the user rpyc connection connection
                        try:
                            userConn = self.project._find_local_client(user)
                            userConn.root.delete_sut('.'.join(child.split('.')[:-1]))
                        except Exception as e:
                            logError('Save and release resource ERROR:: `{}`.'.format(e))

            resources['children'].update([(_res_pointer['path'][0], _res_pointer), ])
            #resources['children'].update([(res_path[0], _res_pointer), ])

            # Check for modifications
            if res_pointer != _res_pointer:
                # Write changes.
                save_result= self._save(root_id, props, res_query, username)

            if not self.reservedResources[user]:
                self.reservedResources.pop(user)
        except Exception as e:
            msg = 'Save and release resource: `{}` !'.format(e)
            logError(msg)
            return '*ERROR* ' + msg

        if not save_result == True and not save_result == None:
            return save_result

        return True #RESOURCE_FREE


    @cherrypy.expose
    def saveReservedResource(self, res_query, props={}, root_id=ROOT_DEVICE, username = None):
        """  """
        logFull('CeResources:saveReservedResource')
        self._load(v=False, props=props)

        if root_id == ROOT_DEVICE:
            resources = self.resources
        else:
            resources = self.systems

        # If no resources...
        if not resources.get('children'):
            msg = 'Save reserved resource: There are no resources defined !'
            logError(msg)
            return '*ERROR* ' + msg

        if ':' in res_query:
            res_query = res_query.split(':')[0]

        res_path = _get_res_path(resources, res_query)
        res_pointer = _get_res_pointer(resources, ''.join('/' + res_path[0]))

        if '/' in res_query:
            res_query = res_query.split('/')[-1]

        if not res_pointer:
            msg = 'Save reserved resource: Cannot find resource path or ID `{}` !'.format(res_query)
            logError(msg)
            return '*ERROR* ' + msg

        res_pointer.update([('path', [res_path[0]]), ])

        user_roles = self.userRoles(props)
        user = user_roles.get('user')
        r = None
        try:
            _res_pointer = copy.deepcopy(self.reservedResources[user][res_pointer['id']])
            if not isinstance(_res_pointer['path'], list):
                _res_pointer['path'] = _res_pointer['path'].split('/')

            # Check for modifications
            if res_pointer != _res_pointer:
                child = None
                # Search in all esources for this SUT
                for c in resources.get('children'):
                    if resources['children'][c]['id'] == _res_pointer['id']:
                        child = c
                # SUT not found in resources; new one or strange scenario; we
                # have to delete existing file to make everything is clean
                if not child == _res_pointer['path'][0]:
                    resources['children'].pop(child)

                    # Delete file
                    if child.split('.')[-1] == 'system':
                        sutsPath = self.project.getUserInfo(user, 'sys_sut_path')
                        if not sutsPath:
                            sutsPath = '{}/config/sut/'.format(TWISTER_PATH)
                        os.remove(os.path.join(sutsPath, '.'.join(child.split('.')[:-1] + ['json'])))
                    else:
                        # Get the user rpyc connection connection
                        try:
                            userConn = self.project._find_local_client(user)
                            userConn.root.delete_sut('.'.join(child.split('.')[:-1]))
                        except Exception as e:
                            logError('Save resource ERROR:: `{}`.'.format(e))

            resources['children'].update([(_res_pointer['path'][0], _res_pointer), ])

            # Check for modifications
            if res_pointer != _res_pointer:
                # Write changes.
                self._save(root_id, props, res_query,username)
        except Exception as e:
            msg = 'Save reserved resource: `{}` !'.format(e)
            logError(msg)
            return '*ERROR* ' + msg

        if not r == True and not r == None:
            return r

        return True #RESOURCE_RESERVED


    @cherrypy.expose
    def saveReservedResourceAs(self, name, res_query, props={}, root_id=ROOT_DEVICE, username = None):
        """  """
        logFull('CeResources:saveReservedResourceAs')
        self._load(v=False, props=props)

        if root_id == ROOT_DEVICE:
            resources = self.resources
        else:
            resources = self.systems

        # If no resources...
        if not resources.get('children'):
            msg = 'Save reserved resource as: There are no resources defined !'
            logError(msg)
            return '*ERROR* ' + msg

        if ':' in res_query:
            res_query = res_query.split(':')[0]

        res_path = _get_res_path(resources, res_query)
        res_pointer = _get_res_pointer(resources, ''.join('/' + res_path[0]))

        if '/' in res_query:
            res_query = res_query.split('/')[-1]

        if not res_pointer:
            msg = 'Save reserved resource as: Cannot find resource path or ID `{}` !'.format(res_query)
            logError(msg)
            return '*ERROR* ' + msg

        res_pointer.update([('path', [res_path[0]]), ])

        user_roles = self.userRoles(props)
        user = user_roles.get('user')

        #if not the same user, we have an error
        if username and user != username:
            msg = 'Save reserved resource as: Cannot find resource path or ID `{}` for user {} !'.format(res_query, user)
            logError(msg)
            return '*ERROR* ' + msg

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
            _res_pointer.update([('path', [name]), ])

            resources['children'].update([(name, _res_pointer), ])

            # Write changes.
            r = self._save(root_id, props, res_query, username)
            if not r == True:
                return r
            return res_id
        except Exception as e:
            msg = 'Save reserved resource as: `{}` !'.format(e)
            logError(msg)
            return '*ERROR* ' + msg

        #return True


    @cherrypy.expose
    def discardAndReleaseReservedResource(self, res_query, props={}, root_id=ROOT_DEVICE, username=None):
        """  """
        logDebug('CeResources:discardAndReleaseReservedResource')
        self._load(v=False, props=props)

        if root_id == ROOT_DEVICE:
            resources = self.resources
        else:
            resources = self.systems

        # If no resources...
        if not resources.get('children'):
            msg = 'Discard reserved resource: There are no resources defined !'
            logError(msg)
            return '*ERROR* ' + msg

        if ':' in res_query:
            res_query = res_query.split(':')[0]

        res_path = _get_res_path(resources, res_query)
        res_pointer = _get_res_pointer(resources, ''.join('/' + res_path[0]))

        if not res_pointer:
            msg = 'Discard reserved resource: Cannot find resource path or ID `{}` !'.format(res_query)
            logError(msg)
            return '*ERROR* ' + msg

        res_pointer.update([('path', [res_path[0]]), ])

        user_roles = self.userRoles(props)
        user = user_roles.get('user')

        if username and user != username:
            #Different user; return
            return

        try:
            self.reservedResources[user].pop(res_pointer['id'])
            if not self.reservedResources[user]:
                self.reservedResources.pop(user)
        except Exception as e:
            msg = 'Discard reserved resource: `{}` !'.format(e)
            logError(msg)
            return '*ERROR* ' + msg

        return True #RESOURCE_FREE


    @cherrypy.expose
    def isResourceLocked(self, res_query, root_id=ROOT_DEVICE):
        """ returns the user or false """
        logFull('CeResources:isResourceLocked')
        if root_id == ROOT_DEVICE:
            resources = self.resources
        else:
            resources = self.systems

        # If no resources...
        if not resources.get('children'):
            # msg = 'Is resource locked: There are no resources defined !'
            # logError(msg)
            # return '*ERROR* ' + msg
            return False

        if ':' in res_query:
            res_query = res_query.split(':')[0]

        res_path = _get_res_path(resources, res_query)
        if not res_path:
            # return '*ERROR* not found'
            return False
        res_pointer = _get_res_pointer(resources, ''.join('/' + res_path[0]))

        if not res_pointer:
            msg = 'Is resource locked: Cannot find resource path or ID `{}` !'.format(res_query)
            logError(msg)
            return '*ERROR* ' + msg

        res_pointer.update([('path', [res_path[0]]), ])

        lockedForUser = [u for u in self.lockedResources if res_pointer['id'] in self.lockedResources[u]]

        if not lockedForUser:
            return False

        if len(lockedForUser) == 1:
            lockedForUser = lockedForUser[0]
        else:
            logDebug('Wrong length for lockedForUser: {}'.format(len(lockedForUser)))
            return False

        return lockedForUser


    @cherrypy.expose
    def lockResource(self, res_query, props={}, root_id=ROOT_DEVICE, username = None):
        """  """
        logDebug('CeResources:lockResource {} {} {} {}'.format(res_query, props, root_id, username))
        self._load(v=False, props=props)

        if root_id == ROOT_DEVICE:
            resources = self.resources
        else:
            resources = self.systems

        # If no resources...
        if not resources.get('children'):
            msg = 'Lock resource: There are no resources defined !'
            logError(msg)
            return '*ERROR* ' + msg

        if ':' in res_query:
            res_query = res_query.split(':')[0]

        user_roles = self.userRoles(props)
        user = user_roles.get('user')

        with self.acc_lock:
            _isResourceReserved = self.isResourceReserved(res_query, root_id)
            if _isResourceReserved and _isResourceReserved != user:
                msg = 'Lock resource: The resource is reserved for {} !'.format(_isResourceReserved)
                logError(msg)
                return '*ERROR* ' + msg

            _isResourceLocked = self.isResourceLocked(res_query, root_id)
            if _isResourceLocked and _isResourceLocked != user:
                msg = 'Lock resource: The resource is locked for {} !'.format(_isResourceLocked)
                logError(msg)
                return '*ERROR* ' + msg

            res_path = _get_res_path(resources, res_query)
            res_pointer = _get_res_pointer(resources, ''.join('/' + res_path[0]))

            if not res_pointer:
                msg = 'Lock Resource: Cannot find resource path or ID `{}` !'.format(res_query)
                logError(msg)
                return '*ERROR* ' + msg

            res_pointer.update([('path', [res_path[0]]), ])

            # if it's not the same user, don't lock the resource, just return
            if username and user != username:
                logDebug('CeResources:lockResource different user {} {}'.format(user, username))
                return False

            user_res = self.lockedResources.get(user, {})
            user_res.update({res_pointer['id']: copy.deepcopy(res_pointer)})
            self.lockedResources[user] = user_res

        return True #RESOURCE_BUSY


    @cherrypy.expose
    def unlockResource(self, res_query, props={}, root_id=ROOT_DEVICE, username = None):
        """  """
        logDebug('CeResources:unlockResource {} {} {} {}'.format(res_query,props,root_id,username))
        self._load(v=False, props=props)

        if root_id == ROOT_DEVICE:
            resources = self.resources
        else:
            resources = self.systems

        # If no resources...
        if not resources.get('children'):
            msg = 'Unlock resource: There are no resources defined !'
            logError(msg)
            return '*ERROR* ' + msg

        if ':' in res_query:
            res_query = res_query.split(':')[0]

        res_path = _get_res_path(resources, res_query)
        res_pointer = _get_res_pointer(resources, ''.join('/' + res_path[0]))

        if not res_pointer:
            msg = 'Unlock resource: Cannot find resource path or ID `{}` !'.format(res_query)
            logError(msg)
            return '*ERROR* ' + msg

        res_pointer.update([('path', [res_path[0]]), ])

        with self.acc_lock:
            user_roles = self.userRoles(props)
            user = user_roles.get('user')
            try:
                self.lockedResources[user].pop(res_pointer['id'])
                if not self.lockedResources[user]:
                    self.lockedResources.pop(user)
            except Exception as e:
                msg = 'Unlock resource: `{}` !'.format(e)
                logError(msg)
                return '*ERROR* ' + msg

        return True #RESOURCE_FREE


    @cherrypy.expose
    def listReservedResources(self):
        return self.reservedResources


    @cherrypy.expose
    def listLockedResources(self):
        return self.lockedResources


    @cherrypy.expose
    def listAllResources(self):
        """
        Fast list testbeds.
        """
        res = []
        for k, v in self.resources.get('children').iteritems():
            path = v.get('path') or _get_res_path(self.resources, v['id']) or []
            res.append(['/'.join(path), v['id']])
        result = []

        def quickFindPath(d, spath):
            for usr, locks in d.iteritems():
                for id, data in locks.iteritems():
                    path = data.get('path', [''])
                    if isinstance(path, str) or isinstance(path, unicode):
                        path = [path]
                    if path == [spath]:
                        return usr
            return None

        for tb, id in sorted(res):
            ruser = quickFindPath(self.reservedResources, tb)
            luser = quickFindPath(self.lockedResources, tb)

            if (not ruser) and (not luser):
                result.append({'id': id, 'name': tb, 'status': 'free'})
            elif ruser:
                result.append({'id': id, 'name': tb, 'status': 'reserved', 'user': ruser})
            elif luser:
                result.append({'id': id, 'name': tb, 'status': 'locked', 'user': luser})
            # Both reserved and locked ?
            else:
                result.append({'id': id, 'name': tb, 'status': 'reserved', 'user': ruser})

        logDebug('Fast listing Resources... Found {}.'.format(res))

        return result


    @cherrypy.expose
    def listAllSuts(self, user):
        """
        Fast list suts.
        """
        suts = []
        result = []
        usrHome = userHome(user)

        # System SUT path
        sysSutsPath = self.project.getUserInfo(user, 'sys_sut_path')
        if not sysSutsPath:
            sysSutsPath = '{}/config/sut/'.format(TWISTER_PATH)

        # User SUT path
        usrSutPath = self.project.getUserInfo(user, 'sut_path')
        if not usrSutPath:
            usrSutPath = '{}/twister/config/sut/'.format(usrHome)

        if os.path.isdir(sysSutsPath):
            s = ['{}.system'.format(os.path.splitext(d)[0]) for d in os.listdir(sysSutsPath) if os.path.splitext(d)[1]=='.json']
            suts.extend(s)
        if os.path.isdir(usrSutPath):
            try:
                s = ['{}.user'.format(os.path.splitext(d)[0]) for d in os.listdir(usrSutPath) if os.path.splitext(d)[1]=='.json']
                suts.extend(s)
            except OSError, e:
                if e.errno == errno.EACCES:
                    # permission denied error, try using the client
                    userConn = None
                    userSutsList = ()
                    userConn = self.project._find_local_client(user)
                    if userConn:
                        userSutsList = userConn.root.exposed_list_all_suts()
                    suts.extend(userSutsList)


        def quickFindPath(d, spath):
            for usr, locks in d.iteritems():
                for id, data in locks.iteritems():
                    path = data.get('path', [''])
                    if isinstance(path, str) or isinstance(path, unicode):
                        path = [path]
                    if path == [spath]:
                        return usr
            return None

        for s in sorted(suts):
            ruser = quickFindPath(self.reservedResources, s)
            luser = quickFindPath(self.lockedResources, s)

            if (not ruser) and (not luser):
                result.append({'name': s, 'status': 'free'})
            elif ruser:
                result.append({'name': s, 'status': 'reserved', 'user': ruser})
            elif luser:
                result.append({'name': s, 'status': 'locked', 'user': luser})
            # Both reserved and locked ?
            else:
                result.append({'name': s, 'status': 'reserved', 'user': ruser})

        logDebug('Fast listing SUTs... Found {}.'.format(suts))

        return result


    @cherrypy.expose
    def copySutFile(self, old_sut, new_sut, user, delete_old=True):
        """
        Copy a SUT file in a new one
        """
        logDebug('CeResources:copySutFile {} {} {} {}'.format(old_sut,new_sut,user,delete_old))

        # check if old_sut exists
        foundOldSut = False
        userSutList = self.listAllSuts(user)
        if userSutList:
            for listElem in userSutList:
                if listElem['name'] == old_sut:
                    foundOldSut = True;
                    continue

        if not foundOldSut:
            msg = 'SUT file {} doesn\'t exit !'.format(old_sut)
            logError(msg)
            return '*ERROR* ' + msg

        # check that the new_sut name doesn't exists
        if userSutList:
            for listElem in userSutList:
                if listElem['name'] == new_sut:
                    msg = 'New SUT file {} already exits !'.format(new_sut)
                    logError(msg)
                    return '*ERROR* ' + msg

        # make sure the SUT file names start with /
        if new_sut[0] != '/':
            new_sut = '/' + new_sut
        if old_sut[0] != '/':
            old_sut = '/' + old_sut

        # create a new SUT file and reserve it
        newSutId = self.setResource(new_sut, '/', '{}', ROOT_SUT, user)
        if isinstance(newSutId,str):
            if '*ERROR*' in newSutId:
                msg = 'New SUT file {} cannot be created!'.format(new_sut)
                logError(msg)
                return '*ERROR* ' + msg

        reserve_res = self.reserveResource(new_sut, '{}', ROOT_SUT, user)
        if  isinstance(reserve_res,str):
             if '*ERROR*' in reserve_res:
                 msg = 'New SUT file {} cannot be reserved!'.format(new_sut)
                 logError(msg)
                 return '*ERROR* ' + msg

        # method to clean the new SUT if needed
        def cleanNewSut(new_sut,user):
            self.reservedResources[user].pop(new_sut)
            if not self.reservedResources[user]:
                self.reservedResources.pop(user)
            self.deleteResource(new_sut, '{}', ROOT_SUT, user)

        # reserve the old SUT file and copy the content into the new SUT file
        # Check if resource is locked; if so, it cannot be copied
        _isResourceLocked = self.isResourceLocked(old_sut, ROOT_SUT)
        if _isResourceLocked and _isResourceLocked != user:
            msg = 'Reserve resource: The resource is locked for {} !'.format(_isResourceLocked)
            logError(msg)
            cleanNewSut(newSutId,user)
            return '*ERROR* ' + msg

        # Check if resource is reserved; if so, it cannot be copied
        _isResourceLocked = self.isResourceReserved(old_sut, ROOT_SUT)
        if _isResourceLocked and _isResourceLocked != user:
            msg = 'Cannot delete: The resource is reserved for {} !'.format(_isResourceLocked)
            logError(msg)
            cleanNewSut(newSutId,user)
            return '*ERROR* ' + msg

        # Try to reserve source SUT file; if error, clean up the new SUT
        reserve_res = self.reserveResource(old_sut, '{}', ROOT_SUT, user)
        if  isinstance(reserve_res,str):
             if '*ERROR*' in reserve_res:
                 msg = 'Source SUT file {} cannot be reserved!'.format(old_sut)
                 logError(msg)
                 cleanNewSut(newSutId,user)
                 return '*ERROR* ' + msg

        # Everything is ready for copy; just do it
        # get the pointer to the old sut and new sut
        old_res_path = _get_res_path(self.systems, old_sut)
        old_res_pointer = _get_res_pointer(self.systems, ''.join('/' + old_res_path[0]))

        new_res_path = _get_res_path(self.systems, new_sut)
        new_res_pointer = _get_res_pointer(self.systems, ''.join('/' + new_res_path[0]))

        #update the meta and children
        new_res_pointer['meta'].update(old_res_pointer['meta'])
        new_res_pointer['children'].update(old_res_pointer['children'])

        if '/' in new_sut:
            new_sut = new_sut.split('/')[-1]

        save_result = self._save(ROOT_SUT, {}, new_sut, user)
        if isinstance(save_result,str):
             if '*ERROR*' in save_result:
                 msg = logDebug('Save SUT file {} ERROR !'.format(new_sut))
                 logError(msg)
                 cleanNewSut(newSutId,user)
                 return '*ERROR* ' + msg

        # release the new SUT
        self.reservedResources[user].pop(newSutId)
        if not self.reservedResources[user]:
            self.reservedResources.pop(user)

        # release the old sut; and delete if needed
        self.reservedResources[user].pop(old_res_pointer['id'])
        if not self.reservedResources[user]:
            self.reservedResources.pop(user)
        if delete_old is True:
            self.deleteResource(old_sut, '{}', ROOT_SUT, user)

        return True


    @cherrypy.expose
    def getReservedResource(self, query):
        """
        Return true is the <query> resource is reserved
        Query examples:
            - tb3
            - tb3/C1
            - sut_1.user
            - sut_1.user/comp_4
            - sut_1.user/comp_1/sub_comp_1
        Function returns True if query is found, else return False
        """
        user_roles = self.userRoles()
        user = user_roles['user']

        userResources = False
        for child in self.reservedResources:
            if child == user:
                userResources = self.reservedResources.get(user)

        if not userResources:
            return False

        # Every resource id is a key in the userResources dcitionary
        for id_key in userResources:
            # get the resource path
            root_path = userResources[id_key]['path']

            # set new_path where value for this key starts
            new_path = userResources[id_key]

            # recursevly build a dictionary with all subcomponents of the new_path
            recursiveList = []
            retDict = {}
            retDict['path'] = root_path[0]
            retDict['meta'] = new_path['meta']
            retDict['id'] = new_path['id']
            retDict['children'] = _recursive_build_comp(new_path.get('children'),retDict['path'],recursiveList)
            # logDebug('\n BOG {}\n'.format(retDict))

            # search the query if the created dictionary
            if _recursive_search_string(retDict, query):
                return True

        return False

#

# Eof()
