
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
import md5
import time

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
    - Test files for specific EpId
    '''

    def __init__(self, config_data):
        if os.path.isfile(config_data):
            self.xmlDict = BeautifulStoneSoup(open(config_data))
        elif config_data and type(config_data)==type('') or type(config_data)==type(u''):
            self.xmlDict = BeautifulStoneSoup(config_data)
        else:
            raise Exception('TSCParser: Invalid config data type: `%s`!' % type(config_data))

        self.configTS = None
        self.configHash = None
        self.updateConfigTS()


    def updateConfigTS(self):
        '''
        Updates Test Suite Cofig file hash and recreates internal XML structure,
        only if the XML file is changed.
        '''
        # Path of TestSuite/ Master XML
        config_ts = str(self.xmlDict.root.masterxmltestsuite.text)
        if config_ts.startswith('~'):
            config_ts = os.getenv('HOME') + config_ts[1:]
        if not os.path.isfile(config_ts):
            print('TSCParser: Test Suite Config file `%s` does not exist!' % config_ts)
            return -1

        # Hash check the XML file, to see if is changed
        newConfigHash = md5.new(open(config_ts).read()).hexdigest()
        if self.configHash != newConfigHash:
            print('TSCParser: Master XML file changed, rebuilding internal structure...')
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
            print('TSCParser: E-mail Config file `%s` does not exist!' % e_file)
            return -1

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


    def getSuiteInfo(self, suite):
        '''
        Returns a list with information about all available Suites from Master XML.
        '''

        prop_keys = suite(lambda tag: tag.name=='propname' and tag.parent.name=='userdefined')
        prop_vals = suite(lambda tag: tag.name=='propvalue' and tag.parent.name=='userdefined')
        res = dict(zip([p.text for p in prop_keys], [p.text for p in prop_vals])) # Pack Key + Value

        return res


    def getFileInfo(self, epid, filename):
        '''
        Find all information about one test file, like deps, props, etc.
        `filename` can be the name of the file, or the file ID.
        '''
        res = {}

        # All suites for this EPID
        suites = self.configTS(text=epid)
        TestCase = None

        if suites:
            TestSuites = [suite.parent.parent for suite in suites]
        else:
            print('TSCParser: Cannot find EPID `%s`! Exiting!' % epid)
            return {}

        for TestSuite in TestSuites:
            file_info = TestSuite(text=filename)
            if file_info:
                TestCase = file_info[0].parent.parent
                res.update(self.getSuiteInfo(TestSuite))

        if not TestCase:
            print('TSCParser: Cannot find Info for `%s`! Exiting!' % filename)
            return {}

        try:
            prop_keys = TestCase.property('propname')  # All extra properties, keys
            prop_vals = TestCase.property('propvalue') # Properties, values
            res.update( dict(zip([p.text for p in prop_keys], [p.text for p in prop_vals])) ) # Pack Key + Value
        except:
            pass # Doesn't have extra properties

        res['id']    = TestCase.tcid.text
        res['file']  = TestCase.tcname.text
        res['epid']  = epid
        res['suite'] = TestSuite.tsname.text
        res['dep']   = TestCase.dependancy.text if TestCase.dependancy else ''
        #print 'File info ::', res
        return res


    def getEpIdsList(self):
        '''
        Returns a list with all available EP-IDs.
        '''
        res = str(self.xmlDict.root.epidsfile.text)
        if res.startswith('~'):
            res = os.getenv('HOME') + res[1:]
        if not os.path.isfile(res):
            print('TSCParser: EpIds file `%s` does not exist!' % res)
            return None

        self.epids = []
        for line in open(res).readlines():
            self.epids.append(line.strip())
        return self.epids


    def getActiveEpIds(self):
        '''
        Returns a list with all active EpIds from Master XML.
        '''
        activeEpids = []
        for ep in self.configTS.findAll('epid'):
            activeEpids.append(ep.text)
        return activeEpids


    def getAllTestFiles(self):
        '''
        Returns a list with ALL files defined for current suite, in order.
        '''
        ti = time.clock()
        if not self.configTS:
            print('TSCParser: Cannot parse Test Suite XML! Exiting!')
            return []

        ts = []
        files = self.configTS('tcname')

        if not files:
            print('TSCParser: Current suite has no files!')

        for TestCase in files:
            fname = TestCase.parent.tcname.text
            ts.append(fname)

        print('TSCParser: TestSuite Files (%s files) took %.4f seconds.' % (len(ts), time.clock()-ti))
        return ts


    def getTestSuiteFileList(self, epid):
        '''
        Returns a list with all files defined for current EP.
        '''
        ti = time.clock()
        if not self.configTS:
            print('TSCParser: Cannot parse Test Suite XML! Exiting!')
            return []

        if epid not in self.epids:
            print('TSCParser: Station `%s` is not in the list of defined EPIds: `%s`!' % \
                (str(epid), str(self.epids)) )
            return []

        soup = self.configTS
        ts = [tsSuite for tsSuite in soup('testsuite') if tsSuite.epid.text == epid]
        if not ts:
            print('TSCParser: Station `%s` has no files!' % str(epid))
            return []

        # For multiple test suites.
        tcNames = []
        for tcName in ts:
            tcNames += [fname.text for fname in tcName('tcname')]

        print('TSCParser: Parsing file fist (%s files) for `%s` took %.4f seconds.' % (len(tcNames), epid, (time.clock()-ti)))
        return tcNames


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # Database XML parser
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


class DBParser():
    '''
    Requirements: BeautifulSoup.
    This parser will read DB.xml.
    '''

    def __init__(self, config_data):
        if os.path.isfile(config_data):
            self.xmlDict = BeautifulStoneSoup(open(config_data))
        elif config_data and type(config_data)==type('') or type(config_data)==type(u''):
            self.xmlDict = BeautifulStoneSoup(config_data)
        else:
            raise Exception('DBParser: Invalid config data type: `%s`!' % type(config_data))

        self.db_config = {}
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

if __name__ == '__main__':

    t = TSCParser(os.getenv('HOME') + '/tscproject/twister/Config/fwmconfig.xml')
    print t.getLogsPath()
    print t.getLogTypes()
    print t.getReportsPath()
    print t.getEpIdsList()
    for l in t.getTestSuiteFileList('EP-1001'):
        print 'Found file:', l

#
