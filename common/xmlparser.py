
# File: xmlparser.py ; This file is part of Twister.

# version: 3.039

# Copyright (C) 2012-2014 , Luxoft

# Authors:
#    Andrei Costachi <acostachi@luxoft.com>
#    Cristi Constantin <crconstantin@luxoft.com>
#    Daniel Cioata <dcioata@luxoft.com>
#    Mihai Tudoran <mtudoran@luxoft.com>

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
Parser for xml configuration files
"""
import os
import sys
import hashlib

from collections import OrderedDict

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print 'TWISTER_PATH environment variable is not set! Exiting!'
    exit(1)
sys.path.append(TWISTER_PATH)

from lxml import etree
from ConfigParser import SafeConfigParser
from plugins import BasePlugin

from common.helpers import userHome
from common.tsclogging import logDebug, logFull, logWarning, logInfo, logError
from common.suitesmanager import SuitesManager
from common.constants import FWMCONFIG_TAGS, PROJECTCONFIG_TAGS
from common.constants import SUITES_TAGS, TESTS_TAGS
from server.CeFs import LocalFS

parser = etree.XMLParser(ns_clean=True, remove_blank_text=True)
etree.set_default_parser(parser)

localFs = LocalFS() # Singleton

__all__ = ['TSCParser', 'DBParser', 'PluginParser', 'ClearCaseParser']


# # #   Helpers   # # #


def parseXML(user, fname):
    """
    Read 1 XML file via remote client and parse the content.
    """
    data = localFs.read_user_file(user, fname)
    try:
        return etree.fromstring(data)
    except Exception as e:
        logError('Error parsing file `{}`, for user `{}`: `{}`!'.format(fname, user, e))
        return None

def dumpXML(user, fname, tree):
    """
    Write 1 XML file via remote client.
    """
    data = etree.tostring(tree, pretty_print=True)
    try:
        return localFs.write_user_file(user, fname, data)
    except Exception as e:
        logError('Error dumping XML into file `{}`, for user `{}`: `{}`!'.format(fname, user, e))
        return None


# # #   Main  Parser   # # #


class TSCParser(object):
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

        self.user = user
        self.user_home = userHome(user)

        if os.path.isfile(base_config):
            base_config = localFs.read_user_file(user, base_config)
        elif base_config and (type(base_config) == type('') or type(base_config) == type(u'')) \
            and (base_config[0] == '<' and base_config[-1] == '>'):
            pass
        else:
            raise Exception('Parser ERROR: Invalid config data : `{}`!'.format(base_config))

        try:
            self.xmlDict = etree.fromstring(base_config)
        except Exception as e:
            raise Exception('Parser ERROR: Cannot access XML config! `{}`'.format(e))


        self.configTS = None
        self.configHash = None
        self.project_globals = {}
        self.files_config = ''

        self.updateConfigTS(files_config)
        self.updateProjectGlobals()


    def updateConfigTS(self, files_config=''):
        """
        Updates Test Suite Cofig file hash and recreates internal XML structure,
        only if the XML file is changed.
        The file number and suite number have to be unique.
        """

        if files_config and (type(files_config) == type('') or type(files_config) == type(u'')) \
                and (files_config[0] == '<' and files_config[-1] == '>'):

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
                logError('User {}: Parser: Test-Suites XML file `{}` does '\
                'not exist! Please check framework config XML file!'.format(self.user, files_config))
                self.configTS = None
                return -1
            else:
                config_ts = localFs.read_user_file(self.user, files_config)

            # Hash check the XML file, to see if is changed
            newConfigHash = hashlib.md5(config_ts).hexdigest()

        if self.configHash != newConfigHash:
            logDebug('User {}: Parser: Test-Suites XML file changed, '\
            'rebuilding internal structure...\n'.format(self.user))
            # Use the new hash
            self.configHash = newConfigHash
            # Create XML Soup from the new XML file
            try:
                self.configTS = etree.fromstring(config_ts)
            except Exception:
                logError('User {}: Parser ERROR: Cannot access Test-Suites XML data!'.format(self.user))
                self.configTS = None
                return -1

        self.files_config = files_config


    def updateProjectGlobals(self):
        """
        Returns the values of many global tags, from FWM and Test-Suites XML.
        """
        logFull('xmlparser:updateProjectGlobals')
        if self.configTS is None:
            logError('User {}: Parser: Cannot get project globals, because'\
            ' Test-Suites XML is invalid!'.format(self.user))
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
            logError('User {}: Parser ERROR: Cannot get active EPs, because' \
            ' Test-Suites XML is invalid!'.format(self.user))
            return []

        activeEPs = []

        for epname in self.configTS.xpath('//EpId/text()'):
            ep = str(epname).strip()
            # Ignore the empty EP names
            if not ep:
                continue
            # Don't add EP twice
            if ep in activeEPs:
                continue
            activeEPs.append(ep)

        return activeEPs


    def list_settings(self, xmlFile, xFilter=''):
        """
        High level function for listing all settings from a Twister XML config file.
        """
        logFull('xmlparser:list_settings')
        if not os.path.isfile(xmlFile):
            logError('User {}: Parse settings error! File path `{}` does not exist!'.format(self.user, xmlFile))
            return False
        xmlSoup = parseXML(self.user, xmlFile)
        if xmlSoup is None:
            return []
        if xFilter:
            return [x.tag for x in xmlSoup.xpath('//*') if xFilter in x.tag]
        else:
            return [x.tag for x in xmlSoup.xpath('//*')]


    def get_settings_value(self, xmlFile, key):
        """
        High level function for getting a value from a Twister XML config file.
        """
        logFull('xmlparser:get_settings_value')
        if not os.path.isfile(xmlFile):
            logError('User {}: Parse settings error! File path `{}` does not exist!'.format(self.user, xmlFile))
            return False
        if not key:
            return False
        else:
            key = str(key)
        xmlSoup = parseXML(self.user, xmlFile)
        if xmlSoup is None:
            return False
        if xmlSoup.xpath(key):
            txt = xmlSoup.xpath(key)[0].text
            return txt or ''
        else:
            return False


    def set_settings_value(self, xmlFile, key, value):
        """
        High level function for setting a value in a Twister XML config file.
        """
        logFull('xmlparser:set_settings_value')
        if not os.path.isfile(xmlFile):
            logError('User {}: Parse settings error! File path `{}` does not exist!'.format(self.user, xmlFile))
            return False
        if not key:
            return False
        else:
            key = str(key)
        if not value:
            value = ''
        else:
            value = str(value)

        xmlSoup = parseXML(self.user, xmlFile)
        if xmlSoup is None:
            return False
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

        return dumpXML(self.user, xmlFile, xmlSoup)


    def del_settings_key(self, xmlFile, key, index=0):
        """
        High level function for deleting a value from a Twister XML config file.
        If the `index` is specified and the `key` returns more values, only the
        index-th value is deleted; unless the `index` is -1, in this case, all
        values are deleted.
        """
        logFull('xmlparser:del_settings_key')
        if not os.path.isfile(xmlFile):
            logError('User {}: Parse settings error! File path `{}` does not exist!'.format(self.user, xmlFile))
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

        xmlSoup = parseXML(self.user, xmlFile)
        if xmlSoup is None:
            return False
        xml_key = xmlSoup.xpath(key)

        if xml_key is None:
            return False

        # For index -1, delete all matches
        if index == -1:
            for xml_v in xml_key:
                xml_parent = xml_v.getparent()
                xml_parent.remove(xml_v)
        else:
            # Use the index-th occurence, or, if the index is wrong, exit
            try:
                xml_key = xml_key[index]
            except Exception:
                return False

            xml_parent = xml_key.getparent()
            xml_parent.remove(xml_key)

        return dumpXML(self.user, xmlFile, xmlSoup)


    def set_persistent_suite(self, xmlFile, suite, info={}, order=-1):
        """
        This function writes in TestSuites.XML file.
        """
        logFull('xmlparser:set_persistent_suite')
        if not os.path.isfile(xmlFile):
            logError('User {}: Parse settings error! File path `{}` does not exist!'.format(self.user, xmlFile))
            return False
        if not suite:
            return False
        else:
            suite = str(suite)
        try:
            order = int(order)
        except Exception:
            return False

        # Root element from Project XML
        xmlSoup = parseXML(self.user, xmlFile)
        if xmlSoup is None:
            return False

        suites_index = [xmlSoup.index(s) for s in xmlSoup.xpath('/Root/TestSuite')]

        if order == 0:
            # Add before the first suite
            insert_pos = 2
        elif abs(order) > len(suites_index):
            # If the negative pos is bigger than the index, add before the first suite
            insert_pos = 2
        elif order > len(suites_index):
            # Add after the last suite
            if not suites_index:
                insert_pos = 2
            else:
                insert_pos = suites_index[-1] + 1
        else:
            # If another position, add there
            if order > 0:
                order -= 1
            if not suites_index:
                insert_pos = 2
            else:
                insert_pos = suites_index[order] + 1

        # Suite XML object
        suite_xml = etree.Element('TestSuite')
        tsName = etree.SubElement(suite_xml, 'tsName')
        tsName.text = suite
        epName = etree.SubElement(suite_xml, 'EpId')
        epName.text = info.get('ep', ' ')
        try:
            del info['ep']
        except Exception:
            pass
        sutName = etree.SubElement(suite_xml, 'SutName')
        sutName.text = info.get('sut', ' ')
        try:
            del info['sut']
        except Exception:
            pass

        for k, v in info.iteritems():
            tag = etree.SubElement(suite_xml, 'UserDefined')
            prop = etree.SubElement(tag, 'propName')
            prop.text = str(k)
            val = etree.SubElement(tag, 'propValue')
            val.text = str(v)

        # Insert the new suite and save
        xmlSoup.insert(insert_pos, suite_xml)

        return dumpXML(self.user, xmlFile, xmlSoup)


    def set_persistent_file(self, xmlFile, suite, fname, info={}, order=-1):
        """
        This function writes in TestSuites.XML file.
        """
        logFull('xmlparser:set_persistent_file')
        if not os.path.isfile(xmlFile):
            logError('User {}: Parse settings error! File path `{}` does not exist!'.format(self.user, xmlFile))
            return False
        if not suite:
            return False
        else:
            suite = str(suite)
        if not fname:
            return False
        else:
            fname = str(fname)
        try:
            order = int(order)
        except Exception:
            return False

        # Root element from Project XML
        xmlSoup = parseXML(self.user, xmlFile)
        if xmlSoup is None:
            return False

        suite_xml = xmlSoup.xpath('/Root/TestSuite[tsName="{0}"]'.format(suite))
        if not suite_xml:
            return False
        else:
            suite_xml = suite_xml[0]

        files_index = [suite_xml.index(s) for s in \
            suite_xml.xpath('/Root/TestSuite[tsName="{0}"]/TestCase'.format(suite))]

        if order == 0:
            # Add before the first file
            insert_pos = 2
        elif abs(order) > len(files_index):
            # If the negative pos is bigger than the index, add before the first file
            insert_pos = 2
        elif order > len(files_index):
            # Add after the last file
            if not files_index:
                insert_pos = 2
            else:
                insert_pos = files_index[-1] + 1
        else:
            # If another position, add there
            if order > 0:
                order -= 1
            if not files_index:
                insert_pos = 2
            else: insert_pos = files_index[order] + 1

        # File XML object
        file_xml = etree.Element('TestCase')
        tcName = etree.SubElement(file_xml, 'tcName')
        tcName.text = fname

        for k, v in info.iteritems():
            tag = etree.SubElement(file_xml, 'Property')
            prop = etree.SubElement(tag, 'propName')
            prop.text = str(k)
            val = etree.SubElement(tag, 'propValue')
            val.text = str(v)

        # Insert the new file and save
        suite_xml.insert(insert_pos, file_xml)

        return dumpXML(self.user, xmlFile, xmlSoup)


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
        return [self._fixLogType(log.tag) for log in self.xmlDict.xpath('LogFiles/*')]


    def getLogFileForType(self, logType):
        """
        Returns the path for one type of log.
        CE will use this path to write the log received from EP.
        """
        logFull('xmlparser:getLogFileForType')
        logs_path = self.project_globals['logs_path']

        if not logs_path:
            logError('User {}: Parser: Logs path is not defined! Please ' \
            'check framework config XML file!'.format(self.user))
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
            logError('User {}: Parser: E-mail Config file `{}` does not exist!'.format(self.user, eml_file))
            return {}

        econfig = parseXML(self.user, eml_file)
        if econfig is None:
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


    def get_binding(self, fpath):
        """
        Read a binding between a CFG and a SUT.
        The result is XML.
        """
        logFull('xmlparser:get_binding')
        cfg_file = '{}/twister/config/bindings.xml'.format(userHome(self.user))

        if not os.path.isfile(cfg_file):
            err = '*ERROR* Bindings Config file `{}`, for user `{}` does not exist!'.format(cfg_file, self.user)
            logError(err)
            return err

        bind_xml = parseXML(self.user, cfg_file)
        if bind_xml is None:
            err = '*ERROR* Config file `{}`, for user `{}` cannot be parsed!'.format(cfg_file, self.user)
            return err
        # Find the old binding
        found = bind_xml.xpath('/root/binding/name[text()="{}"]/..'.format(fpath))

        if found:
            xml_string = etree.tostring(found[0])
            return xml_string.replace('binding>', 'root>')
        else:
            logWarning('*ERROR* Cannot find binding name `{}` for user {}!'.format(fpath, self.user))
            return False


    def set_binding(self, fpath, content):
        """
        Write a binding between a CFG and a SUT.
        Return True/ False.
        """
        logFull('xmlparser:set_binding')
        cfg_file = '{}/twister/config/bindings.xml'.format(userHome(self.user))

        if not os.path.isfile(cfg_file):
            err = '*ERROR* Bindings Config file `{}`, for user `{}` does not exist!'.format(cfg_file, self.user)
            logError(err)
            return err

        bind_xml = parseXML(self.user, cfg_file)
        if bind_xml is None:
            err = '*ERROR* Config file `{}`, for user `{}` cannot be parsed!'.format(cfg_file, self.user)
            return err
        # Find the old binding
        found = bind_xml.xpath('/root/binding/name[text()="{}"]/..'.format(fpath))

        # If found, use it
        if found:
            found = found[0]
            found.clear()
        # Or create it
        else:
            found = etree.SubElement(bind_xml, 'binding')

        name = etree.SubElement(found, 'name')
        name.text = fpath

        try:
            replace_xml = etree.fromstring(content, parser)
        except Exception:
            err = '*ERROR* Invalid XML content, user {}! Cannot parse!'.format(self.user)
            logWarning(err)
            return err

        for elem in replace_xml:
            found.append(elem)

        # Beautify XML ?
        return etree.tostring(bind_xml, pretty_print=True)


    def del_binding(self, fpath):
        """
        Delete a binding between a CFG and a SUT.
        Return True/ False.
        """
        logFull('xmlparser:del_binding')
        cfg_file = '{}/twister/config/bindings.xml'.format(userHome(self.user))

        if not os.path.isfile(cfg_file):
            err = '*ERROR* Bindings Config file `{}`, for user `{}` does not exist!'.format(cfg_file, self.user)
            logError(err)
            return err

        bind_xml = parseXML(self.user, cfg_file)
        if bind_xml is None:
            err = '*ERROR* Config file `{}`, for user `{}` cannot be parsed!'.format(cfg_file, self.user)
            return err
        # Find the binding
        found = bind_xml.xpath('/root/binding/name[text()="{}"]/..'.format(fpath))

        # If found, delete it
        if found:
            bind_xml.remove(found[0])
            logDebug('Removed binding `{}`, for user `{}`.'.format(fpath, self.user))
        else:
            err = '*WARN* Invalid binding `{}`, user `{}`! Cannot unbind!'.format(fpath, self.user)
            # logDebug(err)
            return False

        return dumpXML(self.user, cfg_file, bind_xml)


    def getBindingsConfig(self):
        """
        Parse the bindings file that connects Roots from a config file, with SUTs.
        """
        logFull('xmlparser:getBindingsConfig')
        cfg_file = '{}/twister/config/bindings.xml'.format(userHome(self.user))
        bindings = {}

        if not os.path.isfile(cfg_file):
            err = '*ERROR* Bindings Config file `{}`, for user `{}` does not exist!'.format(cfg_file, self.user)
            logError(err)
            return err

        bind_xml = parseXML(self.user, cfg_file)
        if bind_xml is None:
            err = '*ERROR* Config file `{}`, for user `{}` cannot be parsed!'.format(cfg_file, self.user)
            return err

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


    def _suites_info(self, xml_object, children, epName):
        """
        Create recursive list of folders and files from Tests path.
        """
        if (xml_object is None) or (not epName):
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
        # The first parameter is the Suite name
        if suite_soup.getparent().xpath('id'):
            res['suite'] = suite_soup.getparent().xpath('id')[0].text
        else:
            res['suite'] = ''

        # Add properties from PROJECT
        prop_keys = self.configTS.xpath('/Root/UserDefined/propName')
        prop_vals = self.configTS.xpath('/Root/UserDefined/propValue')
        res.update(dict(zip([k.text for k in prop_keys], [v.text for v in prop_vals])))

        # Add property/ value tags from Suite
        prop_keys = suite_soup.xpath('UserDefined/propName')
        prop_vals = suite_soup.xpath('UserDefined/propValue')
        res.update(dict(zip([k.text for k in prop_keys], [v.text for v in prop_vals])))

        res['type'] = 'suite'
        # Get Suite ID from testsuites.xml
        res['id'] = suite_soup.xpath('ID')[0].text
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
        # Get File ID from testsuites.xml
        res['id'] = file_soup.xpath('ID')[0].text
        # The second parameter is the Suite name
        res['suite'] = file_soup.getparent().xpath('id')[0].text

        # Parse all known File Tags
        for tag_dict in TESTS_TAGS:
            # Create default entry
            res[tag_dict['name']] = tag_dict['default']
            # Exception for config files
            if tag_dict['name'] == '_cfg_files':
                cfg_files = []
                for cfg_soup in file_soup.xpath(tag_dict['tag']):
                    if cfg_soup.get('enabled').lower() == 'true':
                        cfg = {
                            'name': cfg_soup.get('name'),
                            'iter_default': cfg_soup.get('iterator_default'),
                            'iter_sof': cfg_soup.get('iterator_sof')
                        }
                        cfg_files.append(cfg)
                if cfg_files:
                    res[tag_dict['name']] = cfg_files
            # Update value from XML
            elif file_soup.xpath(tag_dict['tag'] + '/text()'):
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


# # #   Database Parser   # # #


class DBParser(object):
    """
    Requirements: LXML.
    This parser will parse DB.xml and Shared_DB.xml.
    """

    def __init__(self, user, config_data, shared_data=None, use_shared_db=True):

        self.user = user
        self.db_config = {}
        self.config_data = config_data
        self.user_xml = None
        self.shared_xml = None
        self.use_shared_db = use_shared_db

        if os.path.isfile(config_data):
            data = localFs.read_user_file(self.user, config_data)
            try:
                self.user_xml = etree.fromstring(data)
                # logDebug('User `{}` loaded priv DB config from file `{}`.'.format(user, config_data))
            except Exception:
                raise Exception('Invalid DB config file `{}`, '\
                    'for user `{}`!'.format(config_data, self.user))
        elif config_data and isinstance(config_data, str) or isinstance(config_data, unicode):
            try:
                self.user_xml = etree.fromstring(config_data)
                # logDebug('User `{}` loaded priv DB config from a string.'.format(user))
            except Exception:
                raise Exception('Cannot parse DB config data, for user `{}`!'.format(self.user))
        else:
            raise Exception('Invalid config data type: `{}`, '\
                'for user `{}`!'.format(type(config_data), self.user))

        if shared_data:
            if os.path.isfile(shared_data):
                data = localFs.read_user_file(self.user, shared_data)
                try:
                    self.shared_xml = etree.fromstring(data)
                    # logDebug('User `{}` loaded shared DB config from file `{}`.'.format(user, shared_data))
                except Exception:
                    raise Exception('Invalid shared DB config file `{}`, '\
                        'for user `{}`!'.format(shared_data, self.user))
            elif shared_data and isinstance(shared_data, str) or isinstance(shared_data, unicode):
                try:
                    self.shared_xml = etree.fromstring(shared_data)
                    # logDebug('User `{}` loaded shared DB config from a string.'.format(user))
                except Exception:
                    logWarning('Cannot parse shared DB config data, for user `{}`!'.format(self.user))
            else:
                raise Exception('Invalid shared config data type: `{}`, '\
                    'for user `{}`!'.format(type(shared_data), self.user))

        # The servers list is used to know how to connect to a specific server name
        self.db_config['servers'] = {}

        if self.user_xml.xpath('db_config/server/text()') and self.user_xml.xpath('db_config/database/text()'):
            # User's server and database
            db_server = self.user_xml.xpath('db_config/server')[0].text
            db_name = self.user_xml.xpath('db_config/database')[0].text
            db_user = self.user_xml.xpath('db_config/user')[0].text
            db_passwd = self.user_xml.xpath('db_config/password')[0].text
            self.db_config['default_server'] = (db_server, db_name, db_user, db_passwd, 'U')
            self.db_config['servers']['User'] = self.db_config['default_server']
        else:
            raise Exception('Invalid DB config, no server and DB, for user `{}`!'.format(self.user))

        if shared_data and self.shared_xml is not None:
            # Servers list
            try:
                db_server = self.shared_xml.xpath('db_config/server')[0].text
                db_name = self.shared_xml.xpath('db_config/database')[0].text
                db_user = self.shared_xml.xpath('db_config/user')[0].text
                db_passwd = self.shared_xml.xpath('db_config/password')[0].text
                self.db_config['servers']['Shared'] = (db_server, db_name, db_user, db_passwd, 'S')
            except Exception as err:
                logWarning('Invalid shared DB XML, for user `{}`: {}!'.format(self.user, err))
                self.shared_xml = None


    def get_inserts(self, db_cfg_role=True):
        """
        Used by Database Manager.
        Returns a list with all insert fields and queries.
        """
        logFull('dbparser:get_inserts')
        insert_queries = OrderedDict()

        # If user has the roles and Use Shared DB is disabled (user DB enabled)
        if db_cfg_role and not self.use_shared_db:
            # Fields and Inserts from private db.xml
            private_db = {}
            private_db['inserts'] = [q.text for q in self.user_xml.xpath('insert_section/sql_statement')]
            fields = OrderedDict()

            for field in self.user_xml.xpath('insert_section/field'):
                data = {}
                data['id'] = field.get('ID', '')
                data['type'] = field.get('Type', '')
                data['query'] = field.get('SQLQuery', '')
                data['level'] = field.get('Level', '') # Project / Suite / Testcase
                fields[data['id']] = data

            private_db['fields'] = fields
            private_db['shared_db'] = False
            # Add private db to inserts
            db_pair = self.db_config['default_server']
            insert_queries[db_pair] = private_db
            # Return after user db inserts !
            return insert_queries

        if self.shared_xml is None:
            logWarning('Invalid shared DB XML on get inserts, for user `{}`!'.format(self.user))
            return insert_queries

        # Invalid entry ?
        if not self.shared_xml.xpath('db_config/server/text()') or \
            not self.shared_xml.xpath('db_config/database/text()'):
            logWarning('Invalid shared DB XML on get inserts, for user `{}`!'.format(self.user))
            return insert_queries

        # Important MySQL server info
        db_server = self.shared_xml.xpath('db_config/server')[0].text
        db_name = self.shared_xml.xpath('db_config/database')[0].text
        db_user = self.shared_xml.xpath('db_config/user')[0].text
        db_passwd = self.shared_xml.xpath('db_config/password')[0].text
        db_pair = (db_server, db_name, db_user, db_passwd, 'S')

        # Insert fields
        fields = OrderedDict()
        for field in self.shared_xml.xpath('insert_section/field'):
            data = {}
            data['id'] = field.get('ID', '')
            data['type'] = field.get('Type', '')
            data['query'] = field.get('SQLQuery', '')
            data['level'] = field.get('Level', '') # Project / Suite / Testcase
            fields[data['id']] = data
        # Insert queries
        inserts = []
        for elem in self.shared_xml.xpath('insert_section/sql_statement'):
            inserts.append(elem.text.strip())
        # Save this info
        insert_queries[db_pair] = {
            'inserts': inserts,
            'fields': fields,
            'shared_db': True
        }
        # Return after shared db inserts !
        return insert_queries


    def get_query(self, field_id):
        """
        Used by the applet.
        """
        logFull('dbparser:get_query')
        res = self.user_xml.xpath('insert_section/field[@ID="%s"]' % field_id)
        if not res:
            logWarning('User {}: Cannot find field ID `{}`!'.format(self.user, field_id))
            return False

        query = res[0].get('SQLQuery')
        return query


    def get_reports(self, db_cfg_role=True):
        """
        Used by Reporting Server.
        Returns a list with all report fields and queries.
        """
        logFull('dbparser:get_reports')
        report_queries = OrderedDict()

        def get_fields(server_data, srv_name):
            """
            All report fields.
            """
            fields = OrderedDict()
            for field in server_data.xpath('reports_section/field'):
                data = {}
                data['id'] = field.get('ID', '')
                data['type'] = field.get('Type', '')
                data['label'] = field.get('Label', data['id'])
                data['sqlquery'] = field.get('SQLQuery', '')
                data['srv_name'] = srv_name
                fields[data['id']] = data
            return fields

        def get_reps(server_data, srv_name):
            """
            All reports.
            """
            reports = OrderedDict()
            for report in server_data.xpath('reports_section/report'):
                data = {}
                data['id'] = report.get('ID', '')
                data['type'] = report.get('Type', '')
                data['path'] = report.get('Path', '')
                data['folder'] = report.get('Folder', '')
                data['sqlquery'] = report.get('SQLQuery', '')
                data['sqltotal'] = report.get('SQLTotal', '')   # SQL Total Query
                data['sqlcompr'] = report.get('SQLCompare', '') # SQL Query Compare side by side
                data['srv_name'] = srv_name # Save server name here
                reports[data['id']] = data
            return reports

        def get_redirects(server_data, srv_name):
            """
            All redirects.
            """
            redirects = OrderedDict()
            for redirect in server_data.xpath('reports_section/redirect'):
                data = {}
                data['id'] = redirect.get('ID', '')
                data['path'] = redirect.get('Path', '')
                data['srv_name'] = srv_name
                redirects[data['id']] = data
            return redirects

        # If the user has the roles AND Use Shared DB is disabled (user DB enabled)
        if db_cfg_role and not self.use_shared_db:
            # Insert user DB first and shared DB second
            db_pair = self.db_config['default_server']
            # Reports and Redirects from private db.xml
            report_queries[db_pair] = {
                'fields': get_fields(self.user_xml, 'User'),
                'reports': get_reps(self.user_xml, 'User'),
                'redirects': get_redirects(self.user_xml, 'User')
            }
        if not self.use_shared_db and not db_cfg_role:
            logInfo('Insufficient privileges to get user reports, for user `{}`!'.format(self.user))

        # Valid shared db.xml
        if self.shared_xml is None:
            logWarning('Invalid shared DB XML on get reports, for user `{}`!'.format(self.user))
            return report_queries

        # Invalid entry ?
        if not self.shared_xml.xpath('db_config/server/text()') or \
            not self.shared_xml.xpath('db_config/database/text()'):
            logWarning('Invalid shared DB XML on get reports, for user `{}`!'.format(self.user))
            return report_queries

        # Important MySQL server info
        db_server = self.shared_xml.xpath('db_config/server')[0].text
        db_name = self.shared_xml.xpath('db_config/database')[0].text
        db_user = self.shared_xml.xpath('db_config/user')[0].text
        db_passwd = self.shared_xml.xpath('db_config/password')[0].text
        db_pair = (db_server, db_name, db_user, db_passwd, 'S')
        # Overwrite all private fields, reports or redirects
        if db_pair in report_queries:
            report_queries[db_pair]['fields'].update(get_fields(self.shared_xml, 'Shared'))
            report_queries[db_pair]['reports'].update(get_reps(self.shared_xml, 'Shared'))
            report_queries[db_pair]['redirects'].update(get_redirects(self.shared_xml, 'Shared'))
        # Save this info
        else:
            report_queries[db_pair] = {
                'fields': get_fields(self.shared_xml, 'Shared'),
                'reports': get_reps(self.shared_xml, 'Shared'),
                'redirects': get_redirects(self.shared_xml, 'Shared')
            }
        # Return after shared db inserts !
        # import pprint ; pprint.pprint(dict(report_queries), width=40)
        return report_queries


# # #   Plugins   # # #


class PluginParser(object):
    """
    Requirements: LXML.
    This parser will read user's Plugins.xml.
    """

    def __init__(self, user):

        self.user = user
        user_home = userHome(user)

        if not os.path.isdir('{}/twister'.format(user_home)):
            raise Exception('PluginParser: Cannot find Twister for user `{}`, '\
                'in path `{}/twister`!'.format(user, user_home))

        config_data = '{}/twister/config/plugins.xml'.format(user_home)
        if not os.path.isfile(config_data):
            raise Exception('PluginParser: Cannot find Plugins for user `{}`, '\
                'in path `{}/twister/config`!'.format(user, user_home))

        # Read directly from CE
        xml_data = localFs.read_system_file(config_data)
        self.config = OrderedDict()

        try:
            self.xmlTree = etree.fromstring(xml_data)
        except Exception:
            raise Exception('PluginParser: Cannot access plugins XML data!')

        for plugin in self.xmlTree.xpath('Plugin'):

            if not (plugin.xpath('name/text()') and plugin.xpath('pyfile') and plugin.xpath('jarfile')):
                logWarning('User {}: PluginParser: Invalid config for plugin: `{}`!'.format(self.user, plugin))
                continue

            prop_keys = plugin.xpath('property/propname')
            prop_vals = plugin.xpath('property/propvalue')
            res = dict(zip([k.text for k in prop_keys], [v.text for v in prop_vals])) # Pack Name + Value

            name = plugin.xpath('name')[0].text

            self.config[name] = res

            self.config[name]['jarfile'] = plugin.xpath('jarfile')[0].text.strip() \
                                             if plugin.xpath('jarfile/text()') else ''
            self.config[name]['pyfile'] = plugin.xpath('pyfile')[0].text.\
            strip() if plugin.xpath('pyfile/text()') else ''

            self.config[name]['status'] = plugin.xpath('status')[0].text.\
            strip() if plugin.xpath('status/text()') else ''


    def getPlugins(self):
        """ Return all plugins info """
        logFull('xmlparser:getPlugins')

        Base = BasePlugin.BasePlugin
        py_modules = [k +'::'+ os.path.splitext(self.config[k]['pyfile'])[0]
                      for k in self.config if self.config[k]['status'] == 'enabled']
        plugins = {}

        for module in py_modules:
            name = module.split('::')[0]
            if not name:
                continue
            mod = module.split('::')[1]
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
                logWarning('User {}: PluginParser ERROR: Unhandled exception' \
                ' in plugin file `{}`! Exception: {}!'.\
                format(self.user, mod, e))
                continue

            if not plug:
                logWarning('User {}: PluginParser ERROR: Plugin `{}` cannot be Null!'.format(self.user, plug))
                continue
            # Check plugin parent. Must be Base Plugin.
            if not issubclass(plug, Base):
                logWarning('User {}: PluginParser ERROR: Plugin `{}` must be' \
                    ' inherited from Base Plugin!'.format(self.user, plug))
                continue

            # Append plugin classes to plugins list
            d = self.config[name]
            d['plugin'] = plug
            plugins[name] = d

        return plugins


# # #   ClearCase   # # #


class ClearCaseParser(object):
    """
    Requirements: LXML.
    This parser will read user's Clearcase.xml.
    """

    def __init__(self, user):

        self.user = user
        user_home = userHome(user)
        self.user_home = user_home
        self.config = {}

        if not os.path.isdir('{}/twister'.format(user_home)):
            raise Exception('ClearCaseParser: Cannot find Twister for user `{}`, '\
                'in path `{}/twister`!'.format(user, user_home))

        config_data = '{}/twister/config/clearcaseconfig.xml'.format(user_home)
        if not os.path.isfile(config_data):
            raise Exception('ClearCaseParser: Cannot find Clearcase XML for user `{}`, '\
                'in path `{}/twister/config`!'.format(user, user_home))

        # Read directly from CE
        xml_data = localFs.read_system_file(config_data)

        try:
            self.xmlTree = etree.fromstring(xml_data)
        except Exception:
            raise Exception('ClearCaseParser: Cannot access Clearcase XML data!')


    def getConfigs(self, filter_tag=None):
        """ Return all ClearCase info. """
        filter_name = False

        # Parse all known FWMCONFIG tags
        for tag_dict in FWMCONFIG_TAGS:
            tag = tag_dict['tag']
            name = tag_dict['name']
            # Filter ?
            if filter_tag and filter_tag != tag:
                continue
            # Found filter ?
            filter_name = name
            xobj = self.xmlTree.xpath('/Root/' + tag)
            # If the tag is active, get the View and the Path
            if len(xobj) >= 1:
                xobj = xobj[0]
                if xobj.get('active') == 'true':
                    path = xobj.get('path')
                    view = xobj.get('view')
                    # actv = xobj.get('activity')
                    self.config[name] = {'path': path, 'view': view, 'actv': ''}

        if filter_tag and filter_name:
            return self.config.get(filter_name, {})
        else:
            return self.config


# Eof()
