
# File: xmlparser.py ; This file is part of Twister.

# version: 3.007

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
from ConfigParser import SafeConfigParser
from plugins import BasePlugin

from common.helpers import *
from common.tsclogging import *
from common.suitesmanager import *
from common.constants import FWMCONFIG_TAGS, PROJECTCONFIG_TAGS
from common.constants import SUITES_TAGS, TESTS_TAGS

__all__ = ['TSCParser', 'DBParser', 'PluginParser']


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


class TSCParser:
    """
    Requirements: LXML.
    This parser reads all client configuration files and returns information like:
    - Test Suite config File
    - Logs Path
    - Reports Path
    - EPs list, active EPs
    - E-mail and Globals config
    """

    def __init__(self, user, base_config='', files_config=''):

        if os.path.isfile(base_config):
            base_config = open(base_config).read()
        elif base_config and ( type(base_config)==type('') or type(base_config)==type(u'') ) \
                and ( base_config[0] == '<' and base_config[-1] == '>' ):
            pass
        else:
            raise Exception('Parser ERROR: Invalid config data : `{}`!'.format(base_config))

        try:
            self.xmlDict = etree.fromstring(base_config)
        except:
            raise Exception('Parser ERROR: Cannot access XML config data!')

        self.user = user
        self.user_home = userHome(user)

        self.configTS = None
        self.configHash = None
        self.project_globals = {}

        self.updateConfigTS(files_config)
        self.updateProjectGlobals()


    def updateConfigTS(self, files_config=''):
        """
        Updates Test Suite Cofig file hash and recreates internal XML structure,
        only if the XML file is changed.
        The file number and suite number have to be unique.
        """
        logFull('xmlparser:updateConfigTS')
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

            if files_config.startswith('~/'):
                files_config = userHome(self.user) + files_config[1:]
            if not os.path.isfile(files_config):
                logError('Parser: Test-Suites XML file `{}` does not exist! Please check framework config XML file!'.format(files_config))
                self.configTS = None
                return -1
            else:
                config_ts = open(files_config).read()

            # Hash check the XML file, to see if is changed
            newConfigHash = hashlib.md5(config_ts).hexdigest()

        if self.configHash != newConfigHash:
            logDebug('Parser: Test-Suites XML file changed, rebuilding internal structure...\n')
            # Use the new hash
            self.configHash = newConfigHash
            # Create XML Soup from the new XML file
            try:
                self.configTS = etree.fromstring(config_ts)
            except:
                logError('Parser ERROR: Cannot access Test-Suites XML data!')
                self.configTS = None
                return -1

        self.files_config = files_config


    def updateProjectGlobals(self):
        """
        Returns the values of many global tags, from FWM and Test-Suites XML.
        """
        logFull('xmlparser:updateProjectGlobals')
        if self.configTS is None:
            logError('Parser: Cannot get project globals, because Test-Suites XML is invalid!')
            return False

        # Reset globals
        self.project_globals = OrderedDict()

        # Parse all known FWMCONFIG tags
        for tag_dict in FWMCONFIG_TAGS:
            # Create default entry
            self.project_globals[tag_dict['name']] = tag_dict['default']
            # Update value from XML
            if self.xmlDict.xpath(tag_dict['tag'] + '/text()'):
                path = self.xmlDict.xpath(tag_dict['tag'])[0].text
                if path[0] == '~':
                    path = self.user_home + path[1:]
                self.project_globals[tag_dict['name']] = path

        # Parse all known PROJECT tags
        for tag_dict in PROJECTCONFIG_TAGS:
            # Create default entry
            self.project_globals[tag_dict['name']] = tag_dict['default']
            # Update value from XML
            if self.configTS.xpath(tag_dict['tag'] + '/text()'):
                # If the variable should be a Boolean
                if tag_dict.get('type') == 'bool':
                    if self.configTS.xpath(tag_dict['tag'] + '/text()')[0].lower() == 'true':
                        value = True
                    else:
                        value = False
                # If the variable should be a Number
                elif tag_dict.get('type') == 'number':
                    value = self.configTS.xpath('round({})'.format(tag_dict['tag']))
                else:
                    value = self.configTS.xpath(tag_dict['tag'])[0].text
                self.project_globals[tag_dict['name']] = value

        return True


    def getActiveEps(self):
        """
        Returns a list with all EPs that appear in Test-Suites XML.
        """
        logFull('xmlparser:getActiveEps')
        if self.configTS is None:
            logError('Parser ERROR: Cannot get active EPs, because Test-Suites XML is invalid!')
            return []

        activeEPs = []
        for epname in self.configTS.xpath('//EpId/text()'):
            activeEPs.append( str(epname) )

        activeEPs = (';'.join(activeEPs)).split(';')
        activeEPs = list(set(activeEPs))
        # Ignore the empty EP names
        activeEPs = [ep.strip() for ep in activeEPs if ep.strip()]
        return activeEPs

# # #

    def listSettings(self, xmlFile, xFilter=''):
        """
        High level function for listing all settings from a Twister XML config file.
        """
        logFull('xmlparser:listSettings')
        if not os.path.isfile(xmlFile):
            logError('Parse settings error! File path `{}` does not exist!'.format(xmlFile))
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
        logFull('xmlparser:getSettingsValue')
        if not os.path.isfile(xmlFile):
            logError('Parse settings error! File path `{}` does not exist!'.format(xmlFile))
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
        logFull('xmlparser:setSettingsValue')
        if not os.path.isfile(xmlFile):
            logError('Parse settings error! File path `{}` does not exist!'.format(xmlFile))
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

        # Else, create it
        else:
            # Try and split the key into parent and node
            if '/' in key:
                parent_path, node_name = '/'.join(key.split('/')[:-1]), key.split('/')[-1]
            else:
                parent_path, node_name = '/', key
            parent = xmlSoup.xpath(parent_path)
            # Invalid parent path ?
            if not parent:
                return False

            # Create the new node
            node = etree.Element(node_name)
            node.text = value
            node.tail = '\n'
            parent[0].insert(-1, node)

        xmlSoup.write(xmlFile, pretty_print=True)
        return True


    def delSettingsKey(self, xmlFile, key, index=0):
        """
        High level function for deleting a value from a Twister XML config file.
        If the `index` is specified and the `key` returns more values, only the
        index-th value is deleted; unless the `index` is -1, in this case, all
        values are deleted.
        """
        logFull('xmlparser:delSettingsKey')
        if not os.path.isfile(xmlFile):
            logError('Parse settings error! File path `{}` does not exist!'.format(xmlFile))
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

        if not len(xml_key):
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

        xmlSoup.write(xmlFile, pretty_print=True)
        return True


    def setPersistentSuite(self, xmlFile, suite, info={}, order=-1):
        """
        This function writes in TestSuites.XML file.
        """
        logFull('xmlparser:setPersistentSuite')
        if not os.path.isfile(xmlFile):
            logError('Parse settings error! File path `{}` does not exist!'.format(xmlFile))
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
        tsName = etree.SubElement(suite_xml, 'tsName')
        tsName.text = suite
        epName = etree.SubElement(suite_xml, 'EpId')
        epName.text = info.get('ep', ' ') ; epName.tail = '\n'
        try: del info['ep']
        except: pass
        sutName = etree.SubElement(suite_xml, 'SutName')
        sutName.text = info.get('sut', ' ') ; sutName.tail = '\n'
        try: del info['sut']
        except: pass

        for k, v in info.iteritems():
            tag = etree.SubElement(suite_xml, 'UserDefined')
            prop = etree.SubElement(tag, 'propName')
            prop.text = str(k)
            val  = etree.SubElement(tag, 'propValue')
            val.text = str(v)

        # Insert the new suite and save
        xml_root.insert(insert_pos, suite_xml)
        xmlSoup.write(xmlFile, pretty_print=True)
        return True


    def setPersistentFile(self, xmlFile, suite, fname, info={}, order=-1):
        """
        This function writes in TestSuites.XML file.
        """
        logFull('xmlparser:setPersistentFile')
        if not os.path.isfile(xmlFile):
            logError('Parse settings error! File path `{}` does not exist!'.format(xmlFile))
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
        xmlSoup.write(xmlFile, pretty_print=True)
        return True

# # #

    def _fixLogType(self, logType):
        """
        Helper function to fix log names.
        """
        logFull('xmlparser:_fixLogType')
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
        logFull('xmlparser:getLogTypes')
        return [ self._fixLogType(log.tag) for log in self.xmlDict.xpath('LogFiles/*')]


    def getLogFileForType(self, logType):
        """
        Returns the path for one type of log.
        CE will use this path to write the log received from EP.
        """
        logFull('xmlparser:getLogFileForType')
        logs_path = self.project_globals['logs_path']

        if not logs_path:
            logError('Parser: Logs path is not defined! Please check framework config XML file!')
            return {}

        logType = self._fixLogType(logType)
        logFile = self.xmlDict.xpath('//{0}/text()'.format(logType))

        if logFile:
            return logs_path + os.sep + logFile[0]
        else:
            return ''


    def getEmailConfig(self, eml_file=''):
        """
        Returns the e-mail configuration.
        After Central Engine stops, an e-mail must be sent to the people interested.
        """
        logFull('xmlparser:getEmailConfig')
        if not eml_file:
            eml_file = self.project_globals['eml_config']

        if not os.path.isfile(eml_file):
            logError('Parser: E-mail Config file `{}` does not exist!'.format(eml_file))
            return {}

        try:
            econfig = etree.parse(eml_file)
        except:
            logError('Parser: Cannot parse e-mail Config file `{}`!'.format(eml_file))
            return {}

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


    def getBinding(self, fpath):
        """
        Read a binding between a CFG and a SUT.
        The result is XML.
        """
        logFull('xmlparser:getBinding')
        cfg_file = '{}/twister/config/bindings.xml'.format(userHome(self.user))

        if not os.path.isfile(cfg_file):
            err = '*ERROR* Bindings Config file `{}` does not exist!'.format(cfg_file)
            logError(err)
            return err

        bind_xml = etree.parse(cfg_file)
        found = bind_xml.xpath('/root/binding/name[text()="{}"]/..'.format(fpath))

        if found:
            xml_string = etree.tostring(found[0])
            return xml_string.replace('binding>', 'root>')
        else:
            logWarning('*ERROR* Cannot find binding name `{}`!'.format(fpath))
            return False


    def setBinding(self, fpath, content):
        """
        Write a binding between a CFG and a SUT.
        Return True/ False.
        """
        logFull('xmlparser:setBinding')
        cfg_file = '{}/twister/config/bindings.xml'.format(userHome(self.user))

        if not os.path.isfile(cfg_file):
            err = '*ERROR* Bindings Config file `{}` does not exist!'.format(cfg_file)
            logError(err)
            return err

        bind_xml = etree.parse(cfg_file)
        # Find the old binding
        found = bind_xml.xpath('/root/binding/name[text()="{}"]/..'.format(fpath))

        # If found, use it
        if found:
            found = found[0]
            found.clear()
        # Or create it
        else:
            found = etree.SubElement(bind_xml.getroot(), 'binding')
            name  = etree.SubElement(found, 'name')
            name.text = fpath

        try:
            replace_xml = etree.XML(content)
        except:
            err = '*ERROR* Invalid XML content! Cannot parse!'
            logWarning(err)
            return err

        for elem in replace_xml:
            found.append(elem)

        bind_xml.write(cfg_file)
        logDebug('Set Binding: Binding `{}` updated in bindings.xml!'.format(fpath))
        return True


    def getBindingsConfig(self):
        """
        Parse the bindings file that connects Roots from a config file, with SUTs.
        """
        logFull('xmlparser:getBindingsConfig')
        cfg_file = '{}/twister/config/bindings.xml'.format(userHome(self.user))
        bindings = {}

        if not os.path.isfile(cfg_file):
            logError('Bindings Config file `{}` does not exist!'.format(cfg_file))
            return {}

        bind_xml = etree.parse(cfg_file)

        for binding in bind_xml.xpath('/root/binding'):
            name = binding.find('name')
            # Valid names ?
            if name is None:
                continue
            name = name.text.strip()
            if not name:
                continue
            bindings[name] = {}
            # All binds cfg -> sut
            for bind in binding.findall('bind'):
                cfg = bind.get('config')
                sut = bind.get('sut')
                bindings[name][cfg] = sut

        logDebug('Found `{}` bindings for user `{}`.'.format(len(bindings), self.user))
        return bindings

# # #

    def _suites_info(self, xml_object, children, epName):
        """
        Create recursive list of folders and files from Tests path.
        """
        if (not len(xml_object)) or (not epName):
            return {}

        # For each testsuite from current xml object
        for obj_xpath in xml_object.xpath('TestSuite[EpId="{}"] | TestCase'.format(epName)):
            # If XML object is suite
            if obj_xpath.tag == 'TestSuite':
                d = self.getSuiteInfo(obj_xpath)
                # Save the suite ID in XML, to be used by the files
                idTag = etree.SubElement(obj_xpath, 'id')
                idTag.text = d['id']
                d['children'] = self._suites_info(obj_xpath, OrderedDict(), epName)
            # If XML object is file, it has not children
            else:
                d = self.getFileInfo(obj_xpath)

            oid = d['id']
            del  d['id'] # Delete the ID tag
            children[oid] = d

        return children


    def getAllSuitesInfo(self, epName):
        """
        Shortcut function.
        """
        logFull('xmlparser:getAllSuitesInfo')
        return self._suites_info(self.configTS, SuitesManager(), epName)


    def getSuiteInfo(self, suite_soup):
        """
        Returns a dict with information about 1 Suite from Test-Suites XML.
        The "suite" must be a XML Soup class.
        """
        logFull('xmlparser:getSuiteInfo')
        # A suite can be a part of only 1 EP !
        res = OrderedDict()

        # Add properties from FWMCONFIG
        prop_keys = self.configTS.xpath('/Root/UserDefined/propName')
        prop_vals = self.configTS.xpath('/Root/UserDefined/propValue')
        res.update( dict(zip( [k.text for k in prop_keys], [v.text for v in prop_vals] )) )

        # Add property/ value tags from Suite
        prop_keys = suite_soup.xpath('UserDefined/propName')
        prop_vals = suite_soup.xpath('UserDefined/propValue')
        res.update( dict(zip( [k.text for k in prop_keys], [v.text for v in prop_vals] )) )

        res['type'] = 'suite'
        self.suite_no += 1
        res['id'] = str(self.suite_no)

        # The first parameter is the EP name
        res['ep'] = suite_soup.xpath('EpId')[0].text

        # Parse all known Suites Tags
        for tag_dict in SUITES_TAGS:
            # Create default entry
            res[tag_dict['name']] = tag_dict['default']
            # Update value from XML
            if suite_soup.xpath(tag_dict['tag'] + '/text()'):
                value = suite_soup.xpath(tag_dict['tag'])[0].text
                if not value.strip():
                    continue
                res[tag_dict['name']] = value

        return res


    def getFileInfo(self, file_soup):
        """
        Returns a dict with information about 1 File from Test-Suites XML.
        The "file" must be a XML class.
        """
        logFull('xmlparser:getFileInfo')
        res = OrderedDict()
        res['type'] = 'file'
        self.file_no += 1
        res['id'] = str(self.file_no)

        # The first parameter is the Suite name
        res['suite'] = file_soup.getparent().xpath('id')[0].text

        # Parse all known File Tags
        for tag_dict in TESTS_TAGS:
            # Create default entry
            res[tag_dict['name']] = tag_dict['default']
            # Update value from XML
            if file_soup.xpath(tag_dict['tag'] + '/text()'):
                value = file_soup.xpath(tag_dict['tag'])[0].text
                if not value.strip():
                    continue
                res[tag_dict['name']] = value

        # Inject this empty variable
        res['twister_tc_revision'] = '-1'

        # Add property/ value tags
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


    def getGlobalParams(self, globs_file=None):
        """
        Returns a dictionary containing All global parameters,
        that will be available for all tests.
        """
        logFull('xmlparser:getGlobalParams')
        # First check, the parameter
        if not globs_file:
            globs_file = self.project_globals['glob_params']
        # Second check, the user config file
        if not globs_file:
            logError('Get Globals: Globals Config file is not defined! Please check framework config XML file!')
            return {}
        if not os.path.isfile(globs_file):
            logError('Get Globals: Globals Config file `{}` does not exist!'.format(globs_file))
            return {}

        params_xml = etree.parse(globs_file)

        def recursive(xml, gparams):
            for folder in xml.xpath('folder'):
                tmp = {gparam.find('name').text: gparam.find('value').text or '' for gparam in folder.xpath('param')}
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

        self.db_config = {}
        self.config_data = config_data
        self.updateConfig()


    def updateConfig(self):
        logFull('xmlparser:updateConfig')

        config_data = self.config_data

        if os.path.isfile(config_data):
            try: self.xmlDict = etree.fromstring(open(config_data).read())
            except: raise Exception('Db Parser: Invalid DB config file `{}`!'.format(config_data))
        elif config_data and type(config_data)==type('') or type(config_data)==type(u''):
            try: self.xmlDict = etree.fromstring(config_data)
            except: raise Exception('Db Parser: Cannot parse DB config file!')
        else:
            raise Exception('Db Parser: Invalid config data type: `{}`!'.format( type(config_data) ))

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

    def getInsertQueries(self):
        """ Used by Central Engine. """
        logFull('xmlparser:getInsertQueries')
        return [q.text for q in self.xmlDict.xpath('insert_section/sql_statement')]


    def getInsertFields(self):
        """
        Used by Central Engine.
        Returns a dictionary with field ID : field info.
        """
        logFull('xmlparser:getInsertFields')
        fields = self.xmlDict.xpath('insert_section/field')

        if not fields:
            logWarning('Db Parser: Cannot load the reports fields section!')
            return {}

        res = OrderedDict()

        for field in fields:
            d = {}
            d['id']    = field.get('ID', '')
            d['type']  = field.get('Type', '')
            d['query'] = field.get('SQLQuery', '')
            res[d['id']]  = d

        return res


    def getQuery(self, field_id):
        """ Used by Central Engine. """
        logFull('xmlparser:getQuery')
        res =  self.xmlDict.xpath('insert_section/field[@ID="%s"]' % field_id)
        if not res:
            logWarning('Db Parser: Cannot find field ID `{}`!'.format(field_id))
            return False

        query = res[0].get('SQLQuery')
        return query

# --------------------------------------------------------------------------------------------------
#           USED BY WEB SERVER - REPORTS
# --------------------------------------------------------------------------------------------------

    def getReportFields(self):
        """ Used by HTTP Server. """
        logFull('xmlparser:getReportFields')
        self.updateConfig()

        fields = self.xmlDict.xpath('reports_section/field')

        if not fields:
            logWarning('Db Parser: Cannot load the reports fields section!')
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
        logFull('xmlparser:getReports')
        """ Used by HTTP Server. """
        self.updateConfig()

        reports = self.xmlDict.xpath('reports_section/report')

        if not reports:
            logWarning('Db Parser: Cannot load the database reports section!')
            return {}

        res = OrderedDict()

        for report in reports:
            d = {}
            d['id']       = report.get('ID', '')
            d['type']     = report.get('Type', '')
            d['path']     = report.get('Path', '')
            d['folder']   = report.get('Folder', '')
            d['sqlquery'] = report.get('SQLQuery', '')
            d['sqltotal'] = report.get('SQLTotal', '')   # SQL Total Query
            d['sqlcompr'] = report.get('SQLCompare', '') # SQL Query Compare side by side
            res[d['id']]  = d

        return res


    def getRedirects(self):
        """ Used by HTTP Server. """
        logFull('xmlparser:getRedirects')
        self.updateConfig()

        redirects = self.xmlDict.xpath('reports_section/redirect')

        if not redirects:
            logWarning('Db Parser: Cannot load the database redirects section!')
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

        user_home = userHome(user)

        if not os.path.exists('{}/twister'.format(user_home)):
            raise Exception('PluginParser ERROR: Cannot find Twister for user `{}`, '\
                'in path `{}/twister`!'.format(user, user_home))

        config_data = '{}/twister/config/plugins.xml'.format(user_home)
        if not os.path.exists(config_data):
            raise Exception('PluginParser ERROR: Cannot find Plugins for user `{}`, '\
                'in path `{}/twister/config`!'.format(user, user_home))

        self.config_data = config_data
        self.configHash = None
        self.p_config = OrderedDict()
        self.updateConfig()


    def updateConfig(self):
        """ Reload all Plugins Xml info """
        logFull('xmlparser:updateConfig')

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
                    logWarning('PluginParser WARN: Invalid config for plugin: `{}`!'.format(plugin))
                    continue
                name = plugin.xpath('name')[0].text

                prop_keys = plugin.xpath('property/propname')
                prop_vals = plugin.xpath('property/propvalue')
                res = dict(zip([k.text for k in prop_keys], [v.text for v in prop_vals])) # Pack Key + Value

                self.p_config[name] = res

                self.p_config[name]['jarfile'] = plugin.xpath('jarfile')[0].text.strip() if plugin.xpath('jarfile/text()') else ''
                self.p_config[name]['pyfile']  = plugin.xpath('pyfile')[0].text.strip()  if plugin.xpath('pyfile/text()') else ''
                self.p_config[name]['status']  = plugin.xpath('status')[0].text.strip()  if plugin.xpath('status/text()') else ''


    def getPlugins(self):
        """ Return all plugins info """
        logFull('xmlparser:getPlugins')

        self.updateConfig()
        Base = BasePlugin.BasePlugin
        py_modules = [k +'::'+ os.path.splitext(self.p_config[k]['pyfile'])[0]
                      for k in self.p_config if self.p_config[k]['status'] == 'enabled']
        plugins = {}

        for module in py_modules:
            name = module.split('::')[0]
            if not name: continue
            mod  = module.split('::')[1]
            if not mod:
                continue
            if not os.path.isfile('{}/plugins/{}.py'.format(TWISTER_PATH, mod)):
                continue
            plug = None
            try:
                # Import the plugin module
                mm = __import__('plugins.' + mod, fromlist=['Plugin'])
                # Reload all data, just in case
                mm = reload(mm)
                plug = mm.Plugin
            except Exception, e:
                logWarning('PluginParser ERROR: Unhandled exception in plugin file `{}`! Exception: {}!'.format(mod, e))
                continue

            if not plug:
                logWarning('PluginParser ERROR: Plugin `{}` cannot be Null!'.format(plug))
                continue
            # Check plugin parent. Must be Base Plugin.
            if not issubclass(plug, Base):
                logWarning('PluginParser ERROR: Plugin `{}` must be inherited from Base Plugin!'.format(plug))
                continue

            # Append plugin classes to plugins list
            d = self.p_config[name]
            d['plugin'] = plug
            plugins[name] = d

        return plugins


# Eof()
