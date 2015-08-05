
# File: CeParser.py ; This file is part of Twister.

# version: 3.018

# Copyright (C) 2012-2014 , Luxoft

# Authors:
#    Mihai Dobre <mihdobre@luxoft.com>
#    Andrei Costachi <acostachi@luxoft.com>
#    Cristi Constantin <crconstantin@luxoft.com>

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''
Module to parse the project file
'''

import os
import re
import copy
import ast
#import json
from binascii import hexlify

from collections import OrderedDict

from common.helpers import userHome
from common.tsclogging import logError, logDebug, logWarning
from lxml import etree

def cartesian(lists):
    """
    Helper function to compute cartesian multiply
    """
    if lists == []:
        return [()]
    return [x + (y,) for x in cartesian(lists[:-1]) for y in lists[-1]]


class CeXmlParser(object):
    """
    Parse and generate project.xml files.
    """

    def __init__(self, project):
        self.project = project


    def _edit_suite(self, ep_id, sut, suite):
        '''
        @param:
            ep_id: the id of the ep
            sut: the name of the sut
            suite: the suite to be edited
        @summary:
            Update suite props with sut name, ep_id
            Delete test cases having running = false.
            Delete the empty suite/subsuite
        '''

        for epname in suite.findall('.//EpId'):
            epname.text = ep_id

        for sut_name in suite.findall('.//SutName'):
            sut_name.text = sut

        # delete tc if running = false
        for prop in suite.findall(".//Property"):
            if prop.find('propName').text == 'Running' and\
            prop.find('propValue').text == 'false':
                grand_parent = (prop.getparent()).getparent()
                grand_parent.remove(prop.getparent())

        # delete empty sub-suites from this suite
        for suite in suite.xpath('//TestSuite'):
            if suite.find('TestSuite') is None and\
            suite.find('TestCase') is None:
                suite_parent = suite.getparent()
                suite_parent.remove(suite)

        return True


    def _resolve_dependencies(self, xml, dependency_dict):
        """
        @param:
            xml: the project/last_edited xml in etree format
            dependency_dict: a dict that stores the link between new and old ids. Old ids are keys.
        @summary:
            Replaces the ids in all Dependency tags with the new and updated ones.
        """
        dependencies = xml.findall('.//Dependency')
        for dependency in dependencies:
            if dependency.text:
                dep_list = dependency.text.split(';')
                new_dep_list = ''
                for dep in dep_list:
                    condition = dep.split(':')[-1]
                    dep_id = dep.split(':')[0]
                    if dep_id in dependency_dict:
                        new_dep_id = [id+':'+condition for id in dependency_dict[dep_id]]
                        new_dep_list += ';'.join(new_dep_id)+';'
                dependency.text = new_dep_list


    def _change_ids(self, xml, repeated_dict):
        '''
        @param:
            xml: the project/last_edited in etree format
            repeated_dict: the dict that storest the link between old and new IDs. Old ids are keys.
        @summary:
            Change IDs for suite/tc. Add them to repeated_dict dictionary to keep track of changes(to be able 
            to resolve dependencies later)
        '''
        suite_no = 100  # Base ID for suites
        file_no = 1000  # Base ID for tests
 
        # Fix long ugly IDs with short integer IDs
        for suite_id in xml.xpath('//TestSuite/ID'):
            suite_no += 1
            if suite_id.text in repeated_dict:
                repeated_dict[suite_id.text].append(str(suite_no))
            else:
                repeated_dict[suite_id.text] = [str(suite_no)]
            suite_id.text = str(suite_no)
  
        # Fix long ugly IDs with short integer IDs
        for file_id in xml.xpath('//TestCase/ID'):
            file_no += 1
            if file_id.text in repeated_dict:
                repeated_dict[file_id.text].append(str(file_no))
            else:
                repeated_dict[file_id.text] = [str(file_no)]
            file_id.text = str(file_no)


    def _get_iterator_values(self, config_file, iterator_default,\
    interval_values, user, part_interval_values=[], default_values_list=[]):
        """
        Calculates all the possible values for iterators for a test
        """
        data = self.project.configs.read_config_file(user, config_file)
        if data.startswith('*ERROR*'):
            logWarning(data)
            return

        # Try to parse the project file
        try:
            xml_config = etree.fromstring(data)
        except:
            msg = "Config file `{}` is invalid!".format(config_file)
            logWarning(msg)
            return

        config_file_st = etree.tostring(xml_config)
        config_file_fst = etree.fromstring(config_file_st)
        # find all entries having tag = iterator
        config_types = config_file_fst.xpath('//type')
        config_types = [x for x in config_types if x.text == 'iterator']

        # Iterators from config file
        for item in config_types:
            prop_iterator = item.getparent()

            # set the parent component(s) of the iterator
            comp_parent = prop_iterator.getparent()
            comp_parent_name = ''
            if comp_parent.find('fname') is not None:
                comp_parent_name = comp_parent.find('fname').text

            # if this is a sub-component, we need to go up to get all parents
            while True:
                comp_parent = comp_parent.getparent()
                if comp_parent is None:
                    # we reached the root; need to break out from this loop
                    break
                comp_fname = comp_parent.find('fname')
                if comp_fname is not None:
                    comp_parent_name = comp_parent.find('fname').text + '/' +\
                    comp_parent_name

            config_name = config_file + '#' + comp_parent_name +\
            '#' + prop_iterator.find('name').text
            values = prop_iterator.find('value').text
            if not values:
                continue

            values_list = values.replace(' ', '').split(',')

            # get the default value
            index_dot = values_list[0].find('..')
            if index_dot > -1:
                try:
                    default_value = ast.literal_eval(values_list[0][:index_dot])
                    default_value = int(default_value)
                except:
                    default_value = values_list[0][:index_dot]
            else:
                try:
                    default_value = ast.literal_eval(values_list[0])
                    default_value = int(default_value)
                except:
                    default_value = values_list[0]

            if iterator_default == 'true':
                part_interval_values.append(['{}={}'.\
                format(config_name, default_value)])
                default_values_list.append('{}={}'.\
                format(config_name, default_value))
            else:
                iter_interval_values = list()
                key_default_value = '{}={}'.format(config_name, default_value)

                for interv in values_list:
                    re_intervals = re.search('(\w*\d*\.?\d+)\.+(\w*\d*\.?\d+)',\
                    interv)
                    try:
                        x_val = ast.literal_eval(re_intervals.group(1))
                        y_val = ast.literal_eval(re_intervals.group(2))
                        range_res = range(int(x_val), int(y_val) + 1)
                        # avoid adding default value again ex: 2, 1...4
                        if default_value in range_res and \
                        key_default_value in iter_interval_values:
                            del range_res[range_res.index(default_value)]
                        for i in range_res:
                            iter_interval_values.append('{}={}'.\
                            format(config_name, i))
                    except:
                        try:
                            x_val = re_intervals.group(1)
                            y_val = re_intervals.group(2)
                            # try to convert to int if possible
                            try:
                                value = int(ast.literal_eval(x_val))
                                iter_interval_values.append('{}={}'.\
                                format(config_name, value))
                            except:
                                iter_interval_values.append('{}={}'.\
                                format(config_name, x_val))
                            try:
                                value = int(ast.literal_eval(y_val))
                                iter_interval_values.append('{}={}'.\
                                format(config_name, value))
                            except:
                                iter_interval_values.append('{}={}'.\
                                format(config_name, y_val))
                        except:
                            try:
                                interv = ast.literal_eval(interv)
                            except:
                                pass
                            # avoid adding default value again ex: 2, 1, 2, 3
                            if default_value != interv or\
                            key_default_value not in iter_interval_values:
                                iter_interval_values.append('{}={}'.\
                                format(config_name, interv))

                part_interval_values.append(iter_interval_values)

            if part_interval_values:
                if config_name in interval_values.keys():
                    interval_values[config_name].extend(part_interval_values)
                else:
                    interval_values[config_name] = part_interval_values


    def _get_cartesian_list(self, user, configs):
        """
        @param:
            user: the authenticated twister user
            configs: the configuration files in xml format
        @return:
            cartesian list of the iterators as list of pairs
        @summary:
            Computes the cartesian list of the iterators 
        """
        interval_values = OrderedDict()
        part_interval_values = []
        default_values_list = []
        for config in configs:
            config_file = config.get('name')
            enabled = config.get('enabled')
            if enabled == 'false':
                continue
            default = config.get('iterator_default')
            self._get_iterator_values(config_file, default, interval_values,\
            user, part_interval_values, default_values_list)
        cartesian_list = []
        if len(interval_values.values()) > 0:
            cartesian_list = cartesian(interval_values.values()[0])

        return cartesian_list


    def _add_property(self, parent, value, inherited_value=''):
        """
        @param:
            parent: element tree node, a TestSuite/TestCase node
            value: the value to be set
            inherited_value: the value inherited from the parent suite. 
                It is used to propagate iterator values on subsuites
        @return:
            cartesian list of the iterators as list of pairs
        @summary:
            Adds a property node to an existing TestSuite/TestCase element tree node
        """
        if value:
            new_prop = etree.SubElement(parent, 'Property')
            new_prop_name = etree.SubElement(new_prop, 'propName')
            new_prop_name.text = 'iterationNr'
            new_prop_value = etree.SubElement(new_prop, 'propValue')
            if inherited_value:
                new_prop_value.text = inherited_value + ', ' + value
            else:
                new_prop_value.text = value


    def _expand_global_configs(self, user, xml, config_list=[]):
        """
        @param:
            user: the twister authenticated user
            xml: the project/last_edited xml in etree format. When going into recursion, xml becomes a suite.
        @summary:
            Suites now support configs, seen as global configs for all test in a suite.
            It duplicates the suite as many times as the iterator says.
            The value from the top suite propagates to the subsuites.
            A property tag is added to store the iteration value.
            Between tc iterators and suite iterators, the last ones have priority.
        """
        for suite in xml.findall('TestSuite'):
            remove = True
            ts_name = suite.find('tsName').text
            cfg_prop = suite.find('ConfigFiles')
            config_info = cfg_prop.findall('Config')
            cartesian_list = self._get_cartesian_list(user, config_info)
            logDebug("CeParser: Will iterate test suite `{}`, {} times, from values: {}, user `{}`."\
                     .format(ts_name, len(cartesian_list), cartesian_list, user))

            inherited_val = ''
            parent_property = xml.findall('Property')
            if len(parent_property) > 0:
                parent_property = parent_property[0]
                inherited_val = parent_property.find('propValue').text
            index = xml.index(suite)
            # duplicate suites
            for item in reversed(cartesian_list):
                deep_copy = copy.deepcopy(suite)
                suite_st = etree.tostring(deep_copy)
                newSuite = etree.fromstring(suite_st)
                xml.insert(index+1, newSuite)
                if isinstance(item, tuple):
                    value = ', '.join(str(x) for x in item)
                else:
                    value = str(item)
                self._add_property(newSuite, value, inherited_val)
                self._expand_global_configs(user, newSuite, config_list+copy.deepcopy(config_info))
                self._expand_tc_configs(user, newSuite, config_list+copy.deepcopy(config_info))
            if len(cartesian_list) == 0:
                remove = False
                if inherited_val:
                    self._add_property(suite, inherited_val)
                self._expand_global_configs(user, suite, config_list+copy.deepcopy(config_info))
                self._expand_tc_configs(user, suite, config_list+copy.deepcopy(config_info))
            # if the suite has iterators, remove the one that is being duplicated
            if remove:
                xml.remove(suite)


    def _expand_tc_configs(self, user, suite, config_list):
        """
        @param: 
            user: the authenticated twister user
            suite: the suite that contains the tc to duplicate
        @summary:
            Explodes the iterators and duplicates the test cases accordingly
            It is called after a suite is expanded, in _expand_global_configs
        """
        for tc in suite.findall('TestCase'):
            remove = True
            tc_name = tc.find('tcName').text
            cfg_prop = tc.find('ConfigFiles')
            config_info = cfg_prop.findall('Config')
            cartesian_list = self._get_cartesian_list(user, config_info)
            cfg_names = []
            for elem in config_list:
                new_cfg_name = elem.get('name')
                cfg_names = [cfg.get('name') for cfg in cfg_prop.findall('Config')]
                if new_cfg_name not in cfg_names:
                    cfg_prop.insert(-1,copy.deepcopy(elem))

            logDebug("CeParser: Will iterate test case `{}`, {} times, from values: {}, user `{}`."\
                     .format(tc_name, len(cartesian_list), cartesian_list, user))

            inherited_val = ''
            parent_property = suite.findall('Property')
            if len(parent_property) > 0:
                parent_property = parent_property[0]
                inherited_val = parent_property.find('propValue').text
            index = suite.index(tc)
            # duplicate suites
            for item in reversed(cartesian_list):
                deep_copy = copy.deepcopy(tc)
                tc_st = etree.tostring(deep_copy)
                new_tc = etree.fromstring(tc_st)
                suite.insert(index+1, new_tc)
                if isinstance(item, tuple):
                    value = ', '.join(str(x) for x in item)
                else:
                    value = str(item)
                self._add_property(new_tc, value, inherited_val)
            if len(cartesian_list) == 0:
                remove = False
                if inherited_val:
                    self._add_property(tc, inherited_val)
            # if the tc has iterators, remove the one that is being duplicated
            if remove:
                suite.remove(tc)


    def _expand_repeat_tag(self,user, xml):
        """
        @param:
            user: the twister authenticated user
            xml: the project/last_edited xml in etree format. When going into recursion, xml becomes a suite.
        @summary:
            Suites can have a repeat tag. It duplicates the suite as many times as the repeat tag says.
        """
        for suite in xml.findall('TestSuite'):
            suite_name = suite.find('tsName').text
            repeat = None
            try:
                repeat = suite.find('Repeat')
                nb_repeat = int(repeat.text)
                logDebug("CeParser: Will repeat suite `{}`, {} times.".format(suite_name, nb_repeat))
            except:
                nb_repeat = 1

            # before copying the suite for multiplication, remove the Repeat
            # tag because it MUST NOT be present in generated xml file
            if repeat is not None:
                suite.remove(repeat)

            index = xml.index(suite)
            for i in range(nb_repeat-1):
                deep_copy = copy.deepcopy(suite)
                suite_st = etree.tostring(deep_copy)
                suite_copy = etree.fromstring(suite_st)
                xml.insert(index+1, suite_copy)
                self._expand_repeat_tag(user, suite_copy)
            self._expand_repeat_tag(user, suite)


    def _expand_by_ep(self, user, xml):
        """
        @param:
            user: the twister authenticated user
            xml: the project/last_edited xml in etree format. When going into recursion, xml becomes a suite.
        @summary:
            The sut tag can contain multiple suts and a sut can contain multiple eps. Main suites must be
            duplicated to run on each ep from each sut.
        """
        suites = xml.findall('TestSuite')
        for suite in suites:
            # get all suts chosen by user
            all_suts = suite.find('SutName').text
            suite_name = suite.find('tsName').text
            if not all_suts:
                err = 'User `{}`: Invalid SUT for suite `{}`! Cannot generate project!'.format(user, suite_name)
                logWarning(err)
                return '*ERROR* ' + err
            suts_list = [q.replace('(', '.').replace(')', '') for q in all_suts.split(';') if q]
            # added get_sut to load the suts in resources dict. get_sut_info\
            # takes resources from the resources dict
            index = xml.index(suite)
            for sut in suts_list:
                self.project.sut.get_sut(sut, props={'__user': user})
                sut = '/' + sut
                sut_eps = self.project.sut.get_info_sut(sut + ':_epnames_' + user, {'__user': user})
                
                if sut_eps and '*ERROR*' in sut_eps:
                    logError(sut_eps)
                    return sut_eps

                if sut_eps and (isinstance(sut_eps, str) or isinstance(sut_eps, unicode)):
                    sut_eps_list = [ep for ep in sut_eps.split(';') if ep]
                    for ep_id in sut_eps_list:
                        deep_copy = copy.deepcopy(suite)
                        suite_st = etree.tostring(deep_copy)
                        suite_copy = etree.fromstring(suite_st)
                        if suite_copy.find('TestCase') is not None or \
                            suite_copy.find('TestSuite') is not None:
                            index += 1
                            xml.insert(index, suite_copy)
                            self._edit_suite(ep_id, sut, suite_copy)
                else:
                    # Find Anonimous EP in the active EPs
                    anonim_ep = self.project._find_anonim_ep(user)
                    if isinstance(anonim_ep, bool):
                        return anonim_ep
                    deep_copy = copy.deepcopy(suite)
                    suite_st = etree.tostring(deep_copy)
                    suite_copy = etree.fromstring(suite_st)
                    if suite_copy.find('TestCase') is not None or \
                        suite_copy.find('TestSuite') is not None:
                        index += 1
                        xml.insert(index, suite_copy)
                        self._edit_suite(anonim_ep, sut, suite_copy)
            xml.remove(suite)


    def generate_xml(self, user, filename):
        '''
        Receives project file.
        Creates testsuites.xml file by multiplying tests depending
        on the suts number and eps.
        '''
        logDebug("CeParser: preparing to convert project file: `{}`,\
        user `{}`.".format(filename, user))

        data = self.project.read_project_file(user, filename)
        if data.startswith('*ERROR*'):
            logWarning(data)
            return data

        # try to parse the project file
        try:
            xml = etree.fromstring(data)
        except Exception as e:
            msg = "The file: '{}' it's not an xml file. Try again!\n{}".\
            format(filename, e)
            logDebug(msg)
            return '*ERROR* ' + msg

        self._expand_global_configs(user, xml)
        
        self._expand_repeat_tag(user, xml)
        
        self._expand_by_ep(user, xml)

        repeated_dict = {}
        self._change_ids(xml, repeated_dict)

        self._resolve_dependencies(xml, repeated_dict)

        for suite in xml.findall('.//TestSuite'):
            prop = suite.find('Property')
            if prop:
                suite.remove(prop)
        # Final XML string
        xml_string = etree.tostring(xml, pretty_print=True)

        # write the xml file
        xml_file = userHome(user) + '/twister/config/testsuites.xml'

        resp = self.project.localFs.write_user_file(user, xml_file, xml_string, 'w')
        if resp != True:
            logError(resp)
            return '*ERROR* ' + resp

        logDebug('CeParser: Successfully generated: `{}`, user `{}`.'.\
        format(xml_file, user))
        return True


    def get_number_of_iterations(self, user, configs):
        """
        Computes the number of iterations each time a user manipulates the
        configs for a test.
        """
        interval_values = OrderedDict()
        part_interval_values = []
        default_values_list = []
        for config in configs.split(';')[:-1]:
            cfg = config.split(',')
            config_file = cfg[0].strip()
            default = cfg[1].strip()
            self._get_iterator_values(config_file, default, interval_values,\
            user, part_interval_values, default_values_list)
        cartesian_list = list()
        if len(interval_values.values()) > 0:
            cartesian_list = cartesian(interval_values.values()[0])

        return len(cartesian_list)


# Eof()
