#!/usr/bin/env python

# version: 2.002

# File: cli.py ; This file is part of Twister.

# Copyright (C) 2012 , Luxoft

# Authors:
#  Andrei Costachi <acostachi@luxoft.com>
#  Andrei Toma <atoma@luxoft.com>
#  Cristian Constantin <crconstantin@luxoft.com>
#  Daniel Cioata <dcioata@luxoft.com>

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''
Commands :
- Start, stop, pause the execution.
- (users) All users that are running tests.
- (eps) Display what EPs are enabled for your user.
- (stats) What is the start time for this run, suites list and tests list.
- (status) Execution summary status: how many test cases are planned for execution,
  how many were executed, how may passed, how many failed.
- (status-details) Execution details status: the same, plus status per test case.
- Queue tests during run time.
'''

import os
import datetime
import xmlrpclib
import subprocess
from optparse import OptionParser

# --------------------------------------------------------------------------------------------------
#   Functions
# --------------------------------------------------------------------------------------------------

STATUS_PENDING  = 10 # Not yet run, waiting to start
STATUS_WORKING  = 1  # Is running now
STATUS_PASS     = 2  # Test is finished successful
STATUS_FAIL     = 3  # Test failed
STATUS_SKIPPED  = 4  # When file doesn't exist, or test has flag `runnable = False`
STATUS_ABORTED  = 5  # When test is stopped while running
STATUS_NOT_EXEC = 6  # Not executed, is sent from TC when tests are paused, and then stopped instead of being resumed
STATUS_TIMEOUT  = 7  # When timer expired
STATUS_INVALID  = 8  # When timer expired, the next run
STATUS_WAITING  = 9  # Is waiting for another test
testStatus = {STATUS_PENDING:'pending', STATUS_WORKING:'working', STATUS_PASS:'pass', STATUS_FAIL:'fail',
STATUS_SKIPPED:'skip', STATUS_ABORTED:'aborted', STATUS_NOT_EXEC:'notexec', STATUS_TIMEOUT:'timeout',
STATUS_INVALID:'null', STATUS_WAITING:'waiting'}


def userHome(user):
	"""
	Find the home folder for the given user.
	"""
	return subprocess.check_output('echo ~' + user, shell=True).strip()


def checkUsers(proxy):
	"""
	Check all users from etc/passwd, that have Twister in their home folder.
	"""
	users = proxy.listUsers(False)
	print('All users that have installed Twister: `{}`.'.format(', '.join(users)))
	users = proxy.listUsers(True)
	if users:
		print('All active users: `{}`.\n'.format(', '.join(users)))
	else:
		print('Active users: None.\n')


def checkEps(proxy, user):
	"""
	Get the list of EPs for this user, then get the status for each EP.
	"""
	eps = proxy.listEPs(user).split(',')
	now = datetime.datetime.today()
	print('Your Execution-Processes are:')

	for ep in eps:
		alive = proxy.getEpVariable(user, ep, 'last_seen_alive')
		if alive:
			d = now - datetime.datetime.strptime(alive, '%Y-%m-%d %H:%M:%S')
			if d.seconds > 10:
				print('{} : idle! (last active {} sec)'.format(ep, d.seconds))
			else:
				print('{} : running (last active {} sec)'.format(ep, d.seconds))
		else:
			print('{} : service not running'.format(ep))
	print


def checkStatus(proxy, user, extra=True):
	stats = proxy.getFileStatusAll(user).split(',')
        if stats == ['']:
            return False
	all_stat = proxy.getExecStatusAll(user).split('; ')
	stats = [int(i) for i in stats]

	s_dict = {
		'status': all_stat[0],
		'date': all_stat[1],
		'time': all_stat[2],
		'texec':  len(stats),
		'tpend':  stats.count(STATUS_PENDING) + stats.count(-1),
		'twork':  stats.count(STATUS_WORKING),
		'tpass':  stats.count(STATUS_PASS),
		'tfail':  stats.count(STATUS_FAIL),
		'tabort': stats.count(STATUS_ABORTED),
		'tnexec': stats.count(STATUS_NOT_EXEC),
		'rate'  : round( (float(stats.count(STATUS_PASS)) / len(stats)* 100), 2),
	}
	s_dict['tother'] = len(stats) -s_dict['tpend'] -s_dict['twork'] -s_dict['tpass'] -s_dict['tfail'] -s_dict['tabort'] -s_dict['tnexec']

	print """User status : {status}
Last started: {date}
Time elapsed: {time}
""".format(**s_dict)

	if extra:
		print """Passed  : {tpass}
Failed  : {tfail}
Pending : {tpend}
Working : {twork}
Aborted : {tabort}
No Exec : {tnexec}
Other   : {tother}
> Total : {texec}
Pass rate: {rate}%
""".format(**s_dict)


def checkDetails(proxy, user, option=None):
	eps = proxy.listEPs(user).split(',')
	now = datetime.datetime.today()
	options = ['running', 'done', 'finished', 'pending', 'all', True]
	if option not in options:
		print('Invalid option for stats `{}`. Valid options are: {}.\n'.format(option, options))
		option = 'all'

	# Data started and Time elapsed
        if checkStatus(proxy, user, False) == False:
                print "No statistics available"
                return

	print('Your Suites are:')

	for ep in eps:
		print('  - on {} :'.format(ep))
		suites = proxy.listSuites(user, ep).split(',')
		for suite in suites:
			if suite:
				s_id  = suite.split(':')[0]
				suite = suite.split(':')[1]
				print('    - {}'.format(suite))
				files = proxy.getSuiteFiles(user, ep, s_id)
				if not files:
					print('      - empty')
				else:
					for f_id in files:
						fname = proxy.getFileVariable(user, ep, f_id, 'file')
						fstat = proxy.getFileVariable(user, ep, f_id, 'status') or STATUS_PENDING
						if option == 'running' and fstat != STATUS_WORKING:
							continue
						elif (option=='done' or option=='finished') and \
							fstat in [STATUS_PENDING, STATUS_WORKING, STATUS_INVALID]:
							continue
						elif option == 'pending' and fstat != STATUS_PENDING:
							continue
						print('      - [{}] {}'.format(testStatus[fstat], fname))
			else:
				print('    - nothing here')
		print


def queueTest(proxy, user, suite, fname):
	"""
	Queue a file, at the end of a suite.
	"""
	r = proxy.queueFile(user, suite, fname)
	if r:
		print('Test `{}` was queued in suite `{}`.'.format(fname, suite))
	else:
		print('Failed to queue test `{}` was queued in suite `{}`!'.format(fname, suite))

	print


# --------------------------------------------------------------------------------------------------
#   M a i n
# --------------------------------------------------------------------------------------------------

if __name__ == '__main__':

	usage = "Usage: %prog --server <ip:port> --command [...parameters]"
	version = "%prog v2.0"
	parser = OptionParser(usage=usage, version=version)
	user = os.getenv('USER')

	# The most important option is the server. By default, it's localhost:8000.
	parser.add_option("--server",      action="store", default="http://127.0.0.1:8000/",
		help="Central engine server IP and Port (default: http://127.0.0.1:8000/).")

	parser.add_option('-u', "--users", action="store_true", help="Show active and inactive users.")

	parser.add_option("--eps",         action="store_true", help="Show active and inactive Eps.")

	parser.add_option("--stats",       action="store_true", help="Show stats.")
	parser.add_option("--status",      action="store_true", help="Show stats.")

	parser.add_option("--details",            action="store_true", help="Show detailed status for All files.")
	parser.add_option("--status-details",     action="store", help="Show detailed status for running, finished, pending, or all files.")

	parser.add_option("-q", "--queue",   action="store", help="Queue a file at the end of a suite. Specify queue like `suite:file`.")

	parser.add_option("-s", "--set",     action="store", help="Set status: start/ stop/ pause. (Must also specify a config and a project)")
	parser.add_option("-c", "--config",  action="store", help="Path to FWMCONFIG.XML file.")
	parser.add_option("-p", "--project", action="store", help="Path to PROJECT.XML file.")

	(options, args) = parser.parse_args()


	# Test if user did install Twister
	if os.path.isdir(userHome(user) + os.sep + 'twister'):
		print('\nHello, user `{}`.\n'.format(user))
	else:
		print('Username `{}` must install Twister before using this script !\n'.format(user))

	# Test Central Engine valid IP + PORT
	try:
		proxy = xmlrpclib.ServerProxy(options.server)
		# print('Connection to Central Engine at `{}` is ok.\n'.format(options.server))
	except:
		print('The server must be a valid IP and PORT combination ! Exiting !\n')
		exit(1)

	# Test Central Engine connection
	try:
		proxy.echo('ping')
		# print('Connection to Central Engine at `{}` is ok.\n'.format(options.server))
	except:
		print('The Central Engine server is down ! Exiting !\n')
		exit(1)


	# Check active and inactive users
	if options.users:
		checkUsers(proxy)
		exit()


	# Check active and inactive EPs
	if options.eps:
		checkEps(proxy, user)
		exit()


	# Check status
	if options.stats or options.status:
                if checkStatus(proxy, user) == False:
                        print "Status not available"
		exit()


	# Check status details
	if options.details or options.status_details:
		opt = options.details or options.status_details
		checkDetails(proxy, user, opt)
		exit()


	# Queue a file at the end of a suite
	if options.queue:
		if not ':' in options.queue:
			print('Must queue `suite:file`, for example `Suite1:/home/user/some_file.py`.')
		suite, fname = options.queue.split(':')
		queueTest(proxy, user, suite, fname)
		exit()


	# If all the other options are not available, it means the command must be a status change.
	if not options.set:
		print('Must specify a status ! Exiting !')
		exit(1)
	if options.set.lower() not in ['stop', 'start', 'pause']:
		print('Must specify a valid status (stop/ start/ pause) ! Exiting !')
		exit(1)

	if not options.config: options.config = ''
	if not options.project: options.project = ''

	if (not options.config) and options.set == 'start':
		print('Must specify a config path ! Exiting !\n')
		exit(1)
	if options.config and ( not os.path.isfile(options.config) ):
		print('Must specify a valid config path, that path does not exist ! Exiting !\n')
		exit(1)
	if (not options.project) and options.set == 'start':
		print('Must specify a project path ! Exiting !\n')
		exit(1)
	if options.project and ( not os.path.isfile(options.project) ):
		print('Must specify a valid project path, that path does not exist ! Exiting !\n')
		exit(1)

	if options.set == 'start':
		print 'Starting...'
		print proxy.setExecStatusAll(user, 2, options.config + ',' + options.project)

	elif options.set == 'stop':
		print 'Stopping...'
		print proxy.setExecStatusAll(user, 0, options.config + ',' + options.project)

	elif options.set == 'pause':
		print 'Paused...'
		print proxy.setExecStatusAll(user, 1, options.config + ',' + options.project)

	print

# Eof()
