# File: CeCommonAllocator.py ; This file is part of Twister.

# version: 3.005

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
Common methods for TB or SUT allocator
'''

import os
import sys
import ast
import copy

import cherrypy
from binascii import hexlify

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print 'TWISTER_PATH environment variable is not set! Exiting!'
    exit(1)
if TWISTER_PATH not in sys.path:
    sys.path.append(TWISTER_PATH)

from common.tsclogging import logFull, logDebug, logError

#

class CommonAllocator(object):
    """
    Common class for TestBeds and SUTs
    """

    def __init__(self):

        self.project = None
        self.resources = dict()
        self.reservedResources = dict()
        self.lockedResources = dict()
        self.acc_lock = None
        self.ren_lock = None
        self.imp_lock = None
        self.save_lock = None
        self.load_lock = None


    def user_info(self, props={}):
        """
        This method returns info about user. The list returned: [user_name, user_roles]
        """
        logFull('CeCommonAllocator:user_info')
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
        return [user_roles.get('user'), user_roles]


    def fix_path(self, res, path=[], modified=False):
        """
        Add path to resources that does not have this field.
        """
        if not res:
            return modified

        if not 'path' in res:
            modified = True
            res['path'] = copy.deepcopy(path)

        if not res.get('children'):
            try:
                path.pop(-1)
            except:
                pass
            return modified

        for node in res.get('children'):
            path.append(node)

            modified = self.fix_path(res['children'][node], path, modified)

        return modified


    def get_id(self, node_id, resource):
        """
        This method searches in resource for node_id and returns its dictionary.
        Also, in the path key we save the complete path from root to this node_id.
        """
        if not resource:
            return None

        if resource.get('id') == node_id:
            return resource

        if not resource.get('children'):
            return None

        for node in resource.get('children'):
            result = self.get_id(node_id, resource['children'][node])

            if result:
                return result


    def get_path(self, query, resource):
        """
        This method searches in resource for a path (query) and returns its dictionary.
        Also, in the path key we save the absolute path (from root)
        """
        parts = [q for q in query.split('/') if q]

        for part in parts:
            if not resource:
                logFull('Did not find a result for this query: {}!'.format(query))
                return None

            if part in resource['children']:
                resource = resource['children'].get(part)
            else:
                logFull('Did not find a result for this path: {}!'.format(part))
                return None

        return resource


    def change_path(self, parent_node, path):
        """
        Update the path of all children, if the parent_node is renamed for example.
        """
        # The node is valid ?
        if not isinstance(parent_node, dict):
            return False
        # This node has children ?
        if not isinstance(parent_node.get('children'), dict):
            return True

        for node in parent_node.get('children'):
            parent_node['children'][node]['path'] = path + [node]
            self.change_path(parent_node['children'][node], parent_node['children'][node]['path'])

        return True


    def change_ids(self, parent_node):
        """
        Update the IDs of all children.
        """
        # The node is valid ?
        if not isinstance(parent_node, dict):
            return False
        # This node has children ?
        if not isinstance(parent_node.get('children'), dict):
            return False

        for node in parent_node['children']:
            parent_node['children'][node]['id'] = hexlify(os.urandom(5))
            self.change_ids(parent_node['children'][node])

        return True


    def get_resource(self, query, resource=None):
        """
        Get the resource from resource by path or id.
        We can search for query in self.resources or in any other resource given as parameter.
        """
        logFull("CeCommonAllocator: Getting the resource {}".format(query))

        if not resource:
            resource = self.resources

        if not resource or not query:
            msg = 'Cannot get a null resource {} or a new query {}!'.format(resource, query)
            logError(msg)
            return False

        if ':' in query:
            query = query.split(':')[0]

        # If the query is an ID
        if '/' not in query:
            result = self.get_id(query, resource)
        else:
            result = self.get_path(query, resource)

        if result:
            return dict(result)

        return result


    def valid_props(self, props):
        """
        Verify if we have recevied valid props.
        """
        logDebug('CeCommonAllocator: valid_props: props = {} '.format(props))

        if not props:
            return dict()
        if isinstance(props, dict):
            return props
        elif isinstance(props, str) or isinstance(props, unicode):
            props = props.strip()
            try:
                props = ast.literal_eval(props)
            except Exception as exp_err:
                logError('Cannot parse properties: `{}`, `{}` !'.format(props, exp_err))
                return None
        else:
            logError('Invalid properties for set method`{}` !'.format(props))
            return False
        return props


    def generate_index(self):
        """
        Generate index when creating a new sut, or test bed.
        """
        logDebug('CeCommonAllocator: generate_index')
        new_sut_id = False

        while not new_sut_id:
            new_sut_id = hexlify(os.urandom(5))
            # If by any chance, this ID already exists, generate another one!
            exists_id = self.get_id(new_sut_id, self.resources)
            if exists_id:
                new_sut_id = False

        return new_sut_id


    def format_resource(self, result, query):
        """
        We have to return data in a certain form - a formated dictionary.
        """

        logDebug('CeCommonAllocator: format_resource query = {}'.format(query))

        meta = ""
        if ':' in query:
            meta = query.split(':')[1]
        if not meta:
            result['children'] = sorted([result['children'][node]['id'] for \
            node in result.get('children') or []], \
            key=lambda node: node.lower())

            if isinstance(result['path'], list):
                result['path'] = '/'.join(result.get('path', []))

            if result['meta'] == '{}':
                result['meta'] = dict()
        else:
            result = result['meta'].get(meta, '')

        return result


    def reserve_resource(self, res_query, props={}):
        """
        reserve a resource for a certain user
        """

        try:
            source = 'xmlrpc' if cherrypy.session.get('username') else 'error' # call from the applet
        except:
            source = 'rpyc' # call from the tests

        user_info = self.user_info(props)
        logDebug('CeCommonAllocator:reserve_resource {} {} {} {}'.\
        format(res_query, props, user_info[0], self.type.upper()))

        # in case we recive meta info too
        if ':' in res_query:
            res_query = res_query.split(':')[0]

        with self.acc_lock:
            # verify if the resource is locked by other user
            _is_res_locked = self.is_resource_locked(res_query)
            if _is_res_locked:
                if _is_res_locked != user_info[0]:
                    msg = 'User {}: The resource is locked for {} !'.format(user_info[0], _is_res_locked)
                    logError(msg)
                    if source == 'rpyc':
                        return (False, 'TB_LOCKED')
                    else:
                        return '*ERROR* ' + msg
                else:
                    msg = 'User {}: Has already locked this resource: {}'.format(user_info[0], res_query)
                    logDebug(msg)
                    if source == 'rpyc':
                        return (False, 'TB_LOCKED')
                    else:
                        return True
            #verify is the resource is reserved by other user
            _is_res_reserved = self.is_resource_reserved(res_query)
            if _is_res_reserved:
                if _is_res_reserved != user_info[0]:
                    msg = 'User {}: The resource is reserved for {}!'.format(user_info[0], _is_res_reserved)
                    logError(msg)
                    if source == 'rpyc':
                        return (False, '{}_RESERVED'.format(self.type.upper()))
                    else:
                        return '*ERROR* ' + msg
                else:
                    msg = 'User {}: Has already reserved this resource: {}'.format(user_info[0], res_query)
                    logDebug(msg)
                    if source == 'rpyc':
                        return (False, '{}_RESERVED'.format(self.type.upper()))
                    else:
                        return True

            node_path = self.get_resource(res_query)

            if not node_path or isinstance(node_path, str):
                msg = "User {}: No such resource {}".format(user_info[0], res_query)
                logError(msg)
                if source == 'rpyc':
                    return (False, '{}_UNKNOWN'.format(self.type.upper()))
                else:
                    return "*ERROR* " + msg

            #we need to set as reserved the root of this resource
            if isinstance(node_path['path'], list) and len(node_path['path']) > 1:
                node_path = self.get_path(node_path['path'][0], self.resources)

                if not node_path:
                    msg = 'User {}: Reserve Resource: Cannot find resource path or ID !'.format(user_info[0])
                    logError(msg)
                    if source == 'rpyc':
                        return (False, '{}_RESERVED'.format(self.type.upper()))
                    else:
                        return '*ERROR* ' + msg

            #adding the resource to reservedResources dictionary
            if user_info[0] in self.reservedResources:
                self.reservedResources[user_info[0]].update([(node_path['id'], copy.deepcopy(node_path)), ])
            else:
                self.reservedResources.update([(user_info[0], {node_path['id']: copy.deepcopy(node_path)}), ])
        if source == 'rpyc':
            return (True, 'NO_ERROR')
        else:
            return True #RESOURCE_RESERVED


    def is_resource_reserved(self, res_query, props={}):
        """
        Verify if a resource is already reserved.
        Returns the user or false.
        """

        logFull('CeCommonAllocator:is_resource_reserved: res_query = {}'.format(res_query))

        resources = self.resources
        if '/' not in res_query:
            res_for_user = [u for u in self.reservedResources if res_query in self.reservedResources[u]]

        if '/' in res_query or not res_for_user:
            #if res_query contains components unsaved yet, search only for the TB
            if '/' in res_query:
                parts = [q for q in res_query.split('/') if q]
                node_path = self.get_resource('/' + parts[0])
            else:
                node_path = self.get_resource(res_query)

            if not node_path or isinstance(node_path, str):
                msg = "No such resource {}".format(res_query)
                logError(msg)
                return False

            if isinstance(node_path['path'], list) and len(node_path['path']) > 1:
                node_path = self.get_path(node_path['path'][0], resources)
                if not node_path and isinstance(node_path, str):
                    msg = "No such resource {}".format(res_query)
                    logError(msg)
                    return False


            res_for_user = [u for u in self.reservedResources if node_path['id'] in self.reservedResources[u]]

        if not res_for_user:
            return False
        return res_for_user[0]


    def get_reserved_resource(self, res_query, props={}):
        """
        Returns the reserved resource.
        """
        logDebug('Get reserved resource `{}`...'.format(res_query))

        resources = self.resources
        # If no resources...
        if not resources:
            msg = 'Get reserved resourcee: There are no resources defined !'
            logError(msg)
            return False

        user_info = self.user_info(props)
        user = user_info[0]

        if not self.reservedResources.get(user):
            msg = 'Get reserved resource: Resource `{}` is not reserved !'.format(res_query)
            logError(msg)
            return False

        # Maybe query is an ID of a component unsaved yet
        for p in self.reservedResources[user]:
            unsaved_res = self.get_resource(res_query, self.reservedResources[user][p])
            if unsaved_res:
                self.reservedResources[user][p]['path'] = unsaved_res['path']
                return self.reservedResources[user][p]

        # Get only the root parent in case the path query contains components unsaved yet
        parts = [q for q in res_query.split('/') if q]
        if '/' in res_query:
            parent_path = parts
            node_path = self.get_resource('/' + parts[0])
        # If query is an saved component
        else:
            node_path = self.get_resource(res_query)
            if node_path and isinstance(node_path, dict):
                parent_path = node_path['path']

        if not node_path:
            msg = 'Get reserved resource: Cannot find resource ID `{}` !'.format(res_query)
            logError(msg)
            return False

        if isinstance(node_path['path'], list) and len(node_path['path']) > 1:
            node_path = self.get_path(node_path['path'][0], resources)

        self.reservedResources[user][node_path['id']]['path'] = parent_path

        return self.reservedResources[user][node_path['id']]


    def lock_resource(self, res_query, props={}):
        """
        lock the resource res_query by adding it to the self.lockedResources dict
        """

        logDebug('CeCommonAllocator:lock_resource {} {}'.format(res_query, props))
        resources = self.resources
        user_info = self.user_info(props)

        # If no resources...
        if not resources.get('children'):
            msg = 'User {}: Lock resource: There are no resources defined !'.format(user_info[0])
            logError(msg)
            return '*ERROR* ' + msg

        if ':' in res_query:
            res_query = res_query.split(':')[0]

        with self.acc_lock:

            # verify if the resource is locked by other user
            _is_res_locked = self.is_resource_locked(res_query)
            if _is_res_locked:
                if _is_res_locked != user_info[0]:
                    msg = 'User {}: The resource is locked for {} !'.format(user_info[0], _is_res_locked)
                    logError(msg)
                    return '*ERROR* ' + msg
                else:
                    msg = 'User {}: Has already locked this resource: {}'.format(user_info[0], res_query)
                    logDebug(msg)
                    return True
            #verify is the resource is reserved by other user
            _is_res_reserved = self.is_resource_reserved(res_query)
            if _is_res_reserved:
                if _is_res_reserved != user_info[0]:
                    msg = 'User {}: The resource is reserved for {}!'.format(user_info[0], _is_res_reserved)
                    logError(msg)
                    return '*ERROR* ' + msg
                else:
                    msg = 'User {}: Has already reserved this resource: {}'.format(user_info[0], res_query)
                    logDebug(msg)
                    return True

            node = self.get_resource(res_query)

            if not node or isinstance(node, str):
                msg = "User {}: No such resource {}".format(user_info[0], res_query)
                logError(msg)
                return "*ERROR* " + msg

            if len(node['path']) > 1:
                node = self.get_path(node['path'][0], resources)
                if isinstance(node, str):
                    msg = 'User {}: Cannot find resource path or ID `{}` !'.format(user_info[0], res_query)
                    logError(msg)
                    return '*ERROR* ' + msg

            user_res = self.lockedResources.get(user_info[0], {})
            user_res.update({node['id']: copy.deepcopy(node)})
            self.lockedResources[user_info[0]] = user_res

        return True


    def unlock_resource(self, res_query, props={}):
        """
        unlock the resource, delete it from self.lockedResources dict
        """

        logDebug('CeCommonAllocator:unlock_resource {} {} '.format(res_query, props))
        user_info = self.user_info(props)
        #we need the id of the resource so we get it from self.resources

        node = self.get_resource(res_query)
        if not node or isinstance(node, str):
            msg = "No such resource {}".format(res_query)
            logError(msg)
            return "*ERROR* " + msg
        #we need to lock the root of the resource
        if len(node['path']) > 1:
            node = self.get_path(node['path'][0], self.resources)

        if isinstance(node, str):
            msg = 'User {}: Unlock resource: Cannot find resource path or ID `{}` !'.format(user_info[0], res_query)
            logError(msg)
            return '*ERROR* ' + msg

        with self.acc_lock:
            try:
                self.lockedResources[user_info[0]].pop(node['id'])
                if not self.lockedResources[user_info[0]]:
                    self.lockedResources.pop(user_info[0])
            except Exception as exp_err:
                msg = 'User {}: Unlock resource: `{}` !'.\
                format(user_info[0], exp_err)
                logError(msg)
                return "*ERROR* " + msg

        return True #RESOURCE_FREE


    def is_resource_locked(self, res_query):
        """
        check if a resource is in self.lockedResources dict
        returns the user or false
        """

        logFull('CeCommonAllocator:is_resource_locked: res_query = {}'.format(res_query))

        # Having the id we can get it directly
        if '/' not in res_query:
            lock_for_user = [u for u in self.lockedResources if res_query in self.lockedResources[u]]
        # Otherwise get the id from the path or get find the root parent of the resource
        if '/' in res_query or not lock_for_user:
            node = self.get_resource(res_query)
            if not node or isinstance(node, str):
                msg = "CeCommonAllocator: is_resource_locked: No such resource {}".format(res_query)
                logFull(msg)
                return False

            if len(node['path']) > 1:
                node = self.get_path(node['path'][0], self.resources)

            if isinstance(node, str):
                logFull('CeCommonAllocator: Cannot find resource path or ID `{}` !'.format(res_query))
                return  False

            lock_for_user = [u for u in self.lockedResources if node['id'] in self.lockedResources[u]]

        if not lock_for_user:
            return False

        return lock_for_user[0]


    def discard_release_reserved_resource(self, res_query, props={}):
        """
        Discard changes for both SUTs and TestBeds
        """

        user_info = self.user_info(props)
        user = user_info[0]
        logDebug('CeCommonAllocator: User {}: discard_release_reserved_resource: {}'.format(user, res_query))

        if ':' in res_query:
            res_query = res_query.split(':')[0]

        # Having the id, we can discard and release directly
        if user in self.reservedResources.keys():

            if res_query in self.reservedResources[user]:
                node_id = res_query
            # Having the name of the resource we have to get the id
            else:
                node = self.get_resource(res_query)
                if not isinstance(node, dict):
                    msg = "Could not found a result for {}".format(res_query)
                    logDebug(msg)
                    return False

                # get the root parent of this resource
                if len(node['path']) > 1:
                    node = self.get_path(node['path'][0], self.resources)

                if not node:
                    logError('User {}: Cannot find resource path or ID `{}` !'.format(user, res_query))
                    return False
                node_id = node['id']
            # Delete the entry from reserved dict
            try:
                self.reservedResources[user].pop(node_id)
                if not self.reservedResources[user]:
                    self.reservedResources.pop(user)
            except Exception as exp_err:
                logError('CeCommonAllocator:discard_release_reserved_resource: `{}` for user {}!'.format(exp_err, user))
                return False

        return True #RESOURCE_FREE


# Eof()
