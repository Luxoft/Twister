
# File: TestCaseRunnerClasses.py ; This file is part of Twister.

# Copyright (C) 2012 , Luxoft

# Authors:
#    Andrei Costachi <acostachi@luxoft.com>
#    Andrei Toma <atoma@luxoft.com>
#    Cristian Constantin <crconstantin@luxoft.com>
#    Daniel Cioata <dcioata@luxoft.com>

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
REQUIRED Python 2.7
This file contains classes that will run TCL/ Python/ Perl test cases.
This script CANNOT run separately, it must be called from TestCaseRunner.
'''

import os
import sys
import time
import subprocess

from collections import OrderedDict # For dumping TCL

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print('TWISTER_PATH environment variable is not set! Exiting!')
    exit(1)

#

class TCRunTcl:

    def __init__(self):

        global TWISTER_PATH
        if not TWISTER_LIBS_PATH in sys.path:
            sys.path.append(TWISTER_LIBS_PATH) # Injected EP name

        try:
            import Tkinter
        except:
            print('*ERROR* Cannot import Python Tkinter! Exiting!')
            exit(1)

        try:
            tcl = Tkinter.Tcl()
        except:
            print('*ERROR* Cannot create TCL console! Exiting!')
            exit(1)

        DEFAULT_INFO_VARS = ['_tkinter_skip_tk_init', 'argc', 'argv', 'argv0', 'auto_index', 'auto_oldpath',
            'auto_path', 'env', 'errorCode', 'errorInfo', 'tcl_interactive', 'tcl_libPath', 'tcl_library',
            'tcl_patchLevel', 'tcl_pkgPath', 'tcl_platform', 'tcl_rcFileName', 'tcl_version', 'exp_library',
            'expect_library', 'exp_exec_library']

        DEFAULT_INFO_PROCS = ['auto_execok', 'auto_import', 'auto_load', 'auto_load_index', 'auto_qualify',
            'clock', 'history', 'tclLog', 'unknown', 'pkg_mkIndex']

        self.all_vars = 0
        self.all_vars_values = 0
        self.all_procs = 0
        self.all_procs_values = 0

        import ce_libs

        dir(ce_libs) # Update ?

        self.tcl = Tkinter.Tcl()
        # Expose all known function, in TCL
        self.tcl.createcommand('logMessage',          ce_libs.logMsg)
        # self.tcl.createcommand('setProperty',         ce_libs.setProperty)
        # self.tcl.createcommand('getProperty',         ce_libs.getProperty)
        # self.tcl.createcommand('delResource',         ce_libs.delResource)
        # self.tcl.createcommand('createEmptyResource', ce_libs.createEmptyResource)

        if os.path.exists(os.getcwd()+'/__recomposed.tcl'):
            # Restore all variables and functions
            self.tcl.evalfile(os.getcwd()+'/__recomposed.tcl')

        # self.tcl.eval('package require Expect')

    def __del__(self):
        #
        # On clean exit, reset _recomposed file
        del self.tcl
        open(os.getcwd()+'/__recomposed.tcl', 'w').close()
        try: os.remove('__recomposed.tcl')
        except: pass
        #

    def _eval(self, str_to_execute, globs={}, params=[]):
        '''
        After executing a TCL statement, the last value will be used
        as return value.
        '''
        #
        self.tcl.setvar('gparam', globs['gparam'])
        #
        to_execute = str_to_execute.data
        #
        to_execute = '\nset argc %i\n' % len(params) + to_execute
        to_execute = 'set argv {%s}\n' % str(params)[1:-1] + to_execute
        #
        _RESULT = self.tcl.eval(to_execute)
        return _RESULT
        #

    def dump_tcl(tcl):
        '''
        Dumps all TCL Variables and Procedures in a file called "__recomposed.tcl".
        This file can be executed later; all vars and procs should be restored correctly.
        Default variables like "argc", "argv", "tcl_platform", etc are ignored.
        Default procedures like "clock", "history", etc are also ignored.
        '''

        # Find all TCL variables !
        self.all_vars = [var0 for var0 in tcl.eval('info vars').split() if var0 not in DEFAULT_INFO_VARS]
        # Everything must be restored in order
        self.all_vars_values = OrderedDict()

        for var in self.all_vars:
            #
            try:
                v = tcl.getvar(var)
            except Tkinter.TclError, e:
                if str(e).endswith('variable is array'):
                    # Recomposed arrays
                    v = tcl.eval('array get %s' % var)
                else:
                    print 'TC Dump Warning: Cannot get value for var `%s`!' % var
                    try: tcl.eval('puts $'+var)
                    except: pass
                    v = ''

            self.all_vars_values[var] = v
            #

        #print('\nProcessing variables...')
        #print(self.all_vars_values)

        # Find all TCL functions !
        self.all_procs = [proc0 for proc0 in tcl.eval('info procs').split() if proc0 not in DEFAULT_INFO_PROCS]
        # Everything must be restored in order
        self.all_procs_values = OrderedDict()
        tcl.eval('set vDefaultArg ""')

        for proc in self.all_procs:
            #
            proc_body = tcl.eval('info body %s' % proc)
            proc_args = tcl.eval('info args %s' % proc)
            compose_args = []
            #
            for arg in proc_args.split():
                has_default = tcl.eval('info default %s %s vDefaultArg' % (proc, arg))
                # If this argument has a default value
                if int(has_default) and tcl.getvar('vDefaultArg'):
                    default_value = tcl.getvar('vDefaultArg')
                    compose_args.append('%s {%s}' % (arg, str(default_value)))
                else:
                    compose_args.append(arg)
                # Reset variable for the next cycle
                tcl.eval('set vDefaultArg ""')

            self.all_procs_values[proc] = ('proc '+proc+' {'+' '.join(compose_args)+'} {'+proc_body+'}')
            #

        tcl.eval('unset vDefaultArg')
        #print('\nProcessesing functions...')
        #print(self.all_procs_values)

        f = open(os.getcwd()+'/__recomposed.tcl', 'w')
        f.write('\n# Recomposed...\n\n')
        for var in self.all_vars_values:
            f.write('variable %s {%s}\n' % (var, self.all_vars_values[var]))
        for proc in self.all_procs_values:
            f.write('\n')
            f.write(self.all_procs_values[proc])
            f.write('\n')
        f.close() ; del f

#

class TCRunPython:

    def _eval(self, str_to_execute, globs={}, params=[]):
        '''
        Variable `_RESULT` must be injected inside the exec,
        or else the return will always be None.
        '''
        #
        global TWISTER_PATH
        if not TWISTER_LIBS_PATH in sys.path:
            sys.path.append(TWISTER_LIBS_PATH) # Injected EP name

        # Start injecting inside tests
        globs_copy = {}
        globs_copy['os']   = os
        globs_copy['sys']  = sys
        globs_copy['time'] = time

        globs_copy['SUITE_ID']   = globs['suite_id']
        globs_copy['SUITE_NAME'] = globs['suite_name']
        globs_copy['FILE_ID']    = globs['file_id']
        globs_copy['FILE_NAME']  = globs['filename']
        globs_copy['USER']       = globs['userName']
        globs_copy['EP']         = globs['globEpName']
        globs_copy['PROXY']      = globs['proxy']
        globs_copy['gparam']     = globs['gparam']

        globEpName = globs_copy['EP']
        to_execute = str_to_execute.data
        to_execute = '\nimport os, sys\nsys.argv = %s\n' % str(["file.py"] + params) + to_execute
        to_execute = '\nsys.path.append(os.getenv("TWISTER_PATH") + "/.twister_cache/")\n' + to_execute

        # *.pyc or *.pyo files
        if to_execute[:4] == '\x03\xf3\r\n':
            fname = '/__to_execute.pyc'
        else:
            fname = '/__to_execute.py'

        fname = TWISTER_PATH + '/.twister_cache/' + globEpName + fname
        f = open(fname, 'wb')
        f.write(to_execute)
        f.close() ; del f

        execfile(fname, globs_copy)
        try: os.remove(fname)
        except: pass

        # The _RESULT must be injected from within the python script
        return globs_copy.get('_RESULT')
        #

#

class TCRunPerl:

    def _eval(self, str_to_execute, globs={}, params=[]):
        '''
        Perl test runner.
        '''
        #
        if not TWISTER_LIBS_PATH in sys.path:
            sys.path.append(TWISTER_LIBS_PATH) # Injected EP name
        #
        _RESULT = None
        to_execute = str_to_execute.data
        #
        f = open('__to_execute.plx', 'wb')
        f.write(to_execute)
        f.close() ; del f
        #
        proc = subprocess.Popen('perl' + ' __to_execute.plx', shell=True, bufsize=1)
        ret = proc.communicate()
        time.sleep(0.5)
        #
        try: os.remove('__to_execute.plx')
        except: pass
        #
        # The _RESULT must be injected from within the perl script
        return _RESULT
        #

#
