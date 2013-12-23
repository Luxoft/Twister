
# File: SchedulerServer.py ; This file is part of Twister.

# version: 2.003

# Copyright (C) 2012 , Luxoft

# Authors:
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

import os
import sys
import thread
import threading
import subprocess
import urlparse
import socket
socket.setdefaulttimeout(3)
import xmlrpclib
import logging
import json

import time
import calendar
from datetime import datetime
from ConfigParser import SafeConfigParser

import cherrypy
from cherrypy import _cptools

"""
Scheduler Server
****************

It's used to schedule the start of Central Engine weekly, daily, or one-time.
"""

# # #

def userHome(user):
    """
    Find the home folder for the given user.
    """
    return subprocess.check_output('echo ~' + user, shell=True).strip()


def _fix_date(date_time):
    '''
    Receives a date string and returns a Date-Time object and the type of task.
    '''

    # If DT has both date and time, or a weekday and time
    if ' ' in date_time:
        part1 = date_time.split()[0]

        # If the first part is the Short name of a week day
        if part1 in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']:
            try:
                dt = time.strptime(date_time, '%a %H:%M:%S')
                proj_type = 'weekly'
            except:
                log.error('Invalid Weekday-time format: `{0}` !'.format(date_time))
                return False, ''
        # If the first part is the Long name of a week day
        elif part1 in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            try:
                dt = time.strptime(date_time, '%A %H:%M:%S')
                proj_type = 'weekly'
            except:
                log.error('Invalid Weekday-time format: `{0}` !'.format(date_time))
                return False, ''
        else:
            try:
                dt = time.strptime(date_time, '%Y-%m-%d %H:%M:%S')
                proj_type = 'one-time'
            except:
                log.error('Invalid Date-time format: `{0}` !'.format(date_time))
                return False, ''

    # If DT has only time, and Not date
    else:
        try:
            dt = time.strptime(date_time, '%H:%M:%S')
            proj_type = 'daily'
        except:
            log.error('Invalid Time-only format: `{0}` !'.format(date_time))
            return False, ''

    return dt, proj_type

# # #


class SchedulerServer(_cptools.XMLRPCController):

    def __init__(self):

        global __config__
        log.debug('Initializing Server on http://{sched_ip}:{sched_port}/ ...'.format(**__config__))
        self.acc_lock = thread.allocate_lock() # Task change lock
        self.tasks = {}
        self._load(v=True)

#

    def _load(self, v=False):

        global __dir__

        if __dir__:
            path = __dir__ + os.sep + 'schedule.json'
        else:
            path = 'schedule.json'

        try:
            f = open(path, 'r')
            self.tasks = json.load(f)
            f.close() ; del f
            if v:
                log.debug('Tasks loaded successfully.')
        except:
            if v:
                log.debug('There are no tasks to load.')


    def _save(self):

        global __dir__

        if __dir__:
            path = __dir__ + os.sep + 'schedule.json'
        else:
            path = 'schedule.json'

        f = open(path, 'w')
        json.dump(self.tasks, f, indent=4)
        f.close() ; del f

#

    @cherrypy.expose
    def rest(self):
        html = '<html>\n<title>Scheduler Server REST</title>\n<body>\n<br>\n{0}\n</body>\n</html>'
        strings = [
            '<b>~ Task {0}:</b> {proj-type} task for user <b>{user}</b> ~<br> &nbsp;'
            'File `{project-file}`, activation date '
            '`{date-time}`, force `{force}`, time limit `{time-limit}`;<br>\n'
            ''.format(k.keys()[0], **k.values()[0]) for k in self.List()
            ]
        return html.format('<br>'.join(strings))


    @cherrypy.expose
    def List(self, user=None):
        """
        Return all available tasks.
        """
        with self.acc_lock:
            self._load()

        result = []
        if user:
            for k, v in self.tasks.iteritems():
                if v['user'] != user:
                    continue
                d = dict(v)
                d['key'] = k
                result.append(d)
        else:
            for k, v in self.tasks.iteritems():
                d = dict(v)
                d['key'] = k
                result.append(d)
        return result


    @cherrypy.expose
    def Add(self, user, args):
        """
        Create a New task.
        A valid task must have:
        - description
        - date/ day/ time
        - project file
        - force?
        - limit time to x
        """

        # Example tasks:
        # {'description':'', 'project-file':'C:/autoexec.bat', 'date-time':'12:12:12', 'force':'0', 'time-limit':'0'}
        # {'description':'', 'project-file':'C:/autoexec.bat', 'date-time':'Wednesday 12:12:12', 'force':'0', 'time-limit':'0'}
        # {'description':'', 'project-file':'C:/autoexec.bat', 'date-time':'2012-12-12 12:12:12', 'force':'1', 'time-limit':'0'}

        # If argument is a string
        if type(args) == type(str()):
            task = urlparse.parse_qs(args)
        # If argument is a valid dict
        elif type(args) == type(dict()):
            task = args
        else:
            msg = 'Add task: Invalid type of argument for add task: `{0}` !'.format(type(args))
            log.error(msg)
            return '*ERROR* ' + msg

        # if not self.conn:
        #     print('Cannot add task! Central Engine connection not available !')
        #     return False
        # elif self.conn.getUserVariable(user, 'status') == False:
        #     print('Cannot add task! Invalid username `{0}` !'.format(user))
        #     return False

        descrip    = task.get('description')
        proj_file  = task.get('project-file')
        proj_dt    = task.get('date-time')
        proj_force = task.get('force')
        time_limit = task.get('time-limit')

        if not os.path.isfile(proj_file):
            msg = 'Add task: Invalid file path `{0}` !'.format(proj_file)
            log.error(msg)
            return '*ERROR* ' + msg

        dt, proj_type = _fix_date(proj_dt)
        if not dt: return False

        # Duplicate dates?
        if proj_dt in [v['date-time'] for v in self.tasks.values()]:
            msg = 'Add task: Duplicate date-time: `{0}` !'.format(proj_dt)
            log.error(msg)
            return '*ERROR* ' + msg

        # If force is not valid, reset it. By default, force is enabled.
        if proj_force != '0':
            proj_force = '1'

        try:
            time_limit = int(time_limit)
        except:
            log.error('Add task: Invalid Time-limit number: `{0}` ! Will default to ZERO.'.format(time_limit))
            time_limit = 0
            if time_limit < 0:
                time_limit = 0

        # This can only be executed by 1 thread at a time,
        # so there will never be 2 threads that create tasks at the same time
        with self.acc_lock:

            created_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

            task_fixed = {
                'user' : user,
                'description' : descrip,
                'project-file': proj_file,
                'date-time'   : proj_dt,
                'force'       : proj_force,
                'time-limit'  : time_limit,
                'proj-type'   : proj_type
            }

            self.tasks[created_time] = task_fixed

            log.debug('Created {proj-type} task for user {user} :: File `{project-file}`, activation date '
                '`{date-time}`, force `{force}`, time limit `{time-limit}`.\n'.format(**task_fixed))

            self._save()

        return created_time


    @cherrypy.expose
    def Change(self, key, args):
        """
        Update a task. Must supply its key.
        """

        if not key in self.tasks:
            msg = 'Change task: Invalid task key `{0}` !'.format(key)
            log.error(msg)
            return '*ERROR* ' + msg

        # If argument is a string
        if type(args) == type(str()):
            task = urlparse.parse_qs(args)
        # If argument is a valid dict
        elif type(args) == type(dict()):
            task = args
        else:
            msg = 'Change task: Invalid type of argument for add task: `{0}` !'.format(type(args))
            log.error(msg)
            return '*ERROR* ' + msg

        descrip    = task.get('description')
        proj_file  = task.get('project-file')
        proj_dt    = task.get('date-time')
        proj_force = task.get('force')
        time_limit = task.get('time-limit')

        # If user wants to change project path
        if proj_file:
            if not os.path.isfile(proj_file):
                msg = 'Change task: Invalid file path `{0}` !'.format(proj_file)
                log.error(msg)
                return '*ERROR* ' + msg

        # If user wants to change Date-Time
        if proj_dt:
            dt, proj_type = _fix_date(proj_dt)
            if not dt: return False

        # If user wants to change Force
        if proj_force:
            if proj_force != '0':
                proj_force = '1'

        # If user wants to change time limit
        if time_limit:
            try:
                time_limit = int(time_limit)
            except:
                log.error('Change task: Invalid Time-limit number: `{0}` ! Will default to ZERO.'.format(time_limit))
                time_limit = 0
            if time_limit < 0:
                time_limit = 0

        # Preparing updated task
        task_fixed = {}

        if descrip:
            if descrip != self.tasks[key]['description']:
                task_fixed['description'] = descrip

        if proj_file:
            task_fixed['project-file'] = proj_file

        if proj_dt:
           task_fixed['date-time'] = proj_dt
           task_fixed['proj-type'] = proj_type

        if proj_force:
            if proj_force != self.tasks[key]['force']:
                task_fixed['force'] = proj_force

        if time_limit is not None:
            if time_limit != self.tasks[key]['time-limit']:
                task_fixed['time-limit'] = time_limit

        # This can only be executed by 1 thread at a time,
        # so there will never be 2 threads that create tasks at the same time
        with self.acc_lock:

            self.tasks[key].update(task_fixed)

            log.debug('Updated task {0} :: File `{project-file}`, activation date `{date-time}`,'
                ' type `{proj-type}`, force `{force}`, time limit `{time-limit}`.\n'.format(key, **self.tasks[key]))

            self._save()

        return True


    @cherrypy.expose
    def Update(self, key, args):
        """
        Update a task. Must supply its key.
        """
        return self.Change(user, key, args)


    @cherrypy.expose
    def Remove(self, user, key):
        """
        Delete a task. Must supply its key.
        """
        if not key in self.tasks:
            msg = 'Remove task: Invalid task key `{0}` !'.format(key)
            log.error(msg)
            return '*ERROR* ' + msg

        with self.acc_lock:
            log.debug('Removing task key `{0}` !'.format(key))
            del self.tasks[key]
            self._save()

        return True


    @cherrypy.expose
    def Delete(self, user, key):
        """
        Delete a task. Must supply its key.
        """
        return self.Remove(user, key)

# # #

class threadCheckTasks(threading.Thread):
    '''
    Threaded class for checking tasks.
    '''
    def __init__(self):

        global __config__
        self.errMsg = True
        self.conns = {}
        threading.Thread.__init__(self)


    def getConnection(self, user):
        '''
        Shortcut function to get or reuse a Central Engine connection.
        '''
        proxy = self.conns.get(user)
        # Try to reuse the old connection
        if isinstance(proxy, xmlrpclib.ServerProxy):
            try:
                proxy.echo('ping')
                return proxy
            except:
                log.debug('Disconnected from the Central Engine. Will reconnect...')
                proxy = None
        else:
            log.debug('Connect to the Central Engine...')
            proxy = None

        proxy = xmlrpclib.ServerProxy('http://{u}:EP@{ce_ip}:{ce_port}/'.format(u=user, **__config__))

        try:
            # Try to ping the Central Engine!
            proxy.echo('ping')
            if not self.errMsg:
                log.debug('Successfully connected to Central Engine. Tasks are now enabled.')
                self.errMsg = True
        except:
            if self.errMsg:
                log.debug('Central Engine is down, cannot run Tasks! Trying to reconnect...')
                self.errMsg = False
            proxy = None

        self.conns[user] = proxy
        return proxy


    def run(self):
        '''
        Chech time to see if CE must be started.
        If force, if CE is running, start it again with the new config.
        Else, don't start CE.
        If time limit, the status of CE must be recorded;
        if CE is stopped, the time limit check must be aborted,
        because it means the job is no longer running !
        '''

        time.sleep(0.1)
        global root, programExit

        while not programExit:

            Tasks = root.List()

            # Date time into standard format
            date_time = time.strptime(time.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
            pure_time = time.strptime(time.strftime('%H:%M:%S'), '%H:%M:%S')
            week_time = time.strptime(time.strftime('%a %H:%M:%S'), '%a %H:%M:%S')

            # Cycle all known tasks
            for glob_task in Tasks:

                task_id = glob_task.get('key')
                if not task_id:
                    log.error('Badly formed task! No key detected! Debug data: `{0}`.'.format(glob_task))
                    continue

                task = dict(root.tasks[task_id]) # Make a copy

                user       = task.get('user')
                proj_file  = str(task.get('project-file'))
                proj_dt    = task.get('date-time')
                proj_force = str(task.get('force'))
                time_limit = task.get('time-limit')

                if not user:
                    log.error('Fatal error in task `{0}`! No user defined!'.format(task_id))
                    continue

                proxy = self.getConnection(user)
                # No connection for this user
                if not isinstance(proxy, xmlrpclib.ServerProxy):
                    time.sleep(2)
                    continue

                proj_dt, proj_type = _fix_date(proj_dt)
                if not proj_dt: continue
                task.update({'proj-type': proj_type})

                # If task is 1 time and the time is not right, continue
                if proj_type == 'one-time' and proj_dt != date_time:
                    continue
                # If the task is daily and the time is not right, continue
                elif proj_type == 'daily' and proj_dt != pure_time:
                    continue
                # If the task is weekly and time is not right, continue
                elif proj_type == 'weekly' and proj_dt != week_time:
                    continue

                log.debug('Starting {proj-type} task for user {user} :: File `{project-file}`, '
                      'activation date `{date-time}`, force `{force}`, time limit `{time-limit}`...'.format(**task))

                # If Force is disabled and Central Engine is already running, break
                if proj_force != '0' and proxy.getUserVariable(user, 'status') == 'running':
                    log.debug('Central Engine is already running! The task will not force!')
                    continue
                else:
                    # Kill all processes for this user
                    proxy.setExecStatusAll(user, 0, 'Force stop from Scheduler!'.format(proj_file))

                time.sleep(1)

                # Start Central Engine !
                proxy.setExecStatusAll(user, 2, '{}/twister/config/fwmconfig.xml,{}'.format(userHome(user), proj_file))

            # Wait before next cycle
            time.sleep(1)

        log.debug('Closing Tasks thread...')

# # #

def load_config():

    global __dir__
    cfg_folder = __dir__ + '/config.ini'
    cfg_dict   =  {'ce_ip': '127.0.0.1', 'ce_port': '8000',
                   'sched_ip': '0.0.0.0', 'sched_port': '88'}
    cfg = SafeConfigParser({'ALL': '0.0.0.0'})
    cfg.read(cfg_folder)

    if not os.path.isfile(cfg_folder):
        cfg.add_section('CONFIG')
        for k, v in cfg_dict.iteritems():
            cfg.set('CONFIG', k, v)
        cfg.write(open(cfg_folder, 'w'))
    else:
        cfg_dict.update( dict(cfg.items('CONFIG')) )

    return cfg_dict


def close():

    global programExit
    log.debug('\nClosing Scheduler...')
    programExit = True

# # #


if __name__ == '__main__':

    __dir__ = os.path.split(__file__)[0]
    if not __dir__: __dir__ = os.getcwd()
    __config__ = load_config()
    programExit = False


    LOGS_PATH = __dir__ + '/Logs/'
    if not os.path.exists(LOGS_PATH):
        os.makedirs(LOGS_PATH)

    # Config cherrypy logging
    cherrypy.log.access_log.propagate = False
    cherrypy.log.error_log.setLevel(logging.DEBUG)
    log = cherrypy.log.error_log

    # Config python logging
    dateTag = datetime.now().strftime("%Y-%b-%d %H-%M-%S")
    LOG_FILE = LOGS_PATH + 'Log %s.txt' % dateTag
    logging.basicConfig(level=logging.NOTSET, format='%(asctime)s  %(levelname)-8s %(message)s',
                        datefmt='%y-%m-%d %H:%M:%S', filename=LOG_FILE, filemode='w')

    console = logging.StreamHandler()
    console.setLevel(logging.NOTSET)
    log.addHandler(console)


    # Root path
    root = SchedulerServer()

    # Config
    conf = {
        'global': {
            'server.socket_host': str(__config__['sched_ip']),
            'server.socket_port': int(__config__['sched_port']),
            'engine.autoreload.on': False,
            'log.screen': False
            }
        }

    # Start !
    threadCheckTasks().start()
    cherrypy.engine.subscribe('exit',  close)
    cherrypy.quickstart(root, '/', config=conf)
    programExit = True

#
