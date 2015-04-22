
# File: CeXmlRpc.py ; This file is part of Twister.

# version: 3.019

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
Central Engine Xml-RPC
**********************

All functions from Central Engine are EXPOSED and can be accesed via XML-RPC.\n
The Central Engine and each EP have a status that can be: start/ stop/ paused.\n
Each test file has a status that can be: pending, working, pass, fail, skip, etc.\n
All the statuses are defined in "constants.py".\n
Central Engine role is to send files and libraries to User EPs, collect statistics and logs from
each file executed, send e-mail and save to database after each Project execution, run plug-ins.
"""
from __future__ import with_statement

import os
import sys
import re
import copy
import time
import datetime
import traceback
import socket
socket.setdefaulttimeout(5)
import binascii
import pickle
import tarfile
import xmlrpclib
import urlparse
import MySQLdb

import cherrypy
from cherrypy import _cptools

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



class CeXmlRpc(_cptools.XMLRPCController):

    """
    *This class is the core of all operations.*
    """

    def __init__(self, proj):

        self.project = proj


    @cherrypy.expose
    def default(self, *vpath, **params):
        """ defaultconnection """
        user_agent = cherrypy.request.headers['User-Agent'].lower()
        if 'xmlrpc' in user_agent or 'xml rpc' in user_agent:
            resp = super(CeXmlRpc, self).default(*vpath, **params)
            if resp is None:
                return False
            return resp
        # If the connection is not XML-RPC, redirect to REST
        raise cherrypy.HTTPRedirect('/web/' + '/'.join(vpath))


# --------------------------------------------------------------------------------------------------
#           H E L P E R   F U N C T I O N S
# --------------------------------------------------------------------------------------------------


    @cherrypy.expose
    def echo(self, msg):
        """
        Simple echo function, for testing connection.
        """
        if msg != 'ping':
            logInfo(':: %s' % str(msg))
        return 'CE reply: ' + msg


    @cherrypy.expose
    def get_twister_path(self):
        '''
        Returns the Twister Path.
        '''
        global TWISTER_PATH
        return TWISTER_PATH


    @cherrypy.expose
    def get_rpyc_port(self):
        '''
        Returns the Twister RPyc Port.
        '''
        return self.project.rsrv.port


    @cherrypy.expose
    def get_sys_info(self):
        '''
        Returns some system information.
        '''
        return systemInfo()


    @cherrypy.expose
    def get_user_home(self):
        '''
        Returns some system information.
        '''
        user = cherrypy.session.get('username')
        return userHome(user)


    @cherrypy.expose
    def get_logs_path(self, user):
        '''
        Returns the path to Logs files.
        '''
        return self.project.get_user_info(user, 'logs_path')


    @cherrypy.expose
    def encrypt_text(self, text):
        """
        Encrypt a piece of text, using AES.\n
        This function is called from the Java GUI.
        """
        logFull('CeXmlRpc:encrypt_text')
        if not text:
            return ''
        cherry_user = cherrypy.session.get('username')
        return self.project.encrypt_text(cherry_user, text)


    @cherrypy.expose
    def decrypt_text(self, text):
        """
        Decrypt a piece of text, using AES.\n
        This function is called from the Java GUI.
        """
        logFull('CeXmlRpc:decrypt_text')
        if not text:
            return ''
        cherry_user = cherrypy.session.get('username')
        return self.project.decrypt_text(cherry_user, text)


    @cherrypy.expose
    def generate_index(self):
        """
        Store in a json file the tags from each test case file
        """
        user = cherrypy.session.get('username')
        userConn = self.project._find_local_client(user)
        try:
            result = userConn.root.generate_index()
        except Exception as e:
            return '*ERROR* Cannot generate index for user `{}`: `{}`!'.format(user, e)
        return result


    @cherrypy.expose
    def search_index(self, query):
        """
        Search for a query in the file index
        """
        user = cherrypy.session.get('username')
        userConn = self.project._find_local_client(user)
        try:
            result = copy.deepcopy(userConn.root.parse_index(query))
        except Exception as e:
            return '*ERROR* Cannot search index for user `{}`: `{}`!'.format(user, e)
        if isinstance(result, str):
            logWarning(result)
            return result

        tests_path = self.project.get_user_info(user, 'tests_path')
        if not result:
            return {'path':tests_path, 'data':'tests', 'folder':True, 'children':[]}

        allFiles = self.project.localFs.list_user_files(user, tests_path, True, True, result)
        return allFiles


    @cherrypy.expose
    def send_ep_echo(self, text, epname='ep'):
        """
        Send remote echo. Used for debug.
        """
        user = cherrypy.session.get('username')
        ep_conn = self.project._find_specific_ep(user, epname)
        if not ep_conn:
            return False
        try:
            ep_conn.root.echo(text)
            return True
        except Exception as e:
            logWarning('User `{}` - exception on EP echo: `{}`!'.format(user, e))
            return False


    @cherrypy.expose
    def send_ep_continue(self, epname='ep'):
        """
        Send remote continue.
        """
        user = cherrypy.session.get('username')
        ep_conn = self.project._find_specific_ep(user, epname)
        if not ep_conn:
            return False
        try:
            ep_conn.root.dbg_continue()
            logDebug('User `{}` sent EP debug continue.'.format(user))
            return True
        except Exception as e:
            logWarning('User `{}` - exception on EP continue: `{}`!'.format(user, e))
            return False


    @cherrypy.expose
    def send_ep_interact(self, epname, response):
        """
        Send remote response to a test interaction.
        """
        user = cherrypy.session.get('username')
        ep_conn = self.project._find_specific_ep(user, epname)
        if not ep_conn:
            return False
        try:
            ep_conn.root.set_interact(response)
            logDebug('User `{}` sent EP response continue.'.format(user))
        except Exception as e:
            logWarning('User `{}` - exception on EP continue: `{}`!'.format(user, e))
        self.project.set_exec_status(user, epname, STATUS_RUNNING)
        return True


# # #


    @cherrypy.expose
    def find_cc_xml_tag(self, tag_or_view):
        """
        Transform 1 ClearCase.XML tag name into a ClearCase view + path.
        """
        user = cherrypy.session.get('username')
        ccConfigs = ClearCaseParser(user).getConfigs(tag_or_view)
        if ccConfigs and 'view' in ccConfigs and 'actv' in ccConfigs:
            return ccConfigs['view'] + ':' + ccConfigs['actv']
        else:
            return False


    @cherrypy.expose
    def file_size(self, fpath, type='fs'):
        """
        Returns file size.
        If the file is from TWISTER PATH, use System file size,
        else get file size from user's home folder.
        """
        user = cherrypy.session.get('username')
        resp = self.project.file_size(user, fpath, type)
        if not isinstance(resp, long):
            logWarning(resp)
        return resp


    @cherrypy.expose
    def read_file(self, fpath, flag='r', fstart=0, type='fs'):
        """
        Read a file from TWISTER PATH, user's home folder, or ClearCase.
        Flag r/ rb = ascii/ binary.
        """
        user = cherrypy.session.get('username')
        logDebug('GUI ReadFile: user {}; flag {}; path {}; start {}; {}'.format(user, flag, fpath, fstart, type))
        resp = self.project.read_file(user, fpath, flag, fstart, type)
        if resp.startswith('*ERROR*'):
            logWarning(resp)
        return binascii.b2a_base64(resp)


    @cherrypy.expose
    def write_file(self, fpath, fdata, flag='w', type='fs'):
        """
        Write a file in user's home folder, or ClearCase.
        Flag w/ wb = ascii/ binary.
        """
        user = cherrypy.session.get('username')
        logDebug('GUI WriteFile: user {}; path {}; flag {}; {}'.format(user, fpath, flag, type))
        fdata = binascii.a2b_base64(fdata)
        # If this is NOT a binary file, fix the newline
        if not 'b' in flag:
            fdata = fdata.replace('\r', '')
        resp = self.project.write_file(user, fpath, fdata, flag, type)
        if resp != True:
            logWarning(resp)
        return resp


    @cherrypy.expose
    def delete_file(self, fpath, type='fs'):
        """
        Delete a file in user's home folder, or ClearCase.
        """
        user = cherrypy.session.get('username')
        return self.project.delete_file(user, fpath, type)


    @cherrypy.expose
    def create_folder(self, fdir, type='fs'):
        """
        Create a file in user's home folder, or ClearCase.
        """
        user = cherrypy.session.get('username')
        return self.project.create_folder(user, fdir, type)


    @cherrypy.expose
    def list_files(self, fdir, hidden=True, recursive=True, type='fs'):
        """
        List files from user's home folder, or ClearCase.
        """
        user = cherrypy.session.get('username')
        return self.project.list_files(user, fdir, hidden, recursive, type)


    @cherrypy.expose
    def delete_folder(self, fdir, type='fs'):
        """
        Delete a folder from user's home folder, or ClearCase.
        """
        user = cherrypy.session.get('username')
        return self.project.delete_folder(user, fdir, type)


# # #


    @cherrypy.expose
    def list_projects(self, type='project'):
        """
        List projects/ predefined projects.
        Magically return the CC paths, if CC is enabled.
        """
        # Check the username from CherryPy connection
        user = cherrypy.session.get('username')

        if type == 'predefined':
            # Auto detect if ClearCase Test Config Path is active
            ccConfig = self.project.get_clearcase_config(user, 'predefined_path')
            if ccConfig:
                view = ccConfig['view']
                actv = ccConfig['actv']
                fdir = ccConfig['path'].rstrip('/')
                if not fdir:
                    return '*ERROR* You did not set ClearCase Predefined Suites Path!'
                user_view_actv = '{}:{}:{}'.format(user, view, actv)
                resp = self.project.clearFs.list_user_files(user_view_actv, fdir)
            else:
                fdir = self.project.get_user_info(user, 'predefined_path')
                resp = self.project.localFs.list_user_files(user, fdir)
            return resp

        else:
            # Auto detect if ClearCase Test Config Path is active
            ccConfig = self.project.get_clearcase_config(user, 'projects_path')
            if ccConfig:
                view = ccConfig['view']
                actv = ccConfig['actv']
                fdir = ccConfig['path'].rstrip('/')
                if not fdir:
                    return '*ERROR* You did not set ClearCase Project Path!'
                user_view_actv = '{}:{}:{}'.format(user, view, actv)
                resp = self.project.clearFs.list_user_files(user_view_actv, fdir)
            else:
                fdir = self.project.get_user_info(user, 'projects_path')
                resp = self.project.localFs.list_user_files(user, fdir)
            return resp


    @cherrypy.expose
    def read_project_file(self, fpath):
        """
        Read a project file - returns a string.
        """
        user = cherrypy.session.get('username')
        logFull('GUI read_project_file {} {}'.format(user, fpath))
        return self.project.read_project_file(user, fpath)


    @cherrypy.expose
    def save_project_file(self, fpath, content):
        """
        Write a project file - returns a True/ False.
        """
        user = cherrypy.session.get('username')
        logFull('GUI save_project_file {} {}'.format(user, fpath))
        return self.project.save_project_file(user, fpath, content)


    @cherrypy.expose
    def delete_project_file(self, fpath):
        """
        Delete project file - returns a True/ False.
        """
        user = cherrypy.session.get('username')
        # Auto detect if ClearCase Test Config Path is active
        ccConfig = self.project.get_clearcase_config(user, 'projects_path')
        if ccConfig:
            view = ccConfig['view']
            actv = ccConfig['actv']
            path = ccConfig['path'].rstrip('/')
            if not path:
                return '*ERROR* User `{}` did not set ClearCase Project Path!'.format(user)
            user_view_actv = '{}:{}:{}'.format(user, view, actv)
            return self.project.clearFs.delete_user_file(user_view_actv, path +'/'+ fpath)
        else:
            dpath = self.project.get_user_info(user, 'projects_path').rstrip('/')
            return self.project.localFs.delete_user_file(user, dpath +'/'+ fpath)


    @cherrypy.expose
    def get_predef_suites_path(self):
        """
        Magically return the predefined suites path, from FWM or CC config.
        """
        # Check the username from CherryPy connection
        user = cherrypy.session.get('username')

        # Auto detect if ClearCase Test Config Path is active
        ccConfig = self.project.get_clearcase_config(user, 'predefined_path')
        if ccConfig:
            fdir = ccConfig['path']
            if not fdir:
                return '*ERROR* You did not set ClearCase Project Path!'
        else:
            fdir = self.project.get_user_info(user, 'predefined_path')
            if not fdir:
                return '*ERROR* You did not set Predefined Suites Path!'
        return fdir


    @cherrypy.expose
    def read_predefined_suite(self, abspath):
        """
        Read a predefined suite file - returns a string.
        """
        user = cherrypy.session.get('username')
        # Auto detect if ClearCase Test Config Path is active
        logDebug('GUI read_predefined_suite {} {}'.format(user, abspath))
        ccConfig = self.project.get_clearcase_config(user, 'predefined_path')
        if ccConfig:
            view = ccConfig['view']
            actv = ccConfig['actv']
            user_view_actv = '{}:{}:{}'.format(user, view, actv)
            return self.project.clearFs.read_user_file(user_view_actv, abspath)
        else:
            return self.project.localFs.read_user_file(user, abspath)


    @cherrypy.expose
    def save_predefined_suite(self, abspath, content):
        """
        Write a predefined suite file - returns a True/ False.
        """
        user = cherrypy.session.get('username')
        # Auto detect if ClearCase Test Config Path is active
        ccConfig = self.project.get_clearcase_config(user, 'predefined_path')
        if ccConfig:
            view = ccConfig['view']
            actv = ccConfig['actv']
            user_view_actv = '{}:{}:{}'.format(user, view, actv)
            return self.project.clearFs.write_user_file(user_view_actv, abspath, content)
        else:
            return self.project.localFs.write_user_file(user, abspath, content)


    @cherrypy.expose
    def list_test_cases(self, type='fs'):
        """
        List normal files/ clearcase files.
        Need option to switch from normal FS to CC.
        """
        # Check the username from CherryPy connection
        user = cherrypy.session.get('username')
        if type == 'clearcase':
            if 'ClearCase' in self.list_plugins(user):
                # Get all ClearCase data from clearcase XML
                ccConfigs = ClearCaseParser(user).getConfigs()
                if not 'tests_path' in ccConfigs:
                    err = '*ERROR* User `{}` did not activate ClearCase Tests Path!'.format(user)
                    logWarning(err)
                    return err
                ccConfig = ccConfigs['tests_path']
                logDebug('CC tests data: {}'.format(ccConfig))
                view = ccConfig['view']
                actv = ccConfig['actv']
                path = ccConfig['path']
                if not path:
                    return '*ERROR* User `{}` did not set ClearCase Tests Path!'.format(user)
                user_view_actv = '{}:{}:{}'.format(user, view, actv)
                return self.project.clearFs.list_user_files(user_view_actv, path)
            else:
                err = '*ERROR* User `{}` is trying to list a ClearCase path, but plug-in is not enabled!'.format(user)
                logWarning(err)
                return err
        else:
            tests_path = self.project.get_user_info(user, 'tests_path')
            return self.project.localFs.list_user_files(user, tests_path)


# # #


    @cherrypy.expose
    def service_mngr_command(self, command, name='', *args, **kwargs):
        """
        Send commands to Service Manager.\n
        Valid commands are: list, start, stop, status, get config, save config, get log.
        """
        logFull('CeXmlRpc:service_mngr_command')
        # Check the username from CherryPy connection
        user = cherrypy.session.get('username')
        user_roles = self.project.authenticate(user)
        if not user_roles:
            return False
        if 'CHANGE_SERVICES' not in user_roles['roles']:
            logDebug('Privileges ERROR! Username `{user}` cannot use Service Manager!'.format(**user_roles))
            return False
        return self.project.manager.send_command(command, name, args, kwargs)


    @cherrypy.expose
    def users_and_groups_mngr(self, cmd, name='', *args, **kwargs):
        """
        Manage users, groups and permissions.
        """
        logFull('CeXmlRpc:users_and_groups_mngr')
        user = cherrypy.session.get('username')
        return self.project.users_and_groups_mngr(user, cmd, name, args, kwargs)


    @cherrypy.expose
    def run_user_script(self, script_path):
        """
        Executes a script.
        Returns a string containing the text printed by the script.\n
        This function is called from the Java GUI.
        """
        logFull('CeXmlRpc:run_user_script')
        return execScript(script_path)


    @cherrypy.expose
    def test_database(self, db_server, db_name, db_user, db_password, shared_db=False):
        """
        Selects from database.
        This function is called from the Java GUI.
        """
        logFull('CeXmlRpc:test_database')
        user = cherrypy.session.get('username')
        conn = False

        try:
            conn = MySQLdb.connect(host=db_server, db=db_name,
                   user=db_user, passwd=db_password, connect_timeout=5)
        except Exception as e:
            err = 'MySQL error `{}`!'.format(e)

        if not conn:
            # Need to magically identify the correct key; the first pair is from private DB.xml;
            if shared_db:
                # Shared DB is True
                users_groups = self.project._parse_users_and_groups()
                encr_key = users_groups.get('shared_db_key', 'Luxoft')
            else:
                # Fallback to shared DB
                encr_key = None

            # Decode database password
            db_password = self.project.decrypt_text(user, db_password, encr_key)

            try:
                conn = MySQLdb.connect(host=db_server, db=db_name,
                       user=db_user, passwd=db_password, connect_timeout=5)
            except Exception as e:
                err = 'MySQL error `{}`!'.format(e)

        if conn:
            logInfo('MySQL {} connection `{} @ {} / {}` is OK, for user `{}`.'.format(
                'Shared' if shared_db else 'User', db_user, db_server, db_name, user))
            return True
        else:
            logInfo('Failed to connect to MySQL {} connection `{} @ {} / {}`, for user `{}`: {}'.format(
                'Shared' if shared_db else 'User', db_user, db_server, db_name, user, err))
            return False


    @cherrypy.expose
    def switch_db_shared(self, shared_db):
        """
        Announce the switch between user and shared DB.xml.
        """
        logFull('CeXmlRpc:switch_db_shared')
        user = cherrypy.session.get('username')
        if shared_db:
            shared_db = 'true'
        else:
            shared_db = 'false'

        logInfo('MySQL database switched to `{}`, for user `{}`.'.format(
                'Shared' if shared_db=='true' else 'User', user))
        self.project.set_user_info(user, 'use_shared_db', shared_db)
        return True


    @cherrypy.expose
    def run_db_select(self, user, field_id):
        """
        Selects from database.
        This function is called from the Java GUI.
        """
        logFull('CeXmlRpc:run_db_select')

        # Get the path to DB.XML
        db_file = self.project.get_user_info(user, 'db_config')
        if not db_file:
            err = 'Database: Null DB.XML file for user `{}`! Cannot connect!'.format(user)
            logError(err)
            return err

        # Use shared DB or not ?
        use_shared_db = self.project.get_user_info(user, 'use_shared_db')
        if use_shared_db and use_shared_db.lower() in ['true', 'yes']:
            use_shared_db = True
        else:
            use_shared_db = False

        # DB.xml + Shared DB parser
        users_groups = self.project._parse_users_and_groups()
        shared_db_path = users_groups['shared_db_cfg']
        # Database parser, fields, queries
        db_parser = DBParser(user, db_file, shared_db_path, use_shared_db)
        query = db_parser.get_query(field_id)
        db_config = db_parser.db_config
        db_server, db_name, db_user, db_passwd = db_config['default_server']
        del db_parser

        if not query:
            err = 'Database: Null Query `{}`, user `{}`!'.format(field_id, user)
            logError(err)
            return err

        conn = self.project.dbmgr.connect_db(user, db_server, db_name, db_user, db_passwd)
        curs = conn.cursor()

        try:
            curs.execute(query)
        except MySQLdb.Error as e:
            err = 'MySQL Error %d: %s' % (e.args[0], e.args[1])
            logError(err)
            return err

        rows = curs.fetchall()
        msg_str = ','.join( '|'.join([str(i) for i in row]) for row in rows )

        curs.close()
        conn.close()

        return msg_str


    @cherrypy.expose
    def send_mail(self, user, force=False):
        """
        Send e-mail after the suites are run.\n
        Server must be in the form `adress:port`.\n
        Username and password are used for authentication.\n
        This function is called every time the Central Engine stops.
        """
        logFull('CeXmlRpc:send_mail user `{}`.'.format(user))
        try:
            ret = self.project.send_mail(user, force)
            return ret
        except Exception as e:
            trace = traceback.format_exc()[34:].strip()
            logError('E-mail: Sending e-mail exception `{}` !'.format(trace))
            return False


    @cherrypy.expose
    def commit_to_database(self, user):
        """
        For each File from each EP, from each Suite, the results of the tests are saved to database,
        exactly as the user defined them in Database.XML.\n
        This function is called from the Java GUI.
        """
        logDebug('CE: Preparing to save into database for user `{}`...'.format(user))
        time.sleep(2) # Wait all the logs
        ret = self.project.save_to_database(user)
        if ret:
            logDebug('Saving to database was successful, user `{}`!'.format(user))
            return True
        else:
            logDebug('Could not save to database, user `{}`!'.format(user))
            return False


    @cherrypy.expose
    def get_shared_db(self):
        """
        Returns the content of Shared DB xml file.
        This function is called from the Java GUI.
        """
        shared_db_path = self.project._parse_users_and_groups()['shared_db_cfg']
        if os.path.isfile(shared_db_path):
            return open(shared_db_path, 'r').read()
        else:
            return ''


# # #   Persistence   # # #


    @cherrypy.expose
    def list_settings(self, config='', x_filter=''):
        """
        List all available settings, for 1 config of a user.
        """
        user = cherrypy.session.get('username')
        return self.project.list_settings(user, config, x_filter)


    @cherrypy.expose
    def get_settings_value(self, config, key):
        """
        Fetch a value from 1 config of a user.
        """
        user = cherrypy.session.get('username')
        return self.project.get_settings_value(user, config, key)


    @cherrypy.expose
    def set_settings_value(self, config, key, value):
        """
        Set a value for a key in the config of a user.
        """
        user = cherrypy.session.get('username')
        return self.project.set_settings_value(user, config, key, value)


    @cherrypy.expose
    def del_settings_key(self, config, key, index=0):
        """
        Del a key from the config of a user.
        """
        user = cherrypy.session.get('username')
        return self.project.del_settings_key(config, key, index)


    @cherrypy.expose
    def set_persistent_suite(self, suite, info={}, order=-1):
        """
        Create a new suite, using the INFO, at the position specified.\n
        This function writes in TestSuites.XML file.\n
        The changes will be available at the next START.
        """
        user = cherrypy.session.get('username')
        return self.project.set_persistent_suite(user, suite, info, order)


    @cherrypy.expose
    def del_persistent_suite(self, suite):
        """
        Delete an XML suite, using a name ; if there are more suites with the same name,
        only the first one is deleted.\n
        This function writes in TestSuites.XML file.\n
        The changes will be available at the next START.
        """
        user = cherrypy.session.get('username')
        return self.project.del_persistent_suite(user, suite)


    @cherrypy.expose
    def set_persistent_file(self, suite, fname, info={}, order=-1):
        """
        Create a new file in a suite, using the INFO, at the position specified.\n
        This function writes in TestSuites.XML file.\n
        The changes will be available at the next START.
        """
        user = cherrypy.session.get('username')
        return self.project.set_persistent_file(user, suite, fname, info, order)


    @cherrypy.expose
    def del_persistent_file(self, suite, fname):
        """
        Delete an XML file from a suite, using a name ; if there are more files
        with the same name, only the first one is deleted.\n
        This function writes in TestSuites.XML file.\n
        The changes will be available at the next START.
        """
        user = cherrypy.session.get('username')
        return self.project.del_persistent_file(user, suite, fname)


# --------------------------------------------------------------------------------------------------
#           E P ,   S U I T E   AND   F I L E   V A R I A B L E S
# --------------------------------------------------------------------------------------------------


    @cherrypy.expose
    def list_users(self, active=False):
        """
        Function called from the CLI,
        to list the users that are using Twister.
        """
        logFull('CeXmlRpc:list_users')
        data = self.project.list_users(active)
        return data


    @cherrypy.expose
    def get_user_variable(self, user, variable):
        """
        Function called from the Execution Process,
        to get information that is available only here, or are hard to get.
        """
        logFull('CeXmlRpc:get_user_variable user `{}`.'.format(user))
        data = self.project.get_user_info(user, variable)
        if data is None:
            data = False
        return data


    @cherrypy.expose
    def set_user_variable(self, user, key, variable):
        """
        Function called from the Execution Process,
        to set information that is available only here, or are hard to get.
        """
        logFull('CeXmlRpc:set_user_variable user `{}`.'.format(user))
        return self.project.set_user_info(user, key, variable)


    @cherrypy.expose
    def has_clients(self, user):
        """
        Find local, or remote clients.
        """
        logFull('CeXmlRpc:has_clients user `{}`.'.format(user))
        if self.project.rsrv.service._findConnection(usr=user, hello='client'):
            return True
        else:
            return False


    @cherrypy.expose
    def search_ep(self, user, epname):
        """
        Search one EP and return True or False.
        """
        logFull('CeXmlRpc:search_ep user `{}`.'.format(user))
        epDict = self.project.get_user_info(user, 'eps')
        return epname in epDict


    @cherrypy.expose
    def find_anonim_ep(self, user):
        """
        Find a local, free EP to be used as Anonim EP.
        """
        logFull('CeXmlRpc:find_anonim_ep user `{}`.'.format(user))
        return self.project._find_anonim_ep(user)


    @cherrypy.expose
    def list_eps(self, user):
        """
        Returns all EPs for current user.
        """
        logFull('CeXmlRpc:list_eps user `{}`.'.format(user))
        epList = self.project.get_user_info(user, 'eps') or {}
        return ','.join(epList.keys())


    @cherrypy.expose
    def get_ep_variable(self, user, epname, variable, compress=False):
        """
        This function is called from the Execution Process,
        to get information that is available only here, or are hard to get:

        - what the user selected in the Java GUI (release, build, comments, etc)
        - the name of the suite, the test files, etc.
        """
        logFull('CeXmlRpc:get_ep_variable user `{}`.'.format(user))
        data = self.project.get_ep_info(user, epname)
        if not data:
            return False
        value = data.get(variable, False)
        if value is None:
            return False
        if compress:
            return pickle.dumps(value)
        else:
            return value


    @cherrypy.expose
    def set_ep_variable(self, user, epname, variable, value):
        """
        This function is called from the Execution Process,
        to inject values inside the EP classes.\n
        The values can saved in the Database, when commiting.\n
        Eg: the OS, the IP, or other information can be added this way.
        """
        logFull('CeXmlRpc:set_ep_variable user `{}`.'.format(user))
        return self.project.set_ep_info(user, epname, variable, value)


    @cherrypy.expose
    def list_suites(self, user, epname):
        """
        Returns all Suites for one EP from current user.
        """
        logFull('CeXmlRpc:list_suites user `{}`.'.format(user))
        if not self.search_ep(user, epname):
            logError('CE ERROR! EP `%s` is not in the list of defined EPs: `%s`!' %\
                     (str(epname), self.list_eps(user)) )
            return False

        suiteList   = [str(k)+':'+v['name'] for k, v in self.project.get_ep_info(user, epname)['suites'].items()]
        return ','.join(suiteList)


    @cherrypy.expose
    def get_suite_variable(self, user, epname, suite, variable, compress=False):
        """
        Function called from the Execution Process,
        to get information that is available only here, or are hard to get.
        """
        logFull('CeXmlRpc:get_suite_variable user `{}`.'.format(user))
        data = self.project.get_suite_info(user, epname, suite)
        if not data:
            return False
        value = data.get(variable, False)
        if value is None:
            return False
        if compress:
            return pickle.dumps(value)
        else:
            return value


    @cherrypy.expose
    def get_file_variable(self, user, epname, file_id, variable):
        """
        Get information about a test file: dependencies, runnable, status, etc.
        """
        logFull('CeXmlRpc:get_file_variable user `{}`.'.format(user))
        data = self.project.get_file_info(user, epname, file_id)
        if not data:
            return False
        value = data.get(variable, False)
        if value is None:
            return False
        return value


    @cherrypy.expose
    def set_file_variable(self, user, epname, filename, variable, value):
        """
        Set extra information for a Filename, like Crash detected, OS, IP.\n
        Can be called from the Runner.\n
        This change only happens in the memory structure and it is reset every time
        Central Engine is start. If you need to make a persistent change, use set_persistent_file.
        """
        logFull('CeXmlRpc:set_file_variable user `{}`.'.format(user))
        return self.project.set_file_info(user, epname, filename, variable, value)


    @cherrypy.expose
    def set_started_by(self, user, data):
        """
        Remember the user that started the Central Engine.\n
        Called from the Java GUI.
        """
        logFull('CeXmlRpc:set_started_by user `{}`.'.format(user))
        name = data.split(';')[0]
        proj = ';'.join(data.split(';')[1:])
        self.project.set_user_info(user, 'started_by', str(name))
        self.project.set_user_info(user, 'proj_xml_name', str(proj))
        return 1


    @cherrypy.expose
    def queue_file(self, user, suite, fname):
        """
        Queue a file at the end of a suite, during runtime.
        If there are more suites with the same name, the first one is used.
        """
        logFull('CeXmlRpc:queue_file user `{}`.'.format(user))
        return self.project.queue_file(user, suite, fname)


    @cherrypy.expose
    def de_queue_files(self, user, data):
        """
        Remove a file from the files queue.
        """
        logFull('CeXmlRpc:de_queue_files user `{}`.'.format(user))
        return self.project.de_queue_files(user, data)


    @cherrypy.expose
    def get_global_variable(self, user, var_path):
        """
        Send a global variable, using a path to the variable.
        """
        logFull('CeXmlRpc:get_global_variable user `{}`.'.format(user))
        return self.project.configs.get_global_variable(user, var_path, False)


    @cherrypy.expose
    def set_global_variable(self, user, var_path, value):
        """
        Set a global variable path, for a user.\n
        The change is not persistent.
        """
        logFull('CeXmlRpc:set_global_variable user `{}`.'.format(user))
        return self.project.configs.set_global_variable(user, var_path, value)


# # #   Config files and folders   # # #


    @cherrypy.expose
    def list_configs(self, user=None):
        """
        Folders and Files from config folder.
        """
        if not user:
            user = cherrypy.session.get('username')
        # Auto detect if ClearCase Test Config Path is active
        ccConfig = self.project.get_clearcase_config(user, 'tcfg_path')
        if ccConfig:
            view = ccConfig['view']
            actv = ccConfig['actv']
            path = ccConfig['path']
            user_view_actv = '{}:{}:{}'.format(user, view, actv)
            return self.project.clearFs.list_user_files(user_view_actv, path)
        else:
            dirpath = self.project.get_user_info(user, 'tcfg_path')
            return self.project.localFs.list_user_files(user, dirpath)


    @cherrypy.expose
    def get_config(self, user, cfg_path, var_path):
        """
        Send a config file, using the full path to a config file and
        the full path to a config variable in that file.
        Function used by EPs / tests.
        """
        logFull('CeXmlRpc:get_config user `{}`.'.format(user))
        return self.project.configs.get_global_variable(user, var_path, cfg_path)


    @cherrypy.expose
    def is_lock_config(self, fpath):
        """ check if config is locked """
        cherry_user = cherrypy.session.get('username')
        return self.project.configs.is_lock_config(cherry_user, fpath)


    @cherrypy.expose
    def lock_config(self, fpath):
        """
        Lock config.
        """
        cherry_user = cherrypy.session.get('username')
        return self.project.configs.lock_config(cherry_user, fpath)


    @cherrypy.expose
    def unlock_config(self, fpath):
        """
        Unlock config.
        """
        cherry_user = cherrypy.session.get('username')
        return self.project.configs.unlock_config(cherry_user, fpath)


    @cherrypy.expose
    def read_config_file(self, fpath):
        """
        Read config file - returns a base64 string.
        """
        user = cherrypy.session.get('username')
        resp = self.project.configs.read_config_file(user, fpath)
        if resp.startswith('*ERROR*'):
            logWarning(resp)
        return binascii.b2a_base64(resp)


    @cherrypy.expose
    def save_config_file(self, fpath, content):
        """
        Save config file - returns a True/ False.
        """
        user = cherrypy.session.get('username')
        return self.project.configs.save_config_file(user, fpath, binascii.a2b_base64(content))


    @cherrypy.expose
    def delete_config_file(self, fpath):
        """
        Delete config file - returns a True/ False.
        """
        user = cherrypy.session.get('username')
        return self.project.configs.delete_config_file(user, fpath)


    @cherrypy.expose
    def create_config_folder(self, fpath):
        """
        Create a new folder in config - returns a True/ False.
        """
        user = cherrypy.session.get('username')
        fpath = fpath.rstrip('/') + '/'

        # Auto detect if ClearCase Test Config Path is active
        ccConfig = self.project.get_clearcase_config(user, 'tcfg_path')
        if ccConfig:
            view = ccConfig['view']
            actv = ccConfig['actv']
            path = ccConfig['path']
            user_view_actv = '{}:{}:{}'.format(user, view, actv)
            return self.project.clearFs.create_user_folder(user_view_actv, path +'/'+ fpath)
        else:
            dirpath = self.project.get_user_info(user, 'tcfg_path')
            return self.project.localFs.create_user_folder(user, dirpath +'/'+ fpath)


    @cherrypy.expose
    def delete_config_folder(self, fpath):
        """
        Delete a config folder - returns a True/ False.
        """
        user = cherrypy.session.get('username')
        fpath = fpath.rstrip('/') + '/'

        def flatten_files(parent_node, result):
            """ translate dictionary """
            # The node is valid ?
            if not parent_node:
                return []
            # This node has children ?
            if not parent_node.get('children'):
                return []

            for node in parent_node['children']:
                name = node['path']
                if not node.get('folder') and name.startswith(fpath):
                    result.append(name)
                flatten_files(node, result)
            return result

        cfgs = self.list_configs()

        for fdir in flatten_files(cfgs, []):
            # Unbind the config file, if it was binded
            self.project.parsers[user].del_binding(fdir)

        # Auto detect if ClearCase Test Config Path is active
        ccConfig = self.project.get_clearcase_config(user, 'tcfg_path')
        if ccConfig:
            view = ccConfig['view']
            actv = ccConfig['actv']
            path = ccConfig['path']
            user_view_actv = '{}:{}:{}'.format(user, view, actv)
            return self.project.clearFs.delete_user_folder(user_view_actv, path +'/'+ fpath)
        else:
            dirpath = self.project.get_user_info(user, 'tcfg_path')
            return self.project.localFs.delete_user_folder(user, dirpath +'/'+ fpath)


    @cherrypy.expose
    def get_binding(self, user, fpath):
        """
        Read a binding between a CFG and a SUT.
        The result is XML.
        """
        logDebug('User `{}` reads bindings for `{}`.'.format(user, fpath))
        return self.project.parsers[user].get_binding(fpath)


    @cherrypy.expose
    def set_binding(self, user, fpath, content):
        """
        Write a binding between a CFG and a SUT.
        Return True/ False.
        """
        fdata = self.project.parsers[user].set_binding(fpath, content)
        r = self.write_file('~/twister/config/bindings.xml', binascii.b2a_base64(fdata))
        if r:
            logDebug('User `{}` writes bindings for `{}`.'.format(user, fpath))
        else:
            logWarning('User `{}` could not update bindings for `{}`!'.format(user, fpath))
        return r


    @cherrypy.expose
    def del_binding(self, user, fpath):
        """
        Delete a binding from bindings.xml.
        Return True/ False.
        """
        logDebug('User `{}` deletes bindings for `{}`.'.format(user, fpath))
        return self.project.parsers[user].del_binding(fpath)


# --------------------------------------------------------------------------------------------------
#           E X E C U T I O N   S T A T U S
# --------------------------------------------------------------------------------------------------


    @cherrypy.expose
    def reset_project(self, user):
        """
        Reset project for 1 user.
        """
        logFull('CeXmlRpc:reset_project user `{}`.'.format(user))
        twister_cache = userHome(user) + '/twister/.twister_cache'
        setFileOwner(user, twister_cache)
        return self.project.reset_project(user)


    @cherrypy.expose
    def generate_testsuites(self, user, project_file):
        """
        Reset project for 1 user.
        """
        logFull('CeXmlRpc:generate_xml user `{}`.'.format(user))
        return self.project.xparser.generate_xml(user, project_file)


    @cherrypy.expose
    def get_exec_status(self, user, epname):
        """
        Return execution status for one EP. (stopped, paused, running, invalid)\n
        Called from the EP.
        """
        logFull('CeXmlRpc:get_exec_status user `{}`.'.format(user))
        if not self.search_ep(user, epname):
            logError('CE ERROR! EP `%s` is not in the list of defined EPs: `%s`!' %
                     (str(epname), self.list_eps(user)) )
            return False

        data = self.project.get_ep_info(user, epname)

        # Set EP last seen alive
        self.project.set_ep_info(user, epname, 'last_seen_alive', \
            datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        # Return a status, or stop
        reversed = dict((v, k) for k, v in EXEC_STATUS.iteritems())
        return reversed[data.get('status', 8)]


    @cherrypy.expose
    def get_interact_status(self, user):
        """
        Return interact queue status.
        Called by applet or other UI
        """
        data = self.project.get_user_info(user)
        interact_queue = data.get('interact',[])
        interact_string = ''
        if interact_queue:
            for interact in interact_queue:
                interact_string += '{}*{}*{}*{}'.format(interact['id'],
                                                        interact['type'],
                                                        interact['msg'],
                                                        interact['ep'])
                if interact['options']:
                    options = ','.join([str(i) for i in interact['options']['options']])
                    default_value = interact['options']['default']
                    interact_string += '*{},{}'.format(options, default_value)
                if interact != interact_queue[-1]:
                    interact_string += '|'
        return interact_string


    @cherrypy.expose
    def get_exec_status_all(self, user):
        """
        Return execution status for all EPs. (stopped, paused, running, invalid)\n
        Called from the Java GUI.
        """
        logFull('CeXmlRpc:get_exec_status_all user `{}`.'.format(user))
        data = self.project.get_user_info(user)
        reversed = dict((v, k) for k, v in EXEC_STATUS.iteritems())
        status = reversed[data.get('status', 8)]

        # If start time is not define, then define it
        if not data.get('start_time'):
            start_time = datetime.datetime.today()
            self.project.set_user_info(user, 'start_time', start_time.strftime('%Y-%m-%d %H:%M:%S'))
        else:
            start_time = datetime.datetime.strptime(data['start_time'], '%Y-%m-%d %H:%M:%S')

        # If the engine is not stopped, update elapsed time
        if data.get('status', 8) != STATUS_STOP:
            elapsed_time = str(datetime.datetime.today() - start_time).split('.')[0]
            self.project.set_user_info(user, 'elapsed_time', elapsed_time)
        else:
            elapsed_time = data.get('elapsed_time', 0)

        # Status + start time + elapsed time
        start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')

        return '{0}; {1}; {2}; {3};'.format(status, start_time, elapsed_time, data.get('started_by', 'X'))


    @cherrypy.expose
    def set_exec_status(self, user, epname, new_status, msg=''):
        """
        Set execution status for one EP. (0, 1, 2, or 3)\n
        Returns a string (stopped, paused, running).\n
        The `message` parameter can explain why the status has changed.\n
        Called from the EP.
        """
        logFull('CeXmlRpc:set_exec_status user `{}`.'.format(user))
        return self.project.set_exec_status(user, epname, new_status, msg)


    @cherrypy.expose
    def set_exec_status_all(self, user, new_status, msg=''):
        """
        Set execution status for all EPs. (STATUS_STOP, STATUS_PAUSED, STATUS_RUNNING).\n
        Returns a string (stopped, paused, running).\n
        The `message` parameter can explain why the status has changed.
        Called from the applet.
        """
        logFull('CeXmlRpc:set_exec_status_all user `{}`.'.format(user))
        return self.project.set_exec_status_all(user, new_status, msg)


# --------------------------------------------------------------------------------------------------
#           T E S T   F I L E   S T A T U S E S
# --------------------------------------------------------------------------------------------------


    @cherrypy.expose
    def get_file_status_all(self, user, epname=None, suite=None):
        """
        Returns a list with all statuses, for all files, in order.\n
        The status of one file can be obtained with get File Variable.\n
        Called from the Java GUI.
        """
        logFull('CeXmlRpc:get_file_status_all user `{}`.'.format(user))
        if epname and not self.search_ep(user, epname):
            logError('*ERROR* EP `{}` is not in the list of defined EPs: '\
                '`{}`!'.format(epname, self.list_eps(user)))
            return ''
        statuses = self.project.get_file_status_all(user, epname, suite)
        return ','.join(statuses)


    @cherrypy.expose
    def set_file_status(self, user, epname, file_id, new_status=10, time_elapsed=0.0):
        """
        Set status for one file and write in log summary.\n
        Called from the Runner.
        """
        logFull('CeXmlRpc:set_file_status user `{}`.'.format(user))
        return self.project.set_file_status(user, epname, file_id, new_status, time_elapsed)


    @cherrypy.expose
    def set_file_status_all(self, user, epname, new_status):
        """
        Reset file status for all files of one EP.\n
        Called from the Runner.
        """
        logFull('CeXmlRpc:set_file_status_all user `{}`.'.format(user))
        return self.project.set_file_status_all(user, epname, new_status)


# --------------------------------------------------------------------------------------------------
#           L I B R A R Y   AND   T E S T   S U I T E   F I L E S
# --------------------------------------------------------------------------------------------------


    @cherrypy.expose
    def list_plugins(self, user):
        """
        List all user plugins.
        """
        logFull('CeXmlRpc:list_plugins user `{}`.'.format(user))
        parser = PluginParser(user)
        pluginsList = parser.getPlugins()
        return pluginsList.keys()


    @cherrypy.expose
    def run_plugin(self, user, plugin, args):
        """
        Run a plugin, with a command.
        """
        logFull('CeXmlRpc:run_plugin user `{}`.'.format(user))

        # If argument is a string
        if type(args) == type(str()):
            try:
                args = urlparse.parse_qs(args)
            except:
                msg = 'CE ERROR: Cannot run plugin `%s` with arguments `%s`!' % (plugin, args)
                logError(msg)
                return msg
        # If argument is a valid dict, pass
        elif type(args) == type(dict()):
            if not 'command' in args:
                return '*ERROR* Invalid dictionary for plugin `%s` : %s !' % (plugin, args)
        else:
            return '*ERROR* Invalid type of argument for plugin `%s` : %s !' % (plugin, type(args))

        plugin_p = self.project._build_plugin(user, plugin)

        if not plugin_p:
            msg = '*ERROR* Plugin `{}` does not exist for user `{}`!'.format(plugin, user)
            logError(msg)
            return msg

        try:
            return plugin_p.run(args)
        except Exception as e:
            trace = traceback.format_exc()[34:].strip()
            logError('*ERROR* Plugin `{}`, ran with arguments `{}` and raised Exception: `{}`!'\
                     .format(plugin, args, trace))
            return 'Error on running plugin `{}` - Exception: `{}`!'.format(plugin, e)


    @cherrypy.expose
    def get_libraries_list(self, user='', all=True):
        """
        Returns the list of exposed libraries, from CE libraries folder.\n
        This list will be used to syncronize the libs on all EP computers.\n
        Called from the Runner and the Java GUI.
        """
        if not user:
            user = cherrypy.session.get('username')
        return self.project.get_libraries_list(user, all)


    @cherrypy.expose
    def get_test_description(self, fname):
        """
        Returns the title, description and all tags from a test file.\n
        Called from the Java GUI.
        """
        logFull('CeXmlRpc:get_test_description')
        if os.path.isfile(fname):
            # This function is defined in helpers.
            return getFileTags(fname)

        # If the user has roles and the ClearCase plugin is enabled...
        user = cherrypy.session.get('username')
        user_roles = self.project.authenticate(user)

        # Auto detect if ClearCase Test Config Path is active
        ccConfig = self.project.get_clearcase_config(user, 'tests_path')
        if user_roles and ccConfig:
            view = ccConfig['view']
            actv = ccConfig['actv']
            text = self.project.read_file(user, fname, type='clearcase:' + view)
            tags = re.findall('^[ ]*?[#]*?[ ]*?<(?P<tag>\w+)>([ -~\n]+?)</(?P=tag)>', text, re.MULTILINE)
            result = '<br>\n'.join(['<b>' + title + '</b> : ' + descr.replace('<', '&lt;') for title, descr in tags])
            # Hack `cleartool ls` data
            user_view_actv = '{}:{}:{}'.format(user, view, actv)
            data = self.project.clearFs.system_command(user_view_actv, 'cleartool ls {}'.format(fname))
            if data:
                cctag = re.search('@@(.+?)\s', data)
                if cctag:
                    result += '<br>\n' + '<b>ClearCase Version</b> : {}'.format(cctag.group(1))
            return result
        else:
            logWarning('Cannot find file `{}`! Null file description!'.format(fname))
            return ''


    @cherrypy.expose
    def is_file_checkout(self, fname):
        """
        Verify if the file is checked out in ClearCase.\n
        Called from the Java GUI.
        """
        logFull('CeXmlRpc:if_file_checkout')

        # If the user has roles and the ClearCase plugin is enabled...
        user = cherrypy.session.get('username')
        user_roles = self.project.authenticate(user)

        # Auto detect if ClearCase Test Config Path is active
        ccConfig = self.project.get_clearcase_config(user, 'tests_path')
        if user_roles and ccConfig:
            view = ccConfig['view']
            actv = ccConfig['actv']

            user_view_actv = '{}:{}:{}'.format(user, view, actv)
            data = self.project.clearFs.system_command(user_view_actv, 'cleartool lsco {}'.format(fname))
            if data:
                if data.find("checkout version") != -1:
                    return "True"
            return "False"
        else:
            logWarning('Cannot find file `{}`! Null file description!'.format(fname))
            return ''


    @cherrypy.expose
    def checkout_file(self, fname, comment):
        """
        Checkout ClearCase file.\n
        Called from the Java GUI.
        """
        logFull('CeXmlRpc:checkout_file')

        # If the user has roles and the ClearCase plugin is enabled...
        user = cherrypy.session.get('username')
        user_roles = self.project.authenticate(user)

        # Auto detect if ClearCase Test Config Path is active
        ccConfig = self.project.get_clearcase_config(user, 'tests_path')
        if user_roles and ccConfig:
            view = ccConfig['view']
            actv = ccConfig['actv']

            user_view_actv = '{}:{}:{}'.format(user, view, actv)
            data = self.project.clearFs.system_command(user_view_actv, 'cleartool co {} {}'.format(comment, fname))
            if data:
                if data.find("cleartool: Error") != -1:
                    # checkou error, we need to return the error
                    data = data.split('\n')
                    return '\n'.join(data[1:])
            return 'True'
        else:
            logWarning('Cannot find file `{}`! Null file description!'.format(fname))
            return ''


    @cherrypy.expose
    def uncheckout_file(self, fname):
        """
        UnCheckout ClearCase file.\n
        Called from the Java GUI.
        """
        logFull('CeXmlRpc:checkout_file')

        # If the user has roles and the ClearCase plugin is enabled...
        user = cherrypy.session.get('username')
        user_roles = self.project.authenticate(user)

        # Auto detect if ClearCase Test Config Path is active
        ccConfig = self.project.get_clearcase_config(user, 'tests_path')
        if user_roles and ccConfig:
            view = ccConfig['view']
            actv = ccConfig['actv']

            user_view_actv = '{}:{}:{}'.format(user, view, actv)
            data = self.project.clearFs.system_command(user_view_actv, 'cleartool unco -rm {}'.format(fname))
            if data:
                if data.find("cleartool: Error") != -1:
                    # checkou error, we need to return the error
                    data = data.split('\n')
                    return '\n'.join(data[1:])
            return 'True'
        else:
            logWarning('Cannot find file `{}`! Null file description!'.format(fname))
            return ''


    @cherrypy.expose
    def checkin_file(self, fname, comment):
        """
        Checkin ClearCase file.\n
        Called from the Java GUI.
        """
        logFull('CeXmlRpc:checkin_file')

        # If the user has roles and the ClearCase plugin is enabled...
        user = cherrypy.session.get('username')
        user_roles = self.project.authenticate(user)

        # Auto detect if ClearCase Test Config Path is active
        ccConfig = self.project.get_clearcase_config(user, 'tests_path')
        if user_roles and ccConfig:
            view = ccConfig['view']
            actv = ccConfig['actv']

            user_view_actv = '{}:{}:{}'.format(user, view, actv)
            data = self.project.clearFs.system_command(user_view_actv, 'cleartool ci {} {}'.format(comment, fname))
            if data:
                if data.find("cleartool: Error") != -1:
                    # checkou error, we need to return the error
                    data = data.split('\n')
                    return '\n'.join(data[1:])
            return 'True'
        else:
            logWarning('Cannot find file `{}`! Null file description!'.format(fname))
            return ''


# --------------------------------------------------------------------------------------------------
#           L O G S
# --------------------------------------------------------------------------------------------------


    @cherrypy.expose
    def get_log_file(self, user, read, fstart, filename):
        """
        Called in the Java GUI to show the logs.
        """
        logFull('CeXmlRpc:get_log_file user `{}`.'.format(user))
        return self.project.get_log_file(user, read, fstart, filename)


    @cherrypy.expose
    def log_message(self, user, log_type, log_message):
        """
        This function is exposed in all tests, all logs are centralized in the HOME of the user.\n
        In order for the user to be able to access the logs written by CE, which runs as ROOT,
        CE will start a small process in the name of the user and the process will write the logs.
        """
        logFull('CeXmlRpc:log_message user `{}`.'.format(user))
        return self.project.log_message(user, log_type, log_message)


    @cherrypy.expose
    def log_live(self, user, epname, log_message):
        """
        Writes CLI messages in a big log, so all output can be checked LIVE.\n
        Called from the EP.
        """
        logFull('CeXmlRpc:log_live user `{}`.'.format(user))
        return self.project.log_live(user, epname, log_message)


    @cherrypy.expose
    def reset_log(self, user, log_name):
        """
        Resets one log.\n
        Called from the Java GUI.
        """
        logFull('CeXmlRpc:reset_log user `{}`.'.format(user))
        return self.project.reset_log(user, log_name)


    @cherrypy.expose
    def reset_logs(self, user):
        """
        All logs defined in master config are erased.\n
        Called from the Java GUI and every time the project is reset.
        """
        logFull('CeXmlRpc:reset_logs user `{}`.'.format(user))
        return self.project.reset_logs(user)


    @cherrypy.expose
    def panic_detect_config(self, user, command, data=None):
        """
        Configure Panic Detect.
        """
        logFull('CeXmlRpc:panic_detect_config user `{}`.'.format(user))
        # If argument is a string
        if type(data) == type(str()):
            try:
                _data = urlparse.parse_qs(data)
                if _data:
                    data = {k: v[0] if isinstance(v, list) else v for k, v in _data.iteritems()}
            except:
                msg = 'CE ERROR: PD cannot parse data: {d}!'.format(d=data)
                logError(msg)
                return msg

        if data:
            args = {
                'command': command,
                'data': data,
            }
        else:
            args = {
                'command': command,
            }

        return self.project.panic_detect_config(user, args)



    @cherrypy.expose
    def get_iterations(self, user, configs):
        """
        It computes the number of iterations a test configuration contains
        It's called each time the user manipulates the configs for a test
        """
        return self.project.xparser.get_number_of_iterations(user,configs)

# Eof()
