
# version: 2.002

import os
import shutil
import time
import pexpect
from BasePlugin import BasePlugin

#

class Plugin(BasePlugin):

    """
    GIT Plugin has a few parameters:
    - server complete path
    - branch used for clone
    - user and password to connect to server
    - snapshot folder, where all data is cloned

    If command is Snapshot, execute a GIT clone;
      if the Snapshot folder is already present, delete it, then GIT clone.
    If command is Update and Overwrite is false, execute a GIT pull;
      if Overwrite is false, delete the folder, then GIT clone.
    """

    def run(self, args):

        src = self.data.get('server')
        dst = self.data.get('snapshot')

        if not args.get('command'):
            return '*ERROR* Must specify a command like `snapshot` or `update` !'

        if args['command'] == ['snapshot']:
            return self.execCheckout(src, dst, 'clone', overwrite=True)

        elif args['command'] == ['update'] and args['overwrite'] == ['false']:
            return self.execCheckout(src, dst, 'pull', overwrite=False)

        elif args['command'] == ['update'] and args['overwrite'] == ['true']:
            return self.execCheckout(src, dst, 'pull', overwrite=True)

        elif args['command'] == ['delete']:
            return self.execCheckout('', '', '', overwrite=True)

        else:
            return 'Invalid command: `{} & {}`!'.format(args['command'], args['overwrite'])


    def execCheckout(self, src, dst, command, overwrite=False):

        if overwrite and os.path.exists(dst):
            print 'GIT Plugin: Deleting folder `{}` ...'.format(dst)
            shutil.rmtree(dst, ignore_errors=True)

        if not src:
            return '*ERROR* Git source folder is NULL !'
        if '//' not in src:
            return '*ERROR* Git source folder `{}` is invalid !'.format(src)
        if not dst:
            return '*ERROR* Git destination folder is NULL !'

        usr = self.data['username']
        pwd = self.data['password']

        src = src.replace('//', '//{}@'.format(usr))

        branch = self.data['branch']
        if branch: branch = '-b ' + branch
        else: branch = ''

        # Normal Git clone operation
        if command == 'clone':

            to_exec = 'git clone {branch} {src} {dst}'.format(branch=branch, src=src, dst=dst)
            print('GIT Plugin: Exec `{}` .'.format(to_exec.strip()))

            try:
                child = pexpect.spawn(to_exec.strip())
                if pwd:
                    child.expect('.*password:')
                    child.sendline(pwd)
            except Exception as e:
                return 'Error on calling GIT {cmd} (from `{src}` to `{dst}`): `{e}`!'.format(
                    cmd=command, src=src, dst=dst, e=e)

            time.sleep(1)
            print(child.before)
            print(child.after)
            print('-'*40)

        # Git pull operation
        elif command == 'pull':

            try:
                os.chdir(dst)
                print('GIT Plugin: CHDIR into `{}`.'.format(dst))
            except:
                return '*ERROR* Cannot chdir into `{}`! Cannot pull!'.format(dst)

            to_exec = 'git pull -f {branch}'.format(branch=branch)
            print('GIT Plugin: Exec `{}` .'.format(to_exec.strip()))

            try:
                child = pexpect.spawn(to_exec.strip())
                if pwd:
                    child.expect('.*password:')
                    child.sendline(pwd)
            except Exception as e:
                return 'Error on calling GIT {cmd} (from `{src}` to `{dst}`): `{e}`!'.format(
                    cmd=command, src=src, dst=dst, e=e)

            time.sleep(1)
            print(child.before)
            print(child.after)
            print('-'*40)

        else:
            return '*ERROR* Unknown plugin command `{}`!'.format(command)

        return 'true'

#
