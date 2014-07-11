
# File: ClearCasePlugin.py ; This file is part of Twister.

# version: 3.003

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
    ClearCase plugin executes the given commands using SshShell library.
"""

from __future__ import print_function

import os, sys
import re
import time
import base64

try: import simplejson as json
except: import json

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    raise Exception('TWISTER_PATH environment variable is not set! Exiting!')

from lib.TscSshLib import SshShell
from BasePlugin import BasePlugin

#

class CC(object):

    """ ClearCase helper """

    def __init__(self, user, password):

        if not user: raise Exception('CC: Username is empty! Cannot login!')
        if not password: raise Exception('CC: Password is empty! Cannot login!')

        self.cleartoolSsh = SshShell(name='cleartool', host='localhost', user=user, password=password)
        self.cleartoolSsh.set_timeout(2)
        time.sleep(1)


    def cmd(self, args):
        """
        Send ssh command command..
        """

        if not isinstance(args, dict):
            return False

        args = {k: v[0] if isinstance(v, list) else v for k, v in args.iteritems()}

        if not args.has_key('command') or not isinstance(args['command'], str):
            return False

        command = args['command']

        if command.startswith('cleartool setview'):
            print('CC: Changing view: `{}`.'.format(command))

        response = self.cleartoolSsh.write(command)

        response = self.parseSshResponse(command, response)
        response = '\n'.join(response)

        if command.startswith('cleartool setview'):
            time.sleep(2)
            response = ''

        return json.dumps(response)


    def parseSshResponse(self, cmd, response):
        """  """

        response = response.splitlines()
        try:
            response = response[response.index(cmd)+1:]
        except Exception as e:
            for line in response:
                if line.startswith(cmd[:80]):
                    response = response[response.index(line)+1:]
                    break

        try:
            if response[len(response)-1] == self.cleartoolSsh.prompt:
                response = response[:len(response)-1]
        except Exception as e:
            pass

        return response


    def getPathTree(self, path):
        """ List files and folders """

        if not path:
            return False

        treeCommand = ( 'import os\n'\
                        'rootdir = %s\n'\
                        'dir = dict()\n'\
                        'rootdir = rootdir.rstrip(os.sep)\n'\
                        'start = rootdir.rfind(os.sep) + 1\n'\
                        'for path, dirs, files in os.walk(rootdir):\n'\
                        '    folders = path[start:].split(os.sep)\n'\
                        '    subdir = {\'\': files}\n'\
                        '    parent = reduce(dict.get, folders[:-1], dir)\n'\
                        '    parent[folders[-1]] = subdir\n'\
                        'r = dict()\n'\
                        'r.update([(rootdir, dir[os.path.basename(rootdir)]), ])\n'\
                        'print(r)' % repr(path) )

        pwd = self.cleartoolSsh.write('pwd')
        self.cleartoolSsh.write('cd')
        self.cleartoolSsh.write('python -c "import base64; print(base64.b64decode(\'{}\'))"  > pathTree.py'.format(base64.b64encode(treeCommand)))
        command = 'python pathTree.py'.format(treeCommand)
        response = self.cleartoolSsh.write(command)
        self.cleartoolSsh.write('rm pathTree.py')
        self.cleartoolSsh.write('cd {}'.format(pwd))

        try:
            response = self.parseSshResponse(command, response)
            response = [r for r in response if r][0]
            response = eval(response)
        except Exception as e:
            print('CC getPathTree error: {} || response: {} '.format(e, response))
            response = ''

        return json.dumps(response)


    def getTestDescription(self, fname):
        """
        Returns the title, description and all tags from a test file.
        """

        try:
            command = 'cat {}'.format(fname)
            response = self.cleartoolSsh.write(command)

            response = self.parseSshResponse(command, response)

            # response = response.splitlines()
            # response = response[3:len(response)-1]

            response = '\n'.join(response)
        except Exception as e:
            print('CC getTestDescription error: {} || response: {} '.format(e, response))
            return ''

        li_tags = re.findall('^[ ]*?[#]*?[ ]*?<(?P<tag>\w+)>([ -~\n]+?)</(?P=tag)>', response, re.MULTILINE)
        tags = '<br>\n'.join(['<b>' + title + '</b> : ' + descr.replace('<', '&lt;') for title, descr in li_tags])
        result = tags

        command = 'cleartool ls {}'.format(fname)
        data = self.cleartoolSsh.write(command)
        data = self.parseSshResponse(command,data)
        data = ''.join(data)

        if data and (data.find('@@') != -1):
            data = data.split()[0].split('@@')[1]
            extra_info = '<b>ClearCase Version</b> : {}'.format(data)

            result += '<br>\n' + extra_info

        return result


    def getTestFile(self, fname, raw=False):
        """
        Send 1 ClearCase file.
        """

        try:
            command = 'cat {}'.format(fname)
            response = self.cleartoolSsh.write(command)
            response = self.parseSshResponse(command, response)

            # response = response.splitlines()
            # response = response[3:len(response)-1]

            response = '\n'.join(response)

            if raw:
                return response
            return response
        except Exception as e:
            print('CC getTestFile error: {} || response: {} '.format(e, response))
            return ''


    def setTestFile(self, fname, content):
        """
        Send 1 ClearCase file.
        """

        try:
            command = 'python -c "import base64; print(base64.b64decode(\'{c}\'))"  > {f}'.format(c=base64.b64encode(content), f=fname)
            response = self.cleartoolSsh.write(command)

            if len(response) >= 2:
                print('CC setTestFile error: {}'.format(response))

            return True
        except Exception as e:
            return ''


    def mkview(self, args):
        """
        Send mkview command.
        """

        try:
            command = 'cleartool mkview'
            for key in args:
                if not key == 'command':
                    command += ' ' + key + ' ' + args[key]

            response = self.cleartoolSsh.write(command)

            if len(response) >= 2:
                print('CC mkview error: {}'.format(response))

            return True
        except Exception as e:
            return ''


    def lsview(self, args):
        """
        Send lsview command.
        """

        try:
            command = 'cleartool lsview'
            for key in args:
                if not key == 'command':
                    command += ' ' + key + ' ' + args[key]

            response = self.cleartoolSsh.write(command)

            if len(response) >= 2:
                print('CC lsview error: {}'.format(response))

            return True
        except Exception as e:
            return ''


    def mkelem(self, args):
        """
        Send mkelem command.
        """

        try:
            command = 'cleartool mkelem'
            for key in args:
                if not key == 'command':
                    command += ' ' + key + ' ' + args[key]

            response = self.cleartoolSsh.write(command)

            if len(response) >= 2:
                print('CC mkelem error: {}'.format(response))

            return True
        except Exception as e:
            return ''


    def rmelem(self, args):
        """
        Send rmelem command.
        """

        try:
            command = 'cleartool rmelem'
            for key in args:
                if not key == 'command':
                    command += ' ' + key + ' ' + args[key]

            response = self.cleartoolSsh.write(command)

            if len(response) >= 2:
                print('CC rmelem error: {}'.format(response))

            return True
        except Exception as e:
            return ''


    def mklabel(self, args):
        """
        Send mklabel command.
        """

        try:
            command = 'cleartool mklabel'
            for key in args:
                if not key == 'command':
                    command += ' ' + key + ' ' + args[key]

            response = self.cleartoolSsh.write(command)

            if len(response) >= 2:
                print('CC mklabel error: {}'.format(response))

            return True
        except Exception as e:
            return ''


    def mkattr(self, args):
        """
        Send mkattr command.
        """

        try:
            command = 'cleartool mkattr'
            for key in args:
                if not key == 'command':
                    command += ' ' + key + ' ' + args[key]

            response = self.cleartoolSsh.write(command)

            if len(response) >= 2:
                print('CC mkattr error: {}'.format(response))

            return True
        except Exception as e:
            return ''


    def describe(self, args):
        """
        Send describe command.
        """

        try:
            command = 'cleartool describe'
            for key in args:
                if not key == 'command':
                    command += ' ' + key + ' ' + args[key]

            response = self.cleartoolSsh.write(command)

            if len(response) >= 2:
                print('CC describe error: {}'.format(response))

            return True
        except Exception as e:
            return ''

    def lsactivity(self, args):
        """
        Send lsactivity command.
        """

        try:
            # we have to extract the view name from sent command
            command = 'cleartool lsview'
            viewname = ''
            for key in args:
                if key == 'view':
                    viewname = args[key]
                    command += ' ' + viewname

            # check if the view exists using lsview
            response = self.cleartoolSsh.write(command)
            response = self.parseSshResponse(command, response)
            response = '\n'.join(response)
            if 'cleartool: Error:' in response:
                return '*ERROR* View `{}` doesn\'t exist !'.format(viewname)

            # set the view
            command = 'cleartool setview ' + viewname
            response = self.cleartoolSsh.write(command)
            response = self.parseSshResponse(command, response)
            response = '\n'.join(response)
            if 'cleartool: Error:' in response:
                return '*ERROR* View `{}` cannot be set !'.format(viewname)

            # list the activities
            command = 'cleartool lsactivity -cview -short'
            response = self.cleartoolSsh.write(command)
            response = self.parseSshResponse(command, response)
            response = '\n'.join(response)

            # exit from view
            response1 = self.cleartoolSsh.write('exit')
            response1 = self.parseSshResponse(command, response1)

            return response
        except Exception as e:
            return ''


# # #


class Plugin(BasePlugin):

    """
    ClearCase plugin
    """

    def __init__(self, user, data):

        if not data: return False
        BasePlugin.__init__(self, user, data)
        self.user = user
        self.data = data
        passwd = self.data['ce'].get_user_info(self.user, 'user_passwd')
        self.conn = CC(self.user, passwd)


    def __del__(self):
        """ On plugin exit """

        print('EXIT PLUGIN')
        del self.user
        del self.data
        del self.conn


    def run(self, args):
        """
        Called for every command
        """

        if args['command'] == 'get_path_tree':
            if not args.has_key('path'):
                return False
            return self.getPathTree(args['path'])

        elif args['command'] == 'get_test_file':
            if not args.has_key('file_name'):
                return False
            return self.getTestFile(args['file_name'], True)

        elif args['command'] == 'get_test_description':
            if not args.has_key('file_name'):
                return False
            return self.getTestDescription('user', args['file_name'])

        elif args['command'] == 'set_test_file':
            if not args.has_key('file_name') or not args.has_key('content'):
                return False
            return self.setTestFile(args['file_name'], args['content'])

        elif args['command'] == 'mkview':
            return self.conn.mkview(args)

        elif args['command'] == 'lsview':
            return self.conn.lsview(args)

        elif args['command'] == 'mkelem':
            return self.conn.mkelem(args)

        elif args['command'] == 'rmelem':
            return self.conn.rmelem(args)

        elif args['command'] == 'mklabel':
            return self.conn.mklabel(args)

        elif args['command'] == 'mkattr':
            return self.conn.mkattr(args)

        elif args['command'] == 'describe':
            return self.conn.describe(args)

        elif args['command'] == 'lsactivity':
            return self.conn.lsactivity(args)

        try:
            resp = self.conn.cmd(args)
        except Exception as e:
            print('CC Plug-in: Exception on args `{}` - `{}` !'.format(args, e))
            return False

        return resp


    def onStart(self, clear_case_view=None):
        """
        Called on project start.
        """

        # No data provided ?
        if not clear_case_view:
            print('CC Plug-in onStart: ClearCase View empty `{}`! Your tests will NOT run!'.format(clear_case_view))
            return False

        print('CC Plug-in: Changing ClearCase View to `{}`.'.format(clear_case_view))

        self.data['clear_case_view'] = clear_case_view
        self.run( {'command': 'cleartool setview {}'.format(clear_case_view)} )


    def getPathTree(self, path):
        """  """
        try:
            return self.conn.getPathTree(path)
        except Exception as e:
            print('CC Plug-in: getPathTree error {}'.format(e))
            return ''


    def getTestFile(self, fname, raw=False):
        """
        Send 1 ClearCase file.
        """

        try:
            return self.conn.getTestFile(fname, raw)
        except Exception as e:
            print('CC Plug-in: getTestFile error {}'.format(e))
            return ''


    def getTestDescription(self, user, fname):
        """
        Returns the title, description and all tags from a test file.
        """

        try:
            return self.conn.getTestDescription(fname)
        except Exception as e:
            print('CC Plug-in: getTestDescription error {}'.format(e))
            return ''


    def setTestFile(self, fname, content):
        """
        Save 1 ClearCase file.
        """

        try:
            return self.conn.setTestFile(fname, content)
        except Exception as e:
            print('CC Plug-in: getTestFile error {}'.format(e))
            return ''

#

"""

#### plugins.xml config ####

<Plugin>
    <name>ClearCase</name>
    <jarfile>ClearCasePlugin.jar</jarfile>
    <pyfile>ClearCasePlugin.py</pyfile>
    <status>disabled</status>
</Plugin>

"""

