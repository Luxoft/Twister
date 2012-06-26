
# File: xmlparser.py ; This file is part of Twister.

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
import time
import hashlib

from collections import OrderedDict

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print('TWISTER_PATH environment variable is not set! Exiting!')
    exit(1)
sys.path.append(TWISTER_PATH)

from trd_party.BeautifulSoup import BeautifulStoneSoup

__all__ = ['TSCParser', 'DBParser']


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # TSC
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


class TSCParser:
    '''
    Requirements: BeautifulSoup.
    This parser is specific for TSC project.
    It returns information like:
    - Test Suite (Test Plan) Config File
    - Logs Path
    - Reports Path
    - EPs list, active EPs
    - Test files for specific EP
    '''

    def __init__(self, config_data):
        if os.path.isfile(config_data):
            self.config_path = config_data
            self.xmlDict = BeautifulStoneSoup(open(config_data))
        elif config_data and type(config_data)==type('') or type(config_data)==type(u''):
            self.config_path = ''
            self.xmlDict = BeautifulStoneSoup(config_data)
        else:
            raise Exception('Parser ERROR: Invalid config data type: `%s`!' % type(config_data))

        if not self.xmlDict.root:
            raise Exception('Parser ERROR: Cannot access XML config data!')

        self.configTS = None
        self.configHash = None
        self.getEpList()
        self.updateConfigTS()


    def updateConfigTS(self):
        '''
        Updates Test Suite Cofig file hash and recreates internal XML structure,
        only if the XML file is changed.
        '''
        # Path of TestSuite/ Test-Suites XML
        config_ts = str(self.xmlDict.root.masterxmltestsuite.text)
        if config_ts.startswith('~'):
            config_ts = os.getenv('HOME') + config_ts[1:]
        if not os.path.isfile(config_ts):
            print('Parser: Test-Suites XML file `%s` does not exist! Please check framework config XML file!' % config_ts)
            return -1

        # Hash check the XML file, to see if is changed
        newConfigHash = hashlib.md5(open(config_ts).read()).hexdigest()
        if self.configHash != newConfigHash:
            print('Parser: Test-Suites XML file changed, rebuilding internal structure...')
            # Use the new hash
            self.configHash = newConfigHash
            # Create Beautiful Soup class from the new XML file
            self.configTS = BeautifulStoneSoup(open(config_ts))


    def getTestSuitePath(self):
        res = str(self.xmlDict.root.masterxmltestsuite.text)
        if res.startswith('~'):
            res = os.getenv('HOME') + res[1:]
        return res


    def getDbConfigPath(self):
        res = str(self.xmlDict.root.dbconfigfile.text)
        if res.startswith('~'):
            res = os.getenv('HOME') + res[1:]
        return res


    def getLogsPath(self):
        res = str(self.xmlDict.root.logspath.text)
        if res.startswith('~'):
            res = os.getenv('HOME') + res[1:]
        return res


    def getReportsPath(self):
        res = str(self.xmlDict.root.reportspath.text)
        if res.startswith('~'):
            res = os.getenv('HOME') + res[1:]
        return res


    def getLogTypes(self):
        '''
        All types of logs exposed from Python to the test cases.
        '''
        return [str(log.name) for log in self.xmlDict.root.logfiles.findAll()]


    def getLogFileForType(self, logType):
        '''
        Returns the path for one type of log.
        CE will use this path to write the log received from EP.
        '''
        baseLogsPath = self.getLogsPath()
        logType = str(logType).lower()
        logFile = self.xmlDict.root.logfiles.find(logType)
        return baseLogsPath + os.sep + str(logFile.text)


    def getEmailConfig(self):
        '''
        Returns the e-mail configuration.
        After Central Engine stops, an e-mail must be sent to the people interested.
        '''
        # Read email.xml
        e_file = str(self.xmlDict.root.emailconfigfile.text)
        if e_file.startswith('~'):
            e_file = os.getenv('HOME') + e_file[1:]
        if not os.path.isfile(e_file):
            print('Parser: E-mail Config file `%s` does not exist! Please check framework config XML file!' % e_file)
            return {}

        econfig = BeautifulStoneSoup(open(e_file))

        res = {}
        res['Enabled'] = ''
        res['SMTPPath'] = ''
        res['SMTPUser'] = ''
        res['SMTPPwd'] = ''
        res['From'] = ''
        res['To'] = ''
        res['Subject'] = ''
        res['Message'] = ''

        if econfig.enabled:
            res['Enabled'] = econfig.enabled.text
        if econfig.smtppath:
            res['SMTPPath'] = econfig.smtppath.text
        if econfig.smtpuser:
            res['SMTPUser'] = econfig.smtpuser.text
        if econfig.smtppwd:
            res['SMTPPwd'] = econfig.smtppwd.text
        if econfig('from'):
            res['From'] = econfig('from')[0].text
        if econfig('to'):
            res['To'] = econfig('to')[0].text
        if econfig.subject:
            res['Subject'] = econfig.subject.text
        if econfig.message:
            res['Message'] = econfig.message.text
        return res


    def getEpList(self):
        '''
        Returns a list with all available EP-IDs.
        '''
        res = str(self.xmlDict.root.epidsfile.text)
        if res.startswith('~'):
            res = os.getenv('HOME') + res[1:]
        if not os.path.isfile(res):
            print('Parser: EP Names file `%s` does not exist! Please check framework config XML file!' % res)
            return None

        self.epids = []
        for line in open(res).readlines():
            self.epids.append(line.strip())
        return self.epids


    def getActiveEps(self):
        '''
        Returns a list with all active EPs from Test-Suites XML.
        '''
        activeEpids = []
        for ep in self.configTS('epid'):
            activeEpids.append(ep.text)
        activeEpids = list(set(activeEpids))
        return activeEpids


    def getFileInfo(self, file_soup):
        '''
        Returns a dict with information about 1 File from Test-Suites XML.
        The "file" must be a BeautifulSoup class.
        '''
        res = OrderedDict()
        res['suite'] = file_soup.parent.tsname.text
        res['file']  = file_soup.tcname.text
        res['dependancy'] = file_soup.dependancy.text if file_soup.dependancy else ''

        prop_keys = file_soup(lambda tag: tag.name=='propname')
        prop_vals = file_soup(lambda tag: tag.name=='propvalue')
        params = ''

        # The order of the properties is important!
        for i in range(len(prop_keys)):
            p_key = prop_keys[i].text
            p_val = prop_vals[i].text

            # Param tags are special
            if p_key == 'param':
                params += p_val + ','
                p_val = params

            res[p_key] = p_val

        return res


    def getSuiteInfo(self, suite_soup):
        '''
        Returns a dict with information about 1 Suite from Test-Suites XML.
        The "suite" must be a BeautifulSoup class.
        '''

        prop_keys = suite_soup(lambda tag: tag.name=='propname' and tag.parent.name=='userdefined')
        prop_vals = suite_soup(lambda tag: tag.name=='propvalue' and tag.parent.name=='userdefined')
        res = dict(zip([p.text for p in prop_keys], [p.text for p in prop_vals])) # Pack Key + Value

        res['files'] = OrderedDict()
        res['ep'] = suite_soup.epid.text

        for file_tag in suite_soup('tcid'):
            file_data = self.getFileInfo(file_tag.parent)
            res['files'][file_tag.text] = file_data

        return res


    def getAllSuitesInfo(self, epname):
        '''
        Returns a list with data for all suites of one EP.
        Also returns the file list, with all file data.
        '''
        if not self.configTS:
            print('Parser: Cannot parse Test Suite XML! Exiting!')
            return []

        if epname not in self.epids:
            print('Parser: Station `%s` is not in the list of defined EPs: `%s`!' %
                (str(epname), str(self.epids)) )
            return []

        res = OrderedDict()
        for suite in [k.parent for k in self.configTS(name='epid') if k.text==epname]:
            suite_name = suite.tsname.text
            res[suite_name] = self.getSuiteInfo(suite)
        return res


    def getAllTestFiles(self):
        '''
        Returns a list with ALL files defined for current suite, in order.
        '''
        ti = time.clock()
        if not self.configTS:
            print('Parser: Fatal error! Cannot parse Test Suite XML!')
            return []

        ts = []
        files = self.configTS('tcname')

        if not files:
            print('Parser: Current suite has no files!')

        for TestCase in files:
            tcid = TestCase.parent.tcid
            if not tcid:
                print('Parser: Fatal error! Found files without ID in Test Suite XML!')
                return []
            ts.append(tcid.text)

        #print('Parser: TestSuite Files (%s files) took %.4f seconds.' % (len(ts), time.clock()-ti))
        return ts


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # Database XML parser
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


class DBParser():
    '''
    Requirements: BeautifulSoup.
    This parser will read DB.xml.
    '''

    def __init__(self, config_data):

        self.config_data = config_data
        self.configHash = None
        self.db_config = {}
        self.updateConfig()


    def updateConfig(self):
        ''' Reload all Database Xml info '''

        config_data = self.config_data
        newConfigHash = hashlib.md5(open(config_data).read()).hexdigest()

        if self.configHash != newConfigHash:
            self.configHash = newConfigHash
            print('DBParser: Database XML file changed, rebuilding internal structure...\n')

            if os.path.isfile(config_data):
                self.xmlDict = BeautifulStoneSoup(open(config_data))
            elif config_data and type(config_data)==type('') or type(config_data)==type(u''):
                self.xmlDict = BeautifulStoneSoup(config_data)
            else:
                raise Exception('DBParser: Invalid config data type: `%s`!' % type(config_data))

            if self.xmlDict.db_config:
                if self.xmlDict.db_config.server:
                    self.db_config['server']    = self.xmlDict.db_config.server.text
                if self.xmlDict.db_config.database:
                    self.db_config['database']  = self.xmlDict.db_config.database.text
                if self.xmlDict.db_config.user:
                    self.db_config['user']      = self.xmlDict.db_config.user.text
                if self.xmlDict.db_config.password:
                    self.db_config['password']  = self.xmlDict.db_config.password.text

# --------------------------------------------------------------------------------------------------
#           USED BY CENTRAL ENGINE
# --------------------------------------------------------------------------------------------------

    def getFields(self):
        ''' Used by Central Engine. '''
        try:
            res = self.xmlDict.field_section('field', type="DbSelect")
        except:
            print('DBParser: Cannot find field_section in DB config!')
            return {}
        return {field['id']:field['sqlquery'] for field in res}


    def getQuery(self, field_id):
        ''' Used by Central Engine. '''
        res = self.xmlDict.field_section('field', id=field_id)
        if not res:
            print('DBParser: Cannot find field ID `%s`!' % field_id)
            return False
        query = res[0].get('sqlquery')
        return query


    def getQueries(self):
        ''' Used by Central Engine. '''
        res = self.xmlDict('sql_statement')
        return [field.text for field in res]

# --------------------------------------------------------------------------------------------------
#           USED BY WEB SERVER - REPORTS
# --------------------------------------------------------------------------------------------------

    def getReportFields(self):
        ''' Used by HTTP Server. '''
        self.updateConfig()

        try:
            fields = self.xmlDict.reports_section('field')
        except:
            print('DBParser: Cannot load the database reports section!')
            return {}
        res = OrderedDict()

        for field in fields:
            d = {}
            d['id']       = field.get('id', '')
            d['type']     = field.get('type', '')
            d['label']    = field.get('label', d['id'])
            d['sqlquery'] = field.get('sqlquery', '')
            res[d['id']]  = d

        return res


    def getReports(self):
        ''' Used by HTTP Server. '''
        self.updateConfig()

        try:
            reports = self.xmlDict.reports_section('report')
        except:
            print('DBParser: Cannot load the database fields section!')
            return {}
        res = OrderedDict()

        for report in reports:
            d = {}
            d['id']       = report.get('id', '')
            d['type']     = report.get('type', '')
            d['path']     = report.get('path', '')
            d['sqlquery'] = report.get('sqlquery', '')
            d['sqltotal'] = report.get('sqltotal', '') # SQL Total Query
            d['sqlcompr'] = report.get('sqlcompare', '') # SQL Query Compare side by side
            res[d['id']]  = d

        return res


    def getRedirects(self):
        ''' Used by HTTP Server. '''
        self.updateConfig()

        try:
            reports = self.xmlDict.reports_section('redirect')
        except:
            print('DBParser: Cannot load the database redirect section!')
            return {}
        res = OrderedDict()

        for redirect in reports:
            d = {}
            d['id']       = redirect.get('id', '')
            d['path']     = redirect.get('path', '')
            res[d['id']]  = d

        return res

#
