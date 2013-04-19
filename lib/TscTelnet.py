# File: TscTelnet.py ; This file is part of Twister.

# version: 2.001
#
# Copyright (C) 2012 , Luxoft
#
# Authors:
#    Adrian Toader <adtoader@luxoft.com>
#
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from telnetlib import Telnet
from time import sleep
#from time import time as epochtime
from thread import start_new_thread
#from os import remove, rename
#from os.path import dirname, exists, abspath, join, getsize
#Efrom json import load, dump




#__dir__ = dirname(abspath(__file__))


class TelnetManager(object):
    """ Twister Telnet connections manager """

    def __init__(self):
        """ init """

        # connections are TelnetConnection instances
        self.connections = {}

        # active connection name; is used for all commands as default
        # if no name is specified
        self.activeConnection = None


    def open_connection(self, name, host, port=23, user=None, password=None,
                        userExpect=None, passwordExpect=None, keepalive=True):
        """ open a new TelnetConnection instance and add it to manager list """

        if not self.connections.has_key(name):
            connection = TelnetConnection(name, host, port, user, password,
                                            userExpect, passwordExpect, keepalive)
            self.connections.update([(name, connection), ])

            return True

        else:
            print('telnet open connection error: connection name already in use')

            return False

    def login(self, name, user=None, password=None,
                     userExpect=None, passwordExpect=None):
        """ login on telnet connection """

        try:
            return self.connections[name].login(user, password,
                                            userExpect, passwordExpect)

        except Exception, e:
            print('telnet manager login error: {er}'.format(er=e))

            return False

    def write(self, command, name=None):
        """ write command to telnet connection """

        if ((not name and not self.activeConnection) or
                (name and not self.connections.has_key(name))):
            print 'connection not found'
            return False

        if name:
            return self.connections[name].write(command)
        elif self.activeConnection:
            return self.connections[self.activeConnection].write(command)

        return False

    def read(self, name=None):
        """ read from telnet connection """

        if ((not name and not self.activeConnection) or
                (name and not self.connections.has_key(name))):
            print 'connection not found'
            return False

        if name:
            return self.connections[name].read()
        elif self.activeConnection:
            return self.connections[self.activeConnection].read()

        return False

    def read_until(self, expected, name=None):
        """ read from telnet connection until expected """

        if ((not name and not self.activeConnection) or
                (name and not self.connections.has_key(name))):
            print 'connection not found'
            return False

        if name:
            return self.connections[name].read_until(expected)
        elif self.activeConnection:
            return self.connections[self.activeConnection].read_until(expected)

        return False

    def set_newline(self, newline, name=None):
        """ set the new line char for telnet connection """

        if ((not name and not self.activeConnection) or
                (name and not self.connections.has_key(name))):
            print 'connection not found'
            return False

        if name:
            return self.connections[name].set_newline(newline)
        elif self.activeConnection:
            return self.connections[self.activeConnection].set_newline(newline)

        return False

    def set_timeout(self, timeout, name=None):
        """ set timeout for operations on telnet connection """

        if ((not name and not self.activeConnection) or
                (name and not self.connections.has_key(name))):
            print 'connection not found'
            return False

        if name:
            return self.connections[name].set_timeout(timeout)
        elif self.activeConnection:
            return self.connections[self.activeConnection].set_timeout(timeout)

        return False

    def get_connection(self, name=None):
        """ get the TelnetConnection instance """

        if ((not name and not self.activeConnection) or
                (name and not self.connections.has_key(name))):
            print 'connection not found'
            return False

        if name:
            return self.connections[name]
        elif self.activeConnection:
            return self.connections[self.activeConnection]

        return False

    def set_active_connection(self, name):
        """ set the active connection """

        if not self.connections.has_key(name):
            print 'connection not found'
            return False

        self.activeConnection = name
        return True

    def list_connections(self):
        """ list all connections """

        return [name for name in self.connections.iterkeys()]

    def close_connection(self, name=None):
        """ close connection """

        if ((not name and not self.activeConnection) or
                (name and not self.connections.has_key(name))):
            print 'connection not found'
            return False

        if not name and self.activeConnection:
            del(self.connections[self.activeConnection])

            self.activeConnection = None

            return True

        try:
            del(self.connections[name])

            if name == self.activeConnection:
                self.activeConnection = None
        except Exception, e:
            print('telnet manager error while closing connection: {er}'.format(er=e))

            return False

        return True

    def close_all_connections(self):
        """ close all connections """

        del(self.connections)
        self.connections = {}

        self.activeConnection = None

        print('all connections closed')

        return True


class TelnetConnection:
    """ tsc telnet connection """

    def __init__(self, name, host, port=23, user=None, password=None,
                    userExpect=None, passwordExpect=None, keepalive=True):
        """ init """

        self.connection = None
        self.host = host
        self.port = port
        self.loginAccount = {
            'user': user,
            'password': password
        }
        self.name = name
        self.newline = '\n'

        self.timeout = 4
        self.keepAliveRetries = 0
        self.keepAliveThread = None
        self.keepAlive = keepalive

        self.loginDriver = {
            'userExpect': userExpect,
            'passwordExpect': passwordExpect
        }
        """
        self.loginDrivers = None
        self.loginDriversPath = join(__dir__, 'logindrivers.list')
        self.loginDriversLockPath = join(__dir__, 'logindrivers.lock')
        self.loadLoginDrivers()
        """
        try:
            self.connection = Telnet(self.host, self.port, self.timeout)
            print('telnet connection created!')

            self.login()
            if self.keepAlive:
                self.keepAliveThread = start_new_thread(self.keep_alive, ())
            else:
                self.keepAliveThread = None
        except Exception, e:
            self.connection = None
            self.keepAliveThread = None
            print('telnet connection failed: {er}'.format(er=e))


    def __del__(self):
        """ delete """

        if self.connection:
            self.connection.close()
        sleep(2)
        del(self)


    def keep_alive(self):
        """ keep connection alive """

        timeout = (0.2, self.timeout)[self.timeout>2]
        while not self.connection.eof:
            self.connection.write('')
            sleep(timeout)


    def alive(self):
        """ check if connection is alive """

        if self.connection and not self.connection.eof:

            return True

        try:
            self.connection = Telnet(self.host, self.port)
            print('telnet connection created!')

            self.login()
            if self.keepAlive:
                self.keepAliveThread = start_new_thread(self.keep_alive, ())
            else:
                self.keepAliveThread = None
        except Exception, e:
            self.connection = None
            self.keepAliveThread = None
            self.keepAliveRetries += 1
            if self.keepAliveRetries > 4:
                print('telnet connection restore retry failed!')

                return False

            print('telnet connection restore failed: {er}'\
                    'retry: {n}!'.format(er=e, n=self.keepAliveRetries))
            self.alive()
        return True


    def set_newline(self, newline):
        """ set the new line char for telnet connection """

        if isinstance(newline, str):
            self.newline = newline
            return True

        return False


    def set_timeout(self, timeout):
        """ set timeout for operations on telnet connection """

        if isinstance(timeout, int):
            self.timeout = [2, timeout][timeout > 2]
            return True

        return False


    def read(self):
        """ read from telnet connection """

        if not self.alive():
            return False

        try:
            response = self.connection.read_very_eager()
            if response:
                return response

        except Exception, e:
            print('read command error: {er}'.format(er=e))
            return False

        return False


    def read_until(self, expected):
        """ read from telnet connection until expected """

        if not self.alive():
            return False

        try:
            response = self.connection.read_until(expected, self.timeout)
            if response:
                print(response)

                return True

        except Exception, e:
            print('read until command error: {er}'.format(er=e))
            return False

        return False


    def write(self, command, result=True, display=True):
        """ write command to telnet connection """

        if not self.alive():
            return False

        try:
            self.connection.write( str(command) + self.newline )
            sleep(2)
            if display: print('command: {c}'.format(c=command))
            if result:
                return self.connection.read_very_eager()

            else:
                return True

        except Exception, e:
            print('send command error: {er}'.format(er=e))

            return False


    def expect(self, expected, command=None, result=True, display=True):
        """ write command to telnet connection on expected prompt """

        if not self.alive():
            return False

        try:
            response = self.connection.read_until(expected, self.timeout)
            print(response)
            if response:
                if command:
                    self.connection.write( str(command) + self.newline)
                    sleep(2)
                    if display: print('command: {c}'.format(c=command))

                if result:
                    return self.connection.read_very_eager()
                else:
                    return True

            return False

        except Exception, e:
            print('expect send command error: {er}'.format(er=e))

            return False


    def login(self, user=None, password=None,
                     userExpect=None, passwordExpect=None):
        """ login on telnet connection """

        if not self.alive():

            return False

        self.loginAccount['user'] = (user,
                                        self.loginAccount['user'])[user is None]
        self.loginAccount['password'] = (password,
                                self.loginAccount['password'])[password is None]
        self.loginDriver['userExpect'] = (userExpect,
                            self.loginDriver['userExpect'])[userExpect is None]
        self.loginDriver['passwordExpect'] = (passwordExpect,
                    self.loginDriver['passwordExpect'])[passwordExpect is None]

        print('login ..')

        if None in [self.loginAccount['user'], self.loginAccount['password']]:
            print('no login data!')

            return False

        if None in [self.loginDriver['userExpect'],
                        self.loginDriver['passwordExpect']]:
            print('no login expected data!')

            return False #return self.autologin()

        response = self.expect(self.loginDriver['userExpect'],
                                    self.loginAccount['user'], False)
        if response:
            response = self.expect(self.loginDriver['passwordExpect'],
                                        self.loginAccount['password'],
                                                        True, False)
            if response:
                print(response)
                """
                if ((self.loginDriver['userExpect'] not in
                    self.loginDrivers['userExpect'] or
                    self.loginDriver['passwordExpect'] not in
                    self.loginDrivers['passwordExpect'])
                    and not None in self.loginDriver.itervalues()):
                    self.saveLoginDrivers(self.loginDriver['userExpect'],
                                        self.loginDriver['passwordExpect'])
                """
                return True

        print('fail')
        return False

    """
    def autologin(self):
        # autologin on telnet connection

        print('tring autologin ..')
        response = self.connection.expect(self.loginDrivers['userExpect'],
                                                                self.timeout)
        if not None in response:
            print(response)
            self.write(self.loginAccount['user'], False)
            response = self.connection.expect(
                                    self.loginDrivers['passwordExpect'],
                                                                self.timeout)

            if not None in response:
                print(response)
                print self.write(self.loginAccount['password'], True, False)

                return True

        print('fail')
        return False


    def loadLoginDrivers(self):
        # load the known login drivers

        retries = 0
        while exists(self.loginDriversLockPath) and retries <= self.timeout * 2:
            retries += 1
            sleep(0.4)

        with open(self.loginDriversLockPath, 'wb+') as loginDriversLockFile:
            loginDriversLockFile.write('lock\n')

        if not exists(self.loginDriversPath):
            with open(self.loginDriversPath, 'wb+') as loginDriversFile:
                self.loginDrivers = {}
                self.loginDrivers['userExpect'] = []
                self.loginDrivers['passwordExpect'] = []
                dump(self.loginDrivers, loginDriversFile)

        if getsize(self.loginDriversPath) > 524288L:
            rename(self.loginDriversPath,
                            self.loginDriversPath + '.bck' + str(epochtime()))

        with open(self.loginDriversPath, 'rb') as loginDriversFile:
            self.loginDrivers = load(loginDriversFile)

        remove(self.loginDriversLockPath)


    def saveLoginDrivers(self, userExpect, passwordExpect):
        # save new login driver

        retries = 0
        while exists(self.loginDriversLockPath) and retries <= self.timeout * 2:
            retries += 1
            sleep(0.4)

        with open(self.loginDriversLockPath, 'wb+') as loginDriversLockFile:
            loginDriversLockFile.write('lock\n')

        with open(self.loginDriversPath, 'rb') as loginDriversFile:
            self.loginDrivers = load(loginDriversFile)

        self.loginDrivers['userExpect'].append(userExpect)
        self.loginDrivers['passwordExpect'].append(passwordExpect)

        with open(self.loginDriversPath, 'wb+') as loginDriversFile:
            dump(self.loginDrivers, loginDriversFile)

        remove(self.loginDriversLockPath)
    """
