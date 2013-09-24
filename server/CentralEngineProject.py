
# File: CentralEngineProject.py ; This file is part of Twister.

# version: 2.042

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
Project Class
*************

The **Project** class collects and organizes all the information for
 the Central Engine.

Information about *users*:

- user name
- user status (start, stop, pause)
- paths to logs and config files
- paths to script pre and script post
- parameters for this project like: libraries, tc delay, DB AutoSave
- global params for current user

Information about *EPs*:

- EP name
- EP status (start, stop, pause)
- EP OS
- EP IP

Information about *Suites*:

- suite name
- other info from Test-Suites.XML (eg: release, or build)
- test bed name
- panic detect

Information about *Test Files*:

- file name
- complete file path
- test title
- test description
- timeout value (if any)
- test status (pass, fail, skip, etc)
- crash detected
- test params
- test date started and finished
- test time elapsed
- test log

"""
from __future__ import with_statement

import os
import sys
import re
import time
import datetime
import random
import subprocess
import socket
socket.setdefaulttimeout(4)
import platform
import smtplib
import binascii
import traceback
import threading
import MySQLdb
import paramiko
import cherrypy

try: import simplejson as json
except: import json

from collections import OrderedDict
from thread import allocate_lock
from thread import start_new_thread
from string import Template
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


if not sys.version.startswith('2.7'):
    print('Python version error! Central Engine must run on Python 2.7!')
    exit(1)

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print('$TWISTER_PATH environment variable is not set! Exiting!')
    exit(1)
if TWISTER_PATH not in sys.path:
    sys.path.append(TWISTER_PATH)


from common.constants  import *
from common.helpers    import *
from common.tsclogging import *
from common.xmlparser  import *
from common.suitesmanager import *
from common import iniparser

from ServiceManager   import ServiceManager
from CentralEngineWebUi import WebInterface
from ResourceAllocator  import ResourceAllocator
from ReportingServer  import ReportingServer

usrs_and_pwds = {}

#

def check_passwd(realm, user, passwd):
    """
    This function is called before ALL XML-RPC calls,
    to check the username and password.
    """
    global usrs_and_pwds
    user_passwd = binascii.hexlify(user+':'+passwd)

    if cherrypy.session.get('user_passwd') == user_passwd:
        return True
    elif user in usrs_and_pwds and usrs_and_pwds.get(user) == passwd:
        if not cherrypy.session.get('username'):
            cherrypy.session['username'] = user
        return True
    elif passwd == 'EP':
        if not cherrypy.session.get('username'):
            cherrypy.session['username'] = user
        return True

    t = paramiko.Transport(('localhost', 22))
    t.logger.setLevel(40) # Less spam, please
    t.start_client()

    # This operation is pretty heavy!!!
    try:
        t.auth_password(user, passwd)
        usrs_and_pwds[user] = passwd
        cherrypy.session['username'] = user
        cherrypy.session['user_passwd'] = user_passwd
        t.stop_thread()
        t.close()
        return True
    except:
        t.stop_thread()
        t.close()
        return False

#

def cache_users(repeat=False):
    """
    Find all system users that have Twister installer.
    """
    global TWISTER_PATH
    ti = time.time()
    logDebug('Starting to cache users...')

    lines = open('/etc/passwd').readlines()
    users = []
    for line in lines:
        path = line.split(':')[5]
        if os.path.isdir(path + '/twister/config'):
            users.append(line.split(':')[0])

    # Check if the machine has NIS users.
    # This operation CAN TAKE A LOT OF TIME!
    try:
        subprocess.check_output('nisdomainname')
        u = subprocess.check_output("ypcat passwd | awk -F : '{print $1}'", shell=True)
        for user in u.split():
            home = userHome(user)
            if os.path.isdir(home + '/twister/config'):
                users.append(user)
    except:
        pass

    # Eliminate duplicates
    users = sorted( set(users) )
    # Write the users on HDD
    with open(TWISTER_PATH + '/config/cached_users.json', 'w') as f:
        try:
            json.dump(users, f, indent=4)
        except:
            logError('Cache users operation failed! Cannot write in file `{}`!'.format(f))
            return False

    tf = time.time()
    logDebug('Cache users operation took `{:.2f}` seconds...'.format( (tf-ti) ))

    if repeat: threading.Timer(60*60, cache_users, (True,)).start()


# --------------------------------------------------------------------------------------------------
# # # #    C L A S S    P r o j e c t    # # #
# --------------------------------------------------------------------------------------------------


class Project(object):

    """
    This class controls data about:

    - users
    - EPs
    - suites
    - test files
    """

    def __init__(self):

        try:
            self.srv_ver = open(TWISTER_PATH + '/server/version.txt').read().strip()
            self.srv_ver = 'version `{}`'.format(self.srv_ver)
        except: self.srv_ver = ''

        ti = time.time()
        logDebug('STARTING TWISTER SERVER {}...'.format(self.srv_ver))

        self.manager = ServiceManager()
        self.web   = WebInterface(self)
        self.ra    = ResourceAllocator(self)
        self.report = ReportingServer(self)

        # Users, parsers, IDs...
        self.users = {}
        self.parsers = {}
        self.test_ids = {}  # IDs shortcut
        self.suite_ids = {} # IDs shortcut
        self.plugins = {}   # User plugins
        self.loggers = {}   # User loggers

        self.usr_lock = allocate_lock()  # User change lock
        self.int_lock = allocate_lock()  # Internal use lock
        self.glb_lock = allocate_lock()  # Global variables lock
        self.eml_lock = allocate_lock()  # E-mail lock
        self.db_lock  = allocate_lock()  # Database lock

        # Read the production/ development option.
        cfg_path = '{}/config/server_init.ini'.format(TWISTER_PATH)
        if not os.path.isfile(cfg_path):
            logError('Production/ Development ERROR: Cannot find server_init in path `{}`! Will default to `no_type`.'.format(cfg_path))
            self.server_init = {'ce_server_type': 'no_type'}
        else:
            cfg = iniparser.ConfigObj(cfg_path)
            self.server_init = cfg.dict()
            # Fix invalid, or inexistend type key?
            self.server_init['ce_server_type'] = self.server_init.get('ce_server_type', 'no_type').lower()
        # Fix server type spelling errors, or invalid types?
        if self.server_init['ce_server_type'] not in ['no_type', 'production', 'development']:
            logError('Production/ Development ERROR: Reset invalid server type from '\
                '`{ce_server_type}` to `no_type`!'.format(**self.server_init))
            self.server_init['ce_server_type'] = 'no_type'

        logDebug('Running server type `{ce_server_type}`.'.format(**self.server_init))

        # Panic Detect, load config for current user
        self.panicDetectConfigPath = '{}/config/PanicDetectData.json'.format(TWISTER_PATH)
        if not os.path.exists(self.panicDetectConfigPath):
            with open(self.panicDetectConfigPath, 'wb') as config:
                config.write('{}')
        with open(self.panicDetectConfigPath, 'rb') as config:
            self.panicDetectRegularExpressions = json.load(config)

        # Start cache users at the beggining...
        start_new_thread(cache_users, (False,))
        # And repeat every hour
        threading.Timer(60*60, cache_users, (True,)).start()

        logDebug('SERVER INITIALIZATION TOOK %.4f SECONDS.' % (time.time()-ti))


    def _common_proj_reset(self, user, base_config, files_config):

        # List with all EPs for this User
        epList = self.parsers[user].epnames
        if not epList:
            logCritical('Project ERROR: Cannot load the list of EPs for user `{}` !'.format(user))
            return False

        # Create EP list
        self.users[user]['eps'] = OrderedDict()

        # Generate the list of EPs in order
        for epname in epList:
            self.users[user]['eps'][epname] = OrderedDict()
            self.users[user]['eps'][epname]['status'] = STATUS_STOP
            self.users[user]['eps'][epname]['sut']    = ''
            # Each EP has a SuitesManager, helper class for managing file and suite nodes!
            self.users[user]['eps'][epname]['suites'] = SuitesManager()

        # Information about ALL project suites
        # Some master-suites might have sub-suites, but all sub-suites must run on the same EP
        suitesInfo = self.parsers[user].getAllSuitesInfo()

        # Allocate each master-suite for one EP
        for s_id, suite in suitesInfo.items():
            epname = suite['ep']
            if epname not in self.users[user]['eps']:
                continue
            self.users[user]['eps'][epname]['sut'] = suite['sut']
            self.users[user]['eps'][epname]['suites'][s_id] = suite

        # Ordered list of file IDs, used for Get Status ALL
        self.test_ids[user] = suitesInfo.getFiles()
        # Ordered list with all suite IDs, for all EPs
        self.suite_ids[user] = suitesInfo.getSuites()

        # Add framework config info to default user
        self.users[user]['config_path']  = base_config
        self.users[user]['project_path'] = files_config

        # Get project global variables from XML:
        # Path to DB, E-mail XML, Globals, `Testcase Delay` value,
        # `Exit on test Fail` value, 'Libraries', `Database Autosave` value,
        # `Pre and Post` project Scripts, `Scripts mandatory` value
        for k, v in self.parsers[user].project_globals.iteritems():
            self.users[user][k] = v

        self.users[user]['log_types'] = {}

        for logType in self.parsers[user].getLogTypes():
            self.users[user]['log_types'][logType] = self.parsers[user].getLogFileForType(logType)

        # Global params for user
        self.users[user]['global_params'] = self.parsers[user].getGlobalParams()


        # Groups and roles for current user
        self.roles = self._parseUsersAndGroups()
        if not self.roles: return False

        # The username from CherryPy connection
        cherry_usr = cherrypy.session.get('username')

        # List of roles for current CherryPy user
        cherry_roles = self.roles['users'].get(cherry_usr)

        # This user doesn't exist in users and groups
        if not cherry_roles:
            logWarning('CherryPy user `{}` cannot be found in users and roles!'.format(cherry_usr))
            return False
        # This user doesn't have any roles in users and groups
        if not cherry_roles['roles']:
            logWarning('CherryPy user `{}` doesn\'t have any roles!'.format(cherry_usr))
            return False

        self.users[user]['user_groups'] = ', '.join(cherry_roles['groups'])
        self.users[user]['user_roles']  = ', '.join(cherry_roles['roles'])

        return True


    def createUser(self, user, base_config='', files_config=''):
        """
        Create or overwrite one user.\n
        This creates a master XML parser and a list with all user variables.
        """
        if not user:
            return False

        config_data = None
        # If config path is actually XML data
        if base_config and ( type(base_config)==type('') or type(base_config)==type(u'') )\
        and ( base_config[0] == '<' and base_config[-1] == '>' ):
            config_data, base_config = base_config, ''

        user_home = userHome(user)

        # If it's a valid path
        if base_config and not os.path.exists(base_config):
            logCritical('Project ERROR: Config path {}` does not exist !'.format(base_config))
            return False
        elif not os.path.exists( '{}/twister'.format(user_home) ):
            logCritical('Project ERROR: Cannot find Twister for user `{}`, '\
                'in path `{}/twister`!'.format(user, user_home))
            return False
        else:
            base_config = '{}/twister/config/fwmconfig.xml'.format(user_home)

        if not files_config:
            files_config = '{}/twister/config/testsuites.xml'.format(user_home)

        # User data + User parser
        # Parsers contain the list of all EPs and the list of all Project Globals
        self.users[user] = OrderedDict()
        self.users[user]['status'] = STATUS_STOP

        if config_data:
            self.parsers[user] = TSCParser(user, config_data, files_config)
        else:
            self.parsers[user] = TSCParser(user, base_config, files_config)

        resp = self._common_proj_reset(user, base_config, files_config)
        if not resp: return False

        # Save everything.
        self._dump()
        logDebug('Project: Registered user `{}` ...'.format(user))

        return True


    def reset(self, user, base_config='', files_config=''):
        """
        Reset user parser, all EPs to STOP, all files to PENDING.
        """
        if not user or user not in self.users:
            logError('Project ERROR: Invalid user `{}` !'.format(user))
            return False

        if base_config and not os.path.isfile(base_config):
            logError('Project ERROR: Config path `{}` does not exist! Using default config!'.format(base_config))
            base_config = False

        r = self.changeUser(user)
        if not r: return False

        ti = time.clock()

        # User config XML files
        if not base_config:
            base_config = self.users[user]['config_path']
        if not files_config:
            files_config = self.users[user]['project_path']

        logDebug('Project: Reload configuration for user `{}`, with config files `{}` and `{}`.'
            ''.format(user, base_config, files_config))

        try: del self.parsers[user]
        except: pass
        self.parsers[user] = TSCParser(user, base_config, files_config)

        resp = self._common_proj_reset(user, base_config, files_config)
        if not resp: return False

        # Save everything.
        self._dump()
        logDebug('Project: Reload user operation took %.4f seconds.' % (time.clock()-ti))
        return True


    def renameUser(self, name, new_name):
        """
        Rename 1 user.
        """
        with self.usr_lock:

            self.users[new_name] = self.users[name]
            self.parsers[new_name] = self.parsers[name]
            self.test_ids[new_name] = self.test_ids[name]
            self.suite_ids[new_name] = self.suite_ids[name]

            del self.users[name]
            del self.parsers[name]
            del self.test_ids[name]
            del self.suite_ids[name]

        self._dump()
        logDebug('Project: Renamed user `{}` to `{}`...'.format(name, new_name))

        return True


    def deleteUser(self, user):
        """
        Delete 1 user.
        """
        with self.usr_lock:

            del self.users[user]
            del self.parsers[user]
            del self.test_ids[user]
            del self.suite_ids[user]

        self._dump()
        logDebug('Project: Deleted user `{}` ...'.format(user))

        return True


    def _checkUser(self):
        """
        Check CherryPy user. Used to quick find the roles of the current CherryPy user.
        """
        # Reload users and groups
        self.roles = self._parseUsersAndGroups()
        if not self.roles: return False

        # The username from CherryPy connection
        cherry_usr = cherrypy.session.get('username')

        # List of roles for current CherryPy user
        cherry_roles = self.roles['users'].get(cherry_usr)

        # This user doesn't exist in users and groups
        if not cherry_roles:
            # The user doesn't exist ...
            logWarning('Production Server: Username `{}` doesn\'t have any roles!'.format(cherry_usr))
            return {'roles': [], 'groups': [], 'user': cherry_usr}

        cherry_roles['user'] = cherry_usr
        return cherry_roles


    def changeUser(self, user):
        """
        Switch user hook. This function is used EVERYWHERE.\n
        This uses a lock, in order to create the user structure only once.
        If the lock is not present, on CE startup, all running EPs from one user will rush
        to create the memory structure.
        """

        with self.usr_lock:

            cherry_roles = self._checkUser()
            if not cherry_roles:
                return False

            if not user:
                return False
            if user not in self.users:
                r = self.createUser(user)
                if not r: return False

            self.users[user]['user_groups'] = ', '.join(cherry_roles['groups'])
            self.users[user]['user_roles']  = ', '.join(cherry_roles['roles'])

        return True


    def listUsers(self, active=False):
        """
        Return the cached list of users.
        """
        users = []
        with open(TWISTER_PATH + '/config/cached_users.json', 'r') as f:
            try:
                users = json.load(f)
            except:
                return users
        # Filter active users ?
        if active:
            users = [u for u in users if u in self.users]
        return users


    def _dump(self):
        """
        Internal function. Save all data structure on HDD.\n
        This function must use a lock!
        """
        with self.int_lock:

            with open(TWISTER_PATH + '/config/project_users.json', 'w') as f:
                try: json.dump(self.users, f, indent=4)
                except: pass


# # #


    def _parseUsersAndGroups(self):
        """
        Parse users and groups and return the values.
        """
        cfg_path = '{}/config/users_and_groups.ini'.format(TWISTER_PATH)

        if not os.path.isfile(cfg_path):
            logError('Users and Groups ERROR: Cannot find roles file in path `{}`!'.format(cfg_path))
            return False

        try:
            cfg = iniparser.ConfigObj(cfg_path, create_empty=True, write_empty_values=True)
        except Exception as e:
            logError('Users and Groups parsing error `{}`!'.format(e))
            return {'users': {}, 'groups': {}}

        srv_type = self.server_init['ce_server_type']
        # Type = no_type => type = development
        if srv_type == 'no_type': srv_type = 'development'

        # Cycle all groups
        for grp, grp_data in cfg['groups'].iteritems():

            roles = grp_data['roles']
            grp_data['roles']    = []

            if roles == '0':
                grp_data['roles'] = []
            elif roles == '*':
                # All roles
                grp_data['roles'] = sorted(ROLES)
            else:
                if isinstance(roles, str):
                    grp_data['roles'] += [r.strip() for r in roles.split(',') if r]
                else:
                    # It's a list
                    grp_data['roles'] += roles

        # Cycle all users
        for usr, usr_data in cfg['users'].iteritems():
            # Invalid user ?
            if 'groups_'+srv_type not in usr_data:
                continue

            usr_data['roles'] = []

            if isinstance(usr_data['groups_'+srv_type], str):
                grps = [g.strip() for g in usr_data['groups_'+srv_type].split(',') if g]
            else:
                # It's a list
                grps = usr_data['groups_'+srv_type]

            # Start adding and fixing roles for current user
            for grp in grps:
                # Invalid group ?
                if grp not in cfg['groups']:
                    continue

                roles = cfg['groups'][grp]['roles']

                if roles == '0':
                    usr_data['roles'] = []
                elif roles == '*':
                    # All roles
                    usr_data['roles'] = sorted(ROLES)
                else:
                    if isinstance(roles, str):
                        usr_data['roles'] += [r.strip() for r in roles.split(',') if r]
                    else:
                        # It's a list
                        usr_data['roles'] += roles

            # Fix roles. Must be a list.
            usr_data['roles'] = sorted( set(usr_data['roles']) )

            # Get old timeout value for user, OR create a new default value
            if not usr_data.get('timeout'):
                usr_data['timeout'] = '01'

            # Fix groups. Must be a list.
            usr_data['groups'] = grps

        return cfg.dict()


    def usersAndGroupsManager(self, cmd, name='', *args, **kwargs):
        """
        Manage users, groups and permissions.\n
        Commands:
        - list params, update param.
        - list users, list groups, list roles.
        - set user, delete user.
        - set group, delete group.
        """
        cfg_path = '{}/config/users_and_groups.ini'.format(TWISTER_PATH)
        def create_cfg():
            return iniparser.ConfigObj(cfg_path, indent_type='\t',
                create_empty=True, write_empty_values=True)

        # Reload users and groups
        with self.usr_lock:
            self.roles = self._parseUsersAndGroups()
            if not self.roles: return '*ERROR* : Invalid users and groups file!'

        # The username from CherryPy connection
        cherry_usr = cherrypy.session.get('username')
        # List of roles for current CherryPy user
        cherry_all = self.roles['users'].get(cherry_usr)

        # This user doesn't exist in users and groups
        if not cherry_all:
            # *ERROR* : Username is not defined in users & groups !
            return {}

        # List of roles for current CherryPy user
        cherry_roles = cherry_all['roles']

        srv_type = self.server_init['ce_server_type']
        # Type = no_type => type = development
        if srv_type == 'no_type': srv_type = 'development'

        if 'CHANGE_USERS' not in cherry_roles and cmd in \
            ['update param', 'set user', 'delete user', 'set group', 'delete group']:
            return '*ERROR* : Insufficient privileges to execute command `{}` !'.format(cmd)

        del cherry_all, cherry_roles

        if cmd == 'list params':
            tmp_roles = dict(self.roles)
            del tmp_roles['users']
            del tmp_roles['groups']
            return tmp_roles

        elif cmd == 'update param':
            cfg = create_cfg()
            if not name:
                return '*ERROR* : The param name cannot be empty!'
            if name in ['users', 'groups', 'roles']:
                return '*ERROR* : `users, groups and roles` are reserved names and cannot be changed!'
            try:
                cfg[name] = args[0][0]
                self.roles[name] = args[0][0]
                with self.usr_lock: cfg.write()
            except Exception, e:
                return '*ERROR* : Exception : `{}` !'.format(e)
            del cfg
            return True


        elif cmd == 'list users':
            # List all known users from users and groups config
            tmp_users = dict(self.roles['users'])
            for usr in tmp_users:
                # Delete the user key, before sending
                try: del tmp_users[usr]['key']
                except: pass
            return tmp_users

        elif cmd == 'list groups':
            # List all known groups from users and groups config
            return self.roles['groups']

        elif cmd == 'list roles':
            # List all known roles
            return sorted(ROLES)


        elif cmd == 'set user':
            # Parameters: user name and list of groups.
            cfg = create_cfg()
            if not name:
                return '*ERROR* : The user name cannot be empty!'
            # Try to check the user for NIS domains
            try:
                d = subprocess.check_output('nisdomainname', shell=True)
                if d.strip() != '(none)':
                    try:
                        subprocess.check_output('ypmatch {} passwd'.format(name), shell=True)
                    except:
                        if name not in self.listUsers(nis=False):
                            return '*ERROR* : Invalid system user `{}` !'.format(name)
            except:
                pass
            try:
                usr_group = args[0][0]
            except Exception, e:
                return '*ERROR* : Invalid group!'
            user_before = cfg['users'].get(name, {})
            try:
                usr_timeout = args[0][1]
            except Exception, e:
                # Get old timeout value for user, OR create a new default value
                usr_timeout = user_before.get('timeout', '01')

            grps = [g.strip() for g in usr_group.split(',') if g in self.roles['groups']]
            if not grps:
                return '*ERROR* : Invalid groups `{}` !'.format(usr_group)
            usr_group = ', '.join(grps)

            # Create new section in Users
            cfg['users'][name] = user_before
            cfg['users'][name]['groups_production']  = ''
            cfg['users'][name]['groups_development'] = ''
            cfg['users'][name]['groups_' + srv_type] = usr_group
            cfg['users'][name]['key']    = user_before.get('key', binascii.hexlify(os.urandom(16)))
            cfg['users'][name]['timeout'] = usr_timeout
            with self.usr_lock: cfg.write()
            logDebug('Set user `{}` in group `{}`, with timeout `{}`, in Users and Groups.'.format(name, usr_group, usr_timeout))
            del cfg

            # Reload users configuration
            with self.usr_lock:
                self.roles = self._parseUsersAndGroups()
            return True


        elif cmd == 'delete user':
            cfg = create_cfg()
            if not name:
                return '*ERROR* : The user name cannot be empty!'
            if name not in self.roles['users']:
                return '*ERROR* : Invalid user name `{}` !'.format(name)
            try:
                del cfg['users'][name]
                with self.usr_lock: cfg.write()
            except Exception, e:
                return '*ERROR* : Exception : `{}` !'.format(e)
            logDebug('Permanently removed user `{}` from Users and Groups.'.format(name))
            del cfg
            # Reload users configuration
            with self.usr_lock:
                self.roles = self._parseUsersAndGroups()
            return True


        elif cmd == 'set group':
            cfg = create_cfg()
            if not name:
                return '*ERROR* : The group name cannot be empty!'
            try:
                grp_roles = args[0][0]
            except Exception, e:
                return '*ERROR* : Exception : `{}` !'.format(e)

            # Fix permissions
            roles = [g.strip() for g in grp_roles.split(',') if g and g in ROLES]
            # Create new section in groups
            cfg['groups'][name] = {}
            cfg['groups'][name]['roles'] = ', '.join(roles)
            with self.usr_lock: cfg.write()
            logDebug('Set group `{}` with roles `{}`, in Users and Groups.'.format(name, roles))
            del cfg
            # Reload users configuration
            with self.usr_lock:
                self.roles = self._parseUsersAndGroups()
            return True

        elif cmd == 'delete group':
            cfg = create_cfg()
            if not name:
                return '*ERROR* : The group name cannot be empty!'
            if name not in self.roles['groups']:
                return '*ERROR* : Invalid group name `{}` !'.format(name)
            try:
                del cfg['groups'][name]
                with self.usr_lock: cfg.write()
            except Exception, e:
                return '*ERROR* : Exception : `{}` !'.format(e)
            logDebug('Permanently removed group `{}` from Users and Groups.'.format(name))
            del cfg
            # Reload users configuration
            with self.usr_lock:
                self.roles = self._parseUsersAndGroups()
            return True

        else:
            return '*ERROR* : Unknown command `{}` !'.format(cmd)


    def encryptText(self, text):
        """
        Encrypt a piece of text, using AES.\n
        It can use the user key, or the shared key.
        """
        # Check the username from CherryPy connection
        cherry_roles = self._checkUser()
        if not cherry_roles: return False
        key = cherry_roles.get('key')
        if not key: return False
        return encrypt(text, key)


    def decryptText(self, text):
        """
        Decrypt a piece of text, using AES.\n
        It can use the user key, or the shared key.
        """
        # Check the username from CherryPy connection
        cherry_roles = self._checkUser()
        if not cherry_roles: return False
        key = cherry_roles.get('key')
        if not key: return False
        return decrypt(text, key)


# # #


    def _getConfigPath(self, user, _config):
        """
        Helper function.
        """
        config = _config.lower()

        if config in ['', 'fwmconfig', 'baseconfig']:
            return self.users[user]['config_path']

        elif config in ['project', 'testsuites']:
            return self.users[user]['project_path']

        elif config in ['db', 'database']:
            return self.users[user]['db_config']

        elif config in ['email', 'e-mail']:
            return self.users[user]['eml_config']

        elif config in ['glob', 'globals']:
            return self.users[user]['glob_params']

        else:
            # Unchanged config
            return _config


    def listSettings(self, user, config, x_filter):
        """
        List all available settings, for 1 config of a user.
        """
        r = self.changeUser(user)
        if not r: return False
        cfg_path = self._getConfigPath(user, config)
        return self.parsers[user].listSettings(cfg_path, x_filter)


    def getSettingsValue(self, user, config, key):
        """
        Fetch a value from 1 config of a user.
        """
        r = self.changeUser(user)
        if not r: return False
        cfg_path = self._getConfigPath(user, config)
        return self.parsers[user].getSettingsValue(cfg_path, key)


    def setSettingsValue(self, user, config, key, value):
        """
        Set a value for a key in the config of a user.
        """
        r = self.changeUser(user)
        if not r: return False
        cfg_path = self._getConfigPath(user, config)
        try:
            ret = self.parsers[user].setSettingsValue(cfg_path, key, value)
            if ret: logDebug('Updated XML config `{}`, `{}` = `{}`.'.format(config, key, value))
            else: logDebug('Unable to update XML config `{}`, `{}` = `{}` !'.format(config, key, value))
        except Exception, e:
            ret = False
            logDebug('Cannot update key `{}` from XML config `{}`! Exception `{}` !'.format(key, config, e))
        return ret


    def delSettingsKey(self, user, config, key, index=0):
        """
        Del a key from the config of a user.
        """
        r = self.changeUser(user)
        if not r: return False
        cfg_path = self._getConfigPath(user, config)
        try:
            ret = self.parsers[user].delSettingsKey(cfg_path, key, index)
            if ret: logDebug('Deleted XML config `{}`, key `{}`, index `{}`.'.format(config, key, index))
            else: logDebug('Unable to delete XML config `{}`, key `{}`, index `{}` !'.format(config, key, index))
        except Exception, e:
            ret = False
            logDebug('Cannot delete key `{}` from XML config `{}`! Exception `{}` !'.format(key, config, e))
        return ret


# # #


    def getUserInfo(self, user, key=None):
        """
        Returns data for the current user, including all EP info.
        If the key is not specified, it can be a huge dictionary.
        """
        global usrs_and_pwds

        r = self.changeUser(user)
        if not r:
            if key:
                return []
            else:
                return {}

        if key == 'user_passwd':
            cherry_usr = cherrypy.session.get('username')
            # Return the password only if the connected user is the user that asks the pwd
            if user == cherry_usr:
                return usrs_and_pwds.get(user, '')
        elif key:
            return self.users[user].get(key)
        else:
            return self.users[user]


    def setUserInfo(self, user, key, value):
        """
        Create or overwrite a variable with a value, for the current user.
        """
        r = self.changeUser(user)
        if not r: return False

        if not key or key == 'eps':
            logDebug('Project: Invalid Key `{}` !'.format(key))
            return False

        self.users[user][key] = value
        self._dump()
        return True


    def getEpInfo(self, user, epname):
        """
        Retrieve all info available, about one EP.
        """
        r = self.changeUser(user)
        if not r: return {}

        return self.users[user]['eps'].get(epname, {})


    def getEpFiles(self, user, epname):
        """
        Return a list with all file IDs associated with one EP.
        The files are found recursive.
        """
        r = self.changeUser(user)
        if not r: return []

        if epname not in self.users[user]['eps']:
            logDebug('Project: Invalid EP name `{}` !'.format(epname))
            return False

        files = self.users[user]['eps'][epname]['suites'].getFiles()
        return files


    def setEpInfo(self, user, epname, key, value):
        """
        Create or overwrite a variable with a value, for one EP.
        """
        r = self.changeUser(user)
        if not r: return False

        if epname not in self.users[user]['eps']:
            logDebug('Project: Invalid EP name `{}` !'.format(epname))
            return False
        if not key or key == 'suites':
            logDebug('Project: Invalid Key `{}` !'.format(key))
            return False

        self.users[user]['eps'][epname][key] = value
        self._dump()
        return True


    def getSuiteInfo(self, user, epname, suite_id):
        """
        Retrieve all info available, about one suite.
        The files are NOT recursive.
        """
        r = self.changeUser(user)
        if not r: return {}
        eps = self.users[user]['eps']

        if epname not in eps:
            logDebug('Project: Invalid EP name `{}` !'.format(epname))
            return False
        if suite_id not in eps[epname]['suites'].getSuites():
            logDebug('Project: Invalid Suite ID `{}` !'.format(suite_id))
            return False

        suite_node = eps[epname]['suites'].findId(suite_id)
        if not suite_node:
            logDebug('Project: Invalid Suite node `{}` !'.format(suite_id))
            return False
        return suite_node


    def getSuiteFiles(self, user, epname, suite_id):
        """
        Return a list with all file IDs associated with one Suite.
        """
        r = self.changeUser(user)
        if not r: return []
        eps = self.users[user]['eps']

        if epname not in eps:
            logDebug('Project: Invalid EP name `{}` !'.format(epname))
            return False
        if suite_id not in eps[epname]['suites'].getSuites():
            logDebug('Project: Invalid Suite ID `{}` !'.format(suite_id))
            return False

        return eps[epname]['suites'].getFiles(suite_id)


    def setSuiteInfo(self, user, epname, suite_id, key, value):
        """
        Create or overwrite a variable with a value, for one Suite.
        """
        r = self.changeUser(user)
        if not r: return False
        eps = self.users[user]['eps']

        if epname not in eps:
            logDebug('Project: Invalid EP name `{}` !'.format(epname))
            return False
        if suite_id not in eps[epname]['suites'].getSuites():
            logDebug('Project: Invalid Suite ID `{}` !'.format(suite_id))
            return False
        if not key or key == 'children':
            logDebug('Project: Invalid Key `{}` !'.format(key))
            return False
        if key == 'type':
            logDebug('Project: Cannot change reserved Key `{}` !'.format(key))
            return False

        suite_node = eps[epname]['suites'].findId(suite_id)
        if not suite_node:
            logDebug('Project: Invalid Suite node `{}` !'.format(suite_id))
            return False
        suite_node[key] = value
        self._dump()
        return True


    def getFileInfo(self, user, epname, file_id):
        """
        Retrieve all info available, about one Test File.\n
        The file ID must be unique!
        """
        r = self.changeUser(user)
        if not r: return {}
        eps = self.users[user]['eps']

        if file_id not in eps[epname]['suites'].getFiles():
            logDebug('Project: Invalid File ID `{}` !'.format(file_id))
            return False

        file_node = eps[epname]['suites'].findId(file_id)
        if not file_node:
            logDebug('Project: Invalid File node `{}` !'.format(file_id))
            return False
        return file_node


    def setFileInfo(self, user, epname, file_id, key, value):
        """
        Create or overwrite a variable with a value, for one Test File.
        """
        r = self.changeUser(user)
        if not r: return False
        eps = self.users[user]['eps']

        if file_id not in eps[epname]['suites'].getFiles():
            logDebug('Project: Invalid File ID `{}` !'.format(file_id))
            return False
        if not key:
            logDebug('Project: Invalid Key `{}` !'.format(key))
            return False
        if key == 'type':
            logDebug('Project: Cannot change reserved Key `{}` !'.format(key))
            return False

        file_node = eps[epname]['suites'].findId(file_id)
        if not file_node:
            logDebug('Project: Invalid File node `{}` !'.format(file_id))
            return False
        file_node[key] = value
        self._dump()
        return True


# # #


    def setExecStatus(self, user, epname, new_status, msg=''):
        """
        Set execution status for one EP. (0, 1, 2, or 3)
        Returns a string (stopped, paused, running).
        The `message` parameter can explain why the status has changed.
        """
        # Check the username from CherryPy connection
        cherry_roles = self._checkUser()
        if not cherry_roles:
            return False
        if not 'RUN_TESTS' in cherry_roles['roles']:
            logDebug('Privileges ERROR! Username `{user}` cannot change EP status!'.format(**cherry_roles))
            return False

        if epname not in self.users[user]['eps']:
            logDebug('Project: Invalid EP name `{}` !'.format(epname))
            return False
        if new_status not in execStatus.values():
            logError('Project: Status value `{}` is not in the list of defined statuses: `{}`!'
                     ''.format(new_status, execStatus.values()) )
            return False

        # Status resume => start running
        if new_status == STATUS_RESUME:
            new_status = STATUS_RUNNING

        ret = self.setEpInfo(user, epname, 'status', new_status)
        reversed = dict((v,k) for k,v in execStatus.iteritems())

        if ret:
            if msg:
                logDebug('Project: Status changed for `{} {}` - {} (from `{}`).\n\tMessage: `{}`.'.format(
                    user, epname, reversed[new_status], cherrypy.request.headers['Remote-Addr'], msg))
            else:
                logDebug('Project: Status changed for `{} {}` - {} (from `{}`).'.format(
                    user, epname, reversed[new_status], cherrypy.request.headers['Remote-Addr']))
        else:
            logError('Project: Cannot change status for `{} {}` !'.format(user, epname))

        # Send start/ stop command to EP !
        if new_status == STATUS_RUNNING:
            self.parent.startEP(user, epname)
        elif new_status == STATUS_STOP:
            self.parent.stopEP(user, epname)

        # If all Stations are stopped, the status for current user is also stop!
        # This is important, so that in the Java GUI, the buttons will change to [Play | Stop]
        if not sum([self.getEpInfo(user, ep).get('status', 8) for ep in self.parsers[user].getActiveEps()]):

            # If User status was not Stop
            if self.getUserInfo(user, 'status'):

                self.setUserInfo(user, 'status', STATUS_STOP)

                logDebug('Project: All processes stopped for user `{}`! General status changed to STOP.\n'.format(user))

                # If this run is Not temporary
                if not (user + '_old' in self.users):
                    # On Central Engine stop, send e-mail
                    self.sendMail(user)

                    # Execute "Post Script"
                    script_post = self.getUserInfo(user, 'script_post')
                    script_mandatory = self.getUserInfo(user, 'script_mandatory')
                    save_to_db = True
                    if script_post:
                        result = execScript(script_post)
                        if result: logDebug('Post Script executed!\n"{}"\n'.format(result))
                        elif script_mandatory:
                            logError('Project: Post Script failed and script is mandatory! Will not save the results into database!')
                            save_to_db = False

                    # On Central Engine stop, save to database
                    db_auto_save = self.getUserInfo(user, 'db_auto_save')
                    if db_auto_save and save_to_db:
                        time.sleep(2) # Wait all the logs
                        self.saveToDatabase(user)

                    # Find the log process for this User and ask it to Exit
                    port = self.loggers[user]['port']
                    sock = self._logConnect(user, port)

                    if sock:
                        sock.sendall('EXIT')
                        resp = sock.recv(1024)
                        if resp == 'EXIT!':
                            sock.close()
                            logDebug('Terminated log server `localhost:{}`, for user `{}`.'.format(port, user))
                        else:
                            logWarning('Cannot stop log server `localhost:{}`, for user `{}`! Response `{}`.'.format(port, user, resp))

                    # Execute "onStop" for all plugins!
                    parser = PluginParser(user)
                    plugins = parser.getPlugins()
                    for pname in plugins:
                        plugin = self._buildPlugin(user, pname,  {'ce_stop': 'automatic'})
                        try:
                            plugin.onStop()
                        except Exception as e:
                            trace = traceback.format_exc()[33:].strip()
                            logWarning('Error on running plugin `{} onStop` - Exception: `{}`!'.format(pname, trace))
                    del parser, plugins

                    # Cycle all files to change the PENDING status to NOT_EXEC
                    eps_pointer = self.users[user]['eps']
                    statuses_changed = 0

                    # All files, for current EP
                    files = eps_pointer[epname]['suites'].getFiles()
                    for file_id in files:
                        current_status = self.getFileInfo(user, epname, file_id).get('status', -1)
                        # Change the files with PENDING status, to NOT_EXEC
                        if current_status in [STATUS_PENDING, -1]:
                            self.setFileInfo(user, epname, file_id, 'status', STATUS_NOT_EXEC)
                            statuses_changed += 1

                    if statuses_changed:
                        logDebug('Changed `{}` file statuses from Pending to Not executed.'.format(statuses_changed))

        return reversed[new_status]


    def setExecStatusAll(self, user, new_status, msg=''):
        """
        Set execution status for all EPs. (STATUS_STOP, STATUS_PAUSED, STATUS_RUNNING).
        Returns a string (stopped, paused, running).
        The `message` parameter can explain why the status has changed.
        """
        # Check the username from CherryPy connection
        cherry_roles = self._checkUser()
        if not cherry_roles:
            return False
        if not 'RUN_TESTS' in cherry_roles['roles']:
            logDebug('Privileges ERROR! Username `{user}` cannot change exec status!'.format(**cherry_roles))
            return False

        if new_status not in execStatus.values():
            logError('Project: Status value `{}` is not in the list of defined statuses: `{}`!'
                     ''.format(new_status, execStatus.values()) )
            return False

        reversed = dict((v,k) for k,v in execStatus.iteritems())

        # If this is a Temporary user
        user_agent = cherrypy.request.headers['User-Agent'].lower()
        if 'xml rpc' in user_agent and (user+'_old') in self.users:
            if msg.lower() != 'kill' and new_status != STATUS_STOP:
                return '*ERROR*! Cannot change status while running temporary!'
            else:
                # Update status for User
                self.setUserInfo(user, 'status', STATUS_STOP)

                # Update status for all active EPs
                active_eps = self.parsers[user].getActiveEps()
                for epname in active_eps:
                    if epname not in self.users[user]['eps']:
                        logError('Set Status: `{}` is not a valid EP Name!'.format(epname))
                        continue
                    self.setEpInfo(user, epname, 'status', STATUS_STOP)

                if msg:
                    logDebug("Status chang for TEMP `%s %s` -> %s. Message: `%s`.\n" % (user, active_eps, reversed[STATUS_STOP], str(msg)))
                else:
                    logDebug("Status chang for TEMP `%s %s` -> %s.\n" % (user, active_eps, reversed[STATUS_STOP]))
                return reversed[STATUS_STOP]

        # Status resume => start running. The logs must not reset on resume
        if new_status == STATUS_RESUME:
            new_status = STATUS_RUNNING

        # Return the current status, or 8 = INVALID
        executionStatus = self.getUserInfo(user, 'status') or 8

        # Re-initialize the Master XML and Reset all logs on fresh start!
        # This will always happen when the START button is pressed, if CE is stopped
        if (executionStatus == STATUS_STOP or executionStatus == STATUS_INVALID) and new_status == STATUS_RUNNING:

            # If the Msg contains 2 paths, separated by comma
            if msg and len(msg.split(',')) == 2:
                path1 = msg.split(',')[0]
                path2 = msg.split(',')[1]
                if os.path.isfile(path1) and os.path.isfile(path2):
                    logDebug('Using custom XML files: `{}` and `{}`.'.format(path1, path2))
                    self.reset(user, path1, path2)
                    msg = ''

            # Or if the Msg is a path to an existing file...
            elif msg and os.path.isfile(msg):
                data = open(msg).read().strip()
                # If the file is XML, send it to project reset function
                if data[0] == '<' and data [-1] == '>':
                    logDebug('Using custom XML file: `{}`...'.format(msg))
                    self.reset(user, msg)
                    msg = ''
                else:
                    logDebug('You are probably trying to use file `{}` as config file, but it\'s not a valid XML!'.format(msg))
                    self.reset(user)
                del data

            else:
                self.reset(user)

            self.resetLogs(user)

            # User start time and elapsed time
            self.setUserInfo(user, 'start_time', datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            self.setUserInfo(user, 'elapsed_time', 0)

            # Execute "Pre Script"
            script_pre = self.getUserInfo(user, 'script_pre')
            script_mandatory = self.getUserInfo(user, 'script_mandatory')
            if script_pre:
                result = execScript(script_pre)
                if result: logDebug('Pre Script executed! {}'.format(result))
                elif script_mandatory:
                    logError('Pre Script failed and script is mandatory! The project failed!')
                    return reversed[STATUS_STOP]

            # Execute "onStart" for all plugins!
            parser = PluginParser(user)
            plugins = parser.getPlugins()
            for pname in plugins:
                plugin = self._buildPlugin(user, pname)
                try:
                    plugin.onStart()
                except Exception as e:
                    trace = traceback.format_exc()[34:].strip()
                    logWarning('Error on running plugin `{} onStop` - Exception: `{}`!'.format(pname, trace))
            del parser, plugins

            # Start all active EPs !
            active_eps = self.parsers[user].getActiveEps()
            for epname in active_eps:
                if epname not in self.users[user]['eps']:
                    continue
                self.parent.startEP(user, epname)

        # If the engine is running, or paused and it received STOP from the user...
        elif (executionStatus == STATUS_RUNNING or executionStatus == STATUS_PAUSED) and new_status == STATUS_STOP:

            # Execute "Post Script"
            script_post = self.getUserInfo(user, 'script_post')
            script_mandatory = self.getUserInfo(user, 'script_mandatory')
            if script_post:
                result = execScript(script_post)
                if result: logDebug('Post Script executed!\n"{}"\n'.format(result))
                elif script_mandatory:
                    logError('Post Script failed!')

            # Execute "onStop" for all plugins... ?
            parser = PluginParser(user)
            plugins = parser.getPlugins()
            for pname in plugins:
                plugin = self._buildPlugin(user, pname, {'ce_stop': 'manual'})
                try:
                    plugin.onStop()
                except Exception as e:
                    trace = traceback.format_exc()[34:].strip()
                    logWarning('Error on running plugin `{} onStop` - Exception: `{}`!'.format(pname, trace))
            del parser, plugins

            # Cycle all active EPs to: STOP them and to change the PENDING status to NOT_EXEC
            active_eps = self.parsers[user].getActiveEps()
            eps_pointer = self.users[user]['eps']
            statuses_changed = 0

            for epname in active_eps:
                if epname not in self.users[user]['eps']:
                    continue
                # All files, for current EP
                files = eps_pointer[epname]['suites'].getFiles()
                for file_id in files:
                    current_status = self.getFileInfo(user, epname, file_id).get('status', -1)
                    # Change the files with PENDING status, to NOT_EXEC
                    if current_status in [STATUS_PENDING, -1]:
                        self.setFileInfo(user, epname, file_id, 'status', STATUS_NOT_EXEC)
                        statuses_changed += 1
                # Send STOP to EP Manager
                self.parent.stopEP(user, epname)

            if statuses_changed:
                logDebug('Set Status: Changed `{}` file statuses from Pending to Not executed.'.format(statuses_changed))

        # Update status for User
        self.setUserInfo(user, 'status', new_status)

        # Update status for all active EPs
        active_eps = self.parsers[user].getActiveEps()
        for epname in active_eps:
            if epname not in self.users[user]['eps']:
                logError('Set Status: `{}` is not a valid EP Name!'.format(epname))
                continue
            self.setEpInfo(user, epname, 'status', new_status)

        reversed = dict((v,k) for k,v in execStatus.iteritems())

        if msg and msg != ',':
            logDebug('Status changed for `{} {}` - {} (from `{}`).\n\tMessage: `{}`.'.format(
                user, active_eps, reversed[new_status], cherrypy.request.headers['Remote-Addr'], msg))
        else:
            logDebug('Status changed for `{} {}` - {} (from `{}`).'.format(
                user, active_eps, reversed[new_status], cherrypy.request.headers['Remote-Addr']))

        return reversed[new_status]


    def getFileStatusAll(self, user, epname=None, suite_id=None):
        """
        Return the status of all files, in order.
        This can be filtered for an EP and a Suite.
        """
        r = self.changeUser(user)
        if not r: return []

        if suite_id and not epname:
            logError('Project: Must provide both EP and Suite!')
            return []

        statuses = {} # Unordered
        final = []    # Ordered
        eps = self.users[user]['eps']

        if epname:
            if suite_id:
                files = eps[epname]['suites'].getFiles(suite_id)
            else:
                files = eps[epname]['suites'].getFiles()
            for file_id in files:
                s = self.getFileInfo(user, epname, file_id).get('status', -1)
                statuses[file_id] = str(s)
        # Default case, no EP and no Suite
        else:
            for epname in eps:
                files = eps[epname]['suites'].getFiles()
                for file_id in files:
                    s = self.getFileInfo(user, epname, file_id).get('status', -1)
                    statuses[file_id] = str(s)

        for tcid in self.test_ids[user]:
            if tcid in statuses:
                final.append(statuses[tcid])

        return final


    def setFileStatus(self, user, epname, file_id, new_status=10, time_elapsed=0.0):
        """
        Set status for one file and write in log summary.
        """
        r = self.changeUser(user)
        if not r: return False
        eps = self.users[user]['eps']

        if epname not in eps:
            logDebug('Project: Invalid EP name `{}` !'.format(epname))
            return False
        if new_status not in testStatus.values():
            logError('Project: Status value `{}` is not in the list of defined statuses: `{}`!'
                     ''.format(new_status, testStatus.values()) )
            return False

        data = self.getFileInfo(user, epname, file_id)
        if not data:
            logDebug('Project: Invalid File ID `{}` !'.format(file_id))
            return False

        filename = os.path.split(data['file'])[1]
        suite = data['suite']

        # Sets file status
        self.setFileInfo(user, epname, file_id, 'status', new_status)
        reversed = dict((v,k) for k,v in testStatus.iteritems())
        status_str = reversed[new_status]

        # Write all statuses in logs, because all files will be saved to database
        if status_str=='not executed': status_str='*NO EXEC*'
        else: status_str='*%s*' % status_str.upper()

        if new_status != STATUS_WORKING:

            # Inject information into Files. This will be used when saving into database.
            now = datetime.datetime.today()

            self.setFileInfo(user, epname, file_id, 'twister_tc_status', status_str.replace('*', ''))
            self.setFileInfo(user, epname, file_id, 'twister_tc_crash_detected',
                                    data.get('twister_tc_crash_detected', 0))
            self.setFileInfo(user, epname, file_id, 'twister_tc_time_elapsed',   int(time_elapsed))
            self.setFileInfo(user, epname, file_id, 'twister_tc_date_started',
                                    (now - datetime.timedelta(seconds=time_elapsed)).isoformat())
            self.setFileInfo(user, epname, file_id, 'twister_tc_date_finished',  (now.isoformat()))
            suite_name = self.getSuiteInfo(user, epname, suite).get('name')

            logMessage = ' {ep}::{suite}::{file} | {status} | {elapsed} | {date}\n'.format(
                    ep = epname.center(9), suite = suite_name.center(9), file = filename.center(28),
                    status = status_str.center(11),
                    elapsed = ('%.2fs' % time_elapsed).center(10),
                    date = now.strftime('%a %b %d, %H:%M:%S'))

            # Get logSummary path from framework config
            logPath = self.getUserInfo(user, 'log_types')['logSummary']
            resp = self._logServerMsg(user, logPath + ':' + logMessage)

            if not resp:
                logError('Summary log file `{}` cannot be written! User `{}` won\'t see any '\
                         'statistics!'.format(logPath, user))

        # Return string
        return status_str


    def setFileStatusAll(self, user, epname=None, new_status=10):
        """
        Reset the status of all files, to value: x.
        """
        r = self.changeUser(user)
        if not r: return False
        eps = self.users[user]['eps']

        for epcycle in eps:
            if epname and epcycle != epname:
                continue
            files = eps[epcycle]['suites'].getFiles()
            for file_id in files:
                # This uses dump, after set file info
                self.setFileInfo(user, epcycle, file_id, 'status', new_status)

        return True


# # #


    def _findGlobalVariable(self, user, node_path, globs_file=False):
        """
        Helper function.
        """
        if not globs_file:
            var_pointer = self.users[user]['global_params']
        else:
            var_pointer = self.parsers[user].getGlobalParams(globs_file)
        if not var_pointer:
            return False

        for node in node_path:
            if node in var_pointer:
                var_pointer = var_pointer[node]
            else:
                # Invalid variable path
                return False

        return var_pointer


    def getGlobalVariable(self, user, variable, globs_file=False):
        """
        Sending a global variable, using a path.
        """
        r = self.changeUser(user)
        if not r: return False

        try: node_path = [v for v in variable.split('/') if v]
        except:
            logError('Global Variable: Invalid variable type `{}`, for user `{}`!'.format(variable, user))
            return False

        var_pointer = self._findGlobalVariable(user, node_path, globs_file)

        if not var_pointer:
            logError('Global Variable: Invalid variable path `{}`, for user `{}`!'.format(node_path, user))
            return False

        return var_pointer


    def setGlobalVariable(self, user, variable, value):
        """
        Set a global variable path, for a user.\n
        The change is not persistent.
        """
        r = self.changeUser(user)
        if not r: return False

        try: node_path = [v for v in variable.split('/') if v]
        except:
            logError('Global Variable: Invalid variable type `{0}`, for user `{1}`!'.format(variable, user))
            return False

        if (not value) or (not str(value)):
            logError('Global Variable: Invalid value `{0}`, for global variable `{1}` from user `{2}`!'\
                ''.format(value, variable, user))
            return False

        # If the path is in ROOT, it's a root variable
        if len(node_path) == 1:
            with self.glb_lock:
                self.users[user]['global_params'][node_path[0]] = value
            return True

        # If the path is more complex, the pointer here will go to the parent
        var_pointer = self._findGlobalVariable(user, node_path[:-1])

        if not var_pointer:
            logError('Global Variable: Invalid variable path `{}`, for user `{}`!'.format(node_path, user))
            return False

        with self.glb_lock:
            var_pointer[node_path[-1]] = value
        return True


# # #


    def setPersistentSuite(self, user, suite, info={}, order=-1):
        """
        This function writes in TestSuites.XML file.
        """
        r = self.changeUser(user)
        if not r: return False
        cfg_path = self._getConfigPath(user, 'project')
        logDebug('Create Suite: Will create suite `{0}` for user `{1}` project.'.format(suite, user))
        return self.parsers[user].setPersistentSuite(cfg_path, suite, info, order)


    def delPersistentSuite(self, user, suite):
        """
        This function writes in TestSuites.XML file.
        """
        r = self.changeUser(user)
        if not r: return False
        xpath_suite = '/Root/TestSuite[tsName="{0}"]'.format(suite)
        logDebug('Del Suite: Will remove suite `{0}` from user `{1}` project.'.format(suite, user))
        return self.delSettingsKey(user, 'project', xpath_suite)


    def setPersistentFile(self, user, suite, fname, info={}, order=-1):
        """
        This function writes in TestSuites.XML file.
        """
        r = self.changeUser(user)
        if not r: return False
        cfg_path = self._getConfigPath(user, 'project')
        logDebug('Create File: Will create file `{0} - {1}` for user `{2}` project.'.format(suite, fname, user))
        return self.parsers[user].setPersistentFile(cfg_path, suite, fname, info, order)


    def delPersistentFile(self, user, suite, fname):
        """
        This function writes in TestSuites.XML file.
        """
        r = self.changeUser(user)
        if not r: return False
        xpath_file = '/Root/TestSuite[tsName="{0}"]/TestCase[tcName="{1}"]'.format(suite, fname)
        logDebug('Del File: Will remove file `{0} - {1}` from user `{2}` project.'.format(suite, fname, user))
        return self.delSettingsKey(user, 'project', xpath_file)


    def queueFile(self, user, suite, fname):
        """
        This function temporary adds a file at the end of the given suite, during runtime.
        """
        r = self.changeUser(user)
        if not r: return False

        if fname.startswith('~/'):
            fname = userHome(user) + fname[1:]
        if not os.path.isfile(fname):
            log = '*ERROR* No such file `{}`!'.format(fname)
            logError(log)
            return log

        # Try create a new file id
        file_id = str( int(max(self.test_ids[user] or [1000])) + 1 )

        eps = self.users[user]['eps']
        suite_id = False
        SuitesManager = False

        # Try to find the suite name
        for epname in eps:
            manager = eps[epname]['suites']
            suites = manager.getSuites()
            for s_id in suites:
                if manager.findId(s_id)['name'] == suite:
                    suite_id = s_id
                    SuitesManager = manager
                    break
            if suite_id:
                break

        if not suite_id:
            log = '*ERROR* Cannot queue file `{}`, because suite `{}` doesn\'t exist !'.format(fname, suite)
            logError(log)
            return log

        # This operation must be atomic !
        with self.usr_lock:

            # Add file in the ordered list of file IDs, used for Get Status ALL
            self.test_ids[user].append(file_id)

            finfo = OrderedDict()
            finfo['type']  = 'file'
            finfo['suite'] = suite_id
            finfo['file']  = fname
            finfo['Runnable'] = "true"

            # Add file for the user, in a specific suite
            suite = SuitesManager.findId(suite_id)
            suite['children'][file_id] = finfo

            # Add the file in suites.xml ?
            # self.setPersistentFile(self, user, suite, fname)

        self._dump()
        logDebug('File ID `{}` added at the end of suite `{}`.'.format(file_id, suite_id))
        return True


    def deQueueFiles(self, user, data):
        """
        This function temporary removes the file id from the project, during runtime.
        If the file did already run, the function does nothing!
        """
        r = self.changeUser(user)
        if not r: return False

        if not data:
            log = '*ERROR* Null EP/ Suite/ File data `{}`!'.format(data)
            logError(log)
            return log

        if ':' not in data:
            epname = data
            rest = ''
        elif data.count(':') == 1:
            epname, rest = data.split(':')
        else:
            log = '*ERROR* Invalid data `{}`! It must be EP, EP:suite_id, EP:Suite, or EP:file_id!'.format(data)
            logError(log)
            return log

        if epname not in self.users[user]['eps']:
            log = '*ERROR* Invalid EP name `{}` !'.format(epname)
            logDebug(log)
            return log

        SuitesManager = self.users[user]['eps'][epname]['suites']

        # There are 4 types of dequeue
        if not rest:
            # All files from EP
            suite_id = None
            files = SuitesManager.getFiles()

            if not files:
                log = '*ERROR* No files left to unqueue!'
                logError(log)
                return log

            logDebug('Removing file IDs `{}` from `{}`...'.format(', '.join(files), epname))

        elif len(rest) == 3:
            # All files from Suite ID
            suite_id = rest

            if suite_id not in SuitesManager.getSuites():
                log = '*ERROR* Invalid Suite ID `{}` !'.format(suite_id)
                logError(log)
                return log

            suite_node = SuitesManager.findId(suite_id)
            files = SuitesManager.getFiles(suite_id)
            logDebug('Removing file IDs `{}` from `{}:{}`...'.format(', '.join(files), epname, suite_id))

        elif len(rest) == 4:
            # A specific File ID
            file_id = rest
            suite_id = None

            if file_id not in SuitesManager.getFiles():
                log = '*ERROR* Invalid File ID `{}` !'.format(file_id)
                logError(log)
                return log

            files = [file_id]
            logDebug('Removing file ID `{}` from `{}`...'.format(file_id, epname))

        else:
            suite_id = None
            suite_node = None

            if not SuitesManager.getFiles():
                log = '*ERROR* No files left to unqueue!'
                logError(log)
                return log

            for id, node in SuitesManager.iterNodes():
                if node['type'] == 'suite' and node['name'] == rest:
                    suite_id = id
                    suite_node = node

            if not suite_id:
                log = '*ERROR* Invalid suite name `{}`!'.format(rest)
                logError(log)
                return log

            files = SuitesManager.getFiles(suite_id)
            logDebug('Removing file IDs `{}` from `{}:{}`...'.format(', '.join(files), epname, rest))


        for file_id in files:
            """
            Find the file node and delete it.
            """
            file_node = SuitesManager.findId(file_id)

            if not file_node:
                log = '*ERROR* Invalid File node `{}` !'.format(file_id)
                logError(log)
                return log

            if file_node.get('status', STATUS_PENDING) != STATUS_PENDING:
                log = '*ERROR* File ID `{}` was already executed, cannot de-queue!'.format(file_id)
                logError(log)
                return log

            if not suite_id:
                suite_id = file_node['suite']
                suite_node = SuitesManager.findId(suite_id)

            if not suite_node:
                log = '*ERROR* Invalid Suite node `{}` !'.format(suite_id)
                logError(log)
                return log

            # This operation must be atomic !
            with self.usr_lock:
                # Remove file from the ordered list of file IDs, used for Get Status ALL
                file_index = self.test_ids[user].index(file_id)
                self.test_ids[user].pop(file_index)
                # Remove file from suites
                del suite_node['children'][file_id]

        self._dump()
        return ', '.join(files)


# # #


    def sendMail(self, user, force=False):
        """
        Send e-mail function.\n
        Use the force to ignore the enabled/ disabled status.
        """
        with self.eml_lock:

            r = self.changeUser(user)
            if not r: return False

            # This is updated every time.
            eMailConfig = self.parsers[user].getEmailConfig()
            if not eMailConfig:
                log = '*ERROR* E-mail configuration not found !'
                logWarning(log)
                return log

            # Decode e-mail password
            try:
                SMTPPwd = self.decryptText(eMailConfig['SMTPPwd'])
            except:
                log = 'SMTP: Password is not set!'
                logError(log)
                return log
            if not SMTPPwd:
                log = 'SMTP: Invalid password! Please update your password and try again!'
                logError(log)
                return log
            eMailConfig['SMTPPwd'] = SMTPPwd

            if force:
                logDebug('Preparing to send a test e-mail ...')

                try:
                    server = smtplib.SMTP(eMailConfig['SMTPPath'], timeout=2)
                except:
                    log = 'SMTP: Cannot connect to SMTP server `{}`!'.format(eMailConfig['SMTPPath'])
                    logError(log)
                    return log

                try:
                    logDebug('SMTP: Preparing to login...')
                    server.ehlo()
                    server.starttls()
                    server.ehlo()

                    server.login(eMailConfig['SMTPUser'], eMailConfig['SMTPPwd'])
                except:
                    log = 'SMTP: Cannot authenticate to SMTP server! Invalid user or password!'
                    logError(log)
                    return log

                try:
                    eMailConfig['To'] = eMailConfig['To'].replace(';', ',')
                    eMailConfig['To'] = eMailConfig['To'].split(',')

                    msg = MIMEMultipart()
                    msg['From'] = eMailConfig['From']
                    msg['To'] = eMailConfig['To'][0]

                    if len(eMailConfig['To']) > 1:
                        # Carbon Copy recipients
                        msg['CC'] = ','.join(eMailConfig['To'][1:])
                    msg['Subject'] = eMailConfig['Subject']

                    msg.attach(MIMEText(eMailConfig['Message'], 'plain'))

                    server.sendmail(eMailConfig['From'], eMailConfig['To'], msg.as_string())

                    logDebug('SMTP: E-mail sent successfully!')
                    server.quit()

                    return True
                except Exception as e:
                    log = 'SMTP: Cannot send e-mail!'
                    logError(log)
                    return log

                return True

            try:
                logPath = self.users[user]['log_types']['logSummary']
                logSummary = open(logPath).read()
            except:
                log = '*ERROR* Cannot open Summary Log `{}` for reading !'.format(logPath)
                logError(log)
                return log

            if not logSummary:
                log = '*ERROR* Log Summary is empty! Nothing to send!'
                logDebug(log)
                return log

            logDebug('E-mail: Preparing... Server `{SMTPPath}`, user `{SMTPUser}`, from `{From}`, to `{To}`...'\
                ''.format(**eMailConfig))

            ce_host = socket.gethostname()
            try: ce_ip = socket.gethostbyname(ce_host)
            except: ce_ip = ''
            system = platform.machine() +' '+ platform.system() +', '+ ' '.join(platform.linux_distribution())

            # Information that will be mapped into subject or message of the e-mail
            map_info = {'date': time.strftime("%Y-%m-%d %H:%M")}

            map_info['twister_user']    = user
            map_info['twister_ce_type'] = self.server_init['ce_server_type'].lower()
            map_info['twister_server_location'] = self.server_init.get('ce_server_location', '')
            map_info['twister_rf_fname']    = '{}/config/resources.json'.format(TWISTER_PATH)
            map_info['twister_pf_fname']    = self.users[user].get('proj_xml_name', '')
            map_info['twister_ce_os']       = system
            map_info['twister_ce_hostname'] = ce_host
            map_info['twister_ce_ip']       = ce_ip
            map_info['twister_ce_python_revision'] = '.'.join([str(v) for v in sys.version_info])

            # Get all useful information, available for each EP
            for ep, ep_data in self.users[user]['eps'].iteritems():

                for k in ep_data:
                    if k in ['suites', 'status', 'last_seen_alive']: continue
                    if ep_data[k] == '': continue
                    # If the information is already in the mapping info
                    if k in map_info:
                        map_info[k] += ', ' + str(ep_data[k])
                        map_info[k] = ', '.join( sorted(set( map_info[k].split(', ') )) )
                    else:
                        map_info[k] = str(ep_data[k])

                # Get all useful information for each Suite
                for suite_id in ep_data['suites'].getSuites():
                    # All info about 1 Suite
                    suite_data = ep_data['suites'].findId(suite_id)

                    for k in suite_data:
                        if k in ['ep', 'children']: continue
                        if suite_data[k] == '': continue
                        # If the information is already in the mapping info
                        if k in map_info:
                            map_info[k] += ', ' + str(suite_data[k])
                            map_info[k] = ', '.join( sorted(set( map_info[k].split(', ') )) )
                        else:
                            map_info[k] = str(suite_data[k])

            try: del map_info['name']
            except: pass
            try: del map_info['type']
            except: pass
            try: del map_info['pd']
            except: pass

            # print 'E-mail map info::', json.dumps(map_info, indent=4, sort_keys=True)

            # Subject template string
            tmpl = Template(eMailConfig['Subject'])
            try:
                eMailConfig['Subject'] = tmpl.substitute(map_info)
            except Exception, e:
                log = 'E-mail ERROR! Cannot build e-mail subject! Error: {}!'.format(e)
                logError(log)
                return log
            del tmpl

            # Message template string
            tmpl = Template(eMailConfig['Message'])
            try:
                eMailConfig['Message'] = tmpl.substitute(map_info)
            except Exception, e:
                log = 'E-mail ERROR! Cannot build e-mail message! Error: {}!'.format(e)
                logError(log)
                return log
            del tmpl

            ROWS = []

            for line in logSummary.split('\n'):
                rows = line.replace('::', '|').split('|')
                if not rows[0]:
                    continue
                rclass = rows[3].strip().replace('*', '')

                rows = ['&nbsp;'+r.strip() for r in rows]
                ROWS.append( ('<tr class="%s"><td>' % rclass) + '</td><td>'.join(rows) + '</td></tr>\n')

            # Body string
            body_path = os.path.split(self.users[user]['config_path'])[0] +os.sep+ 'e-mail-tmpl.htm'
            if not os.path.exists(body_path):
                log = 'E-mail ERROR! Cannot find e-mail template file `{}`!'.format(body_path)
                logError(log)
                return log

            body_tmpl = Template(open(body_path).read())
            body_dict = {
                'texec':  len(logSummary.strip().splitlines()),
                'tpass':  logSummary.count('*PASS*'),
                'tfail':  logSummary.count('*FAIL*'),
                'tabort': logSummary.count('*ABORTED*'),
                'tnexec': logSummary.count('*NO EXEC*'),
                'ttimeout': logSummary.count('*TIMEOUT*'),
                'rate'  : round( (float(logSummary.count('*PASS*'))/ len(logSummary.strip().splitlines())* 100), 2),
                'table' : ''.join(ROWS),
            }

            # Fix TO and CC
            eMailConfig['To'] = eMailConfig['To'].replace(';', ',')
            eMailConfig['To'] = eMailConfig['To'].split(',')

            msg = MIMEMultipart()
            msg['From'] = eMailConfig['From']
            msg['To'] = eMailConfig['To'][0]
            if len(eMailConfig['To']) > 1:
                # Carbon Copy recipients
                msg['CC'] = ','.join(eMailConfig['To'][1:])
            msg['Subject'] = eMailConfig['Subject']

            msg.attach(MIMEText(eMailConfig['Message'], 'plain'))
            msg.attach(MIMEText(body_tmpl.substitute(body_dict), 'html'))

            if (not eMailConfig['Enabled']) or (eMailConfig['Enabled'] in ['0', 'false']):
                e_mail_path = os.path.split(self.users[user]['config_path'])[0] +os.sep+ 'e-mail.htm'
                open(e_mail_path, 'w').write(msg.as_string())
                logDebug('E-mail.htm file written. The message will NOT be sent.')
                # Update file ownership
                setFileOwner(user, e_mail_path)
                return True

            try:
                server = smtplib.SMTP(eMailConfig['SMTPPath'], timeout=2)
            except:
                log = 'SMTP: Cannot connect to SMTP server `{}`!'.format(eMailConfig['SMTPPath'])
                logError(log)
                return log

            try:
                logDebug('SMTP: Preparing to login...')
                server.ehlo()
                server.starttls()
                server.ehlo()

                server.login(eMailConfig['SMTPUser'], eMailConfig['SMTPPwd'])
            except:
                log = 'SMTP: Cannot authenticate to SMTP server! Invalid user or password!'
                logError(log)
                return log

            try:
                server.sendmail(eMailConfig['From'], eMailConfig['To'], msg.as_string())
                logDebug('SMTP: E-mail sent successfully!')
                server.quit()
                return True
            except:
                log = 'SMTP: Cannot send e-mail!'
                logError(log)
                return log


    def saveToDatabase(self, user):
        """
        Save all data from a user: Ep, Suite, File, into database,
        using the DB.XML for the current project.
        """
        with self.db_lock:

            r = self.changeUser(user)
            if not r: return False

            # Get the path to DB.XML
            db_file = self.getUserInfo(user, 'db_config')
            if not db_file:
                logError('Database: Null DB.XML file for user `{}`! Nothing to do!'.format(user))
                return False

            # Database parser, fields, queries
            # This is created every time the Save to Database is called
            db_parser = DBParser(db_file)
            db_config = db_parser.db_config
            queries = db_parser.getInsertQueries()  # List
            fields  = db_parser.getDbSelectFields() # Dictionary
            scripts = db_parser.getUserScriptFields() # List
            del db_parser

            if not queries:
                logDebug('Database: There are no queries defined for user `{}`! Nothing to do!'.format(user))
                return False

            system = platform.machine() +' '+ platform.system() +', '+ ' '.join(platform.linux_distribution())

            # Decode database password
            db_password = self.decryptText( db_config.get('password') )
            if not db_password:
                logError('Database: Cannot decrypt the database password!')
                return False

            try:
                conn = MySQLdb.connect(host=db_config.get('server'), db=db_config.get('database'),
                    user=db_config.get('user'), passwd=db_password)
                curs = conn.cursor()
            except MySQLdb.Error as e:
                logError('MySQL Error `{}`: `{}`!'.format(e.args[0], e.args[1]))
                return False

            conn.autocommit = False
            conn.begin()

            for epname, ep_info in self.users[user]['eps'].iteritems():
                SuitesManager = ep_info['suites']

                for file_id in SuitesManager.getFiles():

                    # Substitute data
                    subst_data = {'file_id': file_id}

                    # Add EP info
                    subst_data.update(ep_info)
                    del subst_data['suites']

                    # Add Suite info
                    file_info = SuitesManager.findId(file_id)
                    suite_id = file_info['suite']
                    suite_info = SuitesManager.findId(suite_id)
                    subst_data.update(suite_info)
                    del subst_data['children']

                    # Add file info
                    subst_data.update(file_info)

                    ce_host = socket.gethostname()
                    try: ce_ip = socket.gethostbyname(ce_host)
                    except: ce_ip = ''

                    # Insert/ fix DB variables
                    subst_data['twister_user']    = user
                    subst_data['twister_ce_type'] = self.server_init['ce_server_type'].lower()
                    subst_data['twister_server_location'] = self.server_init.get('ce_server_location', '')

                    subst_data['twister_rf_fname'] = '{}/config/resources.json'.format(TWISTER_PATH)
                    subst_data['twister_pf_fname'] = self.users[user].get('proj_xml_name', '')

                    subst_data['twister_ce_os']      = system
                    subst_data['twister_ce_hostname'] = ce_host
                    subst_data['twister_ce_ip']      = ce_ip
                    subst_data['twister_ce_python_revision'] = '.'.join([str(v) for v in sys.version_info])
                    subst_data['twister_ep_name']    = epname
                    subst_data['twister_suite_name'] = suite_info['name']
                    subst_data['twister_tc_full_path'] = file_info['file']
                    subst_data['twister_tc_name']  = os.path.split(subst_data['twister_tc_full_path'])[1]
                    subst_data['twister_tc_title'] = ''
                    subst_data['twister_tc_description'] = ''

                    # Escape all unicodes variables before SQL Statements!
                    subst_data = {k: conn.escape_string(v) if isinstance(v, unicode) else v for k,v in subst_data.iteritems()}

                    try:
                        subst_data['twister_tc_log'] = self.findLog(user, epname, file_id, subst_data['twister_tc_full_path'])
                        subst_data['twister_tc_log'] = conn.escape_string( subst_data['twister_tc_log'].replace('\n', '<br>\n') )
                        subst_data['twister_tc_log'] = subst_data['twister_tc_log'].replace('<div', '&lt;div')
                        subst_data['twister_tc_log'] = subst_data['twister_tc_log'].replace('</div', '&lt;/div')
                    except:
                        subst_data['twister_tc_log'] = '*no log*'

                    # Setup and Teardown files will not be saved to database!
                    if subst_data.get('setup_file') or subst_data.get('teardown_file'):
                        continue
                    # Pre-Suite or Post-Suite files will not be saved to database
                    if subst_data.get('Pre-Suite') or subst_data.get('Post-Suite'):
                        continue

                    # :: Debug ::
                    # import pprint ; pprint.pprint(subst_data)

                    # For every insert SQL statement, build correct data...
                    for query in queries:

                        # All variables of type `UserScript` must be replaced with the script result
                        try: vars_to_replace = re.findall('(\$.+?)[,\.\'"\s]', query)
                        except: vars_to_replace = []

                        for field in vars_to_replace:
                            field = field[1:]

                            # If the field is not `UserScript`, ignore it
                            if field not in scripts:
                                continue

                            # Get Script Path, or null string
                            u_script = subst_data.get(field, '')

                            # Execute script and use result
                            r = execScript(u_script)
                            if r: subst_data[field] = r
                            else: subst_data[field] = ''

                        # All variables of type `DbSelect` must be replaced with the SQL result
                        try: vars_to_replace = re.findall('(@.+?@)', query)
                        except: vars_to_replace = []

                        for field in vars_to_replace:
                            # Delete the @ character
                            u_query = fields.get(field.replace('@', ''))

                            if not u_query:
                                logError('File: `{0}`, cannot build query! Field `{1}` is not defined in the fields section!'\
                                    ''.format(subst_data['file'], field))
                                conn.rollback()
                                return False

                            # Execute User Query
                            curs.execute(u_query)
                            q_value = curs.fetchone()[0]
                            # Replace @variables@ with real Database values
                            query = query.replace(field, str(q_value))

                        # String Template
                        tmpl = Template(query)

                        # Build complete query
                        try:
                            query = tmpl.substitute(subst_data)
                        except Exception, e:
                            logError('User `{0}`, file `{1}`: Cannot build query! Error on `{2}`!'\
                                ''.format(user, subst_data['file'], str(e)))
                            conn.rollback()
                            return False

                        # :: For DEBUG ::
                        #open(TWISTER_PATH + '/config/Query.debug', 'a').write('File Query:: `{0}` ::\n{1}\n\n\n'.format(subst_data['file'], query))

                        # Execute MySQL Query!
                        try:
                            curs.execute(query)
                        except MySQLdb.Error, e:
                            logError('Error in query ``{}``'.format(query))
                            logError('MySQL Error {}: {}!'.format(e.args[0], e.args[1]))
                            conn.rollback()
                            return False

            #
            conn.commit()
            curs.close()
            conn.close()
            #

            return True


    def _buildPlugin(self, user, plugin, extra_data={}):
        """
        Parses the list of plugins and creates an instance of the requested plugin.
        All the data
        """
        # The pointer to the plug-in = User name and Plugin name
        key = user +' '+ plugin
        plug_ptr = False

        # If the plug-in was already created, re-use it
        if key in self.plugins:
            plug_ptr = self.plugins.get(key)

        parser = PluginParser(user)
        # All the info about the current plug
        pdict = parser.getPlugins().get(plugin)
        if not pdict:
            logError('Plug-ins: Cannot find plug-in name `{}`!'.format(plugin))
            return False
        del parser

        data = dict(self.getUserInfo(user))
        data.update(pdict)
        data.update(extra_data)
        data['ce'] = self
        try: del data['eps']
        except: pass
        try: del data['global_params']
        except: pass
        try: del data['status']
        except: pass
        # Delete the un-initialized plug class
        try: del data['plugin']
        except: pass

        # Initialize the plug
        if not plug_ptr:
            plugin = pdict['plugin'](user, data)
        # Update the data and re-use the old instance
        else:
            try:
                plug_ptr.data.update(data)
            except:
                plug_ptr.data = data
                logError('Plug-ins: Warning! Overwriting the `data` attr from plug-in `{}`!'.format(plugin))
            plugin = plug_ptr

        self.plugins[key] = plugin
        return plugin


# # #


    def getLogFile(self, user, read, fstart, filename):
        """
        Called in the Java GUI to show the logs.
        """
        if fstart is None:
            return '*ERROR for {}!* Parameter FSTART is NULL!'.format(user)
        if not filename:
            return '*ERROR for {}!* Parameter FILENAME is NULL!'.format(user)

        fpath = self.getUserInfo(user, 'logs_path')

        if not fpath or not os.path.exists(fpath):
            return '*ERROR for {0}!* Logs path `{1}` is invalid! Using master config `{2}` and suites config `{3}`.'\
                .format(user, fpath, self.getUserInfo(user, 'config_path'), self.getUserInfo(user, 'project_path'))

        if filename == 'server_log':
            filename = '{}/{}'.format(TWISTER_PATH, 'server_log.log')
        else:
            filename = fpath + os.sep + filename

        if not os.path.exists(filename):
            return '*ERROR for {0}!* File `{1}` does not exist! Using master config `{2}` and suites config `{3}`'.\
                format(user, filename, self.getUserInfo(user, 'config_path'), self.getUserInfo(user, 'project_path'))

        if not read or read=='0':
            return os.path.getsize(filename)

        fstart = long(fstart)
        f = open(filename)
        f.seek(fstart)
        data = f.read()
        f.close()

        return binascii.b2a_base64(data)


    def _logServer(self, user):
        """
        Launch a log server.
        """
        # Searching for a free port in the safe range...
        while 1:
            free = False
            port = random.randrange(60000, 62000)
            try:
                socket.create_connection((None, port), 1)
            except:
                free = True
            if free: break

        p_cmd = 'su {} -c "{} -u {}/server/LogServer.py {}"'.format(user, sys.executable, TWISTER_PATH, port)
        proc = subprocess.Popen(p_cmd, cwd='{}/twister'.format(userHome(user)), shell=True)
        proc.poll()

        time.sleep(0.3)
        logDebug('Log Server for user `{}` launched on `127.0.0.1:{}` - PID `{}`.'.format(user, port, proc.pid))

        self.loggers[user] = {'proc': proc, 'port': port}


    def _logConnect(self, user, port):
        """
        Create a log server connection.
        """
        for res in socket.getaddrinfo('127.0.0.1', port, socket.AF_UNSPEC, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                sock = socket.socket(af, socktype, proto)
            except socket.error as msg:
                logWarning('Sock create exception: `{}`.'.format(msg))
                sock = None
                continue
            try:
                sock.connect(sa)
            except socket.error as msg:
                logWarning('Sock connect exception: `{}`.'.format(msg))
                sock.close()
                sock = None
                continue
            break
        if sock is None:
            logError('Internal Log Error! Could not connect to Log Server!')
            return False
        else:
            return sock


    def _logServerMsg(self, user, msg):
        """
        Helper function to access the Log Server.
        """
        if user not in self.loggers:
            self._logServer(user)

        sock = self._logConnect(user, self.loggers[user]['port'])

        if not sock:
            logError('Creating a new connection...')
            self._logServer(user)
            sock = self._logConnect(user, self.loggers[user]['port'])
            if not sock:
                return False

        def send(sock, msg):
            sock.sendall(msg)
            r = sock.recv(1024)
            return r

        resp = ''

        if ':' in msg:
            logFile, logMsg = msg.split(':')[0], ':'.join( msg.split(':')[1:] )
            lmsg = 2 ** 12
            lead = len(logFile)
            ind  = 0
            while 1:
                i1 = ind
                i2 = i1 + lmsg - lead - 1
                if i2 <= 0: i2 = -1
                if not logMsg[i1:i2]:
                    break
                msg = logFile +':'+ logMsg[i1:i2]
                resp = send(sock, msg)
                ind = i2
        else:
            resp = send(sock, msg)

        sock.close()

        if resp == 'Ok!':
            return True
        else:
            return False


    def logMessage(self, user, logType, logMessage):
        """
        This function is exposed in all tests, all logs are centralized in the HOME of the user.\n
        In order for the user to be able to access the logs written by CE, which runs as ROOT,
        CE will start a small process in the name of the user and the process will write the logs.
        """
        if os.getuid():
            logError('Log Error! Central Engine must run as ROOT in order to start the Log Server!')
            return False

        logType = str(logType)
        logTypes = self.getUserInfo(user, 'log_types')

        if logType not in logTypes:
            logError('Log Error! Log type `{}` is not in the list of defined types: `{}`!'.format(logType, logTypes))
            return False

        if logType == 'logSummary':
            logWarning('Log Warning! logSummary is reserved and cannot be written into!')
            return False

        logPath = self.getUserInfo(user, 'log_types')[logType]

        return self._logServerMsg(user, logPath + ':' + logMessage)


    def logLIVE(self, user, epname, logMessage):
        """
        Writes CLI messages in a big log, so all output can be checked LIVE.\n
        Called from the EP.
        """
        if os.getuid():
            logError('Log Error! Central Engine must run as ROOT in order to start the Log Server!')
            return False

        logFolder = self.getUserInfo(user, 'logs_path')

        if not logFolder:
            logError('Log Error! Invalid logs folder `{}`!'.format(logFolder))
            return False

        try:
            log_string = binascii.a2b_base64(logMessage)
        except:
            logError('Live Log Error: Invalid base64 log!')
            return False

        # Execute "onLog" for all plugins
        plugins = PluginParser(user).getPlugins()
        for pname in plugins:
            plugin = self._buildPlugin(user, pname, {'log_type': 'cli'})
            try:
                plugin.onLog(epname, log_string)
            except Exception as e:
                trace = traceback.format_exc()[34:].strip()
                logWarning('Error on running plugin `{} onStop` - Exception: `{}`!'.format(pname, trace))
        del plugins

        # Calling Panic Detect
        pd = self._panicDetectLogParse(user, epname, log_string)

        logTypes = self.getUserInfo(user, 'log_types')
        _, logCli = os.path.split( logTypes.get('logCli', 'CLI.log') )
        # Logs Path + EP Name + CLI Name
        logPath = logFolder + os.sep + epname +'_'+ logCli

        if pd:
            self.logMessage(user, 'logRunning', 'PANIC DETECT: Execution stopped.')

        return self._logServerMsg(user, logPath + ':' + log_string)


    def resetLog(self, user, logName):
        """
        Resets one log.\n
        Called from the Java GUI.
        """
        logTypes = self.getUserInfo(user, 'log_types')
        logPath = ''

        # Cycle all log types and paths
        for logType, logN in logTypes.iteritems():
            _, logShort = os.path.split(logN)
            # CLI Logs are special, exploded for each EP
            if logType.lower() == 'logcli':
                for epname in self.getUserInfo(user, 'eps'):
                    logCli = epname +'_'+ logShort
                    if logName == logCli:
                        logPath = _ +'/'+ logCli
                        break
            else:
                # For normal, non-CLI logs...
                if logName == logShort:
                    logPath = logN
                    break

        if not logPath:
            logError('Log Error! Log name `{}` cannot be found!'.format(logName))
            return False

        data = json.dumps({
            'cmd': 'del',
            'logPath': logPath,
            })

        ret = self._logServerMsg(user, data)
        if ret:
            logDebug('Cleaned log `{}`.'.format(logPath))
        return ret


    def resetLogs(self, user):
        """
        All logs defined in master config are erased.\n
        Called from the Java GUI and every time the project is reset.
        """
        logsPath = self.getUserInfo(user, 'logs_path')
        logTypes = self.getUserInfo(user, 'log_types')

        # Archive logs
        archiveLogsPath   = self.getUserInfo(user, 'archive_logs_path')
        archiveLogsActive = self.getUserInfo(user, 'archive_logs_path_active')

        data = json.dumps({
            'cmd': 'reset',
            'logsPath': logsPath,
            'logTypes': logTypes,
            'archiveLogsActive': archiveLogsActive,
            'archiveLogsPath': archiveLogsPath,
            'epnames': ','.join( self.getUserInfo(user, 'eps').keys() ),
            })

        ret = self._logServerMsg(user, data)
        if ret:
            logDebug('Logs reset.')
        return ret


    def findLog(self, user, epname, file_id, file_name):
        '''
        Parses the log file of one EP and returns the log of one test file.
        '''
        logFolder = self.getUserInfo(user, 'logs_path')
        logTypes  = self.getUserInfo(user, 'log_types')
        _, logCli = os.path.split( logTypes.get('logCli', 'CLI.log') )
        # Logs Path + EP Name + CLI Name
        logPath = logFolder + os.sep + epname +'_'+ logCli

        try:
            data = open(logPath, 'r').read()
        except:
            logError('Find Log: File `{}` cannot be read!'.format(logPath))
            return '*no log*'

        fbegin = data.find('<<< START filename: `{}:{}'.format(file_id, file_name))
        if fbegin == -1:
            logDebug('Find Log: Cannot find `{}:{}` in log `{}`!'.format(file_id, file_name, logPath))

        fend = data.find('<<< END filename: `{}:{}'.format(file_id, file_name))
        fend += len('<<< END filename: `{}:{}` >>>'.format(file_id, file_name))

        return data[fbegin:fend]


    def _panicDetectLogParse(self, user, epname, log_string):
        """
        Panic Detect parse log mechanism.
        """
        status = False
        self.panicDetectConfig(user, {'command': 'list'})

        if not self.panicDetectRegularExpressions.has_key(user):
            return status

        # Verify if for current suite Panic Detect is enabled
        suiteID = self.getEpInfo(user, epname).get('curent_suite')
        # When running first, the current_suite is not defined yet
        if not suiteID:
            return status

        enabled = self.getSuiteInfo(user, epname, suiteID).get('pd')

        if not enabled or enabled.lower() == 'false':
            return status

        for key, value in self.panicDetectRegularExpressions[user].iteritems():
            if value.get('enabled') == 'true':
                try:
                    if re.search(value['expression'], log_string):
                        # Stop EP
                        self.setExecStatus(user, epname, STATUS_STOP,
                            msg='Panic detect activated, expression `{}` found in CLI log!'.format(value['expression']))
                        status = True
                except Exception as e:
                    trace = traceback.format_exc()[34:].strip()
                    logError(trace)

        return status


    def panicDetectConfig(self, user, args):
        """ Panic Detect mechanism.
        Valid commands: list, add, update, remove regular expression;

        list command: args = {'command': 'list'}
        add command: args = {'command': 'add', 'data': {'expression': 'reg_exp_string'}}
        update command: args = {'command': 'update', 'data': {'id': 'reg_exp_id',
                                    expression': 'reg_exp_modified_string'}}
        remove command:  args = {'command': 'remove', 'data': 'reg_exp_id'}
        """

        panicDetectCommands = {
            'simple': [
                'list',
            ],
            'argumented': [
                'add', 'update', 'remove',
            ]
        }

        # response structure
        response = {
            'status': {
                'success': True,
                'message': 'None', # error message
            },
            'type': 'reply', # reply type
            'data': 'None', # response data
        }

        if (not args.has_key('command') or args['command'] not
            in panicDetectCommands['argumented'] + panicDetectCommands['simple']):
            response['type'] = 'error reply'

            response['status']['success'] = False
            response['status']['message'] = 'unknown command'

        elif (args['command'] in panicDetectCommands['argumented']
                and not args.has_key('data')):
            response['type'] = 'error reply'

            response['status']['success'] = False
            response['status']['message'] = 'no command data specified'


        # list_regular_expresions
        elif args['command'] == 'list':
            response['type'] = 'list_regular_expressions reply'

            #response['data'] = json.dumps(self.panicDetectRegularExpressions)
            response = json.dumps(self.panicDetectRegularExpressions)


        # add_regular_expression
        elif args['command'] == 'add':
            response['type'] = 'add_regular_expression reply'

            try:
                _args = args['data']
                regExpData = {}

                regExpData.update([('expression', _args['expression']), ])

                if regExpData.has_key('enabled'):
                    regExpData.update([('enabled', _args['enabled']), ])
                else:
                    regExpData.update([('enabled', False), ])

                regExpID = str(time.time()).replace('.', '|')

                if not self.panicDetectRegularExpressions.has_key(user):
                    self.panicDetectRegularExpressions.update([(user, {}), ])

                self.panicDetectRegularExpressions[user].update(
                                                    [(regExpID, regExpData), ])

                with self.int_lock:
                    config = open(self.panicDetectConfigPath, 'wb')
                    json.dump(self.panicDetectRegularExpressions, config)
                    config.close()

                #response['data'] = regExpID
                response = regExpID
                logDebug('Panic Detect: added regular expression `{e}` for user: `{u}`.'.format(u=user, e=regExpID))
            except Exception, e:
                #response['status']['success'] = False
                #response['status']['message'] = '{er}'.format(er=e)
                response = 'error: {er}'.format(er=e)


        # update_regular_expression
        elif args['command'] == 'update':
            response['type'] = 'update_regular_expression reply'

            try:
                _args = args['data']
                regExpID = _args.pop('id')
                regExpData = self.panicDetectRegularExpressions[user].pop(regExpID)

                regExpData.update([('expression', _args['expression']), ])

                if _args.has_key('enabled'):
                    regExpData.update([('enabled', _args['enabled']), ])
                else:
                    regExpData.update([('enabled', regExpData['enabled']), ])

                self.panicDetectRegularExpressions[user].update(
                                                    [(regExpID, regExpData), ])
                with self.int_lock:
                    config = open(self.panicDetectConfigPath, 'wb')
                    json.dump(self.panicDetectRegularExpressions, config)
                    config.close()

                #response['data'] = regExpID
                response = True
                logDebug('Panic Detect: updated regular expression `{e}` for user: `{u}`.'.format(u=user, e=regExpID))
            except Exception, e:
                #response['status']['success'] = False
                #response['status']['message'] = '{er}'.format(er=e)
                response = 'error: {er}'.format(er=e)


        # remove_regular_expression
        elif args['command'] == 'remove':
            response['type'] = 'remove_regular_expression reply'

            try:
                regExpID = args['data']
                regExpData = self.panicDetectRegularExpressions[user].pop(regExpID)
                del(regExpData)

                with self.int_lock:
                    config = open(self.panicDetectConfigPath, 'wb')
                    json.dump(self.panicDetectRegularExpressions, config)
                    config.close()

                #response['data'] = regExpID
                response = True
                logDebug('Panic Detect: removed regular expresion `{e}` for user: `{u}`.'.format(u=user, e=regExpID))
            except Exception, e:
                #response['status']['success'] = False
                #response['status']['message'] = '{er}'.format(er=e)
                response = 'error: {er}'.format(er=e)

        return response


# Eof()
