
# File: CeDatabase.py ; This file is part of Twister.

# version: 3.008

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
Central Engine Database manager
*******************************

This module is responsible with managing connections, read and write in the database.
"""

import os
import re
import sys
import time
import socket
import platform
import subprocess
import MySQLdb
from string import Template
from thread import allocate_lock

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print('TWISTER_PATH environment variable is not set! Exiting!')
    exit(1)
if TWISTER_PATH not in sys.path:
    sys.path.append(TWISTER_PATH)

from common.xmlparser import DBParser
from common.helpers import execScript
from common.tsclogging import logDebug, logInfo, logWarning, logError



class CeDbManager(object):
    """
    Central Engine database manager class.
    """

    project = None   # Pointer to Project instance
    connections = {} # Saved connections
    db_lock = allocate_lock() # Global database lock


    def __init__(self, project):
        """
        Initialize database manager.
        """
        self.project = project


    def connect_db(self, user, db_server='', db_name=''):
        """
        Connect to database.
        """
        # Get the path to DB.XML
        db_file = self.project.get_user_info(user, 'db_config')
        if not db_file:
            logError('Database: Null DB.XML file for user `{}`! Cannot connect!'.format(user))
            return False

        c_time = time.time()
        usr_server = '{}_{}_{}'.format(user, db_server, db_name)

        # Existing connection ?
        if self.connections.get(usr_server):
            # This is a very fresh connection !
            if c_time - self.connections[usr_server]['dt'] < 1.0:
                return self.connections[usr_server]['conn']

        # DB.xml + Shared DB parser
        users_groups = self.project._parse_users_and_groups()
        shared_db_path = users_groups['shared_db_cfg']
        if os.path.isfile(shared_db_path):
            db_config = DBParser(user, db_file, shared_db_path).db_config
        else:
            db_config = DBParser(user, db_file).db_config

        # Try to use the default pair
        if not db_server and not db_name:
            db_server, db_name = db_config['default_server']

        # Check server + DB pair
        if (db_server, db_name) not in db_config['servers']:
            logWarning('Database: Invalid server + DB pair {} for user `{}`! '\
                'Cannot connect!'.format((db_server, db_name), user))
            return False

        db_user = db_config['servers'][(db_server, db_name)]['u']
        db_passwd = db_config['servers'][(db_server, db_name)]['p']
        # Need to magically identify the correct key; the first pair is from private DB.xml;
        if (db_server, db_name) == db_config['servers'].keys()[0]:
            encr_key = None
        else:
            encr_key = users_groups.get('shared_db_key', 'Luxoft')
        # Decode database password
        db_password = self.project.decrypt_text(user, db_passwd, encr_key)

        try:
            logDebug('User `{}` connecting to MySQL `{} @ {} / {}`...'.format(user, db_user, db_server, db_name))
            conn = MySQLdb.connect(host=db_server, db=db_name, user=db_user, passwd=db_password)
            conn.autocommit = False
        except MySQLdb.Error as e:
            logError('MySQL error for user `{}`: `{} - {}`!'.format(user, e.args[0], e.args[1]))
            return False

        # Keep connection
        self.connections[usr_server] = {'conn': conn, 'dt': c_time}

        return conn


    def static_project_data(self, user):
        """
        Collect all files data, for a user.
        """
        # Central Engine variables ...
        system = platform.machine() + ' ' + platform.system() + ', ' + \
             ' '.join(platform.linux_distribution())

        # Timezone. Read from etc/timezone 1st, etc/sysconfig/clock 2nd, or from Time module
        try:
            timezone = open('/etc/timezone').read().strip()
        except Exception:
            try:
                timezone = subprocess.check_output('cat /etc/sysconfig/clock | grep ^ZONE=',
                    shell=True)
                timezone = timezone.strip().replace('"', '').replace('ZONE=', '')
            except Exception:
                timezone = time.strftime('%Z')

        ce_host = socket.gethostname()
        try:
            ce_ip = socket.gethostbyname(ce_host)
        except Exception:
            ce_ip = ''

        # Default substitute dict
        default_subst = {}
        default_subst['twister_user'] = user
        default_subst['twister_ce_type'] = self.project.server_init['ce_server_type'].lower()
        default_subst['twister_server_location'] = self.project.server_init.get('ce_server_location', '')

        default_subst['twister_rf_fname'] = '{}/config/resources.json'.format(TWISTER_PATH)
        default_subst['twister_pf_fname'] = self.project.users[user].get('proj_xml_name', '')

        default_subst['twister_ce_os'] = system
        default_subst['twister_ce_timezone'] = timezone
        default_subst['twister_ce_hostname'] = ce_host
        default_subst['twister_ce_ip'] = ce_ip
        default_subst['twister_ce_python_revision'] = '.'.join([str(v) for v in sys.version_info])

        def fix_log(tc_log):
            tc_log = tc_log.replace('\n', '<br>\n')
            tc_log = conn.escape_string(tc_log)
            tc_log = tc_log.replace('<div', '&lt;div')
            tc_log = tc_log.replace('</div', '&lt;/div')
            return tc_log

        # Pre-calculated data
        all_data = []

        for epname, ep_info in self.project.users[user]['eps'].iteritems():
            # If the suites key is not found continue to the next
            if ep_info.get('suites') is None:
                continue

            SuitesManager = ep_info['suites']

            for file_id in SuitesManager.get_files():

                # Default substitute data
                subst_data = dict(default_subst)
                # Add EP info
                subst_data.update(ep_info)
                del subst_data['suites']

                # Add Suite info
                file_info = SuitesManager.find_id(file_id)
                suite_id = file_info['suite']
                suite_info = SuitesManager.find_id(suite_id)

                # This is the root suite data
                root_suite = dict(suite_info)

                while 1:
                    root_suite_id = root_suite['suite']
                    root_suite = SuitesManager.find_id(root_suite_id)
                    if not root_suite:
                        root_suite = {}
                        break
                    if not root_suite['suite']:
                        break

                # Add root suite data
                subst_data.update(root_suite)
                # Add current suite data
                subst_data.update(suite_info)
                del subst_data['children']

                # Add file info
                subst_data.update(file_info)

                # Setup and Teardown files will not be saved to database!
                if subst_data.get('setup_file') or subst_data.get('teardown_file'):
                    continue
                # Pre-Suite or Post-Suite files will not be saved to database
                if subst_data.get('Pre-Suite') or subst_data.get('Post-Suite'):
                    continue

                # Insert/ fix DB variables
                subst_data['twister_ep_name'] = epname
                subst_data['twister_suite_id'] = suite_id
                subst_data['twister_suite_name'] = suite_info['name']
                subst_data['twister_tc_reason'] = file_info.get('_reason', '')
                subst_data['twister_tc_iteration'] = file_info.get('iterationNr', '')
                subst_data['twister_tc_full_path'] = file_info['file']
                subst_data['twister_tc_name'] = os.path.split(file_info['file'])[1]
                subst_data['twister_tc_id'] = file_id
                # subst_data['twister_tc_title'] = ''
                # subst_data['twister_tc_description'] = ''

                # Delete obsolete keys
                try:
                    del subst_data['name']
                except Exception:
                    pass
                try:
                    del subst_data['status']
                except Exception:
                    pass
                try:
                    del subst_data['type']
                except Exception:
                    pass
                try:
                    del subst_data['pd']
                except Exception:
                    pass

                # Log CLI for this EP - Suite - Test
                try:
                    tc_log = self.project.find_log(user, ltype='logCli', epname=epname,
                       file_id=file_id, file_name=file_info['file'])
                    subst_data['twister_tc_log'] = fix_log(tc_log)
                except Exception:
                    subst_data['twister_tc_log'] = '*no log*'

                # The rest of the logs
                try:
                    tc_log = self.project.find_log(user, ltype='logRunning', epname=epname,
                        file_id=file_id, file_name=file_info['file'])
                    subst_data['twister_tc_log_running'] = fix_log(tc_log)
                except Exception:
                    subst_data['twister_tc_log_running'] = '*no log*'

                try:
                    tc_log = self.project.find_log(user, ltype='logDebug', epname=epname,
                        file_id=file_id, file_name=file_info['file'])
                    subst_data['twister_tc_log_debug'] = fix_log(tc_log)
                except Exception:
                    subst_data['twister_tc_log_debug'] = '*no log*'

                try:
                    tc_log = self.project.find_log(user, ltype='logTest', epname=epname,
                        file_id=file_id, file_name=file_info['file'])
                    subst_data['twister_tc_log_test'] = fix_log(tc_log)
                except Exception:
                    subst_data['twister_tc_log_test'] = '*no log*'

                # :: Debug ::
                import pprint ; pprint.pprint(subst_data)

                # Append all data for current file
                all_data.append(subst_data)

        all_data = sorted(all_data, key=lambda file_info: file_info['twister_tc_id'])

        return all_data


    def project_data(self, user, save_to_db=False):
        """
        Collect all data from a user, using the DB.XML for the current project.
        If save to DB is active, the function will also save.
        """
        # Get the path to DB.XML
        db_file = self.project.get_user_info(user, 'db_config')
        if not db_file:
            logError('Database: Null DB.XML file for user `{}`! Nothing to do!'.format(user))
            return False

        usr_roles = self.project._parse_users_and_groups()
        shared_db_path = usr_roles['shared_db_cfg']
        db_cfg_role = 'CHANGE_DB_CFG' in usr_roles['users'][user]['roles']
        # Get inserts will automatically handle private/ shared DB.xml
        all_inserts = DBParser(user, db_file, shared_db_path).get_inserts(db_cfg_role)

        if not all_inserts:
            logWarning('Database: Cannot use inserts defined for user `{}`!'.format(user))
            return False

        # UserScript cache
        usr_script_cache_s = {} # Suite
        usr_script_cache_p = {} # Project

        # DbSelect cache
        db_select_cache_s = {} # Suite
        db_select_cache_p = {} # Project

        conn, curs = None, None

        # Pre-calculated data
        all_data = []

        for subst_data in self.static_project_data(user):

            # For every host, build correct data...
            for host_db in all_inserts:

                c_inserts = all_inserts[host_db]['inserts']
                c_fields = all_inserts[host_db]['fields']

                conn = self.connect_db(user, *host_db)
                if not conn:
                    continue
                curs = conn.cursor()

                # Escape all unicodes variables before SQL Statements!
                subst_data = {k: conn.escape_string(v) if isinstance(v, unicode) else v for \
                    k, v in subst_data.iteritems()}

                # For every query of the current host
                for query in c_inserts:

                    # All variables of type `UserScript` must be replaced with the script result
                    try:
                        user_script_fields = re.findall('(\$.+?)[,\.\'"\s]', query)
                    except Exception:
                        user_script_fields = []

                    for field in user_script_fields:
                        field = field[1:]

                        # Invalid field ?
                        if field not in c_fields:
                            continue

                        # If the field is not `UserScript`, ignore it
                        if c_fields.get(field, {}).get('type') != 'UserScript':
                            continue

                        # Field level: Suite or Project
                        lvl = c_fields.get(field)['level']

                        # Get Script Path, or null string
                        u_script = subst_data.get(field, '')

                        if not u_script:
                            query = query.replace('$'+field, '')
                            continue

                        # Execute this script based on level
                        if lvl == 'Project':
                            if u_script not in usr_script_cache_p:
                                # Execute script and use result
                                r = execScript(u_script)
                                # logDebug('Database: UserScript for `{}` was executed at '\
                                #     'LVL `{}`.'.format(user, lvl))
                                # Save result in cache
                                usr_script_cache_p[u_script] = r
                            else:
                                # Get script result from cache
                                r = usr_script_cache_p[u_script]
                        # Execute for every suite
                        else:
                            suite_id = subst_data['twister_suite_id']
                            if suite_id not in usr_script_cache_s:
                                usr_script_cache_s[suite_id] = {}
                            if u_script not in usr_script_cache_s[suite_id]:
                                # Execute script and use result
                                r = execScript(u_script)
                                # logDebug('Database: UserScript for `{}` was executed at '\
                                #     'LVL `{}`.'.format(user, lvl))
                                # Save result in cache
                                usr_script_cache_s[suite_id][u_script] = r
                            else:
                                # Get script result from cache
                                r = usr_script_cache_s[suite_id][u_script]

                        # Replace UserScript with with real Script results
                        if not r:
                            r = ''
                        query = query.replace('$'+field, r)

                        # Adding user script fields
                        subst_data[field] = r

                    # All variables of type `DbSelect` must be replaced with the SQL result
                    try:
                        auto_insert_fields = re.findall('(@.+?@)', query)
                    except Exception:
                        auto_insert_fields = []

                    for field in auto_insert_fields:
                        # Delete the @ character
                        field = field[1:-1]

                        # Invalid field ?
                        if field not in c_fields:
                            continue

                        # Get Auto Query, or null string
                        u_query = c_fields.get(field, {}).get('query', '')

                        # Field level: Suite, Project, or Testcase
                        lvl = c_fields.get(field)['level']

                        if not u_query:
                            logError('User `{}`, file `{}`: Cannot build query! Field `{}` '\
                                'is not defined in the fields section!'.format(user, subst_data['file'], field))
                            return False

                        # Execute User Query based on level
                        if lvl == 'Project':
                            if u_query not in db_select_cache_p:
                                # Execute User Query
                                curs.execute(u_query)
                                q_value = curs.fetchone()[0]
                                # logDebug('Database: DbSelect for `{}` was executed at '\
                                #     'LVL `{}`.'.format(user, lvl))
                                # Save result in cache
                                db_select_cache_p[u_query] = q_value
                            else:
                                # Get script result from cache
                                q_value = db_select_cache_p[u_query]
                        # Execute User Query for every suite
                        elif lvl == 'Suite':
                            suite_id = subst_data['twister_suite_id']
                            if suite_id not in db_select_cache_s:
                                db_select_cache_s[suite_id] = {}
                            if u_query not in db_select_cache_s[suite_id]:
                                # Execute User Query
                                curs.execute(u_query)
                                q_value = curs.fetchone()[0]
                                # logDebug('Database: DbSelect for `{}` was executed at '\
                                #     'LVL `{}`.'.format(user, lvl))
                                # Save result in cache
                                db_select_cache_s[suite_id][u_query] = q_value
                            else:
                                # Get script result from cache
                                q_value = db_select_cache_s[suite_id][u_query]
                        else:
                            # Execute User Query
                            curs.execute(u_query)
                            q_value = curs.fetchone()[0]
                            # logDebug('Database: DbSelect for `{}` was executed at '\
                            #     'LVL `TestCase`.'.format(user))

                        # Replace @variables@ with real Database values
                        query = query.replace('@'+field+'@', str(q_value))
                        # Adding auto insert fields
                        subst_data[field] = str(q_value)

                    # String Template
                    tmpl = Template(query)

                    # Build complete query
                    try:
                        query = tmpl.substitute(subst_data)
                    except Exception as e:
                        logError('User `{}`, file `{}`: Cannot build query! '\
                            'Error on `{}`!'.format(user, subst_data['file'], e))
                        return False

                    # Save query in database ?
                    if save_to_db:
                        # Execute MySQL Query!
                        try:
                            curs.execute(query)
                            logDebug('Executed query\n\t``{}``\n\t on {} OK.'.format(query.strip(), host_db))
                            conn.commit()
                        except MySQLdb.Error as e:
                            logError('Error in query ``{}`` , for user `{}`!\n\t'\
                                'MySQL Error {}: {}!'.format(query, user, e.args[0], e.args[1]))
                            conn.rollback()
                            return False

            # :: Debug ::
            # import pprint ; pprint.pprint(subst_data)

            # Append all data for current file
            all_data.append(subst_data)

        return all_data


    def save_to_database(self, user):
        """
        Save all data from a user: Ep, Suite, File, into database,
        using the DB.XML files for the current project.
        """
        with self.db_lock:
            return self.project_data(user, True)


# Eof()
