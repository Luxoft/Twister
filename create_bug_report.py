#!/usr/bin/env python
'''
This script collects all twister file versions, the Central Engine log and the EP logs.
It also collects fwmconfig.xml and testsuites.xml settings.
If the script fails to collect the logs, you must edit the SERVER PATH and CLIENT PATH manually.
'''
import os, sys
import glob
import platform
import subprocess
import zipfile

# Default paths
SERVER_PATH = '/opt/twister'
CLIENT_PATH = '~/twister'

print('Starting...')

system = platform.machine() +' '+ platform.system() +', '+ ' '.join(platform.linux_distribution())
py_version = '.'.join([str(v) for v in sys.version_info])

s_versions = subprocess.check_output('find -L %s -name \*.py -exec grep "# version:" /dev/null {} \;'\
        % (SERVER_PATH), shell=True)
c_versions = subprocess.check_output('find -L %(path)s -type d \( -path %(path)s/.twister_cache -o -path %(path)s/demo \) -prune -o -exec grep "# version:" /dev/null {} \;'\
        % {'path':CLIENT_PATH}, shell=True)

f = open('bug_report.txt', 'wb')
f.write('~Starting report~\n\n')
f.write('Machine OS: {}\n'.format(system))
f.write('Python version: {}\n'.format(py_version))
f.write('\nServer versions:\n{}\n'.format(s_versions.strip()))
f.write('\nClient versions:\n{}\n'.format(c_versions.strip()))
f.write('\n~Finished report~\n')
f.close()

z = zipfile.ZipFile('bug_report.zip', 'w')
z.write('bug_report.txt', 'bug_report.txt')
z.write(SERVER_PATH + '/ce_log.log', 'ce_log.log')

logs_path = os.path.expanduser(CLIENT_PATH) + '/.twister_cache'
for log in glob.glob(logs_path + '/*_LIVE.log'):
    z.write(log, os.path.split(log)[1])

z.write( os.path.expanduser(CLIENT_PATH) + '/config/fwmconfig.xml', 'fwmconfig.xml' )
z.write( os.path.expanduser(CLIENT_PATH) + '/config/testsuites.xml', 'testsuites.xml' )
z.close()

os.remove('bug_report.txt')

print('Done!')
