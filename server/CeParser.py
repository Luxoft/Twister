
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
from lxml import etree


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


    def _do_repeat(self, config_root, repeted_dict, ep):
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

                    self.add_to_repeated(copy.deepcopy(deep_copy.find('ID').text), str(new_id), repeted_dict, ep)

                    # update suite id
                    deep_copy.find('ID').text = str(new_id)

                    if parent is None:
                        config_root.append(deep_copy)
                    else:
                        parent.addnext(deep_copy)

                repeat.getparent().find('Repeat').text = str(1)

            else:
                self.add_to_repeated(copy.deepcopy(parent.find('ID').text), copy.deepcopy(parent.find('ID').text), repeted_dict, ep)

        return True


    def resolve_dependencies(self, repeted_dict, config_fs_root):
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

                    if clean_id in repeted_dict:
                        repeted_dict[clean_id] = list(set(repeted_dict[clean_id]))

                        dep_string = ''
                        found_dep = False

                        for elem in repeted_dict[clean_id]:
                            if ("#" + suite_e_id + "-" + sut_value + "-" + parent_id_ep) in elem:

                                index = elem.find("#")

                                elem_c = elem[:index] + "#" + parent_id_ep
                                dep_string = elem_c + ":" + status + ";"
                                if "#" in dep_id.text:
                                    dep_id.text = dep_id.text + dep_string
                                else:
                                    dep_id.text = dep_string

                                found_dep = True

                        if not found_dep:
                            for elem in repeted_dict[clean_id]:
                                index = elem.find("#")

                                elem_c = elem[:index] + "#" + parent_id_ep
                                dep_string = elem_c + ":" + status + ";"

                                if "#" in dep_id.text:
                                    dep_id.text = dep_id.text + dep_string
                                else:
                                    dep_id.text = dep_string

                config_fs_root.append(suite_e)
                config_fs_root.remove(old_suite)

        return True


    def add_to_repeated(self, kid_id, new_id, repeted_dict, ep):
        '''
        Add to repeated_dict.
        '''
        if "#" not in new_id:
            new_id = new_id + "#" + ep
        if kid_id not in repeted_dict.keys():
            found = False
            for key, values in repeted_dict.items():
                #maybe this is a copy with a changed id of another copy
                if kid_id in values:
                    found = True
                    repeted_dict[key].append(new_id)
                    break
            # create a key with the old id
            if not found:
                repeted_dict[kid_id] = [new_id]
        else:
            # add to the key found
            repeted_dict[kid_id].append(new_id)


    def change_ids(self, config_root, repeted_dict, config_fs_root, ep):
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
                self.add_to_repeated(copy.deepcopy(kid_id.text), str(new_id), repeted_dict, suite_id + "-" + ep)
                kid_id.text = str(new_id)

        return True


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

        repeted_dict = dict()
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
                    sut_eps = self.sut.get_info_sut(sut + ':_epnames_' + user, {'__user': user})

                    if sut_eps and sut_eps != "false":
                        sut_eps_list = [ep for ep in sut_eps.split(';') if ep]

                        for ep in sut_eps_list:
                            config_root_deep = copy.deepcopy(config_root)

                            self.change_ids(config_root_deep, repeted_dict, config_fs_root, sut + "-" + ep)


                            suite_id = config_root_deep.find('ID').text
                            # update sut, ep, id, tunning test cases
                            self._do_repeat(config_root_deep, repeted_dict, suite_id + "-" + sut + "-" + ep)
                            self._edit_suite(ep, sut, config_root_deep)
                            # append suite to the xml root
                            root.append(config_root_deep)
                    else:
                        # Find Anonimous EP in the active EPs
                        anonim_ep = self._find_anonim_ep(user)
                        if isinstance(anonim_ep, bool):
                            return anonim_ep
                        config_root_deep = copy.deepcopy(config_root)
                        self.change_ids(config_root_deep, repeted_dict, config_fs_root, sut + "-" + anonim_ep)

                        suite_id = config_root_deep.find('ID').text
                        self._do_repeat(config_root_deep, repeted_dict, suite_id + "-" + sut + "-" + anonim_ep)
                        self._edit_suite(str(anonim_ep), sut, config_root_deep)
                        # append suite to the xml root
                        root.append(config_root_deep)

        config_ts_root = etree.tostring(root)
        config_fs_root = etree.fromstring(config_ts_root)
        self.resolve_dependencies(repeted_dict, config_fs_root)

        # write the xml file
        xml_file = userHome(user) + '/twister/config/testsuites.xml'

        xml_header = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n\n'
        resp = self.localFs.write_user_file(user, xml_file, xml_header, 'w')
        if resp != True:
            logError(resp)
            return resp

        resp = self.localFs.write_user_file(user, xml_file, etree.tostring(config_fs_root, pretty_print=True), 'w')
        if resp != True:
            logError(resp)
            return resp

        return True


# Eof()
