
# File: CeParser.py ; This file is part of Twister.

# version: 3.008

# Copyright (C) 2012-2014 , Luxoft

# Authors:
#    Andreea Proca <aproca@luxoft.com>
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

import re
import copy
import ast
import uuid
import json

from lxml import etree
from collections import OrderedDict

from common.helpers import *


def cartesian(lists):
    if lists == []:
        return [()]
    return [x + (y,) for x in cartesian(lists[:-1]) for y in lists[-1]]


class CeXmlParser(object):
    """
    Parse and generate project.xml files.
    """

    def __init__(self, project):
        self.project = project


    def _edit_suite(self, ep, sut, config_root):
        '''
        Update suite props with sut name, ep id and id.
        Delete test cases having running = false.
        Used only by generate_xml method.
        '''

        for epname in config_root.xpath('//EpId'):
            epname.text = ep

        for sut_name in config_root.xpath('//SutName'):
            sut_name.text = sut

        # add the ep name to ID
        for id_name in config_root.xpath('//ID'):
            if '#' not in id_name.text:
                id_name.text = id_name.text + "#" + ep

        # delete tc if running = false
        for prop in config_root.xpath("//Property"):
            if prop.find('propName').text == 'Running' and prop.find('propValue').text == 'false':
                grand_parent = (prop.getparent()).getparent()
                grand_parent.remove(prop.getparent())

        # delete empty sub-suites from this suite
        for suite in config_root.xpath('TestSuite'):
            if suite.find('TestSuite') is None and suite.find('TestCase') is None:
                suite_parent = suite.getparent()
                suite_parent.remove(suite)

        return True


    def _do_repeat(self, config_root, repeated_dict, ep):
        '''
        Repeat Test Case or Suites as often as the tag <Repeat>
        says.
        '''

        # get all existing ids from the current testsuites.xml
        generated_ids_elems = copy.deepcopy(config_root.xpath('//ID'))
        generated_ids = []
        for g_id in generated_ids_elems:
            generated_ids.append(g_id.text)

        # get all the repeat tags from this suite
        repeat_list = config_root.xpath('//Repeat')
        if not repeat_list:
            return True

        for repeat in reversed(repeat_list):
            parent = repeat.getparent()

            # get repeat times and delete Repeat tag because it MUST not
            # be present in generated xml file
            repeat_nb = int(repeat.text)
            parent.remove(repeat)

            #if int(repeat.text) > 1:
            if repeat_nb > 1:
                if parent.find('tcName') is not None:
                    elem_name = parent.find('tcName').text
                else:
                    elem_name = parent.find('tsName').text

                logDebug("CeParser: Will repeat element {}, {} times."\
                    .format(elem_name, repeat_nb))

                for i in range(repeat_nb - 1):
                    # create a copy to multiplicate the entries
                    deep_copy = copy.deepcopy(parent)

                    # generate new unique id
                    new_id = uuid.uuid4()
                    while new_id in generated_ids:
                        new_id = uuid.uuid4()
                    # add the id to the already generated ids
                    generated_ids.append(str(new_id))

                    # add the new_id to repeated_dict to know how the ids propagated
                    self._add_to_repeated(copy.deepcopy(deep_copy.find('ID').text), str(new_id), repeated_dict, ep)

                    # update suite id
                    deep_copy.find('ID').text = str(new_id)

                    # the suite repeated - add to root
                    if parent is None:
                        config_root.append(deep_copy)
                    else:
                        parent.addnext(deep_copy)

            else:
                self._add_to_repeated(copy.deepcopy(parent.find('ID').text), copy.deepcopy(parent.find('ID').text), repeated_dict, ep)

        return True


    def _resolve_dependencies(self, repeated_dict, config_fs_root):
        '''
        Modify the dependency tag with the corresponding ones after
        exploding the suite.
        '''

        suites_list =  config_fs_root.xpath('TestSuite')
        #iterate suites
        for suite_e in suites_list:
            old_suite = suite_e
            suite_e = etree.tostring(suite_e)
            suite_e = etree.fromstring(suite_e)

            index_ep = suite_e.find('ID').text.find('#')
            suite_e_id = suite_e.find('ID').text[:index_ep]

            #get dependencies for this suite
            dependencies = suite_e.xpath('//Dependency')
            dependencies = [x for x in dependencies if x.text]

            for dep_id in dependencies:

                # get ep of this suite
                parent = dep_id.getparent()
                parent_id = parent.find('ID').text
                parent_id_ep = parent_id.split('#')[1]

                #get the sut used in this suite
                grandparent_sut = parent.getparent()
                sut_value = grandparent_sut.find('SutName').text

                #may be multimple dependecies
                dep_id_list = dep_id.text.split(';')
                dep_id_list = [x for x in dep_id_list if x]

                # iterate throught dependencies
                for dep_id_s in dep_id_list:
                    if "#" in dep_id_s:
                        continue

                    #separate id and status
                    clean_id = dep_id_s.split(':')[0]
                    status = dep_id_s.split(':')[1]

                    if clean_id in repeated_dict:
                        repeated_dict[clean_id] = list(set(repeated_dict[clean_id]))
                        dep_string = ''
                        found_dep = False

                        for elem in repeated_dict[clean_id]:
                            if ("#" + suite_e_id + "-" + sut_value + "-" + parent_id_ep) in elem:
                                index = elem.find("#")

                                elem_c = elem[:index] + "#" + parent_id_ep
                                dep_string = elem_c + ":" + status + ";"
                                if "#" in dep_id.text:
                                    dep_id.text = dep_id.text + dep_string
                                else:
                                    dep_id.text = dep_string

                                found_dep = True

                        # depends on tc from a another suite
                        if not found_dep:
                            for elem in repeated_dict[clean_id]:
                                index = elem.find("#")

                                elem_c = elem[:index] + "#" + parent_id_ep
                                dep_string = elem_c + ":" + status + ";"
                                if '#' in dep_id.text:
                                    dep_id.text = dep_id.text + dep_string
                                else:
                                    dep_id.text = dep_string

            # add the suite to the root element
            config_fs_root.append(suite_e)
            config_fs_root.remove(old_suite)

        return True


    def _add_to_repeated(self, kid_id, new_id, repeated_dict, ep):
        '''
        Add to repeated_dict.
        '''

        if new_id in ep:
            return True

        # add suite id, sut and ep
        if "#" not in new_id:
            new_id = new_id + "#" + ep

        if kid_id not in repeated_dict.keys():
            found = False
            for key, values in repeated_dict.items():
                for v in values:
                    #maybe this is a copy with a changed id of another copy
                    if kid_id in v:
                        found = True
                        repeated_dict[key].append(new_id)
                        break
            # create a key with the old id
            if not found:
                repeated_dict[kid_id] = [new_id]
        else:
            # add to the key found
            repeated_dict[kid_id].append(new_id)
        return True


    def _change_ids(self, config_root, repeated_dict, config_fs_root, ep):
        '''
        Change IDs if a suite has to repeat
        '''

        generated_ids_elems = copy.deepcopy(config_root.xpath('//ID'))
        generated_ids = []
        for g_id in generated_ids_elems:
            generated_ids.append(g_id.text)

        suites_id = config_fs_root.xpath('//TestSuite/ID')
        for s_id in suites_id:
            clean_id = s_id.text.split('#')[0]
            if config_root.find('ID').text != clean_id:
                return True

        # generate new unique id if necessary
        new_id = uuid.uuid4()
        while new_id in generated_ids:
            new_id = uuid.uuid4()
        generated_ids.append(str(new_id))

        config_root.find('ID').text = str(new_id)
        suite_id = config_root.find('ID').text

        kid_ids = config_root.xpath('//ID')
        for kid_id in kid_ids:
            if kid_id.text != suite_id:
                parent = kid_id.getparent()

                # generate new unique id if necessary
                new_id = uuid.uuid4()
                while new_id in generated_ids:
                    new_id = uuid.uuid4()

                generated_ids.append(str(new_id))

                # add to repeated_dict the old id and the new one
                self._add_to_repeated(copy.deepcopy(kid_id.text), str(new_id), repeated_dict, suite_id + "-" + ep)
                kid_id.text = str(new_id)

        return True


    def _explode_by_config(self, config_root_deep, parent_tc, ep, repeated_dict, cartesian_list):
        '''
        Add iterators if tc has config files.
        Explode the tc as many times as tuples of iterators..
        '''

        # will need to add new prop to tc for iterator
        prop_template = copy.deepcopy(parent_tc.find('Property'))
        parent_tc_copy = parent_tc
        #get the ID to know the key in repeated_dict id dependency
        parent_id_initial = copy.deepcopy(parent_tc.find('ID').text)

        # get all the current ids to avoid creating an identical one
        generated_ids_elems = copy.deepcopy(config_root_deep.xpath('//ID'))
        generated_ids = []
        for g_id in generated_ids_elems:
            generated_ids.append(g_id.text)

        for item in cartesian_list:
            if not item or isinstance(item, tuple) and len(item) < 1:
                continue

            # the tc may alreay have iterator prop because it is a copy -
            # we have to modify it
            find_prop = False
            props_list = parent_tc.findall('Property')
            for prop_p in props_list:
                if prop_p.find('propName').text == 'iterationNr':
                    prop_template = prop_p
                    prop_value = prop_template.find('propValue')
                    find_prop = True

            # first time the copy won't have iterator prop so add it
            if not find_prop:
                prop_name = prop_template.find('propName')
                prop_value = prop_template.find('propValue')
                prop_name.text = 'iterationNr'
                parent_tc_copy.append(prop_template)

            if isinstance(item, tuple):
                prop_value.text = ', '.join(str(x) for x in item)
            else:
                prop_value.text = str(item)

            if parent_tc_copy != parent_tc:
                # generate new unique id
                new_id = uuid.uuid4()
                while new_id in generated_ids:
                    new_id = uuid.uuid4()

                generated_ids.append(str(new_id))
                # add to repeated dict - needed if dependency
                self._add_to_repeated(parent_id_initial, str(new_id), repeated_dict, ep)

                # update parent_tc_copy id
                parent_tc_copy.find('ID').text = str(new_id)

            parent_tc.addnext(parent_tc_copy)
            # create a copy for next iteration
            parent_tc_copy = copy.deepcopy(parent_tc)

        return True


    def _get_config_files(self, user, config_root_deep, ep, repeated_dict):
        '''
        Get the iterators from all the confing files.
        Call a method to multiply the test cases.
        '''
        # get list of test cases
        tests_list = config_root_deep.xpath('TestCase')

        for test_case in tests_list:
            part_interval_values = []

            # get all the ConfigFiles tags for this test case.
            # A tc can have multiple config files
            cfg_prop = test_case.xpath('ConfigFiles')
            for cfg_item in cfg_prop:
                config_info = cfg_item.findall('Config')
                if not config_info:
                    continue
                parent_tc = cfg_item.getparent()
                tc_name = parent_tc.find('tcName').text

                interval_values = OrderedDict()
                default_values_list = []

                for config_entry in config_info:
                    enabled = config_entry.get('enabled')
                    if enabled == 'false':
                        continue

                    config_file = config_entry.get('name')
                    iterator_default = config_entry.get('iterator_default')
                    iterator_sof = config_entry.get('iterator_sof')

                    data = self.project.configs.read_config_file(user, config_file)
                    if data.startswith('*ERROR*'):
                        logWarning(data)
                        continue

                    # Try to parse the project file
                    try:
                        xml_config = etree.fromstring(data)
                    except:
                        msg = "Config file `{}` is invalid!".format(config_file)
                        logWarning(msg)
                        continue

                    config_file_st = etree.tostring(xml_config)
                    config_file_fst = etree.fromstring(config_file_st)
                    # find all entries having tag = iterator
                    config_types = config_file_fst.xpath('//type')
                    config_types = [x for x in config_types if x.text == 'iterator']

                    # Iterators from config file
                    for item in config_types:
                        prop_iterator = item.getparent()

                        config_name = config_entry.get('name') + '#' + prop_iterator.find('name').text
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
                            part_interval_values.append(['{}={}'.format(config_name, default_value)])
                            default_values_list.append('{}={}'.format(config_name, default_value))
                        else:
                            iter_interval_values = list()
                            key_default_value = '{}={}'.format(config_name, default_value)

                            for interv in values_list:
                                re_intervals = re.search('(\w*\d*\.?\d+)\.+(\w*\d*\.?\d+)', interv)
                                try:
                                    x = ast.literal_eval(re_intervals.group(1))
                                    y = ast.literal_eval(re_intervals.group(2))
                                    range_res = range(int(x), int(y) + 1)
                                    # avoid adding default value again ex: 2, 1...4
                                    if default_value in range_res and key_default_value in iter_interval_values:
                                        del(range_res[range_res.index(default_value)])
                                    for i in range_res:
                                        iter_interval_values.append('{}={}'.format(config_name, i))
                                except:
                                    try:
                                        x = re_intervals.group(1)
                                        y = re_intervals.group(2)
                                        # try to convert to int if possible
                                        try:
                                            v = int(ast.literal_eval(x))
                                            iter_interval_values.append('{}={}'.format(config_name, v))
                                        except:
                                            iter_interval_values.append('{}={}'.format(config_name, x))
                                        try:
                                            v = int(ast.literal_eval(y))
                                            iter_interval_values.append('{}={}'.format(config_name, v))
                                        except:
                                            iter_interval_values.append('{}={}'.format(config_name, y))
                                    except:
                                        try:
                                            interv = ast.literal_eval(interv)
                                        except:
                                            pass
                                        # avoid adding default value again ex: 2, 1, 2, 3
                                        if default_value != interv or key_default_value not in iter_interval_values:
                                            iter_interval_values.append('{}={}'.format(config_name, interv))

                            part_interval_values.append(iter_interval_values)

                        if part_interval_values:
                            if config_name in interval_values.keys():
                                interval_values[config_name].extend(part_interval_values)
                            else:
                                interval_values[config_name] = part_interval_values

                # get the cartesian list and explode the test case only if there
                # are iterators
                cartesian_list = list()
                if len(interval_values.values()) > 0:
                    cartesian_list = cartesian(interval_values.values()[0])

                    logDebug("CeParser: Will iterate test case `{}`, {} times, from values: {}, user `{}`."\
                        .format(tc_name, len(cartesian_list), interval_values.values(), user))

                    self._explode_by_config(config_root_deep, parent_tc, ep, repeated_dict, reversed(cartesian_list))

        return True


    def generate_xml(self, user, filename):
        '''
        Receives project file.
        Creates testsuites.xml file by multiplying tests depending
        on the suts number and eps.
        '''
        logDebug("CeParser: preparing to convert project file: `{}`, user `{}`.".format(filename, user))

        data = self.project.read_project_file(user, filename)
        if data.startswith('*ERROR*'):
            logWarning(data)
            return data

        # try to parse the project file
        try:
            xml = etree.fromstring(data)
        except:
            msg = "The file: '{}' it's not an xml file. Try again!".format(filename)
            logDebug(msg)
            return '*ERROR* ' + msg

        # write general props to testsuties.xml file
        root = etree.Element("Root")
        root.append(xml.find('stoponfail'))
        root.append(xml.find('PrePostMandatory'))
        root.append(xml.find('ScriptPre'))
        root.append(xml.find('ClearCaseView'))
        root.append(xml.find('libraries'))
        root.append(xml.find('ScriptPost'))
        root.append(xml.find('dbautosave'))
        root.append(xml.find('tcdelay'))

        config_ts_root = etree.tostring(root)
        config_fs_root = etree.fromstring(config_ts_root)
        repeated_dict = {}

        # Get all suites defined in project file
        for suite in xml.findall('TestSuite'):
            # get all suts chosen by user
            all_suts = suite.find('SutName').text
            suite_name = suite.find('tsName').text
            if not all_suts:
                err = 'User `{}`: Invalid SUT for suite `{}`! Cannot generate project!'.format(user, suite_name)
                logWarning(err)
                return '*ERROR* ' + err

            suts_list = [q.replace('(', '.').replace(')', '') for q in all_suts.split(';') if q]

            # Multiply suite entry as often as the tag 'Repeat' says
            repeat = None
            try:
                repeat = suite.find('Repeat')
                nb_repeat = int(repeat.text)
            except:
                nb_repeat = 1

            if nb_repeat > 1:
                logDebug("CeParser: Will repeat suite `{}`, {} times.".format(suite_name, nb_repeat))

            # before copying the suite for multiplication, remove the Repeat
            # tag because it MUST NOT be present in generated xml file
            if repeat is not None:
                suite.remove(repeat)

            for i in range(nb_repeat):
                deep_copy = copy.deepcopy(suite)
                config_ts = etree.tostring(deep_copy)
                config_root = etree.fromstring(config_ts)

                # for every ep of a sut create entry
                for sut in suts_list:
                    sut = '/' + sut
                    sut_eps = self.project.sut.get_info_sut(sut + ':_epnames_' + user, {'__user': user})

                    if sut_eps and sut_eps != "false":
                        sut_eps_list = [ep for ep in sut_eps.split(';') if ep]

                        for ep in sut_eps_list:
                            config_root_deep = copy.deepcopy(config_root)

                            self._change_ids(config_root_deep, repeated_dict, config_fs_root, sut + "-" + ep)

                            suite_id = config_root_deep.find('ID').text

                            # update sut, ep, id, tunning test cases
                            self._get_config_files(user, config_root_deep, suite_id + "-" + sut + "-" + ep, repeated_dict)

                            self._do_repeat(config_root_deep, repeated_dict, suite_id + "-" + sut + "-" + ep)

                            self._edit_suite(ep, sut, config_root_deep)

                            if config_root_deep.find('TestSuite') is not None or config_root_deep.find('TestCase') is not None:
                                # append suite to the xml root
                                root.append(config_root_deep)
                    else:
                        # Find Anonimous EP in the active EPs
                        anonim_ep = self.project._find_anonim_ep(user)
                        if isinstance(anonim_ep, bool):
                            return anonim_ep

                        config_root_deep = copy.deepcopy(config_root)
                        self._change_ids(config_root_deep, repeated_dict, config_fs_root, sut + "-" + anonim_ep)

                        suite_id = config_root_deep.find('ID').text

                        self._get_config_files(user, config_root_deep, suite_id + "-" + sut + "-" + anonim_ep, repeated_dict)

                        self._do_repeat(config_root_deep, repeated_dict, suite_id + "-" + sut + "-" + anonim_ep)

                        self._edit_suite(str(anonim_ep), sut, config_root_deep)

                        if config_root_deep.find('TestSuite') is not None or config_root_deep.find('TestCase') is not None:
                            # append suite to the xml root
                            root.append(config_root_deep)

        config_ts_root = etree.tostring(root)
        config_fs_root = etree.fromstring(config_ts_root)
        self._resolve_dependencies(repeated_dict, config_fs_root)

        # write the xml file
        xml_file = userHome(user) + '/twister/config/testsuites.xml'

        xml_header = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n\n'
        resp = self.project.localFs.write_user_file(user, xml_file, xml_header, 'w')
        if resp != True:
            logError(resp)
            return '*ERROR* ' + resp

        resp = self.project.localFs.write_user_file(user, xml_file, etree.tostring(config_fs_root, pretty_print=True), 'w')
        if resp != True:
            logError(resp)
            return '*ERROR* ' + resp

        logDebug("CeParser: Successfully generated: `{}`, user `{}`.".format(xml_file, user))
        return True


# Eof()
