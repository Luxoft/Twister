
# File: CentralEngineOthers.py ; This file is part of Twister.

# Copyright (C) 2012 , Luxoft

# Authors:
#    Andrei Costachi <acostachi@luxoft.com>
#    Andrei Toma <atoma@luxoft.com>
#    Cristian Constantin <crconstantin@luxoft.com>
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

The **Project** class collects and organizes all the information for the Central Engine.

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
import smtplib
import MySQLdb

from string import Template
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
        self.data = {}
        self.parsers = {}
        self.current_user = ''
        self.ulock = thread.allocate_lock()


    def createUser(self, user, config_path=''):
        """
        Create or overwrite one user.\n
        This creates a master XML parser and a list with all user variables.
        """

        if config_path and not os.path.exists(config_path):
            logError('Project ERROR: Config path `%s` does not exist !' % config_path)
            return False
        elif not os.path.exists('/home/%s/twister' % user):
            logError('Project ERROR: Cannot find Twister for user `%s` !' % user)
            return False
        else:
            config_path = '/home/%s/twister/config/fwmconfig.xml' % user

        self.users[user] = {'status': STATUS_STOP, 'eps': OrderedDict()}

        # User config XML
        self.parsers[user] = TSCParser(config_path)
        self.parser = self.parsers[user]

        # List with all EPs for this User
        epList = self.parser.getEpList()
        if not epList:
            logError('Project ERROR: Cannot load the list of EPs for user `%s` !' % user)
            return False

        # Calculate the Suites for each EP and the Files for each Suite
        for epname in epList:
            self.users[user]['eps'][epname] = {}
            self.users[user]['eps'][epname]['suites'] = self.parser.getAllSuitesInfo(epname)

        # Add framework config info to default user
        self.users[user]['config_path'] = config_path
        self.users[user]['tests_path'] = self.parser.getTestSuitePath()
        self.users[user]['logs_path'] = self.parser.getLogsPath()
        self.users[user]['log_types'] = {}

        for logType in self.parser.getLogTypes():
            self.users[user]['log_types'][logType] = self.parser.getLogFileForType(logType)

        # Data contains: EP -> Suite -> File
        self.data = self.users[user]

        # Save everything.
        self._dump()
        logDebug('Project: Created user `%s` ...' % user)

        return True


    def changeUser(self, user):
        """
        Switch user. Changes the pointers for `data` and `parser`.
        """

        with self.ulock:
            if user not in self.users:
                r = self.createUser(user)
                if not r: return False
            self.data = self.users[user]
            self.parser = self.parsers[user]

        return True


    def reset(self, user, config_path=''):
        """
        Reset user parser, all EPs to STOP, all files to PENDING.
        """

        if config_path and not os.path.exists(config_path):
            logError('Project ERROR: Config path `%s` does not exist! Using default config!' % config_path)
            config_path = False

        r = self.changeUser(user)
        if not r: return False

        # User config XML
        if not config_path:
            config_path = self.users[user]['config_path']
        self.parsers[user] = TSCParser(config_path)
        self.parser = self.parsers[user]

        # All EPs have status STOP
        for ep in self.data['eps']:
            self.data['eps'][ep]['status'] = STATUS_STOP

        # All tests have status PENDING
        self.setFileStatusAll(user, STATUS_PENDING)
        return True


# # #


    def _dump(self):
        """
        Internal function. Save all data structure on HDD.
        """
        with open(TWISTER_PATH + '/common/project_users.json', 'w') as f:
            try: json.dump(self.users, f, indent=4)
            except: pass


    def _calcPointers(self, user):
        """
        Internal function. Recalculate all pointers for Suites and Files.
        The pointers are useful for searching the data very fast.
        """
        # Ordered list of file IDs
        self.test_ids = self.parsers[user].getAllTestFiles()

        # Shortcut for ALL files data
        self.files_data = OrderedDict()
        for ep in self.data['eps']:
            for suite in self.data['eps'][ep]['suites']:
                for f_id in self.data['eps'][ep]['suites'][suite]['files']:
                    self.files_data[f_id] = self.data['eps'][ep]['suites'][suite]['files'][f_id]


# # #


    def getUserInfo(self, user, key=None):
        """
        Returns data for the current user, including all EP info.
        If the key is not specified, it can be a huge dictionary.
        """
        r = self.changeUser(user)
        if not r: return []

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
        self._calcPointers(user)
        self._dump()
        return True


    def getEpInfo(self, user, epname):
        """
        Retrieve all info available, about one EP.
        """
        r = self.changeUser(user)
        if not r: return {}

        return self.data['eps'].get(epname, {})


    def getEpFiles(self, user, epname):
        """
        Return a list with all files associated with one EP.
        """
        r = self.changeUser(user)
        if not r: return []

        files = []
        for suite in self.data['eps'][epname]['suites']:
            for fname in self.data['eps'][epname]['suites'][suite]['files']:
                files.append(fname)
        return files


    def setEpInfo(self, user, epname, key, value):
        """
        Create or overwrite a variable with a value, for one EP.
        """
        r = self.changeUser(user)
        if not r: return False

        if epname not in self.data['eps']:
            logDebug('Project: Invalid EP name `%s` !' % epname)
            return False
        if not key or key == 'suites':
            logDebug('Project: Invalid Key `%s` !' % str(key))
            return False

        self.data['eps'][epname][key] = value
        self._calcPointers(user)
        self._dump()
        return True


    def getSuiteInfo(self, user, epname, suite):
        """
        Retrieve all info available, about one EP.
        """
        r = self.changeUser(user)
        if not r: return {}

        if epname not in self.data['eps']:
            logDebug('Project: Invalid EP name `%s` !' % epname)
            return False
        if suite not in self.data['eps'][epname]['suites']:
            logDebug('Project: Invalid Suite name `%s` !' % suite)
            return False

        return self.data['eps'][epname]['suites'].get(suite, {})


    def getSuiteFiles(self, user, epname, suite):
        """
        Return a list with all files associated with one Suite.
        """
        r = self.changeUser(user)
        if not r: return []

        return self.data['eps'][epname]['suites'][suite]['files'].keys()


    def setSuiteInfo(self, user, epname, suite, key, value):
        """
        Create or overwrite a variable with a value, for one Suite.
        """
        r = self.changeUser(user)
        if not r: return False

        if epname not in self.data['eps']:
            logDebug('Project: Invalid EP name `%s` !' % epname)
            return False
        if suite not in self.data['eps'][epname]['suites']:
            logDebug('Project: Invalid Suite name `%s` !' % suite)
            return False
        if not key or key == 'files':
            logDebug('Project: Invalid Key `%s` !' % str(key))
            return False

        self.data['eps'][epname]['suites'][suite][key] = value
        self._calcPointers(user)
        self._dump()
        return True


    def getFileInfo(self, user, file_id):
        """
        Retrieve all info available, about one Test File.
        """
        r = self.changeUser(user)
        if not r: return {}

        self._calcPointers(user)
        return self.files_data.get(file_id, {})


    def setFileInfo(self, user, epname, suite, fileid, key, value):
        """
        Create or overwrite a variable with a value, for one Test File.
        """
        r = self.changeUser(user)
        if not r: return False

        if epname not in self.data['eps']:
            logDebug('Project: Invalid EP name `%s` !' % epname)
            return False
        if suite not in self.data['eps'][epname]['suites']:
            logDebug('Project: Invalid Suite name `%s` !' % suite)
            return False
        if fileid not in self.data['eps'][epname]['suites'][suite]['files']:
            logDebug('Project: Invalid File id `%s` !' % fileid)
            return False

        self.data['eps'][epname]['suites'][suite]['files'][fileid][key] = value
        self._calcPointers(user)
        self._dump()
        return True


    def getFileStatusAll(self, user, epname=None, suite=None):
        """
        Return the status of all files, in order.
        """
        r = self.changeUser(user)
        if not r: return []

        if suite and not epname:
            logError('Project: Must provide both EP and Suite!')
            return []

        statuses = {}
        final = []

        if epname:
            if suite:
                for fname in self.data['eps'][epname]['suites'][suite]['files']:
                    s = self.data['eps'][epname]['suites'][suite]['files'][fname].get('status', -1)
                    statuses[fname] = str(s)
            else:
                for suite in self.data['eps'][epname]['suites']:
                    for fname in self.data['eps'][epname]['suites'][suite]['files']:
                        s = self.data['eps'][epname]['suites'][suite]['files'][fname].get('status', -1)
                        statuses[fname] = str(s)
        else:
            statuses = { k: str( self.files_data[k].get('status', -1) ) for k in self.files_data }

        for tcid in self.test_ids:
            if tcid in statuses:
                final.append(statuses[tcid])

        return final


    def setFileStatusAll(self, user, epname=None, new_status=10):
        """
        Reset the status of all files, to value: x.
        """
        r = self.changeUser(user)
        if not r: return False

        for epcycle in self.data['eps']:
            if epname and epcycle != epname:
                continue
            for suite in self.data['eps'][epcycle]['suites']:
                for fname in self.data['eps'][epcycle]['suites'][suite]['files']:
                    self.data['eps'][epcycle]['suites'][suite]['files'][fname]['status'] = new_status

        self._dump()
        return True

# # #


    def setFileOwner(self, user, path):
        """
        Update file ownership for 1 file.
        """
        uinfo = self.getUserInfo(user, 'eps')
        epname = uinfo[uinfo.keys()[0]]
        uid = epname.get('twister_ep_uid')
        gid = epname.get('twister_ep_gid')
        if uid and gid:
            os.chown(path, uid, gid)
            return True
        else:
            return False


    def sendMail(self, user):
        """
        Send e-mail function.
        """
        r = self.changeUser(user)
        if not r: return False

        # This is updated every time.
        eMailConfig = self.parser.getEmailConfig()
        if not eMailConfig:
            logWarning('E-mail: Nothing to do here.')
            return False

        logPath = self.data['log_types']['logsummary']
        logSummary = open(logPath).read()

        if not logSummary:
            logDebug('E-mail: Nothing to send!')
            return False

        logDebug('E-mail: Preparing... Server `{SMTPPath}`, user `{SMTPUser}`, from `{From}`, to `{To}`...'
            ''.format(**eMailConfig))

        # Information that will be mapped into subject or message of the e-mail
        map_info = {'date': time.strftime("%Y-%m-%d %H:%M")}

        for ep in self.data['eps']:
            # All info about 1 EP
            ep_data = self.data['eps'][ep]

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

            for suite in ep_data['suites']:
                # All info about 1 Suite
                suite_data = ep_data['suites'][suite]

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
        body_path = os.path.split(self.parser.config_path)[0] +os.sep+ 'e-mail-tmpl.htm'
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
            e_mail_path = os.path.split(self.parser.config_path)[0] +os.sep+ 'e-mail.htm'
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

    def saveToDatabase(self, user):
        """
        Save all data from a user: Ep, Suite, File, into database,
        using the DB.XML for the current project.
        """
        r = self.changeUser(user)
        if not r: return False

        # Database parser, fields, queries
        # This is created every time the Save is called
        db_path = self.parser.getDbConfigPath()
        db_parser = DBParser(db_path)
        db_config = db_parser.db_config
        queries = db_parser.getQueries()
        fields = db_parser.getFields()
        del db_parser

        #
        conn = MySQLdb.connect(host=db_config.get('server'), db=db_config.get('database'),
            user=db_config.get('user'), passwd=db_config.get('password'))
        curs = conn.cursor()
        #

        for epname in self.data['eps']:

            for suite in self.data['eps'][epname]['suites']:
                for file_id in self.data['eps'][epname]['suites'][suite]['files']:

                    subst_data = dict( self.data['eps'][epname] )
                    del subst_data['suites']
                    subst_data.update( self.data['eps'][epname]['suites'][suite] )
                    del subst_data['files']
                    subst_data.update( self.data['eps'][epname]['suites'][suite]['files'][file_id] )

                    # Prerequisite files will not be saved to database
                    if subst_data.get('Prerequisite'):
                        continue

                    for query in queries:

                        # All variables that must be replaced in Insert
                        vars_to_replace = re.findall('(@.+?@)', query)

                        for field in vars_to_replace:
                            # Delete the @ character
                            u_query = fields.get(field.replace('@', ''))

                            if not u_query:
                                logError('File: {0}, cannot build query! Field {1} is not defined in the fields section!'.format(subst_data['file'], field))
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
                            logError('File: {0}, cannot build query! Error: {1}!'.format(subst_data['file'], str(e)))
                            return False

                        # :: For DEBUG ::
                        #open(TWISTER_PATH + '/config/Query.debug', 'a').write('File Query:: `{0}` ::\n{1}\n\n\n'.format(subst_data['file'], query))

                        # Execute MySQL Query!
                        try:
                            curs.execute(query)
                        except MySQLdb.Error, e:
                            logError('Error in query ``{0}``'.format(query))
                            logError('MySQL Error %d: %s!' % (e.args[0], e.args[1]))
                            return False

        #
        conn.commit()
        curs.close()
        conn.close()
        #

        return True

# # #

# Eof()
