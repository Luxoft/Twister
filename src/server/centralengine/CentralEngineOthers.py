
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

import os
import sys
import re
import time
import json
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

#
# Information about user:
#- user name
#
# Information about EP:
#- EP name
#- EP status (start, stop, pause)
#- EP OS
#- EP IP
#
# Information about Suite:
#- suite name
#- other info from Test-Suites.XML
#
# Information about Test File:
#- file name
#- complete file path
#- test title
#- test description
#- timeout value (if any)
#- test status (pass, fail, skip, etc)
#- crash detected
#- test params
#- test date started and finished
#- test time elapsed
#- test log
#

class Project:

    '''
    This class controls data about:
    - users
    - EPs
    - suites
    - test files
    '''

    def __init__(self, config_path):

        # Framework config XML
        self.config_path = config_path
        self.parser = TSCParser(config_path)

        self.current_user = 'user'
        self.users = {
            'admin': {'status': STATUS_STOP, 'eps': OrderedDict()},
            'user':  {'status': STATUS_STOP, 'eps': OrderedDict()},
            }

        # List with all EPs for this User
        epList = self.parser.getEpList()
        if not epList:
            raise Exception('Project: Cannot load the list of EPs !')

        # Calculate the Suites for each EP,
        # And the Files for each Suite
        for epname in epList:
            self.users[self.current_user]['eps'][epname] = {}
            self.users[self.current_user]['eps'][epname]['suites'] = self.parser.getAllSuitesInfo(epname)

        # Add framework config info to default user
        self.users[self.current_user]['tests_path'] = self.parser.getTestSuitePath()
        self.users[self.current_user]['logs_path'] = self.parser.getLogsPath()
        self.users[self.current_user]['log_types'] = {}

        for logType in self.parser.getLogTypes():
            self.users[self.current_user]['log_types'][logType] = self.parser.getLogFileForType(logType)

        # Data contains: EP -> Suite -> File
        self.data = self.users[self.current_user]

        # Shortcuts for Suites and Files.
        self.calcPointers()
        self._dump()


    def _dump(self):
        '''
        Save all data structure on HDD.
        '''
        f = open(TWISTER_PATH + '/config/project_users.json', 'w')
        json.dump(self.users, f, indent=4)
        f.close()


    def calcPointers(self):
        '''
        Recalculate all pointers for Suites and Files.
        The pointers are useful for searching the data very fast.
        '''
        # Shortcut for ALL suites data
        self.suites_data = OrderedDict()
        for ep in self.data['eps']:
            for suite in self.data['eps'][ep]['suites']:
                self.suites_data[suite] = self.data['eps'][ep]['suites'][suite]
        #
        # Shortcut for ALL files data
        self.files_data = OrderedDict()
        for suite in self.suites_data:
            for f_id in self.suites_data[suite]['files']:
                self.files_data[f_id] = self.suites_data[suite]['files'][f_id]


    def changeUser(self, user):
        '''
        Switch user. The current data becomes the user data.
        '''
        self.current_user = user
        self.data = self.users[user]
        logDebug('Project: Changed user `%s`.' % user)


# # #


    def getUserInfo(self, key=None):
        '''
        Returns data for the current user, including all EP info.
        If the key is not specified, it can be a huge dictionary.
        '''

        if key:
            return self.users[self.current_user].get(key)
        else:
            return self.users[self.current_user]


    def setUserInfo(self, key, value):
        '''
        Create or overwrite a variable with a value, for the current user.
        '''
        if not key or key == 'eps':
            logDebug('Project: Invalid Key `%s` !' % str(key))
            return False

        self.users[self.current_user][key] = value
        self.calcPointers()
        self._dump()
        return True


    def getEpInfo(self, epname):
        '''
        Retrieve all info available, about one EP.
        '''
        return self.data['eps'].get(epname, {})

    getEpInfo.exposed = True


    def getEpFiles(self, epname):
        '''
        Return a list with all files associated with one EP.
        '''
        files = []
        for suite in self.data['eps'][epname]['suites']:
            for fname in self.data['eps'][epname]['suites'][suite]['files']:
                files.append(fname)
        return files


    def setEpInfo(self, epname, key, value):
        '''
        Create or overwrite a variable with a value, for one EP.
        '''
        if epname not in self.data['eps']:
            logDebug('Project: Invalid EP name `%s` !' % epname)
            return False
        if not key or key == 'suites':
            logDebug('Project: Invalid Key `%s` !' % str(key))
            return False

        self.data['eps'][epname][key] = value
        self.calcPointers()
        self._dump()
        return True


    def getSuiteInfo(self, suite):
        '''
        Retrieve all info available, about one EP.
        '''
        return self.suites_data.get(suite, {})

    getSuiteInfo.exposed = True


    def getSuiteFiles(self, epname, suite):
        '''
        Return a list with all files associated with one Suite.
        '''
        return self.data['eps'][epname]['suites'][suite]['files'].keys()


    def setSuiteInfo(self, epname, suite, key, value):
        '''
        Create or overwrite a variable with a value, for one Suite.
        '''
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
        self.calcPointers()
        self._dump()
        return True


    def getFileInfo(self, file_id):
        '''
        Retrieve all info available, about one Test File.
        '''
        return self.files_data.get(file_id, {})

    getFileInfo.exposed = True


    def setFileInfo(self, epname, suite, fileid, key, value):
        '''
        Create or overwrite a variable with a value, for one Test File.
        '''
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
        self.calcPointers()
        self._dump()
        return True


    def getFileStatusAll(self, epname=None, suite=None):
        '''
        Return the status of all files, in order.
        '''
        if suite and not epname:
            logError('Project: Must provide both EP and Suite!')
            return []

        if epname:
            statuses = []
            if suite:
                for fname in self.data['eps'][epname]['suites'][suite]['files']:
                    s = self.data['eps'][epname]['suites'][suite]['files'][fname].get('status', -1)
                    statuses.append( str(s) )
            else:
                for suite in self.data['eps'][epname]['suites']:
                    for fname in self.data['eps'][epname]['suites'][suite]['files']:
                        s = self.data['eps'][epname]['suites'][suite]['files'][fname].get('status', -1)
                        statuses.append( str(s) )
            return statuses
        else:
            return [ str( self.files_data[k].get('status', -1) ) for k in self.files_data ]


    def setFileStatusAll(self, new_status=10, epname=None):
        '''
        Reset the status of all files, to value: x.
        '''
        if epname:
            for suite in self.data['eps'][epname]['suites']:
                for fname in self.data['eps'][epname]['suites'][suite]['files']:
                    self.data['eps'][epname]['suites'][suite]['files'][fname]['status'] = new_status
        else:
            for epname in self.data['eps']:
                for suite in self.data['eps'][epname]['suites']:
                    for fname in self.data['eps'][epname]['suites'][suite]['files']:
                        self.data['eps'][epname]['suites'][suite]['files'][fname]['status'] = new_status
        self._dump()
        return True

# # #

    def sendMail(self):
        '''
        Send e-mail function.
        '''

        # This is updated every time.
        eMailConfig = self.parser.getEmailConfig()

        logPath = self.data['log_types']['logsummary']
        logSummary = open(logPath).read()

        if not logSummary:
            logDebug('E-mail: Nothing to send!')
            return False

        logDebug('E-mail: Preparing... Server `{SMTPPath}`, user `{SMTPUser}`, from `{From}`, to `{To}`...'
            ''.format(**eMailConfig))

        # Information that will be mapped into subject or message of the e-mail
        map_info = {'date': time.strftime("%Y-%m-%d %H:%M")}

        #user_info = .....
        #map_info.update(user_info)

        # Subject template string
        tmpl = Template(eMailConfig['Subject'])
        try:
            eMailConfig['Subject'] = tmpl.substitute(map_info)
        except Exception, e:
            logError('CE ERROR! Cannot build e-mail subject! Error: {0}!'.format(e))
            return False
        del tmpl

        # Message template string
        tmpl = Template(eMailConfig['Message'])
        try:
            eMailConfig['Message'] = tmpl.substitute(map_info)
        except Exception, e:
            logError('CE ERROR! Cannot build e-mail message! Error: {0}!'.format(e))
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
        body_path = os.path.split(self.config_path)[0] +os.sep+ 'e-mail-tmpl.htm'
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
            open(TWISTER_PATH + '/config/e-mail.htm', 'w').write(msg.as_string())
            logDebug('E-mail.htm file written. The message will NOT be sent.')
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

    def saveToDatabase(self):
        '''
        Save all data from a user: Ep, Suite, File, into database,
        using the DB.XML for the current project.
        '''
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

# # #

# Eof()
