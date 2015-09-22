
# File: CeSuts.py ; This file is part of Twister.

# version: 3.013

# Copyright (C) 2012-2014, Luxoft

# Authors:
#    Andreea Proca <aproca@luxoft.com>
#    Andrei Costachi <acostachi@luxoft.com>
#    Cristi Constantin <crconstantin@luxoft.com>

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
Module to manage SUT operations
'''

import os
import sys
import copy
import thread
from binascii import hexlify
import cherrypy
from cherrypy import _cptools
from lxml import etree

try:
    import simplejson as json
except Exception:
    import json

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print 'TWISTER_PATH environment variable is not set! Exiting!'
    exit(1)
if TWISTER_PATH not in sys.path:
    sys.path.append(TWISTER_PATH)

from common.tsclogging import logFull, logDebug, logInfo, logWarning, logError
from common.helpers import userHome
from server.CeCommonAllocator import CommonAllocator

CONSTANT_DICTIONARY = {'version': 0, 'name': '/', 'meta': {}, 'children': {}}


def xml_to_res(xml, gparams):
    """
    Import xml file to SUT.
    """

    def recursive_xml_to_res(xml, res_dict):
        """
        Recursive method - read the xml and generate a dictionary.
        """
        c_nd = {}

        for folder in xml.findall('folder'):
            tb_path = folder.find('path')
            if tb_path is not None:
                c_nd = {'path':[], 'meta': {}, 'id': '', 'children': {}}
                tb_path_text = tb_path.text
                tb_path_list = [q for q in tb_path_text.split('/') if q]
                c_nd['path'].extend(tb_path_list)
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

    # we have to get the information at root level(path, meta, id, version) first
    # version is added only if it exists in xml; the SUT exported files do not
    # have the version tag
    root_dict = {'path':[], 'meta':{}, 'id':'', 'children':{}}
    tb_path_text = xml.find('path').text
    tb_path = [q for q in tb_path_text.split('/') if q]
    if tb_path:
        root_dict['path'].extend(tb_path)
    else:
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
    gparams = root_dict

    # rest of the xml file can be read recursively
    recursive_xml_to_res(xml, gparams['children'])

    return gparams


def res_to_xml(parent_node, xml, skip_header=False):
    """
    Export TB to xml.
    """

    # The node is valid ?
    if not parent_node:
        return False

    # if we are at root level, we need to get path, meta, id and version fields
    if not skip_header:
        # path is a list with 0 or 1 elements
        path = etree.SubElement(xml, 'path')
        if parent_node.get('path') is not None and len(parent_node.get('path')) == 1:
            path.text = '/'.join(parent_node.get('path'))
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
            etree.SubElement(tag, 'desc')

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
        etree.SubElement(folder, 'fdesc')

        # get the path if exists
        if c_nd.get('path'):
            path = etree.SubElement(folder, 'path')
            path.text = '/'.join(c_nd.get('path'))

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
            etree.SubElement(tag, 'desc')

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


class Suts(_cptools.XMLRPCController, CommonAllocator):
    """
    Basic operations for SUTs.
    """

    def __init__(self, project):

        self.project = project
        self.type = 'sut'
        self.resources = CONSTANT_DICTIONARY
        self.reservedResources = {}
        self.lockedResources = {}
        self.id_list = {}
        self.acc_lock = thread.allocate_lock() # Task change lock
        self.ren_lock = thread.allocate_lock() # Rename lock
        self.imp_lock = thread.allocate_lock() # Import lock
        self.save_lock = thread.allocate_lock() # Save lock
        self.load_lock = thread.allocate_lock() # Save lock


    def save_sut(self, props={}, resource_name=None):
        """
        Function used to write the changes on HDD.
        The save is separate for Devices and SUTs, so the version is not incremented
        for both, before saving.
        """
        user = self.user_info(props)[0]
        logDebug('CeSuts:_save {} {} {} '.format(props, resource_name, user))
        log = []

        # Write changes, using the Access Lock.
        with self.save_lock:
            if resource_name[0] == '/':
                resource_name = resource_name[1:]

            if resource_name.split('.')[-1] == 'user':
                suts_gb_path = self.project.get_user_info(user, 'sut_path')
            else:
                suts_gb_path = self.project.get_user_info(user, 'sys_sut_path')

            if not suts_gb_path:
                suts_gb_path = '{}/config/sut/'.format(TWISTER_PATH)

            filename = os.path.join(suts_gb_path, '.'.join(resource_name.split('.')[:-1] + ['json']))

            if resource_name.split('.')[-1] == 'system':
                try:
                    resp = self.project.localFs.write_system_file(filename, \
                        json.dumps(self.resources['children'][resource_name], indent=4), 'w')
                except Exception as exp_err:
                    log.append(exp_err)
                    logError('User {}: Saving ERROR system:: `{}`.'.format(user, exp_err))

            if resource_name.split('.')[-1] == 'user':
                # user SUT file; we have to check if the cleacase plugin
                # is activated; if so, use it to write the SUT file; else
                # use the UserService to read it
                cc_cfg = self.project.get_clearcase_config(user, 'sut_path')
                if cc_cfg:
                    view = cc_cfg['view']
                    actv = cc_cfg['actv']
                    path = cc_cfg['path']
                    user_view_actv = '{}:{}:{}'.format(user, view, actv)
                    f_name = ''.join(resource_name.split('.')[:-1])
                    resp = self.project.clearFs.write_user_file(user_view_actv, path +'/'+ f_name + '.json', \
                        json.dumps(self.resources['children'][resource_name], indent=4))
                else:
                    # Get the user connection
                    resp = self.project.localFs.write_user_file(user, filename, \
                        json.dumps(self.resources['children'][resource_name], indent=4), 'w')
                if resp is not True:
                    log.append(resp)
                    logError('User {}: Saving ERROR user:: `{}`.'.format(user, resp))

                # targeted resource is saved now; do not continue with
                # the rest of resources
        if log:
            return '*ERROR* ' + str(log)

        # update id_list
        self.parse_sut(self.resources['children'][resource_name], resource_name)

        return True


    @cherrypy.expose
    def save_sut_as(self, sut_name, path):
        """
        Function used to write the sut on the user specified path on the disk.
        sut_name: is the new name of the sut to be saved
        path: is the path where the sut is saved. It doesn't contain the sut name at the end.
        """
        user = self.user_info({})[0]
        logFull('CeSuts:_save_as {} {} {} '.format(sut_name, path, user))
        log = []

        # Write changes, using the Access Lock.
        with self.save_lock:
            if sut_name[0] == '/':
                sut_name = sut_name[1:]
            if not os.path.exists(path):
                msg = 'Path does not exist: {}'.format(path)
                logError(msg)
                return '*ERROR* '+msg
            # remove the '_' added when the sut was created
            real_name = sut_name[1:]
            filename = os.path.join(path, '.'.join(real_name.split('.')[:-1] + ['json']))
            try:
                self.project.localFs.write_user_file(user, filename, \
                json.dumps(self.resources['children'][sut_name], indent=4), 'w')
            except Exception as exp_err:
                log.append(exp_err)
                logError('User {}: Saving ERROR system:: `{}`.'.format(user, exp_err))
                # targeted resource is saved now; do not continue with
                # the rest of resources
        if log:
            return '*ERROR* ' + str(log)

        # remove the new sut from resources
        self.resources['children'].pop(sut_name)
        logDebug('Sut resource: `{}` removed from the resources'.format(sut_name))
        return True


    def format_content(self, content, kids_list):
        """
        Find all the ids from a sut.
        Helps creating id_list.
        """
        if not content:
            return kids_list

        if not content.get('children'):
            kids_list.add(content['id'])
            return kids_list

        for node in content['children']:
            kids_list.add(content['children'][node]['id'])
            self.format_content(content['children'][node], kids_list)


    def parse_sut(self, sut_content=None, sut_name=None):
        """
        Adds elements to id_list.
        """
        kids_list = set()
        kids_list.add(sut_content['id'])

        self.format_content(sut_content, kids_list)

        kids_list = list(kids_list)
        self.id_list[sut_name] = kids_list

        return True


    def find_sut_id(self, sut_id):
        """
        Search for an ID in id_list.
        """
        for key, value in self.id_list.items():
            if sut_id in value:
                return key
        return False


    def _format_dict_sut(self, result, query):
        """
        Helper function.
        """
        try:
            result = self.format_resource(result, query)
        except Exception:
            logFull('The sut `{}` is already formated !'.format(query))

        if isinstance(result['path'], list):
            result['path'] = '/'.join(result['path'])
        return result


    @cherrypy.expose
    def index_suts(self, props={}):
        """
        Open all SUT files and creats dict having
        entries like: {sut_name : [ids]}
        """
        user_info = self.user_info(props)
        user = user_info[0]
        usr_home = userHome(user)

        sut_content = False

        try:
            # System SUT path
            suts_gb_path = self.project.get_user_info(user, 'sys_sut_path')
            if not suts_gb_path:
                suts_gb_path = '{}/config/sut/'.format(TWISTER_PATH)

            sut_all_pats = [p for p in os.listdir(suts_gb_path)\
                if os.path.isfile(os.path.join(suts_gb_path, p))\
                     and p.split('.')[-1] == 'json']
            for sut_path in sut_all_pats:
                sut_name = '.'.join(['.'.join(sut_path.split('.')[:-1]  + ['system'])])

                with open(os.path.join(suts_gb_path, sut_path), 'r') as f_p:
                    sut_content = json.load(f_p)
                    self.parse_sut(sut_content, sut_name)
        except Exception as exp_err:
            logError('_load ERROR:: {} for user {}'.format(exp_err, user))

        # User SUT path
        suts_gb_path = self.project.get_user_info(user, 'sut_path')
        if not suts_gb_path:
            suts_gb_path = '{}/twister/config/sut/'.format(usr_home)

        # user SUT file; we have to check if the cleacase plugin
        # is activated; if so, use it to read the SUT file; else
        # use the UserService to read it
        # open all the json files and parse them - need to index all the ids
        # that sut contains
        cc_cfg = self.project.get_clearcase_config(user, 'sut_path')
        if cc_cfg:
            view = cc_cfg['view']
            actv = cc_cfg['actv']
            path = cc_cfg['path']
            user_view_actv = '{}:{}:{}'.format(user, view, actv)

            sut_all_pats = [p for p in os.listdir(suts_gb_path)\
                if os.path.isfile(os.path.join(suts_gb_path, p))\
                     and p.split('.')[-1] == 'json']

            for sut_path in sut_all_pats:
                sut_name = '.'.join(['.'.join(sut_path.split('.')[:-1]  + ['user'])])
                resp = self.project.clearFs.read_user_file(user_view_actv, path +'/'+ sut_name)
                try:
                    sut_content = json.loads(resp)
                except Exception:
                    msg = "User {}: Cannot load ClearCase SUT `{}`!".format(user, sut_name)
                    logWarning(msg)
                    return '*ERROR* ' + msg
                self.parse_sut(sut_content, sut_name)

        else:
            sut_all_pats = [p for p in os.listdir(suts_gb_path)\
                if os.path.isfile(os.path.join(suts_gb_path, p))\
                     and p.split('.')[-1] == 'json']
            for sut_path in sut_all_pats:
                sut_name = '.'.join(['.'.join(sut_path.split('.')[:-1]  + ['user'])])

                if suts_gb_path[-1] != '/' and sut_path[-1] != '/':
                    complete_sut_path = suts_gb_path + '/' + sut_path
                else:
                    complete_sut_path = suts_gb_path + sut_path

                resp = self.project.localFs.read_user_file(user, complete_sut_path)
                try:
                    sut_content = json.loads(resp)
                except Exception:
                    msg = "User {}: Cannot load SUT `{}`!".format(user, sut_name)
                    logWarning(msg)
                    return '*ERROR* ' + msg
                self.parse_sut(sut_content, sut_name)

        return True


    @cherrypy.expose
    def get_sut(self, query, props={}):
        """
        Get the contant of one SUT file using it's name.
        Must provide a SUT name.<type> (type = user/system)

        If query is an id -> positive answer only if sut is in self.resources
        """
        user_info = self.user_info(props)
        username = user_info[0]
        follow_links = False

        # Follow links to TestBeds ?
        if 'follow_links' in props:
            follow_links = props['follow_links']
            del props['follow_links']

        logDebug('CeSuts: get_sut {} {} {}'.format(query, username, follow_links))
        usr_home = userHome(username)
        initial_query = None

        if not query:
            msg = "The name of the SUT is empty!"
            logDebug(msg)
            return False

        if ':' in query:
            meta = query.split(':')[1]
            query = query.split(':')[0]
        else:
            meta = ''

        sut_type = query.split('.')[-1]

        # This is an ID
        # Will return result only if the SUT is in self.resources
        if '/' not in query and sut_type == query:
            initial_query = query
            res_dict = self.get_resource(query)

            if isinstance(res_dict, dict):
                if len(res_dict['path']) > 1:
                    sut_content = self._format_dict_sut(res_dict, query)

                    # If this SUT / component is linked with a TB
                    if sut_content['meta'].get('_id') and follow_links:

                        # Ok, this might be a Device path, instead of SUT path!
                        tb_id = sut_content['meta']['_id']
                        self.project.testbeds.load_tb(verbose=False)
                        sut_content = self.project.testbeds.\
                        get_tb(tb_id, props)

                        # If the Device ID is invalid, bye bye!
                        if not isinstance(sut_content, dict):
                            return False

                    if meta:
                        return sut_content['meta'].get(meta, '')
                    else:
                        return sut_content

                query = res_dict['path'][0]
                sut_type = query.split('.')[-1]

            else:
                # Maybe this sut is already indexed
                result = self.find_sut_id(query)
                # If not index all suts and search
                if not result:
                    self.index_suts(props)
                    result = self.find_sut_id(query)
                    # Probably is a component not saved yet, get it from self.reservedResources
                    if not result:
                        if meta:
                            result = self.get_info_sut(query + ":" + meta, props)
                        else:
                            result = self.get_info_sut(query, props)

                        if isinstance(result, dict):
                            result = self._format_dict_sut(result, query)
                            return result
                        else:
                            msg = 'Invalid SUT ID `{}`, for user `{}`!'.format(query, username)
                            logWarning(msg)
                            return msg

                query = result
                sut_type = query.split('.')[-1]

        # if the query is for a component return the entire SUT
        if query[1:].count('/') >= 1:
            initial_query = query
            parts = [q for q in query.split('/') if q]
            query = parts[0]

        try:
            index = sut_type.index('/')
            sut_type = sut_type[:index]
        except Exception:
            logFull('SutType does not contain any /')

        if sut_type == 'system':
            # System SUT path
            sut_path = self.project.get_user_info(username, 'sys_sut_path')
            if not sut_path:
                sut_path = '{}/config/sut/'.format(TWISTER_PATH)
        elif sut_type == 'user':
            # User SUT path
            sut_path = self.project.get_user_info(username, 'sut_path')
            if not sut_path:
                sut_path = '{}/twister/config/sut/'.format(usr_home)
        else:
            msg = 'Invalid SUT type `{}`, for user `{}`!'.format(sut_type, username)
            logWarning(msg)
            return msg

        # avoid having more than one "/" or not having at all
        if query[0] == '/' and sut_path[-1] == '/':
            query = query[1:]
        elif query[0] != '/' and sut_path[-1] != '/':
            query = '/' + query

        f_name = '.'.join(query.split('.')[:-1]) + '.json'
        sut_file = sut_path + f_name
        sut_content = False

        if not os.path.isdir(sut_path):
            # Cannot get read access to the SUT directory
            msg = '*ERROR* Cannot get access to SUT path `{}`, user `{}`!'.format(sut_path, username)
            logWarning(msg)
            return msg

        if sut_type == 'system':
            # System SUT file
            try:
                with open(sut_file, 'r') as f_p:
                    sut_content = json.load(f_p)
            except Exception as exp_err:
                return '*ERROR* User {}: Cannot read SUT file `{}`! Exception {}'.format(
                    username, sut_file, exp_err)

        else:
            # User SUT file, check if the ClearCase plugin is activated
            # If so, use it to read the SUT file; else use the UserService to read it
            cc_cfg = self.project.get_clearcase_config(username, 'sut_path')
            if cc_cfg:
                view = cc_cfg['view']
                actv = cc_cfg['actv']
                path = cc_cfg['path']
                user_view_actv = '{}:{}:{}'.format(username, view, actv)
                sut_path = (path +'/'+ f_name).replace('//', '/')
                resp = self.project.clearFs.read_user_file(user_view_actv, sut_path)
                # Invalid sut file?
                if resp.startswith('*ERROR*'):
                    logWarning(resp)
                    return resp
                try:
                    sut_content = json.loads(resp)
                except Exception:
                    logWarning('User {}: Cannot load ClearCase SUT `{}`!'.format(username, sut_path))
                    sut_content = False
            else:
                sut_path = (sut_path + '/' + f_name).replace('//', '/')
                resp = self.project.localFs.read_user_file(username, sut_path)
                # Invalid sut file?
                if resp.startswith('*ERROR*'):
                    logWarning(resp)
                    return resp
                try:
                    sut_content = json.loads(resp)
                except Exception:
                    logWarning('User {}: Cannot load SUT `{}`!'.format(username, sut_path))
                    sut_content = False

        if isinstance(sut_content, str) and sut_content.startswith('*ERROR*'):
            return sut_content

        if (sut_content is False) or (not isinstance(sut_content, dict)):
            msg = 'User {}: Invalid SUT `{}`!'.format(username, f_name)
            logWarning(msg)
            return '*ERROR* ' + msg

        # At this point, the SUT is a valid dictionary
        if query[0] == '/':
            query = query[1:]

        if sut_content.get('path'):
            sut_content['path'] = sut_content['path'][0]
        else:
            sut_content['path'] = query

        self.resources['children'][query] = copy.deepcopy(sut_content)
        # make older resources files that don't have 'path' compatible
        self.resources['children'][query]['path'] = [query]
        modified = self.fix_path(self.resources['children'][query], [query])

        if modified:
            # now we have to save the version with path
            issaved = self.save_sut(props, query)
            if isinstance(issaved, str):
                msg = 'Cannot save SUT `{}`, for user `{}`!'.format(query, username)
                logWarning(msg)
                return msg

        if initial_query:
            result = self.get_info_sut(initial_query, props)

            if isinstance(result, dict):
                sut_content = self._format_dict_sut(result, query)

            elif follow_links:
                parts = [p for p in initial_query.split('/') if p]

                if len(parts) == 1:
                    msg = '*ERROR* Internal server error!'
                    logWarning(msg)
                    return msg

                curr_parts = [parts.pop(0)]

                while 1:
                    try:
                        curr_parts.append(parts.pop(0))
                    except Exception:
                        break
                    curr_path = '/' + '/'.join(curr_parts)

                    result = self.get_resource(curr_path)

                    # SUT not loaded
                    if not isinstance(result, dict):
                        msg = '*ERROR* Invalid SUT path `{}`!'.format(curr_path)
                        logWarning(msg)
                        return False

                    if result['meta'].get('_id'):
                        # Ok, this might be a Device path, instead of SUT path!
                        tb_id = result['meta']['_id']
                        self.project.testbeds.load_tb(verbose=False)
                        result = self.project.testbeds.get_tb(tb_id, props)

                        # If the Device ID is invalid, bye bye!
                        if not isinstance(result, dict):
                            return False

                        tb_path = '/' + result['path'] + '/' + '/'.join(parts)
                        result = self.project.testbeds.get_tb(tb_path, props)

                        # If the Device ID is invalid, bye bye!
                        if not isinstance(result, dict):
                            return False

                        if meta:
                            return result['meta'].get(meta, '')
                        else:
                            return result

            # Internal error?
            else:
                msg = '*ERROR* Invalid SUT path `{}`!'.format(initial_query)
                logWarning(msg)
                return msg

        try:
            sut_content = self.format_resource(sut_content, query)
        except Exception:
            logFull('User {}: The sut is already formated {}.'.format(username, query))

        # If this SUT / component is linked with a TB
        if sut_content['meta'].get('_id'):

            # Ok, this might be a Device path, instead of SUT path!
            tb_id = sut_content['meta']['_id']
            self.project.testbeds.load_tb(verbose=False)
            sut_content = self.project.testbeds.get_tb(tb_id, props)

            # If the Device ID is invalid, bye bye!
            if not isinstance(sut_content, dict):
                msg = '*ERROR* Invalid TB link on SUT `{}`!'.format(initial_query)
                logWarning(msg)
                return msg

        if meta:
            return sut_content['meta'].get(meta, '')
        else:
            return sut_content


    @cherrypy.expose
    def get_info_sut(self, res_query, props={}):
        """
        Get the current version of the meta SUT modified and unsaved or
        the version from the disk.
        """
        user_info = self.user_info(props)
        logDebug('CeSuts:get_meta_sut {} {}'.format(res_query, props))

        if ':' in res_query:
            res_query, meta = res_query.split(':')
        else:
            meta = ''

        result = None

        # If the SUT is reserved, get the latest unsaved changes
        if user_info[0] in self.reservedResources:
            for i in range(len(self.reservedResources[user_info[0]].values())):
                current_res_reserved = CONSTANT_DICTIONARY
                current_path_root = self.reservedResources[user_info[0]].values()[i]['path'][0]
                current_res_reserved['children'][current_path_root] = self.reservedResources[user_info[0]].values()[i]

                result = self.get_resource(res_query, current_res_reserved)
                if isinstance(result, dict):
                    break

        if not isinstance(result, dict):
            result = self.get_resource(res_query)
            # SUT not loaded
            if not isinstance(result, dict):
                msg = 'Cannot find `{}`. Call `get_sut` for a SUT, component, or meta.'.format(res_query)
                logWarning(msg)
                return False

        if isinstance(result, dict):
            if meta:
                return result['meta'].get(meta, '')
            else:
                return result

        return False


    @cherrypy.expose
    def reserve_sut(self, res_query, props={}):
        """
        load the SUT wanted and then reserve it
        """
        self.get_sut(res_query, props)
        return self.reserve_resource(res_query, props)


    @cherrypy.expose
    def create_component_sut(self, name, parent=None, props={}):
        """
        Create new component for an existing SUT
        """
        logFull('CeSuts:create_component_sut: parent = {}  props = {}  name = {}'.format(parent, props, name))

        if parent == '/' or parent == '1':
            msg = "The parent value is not an existing SUT. Mayebe you want to add a new SUT. Parent: {}".format(parent)
            logError(msg)
            return '*ERROR* ' + msg

        user_info = self.user_info(props)

        _is_res_reserved = self.is_resource_reserved(parent, props)
        if _is_res_reserved and _is_res_reserved != user_info[0]:
            msg = 'User {}: Cannot create new component: The SUT is reserved for {} !'\
            .format(user_info[0], _is_res_reserved)
            logError(msg)
            return '*ERROR* ' + msg

        _is_res_locked = self.is_resource_locked(parent)
        if _is_res_locked and _is_res_locked != user_info[0]:
            msg = 'User {}: Reserve SUT: The SUT is locked for {} !'\
            .format(user_info[0], _is_res_locked)
            logError(msg)
            return '*ERROR* ' + msg

        props = self.valid_props(props)
        with self.acc_lock:
            #the resource should be reserved previously
            parent_p = self.get_reserved_resource(parent, props)

            if not parent_p:
                logError('Cannot access reserved SUT, path or ID `{}` !'.format(parent))
                return False

            if name in parent_p['children']:
                msg = "A component with this name '{}'' already exists for this Sut: '{}'".format(name, parent)
                logDebug(msg)
                return '*ERROR* ' + msg

            #the resources is deep in the tree, we have to get its direct parent
            if len(parent_p['path']) >= 2:
                full_path = parent_p['path']
                base_path = "/".join(parent_p['path'][1:])
                parent_p = self.get_path(base_path, parent_p)
                parent_p['path'] = full_path

            if '/' in name:
                logDebug('Stripping slash characters from `{}` `{}`...'.format(name, parent))
                name = name.replace('/', '')

            # the resource doesn't exist - create it
            res_id = self.generate_index()
            parent_p['children'][name] = {'id': res_id, 'meta': props, 'children': {}, 'path':parent_p['path'] + [name]}
            epnames_tag = '_epnames_{}'.format(user_info[0])

            # If the epnames tag exists in resources
            if epnames_tag in parent_p['children'][name]['meta']:
                # And the tag is empty
                if not parent_p['children'][name]['meta'][epnames_tag]:
                    logDebug('User {}: Deleting `{}` tag from new resource.'.format(user_info[0], epnames_tag))
                    del parent_p['children'][name]['meta'][epnames_tag]

        return res_id


    @cherrypy.expose
    def create_new_sut(self, name, parent=None, props={}, save=True):
        """
        Create a SUT.
        """
        user_info = self.user_info(props)
        logFull('CeSuts: create_new_sut: parent = {} -- props = {} -- name = {}'.format(parent, props, name))
        props = self.valid_props(props)

        if parent != '/' and parent != "1":
            msg = "User {}: The parent value is not root. Mayebe you want to add a component \
            to an existing SUT. Parent: {}".format(user_info, parent)
            logError(msg)
            return '*ERROR* ' + msg

        with self.acc_lock:
            #root can not be reserved so we just take it
            if name.split('.')[-1] != 'user' and \
            name.split('.')[-1] != 'system':
                name = '.'.join([name, 'user'])

            if '/' in name:
                logDebug('Stripping slash characters from `{}`...'.format(name))
                name = name.replace('/', '')

            if name in self.resources['children']:
                msg = "User {}: A SUT with this name '{}'' already exists'".format(user_info[0], name)
                logDebug(msg)
                return '*ERROR* ' + msg

            # the resource doesn't exist - create it
            res_id = self.generate_index()
            self.resources['children'][name] = {'id': res_id, 'meta': props, 'children': {}, 'path': [name]}

            #save this new SUT
            if save:
                issaved = self.save_sut(props, name)
                if  isinstance(issaved, str):
                    msg = "We could not save this SUT {}".format(name)
                    logDebug(msg)
                    return issaved

            return res_id


    @cherrypy.expose
    def update_meta_sut(self, name, parent=None, props={}):
        """
        Modify a SUT using a name, a parent Path or ID and some properties.
        This method changes meta for a certain SUT.
        """
        user_info = self.user_info(props)
        logDebug('CeSuts:update_meta_sut: parent = {} -- props = {} -- username = {} -- name = {}'\
            .format(parent, props, user_info[0], name))

        # if props does not have the correct format we stop this operation
        if not props or not self.valid_props(props):
            msg = "Wrong format for props = {}".format(props)
            logDebug(msg)
            return '*ERROR* ' + msg

        # can not verify if reserved '/' because I load only the sut that I need
        if parent == "/" or parent == "1":
            if name.split('.')[-1] != 'user' and \
            name.split('.')[-1] != 'system':
                name = '.'.join([name, 'user'])
            # we can not reserve the root so we just take the sut we need
            verify_reserved = name
        else:
            # take the sut that has the component we need
            verify_reserved = parent

        # what if this sut is already reserved by other user? We STOP
        _is_res_reserved = self.is_resource_reserved(verify_reserved, props)
        if _is_res_reserved and _is_res_reserved != user_info[0]:
            msg = 'User {}: Cannot update meta: The resource is reserved for {} !'\
            .format(user_info[0], _is_res_reserved)
            logError(msg)
            return '*ERROR* ' + msg

        # what if this sut is already locked by other user? We STOP
        _is_res_locked = self.is_resource_locked(verify_reserved)
        if _is_res_locked and _is_res_locked != user_info[0]:
            msg = 'User {}: Reserve resource: The resource is locked for {} !'\
            .format(user_info[0], _is_res_locked)
            logError(msg)
            return '*ERROR* ' + msg

        with self.acc_lock:

            parent_p = self.get_reserved_resource(verify_reserved, props)

            if not parent_p:
                logError('Cannot access reserved SUT, path or ID `{}` !'.format(verify_reserved))
                return False

            if '/' in name:
                logDebug('Stripping slash characters from `{}`...'.format(name))
                name = name.replace('/', '')

            # the resources is deep in the tree, we have to get its direct parent
            if len(parent_p['path']) >= 2:
                full_path = parent_p['path']
                base_path = "/".join(parent_p['path'][1:])
                parent_p = self.get_path(base_path, parent_p)
                parent_p['path'] = full_path

            # get the child, update its meta
            if name in parent_p['children']:
                child_p = parent_p['children'][name]
            # update the parent itself
            elif name in parent_p['path']:
                child_p = parent_p

            # We have to update the props
            props = self.valid_props(props)
            epnames_tag = '_epnames_{}'.format(user_info[0])
            child_p['meta'].update(props)

            # if _id key is present in meta and it has no value, we have
            # to remove it from meta dictionary
            if '_id' in child_p['meta'].keys() and not child_p['meta'].get('_id', False):
                child_p['meta'].pop('_id')

            # If the epnames tag exists in resources
            if epnames_tag in child_p['meta']:
                # And the tag is empty
                if not child_p['meta'][epnames_tag]:
                    logDebug('User {}: Deleting `{}` tag from resources.'.format(user_info[0], epnames_tag))
                    del child_p['meta'][epnames_tag]
        return "true"


    @cherrypy.expose
    def set_sut(self, name, parent=None, props={}):
        """
        Higher level wrapper over functions Create new SUT, create component and update meta.
        """
        if parent == '/' or parent == '1':
            if name[0] != '/':
                name = '/' + name
            ndata = self.get_sut(name, props)
            if not isinstance(ndata, dict):
                return self.create_new_sut(name, parent, props)
            else:
                return self.update_meta_sut(name, parent, props)

        # The parent is NOT root
        self.get_sut(parent, props)
        pdata = self.get_resource(parent)
        user_info = self.user_info(props)

        if not isinstance(pdata, dict):
            logWarning('User `{}`: No such parent `{}`!'.format(user_info[0], parent))
            return False

        # If exists, update meta
        if name in pdata['children']:
            return self.update_meta_sut(name, parent, props)
        # This is a new component
        else:
            return self.create_component_sut(name, parent, props)


    @cherrypy.expose
    def rename_sut(self, res_query, new_name, props={}):
        """
        Rename a SUT if it is not reserved or locked by someone.
        If its asked to rename the root of a sut and
        new_name doesn't specify the type (user/system)
        we add ".user". We do that by creating a new Sut having
        name: new_name and delete the old Sut.
        """
        user_info = self.user_info(props)
        logFull('CeSuts:rename_sut {} {}'.format(res_query, props))

        if '/' in new_name or ':' in new_name:
            msg = 'New resource name ({}) cannot contain `/` or `:`!'.format(new_name)
            logError(msg)
            return '*ERROR* ' + msg

        if ':' in res_query:
            res_query = res_query.split(':')[0]

        usr_sut_list = self.list_all_suts(user_info[0])

        # check if res_query exists
        if res_query[0] == '/':
            res_query = res_query[1:]

        found_old_sut = [item for item in usr_sut_list if item['name'] == res_query]
        if not found_old_sut:
            msg = 'User {}: SUT file {} doesn\'t exist !'.format(user_info[0], res_query)
            logError(msg)
            return '*ERROR* ' + msg

        # add 'user' or 'system' at the end of the new_name if it does not have it
        if new_name.split('.')[-1] != 'user' and new_name.split('.')[-1] != 'system':
            if res_query.split('.')[-1] == 'user' or res_query.split('.')[-1] == 'system':
                new_name = '.'.join([new_name, res_query.split('.')[-1]])
            else:
                new_name = '.'.join([new_name, 'user'])

        # check that the 'new_name' doesn't exists
        found_new_sut = [item for item in usr_sut_list if item['name'] == new_name]
        if found_new_sut:
            msg = 'User {}: New SUT file {} already exist !'.format(user_info[0], new_name)
            logError(msg)
            return '*ERROR* ' + msg

        # make sure the SUT file names start with /
        if res_query[0] != '/':
            res_query = '/' + res_query
        if new_name[0] != '/':
            new_name = '/' + new_name

        if new_name == res_query:
            msg = "Not renaming: Both the current name and the new name are the same."
            logError(msg)
            return "*ERROR*" + msg

        # Check if resource is reserved; if so, it cannot be renamed
        _is_res_reserved = self.is_resource_reserved(res_query, props)
        if _is_res_reserved:
            msg = 'User {}: Cannot delete: The resource is reserved for {} !'\
            .format(user_info[0], _is_res_reserved)
            logError(msg)
            return '*ERROR* ' + msg

        _is_res_locked = self.is_resource_locked(res_query)
        if _is_res_locked and _is_res_locked != user_info[0]:
            msg = 'User {}: Reserve resource: The resource is locked for {} !'\
            .format(user_info[0], _is_res_locked)
            logError(msg)
            return '*ERROR* ' + msg

        # Create a new SUT having this new name
        new_sut_id = self.create_new_sut(new_name, "/", props)

        if  isinstance(new_sut_id, str):
            if '*ERROR*' in new_sut_id:
                msg = 'User {}: New SUT file {} cannot be created!'.format(user_info[0], new_name)
                logError(msg)
                return '*ERROR* ' + msg

        reserve_res = self.reserve_resource(new_name, props)
        if  isinstance(reserve_res, str):
            if '*ERROR*' in reserve_res:
                msg = 'User {}: New SUT file {} cannot be reserved!'.format(user_info[0], new_name)
                logError(msg)
                return '*ERROR* ' + msg

        # method to clean the new SUT if needed
        def clean_new_sut(new_sut, user):
            """
            Delete the new SUT if the rename Failed.
            """
            self.reservedResources[user].pop(new_sut)
            if not self.reservedResources[user]:
                self.reservedResources.pop(user)
            self.delete_sut(new_sut, props)

        # Try to reserve source SUT file; if error, clean up the new SUT
        reserve_res = self.reserve_resource(res_query, props)
        if  isinstance(reserve_res, str):
            if '*ERROR*' in reserve_res:
                msg = 'User {}: Source SUT file {} cannot be reserved!'.format(user_info[0], res_query)
                logError(msg)
                clean_new_sut(new_sut_id, user_info[0])
                return '*ERROR* ' + msg

        # get the new path
        new_sut = self.reservedResources[user_info[0]][new_sut_id]
        # get the old sut
        old_sut = self.get_reserved_resource(res_query, props)

        # get all the structure of the old sut
        new_sut['meta'] = old_sut['meta']
        new_sut['children'] = old_sut['children']
        # if the sut has children we have to update the path
        self.change_path(new_sut, new_sut['path'])

        # release the old sut; and delete if needed
        self.reservedResources[user_info[0]].pop(old_sut['id'])
        if not self.reservedResources[user_info[0]]:
            self.reservedResources.pop(user_info[0])

        deleted = self.delete_sut(res_query, props)
        if  isinstance(deleted, str) and deleted.startswith('*ERROR*'):
            #could not delete the old sut so we keep it and delete the new one
            clean_new_sut(new_sut_id, user_info[0])
            msg = "User {} :We couldn't delete the old sut so we cannot complete the rename operation."\
            .format(user_info[0])
            logError(msg)
            return '*ERROR* ' + msg
        else:
            # save and release the new sut
            self.save_release_reserved_sut(new_name, props)

        return "True"


    @cherrypy.expose
    def rename_meta_sut(self, res_query, new_name, props={}):
        """
        Rename meta for SUT.
        SUT must be reserved.
        """
        user_info = self.user_info(props)
        logFull('CeSuts:get_meta_sut {} {}'.format(res_query, props))

        if ':' in res_query:
            meta = res_query.split(':')[1]
            res_query = res_query.split(':')[0]
        else:
            logError("CeSuts:get_meta_sut: User {} called this method without meta!".format(user_info[0]))
            return "false"

        #what if this sut is already reserved by other user? We STOP
        _is_res_reserved = self.is_resource_reserved(res_query, props)
        if _is_res_reserved and _is_res_reserved != user_info[0]:
            msg = 'User {}: Cannot update meta: The resource is reserved for {} !'\
            .format(user_info[0], _is_res_reserved)
            logError(msg)
            return '*ERROR* ' + msg

        #what if this sut is already locked by other user? We STOP
        _is_res_locked = self.is_resource_locked(res_query)
        if _is_res_locked and _is_res_locked != user_info[0]:
            msg = 'User {}: Reserve resource: The resource is locked for {} !'.format(user_info[0], _is_res_locked)
            logError(msg)
            return '*ERROR* ' + msg

        with self.acc_lock:
            parent_p = self.get_reserved_resource(res_query, props)

            if not parent_p:
                logError('Cannot access reserved SUT, path or ID `{}` !'.format(res_query))
                return False
            try:
                if isinstance(parent_p['path'], list):
                    # modify meta to the parent
                    if len(parent_p['path']) == 1:
                        child = parent_p
                    # modify to a component
                    else:
                        base_path = "/".join(parent_p['path'][1:])
                        child = self.get_path(base_path, parent_p)
                child['meta'][new_name] = child['meta'].pop(meta)
            except Exception:
                msg = "This meta that you entered thoes not exist {}".format(meta)
                logDebug(msg)
                return "false"

        return self.save_reserved_sut(res_query, props)


    @cherrypy.expose
    def delete_component_sut(self, res_query, props={}):
        """
        Permanently delete a component of a SUT or meta.
        It can be deleted only if SUT is reserved.
        """
        user_info = self.user_info(props)
        user = user_info[0]
        logFull('CeSuts:delete_component_sut {}'.format(res_query))

        if ':' in res_query:
            meta = res_query.split(':')[1]
            res_query = res_query.split(':')[0]
        else:
            meta = ''

        # Check if resource is reserved; if so, it cannot be deleted
        _is_res_reserved = self.is_resource_reserved(res_query, props)
        if _is_res_reserved and _is_res_reserved != user:
            msg = 'User {}: Cannot delete: The resource is reserved for {} !'.format(
                user, _is_res_reserved)
            logWarning(msg)
            return '*ERROR* ' + msg

        _is_res_locked = self.is_resource_locked(res_query)
        if _is_res_locked and _is_res_locked != user:
            msg = 'User {}: Cannot delete: The resource is locked for {} !'.format(
                user, _is_res_locked)
            logWarning(msg)
            return '*ERROR* ' + msg

        # The resource should be reserved
        parent_p = self.get_reserved_resource(res_query, props)

        if not parent_p:
            logWarning('User {}: Cannot access reserved SUT, path or ID `{}` !'.format(
                user, res_query))
            return False

        # Delete meta
        if meta:
            # we have to delete only the meta property
            correct_path = copy.deepcopy(parent_p['path'])

            # modify meta for parent
            if len(parent_p['path']) == 1:
                child = parent_p
            # modify meta for component
            else:
                base_path = "/".join(parent_p['path'][1:])
                child = self.get_path(base_path, parent_p)
            try:
                child['meta'].pop(meta)
            except Exception:
                msg = 'User {}: Property `{}` does not exist!'.format(user, meta)
                logWarning(msg)
                return 'false'
            child['path'] = correct_path

        # Delete component
        else:
            full_path = ''
            # the resources is deep in the tree, have to get its direct parent
            if len(parent_p['path']) > 2:
                full_path = copy.deepcopy(parent_p['path'])
                base_path = "/".join(parent_p['path'][1:-1])
                parent_p = self.get_path(base_path, parent_p)

            if not full_path:
                full_path = parent_p['path']
            parent_p['children'].pop(full_path[-1])
            parent_p['path'] = full_path[:-1]

        return 'true'


    @cherrypy.expose
    def delete_sut(self, res_query, props={}):
        """
        Permanently delete a SUT.
        Sut can be deteleted only if it is not reserved by anyone.
        """
        user_info = self.user_info(props)
        logFull('CeSuts:delete_sut {}'.format(res_query))

        # Check if resource is reserved; if so, it cannot be deleted
        _is_res_reserved = self.is_resource_reserved(res_query, props)
        if _is_res_reserved:
            msg = 'User {}: Cannot delete: The resource is reserved for {} !'\
            .format(user_info[0], _is_res_reserved)
            logError(msg)
            return '*ERROR* ' + msg

        _is_res_locked = self.is_resource_locked(res_query)
        if _is_res_locked:
            msg = 'User {}: Reserve resource: The resource is locked for {} !'\
            .format(user_info[0], _is_res_locked)
            logError(msg)
            return '*ERROR* ' + msg

        usr_home = userHome(user_info[0])

        # temporary fix; the SUT must be removed from self.resources
        def delete_sut_memory(sut_to_remove):
            parent_p = self.get_resource('/')

            if parent_p is not None and parent_p['children'].get(sut_to_remove) is not None:
                parent_p['children'].pop(sut_to_remove)
        # end temporary fix

        # SUT file can be user or system file
        if res_query.split('.')[-1] == 'system':
            suts_gb_path = self.project.get_user_info(user_info[0], 'sys_sut_path')
            if not suts_gb_path:
                suts_gb_path = '{}/config/sut/'.format(TWISTER_PATH)
            try:
                os.remove(suts_gb_path + res_query.split('.')[0] + '.json')
                delete_sut_memory(res_query.split('/')[-1])
                return "True"
            except Exception as exp_err:
                msg = 'User {}: Cannot delete SUT file: `{}` !'.format(user_info[0], res_query.split('.')[0] + '.json')
                logError(msg + " ERROR: " + exp_err)
                return '*ERROR* ' + msg
            return "True"
        else:
            usr_sut_path = self.project.get_user_info(user_info[0], 'sut_path')
            if not usr_sut_path:
                usr_sut_path = '{}/twister/config/sut/'.format(usr_home)
            delete_sut_memory(res_query.split('/')[-1])

            # delete from id_list if possible
            try:
                del self.id_list[res_query]
            except Exception:
                logDebug('User {}: id_list does not contain the sut: {}'.format(user_info[0], res_query))

            # get user SUT file; we have to check if the cleacase plugin
            # is activated; if so, use it to read the SUT files from view;
            # else use the UserService to read it
            cc_cfg = self.project.get_clearcase_config(user_info[0], 'sut_path')
            if cc_cfg:
                view = cc_cfg['view']
                actv = cc_cfg['actv']
                path = cc_cfg['path']
                user_view_actv = '{}:{}:{}'.format(user_info[0], view, actv)
                if path[-1] != '/' and res_query[-1] != '/':
                    complete_sut_path = path + '/' + res_query.split('.')[0] + '.json'
                else:
                    complete_sut_path = path + res_query.split('.')[0] + '.json'
                return self.project.clearFs.delete_user_file(user_view_actv, complete_sut_path)
            else:
                if usr_sut_path[-1] != '/' and res_query[-1] != '/':
                    complete_sut_path = usr_sut_path + '/' + res_query.split('.')[0] + '.json'
                else:
                    complete_sut_path = usr_sut_path + res_query.split('.')[0] + '.json'
                return self.project.localFs.delete_user_file(user_info[0], complete_sut_path)


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
            s_suts = ['{}.system'.format(os.path.splitext(d)[0]) \
            for d in os.listdir(sys_sut_path) \
            if os.path.splitext(d)[1] == '.json']
            suts.extend(s_suts)

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
                return '*ERROR* ' + resp
            for f_file in resp['children']:
                f_name, file_ext = os.path.splitext(f_file['path'])
                if file_ext and file_ext == '.json':
                    suts.append(f_name + '.user')
        else:
            if os.path.isdir(usr_sut_path):
                resp = self.project.localFs.list_user_files(user, usr_sut_path, False, False)
                if isinstance(resp, str):
                    logWarning(resp)
                for f_file in resp['children']:
                    f_name, file_ext = os.path.splitext(f_file['path'])
                    if file_ext and file_ext == '.json':
                        suts.append(f_name + '.user')

        def quick_find_path(dictionary, spath):
            """
            Find path.
            """
            for usr, locks in dictionary.iteritems():
                for id_sut, data in locks.iteritems():
                    path = data.get('path', [''])
                    if isinstance(path, str) or isinstance(path, unicode):
                        path = [path]
                    if path == [spath]:
                        return usr
            return False

        for s_sut in sorted(suts):
            ruser = quick_find_path(self.reservedResources, s_sut)
            luser = quick_find_path(self.lockedResources, s_sut)

            if (not ruser) and (not luser):
                result.append({'name': s_sut, 'status': 'free'})
            elif ruser:
                result.append({'name': s_sut, 'status': 'reserved', 'user': ruser})
            elif luser:
                result.append({'name': s_sut, 'status': 'locked', 'user': luser})
            # Both reserved and locked ?
            else:
                result.append({'name': s_sut, 'status': 'reserved', 'user': ruser})
        
        suts_on_disk = [s['name'] for s in result]

        # if the status of the CE is stopped for the current user
        # update the CE memory; check for consistency
        status = self.project.users[user]['status']
        if status == 0:
            suts_in_memory = self.resources['children'].keys()
            for sut in suts_in_memory:
                if sut not in suts_on_disk:
                    id = self.resources['children'][sut].get('id')
                    if user in self.reservedResources and id in self.reservedResources[user]:
                        logDebug('Removed sut `{}` from reserved resources.'.format(sut))
                        self.reservedResources[user].pop(id)
                    if user in self.lockedResources and id in self.lockedResources[user]:
                        logDebug('Removed sut `{}` from locked resources.'.format(sut))
                        self.lockedResources[user].pop(id)
                    logDebug('Removed sut `{}` from memory.'.format(sut))
                    self.resources['children'].pop(sut)

        logDebug('User {}: Fast listing SUTs... Found {}.'.format(user, suts))

        return result


    @cherrypy.expose
    def import_sut_xml(self, xml_file, sut_type='user', props={}):
        """
        Import one sut XML file.
        """
        user_info = self.user_info(props)
        user = user_info[0]

        logDebug('User {}: import XML file `{}`...'.format(user, xml_file))

        try:
            params_xml = etree.parse(xml_file)
        except Exception:
            msg = "The file you selected: '{}' it's not an xml file. Try again!".format(xml_file)
            logDebug(msg)
            return '*ERROR* ' + msg

        # parse the xml file and build the json format
        xml_ret = xml_to_res(params_xml, {})

        # build the filename to be saved; xml_file has absolute path; we need
        # to extract the last string after /, remove extension and add .json
        sut_file = xml_file.split('/')[-1].split('.')[0]
        sut_file = sut_file + '.json'

        sut_path = None
        if sut_type == 'system':
            # System SUT path
            sut_path = self.project.get_user_info(user, 'sys_sut_path')
            if not sut_path:
                sut_path = '{}/config/sut/'.format(TWISTER_PATH)
        else:
            # User SUT path
            sut_path = self.project.get_user_info(user, 'sut_path')
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
    def export_sut_xml(self, xml_file, query, props={}):
        """
        Export as XML file.
        """
        user_info = self.user_info(props)
        user = user_info[0]

        logDebug('User {}: export XML file `{}`, query = {}...'.format(user, xml_file, query))

        sut_path = None
        sut_type = query.split('.')[-1]
        if sut_type == 'system':
            # System SUT path
            sut_path = self.project.get_user_info(user, 'sys_sut_path')
            if not sut_path:
                sut_path = '{}/config/sut/'.format(TWISTER_PATH)
        else:
            # User SUT path
            sut_path = self.project.get_user_info(user, 'sut_path')
            if not sut_path:
                usr_home = userHome(user)
                sut_path = '{}/twister/config/sut/'.format(usr_home)

        sut_filename = sut_path + '/' + query.split('/')[1].split('.')[0] + '.json'
        logInfo('User {}: Export SUT file `{}` to `{}`.'.format(user, sut_filename, xml_file))

        # read the content of the user SUT file and load it in json
        if sut_type == 'system':
            resp = self.project.localFs.read_system_file(sut_filename, 'r')
        else:
            resp = self.project.localFs.read_user_file(user, sut_filename, 'r')

        try:
            json_resp = json.loads(resp)
        except Exception:
            msg = "User {}: Cannot load SUT file `{}`!".format(user, sut_filename)
            logWarning(msg)
            return '*ERROR* ' + msg

        # generate the xml structure
        xml = etree.Element('root')
        res_to_xml(json_resp, xml)

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
    def lock_sut(self, res_query, props={}):
        """
        Lock SUT. Add to lockedResources
        """
        return self.lock_resource(res_query, props)


    @cherrypy.expose
    def unlock_sut(self, res_query, props={}):
        """
        Unlock SUT. Delete from lockedResources.
        """
        return self.unlock_resource(res_query, props)


    @cherrypy.expose
    def is_sut_locked(self, res_query):
        """
        Verify if SUT is locked.
        """
        result = self.is_resource_locked(res_query)
        if not result:
            return "false"
        return result


    @cherrypy.expose
    def is_sut_reserved(self, res_query, props={}):
        """
        Verify if SUT is reserved.
        """
        result = self.is_resource_reserved(res_query, props)
        if not result:
            return "false"
        return result


    @cherrypy.expose
    def save_reserved_sut_as(self, name, res_query, props={}):
        """
        Save a reserved SUT as name+path.
        """
        user_info = self.user_info(props)
        user = user_info[0]
        logFull('CeSuts:save_reserved_sut_as {} {} {}'.format(name, res_query, user))
        path = '/'.join(name.split('/')[:-1])
        name = name.split('/')[-1]
        # add a '_' at the begining to be able to save as a new sut with the same name as the old one
        # the sut is deleted from memory after the json.dump
        target_name = '/_'+name+ '.' +res_query.split('.')[-1]#'.user'

        # verify if the sut exists
        usr_sut_list = self.list_all_suts(user)
        if res_query[0] == '/':
            res_query = res_query[1:]

        found_old_sut = [item for item in usr_sut_list if item['name'] == res_query]
        if not found_old_sut:
            msg = 'User {}: SUT file {} doesn\'t exist !'.format(user, res_query)
            logError(msg)
            return '*ERROR* ' + msg

        res_query = '/' + res_query
        # #verify if a SUT having the same name exists
        found_new_sut = [item for item in usr_sut_list if item['name'] == target_name]
        if found_new_sut:
            msg = 'User {}: New SUT file {} already exist !'.format(user, target_name)
            logError(msg)
            return '*ERROR* ' + msg

        # Check if resource is reserved; if so, it cannot be deleted
        _is_res_reserved = self.is_resource_reserved(res_query, props)
        if _is_res_reserved and _is_res_reserved != user:
            msg = 'User {}: Cannot save as: The resource is reserved for {} !'.\
            format(user, _is_res_reserved)
            logError(msg)
            return '*ERROR* ' + msg

        _is_res_locked = self.is_resource_locked(res_query)
        if _is_res_locked and _is_res_locked != user:
            msg = 'User {}: Reserve resource: The resource is locked for {} !'.\
            format(user, _is_res_locked)
            logError(msg)
            return '*ERROR* ' + msg

        # Create a new SUT having this new name
        new_sut_id = self.create_new_sut(target_name, '/', props, False)

        if isinstance(new_sut_id, str) and '*ERROR*' in new_sut_id:
            msg = 'User {}: New SUT file {} cannot be created!'.format(user, target_name)
            logError(msg)
            return '*ERROR* ' + msg

        # Reserve the target SUT
        self.reserve_resource(target_name, props)
        # Get the new path
        new_sut = self.reservedResources[user_info[0]][new_sut_id]
        # Get the old sut
        old_sut = self.get_reserved_resource(res_query, props)

        # Get all the structure of the old sut
        new_sut['meta'].update(copy.deepcopy(old_sut['meta']))
        # Copy children
        new_sut['children'].update(copy.deepcopy(old_sut['children']))

        # Recursive fix children IDs
        self.change_ids(new_sut)
        # Recursive fix children paths
        self.change_path(new_sut, new_sut['path'])

        # Exit now
        return self.save_reserved_sut(target_name, '{}', path)


    @cherrypy.expose
    def save_reserved_sut(self, res_query, props={}, path=''):
        """
        User has made some changes only on self.reserved_resources.
        In this method we sync self.reserved_resources with self.resources
        and the store on the disk
        """
        user_info = self.user_info(props)
        logFull('CeSuts:save_reserved_sut {} {}'.format(res_query, user_info[0]))

        resources = self.resources

        # If no resources...
        if not resources.get('children'):
            msg = 'User {}: Save reserved resource: There are no resources defined !'.format(user_info[0])
            logError(msg)
            return '*ERROR* ' + msg

        user_info = self.user_info(props)

        if ':' in res_query:
            res_query = res_query.split(':')[0]

        if not self.reservedResources.get(user_info[0]):
            msg = "It seems that this user does not have changes to save! {}".format(user_info[0])
            logDebug(msg)
            return '*ERROR* ' + msg

        resource_node = self.get_resource(res_query)
        if not resource_node or isinstance(resource_node, str):
            msg = 'User {}: Cannot find SUT {}'.format(user_info[0], res_query)
            logFull(msg)
            return '*ERROR* ' + msg

        if len(resource_node['path']) > 1:
            resource_node = self.get_path(resource_node['path'][0], resources)

        reserved_node = self.reservedResources[user_info[0]][resource_node['id']]

        # Maybe the user renamed the TB
        if reserved_node['path'][0] != resource_node['path'][0]:
            self.resources['children'][reserved_node['path'][0]] = \
            self.resources['children'].pop(resource_node['path'][0])
        # ...or maybe the name of the resource is the same
        resources['children'].update([(reserved_node['path'][0], reserved_node), ])

        # Update path
        resources['children'][reserved_node['path'][0]]['path'] = [reserved_node['path'][0]]
        # Now save
        if path == '':
            issaved = self.save_sut(props, resource_node['path'][0])
        else:
            issaved = self.save_sut_as(resource_node['path'][0], path)

        if isinstance(issaved, str):
            logDebug("We could not save this Sut for user = {}.".format(user_info[0]))
            return issaved
        return True


    @cherrypy.expose
    def save_release_reserved_sut(self, res_query, props={}):
        """
        Save the changes. Sync self.resources with self.reserved_resources
        and save to the disk
        """
        user_info = self.user_info(props)
        logFull('CeSuts:save_release_reserved_sut {} {} {}'.format(res_query, props, user_info[0]))

        result = self.save_reserved_sut(res_query, props)

        if result and not isinstance(result, str):
            if ':' in res_query:
                res_query = res_query.split(':')[0]

            # Having the id, we can discard and release directly
            if user_info[0] in self.reservedResources.keys():

                if res_query in self.reservedResources[user_info[0]]:
                    node_id = res_query
                else:

                    resource_node = self.get_resource(res_query)
                    if not resource_node or isinstance(resource_node, str):
                        logFull('User {} can not find the resource {}'.format(user_info[0], res_query))
                        return None

                    if len(resource_node['path']) > 1:
                        resource_node = self.get_path(resource_node['path'][0], self.resources)

                    node_id = resource_node['id']

                reserved_node = self.reservedResources[user_info[0]][node_id]
                self.reservedResources[user_info[0]].pop(reserved_node['id'])
                if not self.reservedResources[user_info[0]]:
                    self.reservedResources.pop(user_info[0])
            return True
        else:
            return result


    @cherrypy.expose
    def discard_release_reserved_sut(self, res_query, props={}):
        """
        Discard changes and release SUT.
        Delete entry from reservedResources.
        """
        return self.discard_release_reserved_resource(res_query, props)


    @cherrypy.expose
    def consistency_check_suts(self, user):
        """
        Makes a diff between the content of the self.resources dictionary and what is on the disk.
        If a sut is in dictionary and is not on the disk anymore, then it is deleted form the self.resources.
        If a new sut is on the disk, it is loaded in memory.
        """
        def get_disk_sut_names(suts_on_disk):
            sut_names = []
            for sut_d in suts_on_disk:
                sut_names.append(sut_d['name'])
            return sut_names
        
        # listing all suts
        result = self.list_all_suts(user)

        suts_on_disk = get_disk_sut_names(result)

        # if the status of the CE is stopped for the current user
        # update the CE memory
        status = self.project.users[user]['status']
        if status == 0:
            suts_in_memory = self.resources['children'].keys()
            for sut in suts_in_memory:
                if sut not in suts_on_disk:
                    id = self.resources['children'][sut].get('id')
                    if user in self.reservedResources and id in self.reservedResources[user]:
                        logDebug('Removed sut `{}` from reserved resources.'.format(sut))
                        self.reservedResources[user].pop(id)
                    else:
                        logDebug('Sut `{}` cannot be removed from the reserved resources.'.format(sut))
                        continue
                    if user in self.lockedResources and id in self.lockedResources[user]:
                        logDebug('Removed sut `{}` from locked resources.'.format(sut))
                        self.lockedResources[user].pop(id)
                    else:
                        logDebug('Sut `{}` cannot be removed from the locked resources.'.format(sut))
                        continue
                    logDebug('Removed sut `{}` from memory.'.format(sut))
                    self.resources['children'].pop(sut)

        return result


# Eof()
