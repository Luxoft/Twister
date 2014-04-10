
# File: CeRpyc.py ; This file is part of Twister.

# version: 3.009

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

import os
import sys
import time
import json
import thread
import traceback
import rpyc
from pprint import pformat

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print('$TWISTER_PATH environment variable is not set! Exiting!')
    exit(1)
if TWISTER_PATH not in sys.path:
    sys.path.append(TWISTER_PATH)


from common.constants  import *
from common.helpers    import *
from common.tsclogging import *
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


    def exposed_getLogLevel(self):
        """
        This doesn't require login.
        """
        logFull('CeRpyc:exposed_getLogLevel')
        return getLogLevel()


    def exposed_setLogLevel(self, Level):
        """
        Dinamically set log level.
        This doesn't require login.
        """
        logFull('CeRpyc:exposed_setLogLevel')
        return setLogLevel(Level)


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
        except Exception as e:
            logError('EE: Connect error: {}.'.format(e))

        logDebug('EE: Connected from `{}`.'.format(str_addr))


    def on_disconnect(self):
        """
        On client disconnect
        """
        logFull('CeRpyc:on_disconnect')
        str_addr = self._get_addr()

        hello = self.conns[str_addr].get('hello', '')
        stime = self.conns[str_addr].get('time', time.time())
        if hello: hello += ' - '

        # Unregister the eventual EPs for this connection
        if self.conns[str_addr].get('checked') and self.conns[str_addr].get('user'):
            eps = self.conns[str_addr].get('eps')
            if eps: self.unregisterEps(eps)

        # Delete everything for this address
        try:
            with self.conn_lock:
                del self.conns[str_addr]
        except Exception as e:
            logError('EE: Disconnect error: {}.'.format(e))

        logDebug('EE: Disconnected from `{}{}`, after `{:.2f}` seconds.'.format(
            hello, str_addr, (time.time() - stime)))


    @classmethod
    def _findConnection(self, usr=None, addr=[], hello='', epname=''):
        """
        Helper function to find the first address for 1 user,
        that matches the Address, the hello, or the Ep.
        Possible combinations are: (Addr & Hello), (Hello & Ep).
        The address will match the IP/ host; ex: ['127.0.0.1', 'localhost'].
        The hello should be: `client`, `ep`, or `lib`.
        The EP must be the name of the EP registered by a client;
        it returns the client, not the EP.
        """
        logFull('CeRpyc:_findConnection')
        if isinstance(self, CeRpycService):
            user = self._check_login()
        else:
            user = usr
        if not user: return False

        found = False

        # Cycle all active connections (clients, eps, libs, cli)
        for str_addr, data in self.conns.iteritems():
            # Skip invalid connections, without log-in
            if not data.get('user') or not data.get('checked'):
                continue
            # Will find the first connection match for the user
            if user == data['user'] and data['checked']:
                # Check (Addr & Hello)
                if (addr and hello) and str_addr.split(':')[0] in addr:
                    # If the Hello matches with the filter
                    if data.get('hello') and data['hello'].split(':') and data['hello'].split(':')[0] == hello:
                        found = str_addr
                        break
                # Check (Hello & Ep)
                elif (hello and epname) and data.get('hello') and data['hello'].split(':') and data['hello'].split(':')[0] == hello:
                    # If this connection has registered EPs
                    eps = data.get('eps')
                    if eps and epname in eps:
                        found = str_addr
                        break
                # All filters are null! Return the first conn for this user!
                elif not addr and not hello and not epname:
                    found = str_addr
                    break

        return found


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
        except Exception as e:
            logError('EE: Connect error: {}.'.format(e))

        logDebug('EE: Connected from `{}`.'.format(str_addr))


    def on_disconnect(self):
        """
        On client disconnect
        """
        logFull('CeRpyc:on_disconnect')
        str_addr = self._get_addr()

        hello = self.conns[str_addr].get('hello', '')
        stime = self.conns[str_addr].get('time', time.time())
        if hello: hello += ' - '

        # Unregister the eventual EPs for this connection
        if self.conns[str_addr].get('checked') and self.conns[str_addr].get('user'):
            eps = self.conns[str_addr].get('eps')
            if eps: self.unregisterEps(eps)

        # Delete everything for this address
        try:
            with self.conn_lock:
                del self.conns[str_addr]
        except Exception as e:
            logError('EE: Disconnect error: {}.'.format(e))

        logDebug('EE: Disconnected from `{}{}`, after `{:.2f}` seconds.'.format(
            hello, str_addr, (time.time() - stime)))


    def exposed_cherryAddr(self):
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
        if 'conn' in extra:     del extra['conn']
        if 'user' in extra:     del extra['user']
        if 'checked' in extra:  del extra['checked']
        if 'eps' in extra:
            # Only register the VALID eps...
            self.registerEps(extra['eps'])
            # and delete the invalid ones.
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
        resp = self.project.rpyc_check_passwd(user, passwd)

        user_home = userHome(user)
        if not os.path.exists('{}/twister'.format(user_home)):
            logError('*ERROR* Cannot find Twister for user `{}`, in path `{}/twister`!'.format(user, user_home))
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
        user  = self.conns[str_addr].get('user')
        if (not check) or (not user):
            return False
        else:
            return user


# # #


    def exposed_encryptText(self, text):
        """
        Encrypt a piece of text, using AES.
        """
        logFull('CeRpyc:exposed_encryptText')
        if not text: return ''
        user = self._check_login()
        if not user: return False
        return self.project.encryptText(user, text)


    def exposed_decryptText(self, text):
        """
        Decrypt a piece of text, using AES.
        """
        logFull('CeRpyc:exposed_decryptText')
        if not text: return ''
        user = self._check_login()
        if not user: return False
        return self.project.decryptText(user, text)


    def exposed_usrManager(self, cmd, name='', *args, **kwargs):
        """
        Manage users, groups and permissions.
        """
        logFull('CeRpyc:exposed_usrManager')
        user = self._check_login()
        if not user: return False
        return self.project.usersAndGroupsManager(user, cmd, name, args, kwargs)


    def exposed_listUsers(self, active=False):
        """
        Function called from the CLI, to list the users that are using Twister.
        """
        logFull('CeRpyc:exposed_listUsers')
        return self.project.listUsers(active)


    def exposed_getUserVariable(self, variable):
        """
        Send a user variable
        """
        logFull('CeRpyc:exposed_getUserVariable')
        user = self._check_login()
        if not user: return False
        data = self.project.getUserInfo(user, variable)
        if not data: return False
        return data


    def exposed_setUserVariable(self, key, variable):
        """
        Create or overwrite a user variable
        """
        logFull('CeRpyc:exposed_setUserVariable')
        user = self._check_login()
        if not user: return False
        return self.project.setUserInfo(user, key, variable)


    def exposed_getEpVariable(self, epname, variable):
        """
        Send an EP variable
        """
        logFull('CeRpyc:exposed_getEpVariable')
        user = self._check_login()
        if not user: return False
        data = self.project.getEpInfo(user, epname)
        if not data: return False
        return data.get(variable, False)


    def exposed_setEpVariable(self, epname, variable, value):
        """
        Create or overwrite an EP variable
        """
        logFull('CeRpyc:exposed_setEpVariable')
        user = self._check_login()
        if not user: return False
        return self.project.setEpInfo(user, epname, variable, value)


    def exposed_listSuites(self, epname):
        """
        List all suites for 1 EP, in the current project
        """
        logFull('CeRpyc:exposed_listSuites')
        user = self._check_login()
        if not user: return False
        if not epname: return False
        suiteList = [str(k)+':'+v['name'] for k, v in self.project.getEpInfo(user, epname)['suites'].items()]
        return ','.join(suiteList)


    def exposed_getSuiteVariable(self, epname, suite, variable):
        """
        Send a Suite variable
        """
        logFull('CeRpyc:exposed_getSuiteVariable')
        user = self._check_login()
        if not user: return False
        data = self.project.getSuiteInfo(user, epname, suite)
        if not data: return False
        return data.get(variable, False)


    def exposed_getFileVariable(self, epname, file_id, variable):
        """
        Send a file variable
        """
        logFull('CeRpyc:exposed_getFileVariable')
        user = self._check_login()
        if not user: return False
        data = self.project.getFileInfo(user, epname, file_id)
        if not data: return False
        return data.get(variable, False)


    def exposed_setFileVariable(self, epname, filename, variable, value):
        """
        Create or overwrite a file variable
        """
        logFull('CeRpyc:exposed_setFileVariable')
        user = self._check_login()
        if not user: return False
        return self.project.setFileInfo(user, epname, filename, variable, value)


# # #   Persistence   # # #


    def exposed_readFile(self, fpath, flag='r', fstart=0, type='fs'):
        """
        Read a file from TWISTER PATH, user's home folder, or ClearCase.
        Flag r/ rb = ascii/ binary.
        """
        user = self._check_login()
        if not user: return False
        resp = self.project.readFile(user, fpath, flag, fstart, type)
        if resp and resp.startswith('*ERROR*'):
            logWarning(resp)
        return resp


    def exposed_writeFile(self, fpath, fdata, flag='w', type='fs'):
        """
        Write a file in user's home folder, or ClearCase.
        Flag w/ wb = ascii/ binary.
        """
        user = self._check_login()
        if not user: return False
        resp = self.project.writeFile(user, fpath, fdata, flag, type)
        if resp != True:
            logWarning(resp)
        return resp


    def exposed_listSettings(self, config='', x_filter=''):
        """
        List all available settings, for 1 config of a user.
        """
        user = self._check_login()
        if not user: return False
        return self.project.listSettings(user, config, x_filter)


    def exposed_getSettingsValue(self, config, key):
        """
        Fetch a value from 1 config of a user.
        """
        user = self._check_login()
        if not user: return False
        return self.project.getSettingsValue(user, config, key)


    def exposed_setSettingsValue(self, config, key, value):
        """
        Set a value for a key in the config of a user.
        """
        user = self._check_login()
        if not user: return False
        return self.project.setSettingsValue(user, config, key, value)


    def exposed_delSettingsKey(self, config, key, index=0):
        """
        Del a key from the config of a user.
        """
        user = self._check_login()
        if not user: return False
        return self.project.delSettingsKey(user, config, key, index)


    def exposed_setPersistentSuite(self, suite, info={}, order=-1):
        """
        Create a new suite, using the INFO, at the position specified.\n
        This function writes in TestSuites.XML file.\n
        The changes will be available at the next START.
        """
        user = self._check_login()
        if not user: return False
        return self.project.setPersistentSuite(user, suite, info, order)


    def exposed_delPersistentSuite(self, suite):
        """
        Delete an XML suite, using a name ; if there are more suites with the same name,
        only the first one is deleted.\n
        This function writes in TestSuites.XML file.\n
        The changes will be available at the next START.
        """
        user = self._check_login()
        if not user: return False
        return self.project.delPersistentSuite(user, suite)


    def exposed_setPersistentFile(self, suite, fname, info={}, order=-1):
        """
        Create a new file in a suite, using the INFO, at the position specified.\n
        This function writes in TestSuites.XML file.\n
        The changes will be available at the next START.
        """
        user = self._check_login()
        if not user: return False
        return self.project.setPersistentFile(user, suite, fname, info, order)


    def exposed_delPersistentFile(self, suite, fname):
        """
        Delete an XML file from a suite, using a name ; if there are more files
        with the same name, only the first one is deleted.\n
        This function writes in TestSuites.XML file.\n
        The changes will be available at the next START.
        """
        user = self._check_login()
        if not user: return False
        return self.project.delPersistentFile(user, suite, fname)


# # #   Global Variables and Config Files   # # #


    def exposed_getGlobalVariable(self, var_path):
        """
        Global variables
        """
        logFull('CeRpyc:exposed_getGlobalVariable')
        user = self._check_login()
        if not user: return False
        return self.project.getGlobalVariable(user, var_path, False)


    def exposed_setGlobalVariable(self, var_path, value):
        """
        Global variables
        """
        logFull('CeRpyc:exposed_setGlobalVariable')
        user = self._check_login()
        if not user: return False
        return self.project.setGlobalVariable(user, var_path, value)


    def exposed_getConfig(self, cfg_path, var_path):
        """
        Config files
        """
        logFull('CeRpyc:exposed_getConfig')
        user = self._check_login()
        if not user: return False
        return self.project.getGlobalVariable(user, var_path, cfg_path)


# # #   Register / Start / Stop EPs   # # #


    def exposed_listEPs(self):
        """
        All known EPs for a user, read from project.
        The user is identified automatically.
        """
        logFull('CeRpyc:exposed_listEPs')
        user = self._check_login()
        if not user: return False
        eps = self.project.getUserInfo(user, 'eps').keys()
        return list(eps) # Best to make a copy


    @classmethod
    def exposed_registeredEps(self, user=None):
        """
        Return all registered EPs for all user clients.
        The user MUST be given as a parameter.
        """
        logFull('CeRpyc:exposed_registeredEps')
        if not user: return False
        eps = []

        for str_addr, data in self.conns.iteritems():
            # There might be more clients for a user...
            # And this Addr might be an EP, not a client
            if user is not None and user == data['user'] and data['checked']:
                # If this connection has registered EPs, append them
                e = data.get('eps')
                if e: eps.extend(e)

        return sorted(set(eps))


    def registerEps(self, eps):
        """
        Private function to register all EPs for a client.
        Only a VALID client will be able to register EPs!
        The user is identified automatically.
        """
        logFull('CeRpyc:registerEps')
        str_addr = self._get_addr()
        user = self._check_login()
        if not user: return False

        if not str_addr:
            logError('*ERROR* Cannot identify the remote address!')
            return False

        if not isinstance(eps, type([])):
            logError('*ERROR* Can only register a List of EP names!')
            return False
        else:
            eps = sorted(set(eps))

        logDebug('Begin to register EPs: {} ...'.format(eps))

        try:
            # Send a Hello and this IP to the remote proxy Service
            hello = self._conn.root.hello(self.project.ip_port[0])
        except Exception as e:
            trace = traceback.format_exc()[34:].strip()
            logError('Error: Register client error: {}'.format(trace))
            hello = False

        # If the Hello from the other end of the connection returned False...
        if not hello:
            logDebug('Could not send Hello to the Client Manager `{}` for user `{}`!'.format(str_addr, user))
            return False

        # Register the EPs to this unique client address.
        # On disconnect, this client address will be deleted
        # And the EPs will be automatically un-registered.
        with self.conn_lock:
            for epname in eps:
                self.project._registerEp(user, epname)

            # Before register, find the clients that have already registered these EPs!
            for c_addr, data in self.conns.iteritems():
                # Skip invalid connections, without log-in
                if not data.get('user') or not data.get('checked'):
                    continue
                # There might be more clients for a user. Must find all of them.
                if user == data['user']:
                    # This current Addr might be an EP, not a client
                    # If this connection has registered EPs
                    if not data.get('eps'): continue
                    old_eps   = set(data.get('eps'))
                    new_eps   = set(eps)
                    diff_eps  = old_eps - new_eps
                    intersect = old_eps & new_eps
                    if intersect:
                        logDebug('Un-register EP list {} from `{}` and register then on `{}`.'\
                                 ''.format(sorted(intersect), c_addr, str_addr))
                    # Delete the EPs that must be deleted
                    self.conns[c_addr]['eps'] = sorted(diff_eps)

            self.conns[str_addr]['eps'] = eps

        logInfo('Registered client manager for user `{}`\n\t-> Client from `{}` ++ {}.'.format(user, str_addr, eps))
        return True


    def unregisterEps(self, eps=[]):
        """
        Private, helper function to un-register some EPs for a client.
        The user is identified automatically.
        """
        logFull('CeRpyc:unregisterEps')
        str_addr = self._get_addr()
        user = self._check_login()
        if not user: return False

        if not str_addr:
            logError('*ERROR* Cannot identify the remote address!')
            return False

        if not isinstance(eps, type([])):
            logError('*ERROR* Can only un-register a List of EP names!')
            return False
        else:
            eps = set(eps)

        logDebug('Begin to un-register EPs: {} ...'.format(eps))

        with self.conn_lock:
            for epname in eps:
                self.project._unregisterEp(user, epname)

            data = self.conns[str_addr]
            ee = data.get('eps') or sorted(eps)
            if not ee:
                return True

        remaining = self.exposed_registeredEps(user)
        if remaining == ee:
            logInfo('Un-registered all EPs for user `{}`\n\t-> Client from `{}` -- {}.'\
                    ' No more EPs left for `{}` !'.format(user, str_addr, ee, user))
        else:
            logInfo('Un-registered EPs for user `{}`\n\t-> Client from `{}` -- {} !'.format(user, str_addr, ee))
        return True


    @classmethod
    def exposed_startEP(self, epname, usr=None):
        """
        Start EP for client.
        This must work from any ExecManager instance.
        """
        logFull('CeRpyc:exposed_startEP')
        if isinstance(self, CeRpycService):
            user = self._check_login()
        else:
            user = usr
        if not user: return False

        addr = self._findConnection(user, hello='client', epname=epname)

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
    def exposed_stopEP(self, epname, usr=None):
        """
        Stop EP for client.
        This must work from any ExecManager instance.
        """
        logFull('CeRpyc:exposed_stopEP')
        if isinstance(self, CeRpycService):
            user = self._check_login()
        else:
            user = usr
        if not user: return False

        addr = self._findConnection(user, hello='client', epname=epname)

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


    def exposed_queueFile(self, suite, fname):
        """
        Queue a file at the end of a suite, during runtime.
        If there are more suites with the same name, the first one is used.
        """
        logFull('CeRpyc:exposed_queueFile')
        user = self._check_login()
        if not user: return False
        return self.project.queueFile(user, suite, fname)


    def exposed_deQueueFiles(self, data):
        """
        Remove a file from the files queue.
        """
        logFull('CeRpyc:exposed_deQueueFiles')
        user = self._check_login()
        if not user: return False
        return self.project.deQueueFiles(user, data)


    def exposed_getEpStatus(self, epname):
        """
        Return execution status for one EP. (stopped, paused, running, invalid)
        """
        logFull('CeRpyc:exposed_getEpStatus')
        user = self._check_login()
        if not user: return False

        if epname not in self.project.getUserInfo(user, 'eps'):
            logDebug('*ERROR* Invalid EP name `{}` !'.format(epname))
            return False

        data = self.project.getEpInfo(user, epname)
        reversed = dict((v,k) for k,v in execStatus.iteritems())
        return reversed[data.get('status', 8)]


    def exposed_getEpStatusAll(self):
        """
        Return execution status for all EPs. (stopped, paused, running, invalid)
        """
        logFull('CeRpyc:exposed_getEpStatusAll')
        user = self._check_login()
        if not user: return False

        data = self.project.getUserInfo(user)
        reversed = dict((v,k) for k,v in execStatus.iteritems())
        return reversed[data.get('status', 8)]


    def exposed_setEpStatus(self, epname, new_status, msg=''):
        """
        Set execution status for one EP. (0, 1, 2, or 3)
        Returns a string (stopped, paused, running).
        The `message` parameter can explain why the status has changed.
        """
        logFull('CeRpyc:exposed_setEpStatus')
        user = self._check_login()
        if not user: return False
        return self.project.setExecStatus(user, epname, new_status, msg)


    def exposed_setEpStatusAll(self, new_status, msg=''):
        """
        Set execution status for all EPs. (STATUS_STOP, STATUS_PAUSED, STATUS_RUNNING)
        Returns a string (stopped, paused, running).
        The `message` parameter can explain why the status has changed.
        """
        logFull('CeRpyc:exposed_setEpStatusAll')
        user = self._check_login()
        if not user: return False
        return self.project.setExecStatusAll(user, new_status, msg)


    def exposed_getFileStatusAll(self, epname=None, suite=None):
        """
        Returns a list with all statuses, for all files, in order.
        The status of one file can be obtained with ce.getFileVariable.
        """
        logFull('CeRpyc:exposed_getFileStatusAll')
        user = self._check_login()
        if not user: return False
        return self.project.getFileStatusAll(user, epname, suite)


    def exposed_setFileStatus(self, epname, file_id, new_status=10, time_elapsed=0.0):
        """
        Set status for one file and write in log summary.
        Called from the Runner.
        """
        logFull('CeRpyc:exposed_setFileStatus')
        user = self._check_login()
        if not user: return False
        return self.project.setFileStatus(user, epname, file_id, new_status, time_elapsed)


    def exposed_setFileStatusAll(self, epname, new_status):
        """
        Reset file status for all files of one EP.
        Called from the Runner.
        """
        logFull('CeRpyc:exposed_setFileStatusAll')
        user = self._check_login()
        if not user: return False
        return self.project.setFileStatusAll(user, epname, new_status)


# # #   Download Files and Libraries   # # #


    def exposed_listLibraries(self, all=True):
        """
        Returns the list of exposed libraries, from CE libraries folder.
        This list will be used to syncronize the libs on all EP computers.
        """
        logFull('CeRpyc:exposed_listLibraries')
        user = self._check_login()
        if not user: return False
        return self.project.getLibrariesList(user, all)


    def exposed_downloadLibrary(self, name):
        """
        Sends required library to the EP, to be syncronized.
        The library can be global for all users, or per user.
        """
        logFull('CeRpyc:exposed_downloadLibrary')
        user = self._check_login()
        if not user: return False

        # Global lib path
        glob_lib_path = (TWISTER_PATH + '/lib/' + name).replace('//', '/')

        def _download_file(fpath):
            """
            Just read a file.
            """
            import tarfile
            import cStringIO

            if not os.path.exists(fpath):
                err = '*ERROR* Invalid path `{}`!'.format(fpath)
                return err

            root, name = os.path.split(fpath)

            if os.path.isfile(fpath):
                try:
                    with open(fpath, 'rb') as f:
                        logDebug('User `{}` requested global lib file `{}`.'.format(user, name))
                        return f.read()
                except Exception as e:
                    err = '*ERROR* Cannot read file `{}`! {}'.format(fpath, e)
                    return err

            else:
                os.chdir(root)
                io = cStringIO.StringIO()
                # Write the folder tar.gz into memory
                with tarfile.open(fileobj=io, mode='w:gz') as binary:
                    binary.add(name=name, recursive=True)
                logDebug('User `{}` requested global lib folder `{}`.'.format(user, name))
                return io.getvalue()

        # Auto detect if ClearCase Test Config Path is active
        ccConfig = self.project.getClearCaseConfig(user, 'libs_path')
        if ccConfig:
            view = ccConfig['view']
            path = ccConfig['path'].rstrip('/')
            lib_path = path +'/'+ name
            sz = self.project.clearFs.fileSize
            # Folder
            if sz == 4096:
                resp = self.project.clearFs.targzUserFolder(user +':'+ view, lib_path)
                # Read as ROOT
                if resp.startswith('*ERROR*'):
                    return _download_file(glob_lib_path)
                logDebug('User `{}` requested ClearCase lib folder `{}`.'.format(user, name))
                return resp
            # File
            else:
                resp = self.project.clearFs.readUserFile(user +':'+ view, lib_path)
                # Read as ROOT
                if resp.startswith('*ERROR*'):
                    return _download_file(glob_lib_path)
                logDebug('User `{}` requested ClearCase lib file `{}`.'.format(user, name))
                return resp

        # Normal system path
        else:
            lib_path = self.project.getUserInfo(user, 'libs_path').rstrip('/') +'/'+ name
            # If is file, read the file directly
            if os.path.isfile(lib_path):
                resp = self.project.localFs.readUserFile(user, lib_path)
                # Read as ROOT
                if resp.startswith('*ERROR*'):
                    return _download_file(glob_lib_path)
                logDebug('User `{}` requested local lib file `{}`.'.format(user, name))
                return resp
            # If is folder, compress in memory and return the data
            else:
                resp = self.project.localFs.targzUserFolder(user, lib_path)
                # Read as ROOT
                if resp.startswith('*ERROR*'):
                    return _download_file(glob_lib_path)
                logDebug('User `{}` requested local lib folder `{}`.'.format(user, name))
                return resp


    def exposed_getEpFiles(self, epname):
        """
        Returns all files that must be run on one EP.
        """
        logFull('CeRpyc:exposed_getEpFiles')
        user = self._check_login()
        if not user: return False
        try: data = self.project.getEpFiles(user, epname)
        except: data = False
        return data


    def exposed_getSuiteFiles(self, epname, suite):
        """
        Returns all files that must be run on one Suite ID.
        """
        logFull('CeRpyc:exposed_getSuiteFiles')
        user = self._check_login()
        if not user: return False
        try: data = self.project.getSuiteFiles(user, epname, suite)
        except: data = False
        return data


    def exposed_downloadFile(self, epname, file_info):
        """
        Sends requested file to the EP, to be executed.
        """
        logFull('CeRpyc:exposed_downloadFile')
        user = self._check_login()
        if not user: return False

        if epname not in self.project.getUserInfo(user, 'eps'):
            logDebug('*ERROR* Invalid EP name `{}` !'.format(epname))
            return False

        tests_path = self.project.getUserInfo(user, 'tests_path')

        # If this is a test file path
        if os.path.isfile(tests_path + os.sep + file_info):
            filename = tests_path + os.sep + file_info

        # If this is a file ID
        else:
            file_id = file_info
            data = self.project.getFileInfo(user, epname, file_id)
            if not data:
                logError('*ERROR* Invalid File ID `{}` !'.format(file_id))
                return False

            filename = data['file']

            # Auto detect if ClearCase Test Config Path is active
            ccConfig = self.project.getClearCaseConfig(user, 'tests_path')
            if ccConfig and data.get('clearcase'):
                view = ccConfig['view']
                # Read ClearCase TestCase file
                text = self.project.readFile(user, filename, type='clearcase:' + view)
                tags = re.findall('^[ ]*?[#]*?[ ]*?<(?P<tag>\w+)>([ -~\n]+?)</(?P=tag)>', text, re.MULTILINE)
                # File description
                descr = '<br>\n'.join(['<b>' + title + '</b> : ' + descr.replace('<', '&lt;') for title, descr in tags])
                cctag = '<b>ClearCase Version</b> :'
                if descr and (descr.find(cctag) != -1):
                    pos = descr.find(cctag) + len(cctag)
                    rev = descr[pos:].strip()
                    # Set TC Revision variable
                    self.project.setFileInfo(user, epname, file_id, 'twister_tc_revision', rev)
                logDebug('Execution process `{}:{}` requested ClearCase file `{}`.'.format(user, epname, filename))
                return text
            # End of ClearCase hack !

            # Fix ~ $HOME path (from project XML)
            if filename.startswith('~'):
                filename = userHome(user) + filename[1:]
            # Fix incomplete file path (from project XML)
            if not os.path.isfile(filename):
                filename = tests_path + os.sep + filename

        logDebug('Execution process `{}:{}` requested file `{}`.'.format(user, epname, filename))

        return self.project.localFs.readUserFile(user, filename, 'rb')


# # #   Plugins   # # #


    def exposed_listPlugins(self):
        """
        List all user plugins.
        """
        logFull('CeRpyc:exposed_listPlugins')
        user = self._check_login()
        if not user: return False
        parser = PluginParser(user)
        pluginsList = parser.getPlugins()
        logFull('List Plug-ins: user `{}` has: {}.'.format(user, pluginsList))
        return pluginsList.keys()


    def exposed_runPlugin(self, plugin, args):
        """
        Exposed API for running plug-ins from Execution Processes.
        """
        logFull('CeRpyc:exposed_runPlugin')
        user = self._check_login()
        if not user: return False

        # If argument is a valid dict, pass
        try:
            args = dict(args)
        except:
            return '*ERROR* Invalid type of argument for plugin `{}` : {} !'.format(plugin, type(args))

        if not 'command' in args:
            return '*ERROR* Invalid dictionary for plugin `{}` : {} !'.format(plugin, args)

        plugin_p = self.project._buildPlugin(user, plugin)

        if not plugin_p:
            msg = '*ERROR* Plugin `{}` does not exist for user `{}`!'.format(plugin, user)
            logError(msg)
            return msg

        try:
            return plugin_p.run(args)
        except Exception as e:
            trace = traceback.format_exc()[34:].strip()
            logError('*ERROR* Plugin `{}`, ran with arguments `{}` and raised Exception: `{}`!'\
                     .format(plugin, args, trace))
            return 'Error on running plugin `{}` - Exception: `{}`!'.format(plugin, e)


# # #   Logs   # # #


    def exposed_getLogFile(self, read, fstart, filename):
        """
        Used to show the logs.
        """
        logFull('CeRpyc:exposed_getLogFile')
        user = self._check_login()
        if not user: return False
        return self.project.getLogFile(user, read, fstart, filename)


    def exposed_logMessage(self, logType, logMessage):
        """
        This function is exposed in all tests and all logs are centralized in the HOME of the user.
        In order for the user to be able to access the logs written by CE, which runs as ROOT,
        CE will start a small process in the name of the user and the process will write the logs.
        """
        logFull('CeRpyc:exposed_logMessage')
        user = self._check_login()
        if not user: return False
        return self.project.logMessage(user, logType, logMessage)


    def exposed_logLIVE(self, epname, logMessage):
        """
        Writes CLI messages in a big log, so all output can be checked LIVE.
        """
        logFull('CeRpyc:exposed_logLIVE')
        user = self._check_login()
        if not user: return False
        return self.project.logLIVE(user, epname, logMessage)


    def exposed_resetLog(self, logName):
        """
        Resets one log.
        """
        logFull('CeRpyc:exposed_resetLog')
        user = self._check_login()
        if not user: return False
        return self.project.resetLog(user, logName)


    def exposed_resetLogs(self):
        """
        All logs defined in master config are erased.\n
        """
        logFull('CeRpyc:exposed_resetLogs')
        user = self._check_login()
        if not user: return False
        return self.project.resetLogs(user)


# # #   Resource Allocator   # # #


    def exposed_getResource(self, query):
        logFull('CeRpyc:exposed_getResource')
        user = self._check_login()
        if not user: return False
        try: return self.project.ra.getResource(query=query, props={'__user': user})
        except: return False


    def exposed_setResource(self, name, parent=None, props={}):
        logFull('CeRpyc:exposed_setResource')
        user = self._check_login()
        if not user: return False
        props = dict(props) ; props.update({'__user': user})
        return self.project.ra.setResource(name, parent, props)


    def exposed_renameResource(self, res_query, new_name):
        logFull('CeRpyc:exposed_renameResource')
        user = self._check_login()
        if not user: return False
        return self.project.ra.renameResource(res_query, new_name, props={'__user': user})


    def exposed_deleteResource(self, query):
        logFull('CeRpyc:exposed_deleteResource')
        user = self._check_login()
        if not user: return False
        return self.project.ra.deleteResource(query, props={'__user': user})


    def exposed_getSut(self, query):
        logFull('CeRpyc:exposed_getSut')
        user = self._check_login()
        if not user: return False
        try: return self.project.ra.getSut(query=query, props={'__user': user})
        except: return False


    def exposed_setSut(self, name, parent=None, props={}):
        logFull('CeRpyc:exposed_setSut')
        user = self._check_login()
        if not user: return False
        props = dict(props) ; props.update({'__user': user})
        return self.project.ra.setSut(name, parent, props)


    def exposed_renameSut(self, res_query, new_name):
        logFull('CeRpyc:exposed_renameSut')
        user = self._check_login()
        if not user: return False
        return self.project.ra.renameSut(res_query, new_name, props={'__user': user})


    def exposed_deleteSut(self, query):
        logFull('CeRpyc:exposed_deleteSut')
        user = self._check_login()
        if not user: return False
        return self.project.ra.deleteSut(query, props={'__user': user})


    def exposed_isResourceReserved(self, query):
        logFull('CeRpyc:exposed_isResourceReserved')
        #user = self._check_login()
        #if not user: return False
        return self.project.ra.isResourceReserved(query)


    def exposed_isSutReserved(self, query):
        logFull('CeRpyc:exposed_isSutReserved')
        #user = self._check_login()
        #if not user: return False
        return self.project.ra.isSutReserved(query)


    def exposed_reserveResource(self, query):
        logFull('CeRpyc:exposed_reserveResource')
        user = self._check_login()
        if not user: return False
        return self.project.ra.reserveResource(query, props={'__user': user})


    def exposed_reserveSut(self, query):
        logFull('CeRpyc:exposed_reserveSut')
        user = self._check_login()
        if not user: return False
        return self.project.ra.reserveSut(query, props={'__user': user})


    def exposed_saveAndReleaseReservedResource(self, query):
        logFull('CeRpyc:exposed_saveAndReleaseReservedResource')
        user = self._check_login()
        if not user: return False
        return self.project.ra.saveAndReleaseReservedResource(query, props={'__user': user})


    def exposed_saveReservedResource(self, query):
        logFull('CeRpyc:exposed_saveReservedResource')
        user = self._check_login()
        if not user: return False
        return self.project.ra.saveReservedResource(query, props={'__user': user})


    def exposed_saveReservedResourceAs(self, name, query):
        logFull('CeRpyc:exposed_saveReservedResourceAs')
        user = self._check_login()
        if not user: return False
        return self.project.ra.saveReservedResourceAs(name, query, props={'__user': user})


    def exposed_saveReservedSutAs(self, name, query):
        logFull('CeRpyc:exposed_saveReservedSutAs')
        user = self._check_login()
        if not user: return False
        return self.project.ra.saveReservedSutAs(name, query, props={'__user': user})


    def exposed_saveReservedSut(self, query):
        logFull('CeRpyc:exposed_saveReservedSut')
        user = self._check_login()
        if not user: return False
        return self.project.ra.saveReservedSut(query, props={'__user': user})


    def exposed_saveAndReleaseReservedSut(self, query):
        logFull('CeRpyc:exposed_saveAndReleaseReservedSut')
        user = self._check_login()
        if not user: return False
        return self.project.ra.saveAndReleaseReservedSut(query, props={'__user': user})


    def exposed_discardAndReleaseReservedResource(self, query):
        logFull('CeRpyc:exposed_discardAndReleaseReservedResource')
        user = self._check_login()
        if not user: return False
        return self.project.ra.discardAndReleaseReservedResource(query, props={'__user': user})


    def exposed_discardAndReleaseReservedSut(self, query):
        logFull('CeRpyc:exposed_discardAndReleaseReservedSut')
        user = self._check_login()
        if not user: return False
        return self.project.ra.discardAndReleaseReservedSut(query, props={'__user': user})


# Eof()
