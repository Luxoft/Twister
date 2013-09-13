
# version: 2.002

import os
import shutil
import subprocess
from BasePlugin import BasePlugin

#

class Plugin(BasePlugin):

    """
    SVN Plugin has a few parameters:
    - server complete path
    - user and password to connect to server
    - snapshot folder, where all data is cloned

    If command is Snapshot, execute a SVN checkout;
      if the Snapshot folder is already present, delete it, then SVN checkout.
    If command is Update and Overwrite is false, execute a SVN update;
      if Overwrite is false, delete the folder, then SVN checkout.
    """

    def run(self, args):

        src = self.data.get('server')
        dst = self.data.get('snapshot')

        if not args.get('command'):
            return '*ERROR* Must specify a command like `snapshot` or `update` !'

        if args['command'] == ['snapshot']:
            return self.execCheckout(src, dst, 'checkout', overwrite=True)

        elif args['command'] == ['update'] and args['overwrite'] == ['false']:
            return self.execCheckout(src, dst, 'update', overwrite=False)

        elif args['command'] == ['update'] and args['overwrite'] == ['true']:
            return self.execCheckout(src, dst, 'checkout', overwrite=True)

        else:
            return 'Invalid command: `{} & {}`!'.format(args['command'], args['overwrite'])


    def execCheckout(self, src, dst, command, overwrite=False):

        if overwrite and os.path.exists(dst):
            print 'SVN Plugin: Deleting folder `{}` ...'.format(dst)
            shutil.rmtree(dst, ignore_errors=True)

        usr = self.data['username']
        pwd = self.data['password']

        if usr:
            try:
                p = subprocess.Popen(['svn', command, src, dst, '--username', usr], shell=False)
                p.wait()
            except Exception as e:
                return 'Error on calling SVN {cmd} (from `{src}` to `{dst}`): `{e}`!'.format(
                    cmd=command, src=src, dst=dst, e=e)
        elif usr and pwd:
            try:
                p = subprocess.Popen(['svn', command, src, dst, '--username', usr, '--password', pwd], shell=False)
                p.wait()
            except Exception as e:
                return 'Error on calling SVN {cmd} (from `{src}` to `{dst}`): `{e}`!'.format(
                    cmd=command, src=src, dst=dst, e=e)
        else:
            try:
                p = subprocess.Popen(['svn', command, src, dst], shell=False)
                p.wait()
            except Exception as e:
                return 'Error on calling SVN {cmd} (from `{src}` to `{dst}`): `{e}`!'.format(
                    cmd=command, src=src, dst=dst, e=e)

        return 'true'

#
