
import os
import pexpect
from BasePlugin import BasePlugin

#

class Plugin(BasePlugin):

    """
    Git Plugin has a few parameters:
    - server complete path
    - branch used for clone
    - user and password to connect to server
    - snapshot folder, where all data is cloned

    If command is Snapshot, execute a Git clone;
      if the Snapshot folder is already present, delete it, then Git clone.
    If command is Update and Overwrite is false, execute a Git pull;
      if Overwrite is false, delete the folder, then Git clone.
    """

    def run(self, args):

        src = self.data['server']
        dst = self.data['snapshot']

        if args['command'] == ['snapshot']:
            return self.execCheckout(src, dst, 'clone', overwrite=True)

        elif args['command'] == ['update'] and args['overwrite'] == ['false']:
            return self.execCheckout(src, dst, 'pull', overwrite=False)

        elif args['command'] == ['update'] and args['overwrite'] == ['true']:
            return self.execCheckout(src, dst, 'pull', overwrite=True)

        elif args['command'] == ['delete']:
            return self.execCheckout('', '', '', overwrite=True)

        else:
            return 'Invalid command: `%s & %s`!' % (args['command'], args['overwrite'])


    def execCheckout(self, src, dst, command, overwrite=False):

        if overwrite and os.path.exists(dst):
            print 'Git plugin: Deleting folder `%s` !' % dst
            os.rmdir(dst)
        if not src:
            return 'Git source folder is NULL !'
        if not dst:
            return 'Git destination folder is NULL !'

        usr = self.data['username']
        pwd = self.data['password']

        # Normal Git clone operation
        if command == 'clone':

            branch = self.data['branch']
            if branch: branch = '-b ' + branch
            else: branch = ''

            try:
                child = pexpect.spawn('git clone {branch} {src} {dst}'.format(branch=branch, src=src, dst=dst))
                if pwd:
                    child.expect('.*password:')
                    child.sendline(pwd)
                print 'Running Git plugin::', child.read()
            except:
                return 'Error on calling Git {cmd} (from `{src}` to `{dst}`): `{e}`!'.format(
                    cmd=command, src=src, dst=dst, e=e)

        # Git pull operation
        elif command == 'pull':

            branch = self.data['branch']
            if branch: branch = 'origin ' + branch
            else: branch = ''

            try:
                child = pexpect.spawn('git pull -f {branch}'.format(branch=branch, src=src, dst=dst))
                if pwd:
                    child.expect('.*password:')
                    child.sendline(pwd)
                print 'Running Git plugin::', child.read()

                if 'automatic merge failed' in child.before.lower():
                    if not overwrite:
                        return 'Git pull conflict! Please fix the issues, then update again!\n{0}'.format(child.before)
                    else:
                        # If pull conflict AND should overwrite
                        return self.execCheckout(src, dst, 'clone', overwrite=True)
            except:
                return 'Error on calling Git {cmd} (from `{src}` to `{dst}`): `{e}`!'.format(
                    cmd=command, src=src, dst=dst, e=e)

        else:
            return 'Error on calling Git command `%s`!' % command

        return 'true'

#
