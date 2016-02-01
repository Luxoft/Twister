
# version: 2.003

import os
import subprocess
from BasePlugin import BasePlugin

TWISTER_PATH = os.getenv('TWISTER_PATH')

#
# The Jenkins Post-Script file will call this plugin, to execute
# the script what will send the build to the DUT (Device under test).
# Then, the plugin will execute a test suite, from an XML file.
#
# If you need a method to use the last build number in your reports,
# you must create a field Type="UserScript" in field_section from DB.xml
# and in the applet, you must choose the path to a script that will get
# the last build nr from Jenkins and print it on the screen.
#
# When all the tests are completed, this User Script will be executed
# and the build number will be saved in the database.
#
# How to execute the plugin from a script:
# ce.run_plugin('user', 'Jenkins', {"command":True, "build":"B019"})
#

class Plugin(BasePlugin):

    """
    Jenkins Plugin.
    """
    def run(self, args):
        # This script will load the build on the DUT
        script = self.data['script']
        # This project will run after the above script finishes
        project = self.data['project']

        # This is the build number from Jenkins
        if isinstance(args['build'], str) or isinstance(args['build'], int):
            build = str(args['build'])
        elif isinstance(args['build'], list):
            [build] = args['build']
        else:
            return 'Jenkins Plugin: Invalid build number `{}` !'.format(args['build'])


        with open('{}/plugins/build_number.tmp~'.format(TWISTER_PATH), 'w') as build_file:
            build_file.write(str(build))

        subprocess.Popen([ 'chmod', '644', ('{}/plugins/build_number.tmp~'.format(TWISTER_PATH)) ])

        status = self.data['ce'].get_user_info(self.user, 'status')
        # If the status for this user is 'Running' or 'Paused', don't do anything
        if status in [1, 2]:
            return 'Jenkins Plugin: The Central Engine is already running! Cannot start suite!'

        try:
            txt = subprocess.check_output(script, shell=True)
            print txt.strip()
        except Exception as err:
            #return 'Jenkins Plugin: Execute `{}` returned exception - {}'.format(script, str(err))
            print 'Jenkins Plugin: Execute `{}` returned exception - {}'.format(script, str(err))

        # Start Central Engine !
        self.data['ce'].set_exec_status_all(self.user, 2, project)

        return True

#
