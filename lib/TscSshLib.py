# File: TscSshLib.py ; This file is part of Twister.

# version: 2.002
#
# Copyright (C) 2012-2013 , Luxoft
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


"""
    This module contains SSH connection functions.
"""


import time

import paramiko

__all__ = ['SshManager', 'SshConnection', 'SshShell']

#

class SshManager(object):
    """ Twister SSH connections manager """

    def __init__(self):
        """ init """

        # connections are paramiko.SSHClient instances
        self.connections = dict()

        # active connection name; is used for all commands as default
        # if no name is specified
        self.activeConnection = None


    def open_connection(self, name, host, user=None, password=None, port=22, _type='shell'):
        """ open a new paramiko.Transport instance and add it to manager list """

        if not _type in ['shell', 'session']:
            return False

        if not self.connections.has_key(name) and _type == 'shell':
            connection = SshShell(name, host, port, user, password)
            self.connections.update([(name, connection), ])

            return True
        elif not self.connections.has_key(name) and _type == 'session':
            connection = SshConnection(name, host, port, user, password)
            self.connections.update([(name, connection), ])

            return True

        else:
            print('ssh open connection error: connection name already in use')

            return False

    def write(self, command, result=True, name=None):
        """ write command to ssh connection """

        if ((not name and not self.activeConnection) or
                (name and not self.connections.has_key(name))):
            print 'connection not found'
            return False

        if name:
            return self.connections[name].write(command, result)
        elif self.activeConnection:
            return self.connections[self.activeConnection].write(command, result)

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
        self.timeout = 2

        self.nbytes = 4096

        try:
            self.connection = paramiko.Transport((self.host, self.port))
            self.connection.connect(username=self.loginAccount['user'],
                                    password=self.loginAccount['pass'])
            self.connection.set_keepalive(self.timeout)
            #self.session = self.connection.open_channel(kind='session')

            print('ssh connection created!')
        except Exception as e:
            self.__del__()
            print('ssh connection failed: {er}'.format(er=e))


    def __del__(self):
        """ delete """

        if self.session:
            self.session.close()
            if self.session.exit_status_ready():
                print 'exit status: ', self.session.recv_exit_status()
        if self.connection:
            self.connection.close()
        time.sleep(2)
        del(self)


    def set_timeout(self, timeout):
        """ set timeout for operations on ssh connection """

        if isinstance(timeout, int):
            self.timeout = [0, timeout][timeout > 0]
            return True

        return False


    def read(self):
        """ read from ssh connection """

        self.session = self.connection.open_channel(kind='session')

        if not self.session or not self.session.active:
            return False

        d1 = time.time()
        while not self.session.recv_ready():
            time.sleep(2)

            d2 = time.time()
            if int(d2 - d1) > self.timeout:
                break

        if self.session.recv_stderr_ready():
            print self.session.recv_stderr(self.nbytes)

        if self.session.recv_ready():
            return self.session.recv(self.nbytes)

        if self.session.exit_status_ready():
            return False

        return False


    def write(self, command, result=True):
        """ write command to ssh connection """

        self.session = self.connection.open_channel(kind='session')

        if not self.session or not self.session.active:
            return False

        self.session.exec_command(command)

        if result:
            return self.read()

        return False


class SshShell:
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
        self.timeout = 0.2

        self.nbytes = 4096
        self.prompt = ''

        try:
            self.connection = paramiko.SSHClient()
            self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.connection.connect(host,
                                    username=self.loginAccount['user'],
                                    password=self.loginAccount['pass'])
            self.session = self.connection.invoke_shell(term='xterm', width=256, height=24)
            self.session.settimeout(self.timeout)
            self.setPrompt()

            print('CC_LIB: ssh connection created!')
        except Exception as e:
            print('CC_LIB: ssh connection failed: {er}'.format(er=e))


    def __del__(self):
        """ delete """

        if self.session:
            self.session.close()
            if self.session.exit_status_ready():
                print 'CC_LIB: exit status: ', self.session.recv_exit_status()
        if self.connection:
            self.connection.close()
        time.sleep(2)
        del(self)


    def set_timeout(self, timeout):
        """ set timeout for operations on ssh connection """

        if isinstance(timeout, int):
            self.timeout = [0, timeout][timeout > 0]
            if self.session:
                self.session.settimeout(self.timeout)
            return True

        return False


    def read(self, timeout=True, prompt_set=True):
        """  read from ssh connection """

        if not self.session or not self.session.active:
            return False

        if self.session.recv_stderr_ready():
            print self.session.recv_stderr(self.nbytes)
            return False

        readBuffer = ''
        d1 = time.time()
        while not self.session.recv_ready():
            time.sleep(1)

            d2 = time.time()
            # wait at most 20 minutes
            if (((int(d2 - d1) > self.timeout) and timeout) or int(d2 - d1) > 1200):
                break

        if self.session.recv_ready():
            if prompt_set:
                # read output untill last line is the one with the prompt
                try:
                    last_line = '\n' + self.prompt
                    while True:
                        resp = self.session.recv(self.nbytes)
                        readBuffer += resp
                        # check if it's the prompt line
                        #print('CC_LIB buffer: `{}`.'.format(readBuffer))
                        if last_line == readBuffer[-(len(self.prompt)+1):]:
                            #print('CC_LIB Found last line `{}`.'.format(last_line))
                            break;
                        time.sleep(0.5)
                except Exception as e:
                    print('CC_LIB: Read bufer timeout; prompt is set to `{}`.'.format(self.prompt))
            else:
                # No prompt is set; just try to read untill timeout;
                # repeat 5 times
                try:
                    iter = 0
                    while iter < 5:
                        resp = self.session.recv(1024)
                        readBuffer += resp
                        time.sleep(1)
                        iter += 1
                except Exception as e:
                    print('CC_LIB: Use default prompt')

            return readBuffer

        if self.session.exit_status_ready():
            return False

        return False


    def write(self, command, result=True, read_timeout=False):
        """ write command to ssh connection """

        #print('CC_LIB Got command `{}`.'.format(command))
        if not self.session or not self.session.active:
            return False

        command += '\n'
        self.session.send(command)

        if (command.find('cleartool setview') != -1):
            """ After a setview command, we need to set back the prompt """
            self.setPrompt()
            return ''

        if result:
            time.sleep(0.8)
            return self.read(read_timeout)

        return False

    def getShell(self):
        """ Get the shell for this user to know how to set the prompt """
        if not self.session or not self.session.active:
            return False

        tmp_buffer = ""
        tmp_buffer = self.write('echo $SHELL')
        """ the SHELL is displayed just before the prompt line """
        tmp_buffer = tmp_buffer.splitlines()#('\r\n')
        shell = tmp_buffer[len(tmp_buffer) - 2]

        """ shell line contains the full path; we need only the name """
        shell = shell.split('/')
        shell = shell[len(shell)-1]

        return shell

    def setPrompt(self):
        """ Set prompt to twister_prompt# """

        if not self.session or not self.session.active:
            return False

        """ we have to do a first read to get the initial prompt """
        welcome_msg = self.read(True, False)
        welcome_msg = welcome_msg.splitlines()#('\r\n')
        """ last line is the prompt """
        self.prompt = welcome_msg[len(welcome_msg)-1]

        """ get the shell to know how to set the new prompt """
        shell = self.getShell()

        """ set the new prompt, depending on shell type """
        if shell == 'tcsh' or shell == 'csh':
            self.prompt = 'twister_prompt#'
            self.write('set prompt=\"twister_prompt#\"')
        elif shell == 'bash' or shell == 'ksh':
            self.prompt = 'twister_prompt#'
            self.write('export PS1=\"twister_prompt#\"')

        self.read()

        return True

