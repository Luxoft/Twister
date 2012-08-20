
# File: xmlparser.py ; This file is part of Twister.

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
from plugins import BasePlugin

__all__ = ['TSCParser', 'DBParser', 'PluginParser']


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # TSC
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


class TSCParser:
    """
    Requirements: BeautifulSoup.
    This parser is specific for TSC project.
    It returns information like:
    - Test Suite (Test Plan) Config File
    - Logs Path
    - Reports Path
    - EPs list, active EPs
    - Test files for specific EP
    """

    def __init__(self, base_config='', files_config=''):

        if os.path.isfile(base_config):
            self.xmlDict = BeautifulStoneSoup(open(base_config))
        elif base_config and ( type(base_config)==type('') or type(base_config)==type(u'') ) \
                and ( base_config[0] == '<' and base_config[-1] == '>' ):
            self.xmlDict = BeautifulStoneSoup(base_config)
        else:
            raise Exception('Parser ERROR: Invalid config data type: `%s`!' % type(config_data))

        if not self.xmlDict.root:
            raise Exception('Parser ERROR: Cannot access XML config data!')

        self.configTS = None
        self.configHash = None
        self.getEpList()
        self.updateConfigTS(files_config)


    def updateConfigTS(self, files_config=''):
        """
        Updates Test Suite Cofig file hash and recreates internal XML structure,
        only if the XML file is changed.
        The file number and suite number have to be unique.
        """
        self.file_no = 1000
        self.suite_no = 100

        if files_config and ( type(files_config)==type('') or type(files_config)==type(u'') ) \
                and ( files_config[0] == '<' and files_config[-1] == '>' ):

            # This is pure XML data
            config_ts = files_config
            # Hash check the XML file, to see if is changed
            newConfigHash = hashlib.md5(files_config).hexdigest()

        else:

            if not files_config or not os.path.isfile(files_config):
                # Get path to Test-Suites XML from Master config
                files_config = str(self.xmlDict.root.masterxmltestsuite.text)

            if files_config.startswith('~'):
                files_config = os.getenv('HOME') + files_config[1:]
            if not os.path.isfile(files_config):
                print('Parser: Test-Suites XML file `%s` does not exist! Please check framework config XML file!' % files_config)
                self.configTS = None
                return -1
            else:
                config_ts = open(files_config).read()

            # Hash check the XML file, to see if is changed
            newConfigHash = hashlib.md5(config_ts).hexdigest()

        if self.configHash != newConfigHash:
            print('Parser: Test-Suites XML file changed, rebuilding internal structure...\n')
            # Use the new hash
            self.configHash = newConfigHash
            # Create Beautiful Soup class from the new XML file
            self.configTS = BeautifulStoneSoup(config_ts)

        if not self.configTS.root:
            print('Parser ERROR: Cannot access Test-Suites XML data!')
            return -1


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
        """
        All types of logs exposed from Python to the test cases.
        """
        return [str(log.name) for log in self.xmlDict.root.logfiles.findAll()]


    def getLogFileForType(self, logType):
        """
        Returns the path for one type of log.
        CE will use this path to write the log received from EP.
        """
        baseLogsPath = self.getLogsPath()
        logType = str(logType).lower()
        logFile = self.xmlDict.root.logfiles.find(logType)
        return baseLogsPath + os.sep + str(logFile.text)


    def getExitOnTestFail(self):
        """
        Returns the value of the tag "Exit On Test Fail".
        """
        if not self.configTS:
            print('Parser: Cannot get Exit on test fail status, because Test-Suites XML is invalid!')
            return False
        res = self.configTS.root.stoponfail
        if not res:
            return False
        if res.text.lower() == 'true':
            return True
        else:
            return False


    def getScripts(self):
        """
        Returns the value of the tags "ScriptPre" and "ScriptPost".
        """
        if not self.configTS:
            print('Parser: Cannot get Exit on test fail status, because Test-Suites XML is invalid!')
            return False
        p0 = self.configTS.root.scriptpre
        p1 = self.configTS.root.scriptpost
        if not p0:
            p0 = ''
        else:
            p0 = p0.text
        if not p1:
            p1 = ''
        else:
            p1 = p1.text
        return (p0, p1)


    def getEmailConfig(self):
        """
        Returns the e-mail configuration.
        After Central Engine stops, an e-mail must be sent to the people interested.
        """
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
        """
        Returns a list with all available EP names.
        """
        res = str(self.xmlDict.root.epidsfile.text)
        if res.startswith('~'):
            res = os.getenv('HOME') + res[1:]
        if not os.path.isfile(res):
            print('Parser: EP Names file `%s` does not exist! Please check framework config XML file!' % res)
            return None

        self.epnames = []
        for line in open(res).readlines():
            line = line.strip()
            if not line: continue
            self.epnames.append(line)
        return self.epnames


    def getActiveEps(self):
        """
        Returns a list with all active EPs from Test-Suites XML.
        """
        activeEPs = []
        if not self.configTS:
            print('Parser: Cannot get active EPs, because Test-Suites XML is invalid!')
            return []
        for ep in self.configTS('epid'):
            activeEPs.append(ep.text)
        activeEPs = list(set(activeEPs))
        return activeEPs


    def getSuiteInfo(self, suite_soup):
        """
        Returns a dict with information about 1 Suite from Test-Suites XML.
        The "suite" must be a BeautifulSoup class.
        """

        res = OrderedDict([['name', suite_soup.tsname.text]])
        prop_keys = suite_soup(lambda tag: tag.name=='propname' and tag.parent.name=='userdefined')
        prop_vals = suite_soup(lambda tag: tag.name=='propvalue' and tag.parent.name=='userdefined')
        res.update( dict(zip([p.text for p in prop_keys], [p.text for p in prop_vals])) ) # Pack Key + Value

        res['files'] = OrderedDict()
        res['ep'] = suite_soup.epid.text

        for file_tag in suite_soup('tcname'):
            file_data = self.getFileInfo(file_tag.parent)
            res['files'][str(self.file_no)] = file_data
            self.file_no += 1

        return res


    def getAllSuitesInfo(self, epname):
        """
        Returns a list with data for all suites of one EP.
        Also returns the file list, with all file data.
        """
        if not self.configTS:
            print('Parser: Cannot parse Test Suite XML! Exiting!')
            return {}

        if epname not in self.epnames:
            print('Parser: Station `%s` is not in the list of defined EPs: `%s`!' %
                (str(epname), str(self.epnames)) )
            return {}

        res = OrderedDict()

        for suite in [k.parent for k in self.configTS(name='epid') if k.text==epname]:
            suite_str = str(self.suite_no)
            res[suite_str] = self.getSuiteInfo(suite)
            # Add the suite ID for all files in the suite
            for file_id in res[suite_str]['files']:
                res[suite_str]['files'][file_id]['suite'] = suite_str
            self.suite_no += 1
        return res


    def getFileInfo(self, file_soup):
        """
        Returns a dict with information about 1 File from Test-Suites XML.
        The "file" must be a BeautifulSoup class.
        """
        res = OrderedDict()
        res['file']  = file_soup.tcname.text
        res['suite'] = None
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


    def getAllTestFiles(self):
        """
        Returns a list with ALL files defined for current suite, in order.
        """
        if not self.configTS:
            print('Parser: Fatal error! Cannot parse Test Suite XML!')
            return []

        files = self.configTS('tcname')

        if not files:
            print('Parser: Current suite has no files!')

        ids = range(1000, 1000 + len(files))

        return [str(i) for i in ids]


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # Database XML parser
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


class DBParser():
    """
    Requirements: BeautifulSoup.
    This parser will read DB.xml.
    """

    def __init__(self, config_data):

        self.config_data = config_data
        self.configHash = None
        self.db_config = {}
        self.updateConfig()


    def updateConfig(self):
        """ Reload all Database Xml info """

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
        """
        Used by Central Engine.
        Returns a dictionary with field ID : SQL select.
        """
        try:
            res = self.xmlDict.field_section('field', type="DbSelect")
        except:
            print('DBParser: Cannot find field_section in DB config!')
            return {}
        return {field['id']:field['sqlquery'] for field in res}


    def getScripts(self):
        """
        Used by Central Engine.
        Returns a list with field IDs.
        """
        try:
            res = self.xmlDict.field_section('field', type="UserScript")
        except:
            print('DBParser: Cannot find field_section in DB config!')
            return {}
        return [field['id'] for field in res]


    def getQuery(self, field_id):
        """ Used by Central Engine. """
        res = self.xmlDict.field_section('field', id=field_id)
        if not res:
            print('DBParser: Cannot find field ID `%s`!' % field_id)
            return False
        query = res[0].get('sqlquery')
        return query


    def getQueries(self):
        """ Used by Central Engine. """
        res = self.xmlDict('sql_statement')
        return [field.text for field in res]

# --------------------------------------------------------------------------------------------------
#           USED BY WEB SERVER - REPORTS
# --------------------------------------------------------------------------------------------------

    def getReportFields(self):
        """ Used by HTTP Server. """
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
        """ Used by HTTP Server. """
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
        """ Used by HTTP Server. """
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


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # Plugins XML parser
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


class PluginParser:
    """
    Requirements: BeautifulSoup.
    This parser will read Plugins.xml.
    """

    def __init__(self, user):

        if not os.path.exists('/home/%s/twister' % user):
            raise Exception('PluginParser ERROR: Cannot find Twister for user `%s` !' % user)
        config_data = '/home/%s/twister/config/plugins.xml' % user
        if not os.path.exists(config_data):
            raise Exception('PluginParser ERROR: Cannot find Plugins for user `%s` !' % user)

        self.config_data = config_data
        self.configHash = None
        self.p_config = OrderedDict()
        self.updateConfig()


    def updateConfig(self):
        """ Reload all Plugins Xml info """

        config_data = open(self.config_data).read()
        newConfigHash = hashlib.md5(config_data).hexdigest()

        config_data = config_data.replace('<pyfile/>', '<pyfile></pyfile>')
        config_data = config_data.replace('<jarfile/>', '<jarfile></jarfile>')

        if self.configHash != newConfigHash:
            self.configHash = newConfigHash
            #print('PluginParser: Plugin XML file changed, rebuilding internal structure...\n')

            self.xmlDict = BeautifulStoneSoup(config_data)
            if not self.xmlDict.root:
                print('PluginParser ERROR: Cannot access XML config data!')
                return False

            for plugin in self.xmlDict.root('plugin'):
                name = plugin('name')
                if not name:
                    print('PluginParser ERROR: Invalid plugin: `%s`!' % str(plugin))
                    continue
                name = name[0].text

                prop_keys = plugin(lambda tag: tag.name=='propname' and tag.parent.name=='property')
                prop_vals = plugin(lambda tag: tag.name=='propvalue' and tag.parent.name=='property')
                res = dict(zip([p.text for p in prop_keys], [p.text for p in prop_vals])) # Pack Key + Value

                self.p_config[name] = res
                self.p_config[name]['jarfile'] = plugin.jarfile.text
                self.p_config[name]['pyfile']  = plugin.pyfile.text
                self.p_config[name]['status']  = plugin.status.text


    def getPlugins(self):
        """ Return all plugins info """

        self.updateConfig()
        Base = BasePlugin.BasePlugin
        py_modules = [k +'::'+ os.path.splitext(self.p_config[k]['pyfile'])[0]
                      for k in self.p_config if self.p_config[k]['status'] == 'enabled']
        plugins = {}

        for module in py_modules:
            name = module.split('::')[0]
            mod  = module.split('::')[1]
            plug = None
            try:
                # Import the plugin module
                mm = __import__('plugins.' + mod, fromlist=['Plugin'])
                # Reload all data, just in case
                mm = reload(mm)
                plug = mm.Plugin
            except Exception, e:
                print 'ERROR in module `{0}`! Exception: {1}!'.format(mod, e)
                continue

            if not plug:
                print('Plugin `%s` must not be Null!' % plug)
                continue
            # Check plugin parent. Must be Base Plugin.
            if not issubclass(plug, Base):
                print('Plugin `%s` must be inherited from Base Plugin!' % plug)
                continue

            # Append plugin classes to plugins list
            d = self.p_config[name]
            d['plugin'] = plug
            plugins[name] = d

        return plugins


# Eof()
