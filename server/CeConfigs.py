
# File: CeConfigs.py ; This file is part of Twister.

# version: 3.002

# Copyright (C) 2012-2014 , Luxoft

# Authors:
#    Andrei Costachi <acostachi@luxoft.com>
#    Cristi Constantin <crconstantin@luxoft.com>
#    Mihai Dobre <mihdobre@luxoft.com>

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
Central Engine Config files manager
***********************************

This module is responsible with managing config files and folders.
"""

import os
import sys
from lxml import etree
from thread import allocate_lock

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print('TWISTER_PATH environment variable is not set! Exiting!')
    exit(1)
if TWISTER_PATH not in sys.path:
    sys.path.append(TWISTER_PATH)

from common.tsclogging import logDebug, logInfo, logWarning, logError


class CeConfigs(object):
    """
    Central Engine config manager class.
    """

    project = None # Pointer to Project instance
    glb_lock = allocate_lock() # Global variables lock
    cfg_lock = allocate_lock() # Config access lock
    config_locks = {} # Config locks list


    def __init__(self, project):
        """
        Initialize config manager.
        """
        self.project = project


    def _parse_common(self, xml, gparams):
        """
        Recursive parse globals / configs.
        """
        for folder in xml.xpath('folder'):
            tmp = {gparam.find('name').text: gparam.find('value').text or ''
                for gparam in folder.xpath('param')}
            tmp.update( self._parse_common(folder, tmp) )
            gparams[folder.find('fname').text] = tmp
        return gparams


    def _parse_globals(self, user):
        """
        Returns a dictionary containing all global parameters.
        """
        path_glob = self.project.get_user_info(user, 'glob_params')
        resp = self.project.localFs.read_user_file(user, path_glob)

        if resp.startswith('*ERROR*'):
            logWarning(resp)
            return {}

        gparams = self._parse_common(etree.fromstring(resp), {})
        return gparams


    def _parse_configs(self, user, globs_file):
        """
        Returns a dictionary containing all config parameters.
        """
        resp = self.read_config_file(user, globs_file)

        if resp.startswith('*ERROR*'):
            logWarning(resp)
            return {}

        gparams = self._parse_common(etree.fromstring(resp), {})
        return gparams


    def _find_global_variable(self, user, node_path, globs_file=False):
        """
        Helper function.
        """
        if not globs_file:
            var_pointer = self.project.users[user]['global_params']
        else:
            var_pointer = self._parse_configs(user, globs_file)
        if not var_pointer:
            return False

        for node in node_path:
            if node in var_pointer:
                var_pointer = var_pointer[node]
            else:
                # Invalid variable path
                return False

        return var_pointer


    def get_global_variable(self, user, variable, globs_file=False):
        """
        Sending a global variable, using a path.
        """
        r = self.project.authenticate(user)
        if not r:
            return False

        try:
            node_path = [v for v in variable.split('/') if v]
        except Exception:
            logWarning('Global Variable: Invalid variable type `{}`, for user `{}`!'.format(variable, user))
            return False

        var_pointer = self._find_global_variable(user, node_path, globs_file)

        if not var_pointer:
            node_path = '/'.join(node_path)
            if globs_file:
                logWarning('Global Variable: Invalid variable path `{}` in file `{}`, for user `{}`!'.format(node_path, globs_file, user))
            else:
                logWarning('Global Variable: Invalid variable path `{}`, for user `{}`!'.format(node_path, user))
            return False

        return var_pointer


    def set_global_variable(self, user, variable, value):
        """
        Set a global variable path, for a user.\n
        The change is not persistent.
        """
        r = self.project.authenticate(user)
        if not r:
            return False

        try:
            node_path = [v for v in variable.split('/') if v]
        except Exception:
            logWarning('Global Variable: Invalid variable type `{}`, for user `{}`!'.format(variable, user))
            return False

        if (not value) or (not str(value)):
            logWarning('Global Variable: Invalid value `{}`, for global variable `{}` from user `{}`!'\
                ''.format(value, variable, user))
            return False

        # If the path is in ROOT, it's a root variable
        if len(node_path) == 1:
            with self.glb_lock:
                self.project.users[user]['global_params'][node_path[0]] = value
            return True

        # If the path is more complex, the pointer here will go to the parent
        var_pointer = self._find_global_variable(user, node_path[:-1])

        if not var_pointer:
            logWarning('Global Variable: Invalid variable path `{}`, for user `{}`!'.format(node_path, user))
            return False

        with self.glb_lock:
            var_pointer[node_path[-1]] = value

        logDebug('Global Variable: Set variable `{} = {}`, for user `{}`!'.format(value, variable, user))
        return True


    def is_lock_config(self, user, fpath):
        """
        Complete path from tree - returns True/ False
        """
        if fpath in self.config_locks:
            logDebug('Config file `{}` is locked by `{}`.'.format(fpath, user))
        else:
            logDebug('Config file `{}` is not locked.'.format(fpath))
        return self.config_locks.get(fpath, False)


    def lock_config(self, user, fpath):
        """
        Complete path from tree - returns True/ False
        """
        # If already locked, return False
        if fpath in self.config_locks:
            err = '*ERROR* Config file `{}` is already locked by `{}`! Cannot lock!'.format(fpath, self.config_locks[fpath])
            logDebug(err)
            return err
        with self.cfg_lock:
            self.config_locks[fpath] = user
            logDebug('User `{}` is locking config file `{}`.'.format(user, fpath))
            return True


    def unlock_config(self, user, fpath):
        """
        Complete path from tree - returns True/ False
        """
        # If not locked, return False
        if fpath not in self.config_locks:
            err = '*ERROR* Config file `{}` is not locked'.format(fpath)
            logDebug(err)
            return err
        # If not locked by this user, return False
        if self.config_locks[fpath] != user:
            err = '*ERROR* Config file `{}` is locked by `{}`! Cannot unlock!'.format(fpath, self.config_locks[fpath])
            logDebug(err)
            return err
        with self.cfg_lock:
            del self.config_locks[fpath]
            logDebug('User `{}` is releasing config file `{}`.'.format(user, fpath))
            return True


    def read_config_file(self, user, fpath):
        """
        Read a config file.
        """
        # Auto detect if ClearCase Test Config Path is active
        ccConfig = self.project.get_clearcase_config(user, 'tcfg_path')
        if ccConfig:
            view = ccConfig['view']
            actv = ccConfig['actv']
            path = ccConfig['path'].rstrip('/')
            if not path:
                return '*ERROR* You did not set ClearCase Config Path!'
            user_view_actv = '{}:{}:{}'.format(user, view, actv)
            return self.project.clearFs.read_user_file(user_view_actv, path +'/'+ fpath)
        else:
            dirpath = self.project.get_user_info(user, 'tcfg_path')
            return self.project.localFs.read_user_file(user, dirpath + '/' + fpath)


    def save_config_file(self, user, fpath, content):
        """
        Save config file - returns a True/ False.
        """
        lock = self.config_locks.get(fpath, False)
        if lock and lock != user:
            err = '*ERROR* Config file `{}` is locked by `{}`! Cannot save!'.format(fpath, lock)
            logWarning(err)
            return err

        logDebug('Update config file `{}`, for user `{}`.'.format(fpath, user))

        # Auto detect if ClearCase Test Config Path is active
        ccConfig = self.project.get_clearcase_config(user, 'tcfg_path')
        if ccConfig:
            view = ccConfig['view']
            actv = ccConfig['actv']
            path = ccConfig['path'].rstrip('/')
            if not path:
                return '*ERROR* You did not set ClearCase Config Path!'
            user_view_actv = '{}:{}:{}'.format(user, view, actv)
            # If file exists
            fsz = self.project.clearFs.file_size(user_view_actv, path + '/' + fpath)
            # Cannot save an existing file that isn't locked!
            if isinstance(fsz, long) and not lock:
                err = '*ERROR* Cannot save CC config file `{}`, because it\'s not locked!'.format(fpath)
                logWarning(err)
                return err
            return self.project.write_file(user, path + '/' + fpath, content,
                type='clearcase:{}:{}'.format(view, actv))
        else:
            dirpath = self.project.get_user_info(user, 'tcfg_path')
            # If file exists
            fsz = self.project.localFs.file_size(user, dirpath + '/' + fpath)
            # Cannot save an existing file that isn't locked!
            if isinstance(fsz, long) and not lock:
                err = '*ERROR* Cannot save config file `{}`, because it\'s not locked!'.format(fpath)
                logWarning(err)
                return err
            return self.project.write_file(user, dirpath + '/' + fpath, content)


    def delete_config_file(self, user, fpath):
        """
        Delete config file - returns a True/ False.
        """
        lock = self.config_locks.get(fpath, False)
        # Cannot Delete a locked file!
        if lock:
            err = '*ERROR* Config file `{}` is locked by `{}`! Cannot delete!'.format(fpath, lock)
            logWarning(err)
            return err

        logDebug('Delete config file `{}`, for user `{}`.'.format(fpath, user))

        # Unbind the config file, if it was binded
        self.project.parsers[user].del_binding(fpath)

        # Auto detect if ClearCase Test Config Path is active
        ccConfig = self.project.get_clearcase_config(user, 'tcfg_path')
        if ccConfig:
            view = ccConfig['view']
            actv = ccConfig['actv']
            path = ccConfig['path'].rstrip('/')
            if not path:
                return '*ERROR* You did not set ClearCase Config Path!'
            user_view_actv = '{}:{}:{}'.format(user, view, actv)
            return self.project.clearFs.delete_user_file(user_view_actv, path + '/' + fpath)
        else:
            dirpath = self.project.get_user_info(user, 'tcfg_path')
            return self.project.localFs.delete_user_file(user, dirpath + '/' + fpath)


# Eof()
