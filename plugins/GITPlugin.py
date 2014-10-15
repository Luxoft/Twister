
# version: 2.005

import os, sys
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
    If command is Update and Overwrite is false, execute a GIT checkout and GIT pull on the specified branch;
      if Overwrite is true, delete the folder, then GIT clone for the specified branch.
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
        
        child = pexpect.spawn(['bash'])
        child.logfile = sys.stdout
        
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
        if not branch: 
            return 'You must specify a branch for snapshot/update!'
        
        # Normal Git clone operation
        if command == 'clone' or (command == 'pull' and overwrite):

            if overwrite and os.path.exists(dst):
                print 'GIT Plugin: Deleting folder `{}` ...'.format(dst)
                shutil.rmtree(dst, ignore_errors=True)

            to_exec = 'git clone -b {branch} {src} {dst}'.format(branch=branch, src=src, dst=dst)
            print('GIT Plugin: Exec `{}` .'.format(to_exec.strip()))

            try:
                child.sendline(to_exec.strip())
                
                try:
                    i = child.expect(['.*password:','Are you sure.*'], 10)
                    if i == 0 and pwd:
                        child.sendline(pwd)
                    elif i == 1 and pwd:
                        child.sendline('yes')

                        time.sleep(1)

                        try:
                            child.expect('.*password:')
                            child.sendline(pwd)
                        except Exception as e:
                            return 'Error on calling GIT {cmd} (from `{src}` to `{dst}`): `{e}`!'.format(
                                cmd=command, src=src, dst=dst, e=e)
                except Exception as e:
                    return 'Error on calling GIT {cmd} (from `{src}` to `{dst}`): `{e}`!'.format(
                        cmd=command, src=src, dst=dst, e=e)
            except Exception as e:
                return 'Error on calling GIT {cmd} (from `{src}` to `{dst}`): `{e}`!'.format(
                    cmd=command, src=src, dst=dst, e=e)

            time.sleep(1)

            try:
                i = child.expect(['Resolving deltas.*done\.',
                                  'fatal: The remote end hung up unexpectedly'], None)
                if i == 1:
                    # fatal: Remote branch branch_name not found in upstream origin
                    print 'Error on calling GIT clone: {} do not exist.'.format(branch)
                    return 'Error on calling GIT {cmd} (from `{src}` to `{dst}`)! Branch {br} do not exist!'.format(
                                cmd=command, src=src, dst=dst,br=branch)
            except Exception as e:
                return 'Error after calling GIT {cmd}: `{e}`!'.format(cmd=command, e=e)
            
            child.sendline('\n\n')

            time.sleep(1)

            print('-'*40)

        # Git pull operation
        elif command == 'pull':
            
            child.sendline('cd {}'.format(dst))

            time.sleep(1)

            child.expect('.*')
            to_exec = 'git checkout {}'.format(branch)
            print('GIT Plugin: Exec `{}` .'.format(to_exec.strip()))

            child.sendline(to_exec.strip())
            time.sleep(1)

            try:
                i = child.expect(['Switched to.*',
                                  'Your branch is up-to-date with',
                                  'error',
                                  'Not a git repository',
                                  'Already on.*'], 30)
                if i == 2:
                    # error: pathspec branch_name did not match any file(s) known to git.
                    # the specified branch does not exist on the repository
                    print 'Error on calling GIT checkout: branch {} do not exist.'.format(branch)
                    return 'Error on calling GIT {cmd} (from `{src}` to `{dst}`)!\n\
 Branch `{br}` does not exist!'.format(cmd=command, src=src, dst=dst, br=branch)
                elif i == 3:
                    # fatal: Not a git repository (or any of the parent directories): .git
                    # Trying to make a checkout without making a clone first
                    print 'Error on calling GIT checkout: repository {} does not exist.'.format(branch)
                    return 'Error on calling GIT {cmd} (from `{src}` to `{dst}`)!\n\
 Make a snapshot before doing an update!'.format(cmd=command, src=src, dst=dst, br=branch)
            except Exception as e:
                print 'Error on calling {}. Got unexpected response from GIT.'.format(to_exec)
                return 'Error on calling GIT {cmd} (from `{src}` to `{dst}`): `{e}`!'.format(
                    cmd=command, src=src, dst=dst, e=e)
            time.sleep(1)

            child.sendline('git pull -f')
            try:
                child.expect('.*password:')
                time.sleep(1)

                child.sendline(pwd)
            except Exception as e:
                print 'Error after calling GIT pull -f'
                return 'Error after calling GIT {cmd}: `{e}`!'.format(cmd=command, e=e)
            
            time.sleep(1)

            try:
                child.expect(['up-to-date', 'files changed'], 120)
                child.sendline('\n\n')
            except Exception as e:
                return 'Error after calling GIT {cmd}: `{e}`!'.format(cmd=command, e=e)

            time.sleep(1)
            print('-'*40)

        else:
            return '*ERROR* Unknown plugin command `{}`!'.format(command)

        return 'true'

#