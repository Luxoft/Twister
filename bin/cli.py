#!/usr/bin/env python2.7

# version: 3.002

# File: cli.py ; This file is part of Twister.

# Copyright (C) 2012-2014, Luxoft

# Authors:
#    Andreea Proca <aproca@luxoft.com>
#    Andrei Costachi <acostachi@luxoft.com>
#    Cristi Constantin <crconstantin@luxoft.com>

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
- (status) Execution summary status: What is the start time for this run, suites list and tests list,
  how many test cases are planned for execution, how many were executed, how may passed, how many failed.
- (status-details) Execution details status: the same, plus status per test case.
- Queue or Dequeue tests during run time.
'''

import os
import time
import datetime
import binascii
import subprocess
import signal
from optparse import OptionParser
import rpyc

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

TEST_STATUS = {STATUS_PENDING:'pending', STATUS_WORKING:'working', STATUS_PASS:'pass', STATUS_FAIL:'fail',
STATUS_SKIPPED:'skip', STATUS_ABORTED:'aborted', STATUS_NOT_EXEC:'notexec', STATUS_TIMEOUT:'timeout',
STATUS_INVALID:'null', STATUS_WAITING:'waiting'}


def user_home():
    """
    Find the home folder for the given user.
    """
    return subprocess.check_output('echo ~' + USER, shell=True).strip()


def check_users(proxy):
    """
    Check all users from etc/passwd, that have Twister in their home folder.
    """
    users = proxy.list_users(False)
    print('All users that have installed Twister: `{}`.'.format(', '.join(users)))
    users = proxy.list_users(True)
    if users:
        print('All active users: `{}`.\n'.format(', '.join(users)))
    else:
        print('Active users: None.\n')


def check_eps(proxy):
    """
    Get the list of EPs for this user, then get the status for each EP.
    """
    eps = proxy.list_eps()
    now = datetime.datetime.today()
    print('Your Execution-Processes are:')

    for ep in eps:
        alive = proxy.get_ep_variable(ep, 'last_seen_alive')
        if alive:
            d = now - datetime.datetime.strptime(alive, '%Y-%m-%d %H:%M:%S')
            if d.seconds > 10:
                print('{} : idle! (last active {} sec)'.format(ep, d.seconds))
            else:
                print('{} : running (last active {} sec)'.format(ep, d.seconds))
        else:
            print('{} : service not running'.format(ep))
    print


def check_status(proxy, extra=True):
    """ check execution status """
    stats = proxy.get_file_status_all()
    if stats == ['']:
        return False

    all_stat = proxy.get_ep_status_all()
    stats = [int(i) for i in stats]

    if len(stats) > 0:
        round_rate = round( (float(stats.count(STATUS_PASS)) / len(stats)* 100), 2)
    else:
        round_rate = 0

    s_dict = {
        'status': all_stat,
        'date': proxy.get_user_variable('start_time'),
        'time': proxy.get_user_variable('elapsed_time'),
        'texec':  len(stats),
        'tpend':  stats.count(STATUS_PENDING) + stats.count(-1),
        'twork':  stats.count(STATUS_WORKING),
        'tpass':  stats.count(STATUS_PASS),
        'tfail':  stats.count(STATUS_FAIL),
        'tabort': stats.count(STATUS_ABORTED),
        'tnexec': stats.count(STATUS_NOT_EXEC),
        'rate'  : round_rate,
    }
    s_dict['tother'] = len(stats) -s_dict['tpend'] -s_dict['twork'] \
        -s_dict['tpass'] -s_dict['tfail'] -s_dict['tabort'] -s_dict['tnexec']

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

    return True


def check_details(proxy, user, option=None):
    """ get run details """
    eps = proxy.list_eps()
    options = ['running', 'done', 'finished', 'pending', 'all', True]
    if option not in options:
        print('Invalid option for stats `{}`. Valid options are: {}.\n'.format(option, options))
        option = 'all'

    # Data started and Time elapsed
    if not check_status(proxy, False):
        print 'No statistics available.\n'
        return False

    print('Your Suites are:')

    for ep in eps:
        print('  - on {} :'.format(ep))
        suites = proxy.list_suites(ep).split(',')
        for suite in suites:
            if suite:
                s_id  = suite.split(':')[0]
                suite = suite.split(':')[1]
                print('    - (id {}) {}'.format(s_id, suite))
                files = proxy.get_suite_files(ep, s_id)
                if not files:
                    print('      - empty')
                else:
                    for f_id in files:
                        fname = proxy.get_file_variable(ep, f_id, 'file')
                        fstat = proxy.get_file_variable(ep, f_id, 'status') or STATUS_PENDING
                        if option == 'running' and fstat != STATUS_WORKING:
                            continue
                        elif (option=='done' or option=='finished') and \
                            fstat in [STATUS_PENDING, STATUS_WORKING, STATUS_INVALID]:
                            continue
                        elif option == 'pending' and fstat != STATUS_PENDING:
                            continue
                        print('      - [{}] (id {}) {}'.format(TEST_STATUS[fstat], f_id, fname))
            else:
                print('    - nothing here')
        print

    return True


def queue_test(proxy, suite, fname):
    """
    Queue a file, at the end of a suite.
    """
    r = proxy.queue_file(suite, fname)
    if r is True or 'ERROR' not in r:
        print('Test `{}` was queued in suite `{}`.'.format(fname, suite))
    else:
        print(r)

    print


def de_queue_test(proxy, data):
    """
    Un-Queue a file, from the current project.
    """
    r = proxy.de_queue_files(data)
    if r is True or 'ERROR' not in r:
        print('Tests `{}` removed from the project.'.format(r))
    else:
        print(r)

    print


def run_test(user, sut, fname):
    """
    Run a test blocking and show the logs.
    """
    global PROXY

    def stop_ep(*arg, **kw):
        """ stop EP execution """
        print('\nWill exit and stop the EP !')
        return PROXY.set_ep_status_all(0)
    # Capture signal
    signal.signal(signal.SIGINT, stop_ep)

    r = False
    sut = sut.strip('/')
    r = PROXY.del_settings_key('project', '//TestSuite', -1)
    print('Cleanup the old suites...')
    s = PROXY.get_sut('/{}'.format(sut))
    print('Suts found: {}'.format(s))
    eps = [e for e in s['meta'].get('_epnames_'+user, '').split(';') if e]
    if not eps:
        print('Cannot find EPs on SUT `{}`, for user `{}`! Exiting!\n'.format(sut, user))
        return False
    r = PROXY.set_persistent_suite('Suite1', {'ep': eps[0], 'sut': sut})
    print('Created suite: `Suite1` on SUT `{}` and EP `{}`.'.format(sut, eps[0]))
    r = PROXY.set_persistent_file('Suite1', fname, {})
    print('Added file: `{}`.'.format(fname))
    print('Started execution!...')
    PROXY.set_ep_status_all(2)
    while 1:
        status = PROXY.get_ep_status_all()
        if status.startswith('stopped'):
            break
        time.sleep(1)
    print('Execution complete.\n')
    log = PROXY.get_log_file(1, 0, eps[0]+'_CLI.log')
    print(binascii.a2b_base64(log))


def string_check(option, opt, value, parser):
    """
    Verify input string.
    """
    # Break the option instance into a list
    # Formed by pair [short_version/long_version] (e.g. [-u/--users])
    # We want to get the long_version
    pair_list = str(option).split("/")
    if len(pair_list) == 1:
        alternate_string = pair_list[0]
    else:
        alternate_string = pair_list[1]

    # Check if the long version is in parameters list. Special case for -u
    if alternate_string in parser._get_args(None) or opt == '-u':
        if alternate_string == '--eps':
            parser.values.eps = True
        elif alternate_string == '--users':
            parser.values.users = True
        elif alternate_string == '--stats':
            parser.values.stats = True
        elif alternate_string == '--details':
            parser.values.details = 'all'
        elif alternate_string == '--status-details':
            # status-details needs an argument; we want to get it and
            # compare with possible options (all,finished,pending,running)
            param_list = parser._get_args(None)
            try:
                option = param_list[param_list.index(alternate_string)+1]
            except Exception:
                option = None
            if option in ['all', 'finished', 'pending', 'running']:
                parser.values.status_details = option
            else:
                parser.values.status_details = None
    else:
        print 'Bad option!'
        print 'Usage: cli --server <ip:port> --command [...parameters]'
        exit(1)


# --------------------------------------------------------------------------------------------------
#   M a i n
# --------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    USAGE = "Usage: %prog --server <ip:port> --command [...parameters]"

    VERSION = ""
    for line in open(__file__):
        if line.strip().startswith("# version:"):
            VERSION = "%prog " + line.split("version:")[1]
        if VERSION:
            break

    PARSER = OptionParser(usage=USAGE, version=VERSION)

    # Set the dafault values for None to make sure thay will exist in parser list for any scenario
    PARSER.set_defaults(users=None, eps=None, stats=None, details=None, status_details=None)

    # The most important option is the server.
    PARSER.add_option("--server",      action="store", default="127.0.0.1:8000",
        help="The Central Engine IP : port (default= 127.0.0.1:8000)")
    # The second important option is the user and password.
    PARSER.add_option("--login",      action="store", default="user:password",
        help="Login on the Central Engine with user : password (default= user:password)")

    PARSER.add_option('-u', "--users", action="callback", callback=string_check, help="Show active and inactive users.")

    PARSER.add_option("--eps",         action="callback", callback=string_check, help="Show active and inactive Eps.")

    PARSER.add_option("--stats",       action="callback", callback=string_check, help="Show stats.")

    PARSER.add_option("--details",        action="callback", \
        callback=string_check, help="Show detailed status for All files.")
    PARSER.add_option("--status-details", action="callback", \
        callback=string_check, help="Show detailed status for running, finished, pending, or all files.")

    PARSER.add_option("-q", "--queue",   action="store", help="Queue a file ' \
        'at the end of a suite. Specify queue like `Suite:file_path`.")
    PARSER.add_option("-d", "--dequeue", action="store", help="Un-Queue 1 or' \
        ' more files. Specify like `EP, EP:suite_id, EP:Suite, or EP:file_id`.")

    PARSER.add_option("--run-test",      action="store", help="Add a file in' \
        ' a suite, run blocking and then show the log. Specify the fname and the SUT.")
    PARSER.add_option("--sut",           action="store", help="Use this with the `run-test` option.")

    PARSER.add_option("-s", "--set",     action="store", help="Set status: ' \
        'start/ stop/ pause. (Must also specify a config and a project)")
    PARSER.add_option("-c", "--config",  action="store", help="Path to FWMCONFIG.XML file.")
    PARSER.add_option("-p", "--project", action="store", help="Path to PROJECT.XML file.")

    (OPTIONS, ARGS) = PARSER.parse_args()


    if OPTIONS.login:
        try:
            USER, PASSWD = OPTIONS.login.split(':')[0], ':'.join(OPTIONS.login.split(':')[1:])
        except Exception:
            print('Cannot split the provided username:password combination! Exiting !\n')
            exit(1)
    else:
        print('Must provide a username:password combination! Exiting !\n')

    # Test if user did install Twister
    if os.path.isdir(user_home() + os.sep + 'twister'):
        print('\nHello, user `{}`.'.format(USER))
    else:
        print('Username `{}` must install Twister before using this script ! Exiting !\n'.format(USER))
        exit(1)


    if OPTIONS.server:
        try:
            CE_IP, CE_PORT = OPTIONS.server.split(':')
            # Transform XML-RPC port into RPyc Port; RPyc port = XML-RPC port + 10 !
            CE_PORT = int(CE_PORT) + 10
        except Exception:
            print('Cannot split the CE IP:Port combination `{}` ! Exiting !\n'.format(OPTIONS.server))
            exit(1)
    else:
        print('Must provide a CE IP:Port combination! Exiting !\n')


    # RPyc config
    CONFIG = {
        'allow_pickle': True,
        'allow_getattr': True,
        'allow_setattr': True,
        'allow_delattr': True,
        'allow_all_attrs': True,
        }

    # Connect to RPyc server
    try:
        CE = rpyc.connect(CE_IP, CE_PORT, config=CONFIG)
        CE.root.hello('CLI::' + USER)
    except Exception as e:
        print('*ERROR* Cannot connect to CE path `{}:{}`! Exception: `{}`!\n'.format(CE_IP, CE_PORT, e))
        exit(1)

    # Authenticate on RPyc server
    try:
        CHECK = CE.root.login(USER, PASSWD)
        if CHECK:
            print('Authentication successful!\n')
    except Exception as e:
        print('*ERROR* Cannot authenticate on CE path `{}:{}`! Exception: `{}`!\n'.format(CE_IP, CE_PORT, e))
        exit(1)

    if not CHECK:
        print('*ERROR* Cannot authenticate on CE path `{}:{}`! Exiting !\n'.format(CE_IP, CE_PORT))
        exit(1)
    else:
        PROXY = CE.root


    # Check active and inactive users
    if OPTIONS.users:
        check_users(PROXY)
        exit()


    # Check active and inactive EPs
    if OPTIONS.eps:
        check_eps(PROXY)
        exit()


    # Check stats
    if OPTIONS.stats:
        if not check_status(PROXY):
            print 'Stats not available.\n'
        exit()


    # Check status details
    if OPTIONS.details or OPTIONS.status_details:
        OPT = OPTIONS.details or OPTIONS.status_details
        check_details(PROXY, USER, OPT)
        exit()


    # Queue a file at the end of a suite
    if OPTIONS.queue:
        if not ':' in OPTIONS.queue:
            print('Must queue `suite:file`, for example `Suite1:/home/user/some_file.py` !\n')
            exit(1)
        SUITE, FNAME = OPTIONS.queue.split(':')
        queue_test(PROXY, SUITE, FNAME)
        exit()


    # Un-Queue a file, using the File ID
    if OPTIONS.dequeue:
        de_queue_test(PROXY, OPTIONS.dequeue)
        exit()


    # Run a single test, using the File path and the SUT
    if OPTIONS.run_test:
        if not OPTIONS.sut:
            print('Must specify a SUT to run this file!')
            exit(1)
        run_test(USER, OPTIONS.sut, OPTIONS.run_test)
        exit()


    # If all the other options are not available, it means the command must be a status change.
    if not OPTIONS.set:
        print('You didn\'t specify a command ! Exiting !\n')
        exit(1)
    if OPTIONS.set.lower() not in ['stop', 'start', 'pause']:
        print('Must specify a valid status (stop/ start/ pause) ! Exiting !\n')
        exit(1)

    if not OPTIONS.config:
        OPTIONS.config = ''
    if not OPTIONS.project:
        OPTIONS.project = ''

    if (not OPTIONS.config) and OPTIONS.set == 'start':
        print('Must specify a config path ! Exiting !\n')
        exit(1)
    if OPTIONS.config and ( not os.path.isfile(OPTIONS.config) ):
        print('Must specify a valid config path, that path does not exist ! Exiting !\n')
        exit(1)
    if (not OPTIONS.project) and OPTIONS.set == 'start':
        print('Must specify a project path ! Exiting !\n')
        exit(1)
    if OPTIONS.project and ( not os.path.isfile(OPTIONS.project) ):
        print('Must specify a valid project path, that path does not exist ! Exiting !\n')
        exit(1)

    if OPTIONS.set == 'start':
        print 'Starting...'
        print PROXY.set_ep_status_all(2, OPTIONS.config + ',' + OPTIONS.project)

    elif OPTIONS.set == 'stop':
        print 'Stopping...',
        print PROXY.set_ep_status_all(0, OPTIONS.config + ',' + OPTIONS.project)

    elif OPTIONS.set == 'pause':
        print 'Sending pause...',
        print PROXY.set_ep_status_all(1, OPTIONS.config + ',' + OPTIONS.project)

    print

# Eof()
