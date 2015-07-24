
# File: CeRpyc.py ; This file is part of Twister.

# version: 3.034

# Copyright (C) 2012-2014 , Luxoft

# Authors:
#    Andrei Costachi <acostachi@luxoft.com>
#    Cristi Constantin <crconstantin@luxoft.com>
#    Mihai Dobre <mihdobre@luxoft.com>

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
RPYC interface to clients.
"""

import os
import sys
import copy
import time
import thread
import traceback
import rpyc
from lxml import etree

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print '$TWISTER_PATH environment variable is not set! Exiting!'
    exit(1)
if TWISTER_PATH not in sys.path:
    sys.path.append(TWISTER_PATH)


from common.constants  import EXEC_STATUS, STATUS_INTERACT
from common.helpers    import userHome, re
from common.tsclogging import logError, logInfo, logFull, logDebug, logWarning
from common.tsclogging import getLogLevel, setLogLevel
from common.xmlparser  import PluginParser

#

class CeRpycService(rpyc.Service):

    """
    Execution Manager class organizes the EP / Suite / Testcase functions.
    """

    project = None

    # This dictionary will contain pairs of:
    # - keys of connection ip+ports from remote locations
    # - values of meta info about each connection, like:
    #   {
    #    'time': 12345...,
    #    'hello': 'client | ep | lib',
    #    'checked': True, 'user': '...',
    #    'conn': <Remote RPyc Service>,
    #    'eps': ['...'],
    #   }
    conns = {}
    conn_lock = thread.allocate_lock()


    def exposed_get_log_level(self):
        """
        This doesn't require login.
        """
        logFull('CeRpyc:exposed_get_log_level')
        return getLogLevel()


    def exposed_set_log_level(self, level):
        """
        Dinamically set log level.
        This doesn't require login.
        """
        logFull('CeRpyc:exposed_set_log_level')
        return setLogLevel(level)


    @classmethod
    def inject_object(self, name, obj):
        """
        Inject a variable inside this class
        """
        setattr(self, name, obj)
        return True


    def _get_addr(self):
        """
        Helper method to find the IP + Port of the current connection
        """
        try:
            return self._conn._config['connid']
        except:
            return ''


    def on_connect(self):
        """
        On client connect
        """
        logFull('CeRpyc:on_connect')
        str_addr = self._get_addr()

        # Add this connection in the list of connections,
        # If this connection CAN be added!
        try:
            with self.conn_lock:
                self.conns[str_addr] = {'conn': self._conn, 'time': time.time()}
        except Exception as exp_err:
            logError('EE: Connect error: {}.'.format(exp_err))

        logDebug('EE: Connected from `{}`.'.format(str_addr))


    def on_disconnect(self):
        """
        On client disconnect
        """
        logFull('CeRpyc:on_disconnect')
        str_addr = self._get_addr()

        hello = self.conns[str_addr].get('hello', '')
        stime = self.conns[str_addr].get('time', time.time())
        if hello:
            hello += ' - '

        # Unregister the eventual EPs for this connection
        if self.conns[str_addr].get('checked') and self.conns[str_addr].get('user'):
            eps = self.conns[str_addr].get('eps')
            if eps:
                self.unregister_eps(eps)

        # Delete everything for this address
        try:
            with self.conn_lock:
                del self.conns[str_addr]
        except Exception as exp_err:
            logError('EE: Disconnect error: {}.'.format(exp_err))

        logDebug('EE: Disconnected from `{}{}`, after `{:.2f}` seconds.'.format(
            hello, str_addr, (time.time() - stime)))


    @classmethod
    def _findConnection(self, usr, hello, addr=[], epname=''):
        """
        Helper function to find the first address for 1 user, that matches the hello,
        the Address, or the Ep.
        The hello should be: `client`, `ep`, or `lib`.
        The address will match the IP/ host; ex: ['127.0.0.1', 'localhost'].
        The EP must be the name of the EP registered by a client; returns the client, not the EP.
        Examples :
        // Find a client that has a specific EP; need to send commands to the client.
        // Find a local client, the EP is not important.
        // Find a specific EP, to send debug commands.
        """
        logFull('CeRpyc:_findConnection')
        if isinstance(self, CeRpycService):
            user = self._check_login()
        else:
            user = usr
        if not user:
            return False

        # logDebug('Find connection:: usr={}, addr={}, hello={}, epname={} in `{}` conns::\n{}'.format(
        #         usr, addr, (hello or None), (epname or None), len(self.conns),
        #         pformat(self.conns, width=140)))

        found = False

        # Cycle all active connections (clients, eps, libs, cli)
        for str_addr, data in self.conns.iteritems():
            # Skip invalid connections, without log-in, or without hello
            if not data.get('user') or not data.get('checked') or not data.get('hello'):
                continue
            if user != data['user']:
                continue
            # Searching for a specific hello
            if not (':' in data['hello'] and hello == data['hello'].split(':')[0] or hello == data['hello']):
                continue

            # If address is required, check
            if addr:
                # Invalid address !
                if str_addr.split(':')[0] not in addr:
                    continue

                # If we are looking for a specific EP inside a client
                if epname and epname in data.get('eps'):
                    found = str_addr
                    break
                # If not looking for a specific EP, it's ok
                elif not epname:
                    found = str_addr
                    break
            # Address is not required
            else:
                # If we are looking for a specific EP inside a client
                if epname and epname in data.get('eps', []):
                    found = str_addr
                    break
                # If not looking for a specific EP, it's ok
                elif not epname:
                    found = str_addr
                    break
                # If looking for a specific ep by epname
                elif epname and hello and data.get('hello') == 'ep::' + epname:
                    found = str_addr
                    break
        # logDebug('Found conn:: {}'.format(pformat(self.conns.get(found), width=140)))

        return found


    def exposed_cherry_addr(self):
        """
        Returns the CherryPy IP and PORT, for the Central Engine.
        This might be used to create an XML-RPC connection, using this addr.
        """
        return self.project.ip_port


    def exposed_echo(self, msg):
        """
        This function is MASSIVELY used by all clients, for testing the connection.
        """
        if msg != 'ping':
            logInfo(':: {}'.format(msg))
        return 'Echo: {}'.format(msg)


    def exposed_hello(self, hello='', extra={}):
        """
        Used by a Client for setting a name and other props.
        """
        logFull('CeRpyc:exposed_hello')
        str_addr = self._get_addr()
        extra = dict(extra)
        extra.update({'hello': str(hello)})
        # logInfo('Hello `{} - {}` !'.format(hello, str_addr))

        # Delete the invalid extra meta-data
        if 'conn' in extra:
            del extra['conn']
        if 'user' in extra:
            del extra['user']
        if 'checked' in extra:
            del extra['checked']
        if 'eps' in extra:
            # Register the VALID eps...
            self.register_eps(extra['eps'])
            del extra['eps']

        with self.conn_lock:
            old_data = self.conns.get(str_addr, {})
            old_data.update(extra)
            self.conns[str_addr] = old_data

        return True


    def exposed_login(self, user, passwd):
        """
        Log in before anything else.
        A user cannot execute commands without logging in first!
        """
        logFull('CeRpyc:exposed_login user `{}`.'.format(user))
        str_addr = self._get_addr()

        user_home = userHome(user)
        if not os.path.isdir('{}/twister/config'.format(user_home)):
            logError('Cannot find Twister for user `{}`!'.format(user))
            return False

        # Check SSH password
        resp = self.project.rpyc_check_passwd(user, passwd)
        # List of roles for user
        user_roles = self.project.authenticate(user)
        # This user doesn't exist in users and groups
        if (not user_roles) or (not user_roles.get('roles')):
            logWarning('Username `{}` doesn\'t have any roles!'.format(user))
            return False

        with self.conn_lock:
            old_data = self.conns.get(str_addr, {})
            old_data.update({'checked': resp, 'user': user})
            self.conns[str_addr] = old_data

        logDebug('User login: `{}`: {}.'.format(user, 'success' if resp else 'failure'))
        return resp


    def _check_login(self):
        """
        Auto-detect the user based on the client connection,
        then check user login.
        """
        logFull('CeRpyc:_check_login')
        str_addr = self._get_addr()
        check = self.conns[str_addr].get('checked')
        user = self.conns[str_addr].get('user')
        if (not check) or (not user):
            return False
        else:
            return user


# # #


    def exposed_encrypt_text(self, text):
        """
        Encrypt a piece of text, using AES.
        """
        logFull('CeRpyc:exposed_encrypt_text')
        if not text:
            return ''
        user = self._check_login()
        if not user:
            return False
        return self.project.encrypt_text(user, text)


    def exposed_decrypt_text(self, text):
        """
        Decrypt a piece of text, using AES.
        """
        logFull('CeRpyc:exposed_decrypt_text')
        if not text:
            return ''
        user = self._check_login()
        if not user:
            return False
        return self.project.decrypt_text(user, text)


    def exposed_usr_manager(self, cmd, name='', *args, **kwargs):
        """
        Manage users, groups and permissions.
        """
        logFull('CeRpyc:exposed_usr_manager')
        user = self._check_login()
        if not user:
            return False
        return self.project.users_and_groups_mngr(user, cmd, name, args, kwargs)


    def exposed_list_users(self, active=False):
        """
        Function called from the CLI, to list the users that are using Twister.
        """
        logFull('CeRpyc:exposed_list_users')
        return self.project.list_users(active)


    def exposed_get_user_variable(self, variable):
        """
        Send a user variable
        """
        logFull('CeRpyc:exposed_get_user_variable')
        user = self._check_login()
        if not user:
            return False
        data = self.project.get_user_info(user, variable)
        if not data:
            return False
        return data


    def exposed_set_user_variable(self, key, variable):
        """
        Create or overwrite a user variable
        """
        logFull('CeRpyc:exposed_set_user_variable')
        user = self._check_login()
        if not user:
            return False
        return self.project.set_user_info(user, key, variable)


    def exposed_get_ep_variable(self, epname, variable):
        """
        Send an EP variable
        """
        logFull('CeRpyc:exposed_get_ep_variable')
        user = self._check_login()
        if not user:
            return False
        data = self.project.get_ep_info(user, epname)
        if not data:
            return False
        return data.get(variable, False)


    def exposed_set_ep_variable(self, epname, variable, value):
        """
        Create or overwrite an EP variable
        """
        logFull('CeRpyc:exposed_set_ep_variable')
        user = self._check_login()
        if not user:
            return False
        return self.project.set_ep_info(user, epname, variable, value)


    def exposed_list_suites(self, epname):
        """
        List all suites for 1 EP, in the current project
        """
        logFull('CeRpyc:exposed_list_suites')
        user = self._check_login()
        if not user:
            return False
        if not epname:
            return False
        tmp_suites = self.project.get_ep_info(user, epname).get('suites', {}).items()
        suite_list = [str(k)+':'+v['name'] for k, v in tmp_suites]
        return ','.join(suite_list)


    def exposed_get_suite_variable(self, epname, suite, variable):
        """
        Send a Suite variable
        """
        logFull('CeRpyc:exposed_get_suite_variable')
        user = self._check_login()
        if not user:
            return False
        data = self.project.get_suite_info(user, epname, suite)
        if not data:
            return False
        return data.get(variable, False)


    def exposed_get_file_variable(self, epname, file_id, variable):
        """
        Send a file variable
        """
        logFull('CeRpyc:exposed_get_file_variable')
        user = self._check_login()
        if not user:
            return False
        data = self.project.get_file_info(user, epname, file_id)
        if not data:
            return False
        return data.get(variable, False)


    def exposed_set_file_variable(self, epname, filename, variable, value):
        """
        Create or overwrite a file variable
        """
        logFull('CeRpyc:exposed_set_file_variable')
        user = self._check_login()
        if not user:
            return False
        return self.project.set_file_info(user, epname, filename, variable, value)


    def exposed_get_dependency_info(self, dep_id):
        """ get infromation about dependencies """
        logFull('CeRpyc:exposed_get_dependency_info')
        user = self._check_login()
        if not user:
            return False
        return self.project.get_dependency_info(user, dep_id)


# # #   Persistence   # # #


    def exposed_read_file(self, fpath, flag='r', fstart=0, f_type='fs'):
        """
        Read a file from TWISTER PATH, user's home folder, or ClearCase.
        Flag r/ rb = ascii/ binary.
        """
        user = self._check_login()
        if not user:
            return False
        resp = self.project.read_file(user, fpath, flag, fstart, f_type)
        if resp and resp.startswith('*ERROR*'):
            logWarning(resp)
        return resp


    def exposed_write_file(self, fpath, fdata, flag='w', f_type='fs'):
        """
        Write a file in user's home folder, or ClearCase.
        Flag w/ wb = ascii/ binary.
        """
        user = self._check_login()
        if not user:
            return False
        resp = self.project.write_file(user, fpath, fdata, flag, f_type)
        if resp != True:
            logWarning(resp)
        return resp


    def exposed_list_settings(self, config='', x_filter=''):
        """
        List all available settings, for 1 config of a user.
        """
        user = self._check_login()
        if not user:
            return False
        return self.project.list_settings(user, config, x_filter)


    def exposed_get_settings_value(self, config, key):
        """
        Fetch a value from 1 config of a user.
        """
        user = self._check_login()
        if not user:
            return False
        return self.project.get_settings_value(user, config, key)


    def exposed_set_settings_value(self, config, key, value):
        """
        Set a value for a key in the config of a user.
        """
        user = self._check_login()
        if not user:
            return False
        return self.project.set_settings_value(user, config, key, value)


    def exposed_del_settings_key(self, config, key, index=0):
        """
        Del a key from the config of a user.
        """
        user = self._check_login()
        if not user:
            return False
        return self.project.del_settings_key(user, config, key, index)


    def exposed_set_persistent_suite(self, suite, info={}, order=-1):
        """
        Create a new suite, using the INFO, at the position specified.\n
        This function writes in TestSuites.XML file.\n
        The changes will be available at the next START.
        """
        user = self._check_login()
        if not user:
            return False
        return self.project.set_persistent_suite(user, suite, info, order)


    def exposed_del_persistent_suite(self, suite):
        """
        Delete an XML suite, using a name ; if there are more suites with the same name,
        only the first one is deleted.\n
        This function writes in TestSuites.XML file.\n
        The changes will be available at the next START.
        """
        user = self._check_login()
        if not user:
            return False
        return self.project.del_persistent_suite(user, suite)


    def exposed_set_persistent_file(self, suite, fname, info={}, order=-1):
        """
        Create a new file in a suite, using the INFO, at the position specified.\n
        This function writes in TestSuites.XML file.\n
        The changes will be available at the next START.
        """
        user = self._check_login()
        if not user:
            return False
        return self.project.set_persistent_file(user, suite, fname, info, order)


    def exposed_del_persistent_file(self, suite, fname):
        """
        Delete an XML file from a suite, using a name ; if there are more files
        with the same name, only the first one is deleted.\n
        This function writes in TestSuites.XML file.\n
        The changes will be available at the next START.
        """
        user = self._check_login()
        if not user:
            return False
        return self.project.del_persistent_file(user, suite, fname)


# # #   Global Variables and Config Files   # # #


    def exposed_get_global_variable(self, var_path):
        """
        Global variables
        """
        logFull('CeRpyc:exposed_get_global_variable')
        user = self._check_login()
        if not user:
            return False
        return self.project.configs.get_global_variable(user, var_path, False)


    def exposed_set_global_variable(self, var_path, value):
        """
        Global variables
        """
        logFull('CeRpyc:exposed_set_global_variable')
        user = self._check_login()
        if not user:
            return False
        return self.project.configs.set_global_variable(user, var_path, value)

    def exposed_get_config(self, cfg_path, var_path):
        """
        Config files
        """
        logFull('CeRpyc:exposed_get_config')
        user = self._check_login()
        if not user:
            return False
        return self.project.configs.get_global_variable(user, var_path, cfg_path)


    def exposed_get_binding(self, cfg_name):
        """
        Read a binding between a CFG and a SUT.
        The result is XML.
        """
        user = self._check_login()
        if not user:
            return False
        logDebug('User `{}` reads bindings for `{}`.'.format(user, cfg_name))
        return self.project.parsers[user].get_binding(cfg_name)


    def exposed_set_binding(self, cfg_name, component, sut):
        """
        Write a binding between a CFG and a SUT.
        Return True/ False.
        """
        user = self._check_login()
        if not user:
            return (False, 'DEFAULT_ERROR')

        # <root><name>cfg1</name><bind config="cp1" sut="/s1.user"/></root>

        # check if the component exists
        result = self.exposed_get_config(cfg_name, '')
        if not isinstance(result, dict):
            logWarning('Config "{}" does not exist!'.format(cfg_name))
            return (False, 'NO_CONFIG_FILE')

        if component not in result:
            logWarning('Component "{}" does not exist in config "{}"!'.format(component, cfg_name))
            return (False, 'NO_COMPONENT')

        # check if the sut exists
        result = self.project.sut.get_sut(sut, props={'__user': user})
        if not isinstance(result, dict):
            logWarning('Sut "{}" does not exist!'.format(sut))
            return (False, 'NO_SUT')

        bindings_xml = self.exposed_get_binding(cfg_name)
        bindings_xml = bindings_xml.replace('<name>{}</name>'.format(cfg_name), '')
        bindings_tree = etree.fromstring(bindings_xml)
        #search the binding between the component and the sut(search by component -> they are unique)
        found = bindings_tree.xpath('/root/bind[@config="{}"]'.format(component))
        if len(found) == 0:
            # add the new binding to the xml
            bindings_xml = bindings_xml[:-7] + \
            '<bind config="{comp}" sut="{s}"/>'.\
            format(comp=component, s=sut) + bindings_xml[-7:]
        else:
            found = found[0]
            found.set('sut', sut)
            bindings_xml = etree.tostring(bindings_tree)

        fdata = self.project.parsers[user].set_binding(cfg_name, bindings_xml)
        ret = self.project.write_file(user, '~/twister/config/bindings.xml', fdata)
        if isinstance(ret, str):
            logWarning('User `{}` could not update bindings for `{}`!'.format(user, cfg_name))
            return (False, 'DEFAULT_ERROR')
        else:
            logDebug('User `{}` writes bindings for `{}`.'.format(user, cfg_name))

        # Cfg -> Sut bindings for user
        self.project.users[user]['bindings'] = self.project.parsers[user].getBindingsConfig()
        return (True, 'NO_ERROR')


    def exposed_del_binding(self, cfg_name, component):
        """
        Method that deletes a binding from the list of config->SUT bindings
        """
        user = self._check_login()
        if not user:
            return (False, 'DEFAULT_ERROR')
        # check if the component exists
        result = self.exposed_get_config(cfg_name, '')
        if not isinstance(result, dict):
            logWarning('Config "{}" does not exist!'.format(cfg_name))
            return (False, 'NO_CONFIG_FILE')

        if component not in result:
            logWarning('Component "{}" does not exist in config "{}"!'.format(component, cfg_name))
            return (False, 'NO_COMPONENT')

        bindings_xml = self.exposed_get_binding(cfg_name)
        bindings_xml = bindings_xml.replace('<name>{}</name>'.format(cfg_name), '')
        bindings_xml = re.sub('<bind config="{}" sut=".*?"/>'.format(component), '', bindings_xml)

        fdata = self.project.parsers[user].set_binding(cfg_name, bindings_xml)

        ret = self.project.write_file(user, '~/twister/config/bindings.xml', fdata)
        if isinstance(ret, str):
            logWarning('User `{}` could not update bindings for `{}`!'.format(user, cfg_name))
            return (False, 'DEFAULT_ERROR')
        else:
            logDebug('User `{}` writes bindings for `{}`.'.format(user, cfg_name))

        # Cfg -> Sut bindings for user
        self.project.users[user]['bindings'] = self.project.parsers[user].getBindingsConfig()
        return (True, 'NO_ERROR')


# # #   Register / Start / Stop EPs   # # #


    def exposed_list_eps(self):
        """
        All known EPs for a user, read from project.
        The user is identified automatically.
        """
        logFull('CeRpyc:exposed_list_eps')
        user = self._check_login()
        if not user:
            return False
        eps = self.project.get_user_info(user, 'eps').keys()
        return list(eps) # Best to make a copy


    @classmethod
    def exposed_registered_eps(self, user=None):
        """
        Return all registered EPs for all user clients.
        The user MUST be given as a parameter.
        """
        logFull('CeRpyc:exposed_registered_eps')
        if not user:
            return False
        eps = []

        for str_addr, data in self.conns.iteritems():
            # There might be more clients for a user...
            # And this Addr might be an EP, not a client
            if user is not None and user == data.get('user') and data.get('checked'):
                # If this connection has registered EPs, append them
                ep_el = data.get('eps')
                if ep_el:
                    eps.extend(ep_el)

        return sorted(set(eps))


    def register_eps(self, eps):
        """
        Private function to register all EPs for a client.
        Only a VALID client will be able to register EPs!
        The user is identified automatically.
        """
        str_addr = self._get_addr()
        user = self._check_login()
        if not user:
            return False

        if not str_addr:
            # Crash, to send the exception to the client
            raise Exception('*ERROR* Cannot identify the remote address!')

        if not isinstance(eps, type([])):
            # Crash, to send the exception to the client
            raise Exception('*ERROR* Can only register a List of EP names!')
        else:
            eps = sorted(set(eps))

        logDebug('Begin to register EPs: {} ...'.format(eps))

        try:
            # Send a Hello and this IP to the remote proxy Service
            self._conn.root.hello(self.project.ip_port[0])
        except Exception as exp_err:
            logWarning('Error: Register client error: {}'.format(exp_err))

        # Register the EPs to this unique client address.
        # On disconnect, this client address will be deleted
        # And the EPs will be automatically un-registered.
        with self.conn_lock:
            reg_eps = []
            for epname in eps:
                resp = self.project._register_ep(user, epname)
                reg_eps.append(resp)

            if True not in reg_eps:
                # Crash, to send the exception to the client
                raise Exception('The EPs were not registered!')

            # Before register, find the clients that have already registered these EPs!
            for c_addr, data in self.conns.iteritems():
                # Skip invalid connections, without log-in
                if not data.get('user') or not data.get('checked'):
                    continue
                # There might be more clients for a user. Must find all of them.
                if user == data['user']:
                    # This current Addr might be an EP, not a client
                    # If this connection has registered EPs
                    if not data.get('eps'):
                        continue
                    old_eps = set(data.get('eps'))
                    new_eps = set(eps)
                    diff_eps = old_eps - new_eps
                    intersect = old_eps & new_eps
                    if intersect:
                        logDebug('Un-register EP list {} from `{}` and register them on `{}`.'\
                                 ''.format(sorted(intersect), c_addr, str_addr))
                    # Delete the EPs that must be deleted
                    self.conns[c_addr]['eps'] = sorted(diff_eps)

            self.conns[str_addr]['eps'] = eps

        logInfo('Registered client manager for user `{}`\n\t-> Client from `{}` ++ {}.'.format(user, str_addr, eps))
        return True


    def unregister_eps(self, eps=[]):
        """
        Private, helper function to un-register some EPs for a client.
        The user is identified automatically.
        """
        logFull('CeRpyc:unregister_eps')
        str_addr = self._get_addr()
        user = self._check_login()
        if not user:
            return False

        if not str_addr:
            logError('*ERROR* Cannot identify the remote address!')
            return False

        if not isinstance(eps, type([])):
            logError('*ERROR* Can only un-register a List of EP names!')
            return False
        else:
            eps = set(eps)

        logDebug('Begin to un-register EPs: {} ...'.format(sorted(eps)))

        with self.conn_lock:
            for epname in eps:
                try:
                    self.project._unregister_ep(user, epname)
                except Exception as exp_err:
                    logError('Error un-register EP: `{}`!'.format(exp_err))

            data = self.conns[str_addr]
            s_eps = data.get('eps') or sorted(eps)
            if not s_eps:
                return True

        remaining = self.exposed_registered_eps(user)
        if remaining == s_eps:
            logInfo('Un-registered all EPs for user `{}`\n\t-> Client from `{}` -- {}.'\
                    ' No more EPs left for `{}` !'.format(user, str_addr, s_eps, user))
        else:
            logInfo('Un-registered EPs for user `{}`\n\t-> Client from `{}` -- {} !'.format(user, str_addr, s_eps))
        return True


    @classmethod
    def exposed_start_ep(self, epname, usr=None):
        """
        Start EP for client.
        This must work from any ExecManager instance.
        """
        logFull('CeRpyc:exposed_start_ep')
        if isinstance(self, CeRpycService):
            user = self._check_login()
        else:
            user = usr
        if not user:
            return False

        addr = self._findConnection(usr=user, hello='client', epname=epname)

        if not addr:
            logError('Unknown Execution Process: `{}`! The project will not run.'.format(epname))
            return False

        conn = self.conns.get(addr, {}).get('conn')

        try:
            result = conn.root.start_ep(epname)
            logDebug('Starting `{}:{}`..... {} !'.format(user, epname, result))
            return result
        except:
            trace = traceback.format_exc()[34:].strip()
            logError('Error: Start EP error: {}'.format(trace))
            return False


    @classmethod
    def exposed_stop_ep(self, epname, usr=None):
        """
        Stop EP for client.
        This must work from any ExecManager instance.
        """
        logFull('CeRpyc:exposed_stop_ep')
        if isinstance(self, CeRpycService):
            user = self._check_login()
        else:
            user = usr
        if not user:
            return False

        addr = self._findConnection(usr=user, hello='client', epname=epname)

        if not addr:
            logError('Unknown Execution Process: `{}`! Cannot stop the EP.'.format(epname))
            return False

        conn = self.conns.get(addr, {}).get('conn')

        try:
            result = conn.root.stop_ep(epname)
            logDebug('Stopping `{}:{}`..... {} !'.format(user, epname, result))
            return result
        except:
            trace = traceback.format_exc()[34:].strip()
            logError('Error: Stop EP error: {}'.format(trace))
            return False


# # #   EP and File statuses   # # #


    def exposed_queue_file(self, suite, fname):
        """
        Queue a file at the end of a suite, during runtime.
        If there are more suites with the same name, the first one is used.
        """
        logFull('CeRpyc:exposed_queue_file')
        user = self._check_login()
        if not user:
            return False
        return self.project.queue_file(user, suite, fname)


    def exposed_dequeue_files(self, data):
        """
        Remove a file from the files queue.
        """
        logFull('CeRpyc:exposed_dequeue_files')
        user = self._check_login()
        if not user:
            return False
        return self.project.de_queue_files(user, data)


    def exposed_get_ep_status(self, epname):
        """
        Return execution status for one EP. (stopped, paused, running, invalid)
        """
        logFull('CeRpyc:exposed_get_ep_status')
        user = self._check_login()
        if not user:
            return False

        if epname not in self.project.get_user_info(user, 'eps'):
            logDebug('*ERROR* Invalid EP name `{}` !'.format(epname))
            return False

        data = self.project.get_ep_info(user, epname)
        reversed = dict((v, k) for k, v in EXEC_STATUS.iteritems())
        return reversed[data.get('status', 8)]


    def exposed_get_ep_status_all(self):
        """
        Return execution status for all EPs. (stopped, paused, running, invalid)
        """
        logFull('CeRpyc:exposed_get_ep_status_all')
        user = self._check_login()
        if not user:
            return False

        data = self.project.get_user_info(user)
        rev_dict = dict((v, k) for k, v in EXEC_STATUS.iteritems())
        return rev_dict[data.get('status', 8)]


    def exposed_set_ep_status(self, epname, new_status, msg=''):
        """
        Set execution status for one EP. (0, 1, 2, or 3)
        Returns a string (stopped, paused, running).
        The `message` parameter can explain why the status has changed.
        """
        logFull('CeRpyc:exposed_set_ep_status')
        user = self._check_login()
        if not user:
            return False
        return self.project.set_exec_status(user, epname, new_status, msg)


    def exposed_set_ep_status_all(self, new_status, msg=''):
        """
        Set execution status for all EPs. (STATUS_STOP, STATUS_PAUSED, STATUS_RUNNING)
        Returns a string (stopped, paused, running).
        The `message` parameter can explain why the status has changed.
        """
        logFull('CeRpyc:exposed_set_ep_status_all')
        user = self._check_login()
        if not user:
            return False
        return self.project.set_exec_status_all(user, new_status, msg)


    def exposed_get_file_status_all(self, epname=None, suite=None):
        """
        Returns a list with all statuses, for all files, in order.
        The status of one file can be obtained with ce.get_file_variable.
        """
        logFull('CeRpyc:exposed_get_file_status_all')
        user = self._check_login()
        if not user:
            return False
        return self.project.get_file_status_all(user, epname, suite)


    def exposed_set_file_status(self, epname, file_id, new_status=10, time_elapsed=0.0):
        """
        Set status for one file and write in log summary.
        Called from the Runner.
        """
        logFull('CeRpyc:exposed_set_file_status')
        user = self._check_login()
        if not user:
            return False
        return self.project.set_file_status(user, epname, file_id, new_status, time_elapsed)


    def exposed_set_file_status_all(self, epname, new_status):
        """
        Reset file status for all files of one EP.
        Called from the Runner.
        """
        logFull('CeRpyc:exposed_set_file_status_all')
        user = self._check_login()
        if not user:
            return False
        return self.project.set_file_status_all(user, epname, new_status)


# # #   Download Files and Libraries   # # #


    def exposed_list_libraries(self, all_ep=True):
        """
        Returns the list of exposed libraries, from CE libraries folder.
        This list will be used to syncronize the libs on all EP computers.
        """
        logFull('CeRpyc:exposed_list_libraries')
        user = self._check_login()
        if not user:
            return False
        return self.project.get_libraries_list(user, all_ep)


    def exposed_download_library(self, name):
        """
        Sends required library to the EP, to be syncronized.
        The library can be global for all users, or per user.
        """
        logFull('CeRpyc:exposed_download_library')
        user = self._check_login()
        if not user:
            return False

        # Maybe the name begins with /
        name = name.lstrip('/')
        # Global lib path
        glob_lib_path = (TWISTER_PATH + '/lib/' + name).replace('//', '/')

        def _download_lib():
            """
            Just read a file.
            """
            import tarfile
            import cStringIO

            if not os.path.exists(glob_lib_path):
                err = '*ERROR* Invalid library `{}`!'.format(glob_lib_path)
                return err

            # If this is a "deep" file, or folder
            if '/' in name:
                root = glob_lib_path[:-len(name)]
                fname = name
            else:
                root, fname = os.path.split(glob_lib_path)

            # If the required library is a file and isn't inside a folder
            if os.path.isfile(glob_lib_path) and ('/' not in name):
                try:
                    with open(glob_lib_path, 'rb') as f_p:
                        logDebug('User `{}` requested global lib file `{}`.'.format(user, fname))
                        return f_p.read()
                except Exception as exp_err:
                    err = '*ERROR* Cannot read file `{}`! {}'.format(glob_lib_path, exp_err)
                    return err

            else:
                os.chdir(root)
                io_s = cStringIO.StringIO()
                # Write the folder tar.gz into memory
                with tarfile.open(fileobj=io_s, mode='w:gz') as binary:
                    binary.add(name=fname, recursive=True)
                if '/' in name:
                    logDebug('User `{}` requested global `deep` library `{}`.'.format(user, fname))
                else:
                    logDebug('User `{}` requested global lib folder `{}`.'.format(user, fname))
                return io_s.getvalue()

        # Auto detect if ClearCase Test Config Path is active
        cc_cfg = self.project.get_clearcase_config(user, 'libs_path')
        if cc_cfg:
            view = cc_cfg['view']
            actv = cc_cfg['actv']
            cc_lib = cc_cfg['path'].rstrip('/') + '/'
            lib_path = cc_lib + name
            # logDebug('Before downloading ClearCase lib `{}`.'.format(lib_path))
            user_view_actv = '{}:{}:{}'.format(user, view, actv)
            is_folder = self.project.clearFs.is_folder(user_view_actv, lib_path)
            if str(is_folder).startswith('*ERROR*'):
                return _download_lib()

            # If is folder, or "deep" file or folder, compress in memory and return the data
            if is_folder == True or '/' in name:
                logDebug('User `{}` requested ClearCase lib folder `{}`.'.format(user, name))
                resp = self.project.clearFs.targz_user_folder(user_view_actv, lib_path, cc_lib)
                # Read as ROOT
                if resp.startswith('*ERROR*'):
                    return _download_lib()
                return resp
            # File
            else:
                logDebug('User `{}` requested ClearCase lib file `{}`.'.format(user, name))
                resp = self.project.clearFs.read_user_file(user_view_actv, lib_path)
                # Read as ROOT
                if resp.startswith('*ERROR*'):
                    return _download_lib()
                return resp

        # User's home path
        else:
            user_lib = self.project.get_user_info(user, 'libs_path').rstrip('/') + '/'
            lib_path = user_lib + name
            # logDebug('Before downloading local lib `{}`.'.format(lib_path))
            is_folder = self.project.localFs.is_folder(user, lib_path)
            is_global_folder = os.path.isdir(glob_lib_path)

            # If is folder, or "deep" file or folder, compress in memory and return the data
            if is_folder == True or is_global_folder == True or '/' in name:
                logDebug('User `{}` requested local lib folder `{}`.'.format(user, name))
                resp = self.project.localFs.targz_user_folder(user, lib_path, user_lib)
                # Try as ROOT
                if resp.startswith('*ERROR*'):
                    return _download_lib()
                return resp
            # If is root library file, read the file directly
            else:
                logDebug('User `{}` requested local lib file `{}`.'.format(user, name))
                resp = self.project.localFs.read_user_file(user, lib_path)
                # Try as ROOT
                if resp.startswith('*ERROR*'):
                    return _download_lib()
                return resp


    def exposed_get_ep_files(self, epname):
        """
        Returns all files that must be run on one EP.
        """
        logFull('CeRpyc:exposed_get_ep_files')
        user = self._check_login()
        if not user:
            return False
        try:
            data = self.project.get_ep_files(user, epname)
        except:
            data = False
        return data


    def exposed_get_suite_files(self, epname, suite):
        """
        Returns all files that must be run on one Suite ID.
        """
        logFull('CeRpyc:exposed_get_suite_files')
        user = self._check_login()
        if not user:
            return False
        try:
            data = self.project.get_suite_files(user, epname, suite)
        except:
            data = False
        return data


    def exposed_download_file(self, epname, file_info):
        """
        Sends requested file to the EP, to be executed.
        """
        logFull('CeRpyc:exposed_download_file')
        user = self._check_login()
        if not user:
            return False

        if epname not in self.project.get_user_info(user, 'eps'):
            logDebug('*ERROR* Invalid EP name `{}` !'.format(epname))
            return False

        tests_path = self.project.get_user_info(user, 'tests_path')

        # If this is a test file path
        if os.path.isfile(tests_path + os.sep + file_info):
            filename = tests_path + os.sep + file_info

        # If this is a file ID
        else:
            file_id = file_info
            data = self.project.get_file_info(user, epname, file_id)
            if not data:
                logError('*ERROR* Invalid File ID `{}` !'.format(file_id))
                return False

            filename = data['file']

            # Auto detect if ClearCase Test Config Path is active
            cc_cfg = self.project.get_clearcase_config(user, 'tests_path')
            if cc_cfg and data.get('clearcase'):
                logDebug('Execution process `{}:{}` requested ClearCase file `{}`.'.format(user, epname, filename))
                # Set TC Revision variable
                self.project.set_file_info(user, epname, file_id, 'twister_tc_revision', -1)
                view = cc_cfg['view']
                # Read ClearCase TestCase file
                text = self.project.read_file(user, filename, type='clearcase:' + view)
                return text
            # End of ClearCase hack !

            # Fix ~ $HOME path (from project XML)
            if filename.startswith('~'):
                filename = userHome(user) + filename[1:]
            # Fix incomplete file path (from project XML)
            if not os.path.isfile(filename):
                filename = tests_path + os.sep + filename

        logDebug('Execution process `{}:{}` requested file `{}`.'.format(user, epname, filename))

        return self.project.localFs.read_user_file(user, filename, 'rb')


# # #   Plugins   # # #


    def exposed_list_plugins(self):
        """
        List all user plugins.
        """
        logFull('CeRpyc:exposed_list_plugins')
        user = self._check_login()
        if not user:
            return False
        parser = PluginParser(user)
        plugins_list = parser.getPlugins()
        logFull('List Plug-ins: user `{}` has: {}.'.format(user, plugins_list))
        return plugins_list.keys()


    def exposed_run_plugin(self, plugin, args):
        """
        Exposed API for running plug-ins from Execution Processes.
        """
        logFull('CeRpyc:exposed_run_plugin')
        user = self._check_login()
        if not user:
            return False

        # If argument is a valid dict, pass
        try:
            args = dict(args)
        except:
            return '*ERROR* Invalid type of argument for plugin `{}` : {} !'.format(plugin, type(args))

        if not 'command' in args:
            return '*ERROR* Invalid dictionary for plugin `{}` : {} !'.format(plugin, args)

        plugin_p = self.project._build_plugin(user, plugin)

        if not plugin_p:
            msg = '*ERROR* Plugin `{}` does not exist for user `{}`!'.format(plugin, user)
            logError(msg)
            return msg

        try:
            return plugin_p.run(args)
        except Exception as exp_err:
            trace = traceback.format_exc()[34:].strip()
            logError('*ERROR* Plugin `{}`, ran with arguments `{}` and raised Exception: `{}`!'\
                     .format(plugin, args, trace))
            return 'Error on running plugin `{}` - Exception: `{}`!'.format(plugin, exp_err)


# # #   Logs   # # #


    def exposed_get_log_file(self, read, fstart, filename):
        """
        Used to show the logs.
        """
        logFull('CeRpyc:exposed_get_log_file')
        user = self._check_login()
        if not user:
            return False
        return self.project.get_log_file(user, read, fstart, filename)


    def exposed_log_message(self, log_type, log_message):
        """
        This function is exposed in all tests and all logs are centralized in the HOME of the user.
        In order for the user to be able to access the logs written by CE, which runs as ROOT,
        CE will start a small process in the name of the user and the process will write the logs.
        """
        logFull('CeRpyc:exposed_log_message')
        user = self._check_login()
        if not user:
            return False
        return self.project.log_message(user, log_type, log_message)


    def exposed_log_live(self, epname, log_message):
        """
        Writes CLI messages in a big log, so all output can be checked LIVE.
        """
        logFull('CeRpyc:exposed_log_live')
        user = self._check_login()
        if not user:
            return False
        return self.project.log_live(user, epname, log_message)


    def exposed_reset_log(self, log_name):
        """
        Resets one log.
        """
        logFull('CeRpyc:exposed_reset_log')
        user = self._check_login()
        if not user:
            return False
        return self.project.reset_log(user, log_name)


    def exposed_reset_logs(self):
        """
        All logs defined in master config are erased.\n
        """
        logFull('CeRpyc:exposed_reset_logs')
        user = self._check_login()
        if not user:
            return False
        return self.project.reset_logs(user)


# # #   Resource Allocator   # # #


    def exposed_list_all_tbs(self):
        """
        List.
        """
        return self.project.testbeds.list_all_tbs()


    def exposed_list_all_suts(self):
        """
        List.
        """
        logFull('CeRpyc:exposed_list_all_suts')
        user = self._check_login()
        if not user:
            return False
        return self.project.sut.list_all_suts(user)


    def exposed_get_tb(self, query):
        """
        Get resource content.
        """
        logFull('CeRpyc:exposed_get_tb')
        user = self._check_login()
        if not user:
            return False
        try:
            return self.project.testbeds.\
            get_tb(query=query, props={'__user': user})
        except Exception as exp_err:
            logWarning(exp_err)
            return False


    def exposed_create_new_tb(self, name, parent, props={}):
        """
        New TB.
        """
        logFull('CeRpyc:exposed_create_new_tb')
        user = self._check_login()
        if not user:
            return False
        props['__user'] = user
        return self.project.testbeds.create_new_tb(name, parent, props)


    def exposed_create_component_tb(self, name, parent, props={}):
        """
        New TB component.
        """
        logFull('CeRpyc:exposed_create_component_tb')
        user = self._check_login()
        if not user:
            return False
        props['__user'] = user
        return self.project.testbeds.create_component_tb(name, parent, props)


    def exposed_update_meta_tb(self, name, parent, props={}):
        """
        Update meta.
        """
        logFull('CeRpyc:exposed_update_meta_tb')
        user = self._check_login()
        if not user:
            return False
        props['__user'] = user
        return self.project.testbeds.update_meta_tb(name, parent, props)


    def exposed_set_tb(self, name, parent='/', props={}):
        """
        Update a TB.
        """
        logFull('CeRpyc:exposed_set_tb')
        user = self._check_login()
        if not user:
            return False
        props['__user'] = user
        return self.project.testbeds.set_tb(name, parent, props)


    def exposed_create_new_sut(self, name, parent, props={}):
        """
        New SUT.
        """
        logFull('CeRpyc:exposed_create_new_sut')
        user = self._check_login()
        if not user:
            return False
        props['__user'] = user
        return self.project.sut.create_new_sut(name, parent, props)


    def exposed_create_component_sut(self, name, parent, props={}):
        """
        New SUT component.
        """
        logFull('CeRpyc:exposed_create_component_sut')
        user = self._check_login()
        if not user:
            return False
        props['__user'] = user
        return self.project.sut.create_component_sut(name, parent, props)


    def exposed_update_meta_sut(self, name, parent, props={}):
        """
        Update meta.
        """
        logFull('CeRpyc:exposed_update_meta_sut')
        user = self._check_login()
        if not user:
            return False
        props['__user'] = user
        return self.project.sut.update_meta_sut(name, parent, props)


    def exposed_set_sut(self, name, parent='/', props={}):
        """
        Update a SUT.
        """
        logFull('CeRpyc:exposed_set_sut')
        user = self._check_login()
        if not user:
            return False
        props['__user'] = user
        return self.project.sut.set_sut(name, parent, props)


    def exposed_rename_tb(self, res_query, new_name):
        """
        Rename a resource.
        """
        logFull('CeRpyc:exposed_rename_tb')
        user = self._check_login()
        if not user:
            return False
        return self.project.testbeds.\
        rename_tb(res_query, new_name, props={'__user': user})


    def exposed_delete_tb(self, query):
        """
        Delete a resource.
        """
        logFull('CeRpyc:exposed_delete_tb')
        user = self._check_login()
        if not user:
            return False
        return self.project.testbeds.delete_tb(query, props={'__user': user})


    def exposed_get_sut(self, query, follow_links=False):
        """
        Get SUT content.
        """
        logFull('CeRpyc:exposed_get_sut')
        user = self._check_login()
        if not user:
            return False
        try:
            # Delete possible net-refs
            if follow_links:
                follow_links = True
            else:
                follow_links = False
            return self.project.sut.get_sut(query,\
            props={'__user': user, 'follow_links': follow_links})
        except Exception as exp_err:
            logWarning(exp_err)
            return False


    def exposed_get_info_sut(self, query):
        """
        Get SUT meta.
        """
        logFull('CeRpyc:exposed_get_info_sut')
        user = self._check_login()
        if not user:
            return False
        return self.project.sut.get_info_sut(query, props={'__user': user})


    def exposed_rename_sut(self, res_query, new_name):
        """
        Rename a SUT.
        """
        logFull('CeRpyc:exposed_rename_sut')
        user = self._check_login()
        if not user:
            return False
        return self.project.sut.rename_sut(res_query, new_name, props={'__user': user})


    def exposed_rename_meta_sut(self, res_query, new_name):
        """
        Rename a SUT.
        """
        logFull('CeRpyc:exposed_rename_meta_sut')
        user = self._check_login()
        if not user:
            return False
        return self.project.sut.rename_meta_sut(res_query, new_name, props={'__user': user})


    def exposed_delete_sut(self, query):
        """
        Delete a SUT.
        """
        logFull('CeRpyc:exposed_delete_sut')
        user = self._check_login()
        if not user:
            return False
        return self.project.sut.delete_sut(query, props={'__user': user})


    def exposed_delete_component_sut(self, query):
        """
        Delete a SUT component.
        """
        logFull('CeRpyc:exposed_delete_component_sut')
        user = self._check_login()
        if not user:
            return False
        return self.project.sut.delete_component_sut(query, props={'__user': user})


    def exposed_is_tb_reserved(self, query):
        """ check if resource is reserved """
        logFull('CeRpyc:exposed_is_tb_reserved')
        user = self._check_login()
        if not user:
            return False
        return self.project.testbeds.\
        is_tb_reserved(query, props={'__user': user})


    def exposed_is_sut_reserved(self, query):
        """ check if SUT is reserved """
        logFull('CeRpyc:exposed_is_sut_reserved')
        user = self._check_login()
        if not user:
            return False
        return self.project.sut.is_sut_reserved(query, props={'__user': user})


    def exposed_reserve_tb(self, query):
        """ reserve resource """
        logFull('CeRpyc:exposed_reserve_tb')
        user = self._check_login()
        if not user:
            return (False, 'DEFAULT_ERROR')
        return self.project.testbeds.reserve_tb(query, props={'__user': user})


    def exposed_reserve_sut(self, query):
        """ reserve SUT """
        logFull('CeRpyc:exposed_reserve_sut')
        user = self._check_login()
        if not user:
            return (False, 'DEFAULT_ERROR')
        return self.project.sut.reserve_sut(query, props={'__user': user})


    def exposed_save_reserved_tb(self, query):
        """ save reserved resource and keep it reserved """
        logFull('CeRpyc:exposed_save_reserved_tb')
        user = self._check_login()
        if not user:
            return False
        return self.project.testbeds.\
        save_reserved_tb(query, props={'__user': user})


    def exposed_save_reserved_sut(self, query):
        """ save SUT and keep it reserved """
        logFull('CeRpyc:exposed_save_reserved_sut')
        user = self._check_login()
        if not user:
            return False
        return self.project.sut.save_reserved_sut(query, props={'__user': user})


    def exposed_save_reserved_sut_as(self, name, query):
        """ save SUT with a different name """
        logFull('CeRpyc:exposed_save_reserved_sut_as')
        user = self._check_login()
        if not user:
            return False
        return self.project.sut.save_reserved_sut_as(name, query, props={'__user': user})


    def exposed_save_release_reserved_tb(self, query):
        """ save and release resource """
        logFull('CeRpyc:exposed_save_rel_res_res')
        user = self._check_login()
        if not user:
            return False
        return self.project.testbeds.\
        save_release_reserved_tb(query, props={'__user': user})


    def exposed_save_release_reserved_sut(self, query):
        """ save SUT changes and release """
        logFull('CeRpyc:exposed_save_rel_res_sut')
        user = self._check_login()
        if not user:
            return False
        return self.project.sut.save_release_reserved_sut(query, props={'__user': user})


    def exposed_discard_release_reserved_tb(self, query):
        """ drop changes and release resource """
        logFull('CeRpyc:exposed_disc_rel_res_res')
        user = self._check_login()
        if not user:
            return False
        return self.project.testbeds.\
        discard_release_reserved_tb(query, props={'__user': user})


    def exposed_discard_release_reserved_sut(self, query):
        """ drop changes and release SUT """
        logFull('CeRpyc:exposed_disc_rel_res_sut')
        user = self._check_login()
        if not user:
            return False
        return self.project.sut.discard_release_reserved_sut(query, props={'__user': user})


    def exposed_interact(self, m_id, ep, m_type, msg, timeout, options):
        """
        Adds interact information in the interaction pool.
        The interaction pool is held in the `interact` variable under each user.
        """
        user = self._check_login()
        if not user:
            return False
        interact_options = {'id': m_id, 'ep':ep, 'type':m_type, 'msg':msg, \
        'timeout':timeout, 'options':options}
        with self.project.interact_lock:
            interact_data = self.project.get_user_info(user, 'interact')
            if interact_data:
                # it is supposed to be a list of dictionaries
                interact_data.extend([interact_options])
            else:
                interact_data = [interact_options]
            self.project.set_user_info(user, 'interact', copy.deepcopy(interact_data))

        self.project.set_exec_status(user, ep, STATUS_INTERACT)

        return True


    def exposed_remove_interact(self, m_id, ep, m_type, msg, timeout, options, reason=''):
        """
        Removes an interaction from the interaction pool.
        The interaction pool is held in the `interact` variable under each user.
        """
        user = self._check_login()
        if not user:
            return False
        # global lock for interaction pool
        with self.project.interact_lock:
            interact_data = self.project.get_user_info(user, 'interact')
            try:
                elem = filter(lambda interact: interact.get('id') == m_id, interact_data)[0]
                el_index = interact_data.index(elem)
                interact_data.pop(el_index)
            except Exception as exp_err:
                logDebug('Element has been already removed from queue: {}'.format(exp_err))
            self.project.set_user_info(user, 'interact', interact_data)
        return True


# Eof()
