
# version: 2.003

import sys
import xmlrpclib
from jenkinsapi import api

username = sys.argv[1]
password = sys.argv[2]

jenkins = api.Jenkins('http://localhost:8080')
twister_job = jenkins.get_job('twister') # The Jenkins job is called `twister` !
twister_build = twister_job.get_last_build()
twister_status = twister_build.get_status()

print 'Status:', twister_status

if twister_build.is_good():
    print 'The build passed successfully'
else:
    print 'The build is not successful!'
    exit(1)

# Central Engine is considered to run on localhost:8000
server = xmlrpclib.ServerProxy('http://{}:{}@127.0.0.1:8000/'.format(username, password))

to_send = 'Jenkins: Job `{0}`, Build `{1}`, Status `{2}`!'.format(twister_job, twister_build, twister_status)
try:
    server.echo(to_send)
except Exception as err:
    print err
    print 'Usage: python {} twister_username twister_password'.format(sys.argv[0])
    sys.exit(1)
# The Twister user is called `jenkins`
server.run_plugin(username, 'Jenkins', {"command":True, "build":twister_build})
