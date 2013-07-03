# File: TscSsh.py ; This file is part of Twister.

# version: 1.0
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


from time import sleep

from paramiko import Transport




class SshManager(object):
    """ Twister SSH connections manager """

    def __init__(self):
        """ init """

        # connections are paramiko.SSHClient instances
        self.connections = {}

        # active connection name; is used for all commands as default
        # if no name is specified
        self.activeConnection = None


    def open_connection(self, name, host, user=None, password=None, port=22):
        """ open a new paramiko.Transport instance and add it to manager list """

        if not self.connections.has_key(name):
            connection = SshConnection(name, host, port, user, password)
            self.connections.update([(name, connection), ])

            return True

        else:
            print('ssh open connection error: connection name already in use')

            return False

    def write(self, command, name=None):
        """ write command to ssh connection """

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
        """ read from ssh connection """

        if ((not name and not self.activeConnection) or
                (name and not self.connections.has_key(name))):
            print 'connection not found'
            return False

        if name:
            return self.connections[name].read()
        elif self.activeConnection:
            return self.connections[self.activeConnection].read()

        return False

    def set_timeout(self, timeout, name=None):
        """ set timeout for operations on ssh connection """

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
        """ get the SshConnection instance """

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

        if name:
            del(self.connections[name])

            if name == self.activeConnection:
                self.activeConnection = None

            return True
        elif self.activeConnection:
            del(self.connections[self.activeConnection])

            self.activeConnection = None

            return True

        return False

    def close_all_connections(self):
        """ close all connections """

        del(self.connections)
        self.connections = {}

        self.activeConnection = None

        print('all connections closed')

        return True


class SshConnection:
    """ tsc ssh connection """

    def __init__(self, name, host, port=22, user=None, password=None):
        """ init """

        self.connection = None
        self.session = None
        self.host = host
        self.port = port
        self.loginAccount = {
            'user': user,
            'pass': password
        }
        self.name = name
        self.timeout = 4

        self.nbytes = 4096

        try:
            self.connection =  Transport((self.host, self.port))
            self.connection.connect(username=self.loginAccount['user'],
                                    password=self.loginAccount['pass'])
            self.connection.set_keepalive(self.timeout)
            self.session = self.connection.open_channel(kind='session')

            print('ssh connection created!')
        except Exception, e:
            self.__del__()
            print('telnet connection failed: {er}'.format(er=e))


    def __del__(self):
        """ delete """

        if self.session:
            self.session.close()
            if self.session.exit_status_ready():
                print 'exit status: ', self.session.recv_exit_status()
        if self.connection:
            self.connection.close()
        sleep(2)
        del(self)


    def set_timeout(self, timeout):
        """ set timeout for operations on ssh connection """

        if isinstance(timeout, int):
            self.timeout = [0, timeout][timeout > 0]
            return True

        return False


    def read(self):
        """ read from ssh connection """

        if not self.session or not self.session.active:
            return False

        if self.session.recv_stderr_ready():
            print self.session.recv_stderr(self.nbytes)

        if self.session.recv_ready():
            return self.session.recv(self.nbytes)

        return False


    def write(self, command, result=True):
        """ write command to ssh connection """

        if not self.session or not self.session.active:
            return False

        self.session.exec_command(command)

        if self.session.recv_stderr_ready():
            print self.session.recv_stderr(self.nbytes)

        if result:
            sleep(2)
            if self.session.recv_ready():
                return self.session.recv(self.nbytes)

        return False
