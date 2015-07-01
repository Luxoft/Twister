
# File: CeResources.py ; This file is part of Twister.

# version: 3.003

# Copyright (C) 2012-2013 , Luxoft

# Authors:
#    Andreea Proca <aproca@luxoft.com>
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
#import errno

try:
    import simplejson as json
except:
    import json

import cherrypy
from lxml import etree
from binascii import hexlify
from cherrypy import _cptools
from mako.template import Template
import time

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print 'TWISTER_PATH environment variable is not set! Exiting!'
    exit(1)
if TWISTER_PATH not in sys.path:
    sys.path.append(TWISTER_PATH)

from common.tsclogging import logError, logInfo, logFull, logDebug, logWarning
from common.helpers    import userHome

RESOURCE_FREE = 1
RESOURCE_BUSY = 2
RESOURCE_RESERVED = 3

ROOT_DEVICE = 1
ROOT_SUT = 2

ROOT_NAMES = {
    ROOT_DEVICE: 'Device', ROOT_SUT: 'SUT'
}

CONSTANT_DICTIONARY = {'version': 0, 'name': '/', 'meta': {}, 'children': {}}

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

    try:
        path.pop(-1)
    except:
        pass

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
        for c_child in node['children']:
            node['children'][c_child] = _recursive_refresh_id(node['children'][c_child])

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
            return None

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


def flatten_nodes(parent_node, result):
    """ create a list of nodes """
    # The node is valid ?
    if not parent_node:
        return False
    # This node has children ?
    if not parent_node.get('children'):
        return False

    for node in sorted(parent_node['children'].keys()):
        c_nd = dict(parent_node['children'][node])
        c_nd['label'] = node
        f_ch = flatten_nodes(parent_node['children'][node], [])
        c_nd['children'] = f_ch or []
        result.append(c_nd)
    return result


def xml_to_res(xml, gparams, root_type, skip_header=False):
    """ import xml file to resources """
    def recursive_xml_to_res(xml, res_dict):
        """
        this is a recursive method to read the xml and generate a dictionary
        """
        c_nd = dict()
        for folder in xml.findall('folder'):
            tb_path = folder.find('path')
            if tb_path is not None:
                c_nd = {'path':[], 'meta': {}, 'id': '', 'children': {}}
                c_nd['path'].append(tb_path.text)
            else:
                c_nd = {'meta': {}, 'id': '', 'children': {}}

            # Populate META properties
            meta = folder.find('meta')
            if meta is not None:
                for meta_params in meta.findall('param'):
                    meta_name = meta_params.find('name')
                    if meta_name is not None:
                        meta_value = meta_params.find('value')
                        if meta_value is not None and meta_value.text is not None:
                            c_nd['meta'][meta_name.text] = meta_value.text
                        else:
                            c_nd['meta'][meta_name.text] = ''

            # If the XML node contains an ID, use it; else, create a random ID
            tb_id = folder.find('id')
            if tb_id is not None:
                id_value = tb_id.find('value')
                if id_value is not None and id_value.text is not None:
                    c_nd['id'] = id_value.text
                else:
                    c_nd['id'] = hexlify(os.urandom(5))
            else:
                c_nd['id'] = hexlify(os.urandom(5))

            # Add children for this node
            res_dict[folder.find('fname').text] = c_nd
            recursive_xml_to_res(folder, res_dict[folder.find('fname').text]['children'])

    # we have to get the information at root level(path,meta,id,version) first
    # version is added only if it exists in xml; the SUT exported files do not
    # have the version tag
    if not skip_header:
        root_dict = {'path':[], 'meta':{}, 'id':'', 'children':{}}
        tb_path = xml.find('path').text
        if tb_path:
            root_dict['path'].append(tb_path)
        else:
            if root_type == ROOT_SUT:
                root_dict['path'].append('')
        meta = xml.find('meta')
        for meta_elem in meta:
            key = meta_elem.find('name').text
            val = meta_elem.find('value').text
            if val:
                root_dict['meta'][key] = val
            else:
                root_dict['meta'][key] = ''
        root_dict['id'] = xml.find('id').text
        if xml.find('version') is not None and xml.find('version').text is not None:
            root_dict['version'] = int(xml.find('version').text)
        #else:
        #    root_dict['version'] = ''

        gparams = root_dict

    # rest of the xml file can be read recursively
    recursive_xml_to_res(xml, gparams['children'])

    return gparams

def res_to_xml(parent_node, xml, skip_header=False):
    """ export resources to xml """
    # The node is valid ?
    if not parent_node:
        return False

    # if we are at root level, we need to get path, meta, id and version fields
    if not skip_header:
        # path is a list with 0 or 1 elements
        path = etree.SubElement(xml, 'path')
        if parent_node.get('path') is not None and len(parent_node.get('path')) == 1:
            path.text = parent_node.get('path')[0]
        else:
            path.text = ''

        meta = etree.SubElement(xml, 'meta')
        # meta is a dictionary
        for k_var, v_var in parent_node.get('meta').iteritems():
            tag = etree.SubElement(meta, 'param')
            prop = etree.SubElement(tag, 'name')
            prop.text = str(k_var)
            val = etree.SubElement(tag, 'value')
            if v_var:
                val.text = str(v_var)
            else:
                val.text = ''
            typ = etree.SubElement(tag, 'type')
            typ.text = 'string'
            desc = etree.SubElement(tag, 'desc')

        tb_id = etree.SubElement(xml, 'id')
        tb_id.text = parent_node.get('id')
        # add version only if it exists in dictionary; the SUT
        # files don't have version
        if parent_node.get('version') is not None:
            version = etree.SubElement(xml, 'version')
            version.text = str(parent_node.get('version'))

    # This node has children ?
    if not parent_node.get('children'):
        return False

    for node in sorted(parent_node['children'].keys()):
        c_nd = dict(parent_node['children'][node])

        # Create empty folder
        folder = etree.SubElement(xml, 'folder')
        # Folder fname
        fname = etree.SubElement(folder, 'fname')
        fname.text = node
        # Folder fdesc
        fdesc = etree.SubElement(folder, 'fdesc')

        # get the path if exists
        if c_nd.get('path'):
            path = etree.SubElement(folder, 'path')
            path.text = c_nd.get('path')[0]

        # get meta information
        meta = etree.SubElement(folder, 'meta')
        for k_var, v_var in c_nd['meta'].iteritems():
            tag = etree.SubElement(meta, 'param')
            prop = etree.SubElement(tag, 'name')
            prop.text = str(k_var)
            val = etree.SubElement(tag, 'value')
            if v_var:
                val.text = str(v_var)
            else:
                val.text = ''
            typ = etree.SubElement(tag, 'type')
            typ.text = 'string'
            desc = etree.SubElement(tag, 'desc')

        # get the id
        if c_nd.get('id'):
            tag = etree.SubElement(folder, 'id')
            val = etree.SubElement(tag, 'value')
            val.text = c_nd['id']
            typ = etree.SubElement(tag, 'type')
            typ.text = 'string'
            desc = etree.SubElement(tag, 'desc')

        res_to_xml(c_nd, folder, True)

    return xml

def _recursive_build_comp(parent, old_path, append_list=[]):
    '''
    parent - pointer in dictionary
    old_path - string with the parent component name
    append_list - list to append the sub-components
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
                child_list = list()
                _recursive_build_comp(new_dict['children'], new_path,\
                child_list)
                # append the list of sub-components
                add_dic['children'] = child_list
            else:
                # no children, just add an empy list
                add_dic['children'] = []

            append_list.append(add_dic)

        return append_list


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
                result = _recursive_search_string(child, query_string)
                if result is True:
                    return True
    return False

#

class ResourceAllocator(_cptools.XMLRPCController):
    """ Class to handle the resources for TB and SUT """
    def __init__(self, project):

        logInfo('Starting Resource Allocator...')
        ti = time.time()

        self.project = project

        self.resources = CONSTANT_DICTIONARY
        self.reserved_res = dict()
        self.locked_res = dict()
        self.systems = CONSTANT_DICTIONARY
        self.acc_lock = thread.allocate_lock() # Task change lock
        self.ren_lock = thread.allocate_lock() # Rename lock
        self.imp_lock = thread.allocate_lock() # Import lock
        self.save_lock = thread.allocate_lock() # Save lock
        self.load_lock = thread.allocate_lock() # Save lock
        self.res_file = '{}/config/resources.json'.format(TWISTER_PATH)
        self._loaded_usrs = dict()
        self._load(True)

        logInfo('Resource Allocator initialization took `{:.4f}` sec.'.format(time.time()-ti))


    @cherrypy.expose
    def default(self, *vpath, **params):
        """ For XML RPX connection to clients"""
        user_agent = cherrypy.request.headers['User-Agent'].lower()
        if 'xmlrpc' in user_agent or 'xml rpc' in user_agent:
            return super(ResourceAllocator, self).default(*vpath, **params)
        # If the connection is not XML-RPC, return the RA main
        output = Template(filename=TWISTER_PATH + '/server/template/ra_main.htm')
        return output.render()

#
    def get_user_name(self):
        """ Return the username """
        user_roles = self.user_roles({})
        user = user_roles.get('user')
        return user

    def _load(self, verbose=False, props={}, force=False):
        """ Load resources file from disk """
        # import time
        # t0 = time.time()
        logFull('CeResources:_load {} {} {}'.format(verbose, props, force))

        if not force:
            try:
                user_roles = self.user_roles(props)
                user = user_roles.get('user')
                if user in self._loaded_usrs:
                    # Get the user rpyc connection suts and count
                    try:
                        usr_conn = self.project._find_local_client(user)
                        usr_suts_len = copy.deepcopy(usr_conn.root.exposed_get_suts_len())
                        loaded_len = 0
                        for c_child in self._loaded_usrs[user]['children']:
                            if c_child.split('.')[-1] == 'user':
                                loaded_len += 1
                        if not usr_suts_len == loaded_len:
                            user_suts = copy.deepcopy(usr_conn.root.get_suts())
                            if user_suts:
                                self.systems['children'].update(user_suts)

                                user_systems = CONSTANT_DICTIONARY
                                user_systems['children'].update(user_suts)
                                self._loaded_usrs.update([(user, user_systems), ])
                    except Exception as exp_err:
                        if verbose:
                            logError('_load ERROR:: {} for user {}'.format(exp_err, self.get_user_name()))

                    self.systems = self._loaded_usrs[user]
                    try:
                        suts_path = self.project.get_user_info(user, 'sys_sut_path')
                        if not suts_path:
                            suts_path = '{}/config/sut/'.format(TWISTER_PATH)
                        sut_all_paths = [p for p in os.listdir(suts_path) if os.path.isfile(os.path.join(suts_path, p))\
                         and p.split('.')[-1] == 'json']
                        for sut_path in sut_all_paths:
                            sut_name = '.'.join(['.'.join(sut_path.split('.')[:-1]  + ['system'])])
                            with open(os.path.join(suts_path, sut_path), 'r') as f_p:
                                self.systems['children'].update([(sut_name, json.load(f_p)), ])
                    except Exception as exp_err:
                        if verbose:
                            logError('_load ERROR:: {} for user {}'.format(exp_err, self.get_user_name()))
                    return True
            except Exception as exp_err:
                if verbose:
                    logError('RA: There are no devices to load for \
                    user {} ! `{}`!'.format(self.get_user_name(), exp_err))

        with self.load_lock:

            if not self.resources.get('children'):
                self.resources = CONSTANT_DICTIONARY
            if not self.systems.get('children'):
                self.systems = CONSTANT_DICTIONARY

            # try to load test bed resources file
            try:
                f_p = open(self.res_file, 'r')
                self.resources = json.load(f_p)
                f_p.close()
                del f_p
                if verbose:
                    logDebug('RA: Devices loaded successfully for user {}.'.format(self.get_user_name()))

            except Exception as exp_err:
                if verbose:
                    logError('RA: There are no devices to load for \
                    user {}! `{}`!'.format(self.get_user_name(), exp_err))
            # try to load SUT file
            try:
                self.systems = CONSTANT_DICTIONARY

                if verbose:
                    logDebug('RA: Systems root loaded successfully for user {}.'.format(self.get_user_name()))

                try:
                    user_roles = self.user_roles(props)
                    user = user_roles.get('user')
                    suts_path = self.project.get_user_info(user, 'sys_sut_path')
                    if not suts_path:
                        suts_path = '{}/config/sut/'.format(TWISTER_PATH)
                    sut_all_paths = [p for p in os.listdir(suts_path)\
                        if os.path.isfile(os.path.join(suts_path, p))\
                             and p.split('.')[-1] == 'json']
                    for sut_path in sut_all_paths:
                        sut_name = '.'.join(['.'.join(sut_path.split('.')[:-1]  + ['system'])])
                        with open(os.path.join(suts_path, sut_path), 'r') as f_p:
                            self.systems['children'].update([(sut_name, json.load(f_p)), ])
                except Exception as exp_err:
                    if verbose:
                        logError('_load ERROR:: {} for user {}'.format(exp_err, self.get_user_name()))

                # Get the user rpyc connection connection
                try:
                    user_roles = self.user_roles(props)
                    user = user_roles.get('user')
                    usr_conn = self.project._find_local_client(user)
                    user_suts = copy.deepcopy(usr_conn.root.get_suts())
                    if user_suts:
                        self.systems['children'].update(user_suts)

                    user_systems = CONSTANT_DICTIONARY
                    if user_suts:
                        user_systems['children'].update(user_suts)
                    self._loaded_usrs.update([(user, user_systems), ])
                except Exception as exp_err:
                    if verbose:
                        logError('_load ERROR:: {} for user {}'.format(exp_err, self.get_user_name()))

                if verbose:
                    logDebug('RA: Systems loaded successfully for user {}.'.format(self.get_user_name()))
            except Exception as exp_err:
                if verbose:
                    logError('RA: There are no SUTs to load for user {} ! `{}`!'.format(self.get_user_name(), exp_err))
        ret = None
        if not ret == True and not ret == None:
            logDebug('_load ERROR: {} for user {}'.format(ret, self.get_user_name()))
        # t1 = time.time()
        # logDebug('|||||||||||||_load time:: ', t1-t0)
        return True


    def _save(self, root_id=ROOT_DEVICE, props={}, resource_name=None, username=None):
        '''
        Function used to write the changes on HDD.
        The save is separate for Devices and SUTs, so the version is not incremented
        for both, before saving.
        '''
        logFull('CeResources:_save {} {} {} {}'.format(root_id, props, resource_name, username))
        log = list()
        # Write changes, using the Access Lock.
        with self.save_lock:

            if root_id == ROOT_DEVICE:
                try:
                    version = self.resources.get('version', 1)
                    logDebug('User {}: Saving {} file, version `{}`.'\
                        .format(self.get_user_name(), ROOT_NAMES[root_id], version))
                    self.resources['version'] = version
                    file_p = open(self.res_file, 'w')
                    json.dump(self.resources, file_p, indent=4)
                    file_p.close()
                    del file_p
                except Exception as exp_err:
                    log.append(exp_err)
                    logError('User {}: Save ERROR: `{}`!'.format(self.get_user_name(), exp_err))

            else:
                try:
                    user_roles = self.user_roles(props)
                    user = user_roles.get('user')
                    if user in self._loaded_usrs:
                        self.systems = self._loaded_usrs[user]
                except Exception as exp_err:
                    log.append(exp_err)
                    logError('User {}: Save ERROR: `{}`!'.format(self.get_user_name(), exp_err))

                if resource_name[0] == '/':
                    resource_name = resource_name.split('/')[-1]

                v = self.systems.get('version', 1)
                self.systems['version'] = v

                systemsChildren = copy.deepcopy(self.systems['children'])
                self.systems['children'] = dict()

                self.systems = CONSTANT_DICTIONARY

                self.systems['children'] = copy.deepcopy(systemsChildren)
                del systemsChildren

                user_suts = list()
                systemSuts = list()
                #logError('||||save sys', user, self.systems)
                for child in self.systems.get('children'):
                    if resource_name and child != resource_name:
                        continue

                    # Check where to save (ce / user)
                    user_roles = self.user_roles(props)
                    user = user_roles.get('user')
                    logDebug('User {}: Trying to save SUT file {}'.format(self.get_user_name(), child))
                    if username and user != username:
                        # different user; dont't save it
                        logDebug('SUT file not saved; different users {} vs {}'.format(user, username))
                        continue

                    # check if it's user or system sut
                    filename = ''
                    if child.split('.')[1] == 'user':
                        suts_path = self.project.get_user_info(user, 'sut_path')
                        filename = suts_path+'/'+child.split('.')[0]+'.json'
                    else:
                        suts_path = self.project.get_user_info(user, 'sys_sut_path')
                        filename = suts_path+'/'+child.split('.')[0]+'.json'

                    suts_path = self.project.get_user_info(user, 'sys_sut_path')
                    if not suts_path:
                        suts_path = '{}/config/sut/'.format(TWISTER_PATH)
                    childPath = os.path.join(suts_path, '.'.join(child.split('.')[:-1] + ['json']))
                    if child.split('.')[-1] == 'system':
                        systemSuts.append((childPath, self.systems['children'][child]))
                    else:
                        user_suts.append(('.'.join(child.split('.')[:-1] + ['json']), self.systems['children'][child]))

                    if child.split('.')[1] == 'user':
                        # Get the user connection
                        try:
                            resp = self.project.localFs.write_user_file(user, filename, \
                             json.dumps(self.systems['children'][child], indent=4), 'w')
                            if resp is not True:
                                log.append(resp)
                        except Exception as exp_err:
                            log.append(exp_err)
                            logError('User {}: Saving ERROR user:: `{}`.'.format(self.get_user_name(), exp_err))

                    if child.split('.')[1] == 'system' and not log:
                        for sys_sut in systemSuts:
                            try:
                                resp = self.project.localFs.write_system_file(filename, \
                                 json.dumps(self.systems['children'][child], indent=4), 'w')
                            except Exception as exp_err:
                                log.append(exp_err)
                                logError('User {}: Saving ERROR system:: `{}`.'.format(self.get_user_name(), exp_err))

                    # update loaded users systems
                    self._loaded_usrs.update([(user, self.systems), ])

                    # targeted resource is saved now; do not continue with
                    # the rest of resources
                    break

        if log:
            return '*ERROR* ' + str(log)

        return True

    def _get_reserved_res_pointer(self, res_query):
        """ Return pointer to a resource in reserved list """
        # the res_pointer not found; this might happen if the
        # resource was renamed; if so, the new name should be in
        # reserved_res; get the ID from there and search again
        res_pointer = None

        if '/' in res_query:
            res_query = res_query.split('/')[1]

        if not self.reserved_res.get(self.get_user_name()):
            return None, None

        for reserved_res in self.reserved_res[self.get_user_name()]:
            reserved_res_p = self.reserved_res[self.get_user_name()][reserved_res]
            if reserved_res_p['path'][0] == res_query:
                query_id = reserved_res_p['id']
                res_path = _get_res_path(self.resources, query_id)
                res_pointer = _get_res_pointer(self.resources, ''.join('/' + res_path[0]))
                return (res_path, res_pointer)

        return None, None


    @cherrypy.expose
    def echo(self, msg):
        '''
        Simple echo function, for testing connection.
        '''
        logDebug('User {}: Echo: {}'.format(self.get_user_name(), msg))
        return 'RA reply: {}'.format(msg)


    @cherrypy.expose
    def tree(self, root_id=ROOT_DEVICE, props={}, *arg, **kw):
        '''
        Return the structure, list based.
        '''
        logFull('CeResources:tree')
        self._load(False, props=props)

        try:
            root_id = int(root_id)
        except:
            root_id = ROOT_DEVICE

        if root_id == ROOT_DEVICE:
            root = self.resources
        else:
            root = self.systems

        result = [{'name': '/', 'id': '1', 'meta': {}, 'children': flatten_nodes(root, [])}]
        cherrypy.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        cherrypy.response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        cherrypy.response.headers['Pragma'] = 'no-cache'
        cherrypy.response.headers['Expires'] = 0
        return json.dumps(result, indent=4, sort_keys=True)


    @cherrypy.expose
    def import_xml(self, xml_file, sut_type='user', root_id=ROOT_DEVICE, props={}, username=None):
        '''
        Import one XML file.
        WARNING! This erases everything!
        '''
        self._load(False, props=props)
        user_roles = self.user_roles(props)
        user = user_roles['user']

        if not os.path.isfile(xml_file):
            msg = 'User {} import XML: XML file `{}` does not exist!'.format(user, xml_file)
            logError(msg)
            return '*ERROR* ' + msg

        logDebug('User {}: importing XML file `{}`...'.format(user, xml_file))
        params_xml = etree.parse(xml_file)
        sut_name = ""

        with self.imp_lock:
            if root_id == ROOT_DEVICE:
                try:
                    self.resources = xml_to_res(params_xml, {}, ROOT_DEVICE)
                except Exception as exp_err:
                    msg = 'User {}: Import XML: Exception `{}`.'.format(self.get_user_name(), exp_err)
                    logError(msg)
                    return '*ERROR* ' + msg
            else:
                try:
                    # default save to user path
                    sut_name = os.path.basename(xml_file).split('.')[:-1]
                    if not sut_name:
                        sut_name = [os.path.basename(xml_file)]

                    # sut name is a list; make it string
                    sut_name = ''.join(sut_name)
                    # if we already have same SUT name, add timestamp to
                    # differentiate
                    tmp_sut_name = sut_name + '.' + sut_type
                    if tmp_sut_name in self.systems.get('children'):
                        actual_time = time.localtime()
                        sut_name = '{}_{}'.format(sut_name, time.strftime('%Y_%m_%d_%H_%M_%S', actual_time))

                    # Add SUT type ( user/system )
                    sut_name = sut_name + '.' + sut_type

                    sut_content = xml_to_res(params_xml, {}, ROOT_SUT)
                    sut_content = sut_content.popitem()[1]
                    sut_content.update([('path', sut_name.split()), ])
                    sut_content = _recursive_refresh_id(sut_content)
                    self.systems['children'].update([(sut_name, sut_content), ])
                except Exception as exp_err:
                    msg = 'User {}: Import XML: Exception `{}`.'.format(self.get_user_name(), exp_err)
                    logError(msg)
                    return'*ERROR* ' + msg

        # Write changes for Device or SUT
        if username:
            if '/' in sut_name:
                name_to_save = sut_name.split('/')[-1]
                ret = self._save(root_id, props, name_to_save, username)
            else:
                ret = self._save(root_id, props, sut_name, username)
        else:
            ret = self._save(root_id, props)
        if not ret == True:
            return ret

        return True


    @cherrypy.expose
    def export_xml(self, xml_file, root_id=ROOT_DEVICE, root=None, props={}):
        '''
        Export as XML file.
        '''
        self._load(False, props=props)
        user_roles = self.user_roles(props)
        user = user_roles['user']

        try:
            file_p = open(xml_file, 'w')
        except:
            msg = 'User {}: export XML: XML file `{}` cannot be written !'.format(user, xml_file)
            logError(msg)
            return '*ERROR* ' + msg

        logDebug('User {}: exporting to XML file `{}`...'.format(user, xml_file))

        skip_header = False
        if root_id == ROOT_DEVICE:
            _root = self.resources
        elif root_id == ROOT_SUT:
            _root = self.systems
            skip_header = True
        elif root:
            _root = root

        xml = etree.Element('root')
        res_to_xml(_root, xml, skip_header)
        file_p.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n\n')
        file_p.write(etree.tostring(xml, pretty_print=True))
        file_p.close()

        return True


    @cherrypy.expose
    def import_sut_xml(self, xml_file, sut_type='user', username=None):
        '''
        Import one sut XML file.
        '''
        user_roles = self.user_roles({})
        user = user_roles['user']
        logDebug('User {}: importing XML file `{}`...'.format(user, xml_file))
        params_xml = etree.parse(xml_file)

        # parse the xml file and build the json format
        xml_ret = xml_to_res(params_xml, {}, ROOT_SUT)

        # build the filename to be saved; xml_file has absolute path; we need
        # to extract the last string after /, remove extension and add .json
        sut_file = xml_file.split('/')[-1].split('.')[0]
        sut_file = sut_file + '.json'

        sut_path = None
        if sut_type == 'system':
            # System SUT path
            sut_path = self.project.get_user_info(username, 'sys_sut_path')
            if not sut_path:
                sut_path = '{}/config/sut/'.format(TWISTER_PATH)
        else:
            # User SUT path
            sut_path = self.project.get_user_info(username, 'sut_path')
            if not sut_path:
                usr_home = userHome(user)
                sut_path = '{}/twister/config/sut/'.format(usr_home)
        sut_file = sut_path + '/' + sut_file

        resp = True
        if sut_type == 'system':
            resp = self.project.localFs.write_system_file(sut_file, json.dumps(xml_ret, indent=4), 'w')
        else:
            resp = self.project.localFs.write_user_file(user, sut_file, json.dumps(xml_ret, indent=4), 'w')

        return resp


    @cherrypy.expose
    def export_sut_xml(self, xml_file, query, username=None):
        '''
        Export as XML file.
        '''
        user_roles = self.user_roles({})
        user = user_roles['user']

        sut_path = None
        sut_type = query.split('.')[-1]
        if sut_type == 'system':
            # System SUT path
            sut_path = self.project.get_user_info(username, 'sys_sut_path')
            if not sut_path:
                sut_path = '{}/config/sut/'.format(TWISTER_PATH)
        else:
            # User SUT path
            sut_path = self.project.get_user_info(username, 'sut_path')
            if not sut_path:
                usr_home = userHome(user)
                sut_path = '{}/twister/config/sut/'.format(usr_home)

        sut_filename = sut_path + '/' + query.split('/')[1].split('.')[0] + '.json'
        logInfo('User {}: export SUT file: {} to {} file.'.format(user, sut_filename, xml_file))

        # read the content of the user SUT file and load it in json
        if sut_type == 'system':
            resp = self.project.localFs.read_system_file(sut_filename, 'r')
        else:
            resp = self.project.localFs.read_user_file(user, sut_filename, 'r')
        json_resp = json.loads(resp)

        # generate the xml structure
        xml = etree.Element('root')
        result = res_to_xml(json_resp, xml)

        # write the xml file
        xml_header = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n\n'
        resp = self.project.localFs.write_user_file(user, xml_file, xml_header, 'w')
        if resp != True:
            logError(resp)
            return resp

        resp = self.project.localFs.write_user_file(user, xml_file, etree.tostring(xml, pretty_print=True), 'w')
        if resp != True:
            logError(resp)
            return resp

        return True


    @cherrypy.expose
    def export_glob_sut_xml(self, xml_file, props={}):
        '''
        Export all suts as XML file.
        '''
        return self.export_xml(xml_file, ROOT_SUT, props)


    def user_roles(self, props={}):
        """ Return roles of user """
        logFull('CeResources:user_roles')
        # Check the username from CherryPy connection
        try:
            user = cherrypy.session.get('username')
        except:
            user = ''

        # Fallback
        if not user:
            user = props.get('__user', '')

        user_roles = self.project.authenticate(user)
        default = {'user': user, 'roles': [], 'groups': []}
        if not user_roles:
            return default
        user_roles.update({'user': user})
        return user_roles

#

    @cherrypy.expose
    def get_resource(self, query, root_id=ROOT_DEVICE, flatten=True, props={}, username=None):
        '''
        Show all the properties, or just 1 property of a resource.
        Must provide a Resource ID, or a Query.
        The function is used for both Devices and SUTs, by providing the ROOT ID.
        '''
        logFull('CeResources:get_resource')
        self._load(False, props=props)
        user_roles = self.user_roles(props)
        user = user_roles['user']

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

            msg = 'User {}: Get {}: There are no devices defined !'.format(self.get_user_name(), root_name)
            logError(msg)
            return '*ERROR* ' + msg

        if not query:
            msg = 'User {}: Get {}: Cannot get a null resource !'.format(user, root_name)
            logError(msg)
            return '*ERROR* ' + msg

        logDebug('User {}: Get {} `{}`.'.format(self.get_user_name(), root_name, query))

        query = str(query)

        # If the query asks for a specific Meta Tag
        if query.count(':') > 1:
            msg = 'User {}: Get {}: Invalid query ! Cannot access more than '\
                '1 meta info !'.format(self.get_user_name(), root_name)
            logError(msg)
            return '*ERROR* ' + msg

        if ':' in query:
            meta = query.split(':')[1]
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
                    if not result:
                        return '*ERROR* no result'
                    result = result['children'].get(part)
            # If this is a SUT
            else:
                for part in parts:
                    if not result:
                        return '*ERROR* no result'
                    res = result['children'].get(part)
                    if not res:
                        # Ok, this might be a Device path, instead of SUT path!
                        tb_id = result['meta'].get('_id')
                        # If this SUT doesn't have a Device ID assigned, bye bye!
                        if not tb_id:
                            return '*ERROR* no result'
                        res_data = _recursive_find_id(self.resources, tb_id, [])
                        # If the Device ID is invalid, bye bye!
                        if not res_data:
                            return '*ERROR* no result'
                        # Find out the Device path from Resources and add the rest of the parts
                        link_path = '/' + '/'.join(res_data.get('path', '')) + '/' + part
                        result = self.get_resource(link_path, flatten=False)
                        # After this, scan the next PART from PARTS
                    else:
                        result = res

            if not result:
                return '*ERROR* no result'
            # Delete empty node paths
            result['path'] = [p for p in parts if p]

        result = dict(result)

        if not meta:
            # Flatten the children ?
            if flatten:
                result['children'] = sorted([result['children'][node]['id'] \
                for node in result.get('children') or []], \
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
                if not tb_id:
                    return '*ERROR* no device id'
                return self.get_resource(tb_id +':'+ meta)


    @cherrypy.expose
    def get_sut(self, query, props={}, username=None):
        '''
        Show all the properties, or just 1 property of a SUT.
        Must provide a SUT ID, or a SUT Path.
        '''
        logDebug('CeResources: Get SUT for: `{}` `{}`!'.format(query, self.get_user_name()))
        # query, root_id, flatten, props, username
        ret = self.get_resource(query, ROOT_SUT, True, props, username)
        return ret


    @cherrypy.expose
    def get_sut_by_name(self, query, username):
        '''
        Get the contant of one SUT file using it's name
        Must provide a SUT name.<type> ( type = user/system) and username
        '''
        logDebug('CeResources: GetSutByName {} {}'.format(query, self.get_user_name(),))
        usr_home = userHome(username)

        sut_path = None
        sut_type = query.split('.')[-1]
        if sut_type == 'system':
            # System SUT path
            sut_path = self.project.get_user_info(username, 'sys_sut_path')
            if not sut_path:
                sut_path = '{}/config/sut/'.format(TWISTER_PATH)
        else:
            # User SUT path
            sut_path = self.project.get_user_info(username, 'sut_path')
            if not sut_path:
                sut_path = '{}/twister/config/sut/'.format(usr_home)

        # if sut path doesn't end with '/' character, we have to add it
        if sut_path[-1] != '/':
            sut_path += '/'
        file_name = query.split('.')[0] + '.json'
        sut_file = sut_path + file_name

        sut_content = False
        user = self.get_user_name()

        if os.path.isdir(sut_path):
            if sut_type == 'system':
                # system SUT file
                try:
                    file_p = open(sut_file, 'r')
                    sut_content = json.load(file_p)
                    file_p.close()
                    del file_p
                except Exception as exp_err:
                    return '*ERROR* Cannot get access to SUT path for user {} Exception {}'.format(user, exp_err)
            else:
                # user SUT file; we have to check if the cleacase plugin
                # is activated; if so, use it to read the SUT file; else
                # use the UserService to read it
                cc_cfg = self.project.get_clearcase_config(user, 'sut_path')
                if cc_cfg:
                    view = cc_cfg['view']
                    actv = cc_cfg['actv']
                    path = cc_cfg['path']
                    user_view_actv = '{}:{}:{}'.format(user, view, actv)
                    resp = self.project.clearFs.read_user_file(user_view_actv, path +'/'+ file_name)
                    sut_content = json.loads(resp)
                else:
                    resp = self.project.localFs.read_user_file(user, sut_path + file_name)
                    sut_content = json.loads(resp)

            if sut_content is False or (isinstance(sut_content, str) and sut_content.startswith('*ERROR*')):
                return sut_content

            if isinstance(sut_content, dict):
                # Now we have the SUT content; we need to format it for GUI
                rec_list = list()
                ret_dict = dict()
                if sut_content.get('path'):
                    ret_dict['path'] = sut_content['path'][0]
                else:
                    ret_dict['path'] = query
                ret_dict['meta'] = sut_content['meta']
                ret_dict['id'] = sut_content['id']
                ret_dict['children'] = _recursive_build_comp(sut_content.get('children'), ret_dict['path'], rec_list)

                # make sure that self.systems is in sync with the opened
                # content
                if self.systems['children'].get(query) is not None:
                    self.systems['children'][query] = sut_content

                return ret_dict

        # if we get here, we cannot get read access to the SUT directory
        return '*ERROR* Cannot get access to SUT path for user {}'.format(self.get_user_name())


#

    @cherrypy.expose
    def set_resource(self, name, parent=None, props={}, root_id=ROOT_DEVICE, username=None):
        '''
        Create or change a resource, using a name, a parent Path or ID and some properties.
        The function is used for both Devices and SUTs, by providing the ROOT ID.
        '''
        logFull('CeResources:set_resource {} {} {} {} {}'.format(name, parent, props, root_id, username))
        self._load(False, props=props)

        user_roles = self.user_roles(props)

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
            _is_res_locked = self.is_resource_locked(parent, root_id)
            if _is_res_locked and _is_res_locked != username:
                msg = 'User {}: Reserve resource: The resource is locked for '\
                    '{} !'.format(self.get_user_name(), _is_res_locked)
                logError(msg)
                return '*ERROR* ' + msg

        with self.acc_lock:
            # If this is the root resource, update the properties
            if name == '/' and parent == '/':
                if isinstance(props, dict):
                    pass
                elif isinstance(props, str) or isinstance(props, unicode):
                    props = props.strip()
                    try:
                        props = ast.literal_eval(props)
                    except Exception as exp_err:
                        msg = 'User {}: Set {}: Cannot parse properties: '\
                        '`{}`, `{}` !'.format(self.get_user_name(),\
                                       root_name, props, exp_err)
                        logError(msg)
                        return '*ERROR* ' + msg
                else:
                    msg = 'User {}: Set {}: Invalid properties `{}` !'.format(self.get_user_name(), root_name, props)
                    logError(msg)
                    return '*ERROR* ' + msg

                epnames_tag = '_epnames_{}'.format(username)

                resources['meta'].update(props)
                # if _id key is present in meta and it has no value,
                #we have to remove it from meta dictionary
                if '_id' in resources['meta'].keys() and not resources['meta'].get('_id', False):
                    resources['meta'].pop('_id')

                # If the epnames tag exists in resources
                if epnames_tag in resources['meta']:
                    # And the tag is empty
                    if not resources['meta'][epnames_tag]:
                        logDebug('User {}: Deleting `{}` tag from resources.'.format(self.get_user_name(), epnames_tag))
                        del resources['meta'][epnames_tag]

                # Write changes for Device or SUT
                if username:
                    if '/' in name:
                        name_to_save = name.split('/')[-1]
                        ret = self._save(root_id, props, name_to_save, username)
                    else:
                        ret = self._save(root_id, props, name, username)
                else:
                    ret = self._save(root_id, props)
                logInfo('User {}: Set {}: Updated ROOT with properties: `{}`.'\
                    .format(self.get_user_name(), root_name, props))
                if not ret == True:
                    return ret
                return True

            if parent == '/' or parent == '1': # can alsow be 1
                parent_p = _get_res_pointer(resources, parent)

                if (root_id == ROOT_SUT and
                        (not name.split('.')[-1] == 'user' and not name.split('.')[-1] == 'system')):
                    name = '.'.join([name, 'user'])
            else:
                parent_p = self._get_reserved_resource(parent, props, root_id)

            if not parent_p:
                msg = 'User {}: Set {}: Cannot access parent path or ID `{}` '\
                    '!'.format(self.get_user_name(), root_name, parent)
                logError(msg)
                return '*ERROR* ' + msg

            if not isinstance(parent_p.get('path'), list):
                parent_p['path'] = parent_p.get('path', '').split('/')

            if '/' in name:
                logDebug('User {}: Set {}: Stripping slash characters from '\
                    '`{}`...'.format(self.get_user_name(), root_name, name))
                name = name.replace('/', '')

            if isinstance(props, dict):
                pass
            elif isinstance(props, str) or isinstance(props, unicode):
                props = props.strip()
                try:
                    props = ast.literal_eval(props)
                except Exception as exp_err:
                    msg = 'User {}: Set {}: Cannot parse properties: `{}`, '\
                    '`{}` !'.format(self.get_user_name(), root_name, props, exp_err)
                    logError(msg)
                    return '*ERROR* ' + msg
            else:
                msg = 'User {}: Set {}: Invalid properties `{}` !'.format(self.get_user_name(), root_name, props)
                logError(msg)
                return '*ERROR* ' + msg

            if not 'children' in parent_p:
                parent_p['children'] = {}

            if '/' in parent:
                for c_child in [p for p in parent.split('/') if p][1:]:
                    parent_p = parent_p['children'][c_child]
            else:
                resource_path = _recursive_find_id(parent_p, parent, [])['path']
                for c_child in resource_path:
                    parent_p = parent_p['children'][c_child]

            # If the resource exists, patch the new properties!
            if name in parent_p['children']:
                if parent == '/' or parent == '1':
                    child_p = self._get_reserved_resource('/' + name, props, root_id)
                else:
                    child_p = parent_p['children'][name]

                if not child_p:
                    return '*ERROR* no found'

                old_child = copy.deepcopy(child_p)

                logDebug('User {}: Set Resource update props:: {} for child '\
                    '{}'.format(self.get_user_name(), props, child_p))

                epnames_tag = '_epnames_{}'.format(username)

                child_p['meta'].update(props)
                # if _id key is present in meta and it has no value, we have
                # to remove it from meta dictionary
                if '_id' in child_p['meta'].keys() and not child_p['meta'].get('_id', False):
                    child_p['meta'].pop('_id')

                # If the epnames tag exists in resources
                if epnames_tag in child_p['meta']:
                    # And the tag is empty
                    if not child_p['meta'][epnames_tag]:
                        logDebug('User {}: Deleting `{}` tag from resources.'.format(self.get_user_name(), epnames_tag))
                        del child_p['meta'][epnames_tag]

                return True

            elif self._get_reserved_res_pointer(name) != (None, None):
                # resource was just created and reserved
                res_path, res_pointer = self._get_reserved_res_pointer(name)
                res_pointer['meta'] = props
                return True
            else:
                # resource is new, create it.
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
                        logDebug('User {}: Deleting `{}` tag from new '\
                            'resource.'.format(self.get_user_name(), epnames_tag))
                        del parent_p['children'][name]['meta'][epnames_tag]

                ret = None
                if parent == '/' or parent == '1':
                    # if this is a SUT file, we need to add path
                    #if root_id == ROOT_SUT:
                    sut_path = list()
                    sut_path.append(name)
                    parent_p['children'][name]['path'] = sut_path

                    # Write changes for Device or SUT
                    ret = self._save(root_id, props, name, username)
                    if isinstance(ret, str):
                        if '*ERROR*' in ret:
                            # do clean up
                            parent_p['children'].pop(name)
                    else:
                        logDebug('User {}: Created {} `{}`, id `{}` : `{}` .'\
                            .format(self.get_user_name(), root_name,\
                             name, res_id, props))

                if not ret == True and not ret == None:
                    return ret
                return res_id


    @cherrypy.expose
    def set_sut(self, name, parent=None, props={}, username=None):
        '''
        Create or change a SUT, using a name, a parent Path or ID and some properties.
        '''
        logDebug('CeResources:set_sut {} {} {} {}'.format(name, parent, props, username))
        if not props:
            props = {}
        if not parent:
            parent = '/'
        return self.set_resource(name, parent, props, ROOT_SUT, username)


    @cherrypy.expose
    def rename_resource(self, res_query, new_name, props={}, root_id=ROOT_DEVICE):
        '''
        Rename a resource.
        '''
        logDebug('CeResources:rename_resource {} {} {}'.format(res_query, new_name, props))
        self._load(False, props=props)

        user_roles = self.user_roles(props)
        user = user_roles['user']

        # If the root is not provided, use the default root
        if root_id == ROOT_DEVICE:
            if 'CHANGE_TESTBED' not in user_roles.get('roles', []):
                msg = 'Privileges ERROR! Username `{}` cannot use Rename Resource!'.format(user)
                logDebug(msg)
                return '*ERROR* ' + msg
            resources = self.resources
        else:
            if 'CHANGE_SUT' not in user_roles.get('roles', []):
                msg = 'Privileges ERROR! Username `{}` cannot use Rename SUT!'.format(user)
                logDebug(msg)
                return '*ERROR* ' + msg
            resources = self.systems

        root_name = ROOT_NAMES[root_id]

        # If no resources...
        if not resources.get('children'):
            msg = 'User {}: Rename {}: There are no resources defined !'.format(self.get_user_name(), root_name)
            logError(msg)
            return '*ERROR* ' + msg

        if '/' in new_name:
            msg = 'User {}: Rename {}: New resource name cannot contain `/` !'.format(self.get_user_name(), root_name)
            logError(msg)
            return '*ERROR* ' + msg

        if ':' in new_name:
            msg = 'User {}: Rename {}: New resource name cannot contain `:` !'.format(self.get_user_name(), root_name)
            logError(msg)
            return '*ERROR* ' + msg

        if ':' in res_query:
            meta = res_query.split(':')[1]
            res_query = res_query.split(':')[0]
        else:
            meta = ''

        _is_res_locked = self.is_resource_locked(res_query, root_id)
        if _is_res_locked and _is_res_locked != user:
            msg = 'User {}: Reserve resource: The resource is locked for {} !'\
                .format(self.get_user_name(), _is_res_locked)
            logError(msg)
            return '*ERROR* ' + msg

        res_p = self._get_reserved_resource(res_query, props, root_id)
        if not res_p:
            msg = 'User {}: Rename {}: Cannot access reserved resource, path '\
                'or ID `{}` !'.format(self.get_user_name(), root_name, res_query)
            logError(msg)
            return '*ERROR* ' + msg

        res_path = None
        # if the renamed resource is the testbed itself, it must be renamed
        # in self.resources location; check if the res_query is a testbed; that
        # means it has to be at first level of self.resources and it's
        # id is equal with the res_query
        for tb_res in self.resources['children']:
            if res_query == self.resources['children'][tb_res]['id']:
                res_path = _get_res_path(resources, res_query)
                # found the resource; break out from loop
                break

        if res_path == None:
            # find the resource path in reserved resources
            try:
                for res in self.reserved_res[user]:
                    res_path = _get_res_path(self.reserved_res[user][res], res_query)
                    if res_path:
                        res_pointer = self.reserved_res[user][res]
                        res_path.insert(0, res)
                        break

                    # it can be a meta parameter for the TB; we need to
                    # check this case because get_res_path doesn't return
                    # correct in this case
                    if res == res_query:
                        res_pointer = self.reserved_res[user][res]
                        res_path = res_pointer.get('path')
                        res_path.insert(0, res)
                        break
            except Exception, exp_err:
                res_path = None

        if res_path == None:
            msg = 'User {}: Rename {}: Cannot access resource `{}` !'\
                  .format(self.get_user_name(), root_name, res_query)
            logError(msg)
            return '*ERROR* ' + msg

        node_path = [p for p in res_path if p]
        # Renamed node path; applicable for SUT only
        if not meta and len(node_path) == 1 and root_id == ROOT_SUT and \
        (not new_name.split('.')[-1] == 'user' and \
        not new_name.split('.')[-1] == 'system'):
            new_name = '.'.join([new_name, 'user'])
        new_path = list(node_path)
        new_path[-1] = new_name

        if not node_path:
            msg = 'User {}: Rename {}: Cannot find resource node path `{}` !'\
                .format(self.get_user_name(), root_name, node_path)
            logError(msg)
            return '*ERROR* ' + msg

        if node_path == new_path:
            logDebug('User {}: No changes have been made to {} `{}`.'.format(self.get_user_name(), root_name, new_name))
            return True

        if node_path[1:]:
            exec_string = 'res_p["children"]["{}"]'.format('"]["children"]["'.join(node_path[1:]))
        else:
            exec_string = 'res_p'

        with self.ren_lock:

            # If must rename a Meta info
            if meta:
                exec('val = {}["meta"].get("{}")'.format(exec_string, meta))

                exec('{0}["meta"]["{1}"] = {0}["meta"]["{2}"]'.format(exec_string, new_name, meta))
                exec('del {}["meta"]["{}"]'.format(exec_string, meta))

                logDebug('User {0}: Renamed {1} meta `{2}:{3}` to `{2}:{4}`.'\
                    .format(self.get_user_name(), root_name, '/'\
                    .join(node_path), meta, new_name))
            # If must rename a normal node
            else:
                if new_path[1:]:
                    # update a component; first update the component name
                    new_string = 'res_p["children"]["{}"]'.format('"]["children"]["'.join(new_path[1:]))
                    exec(new_string + ' = ' + exec_string)
                    exec('del ' + exec_string)
                else:
                    # update the path for a TB
                    res_p.update([('path', [new_name]), ])

                logDebug('User {}: Renamed {} path `{}` to `{}`.'\
                    .format(self.get_user_name(), root_name, '/'\
                    .join(node_path), '/'.join(new_path)))

        return True


    @cherrypy.expose
    def rename_sut(self, res_query, new_name, username=None):
        '''
        Rename a SUT.
        '''
        logDebug('CeResources:rename_sut {} {} {}'.format(res_query, new_name, username))

        return self.copy_sut_file(res_query, new_name, username, True)


    @cherrypy.expose
    def delete_resource(self, res_query, props={}, root_id=ROOT_DEVICE, username=None):
        '''
        Permanently delete a resource.
        '''
        logDebug('CeResources:delete_resource {} {} {} {}'.format(res_query, props, root_id, username))
        self._load(False, props=props)

        user_roles = self.user_roles(props)

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
            msg = 'User {}: Del {}: There are no resources defined !'.format(self.get_user_name(), root_name)
            logError(msg)
            return '*ERROR* ' + msg

        if ':' in res_query:
            meta = res_query.split(':')[1]
            res_query = res_query.split(':')[0]
        else:
            meta = ''

        user = user_roles.get('user')

        # Check if resource is locked; if so, it cannot be deleted
        _is_res_locked = self.is_resource_locked(res_query, root_id)
        if _is_res_locked and _is_res_locked != user:
            msg = 'User {}: Reserve resource: The resource is locked for {} !'\
                .format(self.get_user_name(), _is_res_locked)
            logError(msg)
            return '*ERROR* ' + msg

        # Check if resource is reserved; if so, it cannot be deleted
        _is_res_locked = self.is_resource_reserved(res_query, root_id)
        if _is_res_locked and _is_res_locked != user:
            msg = 'User {}: Cannot delete: The resource is reserved for '\
                  '{} !'.format(self.get_user_name(), _is_res_locked)
            logError(msg)
            return '*ERROR* ' + msg

        # Check if is reserved
        try:
            for res in self.reserved_res[user]:
                res_path = _get_res_path(self.reserved_res[user][res], res_query)
                if res_path:
                    res_pointer = self.reserved_res[user][res]
                    break

                # it can be a meta parameter for the TB; we need to
                # check this case because get_res_path doesn't return
                # correct in this case
                if res == res_query:
                    res_pointer = self.reserved_res[user][res]
                    res_path = res_pointer.get('path')
                    break
        except Exception, exp_err:
            res_path = None

        if res_path:
            # resource can be at test bed level or at children of test bed
            # level; we have to differentiate
            if res_pointer.get('path') == res_path:
                # test bed level
                exec_string = 'res_pointer'
            else:
                # child of test bed level
                exec_string = 'res_pointer["children"]["{}"]'.format('"]["children"]["'.join(res_path))

            # If must delete a Meta info
            if meta:
                logDebug('User {}: Executing `{}` ...'\
                    .format(self.get_user_name(), 'val = {}["meta"].get("{}")'\
                    .format(exec_string, meta)))
                exec('val = {}["meta"].get("{}")'.format(exec_string, meta))

                logDebug('User {}: Executing `{}` ...'\
                    .format(self.get_user_name(), 'del {}["meta"]["{}"]'\
                    .format(exec_string, meta)))
                exec('del {}["meta"]["{}"]'.format(exec_string, meta))
                logDebug('User {}: Deleted {} meta `{}:{}`.'\
                         .format(self.get_user_name(), root_name,\
                         '/'.join(res_path), meta))

            # If must delete a normal node
            else:
                logDebug('User {}: Executing `{}` ...'.format(self.get_user_name(), 'del ' + exec_string))
                exec('del ' + exec_string)
                logDebug('User {}: Deleted {} path `{}`.'.\
                format(self.get_user_name(), root_name, '/'.join(res_path)))

            return True

        res_path = _get_res_path(resources, res_query)
        res_pointer = _get_res_pointer(resources, ''.join('/' + res_path[0]))

        # Find the resource pointer.
        if root_id == ROOT_DEVICE:
            res_p = self.get_resource(res_query, props=props)
        else:
            res_p = self.get_sut(res_query, props=props)

        if not res_p:
            msg = 'User {}: Del {}: Cannot find resource path or ID `{}` !'\
                  .format(self.get_user_name(), root_name, res_query)
            logError(msg)
            return '*ERROR* ' + msg

        # Correct node path
        node_path = [p for p in res_p['path'].split('/') if p]

        if not node_path:
            msg = 'User {}: Del {}: Cannot find resource node path `{}` !'\
                  .format(self.get_user_name(), root_name, node_path)
            logError(msg)
            return '*ERROR* ' + msg

        # Must use the real pointer instead of `resource` pointer in order to update the real data
        if root_id == ROOT_DEVICE:
            exec_string = 'self.resources["children"]["{}"]'.format('"]["children"]["'.join(node_path))
        else:
            exec_string = 'self.systems["children"]["{}"]'.format('"]["children"]["'.join(node_path))

        # If must delete a Meta info
        if meta:
            exec('val = {}["meta"].get("{}")'.format(exec_string, meta))
            exec('del {}["meta"]["{}"]'.format(exec_string, meta))
            logDebug('User {}: Deleted {} meta `{}:{}`.'.\
            format(self.get_user_name(), root_name, '/'.join(node_path), meta))

        # If must delete a normal node
        else:
            exec('del ' + exec_string)
            logDebug('User {}: Deleted {} path `{}`.'.format(self.get_user_name(), root_name, '/'.join(node_path)))

        # Write changes.
        if username:
            if '/' in res_query:
                name_to_save = res_query.split('/')[-1]
                ret = self._save(root_id, props, name_to_save, username)
            else:
                ret = self._save(root_id, props, res_query, username)
        else:
            ret = self._save(root_id, props)

        # Delete file if it's SUT file
        if not meta and len(node_path) == 1 and root_id == ROOT_SUT:
            if node_path[0].split('.')[-1] == 'system':
                suts_path = self.project.get_user_info(user, 'sys_sut_path')
                if not suts_path:
                    suts_path = '{}/config/sut/'.format(TWISTER_PATH)
                file_name = node_path[0].split('.')[:-1][0]
                file_name += '.json'

                os.remove(suts_path+'/'+file_name)
            else:
                # Get the user rpyc connection connection
                try:
                    usr_conn = self.project._find_local_client(user)
                    usr_conn.root.delete_sut('.'.join(node_path[0].split('.')[:-1]))
                except Exception as exp_err:
                    logError('User {}: Saving ERROR:: `{}`.'.format(self.get_user_name(), exp_err))

        if not ret == True:
            return ret

        return True


    @cherrypy.expose
    def delete_sut(self, res_query, username=None):
        '''
        Permanently delete a SUT.
        '''
        logFull('CeResources:delete_sut {}'.format(res_query))

        usr_home = userHome(self.get_user_name())

        logDebug('Prepare to delete SUT `{}`.'.format(res_query))

        def delete_sut_memory(sut_to_remove):
            """ temporary fix; the SUT must be removed from self.systems """
            parent_p = _get_res_pointer(self.systems, '/')
            if parent_p is not None and parent_p['children'].get(sut_to_remove) is not None:
                parent_p['children'].pop(sut_to_remove)
        # end temporary fix

        # SUT file can be user or system file
        if res_query.split('.')[-1] == 'system':
            suts_path = self.project.get_user_info(self.get_user_name(), 'sys_sut_path')
            if not suts_path:
                suts_path = '{}/config/sut/'.format(TWISTER_PATH)
            try:
                os.remove(suts_path + res_query.split('.')[0] + '.json')
                delete_sut_memory(res_query.split('/')[-1])
                return True
            except Exception as exp_err:
                msg = 'User {}: Cannot delete SUT file: `{}` !'\
                .format(self.get_user_name(), res_query.split('.')[0] + '.json')
                logError(msg)
                return '*ERROR* ' + msg
            return True
        else:
            usr_sut_path = self.project.get_user_info(self.get_user_name(), 'sut_path')
            if not usr_sut_path:
                usr_sut_path = '{}/twister/config/sut/'.format(usr_home)
            delete_sut_memory(res_query.split('/')[-1])
            return self.project.localFs.delete_user_file(self.get_user_name(),\
            usr_sut_path + res_query.split('.')[0] + '.json')


    @cherrypy.expose
    def is_sut_reserved(self, res_query):
        """ returns the user or false """

        logFull('CeResources:is_sut_reserved')
        return self.is_resource_reserved(res_query, ROOT_SUT)


    @cherrypy.expose
    def reserve_sut(self, res_query, username=None):
        '''
        Reserve a SUT.
        '''
        logFull('CeResources:reserve_sut')
        return self.reserve_resource(res_query, {}, ROOT_SUT, username)


    @cherrypy.expose
    def save_reserved_sut_as(self, name, res_query, username=None):
        '''
        Save a reserved SUT as.
        '''
        logDebug('CeResources:save_reserved_sut_as {} {} {}'.format(name, res_query, username))

        # we need to create the SUT file if it doesn't exists
        target_name = '/'+name+'.user'
        ret_resource = self.get_resource(target_name, ROOT_SUT, False)
        if isinstance(ret_resource, str):
            if '*ERROR*' in ret_resource:
                # the targeted SUT doesn't exists, create it and get it's
                # structure
                self.set_resource(target_name, '/', '{}', ROOT_SUT)
                ret_resource = self.get_resource(target_name, ROOT_SUT, False)
                # this should NOT happen, if so, something is very bad
                if isinstance(ret_resource, str):
                    if '*ERROR*' in ret_resource:
                        msg = 'User {}: SUT file {} cannot be saved!'.format(self.get_user_name(), name + '.json')
                        logError(msg)
                        return '*ERROR* ' + msg

        # reserve the target SUT
        self.reserve_resource(target_name, '{}', ROOT_SUT)

        # search for original SUT in reserved resources and
        # get the children and meta sections to copy into the new SUT
        if '/' in res_query:
            res_query = res_query.split('/')[-1]
        orig_children = dict()
        orig_meta = dict()
        for reserved_res in self.reserved_res[self.get_user_name()]:
            reserved_res_p = self.reserved_res[self.get_user_name()][reserved_res]
            if reserved_res_p['path'][0] == res_query:
                # found the original SUT; get the children
                orig_children = reserved_res_p['children']
                orig_meta = reserved_res_p['meta']
                break

        # search for target SUT in reserved resources and
        # overwrite the children and meta sections with values
        # from original SUT
        if '/' in target_name:
            target_name = target_name.split('/')[-1]
        for reserved_res in self.reserved_res[self.get_user_name()]:
            reserved_res_p = self.reserved_res[self.get_user_name()][reserved_res]
            if reserved_res_p['path'][0] == target_name:
                # found the original SUT; write the children
                reserved_res_p['children'] = orig_children
                reserved_res_p['meta'] = orig_meta
                break

        # we need to realease & discard the original SUT and to save & release
        # the targeted SUT
        self.discard_release_reserved_res('/'+res_query, '{}', ROOT_SUT, self.get_user_name())
        return self.save_reserved_resource('/'+target_name, '{}', ROOT_SUT, self.get_user_name())


    @cherrypy.expose
    def save_reserved_sut(self, res_query, username=None):
        '''
        Save a reserved SUT.
        '''
        logFull('CeResources:save_reserved_sut')
        props = {}
        return self.save_reserved_resource(res_query, props, ROOT_SUT, username)


    @cherrypy.expose
    def save_release_reserved_sut(self, res_query, username=None):
        '''
        Save a reserved SUT.
        '''
        logFull('CeResources:save_release_reserved_sut')
        return self.save_release_reserved_resource(res_query, {}, ROOT_SUT, username)


    @cherrypy.expose
    def discard_release_reserved_sut(self, res_query, username=None):
        '''
        Discard a reserved SUT.
        '''
        logFull('CeResources:discard_release_reserved_sut')
        props = {}
        return self.discard_release_reserved_res(res_query, props, ROOT_SUT, username)


    @cherrypy.expose
    def is_sut_locked(self, res_query):
        """ returns the user or false """

        logFull('CeResources:is_sut_locked')
        return self.is_resource_locked(res_query, ROOT_SUT)


    @cherrypy.expose
    def lock_sut(self, res_query, props={}, username=None):
        '''
        Lock a SUT.
        '''
        logFull('CeResources:lock_sut')
        return self.lock_resource(res_query, props, ROOT_SUT, username)


    @cherrypy.expose
    def unlock_sut(self, res_query, props={}, username=None):
        '''
        Unlock a SUT.
        '''
        logFull('CeResources:unlock_sut')
        return self.unlock_resource(res_query, props, ROOT_SUT, username)


# # # Allocation and reservation of resources # # #


    def _get_reserved_resource(self, res_query, props={}, root_id=ROOT_DEVICE):
        '''
        Returns the reserved resource.
        '''
        logFull('CeResources:_get_reserved_resource')
        if root_id == ROOT_DEVICE:
            resources = self.resources
        else:
            resources = self.systems

        # If no resources...
        if not resources.get('children'):
            msg = 'User {}: Get reserved resource: There are no resources defined !'.format(self.get_user_name())
            logError(msg)
            return False

        user_roles = self.user_roles(props)
        user = user_roles.get('user')

        if ':' in res_query:
            res_query = res_query.split(':')[0]

        res_path = _get_res_path(resources, res_query)
        if not res_path:
            if '/' in res_query:
                res_path = [p for p in res_path.split('/') if p]
            else:
                for p_res in self.reserved_res[user]:
                    res_path = _get_res_path(self.reserved_res[user][p_res], res_query)

                    if res_path:
                        return self.reserved_res[user][p_res]

        res_pointer = _get_res_pointer(resources, ''.join('/' + res_path[0]))
        if not res_pointer:
            res_path, res_pointer = self._get_reserved_res_pointer(res_query)

        if not res_pointer:
            msg = 'User {}: Get reserved resource: Cannot find resource path '\
                  'or ID `{}` !'.format(self.get_user_name(), res_query)
            logError(msg)
            return False

        if not self.reserved_res.get(user):
            msg = 'User {}: Get reserved resource: Resource `{}` is not '\
                  'reserved !'.format(self.get_user_name(), res_query)
            logError(msg)
            return False

        if root_id == ROOT_DEVICE and '/' in res_query:
            res_pointer.update([('path', res_path), ])

        join_path = self.reserved_res[user][res_pointer['id']].get('path', '')
        if isinstance(join_path, str):
            join_path = [join_path]

        self.reserved_res[user][res_pointer['id']]['path'] = ['/'.join(join_path)]

        return self.reserved_res[user][res_pointer['id']]


    @cherrypy.expose
    def is_resource_reserved(self, res_query, root_id=ROOT_DEVICE):
        """ returns the user or false """
        logFull('CeResources:is_resource_reserved')
        if root_id == ROOT_DEVICE:
            resources = self.resources
        else:
            resources = self.systems

        # If no resources...
        if not resources.get('children'):
            msg = 'User {}: Is resource reserved: There are no resources defined !'.format(self.get_user_name())
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
            msg = 'User {}: Is resource reserved: Cannot find resource path '\
                  'or ID `{}` !'.format(self.get_user_name(), res_query)
            logError(msg)
            return '*ERROR* ' + msg

        res_pointer.update([('path', [res_path[0]]), ])

        reserved_for_usr = [u for u in self.reserved_res if res_pointer['id'] in self.reserved_res[u]]

        if not reserved_for_usr:
            return False

        if len(reserved_for_usr) == 1:
            reserved_for_usr = reserved_for_usr[0]
        else:
            logDebug('Wrong length for reservedForUser: {}'.format(len(reserved_for_usr)))
            return False

        return reserved_for_usr


    @cherrypy.expose
    def reserve_resource(self, res_query, props={}, root_id=ROOT_DEVICE, username=None):
        """ Reserve a resource """
        logDebug('CeResources:reserve_resource {} {} {} {}'.format(res_query, props, root_id, username))
        self._load(False, props=props)

        if root_id == ROOT_DEVICE:
            resources = self.resources
        else:
            resources = self.systems

        # If no resources...
        if not resources.get('children'):
            msg = 'User {}: Reserve resource: There are no resources defined !'.format(self.get_user_name())
            logError(msg)
            return '*ERROR* ' + msg

        if ':' in res_query:
            res_query = res_query.split(':')[0]

        user_roles = self.user_roles(props)
        user = user_roles.get('user')

        with self.acc_lock:
            _is_res_locked = self.is_resource_locked(res_query, root_id)
            if _is_res_locked and _is_res_locked != user:
                msg = 'User {}: Reserve resource: The resource is locked for'\
                      ' {} !'.format(self.get_user_name(), _is_res_locked)
                logError(msg)
                return '*ERROR* ' + msg

            _is_res_reserved = self.is_resource_reserved(res_query, root_id)
            if _is_res_reserved and _is_res_reserved != user:
                msg = 'User {}: Reserve resource: The resource is reserved '\
                     'for {} !'.format(self.get_user_name(), _is_res_reserved)
                logError(msg)
                return '*ERROR* ' + msg

            res_path = _get_res_path(resources, res_query)
            res_pointer = _get_res_pointer(resources, ''.join('/' + res_path[0]))

            if not res_pointer:
                msg = 'User {}: Reserve Resource: Cannot find resource path '\
                      'or ID `{}` !'.format(self.get_user_name(), res_query)
                logError(msg)
                return '*ERROR* ' + msg

            res_pointer.update([('path', [res_path[0]]), ])

            if user in self.reserved_res:
                self.reserved_res[user].update([(res_pointer['id'], copy.deepcopy(res_pointer)), ])
            else:
                self.reserved_res.update([(user, {res_pointer['id']: copy.deepcopy(res_pointer)}), ])

        return True #RESOURCE_RESERVED


    @cherrypy.expose
    def save_release_reserved_resource(self, res_query, props={}, root_id=ROOT_DEVICE, username=None):
        """ Save the resource and release it """
        logDebug('CeResources:save_release_reserved_resource {} {} {} {}'.format(res_query, props, root_id, username))
        self._load(False, props=props)

        if root_id == ROOT_DEVICE:
            resources = self.resources
        else:
            resources = self.systems

        # If no resources...
        if not resources.get('children'):
            msg = 'User {}: Save and release reserved resource: There are no '\
                  ' resources defined !'.format(self.get_user_name())
            logError(msg)
            return '*ERROR* ' + msg

        if ':' in res_query:
            res_query = res_query.split(':')[0]

        res_path = _get_res_path(resources, res_query)
        res_pointer = _get_res_pointer(resources, ''.join('/' + res_path[0]))
        # the res_pointer not found; this might happen if the
        # resource was renamed; if so, the new name should be in
        # reserved_res; get the ID from there and search again
        if not res_pointer:
            res_path, res_pointer = self._get_reserved_res_pointer(res_query)

        if '/' in res_query:
            res_query = res_query.split('/')[-1]

        if not res_pointer:
            msg = 'User {}: Save and release resource: Cannot find resource '\
                  'path or ID `{}` !'.format(self.get_user_name(), res_query)
            logError(msg)
            return '*ERROR* ' + msg

        res_pointer.update([('path', [res_path[0]]), ])

        user_roles = self.user_roles(props)
        user = user_roles.get('user')

        #if not the same user, we have an error
        if username and user != username:
            msg = 'User {}: Save reserved resource: Cannot find resource path or ID `{}`!'.format(user, res_query)
            logError(msg)
            return '*ERROR* ' + msg

        save_result = None
        try:
            _res_pointer = self.reserved_res[user].pop(res_pointer['id'])
            if not isinstance(_res_pointer['path'], list):
                _res_pointer['path'] = _res_pointer['path'].split('/')

            # Check for modifications
            if res_pointer != _res_pointer:
                child = None
                for c_res in resources.get('children'):
                    if resources['children'][c_res]['id'] == _res_pointer['id']:
                        child = c_res
                if not child == _res_pointer['path'][0]:
                    resources['children'].pop(child)

                    # Delete file
                    if child.split('.')[-1] == 'system':
                        suts_path = self.project.get_user_info(user, 'sys_sut_path')
                        if not suts_path:
                            suts_path = '{}/config/sut/'.format(TWISTER_PATH)
                        os.remove(os.path.join(suts_path, '.'.join(child.split('.')[:-1] + ['json'])))
                    else:
                        # Get the user rpyc connection connection
                        try:
                            usr_conn = self.project._find_local_client(user)
                            usr_conn.root.delete_sut('.'.join(child.split('.')[:-1]))
                        except Exception as exp_err:
                            logError('User {}: Save and release resource \
                            ERROR:: `{}`.'.\
                            format(self.get_user_name(), exp_err))

            resources['children'].update([(_res_pointer['path'][0], _res_pointer), ])
            #resources['children'].update([(res_path[0], _res_pointer), ])

            # Check for modifications
            if res_pointer != _res_pointer:
                # Write changes.
                save_result = self._save(root_id, props, res_query, username)

            if not self.reserved_res[user]:
                self.reserved_res.pop(user)
        except Exception as exp_err:
            msg = 'User {}: Save and release resource: `{}` !'.format(self.get_user_name(), exp_err)
            logError(msg)
            return '*ERROR* ' + msg

        if not save_result == True and not save_result == None:
            return save_result

        return True #RESOURCE_FREE


    @cherrypy.expose
    def save_reserved_resource(self, res_query, props={}, root_id=ROOT_DEVICE, username=None):
        """ Save the reserved resource """
        logFull('CeResources:save_reserved_resource {}'.format(res_query))
        self._load(False, props=props)

        if root_id == ROOT_DEVICE:
            resources = self.resources
        else:
            resources = self.systems

        # If no resources...
        if not resources.get('children'):
            msg = 'User {}: Save reserved resource: There are no resources defined !'.format(self.get_user_name())
            logError(msg)
            return '*ERROR* ' + msg

        if ':' in res_query:
            res_query = res_query.split(':')[0]

        res_path = _get_res_path(resources, res_query)
        res_pointer = _get_res_pointer(resources, ''.join('/' + res_path[0]))
        # the res_pointer not found; this might happen if the
        # resource was renamed; if so, the new name should be in
        # reserved_res; get the ID from there and search again
        if not res_pointer:
            res_path, res_pointer = self._get_reserved_res_pointer(res_query)

        if not res_pointer:
            msg = 'User {}: Save reserved resource: Cannot find resource path'\
                  ' or ID `{}` !'.format(self.get_user_name(), res_query)
            logError(msg)
            return '*ERROR* ' + msg

        res_pointer.update([('path', [res_path[0]]), ])

        user_roles = self.user_roles(props)
        user = user_roles.get('user')
        res = None
        try:
            _res_pointer = copy.deepcopy(self.reserved_res[user][res_pointer['id']])
            if not isinstance(_res_pointer['path'], list):
                _res_pointer['path'] = _res_pointer['path'].split('/')

            # Check for modifications
            if res_pointer != _res_pointer:
                child = None
                # Search in all esources for this SUT
                for r_child in resources.get('children'):
                    if resources['children'][r_child]['id'] == _res_pointer['id']:
                        child = r_child
                # SUT not found in resources; new one or strange scenario; we
                # have to delete existing file to make everything is clean
                if not child == _res_pointer['path'][0]:
                    resources['children'].pop(child)

                    # Delete file
                    if child.split('.')[-1] == 'system':
                        suts_path = self.project.get_user_info(user, 'sys_sut_path')
                        if not suts_path:
                            suts_path = '{}/config/sut/'.format(TWISTER_PATH)
                        os.remove(os.path.join(suts_path, '.'.join(child.split('.')[:-1] + ['json'])))
                    else:
                        # Get the user rpyc connection connection
                        try:
                            usr_conn = self.project._find_local_client(user)
                            usr_conn.root.delete_sut('.'.join(child.split('.')[:-1]))
                        except Exception as exp_err:
                            logError('User {}: Save resource ERROR:: `{}`.'.format(self.get_user_name(), exp_err))

            resources['children'].update([(_res_pointer['path'][0], _res_pointer), ])

            # Check for modifications
            if res_pointer != _res_pointer:
                # Write changes.
                self._save(root_id, props, res_query, username)
        except Exception as exp_err:
            msg = 'User {}: Save reserved resource: `{}` !'.format(self.get_user_name(), exp_err)
            logError(msg)
            return '*ERROR* ' + msg

        if not res == True and not res == None:
            return res

        return True #RESOURCE_RESERVED


    @cherrypy.expose
    def save_reserved_resource_as(self, name, res_query, props={}, root_id=ROOT_DEVICE, username=None):
        """ Save a reserved resource with a different name"""
        logFull('CeResources:save_reserved_resource_as {} {}'.format(name, res_query))
        self._load(False, props=props)

        if root_id == ROOT_DEVICE:
            resources = self.resources
        else:
            resources = self.systems

        # If no resources...
        if not resources.get('children'):
            msg = 'User {}: Save reserved resource as: There are no resources defined !'.format(self.get_user_name())
            logError(msg)
            return '*ERROR* ' + msg

        if ':' in res_query:
            res_query = res_query.split(':')[0]

        res_path = _get_res_path(resources, res_query)
        res_pointer = _get_res_pointer(resources, ''.join('/' + res_path[0]))

        if '/' in res_query:
            res_query = res_query.split('/')[-1]

        if not res_pointer:
            msg = 'User {}: Save reserved resource as: Cannot find resource '\
                  'path or ID `{}` !'.format(self.get_user_name(), res_query)
            logError(msg)
            return '*ERROR* ' + msg

        res_pointer.update([('path', [res_path[0]]), ])

        user_roles = self.user_roles(props)
        user = user_roles.get('user')

        #if not the same user, we have an error
        if username and user != username:
            msg = 'User {}: Save reserved resource as: Cannot find resource path or ID `{}`!'.format(user, res_query)
            logError(msg)
            return '*ERROR* ' + msg

        try:
            name = '.'.join([name, 'user'])

            _res_pointer = copy.deepcopy(self.reserved_res[user][res_pointer['id']])
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
            res = self._save(root_id, props, res_query, username)
            if not res == True:
                return res
            return res_id
        except Exception as exp_err:
            msg = 'User {}: Save reserved resource as: `{}` !'.format(self.get_user_name(), exp_err)
            logError(msg)
            return '*ERROR* ' + msg

        #return True


    @cherrypy.expose
    def discard_release_reserved_res(self, res_query, props={}, root_id=ROOT_DEVICE, username=None):
        """  Discard changes and save the resource """
        logDebug('User {}: CeResources:discard_release_reserved_res'.format(self.get_user_name()))
        self._load(False, props=props)

        if root_id == ROOT_DEVICE:
            resources = self.resources
        else:
            resources = self.systems

        # If no resources...
        if not resources.get('children'):
            msg = 'User {}: Discard reserved resource: There are no resources defined !'.format(self.get_user_name())
            logError(msg)
            return '*ERROR* ' + msg

        if ':' in res_query:
            res_query = res_query.split(':')[0]

        res_path = _get_res_path(resources, res_query)
        res_pointer = _get_res_pointer(resources, ''.join('/' + res_path[0]))

        # the res_pointer not found; this might happen if the
        # resource was renamed; if so, the new name should be in
        # reserved_res; get the ID from there and search again
        if not res_pointer:
            res_path, res_pointer = self._get_reserved_res_pointer(res_query)

        if not res_pointer:
            msg = 'User {}: Discard reserved resource: Cannot find resource '\
                  'path or ID `{}` !'.format(self.get_user_name(), res_query)
            logError(msg)
            return '*ERROR* ' + msg

        res_pointer.update([('path', [res_path[0]]), ])

        user_roles = self.user_roles(props)
        user = user_roles.get('user')

        if username and user != username:
            #Different user; return
            return

        try:
            self.reserved_res[user].pop(res_pointer['id'])
            if not self.reserved_res[user]:
                self.reserved_res.pop(user)
        except Exception as exp_err:
            msg = 'Discard reserved resource: `{}` for user !'.format(exp_err, user)
            logError(msg)
            return '*ERROR* ' + msg

        return True #RESOURCE_FREE


    @cherrypy.expose
    def is_resource_locked(self, res_query, root_id=ROOT_DEVICE):
        """ returns the user or false """
        logFull('CeResources:is_resource_locked')
        if root_id == ROOT_DEVICE:
            resources = self.resources
        else:
            resources = self.systems

        # If no resources...
        if not resources.get('children'):
            return False

        if ':' in res_query:
            res_query = res_query.split(':')[0]

        res_path = _get_res_path(resources, res_query)
        if not res_path:
            # return '*ERROR* not found'
            return False
        res_pointer = _get_res_pointer(resources, ''.join('/' + res_path[0]))

        # the res_pointer not found; this might happen if the
        # resource was renamed; if so, the new name should be in
        # reserved_res; get the ID from there and search again
        if not res_pointer:
            res_path, res_pointer = self._get_reserved_res_pointer(res_query)

        if not res_pointer:
            msg = 'User {}: Is resource locked: Cannot find resource path or '\
                  'ID `{}` !'.format(self.get_user_name(), res_query)
            logError(msg)
            return '*ERROR* ' + msg

        res_pointer.update([('path', [res_path[0]]), ])

        lock_for_user = [u for u in self.locked_res if res_pointer['id'] in self.locked_res[u]]

        if not lock_for_user:
            return False

        if len(lock_for_user) == 1:
            lock_for_user = lock_for_user[0]
        else:
            logDebug('Wrong length for lockedForUser: {}'.format(len(lock_for_user)))
            return False

        return lock_for_user


    @cherrypy.expose
    def lock_resource(self, res_query, props={}, root_id=ROOT_DEVICE, username=None):
        """ Lock a resource """
        logDebug('CeResources:lock_resource {} {} {} {}'.format(res_query, props, root_id, username))
        self._load(False, props=props)

        if root_id == ROOT_DEVICE:
            resources = self.resources
        else:
            resources = self.systems

        # If no resources...
        if not resources.get('children'):
            msg = 'User {}: Lock resource: There are no resources defined !'.format(self.get_user_name())
            logError(msg)
            return '*ERROR* ' + msg

        if ':' in res_query:
            res_query = res_query.split(':')[0]

        user_roles = self.user_roles(props)
        user = user_roles.get('user')

        with self.acc_lock:
            _is_res_reserved = self.is_resource_reserved(res_query, root_id)
            if _is_res_reserved and _is_res_reserved != user:
                msg = 'User {}: Lock resource: The resource is reserved for '\
                      '{} !'.format(self.get_user_name(), _is_res_reserved)
                logError(msg)
                return '*ERROR* ' + msg

            _is_res_locked = self.is_resource_locked(res_query, root_id)
            if _is_res_locked and _is_res_locked != user:
                msg = 'User {}: Lock resource: The resource is locked for '\
                      '{} !'.format(self.get_user_name(), _is_res_locked)
                logError(msg)
                return '*ERROR* ' + msg

            res_path = _get_res_path(resources, res_query)
            res_pointer = _get_res_pointer(resources, ''.join('/' + res_path[0]))

            if not res_pointer:
                msg = 'User {}: Lock Resource: Cannot find resource path or '\
                      'ID `{}` !'.format(self.get_user_name(), res_query)
                logError(msg)
                return '*ERROR* ' + msg

            res_pointer.update([('path', [res_path[0]]), ])

            # if it's not the same user, don't lock the resource, just return
            if username and user != username:
                logDebug('CeResources:lock_resource different user {} {}'.format(user, username))
                return False

            user_res = self.locked_res.get(user, {})
            user_res.update({res_pointer['id']: copy.deepcopy(res_pointer)})
            self.locked_res[user] = user_res

        return True #RESOURCE_BUSY


    @cherrypy.expose
    def unlock_resource(self, res_query, props={}, root_id=ROOT_DEVICE, username=None):
        """ Unlock a resource """
        logDebug('CeResources:unlock_resource {} {} {} {}'.format(res_query, props, root_id, username))
        self._load(False, props=props)

        if root_id == ROOT_DEVICE:
            resources = self.resources
        else:
            resources = self.systems

        # If no resources...
        if not resources.get('children'):
            msg = 'User {}: Unlock resource: There are no resources defined !'.format(self.get_user_name())
            logError(msg)
            return '*ERROR* ' + msg

        if ':' in res_query:
            res_query = res_query.split(':')[0]

        res_path = _get_res_path(resources, res_query)
        res_pointer = _get_res_pointer(resources, ''.join('/' + res_path[0]))

        if not res_pointer:
            msg = 'User {}: Unlock resource: Cannot find resource path or '\
                  'ID `{}` !'.format(self.get_user_name(), res_query)
            logError(msg)
            return '*ERROR* ' + msg

        res_pointer.update([('path', [res_path[0]]), ])

        with self.acc_lock:
            user_roles = self.user_roles(props)
            user = user_roles.get('user')
            try:
                self.locked_res[user].pop(res_pointer['id'])
                if not self.locked_res[user]:
                    self.locked_res.pop(user)
            except Exception as exp_err:
                msg = 'User {}: Unlock resource: `{}` !'.format(self.get_user_name(), exp_err)
                logError(msg)
                return '*ERROR* ' + msg

        return True #RESOURCE_FREE


    @cherrypy.expose
    def list_reserved_resources(self):
        """ Return list if reserved resources """
        return self.reserved_res


    @cherrypy.expose
    def list_locked_resources(self):
        """ Return list if locked resources """
        return self.locked_res


    @cherrypy.expose
    def list_all_resources(self):
        """
        Fast list testbeds.
        """
        res = []
        for k_var, v_var in self.resources.get('children').iteritems():
            path = v_var.get('path') or _get_res_path(self.resources, v_var['id']) or []
            res.append(['/'.join(path), v_var['id']])
        result = []

        def quick_find_path(directory, spath):
            """ function to find the path """
            for usr, locks in directory.iteritems():
                for el_id, data in locks.iteritems():
                    path = data.get('path', [''])
                    if isinstance(path, str) or isinstance(path, unicode):
                        path = [path]
                    if path == [spath]:
                        return usr
            return None

        for tb_name, tb_id in sorted(res):
            ruser = quick_find_path(self.reserved_res, tb_name)
            luser = quick_find_path(self.locked_res, tb_name)

            if (not ruser) and (not luser):
                result.append({'id': tb_id, 'name': tb_name, 'status': 'free'})
            elif ruser:
                result.append({'id': tb_id, 'name': tb_name, 'status': 'reserved', 'user': ruser})
            elif luser:
                result.append({'id': tb_id, 'name': tb_name, 'status': 'locked', 'user': luser})
            # Both reserved and locked ?
            else:
                result.append({'id': tb_id, 'name': tb_name, 'status': 'reserved', 'user': ruser})

        logDebug('User {}: Fast listing Resources... Found {}.'.format(self.get_user_name(), res))

        return result


    @cherrypy.expose
    def list_all_suts(self, user):
        """
        Fast list suts.
        """
        suts = []
        result = []
        usr_home = userHome(user)

        # System SUT path
        sys_sut_path = self.project.get_user_info(user, 'sys_sut_path')
        if not sys_sut_path:
            sys_sut_path = '{}/config/sut/'.format(TWISTER_PATH)

        # User SUT path
        usr_sut_path = self.project.get_user_info(user, 'sut_path')
        if not usr_sut_path:
            usr_sut_path = '{}/twister/config/sut/'.format(usr_home)

        # first, get all system SUT files
        if os.path.isdir(sys_sut_path):
            s_sut = ['{}.system'.format(os.path.splitext(d)[0])\
                for d in os.listdir(sys_sut_path)\
                if os.path.splitext(d)[1] == '.json']
            suts.extend(s_sut)

        # get user SUT file; we have to check if the cleacase plugin
        # is activated; if so, use it to read the SUT files from view;
        # else use the UserService to read it
        cc_cfg = self.project.get_clearcase_config(user, 'sut_path')
        if cc_cfg:
            view = cc_cfg['view']
            actv = cc_cfg['actv']
            path = cc_cfg['path']
            user_view_actv = '{}:{}:{}'.format(user, view, actv)
            resp = self.project.clearFs.list_user_files(user_view_actv, path, False, False)
            if isinstance(resp, str):
                logWarning(resp)
            for file_p in resp['children']:
                file_name, file_ext = os.path.splitext(file_p['path'])
                if file_ext and file_ext == '.json':
                    suts.append(file_name + '.user')
        else:
            if os.path.isdir(usr_sut_path):
                resp = self.project.localFs.list_user_files(user, usr_sut_path, False, False)
                if isinstance(resp, str):
                    logWarning(resp)
                for file_p in resp['children']:
                    file_name, file_ext = os.path.splitext(file_p['path'])
                    if file_ext and file_ext == '.json':
                        suts.append(file_name + '.user')

        def quick_find_path(directory, spath):
            """ function to find path """
            for usr, locks in directory.iteritems():
                for el_id, data in locks.iteritems():
                    path = data.get('path', [''])
                    if isinstance(path, str) or isinstance(path, unicode):
                        path = [path]
                    if path == [spath]:
                        return usr
            return None

        for s_sut in sorted(suts):
            ruser = quick_find_path(self.reserved_res, s_sut)
            luser = quick_find_path(self.locked_res, s_sut)

            if (not ruser) and (not luser):
                result.append({'name': s_sut, 'status': 'free'})
            elif ruser:
                result.append({'name': s_sut, 'status': 'reserved', 'user': ruser})
            elif luser:
                result.append({'name': s_sut, 'status': 'locked', 'user': luser})
            # Both reserved and locked ?
            else:
                result.append({'name': s_sut, 'status': 'reserved', 'user': ruser})

        logDebug('User {}: Fast listing SUTs... Found {}.'.format(self.get_user_name(), suts))

        return result


    @cherrypy.expose
    def copy_sut_file(self, old_sut, new_sut, user, delete_old=True):
        """
        Copy a SUT file in a new one
        """
        logDebug('CeResources:copy_sut_file {} {} {} {}'.format(old_sut, new_sut, user, delete_old))

        # check if old_sut exists
        found_old_sut = False
        user_sut_list = self.list_all_suts(user)
        if user_sut_list:
            for list_elem in user_sut_list:
                if list_elem['name'] == old_sut:
                    found_old_sut = True
                    continue

        if not found_old_sut:
            msg = 'User {}: SUT file {} doesn\'t exit !'.format(self.get_user_name(), old_sut)
            logError(msg)
            return '*ERROR* ' + msg

        # check that the new_sut name doesn't exists
        if user_sut_list:
            for list_elem in user_sut_list:
                if list_elem['name'] == new_sut:
                    msg = 'User {}: New SUT file {} already exits !'.format(self.get_user_name(), new_sut)
                    logError(msg)
                    return '*ERROR* ' + msg

        # make sure the SUT file names start with /
        if new_sut[0] != '/':
            new_sut = '/' + new_sut
        if old_sut[0] != '/':
            old_sut = '/' + old_sut

        # create a new SUT file and reserve it
        new_sut_id = self.set_resource(new_sut, '/', '{}', ROOT_SUT, user)
        if isinstance(new_sut_id, str):
            if '*ERROR*' in new_sut_id:
                msg = 'User {}: New SUT file {} cannot be created!'.format(self.get_user_name(), new_sut)
                logError(msg)
                return '*ERROR* ' + msg

        reserve_res = self.reserve_resource(new_sut, '{}', ROOT_SUT, user)
        if  isinstance(reserve_res, str):
            if '*ERROR*' in reserve_res:
                msg = 'User {}: New SUT file {} cannot be reserved!'.format(self.get_user_name(), new_sut)
                logError(msg)
                return '*ERROR* ' + msg

        def clean_new_sut(new_sut, user):
            """ method to clean the new SUT if needed """
            self.reserved_res[user].pop(new_sut)
            if not self.reserved_res[user]:
                self.reserved_res.pop(user)
            self.delete_resource(new_sut, '{}', ROOT_SUT, user)

        # reserve the old SUT file and copy the content into the new SUT file
        # Check if resource is locked; if so, it cannot be copied
        _is_res_locked = self.is_resource_locked(old_sut, ROOT_SUT)
        if _is_res_locked and _is_res_locked != user:
            msg = 'User {}: Reserve resource: The resource is locked for {} !'\
                  .format(self.get_user_name(), _is_res_locked)
            logError(msg)
            clean_new_sut(new_sut_id, user)
            return '*ERROR* ' + msg

        # Check if resource is reserved; if so, it cannot be copied
        _is_res_locked = self.is_resource_reserved(old_sut, ROOT_SUT)
        if _is_res_locked and _is_res_locked != user:
            msg = 'User {}: Cannot delete: The resource is reserved for {} !'\
                  .format(self.get_user_name(), _is_res_locked)
            logError(msg)
            clean_new_sut(new_sut_id, user)
            return '*ERROR* ' + msg

        # Try to reserve source SUT file; if error, clean up the new SUT
        reserve_res = self.reserve_resource(old_sut, '{}', ROOT_SUT, user)
        if  isinstance(reserve_res, str):
            if '*ERROR*' in reserve_res:
                msg = 'User {}: Source SUT file {} cannot be reserved!'.format(self.get_user_name(), old_sut)
                logError(msg)
                clean_new_sut(new_sut_id, user)
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
        if isinstance(save_result, str):
            if '*ERROR*' in save_result:
                msg = 'User {}: Save SUT file {} ERROR !'.format(self.get_user_name(), new_sut)
                logError(msg)
                clean_new_sut(new_sut_id, user)
                return '*ERROR* ' + msg

        # release the new SUT
        self.reserved_res[user].pop(new_sut_id)
        if not self.reserved_res[user]:
            self.reserved_res.pop(user)

        # release the old sut; and delete if needed
        self.reserved_res[user].pop(old_res_pointer['id'])
        if not self.reserved_res[user]:
            self.reserved_res.pop(user)
        if delete_old is True:
            self.delete_resource(old_sut, '{}', ROOT_SUT, user)

        return True


    @cherrypy.expose
    def get_reserved_resource(self, query):
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
        user_roles = self.user_roles()
        user = user_roles['user']

        user_resources = False
        for child in self.reserved_res:
            if child == user:
                user_resources = self.reserved_res.get(user)

        if not user_resources:
            return False

        # Every resource id is a key in the user_resources dcitionary
        for id_key in user_resources:
            # get the resource path
            root_path = user_resources[id_key]['path']

            # set new_path where value for this key starts
            new_path = user_resources[id_key]

            # recursevly build a dictionary with all subcomponents of the new_path
            rec_list = []
            ret_dict = {}
            ret_dict['path'] = root_path[0]
            ret_dict['meta'] = new_path['meta']
            ret_dict['id'] = new_path['id']
            ret_dict['children'] = _recursive_build_comp(new_path.get('children'), ret_dict['path'], rec_list)

            # search the query if the created dictionary
            if _recursive_search_string(ret_dict, query):
                return True

        return False
#

# Eof()
