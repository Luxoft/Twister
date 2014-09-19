
# File: CeParser.py ; This file is part of Twister.

# version: 3.001

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

import copy
import uuid
import re
import ast
from lxml import etree

from common.helpers    import *

def cartesian (lists):
    if lists == []: return [()]
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

        # delete empty suites
        for suite in config_root.xpath('TestSuite'):
            if not suite.find('TestSuite') and not suite.find('TestCase'):
                suite_parent = suite.getparent()
                suite_parent.remove(suite)

        return True


    def _do_repeat(self, config_root, repeated_dict, ep):
        '''
        Repet Test Case or Suites as often as the tag <Reapet>
        says.
        '''

        generated_ids_elems = copy.deepcopy(config_root.xpath('//ID'))
        generated_ids = []
        for g_id in generated_ids_elems:
            generated_ids.append(g_id.text)

        repeat_list = config_root.xpath('//Repeat')
        if not repeat_list:
            return True

        for repeat in reversed(repeat_list):
            parent = repeat.getparent()
            if int(repeat.text) > 1:
                for i in range(int(repeat.text) - 1):

                    deep_copy = copy.deepcopy(repeat.getparent())
                    deep_copy.find('Repeat').text = str(1)

                    # generate new unique id if necessary
                    new_id = uuid.uuid4()
                    while new_id in generated_ids:
                        new_id = uuid.uuid4()

                    generated_ids.append(str(new_id))

                    self._add_to_repeated(copy.deepcopy(deep_copy.find('ID').text), str(new_id), repeated_dict, ep)

                    # update suite id
                    deep_copy.find('ID').text = str(new_id)

                    if parent is None:
                        config_root.append(deep_copy)
                    else:
                        parent.addnext(deep_copy)

                repeat.getparent().find('Repeat').text = str(1)

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

                config_fs_root.append(suite_e)
                config_fs_root.remove(old_suite)

        return True


    def _add_to_repeated(self, kid_id, new_id, repeated_dict, ep):
        '''
        Add to repeated_dict.
        '''

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


    def explode_by_config(self, config_root_deep, parent_tc, ep, repeated_dict, cartesian_list):
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


    def get_config_files(self, user, config_root_deep, ep, repeated_dict):
        '''
        Get the iterators from all the confing files.
        Call a method to multiply the tc.
        '''

        cfg_path = self.project.get_user_info(user, 'tcfg_path')
        cfg_prop = config_root_deep.xpath('//ConfigFiles')

        #get all the ConfigFiles tags. A tc can have
        for cfg_item in cfg_prop:

            config_info = cfg_item.findall('Config')
            if not config_info:
                continue
            parent_tc = cfg_item.getparent()

            interval_values = dict()
            default_values_list = []

            for config_entry in config_info:
                config_file = cfg_path + "/" + config_entry.get('name')
                iterator_default = config_entry.get('iterator_default')
                iterator_sof = config_entry.get('iterator_sof')

                # try to parse the project file
                try:
                    xml_config = etree.parse(config_file)
                except:
                    msg = "The file: '{}' it's not an xml file. Try again!".format(filename)
                    logDebug(msg)
                    return '*ERROR* ' + msg

                config_file_st = etree.tostring(xml_config)
                config_file_fst = etree.fromstring(config_file_st)
                #find all entries having tag = iterator
                config_types = config_file_fst.xpath('//type')
                config_types = [x for x in config_types if x.text == 'iterator']

                # iterators from a config file
                for item in config_types:
                    part_interval_values = []
                    prop_iterator = item.getparent()

                    values = prop_iterator.find('value').text

                    if not values:
                        continue

                    values = values.replace(" ", "")
                    values_list = values.split(',')

                    # get the default value
                    index_dot = values_list[0].find("..")
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

                    if iterator_default == "true":
                        part_interval_values.append(default_value)
                        default_values_list.append(default_value)
                    else:
                        for interv in values_list:
                            try:
                                re_intervals = re.search('(\d*\.?\d+)\.+(\d*\.?\d+)', interv)
                                x = ast.literal_eval(re_intervals.group(1))
                                y = ast.literal_eval(re_intervals.group(2))
                                range_res = range(int(x), int(y) + 1)
                                part_interval_values.extend(range_res)
                            except:
                                try:
                                    part_interval_values.append(ast.literal_eval(interv))
                                except:
                                    part_interval_values.append(interv)

                    if part_interval_values:
                        if config_file in interval_values.keys():
                            interval_values[config_file].extend(part_interval_values)
                        else:
                            interval_values[config_file] = part_interval_values

            cartesian_list = cartesian(interval_values.values())
            if default_values_list:
                cartesian_list.extend(default_values_list)

            self.explode_by_config(config_root_deep, parent_tc, ep, repeated_dict, reversed(cartesian_list))


    def generate_xml(self, user, filename):
        '''
        Receives project file.
        Creates testsuites.xml file by multiplying tests depending
        on the suts number and eps.
        '''

        # try to parse the project file
        try:
            xml = etree.parse(filename)
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

        repeated_dict = dict()
        # get all suites defined in project file
        all_suites = xml.findall('TestSuite')
        for suite in all_suites:
            # get all suts chosen by user
            # try:
            all_suts = suite.find('SutName').text
            suts_list = [q for q in all_suts.split(';') if q]
            suts_list = [q.replace('(', '.').replace(')', '') for q in suts_list if q]

            # multiply Suite entry as often as the tag 'Repeat' says
            try:
                repeat = suite.find('Repeat')
                no_repeat = int(repeat.text)
            except:
                no_repeat = 1

            suite_name = suite.find('tsName').text
            for i in range(no_repeat):


                deep_copy = copy.deepcopy(suite)
                config_ts = etree.tostring(deep_copy)
                config_root = etree.fromstring(config_ts)

                if no_repeat > 1:
                    try:
                        config_root.find('Repeat').text = str(1)
                    except:
                        pass
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

                            self.get_config_files(user, config_root_deep, suite_id + "-" + sut + "-" + ep, repeated_dict)

                            self._do_repeat(config_root_deep, repeated_dict, suite_id + "-" + sut + "-" + ep)
                            self._edit_suite(ep, sut, config_root_deep)

                            if config_root_deep.find('TestSuite') or config_root_deep.find('TestCase'):
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

                        self.get_config_files(user, config_root_deep, suite_id + "-" + sut + "-" + anonim_ep, repeated_dict)

                        self._do_repeat(config_root_deep, repeated_dict, suite_id + "-" + sut + "-" + anonim_ep)
                        self._edit_suite(str(anonim_ep), sut, config_root_deep)

                        if config_root_deep.find('TestSuite') or config_root_deep.find('TestCase'):
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
            return resp

        resp = self.project.localFs.write_user_file(user, xml_file, etree.tostring(config_fs_root, pretty_print=True), 'w')
        if resp != True:
            logError(resp)
            return resp

        return True


# Eof()
