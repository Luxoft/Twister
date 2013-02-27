
# File: xmlparser.py ; This file is part of Twister.

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

from lxml import etree
from plugins import BasePlugin

from common.tsclogging import *

__all__ = ['TSCParser', 'DBParser', 'PluginParser', 'userHome']

#

def userHome(user):
    """
    Find the home folder for the given user, using /etc/passwd file.
    """
    lines = open('/etc/passwd').readlines()
    user_line = [line for line in lines if line.startswith(user + ':')]
    if not user_line: return False
    user_line = user_line[0].split(':')
    return user_line[-2]

#

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # TSC
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


class TSCParser:
    """
    Requirements: LXML.
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
            base_config = open(base_config).read()
        elif base_config and ( type(base_config)==type('') or type(base_config)==type(u'') ) \
                and ( base_config[0] == '<' and base_config[-1] == '>' ):
            pass
        else:
            raise Exception('Parser ERROR: Invalid config data type: `%s`!' % type(config_data))

        try:
            self.xmlDict = etree.fromstring(base_config)
        except:
            raise Exception('Parser ERROR: Cannot access XML config data!')

        self.configTS = None
        self.configHash = None
        self.epnames = []
        self.project_globals = {}

        self.updateConfigTS(files_config)
        self.updateProjectGlobals()
        self.getEpList()


    def updateConfigTS(self, files_config=''):
        """
        Updates Test Suite Cofig file hash and recreates internal XML structure,
        only if the XML file is changed.
        The file number and suite number have to be unique.
        """
        self.file_no = 1000
        self.suite_no = 100
        self.files_config = ''

        if files_config and ( type(files_config)==type('') or type(files_config)==type(u'') ) \
                and ( files_config[0] == '<' and files_config[-1] == '>' ):

            # This is pure XML data
            config_ts = files_config
            # Hash check the XML file, to see if is changed
            newConfigHash = hashlib.md5(files_config).hexdigest()

        else:

            if not files_config or not os.path.isfile(files_config):
                # Get path to Test-Suites XML from Master config
                files_config = self.files_config

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
            # Create XML Soup from the new XML file
            try:
                self.configTS = etree.fromstring(config_ts)
            except:
                print('Parser ERROR: Cannot access Test-Suites XML data!')
                self.configTS = None
                return -1

        self.files_config = files_config


    def updateProjectGlobals(self):
        """
        Returns the values of many global tags, from FWM and Test-Suites XML.
        """
        if self.configTS is None:
            print('Parser: Cannot get project globals, because Test-Suites XML is invalid!')
            return False

        # Reset globals
        self.project_globals = OrderedDict([
            ('EpsFile', ''),
            ('TestsPath', ''),
            ('DbConfig', ''),
            ('EmailConfig', ''),
            ('LogsPath', ''),
            ('ExitOnTestFail', False),
            ('DbAutoSave', False),
            ('TestcaseDelay', 0),
            ('ScriptPre', ''),
            ('ScriptPost', ''),
            ('Libraries', ''),
            ('GlobalParams', ''),
        ])

        # From FWM Config
        if self.xmlDict.xpath('EPIdsFile/text()'):
            path = self.xmlDict.xpath('EPIdsFile')[0].text
            self.project_globals['EpsFile'] = path

        if self.xmlDict.xpath('TestCaseSourcePath/text()'):
            path = self.xmlDict.xpath('TestCaseSourcePath')[0].text
            self.project_globals['TestsPath'] = path

        if self.xmlDict.xpath('DbConfigFile/text()'):
            path = self.xmlDict.xpath('DbConfigFile')[0].text
            if path.startswith('~'):
                path = os.getenv('HOME') + path[1:]
            self.project_globals['DbConfig'] = path

        if self.xmlDict.xpath('EmailConfigFile/text()'):
            path = self.xmlDict.xpath('EmailConfigFile')[0].text
            if path.startswith('~'):
                path = os.getenv('HOME') + path[1:]
            self.project_globals['EmailConfig'] = path

        if self.xmlDict.xpath('LogsPath/text()'):
            path = self.xmlDict.xpath('LogsPath')[0].text
            if path.startswith('~'):
                path = os.getenv('HOME') + path[1:]
            self.project_globals['LogsPath'] = path

        if self.xmlDict.xpath('GlobalParams/text()'):
            path = self.xmlDict.xpath('GlobalParams')[0].text
            if path.startswith('~'):
                path = os.getenv('HOME') + path[1:]
            self.project_globals['GlobalParams'] = path

        # From Project Config
        if self.configTS.xpath('stoponfail/text()'):
            if self.configTS.xpath('stoponfail/text()')[0].lower() == 'true':
                self.project_globals['ExitOnTestFail'] = True

        if self.configTS.xpath('dbautosave/text()'):
            if self.configTS.xpath('dbautosave/text()')[0].lower() == 'true':
                self.project_globals['DbAutoSave'] = True

        if self.configTS.xpath('tcdelay/text()'):
            self.project_globals['TestcaseDelay'] = self.configTS.xpath('round(tcdelay)')

        if self.configTS.xpath('ScriptPre/text()'):
            self.project_globals['ScriptPre'] = self.configTS.xpath('ScriptPre')[0].text

        if self.configTS.xpath('ScriptPost/text()'):
            self.project_globals['ScriptPost'] = self.configTS.xpath('ScriptPost')[0].text

        if self.configTS.xpath('libraries/text()'):
            self.project_globals['Libraries'] = self.configTS.xpath('libraries')[0].text

        return True


    def getEpList(self):
        """
        Returns a list with all available EP names.
        """
        eps_file = self.project_globals['EpsFile']

        if not eps_file:
            print('Parser: EP Names file is not defined! Please check framework config XML file!')
            return None
        if not os.path.isfile(eps_file):
            print('Parser: EP Names file `%s` does not exist! Please check framework config XML file!' % eps_file)
            return None

        # Reset EP list
        self.epnames = []

        for line in open(eps_file).readlines():
            line = line.strip()
            if not line: continue
            self.epnames.append(line)
        return self.epnames


    def getActiveEps(self):
        """
        Returns a list with all active EPs from Test-Suites XML.
        """
        if self.configTS is None:
            print('Parser: Cannot get active EPs, because Test-Suites XML is invalid!')
            return []

        activeEPs = []
        for epname in self.configTS.xpath('//EpId/text()'):
            activeEPs.append( str(epname) )

        activeEPs = (';'.join(activeEPs)).split(';')
        activeEPs = sorted(list(set(activeEPs)))
        activeEPs = [ep.strip() for ep in activeEPs if ep.strip()]
        return activeEPs

# # #

    def listSettings(self, xmlFile, xFilter=''):
        """
        High level function for listing all settings from a Twister XML config file.
        """
        if not os.path.isfile(xmlFile):
            print('Parse settings error! File path `{0}` does not exist!'.format(xmlFile))
            return False
        xmlSoup = etree.parse(xmlFile)
        if xFilter:
            return [x.tag for x in xmlSoup.xpath('//*') if xFilter in x.tag]
        else:
            return [x.tag for x in xmlSoup.xpath('//*')]


    def getSettingsValue(self, xmlFile, key):
        """
        High level function for getting a value from a Twister XML config file.
        """
        if not os.path.isfile(xmlFile):
            print('Parse settings error! File path `{0}` does not exist!'.format(xmlFile))
            return False
        if not key:
            return False
        else:
            key = str(key)

        xmlSoup = etree.parse(xmlFile)
        if xmlSoup.xpath(key):
            txt = xmlSoup.xpath(key)[0].text
            return (txt or '')
        else:
            return False


    def setSettingsValue(self, xmlFile, key, value):
        """
        High level function for setting a value in a Twister XML config file.
        """
        if not os.path.isfile(xmlFile):
            print('Parse settings error! File path `{0}` does not exist!'.format(xmlFile))
            return False
        if not key:
            return False
        else:
            key = str(key)
        if not value:
            value = ''
        else:
            value = str(value)

        xmlSoup = etree.parse(xmlFile)
        xml_key = xmlSoup.xpath(key)

        # If the key is found, update it
        if xml_key:
            xml_key[0].text = value
            xmlSoup.write(xmlFile)
            return True
        else:
            return False


    def delSettingsKey(self, xmlFile, key, index=0):
        """
        High level function for deleting a value from a Twister XML config file.
        If the `index` is specified and the `key` returns more values, only the
        index-th value is deleted; unless the `index` is -1, in this case, all
        values are deleted.
        """
        if not os.path.isfile(xmlFile):
            print('Parse settings error! File path `{0}` does not exist!'.format(xmlFile))
            return False
        # The key must be string
        if not (isinstance(key, str) or isinstance(key, unicode)):
            return False
        # The index must be integer
        if not isinstance(index, int):
            return False
        # The key must not be Null
        if not key:
            return False
        else:
            key = str(key)

        xmlSoup = etree.parse(xmlFile)
        xml_key = xmlSoup.xpath(key)

        if not xml_key:
            return False

        # For index -1, delete all matches
        if index == -1:
            for xml_v in xml_key:
                xml_parent = xml_v.getparent()
                xml_parent.remove(xml_v)
        else:
            # Use the index-th occurence, or, if the index is wrong, exit
            try: xml_key = xml_key[index]
            except: return False

            xml_parent = xml_key.getparent()
            xml_parent.remove(xml_key)

        xmlSoup.write(xmlFile)
        return True


    def setPersistentSuite(self, xmlFile, suite, info={}, order=-1):
        """
        This function writes in TestSuites.XML file.
        """
        if not os.path.isfile(xmlFile):
            print('Parse settings error! File path `{0}` does not exist!'.format(xmlFile))
            return False
        if not suite:
            return False
        else:
            suite = str(suite)
        try: order = int(order)
        except: return False

        # Root element from Project XML
        xmlSoup = etree.parse(xmlFile)
        xml_root = xmlSoup.getroot()
        suites_index = [xml_root.index(s) for s in xml_root.xpath('/Root/TestSuite')]

        if order == 0:
            # Add before the first suite
            insert_pos = 2
        elif abs(order) > len(suites_index):
            # If the negative pos is bigger than the index, add before the first suite
            insert_pos = 2
        elif order > len(suites_index):
            # Add after the last suite
            if not suites_index: insert_pos = 2
            else: insert_pos = suites_index[-1] + 1
        else:
            # If another position, add there
            if order > 0: order -= 1
            if not suites_index: insert_pos = 2
            else: insert_pos = suites_index[order] + 1

        # Suite XML object
        suite_xml = etree.Element('TestSuite')
        suite_xml.text = '\n' ; suite_xml.tail = '\n\n'
        tsName = etree.SubElement(suite_xml, 'tsName')
        tsName.text = suite ; tsName.tail = '\n'
        epName = etree.SubElement(suite_xml, 'EpId')
        epName.text = info.get('ep', ' ')
        epName.tail = '\n'
        try: del info['ep']
        except: pass

        for k, v in info.iteritems():
            tag = etree.SubElement(suite_xml, 'UserDefined')
            tag.text = '\n' ; tag.tail = '\n'
            prop = etree.SubElement(tag, 'propName')
            prop.text = str(k) ; prop.tail = '\n'
            val  = etree.SubElement(tag, 'propValue')
            val.text = str(v) ; val.tail = '\n'

        # Insert the new suite and save
        xml_root.insert(insert_pos, suite_xml)
        xmlSoup.write(xmlFile)
        return True


    def setPersistentFile(self, xmlFile, suite, fname, info={}, order=-1):
        """
        This function writes in TestSuites.XML file.
        """
        if not os.path.isfile(xmlFile):
            print('Parse settings error! File path `{0}` does not exist!'.format(xmlFile))
            return False
        if not suite:
            return False
        else:
            suite = str(suite)
        if not fname:
            return False
        else:
            fname = str(fname)
        try: order = int(order)
        except: return False

        # Root element from Project XML
        xmlSoup = etree.parse(xmlFile)
        xml_root = xmlSoup.getroot()

        suite_xml = xml_root.xpath('/Root/TestSuite[tsName="{0}"]'.format(suite))
        if not suite_xml: return False
        else: suite_xml = suite_xml[0]

        files_index = [ suite_xml.index(s) for s in \
            suite_xml.xpath('/Root/TestSuite[tsName="{0}"]/TestCase'.format(suite)) ]

        if order == 0:
            # Add before the first file
            insert_pos = 2
        elif abs(order) > len(files_index):
            # If the negative pos is bigger than the index, add before the first file
            insert_pos = 2
        elif order > len(files_index):
            # Add after the last file
            if not files_index: insert_pos = 2
            else: insert_pos = files_index[-1] + 1
        else:
            # If another position, add there
            if order > 0: order -= 1
            if not files_index: insert_pos = 2
            else: insert_pos = files_index[order] + 1

        # File XML object
        file_xml = etree.Element('TestCase')
        file_xml.text = '\n' ; file_xml.tail = '\n'
        tcName = etree.SubElement(file_xml, 'tcName')
        tcName.text = fname ; tcName.tail = '\n'

        for k, v in info.iteritems():
            tag = etree.SubElement(file_xml, 'Property')
            tag.text = '\n' ; tag.tail = '\n'
            prop = etree.SubElement(tag, 'propName')
            prop.text = str(k) ; prop.tail = '\n'
            val  = etree.SubElement(tag, 'propValue')
            val.text = str(v) ; val.tail = '\n'

        # Insert the new file and save
        suite_xml.insert(insert_pos, file_xml)
        xmlSoup.write(xmlFile)
        return True

# # #

    def _fixLogType(self, logType):
        """
        Helper function to fix log names.
        """
        if logType.lower() == 'logrunning':
            logType = 'logRunning'
        elif logType.lower() == 'logdebug':
            logType = 'logDebug'
        elif logType.lower() == 'logsummary':
            logType = 'logSummary'
        elif logType.lower() == 'logtest':
            logType = 'logTest'
        elif logType.lower() == 'logcli':
            logType = 'logCli'
        return logType


    def getLogTypes(self):
        """
        All types of logs exposed from Python to the test cases.
        """
        return [ self._fixLogType(log.tag) for log in self.xmlDict.xpath('LogFiles/*')]


    def getLogFileForType(self, logType):
        """
        Returns the path for one type of log.
        CE will use this path to write the log received from EP.
        """
        logs_path = self.project_globals['LogsPath']

        if not logs_path:
            print('Parser: Logs path is not defiled! Please check framework config XML file!')
            return {}
        if not os.path.isdir(logs_path):
            print('Parser: Invalid logs path `{0}`!'.format(logs_path))
            return ''

        logType = self._fixLogType(logType)
        logFile = self.xmlDict.xpath('//{0}/text()'.format(logType))

        if logFile:
            return logs_path + os.sep + logFile[0]
        else:
            return ''


    def getEmailConfig(self):
        """
        Returns the e-mail configuration.
        After Central Engine stops, an e-mail must be sent to the people interested.
        """
        eml_file = self.project_globals['EmailConfig']

        if not eml_file:
            print('Parser: E-mail Config file is not defined! Please check framework config XML file!')
            return {}
        if not os.path.isfile(eml_file):
            print('Parser: E-mail Config file `%s` does not exist! Please check framework config XML file!' % eml_file)
            return {}

        econfig = etree.parse(eml_file)

        res = {}
        res['Enabled'] = ''
        res['SMTPPath'] = ''
        res['SMTPUser'] = ''
        res['SMTPPwd'] = ''
        res['From'] = ''
        res['To'] = ''
        res['Subject'] = ''
        res['Message'] = ''

        if econfig.xpath('Enabled/text()'):
            res['Enabled'] = econfig.xpath('Enabled')[0].text
        if econfig.xpath('SMTPPath/text()'):
            res['SMTPPath'] = econfig.xpath('SMTPPath')[0].text
        if econfig.xpath('SMTPUser/text()'):
            res['SMTPUser'] = econfig.xpath('SMTPUser')[0].text
        if econfig.xpath('SMTPPwd/text()'):
            res['SMTPPwd'] = econfig.xpath('SMTPPwd')[0].text

        if econfig.xpath('From/text()'):
            res['From'] = econfig.xpath('From')[0].text
        if econfig.xpath('To/text()'):
            res['To'] = econfig.xpath('To')[0].text
        if econfig.xpath('Subject/text()'):
            res['Subject'] = econfig.xpath('Subject')[0].text
        if econfig.xpath('Message/text()'):
            res['Message'] = econfig.xpath('Message')[0].text
        return res


    def getSuiteInfo(self, epname, suite_soup):
        """
        Returns a dict with information about 1 Suite from Test-Suites XML.
        The "suite" must be a XML Soup class.
        """

        res = OrderedDict([ ['name', suite_soup.xpath('tsName/text()')[0]] ])
        res['ep'] = epname
        res['tb'] = ''
        res['pd'] = ''
        res['libraries'] = ''

        if suite_soup.xpath('libraries/text()'):
            res['libraries'] = suite_soup.xpath('libraries')[0].text

        if suite_soup.xpath('TbName/text()'):
            res['tb'] = suite_soup.xpath('TbName')[0].text

        if suite_soup.xpath('PanicDetect/text()'):
            res['pd'] = suite_soup.xpath('PanicDetect')[0].text

        prop_keys = suite_soup.xpath('UserDefined/propName')
        prop_vals = suite_soup.xpath('UserDefined/propValue')

        res.update( dict(zip( [k.text for k in prop_keys], [v.text for v in prop_vals] )) ) # Pack Key + Value

        res['files'] = OrderedDict()

        for file_soup in suite_soup.xpath('TestCase'):
            file_data = self.getFileInfo(file_soup)
            res['files'][str(self.file_no)] = file_data
            self.file_no += 1

        return res


    def getAllSuitesInfo(self, epname):
        """
        Returns a list with data for all suites of one EP.
        Also returns the file list, with all file data.
        """
        if self.configTS is None:
            print('Parser: Cannot parse Test Suite XML! Exiting!')
            return {}

        if epname not in self.epnames:
            print('Parser: Station `%s` is not in the list of defined EPs: `%s`!' %
                (str(epname), str(self.epnames)) )
            return {}

        res = OrderedDict()

        for suite in [s for s in self.configTS.xpath('//TestSuite') if epname in s.xpath('EpId/text()')[0].split(';')]:
            suite_str = str(self.suite_no)
            res[suite_str] = self.getSuiteInfo(epname, suite)
            # Add the suite ID for all files in the suite
            for file_id in res[suite_str]['files']:
                res[suite_str]['files'][file_id]['suite'] = suite_str
            self.suite_no += 1

        return res


    def getFileInfo(self, file_soup):
        """
        Returns a dict with information about 1 File from Test-Suites XML.
        The "file" must be a XML class.
        """
        res = OrderedDict()
        res['file']  = file_soup.xpath('tcName')[0].text
        res['suite'] = None
        res['dependancy'] = file_soup.xpath('tcName')[0].text if file_soup.xpath('tcName/text()') else ''

        prop_keys = file_soup.xpath('Property/propName')
        prop_vals = file_soup.xpath('Property/propValue')
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
        if self.configTS is None:
            print('Parser: Fatal error! Cannot parse Test Suite XML!')
            return []

        files = self.configTS.xpath('//tcName')

        if not files:
            print('Parser: Current suite has no files!')

        ids = range(1000, 1000 + len(files))

        return [str(i) for i in ids]


    def getGlobalParams(self):
        """
        Returns a dictionary containing All global parameters,
        that will be available for all tests.
        """
        globs_file = self.project_globals['GlobalParams']

        if not globs_file:
            print('Parser: Globals Config file is not defined! Please check framework config XML file!')
            return {}
        if not os.path.isfile(globs_file):
            print('Parser: Globals Config file `%s` does not exist! Please check framework config XML file!' % globs_file)
            return {}

        params_xml = etree.parse(globs_file)

        def recursive(xml, gparams):
            for folder in xml.xpath('folder'):
                tmp = {gparam.find('name').text: gparam.find('value').text for gparam in folder.xpath('param')}
                tmp.update( recursive(folder, tmp) )
                gparams[folder.find('fname').text] = tmp
            return gparams

        gparams = recursive(params_xml, {})
        return gparams


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # Database XML parser
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


class DBParser():
    """
    Requirements: LXML.
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
            # print('DBParser: Database XML file changed, rebuilding internal structure...\n')

            if os.path.isfile(config_data):
                try: self.xmlDict = etree.fromstring(open(config_data).read())
                except: raise Exception('DBParser: Cannot parse DB config file!')
            elif config_data and type(config_data)==type('') or type(config_data)==type(u''):
                try: self.xmlDict = etree.fromstring(config_data)
                except: raise Exception('DBParser: Cannot parse DB config file!')
            else:
                raise Exception('DBParser: Invalid config data type: `%s`!' % type(config_data))

            if self.xmlDict.xpath('db_config/server/text()'):
                self.db_config['server']    = self.xmlDict.xpath('db_config/server')[0].text
            if self.xmlDict.xpath('db_config/database/text()'):
                self.db_config['database']  = self.xmlDict.xpath('db_config/database')[0].text
            if self.xmlDict.xpath('db_config/user/text()'):
                self.db_config['user']      = self.xmlDict.xpath('db_config/user')[0].text
            if self.xmlDict.xpath('db_config/password/text()'):
                self.db_config['password']  = self.xmlDict.xpath('db_config/password')[0].text

# --------------------------------------------------------------------------------------------------
#           USED BY CENTRAL ENGINE
# --------------------------------------------------------------------------------------------------

    def getFields(self):
        """
        Used by Central Engine.
        Returns a dictionary with field ID : DB select.
        """
        if not self.xmlDict.xpath('twister_user_defined/field_section/field'):
            print('DBParser: There are no fields in the field_section, in DB config!')
            return {}

        ids = self.xmlDict.xpath('twister_user_defined/field_section/field[@Type="DbSelect"]/@ID')
        sqls = self.xmlDict.xpath('twister_user_defined/field_section/field[@Type="DbSelect"]/@SQLQuery')

        return dict(zip( [str(x) for x in ids], [str(x) for x in sqls] ))


    def getScripts(self):
        """
        Used by Central Engine.
        Returns a list with field IDs.
        """
        if not self.xmlDict.xpath('twister_user_defined/field_section/field'):
            print('DBParser: There are no fields in the field_section, in DB config!')
            return {}

        scripts = self.xmlDict.xpath('twister_user_defined/field_section/field[@Type="UserScript"]/@ID')

        return [str(x) for x in scripts]


    def getQuery(self, field_id):
        """ Used by Central Engine. """
        res =  self.xmlDict.xpath('twister_user_defined/field_section/field[@ID="%s"]' % field_id)
        if not res:
            print('DBParser: Cannot find field ID `%s`!' % field_id)
            return False

        query = res[0].get('SQLQuery')
        return query


    def getQueries(self):
        """ Used by Central Engine. """
        return [q.text for q in self.xmlDict.xpath('twister_user_defined/insert_section/sql_statement')]

# --------------------------------------------------------------------------------------------------
#           USED BY WEB SERVER - REPORTS
# --------------------------------------------------------------------------------------------------

    def getReportFields(self):
        """ Used by HTTP Server. """
        self.updateConfig()

        fields = self.xmlDict.xpath('twister_user_defined/reports_section/field')

        if not fields:
            print('DBParser: Cannot load the reports fields section!')
            return {}

        res = OrderedDict()

        for field in fields:
            d = {}
            d['id']       = field.get('ID', '')
            d['type']     = field.get('Type', '')
            d['label']    = field.get('Label', d['id'])
            d['sqlquery'] = field.get('SQLQuery', '')
            res[d['id']]  = d

        return res


    def getReports(self):
        """ Used by HTTP Server. """
        self.updateConfig()

        reports = self.xmlDict.xpath('twister_user_defined/reports_section/report')

        if not reports:
            print('DBParser: Cannot load the database reports section!')
            return {}

        res = OrderedDict()

        for report in reports:
            d = {}
            d['id']       = report.get('ID', '')
            d['type']     = report.get('Type', '')
            d['path']     = report.get('Path', '')
            d['sqlquery'] = report.get('SQLQuery', '')
            d['sqltotal'] = report.get('SQLTotal', '')   # SQL Total Query
            d['sqlcompr'] = report.get('SQLCompare', '') # SQL Query Compare side by side
            res[d['id']]  = d

        return res


    def getRedirects(self):
        """ Used by HTTP Server. """
        self.updateConfig()

        redirects = self.xmlDict.xpath('twister_user_defined/reports_section/redirect')

        if not redirects:
            print('DBParser: Cannot load the database redirects section!')
            return {}

        res = OrderedDict()

        for redirect in redirects:
            d = {}
            d['id']       = redirect.get('ID', '')
            d['path']     = redirect.get('Path', '')
            res[d['id']]  = d

        return res


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # Plugins XML parser
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


class PluginParser:
    """
    Requirements: LXML.
    This parser will read Plugins.xml.
    """

    def __init__(self, user):

        if not os.path.exists('{0}/twister'.format(userHome(user))):
            raise Exception('PluginParser ERROR: Cannot find Twister for user `%s` !' % user)
        config_data = '{0}/twister/config/plugins.xml'.format(userHome(user))
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

        if self.configHash != newConfigHash:
            self.configHash = newConfigHash

            try:
                self.xmlDict = etree.fromstring(config_data)
            except:
                logError('PluginParser ERROR: Cannot access plugins XML data!')
                return False

            for plugin in self.xmlDict.xpath('Plugin'):

                if (not plugin.xpath('name/text()')) or (not plugin.xpath('pyfile')) or (not plugin.xpath('jarfile')):
                    logError('PluginParser ERROR: Invalid plugin: `%s`!' % str(plugin))
                    continue
                name = plugin.xpath('name')[0].text

                prop_keys = plugin.xpath('property/propname')
                prop_vals = plugin.xpath('property/propvalue')
                res = dict(zip([k.text for k in prop_keys], [v.text for v in prop_vals])) # Pack Key + Value

                self.p_config[name] = res
                self.p_config[name]['jarfile'] = plugin.xpath('jarfile')[0].text
                self.p_config[name]['pyfile']  = plugin.xpath('pyfile')[0].text
                self.p_config[name]['status']  = plugin.xpath('status')[0].text


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
                logError('PluginParser ERROR: Unhandled exception in plugin file `{0}`! Exception: {1}!'.format(mod, e))
                continue

            if not plug:
                logError('PluginParser ERROR: Plugin `%s` cannot be Null!' % plug)
                continue
            # Check plugin parent. Must be Base Plugin.
            if not issubclass(plug, Base):
                logError('PluginParser ERROR: Plugin `%s` must be inherited from Base Plugin!' % plug)
                continue

            # Append plugin classes to plugins list
            d = self.p_config[name]
            d['plugin'] = plug
            plugins[name] = d

        return plugins


# Eof()
