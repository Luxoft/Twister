
# File: CentralEngineOthers.py ; This file is part of Twister.

# Copyright (C) 2012 , Luxoft

# Authors:
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

Information about *EPs*:

- EP name
- EP status (start, stop, pause)
- EP OS
- EP IP

Information about *Suites*:

- suite name
- other info from Test-Suites.XML (eg: release, or build)

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

import os
import sys
import re
import time
import json
import thread
import subprocess
import platform
import smtplib
import MySQLdb


from string import Template
from ast import literal_eval
from collections import OrderedDict
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print('$TWISTER_PATH environment variable is not set! Exiting!')
    exit(1)
sys.path.append(TWISTER_PATH)

from common.constants import *
from common.tsclogging import *
from common.xmlparser import *


class Project:

    """
    This class controls data about:

    - users
    - EPs
    - suites
    - test files

    """

    def __init__(self):

        self.users = {}
        self.parsers = {}
        self.plugins = {}
        self.test_ids = {}

        self.usr_lock = thread.allocate_lock()  # User change lock
        self.int_lock = thread.allocate_lock()  # Internal use lock
        self.eml_lock = thread.allocate_lock()  # E-mail lock
        self.db_lock  = thread.allocate_lock()  # Database lock

        ## Panic Detect __init__ ##
        # load config for current user
        self.panicDetectConfigPath = TWISTER_PATH + '/common/PanicDetectData.json'
        if not os.path.exists(self.panicDetectConfigPath):
            with self.int_lock:
                config = open(self.panicDetectConfigPath, 'wb')
                config.write('{}')
                config.close()
        config = open(self.panicDetectConfigPath, 'rb')
        self.panicDetectRegularExpressions = json.load(config)
        config.close()


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

        # If it's a valid path
        if base_config and not os.path.exists(base_config):
            logError('Project ERROR: Config path `%s` does not exist !' % base_config)
            return False
        elif not os.path.exists('/home/%s/twister' % user):
            logError('Project ERROR: Cannot find Twister for user `%s` !' % user)
            return False
        else:
            base_config = '/home/%s/twister/config/fwmconfig.xml' % user

        if not files_config:
            files_config = '/home/%s/twister/config/testsuites.xml' % user

        # User data + User parser
        # Parsers contain the list of all EPs and the list of all Project Globals
        self.users[user] = {'status': STATUS_STOP, 'eps': OrderedDict()}
        if config_data:
            self.parsers[user] = TSCParser(config_data, files_config)
        else:
            self.parsers[user] = TSCParser(base_config, files_config)

        # List with all EPs for this User
        epList = self.parsers[user].epnames
        if not epList:
            logCritical('Project ERROR: Cannot load the list of EPs for user `%s` !' % user)
            return False

        # Calculate the Suites for each EP and the Files for each Suite
        for epname in epList:
            self.users[user]['eps'][epname] = {}
            self.users[user]['eps'][epname]['suites'] = self.parsers[user].getAllSuitesInfo(epname)

        # Ordered list of file IDs, used for Get Status ALL
        self.test_ids[user] = self.parsers[user].getAllTestFiles()

        # Get project global variables from XML
        project_globals = self.parsers[user].project_globals

        # Add framework config info to default user
        self.users[user]['config_path'] = base_config
        self.users[user]['tests_path'] = files_config
        self.users[user]['logs_path'] = project_globals['LogsPath']
        self.users[user]['log_types'] = {}


        # Add path to DB, E-mail XML, Globals
        self.users[user]['db_config']  = project_globals['DbConfig']
        self.users[user]['eml_config'] = project_globals['EmailConfig']
        self.users[user]['glob_params'] = project_globals['GlobalParams']

        # Add the `exit on test Fail` value
        self.users[user]['exit_on_test_fail'] = project_globals['ExitOnTestFail']

        # Add the `Pre and Post` project Scripts
        self.users[user]['script_pre'] =  project_globals['ScriptPre']
        self.users[user]['script_post'] = project_globals['ScriptPost']

        # Add the `Database Autosave` value
        self.users[user]['db_auto_save'] = project_globals['DbAutoSave']

        # Add the 'Libraries'
        self.users[user]['libraries'] = project_globals['Libraries']

        # Add the `Testcase Delay` value
        self.users[user]['tc_delay'] = project_globals['TestcaseDelay']
        del project_globals

        for logType in self.parsers[user].getLogTypes():
            self.users[user]['log_types'][logType] = self.parsers[user].getLogFileForType(logType)

        # Save everything.
        self._dump()
        logDebug('Project: Created user `%s` ...' % user)

        return True


    def renameUser(self, name, new_name):
        """
        Rename 1 user.
        """
        with self.usr_lock:

            self.users[new_name] = self.users[name]
            self.parsers[new_name] = self.parsers[name]
            self.test_ids[new_name] = self.test_ids[name]

            del self.users[name]
            del self.parsers[name]
            del self.test_ids[name]

        self._dump()
        logDebug('Project: Renamed user `{0}` to `{1}`...'.format(name, new_name))

        return True


    def deleteUser(self, user):
        """
        Delete 1 user.
        """
        with self.usr_lock:

            del self.users[user]
            del self.parsers[user]
            del self.test_ids[user]

        self._dump()
        logDebug('Project: Deleted user `%s` ...' % user)

        return True


    def changeUser(self, user):
        """
        Switch user.\n
        This uses a lock, in order to create the user structure only once.
        If the lock is not present, on CE startup, all running EPs from one user will rush
        to create the memory structure.
        """
        with self.usr_lock:

            if not user:
                return False
            if user not in self.users:
                r = self.createUser(user)
                if not r: return False

        return True


    def reset(self, user, base_config='', files_config=''):
        """
        Reset user parser, all EPs to STOP, all files to PENDING.
        """
        if not user or user not in self.users:
            logError('Project ERROR: Invalid user `{0}` !'.format(user))
            return False

        if base_config and not os.path.isfile(base_config):
            logError('Project ERROR: Config path `%s` does not exist! Using default config!' % base_config)
            base_config = False

        r = self.changeUser(user)
        if not r: return False

        ti = time.clock()

        # User config XML files
        if not base_config:
            base_config = self.users[user]['config_path']
        if not files_config:
            files_config = self.users[user]['tests_path']

        logDebug('Project: RESET configuration for user `{0}`, using config files `{1}` and `{2}`.'.format(
            user, base_config, files_config))
        self.parsers[user] = TSCParser(base_config, files_config)

        # Calculate the Suites for each EP and the Files for each Suite
        for epname in self.users[user]['eps']:
            # All EPs must have status STOP
            self.users[user]['eps'][epname]['status'] = STATUS_STOP
            self.users[user]['eps'][epname] = {}
            self.users[user]['eps'][epname]['suites'] = self.parsers[user].getAllSuitesInfo(epname)

        # Ordered list of file IDs, used for Get Status ALL
        self.test_ids[user] = self.parsers[user].getAllTestFiles()

        # Get project global variables from XML
        project_globals = self.parsers[user].project_globals

        # Add framework config info to default user
        self.users[user]['config_path'] = base_config
        self.users[user]['tests_path'] = files_config
        self.users[user]['logs_path'] = project_globals['LogsPath']
        self.users[user]['log_types'] = {}

        # Add path to DB, E-mail XML, Globals
        self.users[user]['db_config']  = project_globals['DbConfig']
        self.users[user]['eml_config'] = project_globals['EmailConfig']
        self.users[user]['glob_params'] = project_globals['GlobalParams']

        # Add the `exit on test Fail` value
        self.users[user]['exit_on_test_fail'] = project_globals['ExitOnTestFail']

        # Add the `Pre and Post` project Scripts
        self.users[user]['script_pre']  = project_globals['ScriptPre']
        self.users[user]['script_post'] = project_globals['ScriptPost']

        # Add the `Database Autosave` value
        self.users[user]['db_auto_save'] = project_globals['DbAutoSave']

        # Add the 'Libraries'
        self.users[user]['libraries'] = project_globals['Libraries']

        # Add the `Testcase Delay` value
        self.users[user]['tc_delay'] = project_globals['TestcaseDelay']
        del project_globals

        for logType in self.parsers[user].getLogTypes():
            self.users[user]['log_types'][logType] = self.parsers[user].getLogFileForType(logType)

        logDebug('Project: RESET operation took %.4f seconds.' % (time.clock()-ti))
        return True


    def _dump(self):
        """
        Internal function. Save all data structure on HDD.\n
        This function must use a lock!
        """
        with self.int_lock:

            with open(TWISTER_PATH + '/common/project_users.json', 'w') as f:
                try: json.dump(self.users, f, indent=4)
                except: pass


# # #


    def _getConfigPath(self, user, _config):
        """
        Helper function.
        """
        config = _config.lower()

        if config in ['', 'fwmconfig', 'baseconfig']:
            return self.users[user]['config_path']

        elif config in ['project', 'testsuites']:
            return self.users[user]['tests_path']

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
        return self.parsers[user].setSettingsValue(cfg_path, key, value)


# # #


    def getUserInfo(self, user, key=None):
        """
        Returns data for the current user, including all EP info.
        If the key is not specified, it can be a huge dictionary.
        """
        r = self.changeUser(user)
        if not r:
            if key:
                return []
            else:
                return {}

        if key:
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
            logDebug('Project: Invalid Key `%s` !' % str(key))
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
        Return a list with all files associated with one EP.
        """
        r = self.changeUser(user)
        if not r: return []
        files = []

        for suite_id in self.users[user]['eps'][epname]['suites']:
            for fname in self.users[user]['eps'][epname]['suites'][suite_id]['files']:
                files.append(fname)

        return files


    def setEpInfo(self, user, epname, key, value):
        """
        Create or overwrite a variable with a value, for one EP.
        """
        r = self.changeUser(user)
        if not r: return False

        if epname not in self.users[user]['eps']:
            logDebug('Project: Invalid EP name `%s` !' % epname)
            return False
        if not key or key == 'suites':
            logDebug('Project: Invalid Key `%s` !' % str(key))
            return False

        self.users[user]['eps'][epname][key] = value
        self._dump()
        return True


    def getSuiteInfo(self, user, epname, suite_id):
        """
        Retrieve all info available, about one EP.
        """
        r = self.changeUser(user)
        if not r: return {}
        eps = self.users[user]['eps']

        if epname not in eps:
            logDebug('Project: Invalid EP name `%s` !' % epname)
            return False
        if suite_id not in eps[epname]['suites']:
            logDebug('Project: Invalid Suite name `%s` !' % suite_id)
            return False

        return eps[epname]['suites'].get(suite_id, {})


    def getSuiteFiles(self, user, epname, suite_id):
        """
        Return a list with all files associated with one Suite.
        """
        r = self.changeUser(user)
        if not r: return []
        eps = self.users[user]['eps']

        return eps[epname]['suites'][suite_id]['files'].keys()


    def setSuiteInfo(self, user, epname, suite_id, key, value):
        """
        Create or overwrite a variable with a value, for one Suite.
        """
        r = self.changeUser(user)
        if not r: return False
        eps = self.users[user]['eps']

        if epname not in eps:
            logDebug('Project: Invalid EP name `%s` !' % epname)
            return False
        if suite_id not in eps[epname]['suites']:
            logDebug('Project: Invalid Suite name `%s` !' % suite_id)
            return False
        if not key or key == 'files':
            logDebug('Project: Invalid Key `%s` !' % str(key))
            return False

        eps[epname]['suites'][suite_id][key] = value
        self._dump()
        return True


    def getFileInfo(self, user, file_id):
        """
        Retrieve all info available, about one Test File.\n
        The file ID must be unique!
        """
        r = self.changeUser(user)
        if not r: return {}
        eps = self.users[user]['eps']

        for epname in eps:
            for suite_id in eps[epname]['suites']:
                for fname in eps[epname]['suites'][suite_id]['files']:
                    if fname == file_id:
                        return eps[epname]['suites'][suite_id]['files'][fname]

        return {}


    def setFileInfo(self, user, epname, suite_id, file_id, key, value):
        """
        Create or overwrite a variable with a value, for one Test File.
        """
        r = self.changeUser(user)
        if not r: return False
        eps = self.users[user]['eps']

        if epname not in eps:
            logDebug('Project: Invalid EP name `%s` !' % epname)
            return False
        if suite_id not in eps[epname]['suites']:
            logDebug('Project: Invalid Suite name `%s` !' % suite_id)
            return False
        if file_id not in eps[epname]['suites'][suite_id]['files']:
            logDebug('Project: Invalid File id `%s` !' % file_id)
            return False

        eps[epname]['suites'][suite_id]['files'][file_id][key] = value
        self._dump()
        return True


    def getFileStatusAll(self, user, epname=None, suite_id=None):
        """
        Return the status of all files, in order.
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
                for file_id in eps[epname]['suites'][suite_id]['files']:
                    s = eps[epname]['suites'][suite_id]['files'][file_id].get('status', -1)
                    statuses[file_id] = str(s)
            else:
                for suite_id in eps[epname]['suites']:
                    for file_id in eps[epname]['suites'][suite_id]['files']:
                        s = eps[epname]['suites'][suite_id]['files'][file_id].get('status', -1)
                        statuses[file_id] = str(s)
        else:
            for epname in eps:
                for suite_id in eps[epname]['suites']:
                    for file_id in eps[epname]['suites'][suite_id]['files']:
                        s = eps[epname]['suites'][suite_id]['files'][file_id].get('status', -1)
                        statuses[file_id] = str(s)

        for tcid in self.test_ids[user]:
            if tcid in statuses:
                final.append(statuses[tcid])

        return final


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
            for suite_id in eps[epcycle]['suites']:
                for fname in eps[epcycle]['suites'][suite_id]['files']:
                    eps[epcycle]['suites'][suite_id]['files'][fname]['status'] = new_status

        self._dump()
        return True


# # #


    def setFileOwner(self, user, path):
        """
        Update file ownership for 1 file.\n
        `Chown` function works ONLY in Linux.
        """
        try:
            from pwd import getpwnam
            uid = getpwnam(user)[2]
            gid = getpwnam(user)[3]
        except:
            return False

        try:
            os.chown(path, uid, gid)
        except:
            logWarning('ERROR on set file owner! Cannot chown `{0}:{1}`!'.format(uid, gid))
            return False
        return True


    def execScript(self, script_path):
        """
        Execute a user script and return the text printed on the screen.
        """
        if not os.path.exists(script_path):
            logError('Exec script: The path `{0}` does not exist!'.format(script_path))
            return False

        try: os.system('chmod +x {0}'.format(script_path))
        except: pass

        logDebug('CE: Executing script `%s`...' % script_path)

        try:
            txt = subprocess.check_output([script_path])
            return txt.strip()
        except Exception, e:
            logError('Exec script `%s`: Exception - %s' % (script_path, str(e)) )
            return False


# # #


    def sendMail(self, user):
        """
        Send e-mail function.
        """
        with self.eml_lock:

            r = self.changeUser(user)
            if not r: return False

            # This is updated every time.
            eMailConfig = self.parsers[user].getEmailConfig()
            if not eMailConfig:
                logWarning('E-mail: Nothing to do here.')
                return False

            try:
                logPath = self.users[user]['log_types']['logSummary']
                logSummary = open(logPath).read()
            except:
                logError('E-mail: Cannot open Summary Log `{0}` for reading !'.format(logPath))
                return False

            if not logSummary:
                logDebug('E-mail: Nothing to send!')
                return False

            logDebug('E-mail: Preparing... Server `{SMTPPath}`, user `{SMTPUser}`, from `{From}`, to `{To}`...'\
                ''.format(**eMailConfig))

            # Information that will be mapped into subject or message of the e-mail
            map_info = {'date': time.strftime("%Y-%m-%d %H:%M")}

            for ep in self.users[user]['eps']:
                # All info about 1 EP
                ep_data = self.users[user]['eps'][ep]

                for k in ep_data:
                    if k in ['suites', 'status', 'last_seen_alive']: continue
                    if ep_data[k] == '': continue
                    # If the information is already in the mapping info
                    if k in map_info:
                        map_info[k] += ', ' + str(ep_data[k])
                        map_info[k] = ', '.join( list(set( map_info[k].split(', ') )) )
                        #map_info[k] = ', '.join(sorted( list(set(map_info[k].split(', '))) )) # Sorted ?
                    else:
                        map_info[k] = str(ep_data[k])

                for suite_id in ep_data['suites']:
                    # All info about 1 Suite
                    suite_data = ep_data['suites'][suite_id]

                    for k in suite_data:
                        if k in ['ep', 'files']: continue
                        if suite_data[k] == '': continue
                        # If the information is already in the mapping info
                        if k in map_info:
                            map_info[k] += ', ' + str(suite_data[k])
                            map_info[k] = ', '.join( list(set( map_info[k].split(', ') )) )
                            #map_info[k] = ', '.join(sorted( list(set(map_info[k].split(', '))) )) # Sorted ?
                        else:
                            map_info[k] = str(suite_data[k])

            # print 'E-mail map info::', map_info

            # Subject template string
            tmpl = Template(eMailConfig['Subject'])
            try:
                eMailConfig['Subject'] = tmpl.substitute(map_info)
            except Exception, e:
                logError('E-mail ERROR! Cannot build e-mail subject! Error: {0}!'.format(e))
                return False
            del tmpl

            # Message template string
            tmpl = Template(eMailConfig['Message'])
            try:
                eMailConfig['Message'] = tmpl.substitute(map_info)
            except Exception, e:
                logError('E-mail ERROR! Cannot build e-mail message! Error: {0}!'.format(e))
                return False
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
                logError('CE ERROR! Cannot find e-mail template file `{0}`!'.format(body_path))
                return False

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
                self.setFileOwner(user, e_mail_path)
                return True

            try:
                server = smtplib.SMTP(eMailConfig['SMTPPath'])
            except:
                logError('SMTP: Cannot connect to SMTP server!')
                return False

            try:
                logDebug('SMTP: Preparing to login...')
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(eMailConfig['SMTPUser'], eMailConfig['SMTPPwd'])
                logDebug('SMTP: Connect success!')
            except:
                logError('SMTP: Cannot autentificate to SMTP server!')
                return False

            try:
                server.sendmail(eMailConfig['From'], eMailConfig['To'], msg.as_string())
                logDebug('SMTP: E-mail sent successfully!')
                server.quit()
                return True
            except:
                logError('SMTP: Cannot send e-mail!')
                return False


# # #


    def findLog(self, user, epname, file_id, file_name):
        '''
        Parses the log file of one EP and returns the log of one test file.
        '''
        logPath = self.getUserInfo(user, 'logs_path') + os.sep + epname + '_CLI.log'

        try:
            data = open(logPath, 'r').read()
        except:
            logError('Find Log: File `{0}` cannot be read!'.format(logPath))
            return '*no log*'

        fbegin = data.find('<<< START filename: `%s:%s' % (file_id, file_name))
        if fbegin == -1:
            logDebug('Find Log: Cannot find `{0}:{1}` in log `{2}`!'.format(file_id, file_name, logPath))

        fend = data.find('<<< END filename: `%s:%s' % (file_id, file_name))
        fend += len('<<< END filename: `%s:%s` >>>' % (file_id, file_name))

        return data[fbegin:fend]


    def saveToDatabase(self, user):
        """
        Save all data from a user: Ep, Suite, File, into database,
        using the DB.XML for the current project.
        """
        with self.db_lock:

            r = self.changeUser(user)
            if not r: return False

            # Database parser, fields, queries
            # This is created every time the Save is called
            db_path = self.users[user]['db_config']
            db_parser = DBParser(db_path)
            db_config = db_parser.db_config
            queries = db_parser.getQueries() # List
            fields  = db_parser.getFields()  # Dictionary
            scripts = db_parser.getScripts() # List
            del db_parser

            if not queries:
                logDebug('Database: There are no queries defined! Nothing to do!')
                return False

            system = platform.machine() +' '+ platform.system() +', '+ ' '.join(platform.linux_distribution())

            #
            try:
                conn = MySQLdb.connect(host=db_config.get('server'), db=db_config.get('database'),
                    user=db_config.get('user'), passwd=db_config.get('password'))
                curs = conn.cursor()
            except MySQLdb.Error, e:
                logError('MySQL Error %d: %s!' % (e.args[0], e.args[1]))
                return False
            #

            conn.autocommit = False
            conn.begin()

            for epname in self.users[user]['eps']:

                for suite_id in self.users[user]['eps'][epname]['suites']:
                    for file_id in self.users[user]['eps'][epname]['suites'][suite_id]['files']:

                        # Substitute data
                        subst_data = {'file_id': file_id}
                        subst_data.update( self.users[user]['eps'][epname] )
                        del subst_data['suites']
                        subst_data.update( self.users[user]['eps'][epname]['suites'][suite_id] )
                        del subst_data['files']
                        subst_data.update( self.users[user]['eps'][epname]['suites'][suite_id]['files'][file_id] )

                        # Insert/ fix DB variables
                        subst_data['twister_ce_os'] = system
                        subst_data['twister_ep_name'] = epname
                        subst_data['twister_suite_name'] = self.users[user]['eps'][epname]['suites'][suite_id]['name']
                        subst_data['twister_tc_full_path'] = self.users[user]['eps'][epname]['suites'][suite_id]['files'][file_id]['file']
                        subst_data['twister_tc_name'] = os.path.split(subst_data['twister_tc_full_path'])[1]
                        subst_data['twister_tc_title'] = ''
                        subst_data['twister_tc_description'] = ''

                        # Escape all unicodes variables before sql statements
                        subst_data = {k: conn.escape_string(v) if isinstance(v, unicode) else v for k,v in subst_data.iteritems()}

                        try:
                            subst_data['twister_tc_log'] = self.findLog(user, epname, file_id, subst_data['twister_tc_full_path'])
                            subst_data['twister_tc_log'] = conn.escape_string( subst_data['twister_tc_log'].replace('\n', '<br>\n') )
                            subst_data['twister_tc_log'] = subst_data['twister_tc_log'].replace('<div', '&lt;div')
                            subst_data['twister_tc_log'] = subst_data['twister_tc_log'].replace('</div', '&lt;/div')
                        except:
                            subst_data['twister_tc_log'] = '*no log*'

                        # Prerequisite files will not be saved to database
                        if subst_data.get('Prerequisite'):
                            continue
                        # Pre-Suite or Post-Suite files will not be saved to database
                        if subst_data.get('Pre-Suite') or subst_data.get('Post-Suite'):
                            continue

                        # For every insert SQL statement, build correct data...
                        for query in queries:

                            # All variables of type `UserScript` must be replaced with the script result
                            try: vars_to_replace = re.findall('(\$.+?)[,\'"\s]', query)
                            except: vars_to_replace = []

                            for field in vars_to_replace:
                                field = field[1:]
                                # If the field is not `UserScript`, ignore it
                                if field not in scripts:
                                    continue

                                # Get Script Path, or null string
                                u_script = subst_data.get(field, '')

                                # Execute script and use result
                                r = self.execScript(u_script)
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
                            #open(TWISTER_PATH + '/common/Query.debug', 'a').write('File Query:: `{0}` ::\n{1}\n\n\n'.format(subst_data['file'], query))

                            # Execute MySQL Query!
                            try:
                                curs.execute(query)
                            except MySQLdb.Error, e:
                                logError('Error in query ``{0}``'.format(query))
                                logError('MySQL Error %d: %s!' % (e.args[0], e.args[1]))
                                conn.rollback()
                                return False

            #
            conn.commit()
            curs.close()
            conn.close()
            #

            return True


    def panicDetectConfig(self, user, args):
        """ Panic Detect mechanism
        valid commands: list, add, update, remove regular expression;

        list command: {'command': 'list'}
        add command: {'command': 'add', 'data': "{'expression': 'reg_exp_string'}"}
        update command: {'command': 'update', 'data': "{'id': 'reg_exp_id',
                                    expression': 'reg_exp_modified_string'}"}
        remove command:  {'command': 'remove', 'data': 'reg_exp_id'}
        """

        panicDetectCommands = {
            'simple': [
                'list',
            ],
            'argumented': [
                'add', 'update', 'remove',
            ]
        }

        args = {k: v[0] if isinstance(v, list) else v for k,v in args.iteritems()}

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

            response['data'] = json.dumps(self.panicDetectRegularExpressions)


        # add_regular_expression
        elif args['command'] == 'add':
            response['type'] = 'add_regular_expression reply'

            try:
                _args = literal_eval(args['data'])
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

                response['data'] = regExpID
                logDebug('Panic Detect: added regular expression for user: {u}'.format(u=user))
            except Exception, e:
                response['status']['success'] = False
                response['status']['message'] = '{er}'.format(er=e)


        # update_regular_expression
        elif args['command'] == 'update':
            response['type'] = 'update_regular_expression reply'

            try:
                _args = literal_eval(args['data'])
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

                response['data'] = regExpID
                logDebug('Panic Detect: updated regular expression for user: {u}'.format(u=user))
            except Exception, e:
                response['status']['success'] = False
                response['status']['message'] = '{er}'.format(er=e)

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

                response['data'] = regExpID
                logDebug('Panic Detect: removed regular expresion for user: {u}'.format(u=user))
            except Exception, e:
                response['status']['success'] = False
                response['status']['message'] = '{er}'.format(er=e)

        return response

# # #

# Eof()
