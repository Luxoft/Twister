
# File: TestCaseRunnerClasses.py ; This file is part of Twister.

# version: 3.012

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

"""
REQUIRED Python 2.7.
This file contains classes that will run TCL/ Python/ Perl test cases.
This script CANNOT run separately, it must be called from TestCaseRunner.
"""
from __future__ import with_statement

import os
import sys
import time
import glob
import json
from shutil import copyfile

import subprocess # For running Perl/ Jython
from subprocess import PIPE
from collections import OrderedDict # For dumping TCL
from ConfigParser import SafeConfigParser # For parsing Jython config

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print 'TWISTER_PATH environment variable is not set! Exiting!'
    exit(1)


__all__ = ['TCRunTcl', 'TCRunPython', 'TCRunPerl', 'TCRunJava']


class TCRunTcl(object):
    """
    TCL runner class.
    """
    epname = ''
    all_vars = 0
    all_vars_values = 0
    all_procs = 0
    all_procs_values = 0

    def __init__(self):

        try:
            import Tkinter
        except Exception:
            raise Exception('*ERROR* Cannot import Python Tkinter! Exiting!')

        try:
            self.tcl = Tkinter.Tcl()
        except Exception:
            raise Exception('*ERROR* Cannot create TCL console! Exiting!')

        if os.path.exists(os.getcwd()+'/__recomposed.tcl'):
            # Restore all variables and functions
            self.tcl.evalfile(os.getcwd()+'/__recomposed.tcl')

        # self.tcl.eval('package require Tcl')
        # self.tcl.eval('package require Expect')

    def __del__(self):
        """
        On exit delete all recomposed and Tcl files
        """
        del self.tcl
        open(os.getcwd()+'/__recomposed.tcl', 'w').close()
        try:
            os.remove('__recomposed.tcl')
        except Exception:
            pass
        fnames = '{}/.twister_cache/{}/*.tcl'.format(TWISTER_PATH, self.epname)
        for fname in glob.glob(fnames):
            # print('Cleanup TCL file:', fname)
            try:
                os.remove(fname)
            except Exception:
                pass

    def _eval(self, str_to_execute, globs={}, params=[]):
        '''
        After executing a TCL statement, the last value will be used
        as return value.
        '''
        self.epname = globs['EP']

        # Inject variables
        self.tcl.setvar('USER', globs['USER'])
        self.tcl.setvar('EP', globs['EP'])
        self.tcl.setvar('SUT', globs['SUT'])
        self.tcl.setvar('SUITE_ID', globs['SUITE_ID'])
        self.tcl.setvar('SUITE_NAME', globs['SUITE_NAME'])
        self.tcl.setvar('FILE_ID', globs['FILE_ID'])
        self.tcl.setvar('FILE_NAME', globs['FILE_NAME'])
        self.tcl.setvar('CONFIG', ';'.join(globs['CONFIG']))
        self.tcl.setvar('ITERATION', globs['ITERATION'])
        self.tcl.setvar('FIRST_ITERATOR_VAL', globs['FIRST_ITERATOR_VAL'])
        self.tcl.setvar('FIRST_ITERATOR_NAME', globs['FIRST_ITERATOR_NAME'])
        self.tcl.setvar('FIRST_ITERATOR_COMP', globs['FIRST_ITERATOR_COMP'])

        # Set properties Associative Array
        for k_val, v_val in globs['PROPERTIES'].iteritems():
            self.tcl.eval('set PROPERTIES({}) {}'.format(k_val, v_val))

        # Compatibility log message
        self.tcl.createcommand('logMessage', globs['log_msg'])

        # Inject all functions
        for func in globs:
            # print('DEBUG: Exposing Python command `{}` into TCL...'.format(f))
            if callable(globs[func]):
                self.tcl.createcommand(func, globs[func])

        to_execute = '\nset argc %i\n' % len(params) + str_to_execute
        to_execute = 'set argv {%s}\n' % str(params)[1:-1] + to_execute

        return self.tcl.eval(to_execute)
        #

    def dump_tcl(self, tcl):
        """
        Dumps all TCL Variables and Procedures in a file called "__recomposed.tcl".
        This file can be executed later; all vars and procs should be restored correctly.
        Default variables like "argc", "argv", "tcl_platform", etc are ignored.
        Default procedures like "clock", "history", etc are also ignored.
        """

        default_info_vars = ['_tkinter_skip_tk_init', 'argc', 'argv', 'argv0',\
        'auto_index', 'auto_oldpath', 'auto_path', 'env', 'errorCode',\
        'errorInfo', 'tcl_interactive', 'tcl_libPath', 'tcl_library',\
        'tcl_patchLevel', 'tcl_pkgPath', 'tcl_platform', 'tcl_rcFileName',\
        'tcl_version', 'exp_library', 'expect_library', 'exp_exec_library']

        default_info_procs = ['auto_execok', 'auto_import', 'auto_load',\
        'auto_load_index', 'auto_qualify', 'clock', 'history', 'tclLog',\
        'unknown', 'pkg_mkIndex']

        # Find all TCL variables !
        self.all_vars = [var0 for var0 in tcl.eval('info vars').split() if var0 not in default_info_vars]
        # Everything must be restored in order
        self.all_vars_values = OrderedDict()

        for var in self.all_vars:
            try:
                val = tcl.getvar(var)
            except Tkinter.TclError as exp_err:
                if str(exp_err).endswith('variable is array'):
                    # Recomposed arrays
                    val = tcl.eval('array get %s' % var)
                else:
                    print 'TC Dump Warning: Cannot get value for var `%s`!'\
                    % var
                    try:
                        tcl.eval('puts $'+var)
                    except Exception:
                        pass
                    val = ''

            self.all_vars_values[var] = val

        #print('\nProcessing variables...')
        #print(self.all_vars_values)

        # Find all TCL functions !
        self.all_procs = [proc0 for proc0 in tcl.eval('info procs').split() if proc0 not in default_info_procs]
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

        fname = open(os.getcwd()+'/__recomposed.tcl', 'w')
        fname.write('\n# Recomposed...\n\n')
        for var in self.all_vars_values:
            fname.write('variable %s {%s}\n' % (var, self.all_vars_values[var]))
        for proc in self.all_procs_values:
            fname.write('\n')
            fname.write(self.all_procs_values[proc])
            fname.write('\n')
        fname.close()

#

class TCRunPython(object):
    """
    Python runner class.
    """
    epname = ''
    filename = ''

    def _eval(self, str_to_execute, globs={}, params=[]):
        """
        Variable `_RESULT` must be injected inside the exec,
        or else the return will always be None.
        """
        self.epname = globs['EP']
        self.filename = os.path.split(globs['FILE_NAME'])[1]
        params.insert(0, self.filename)
        fpath = '{}/.twister_cache/{}/{}'.format(TWISTER_PATH, self.epname, self.filename)

        # Start injecting inside tests
        globs_copy = dict(globs)
        globs_copy['os'] = os
        globs_copy['sys'] = sys
        globs_copy['time'] = time

        script_head = """
__file__ = '{}'
sys.argv = {}
""".format(fpath, params)

        fname = open(fpath, 'wb')
        fname.write(script_head)
        fname.write(str_to_execute)
        fname.close()

        execfile(fpath, globs_copy)

        # The _RESULT must be injected from within the python script,
        # or the test will default to FAIL
        # The _REASON is a string
        return globs_copy.get('_RESULT'), globs_copy.get('_REASON', '')
        #


    def __del__(self):
        """
        On exit, delete all Python files.
        """
        fnames = '{}/.twister_cache/{}/*.py*'.format(TWISTER_PATH, self.epname)
        for fname in glob.glob(fnames):
            # print('Cleanup Python file:', fname)
            try:
                os.remove(fname)
            except Exception:
                pass

#

class TCRunPerl(object):
    """
    Perl test runner.
    """
    epname = ''
    filename = ''

    def _eval(self, str_to_execute, globs={}, params=[]):
        """
        Variable `_RESULT` must be injected inside the exec,
        or else the return will always be None.
        """
        self.epname = globs['EP']
        self.filename = os.path.split(globs['FILE_NAME'])[1]
        fdir = '{}/.twister_cache/{}'.format(TWISTER_PATH, self.epname)
        fpath = fdir + os.sep + self.filename

        # String begins with #!/usr/bin/perl ?
        if  str_to_execute[0] == '#':
            str_to_execute = '\n'.join(str_to_execute.split('\n')[1:])

        perl_config = '( ' + json.dumps(globs['CONFIG'])[1:-1] + ' )'
        perl_props = '( ' + json.dumps(globs['PROPERTIES'])[1:-1].replace('": ', '" => ') + ' )'

        text_head = r"""#!/usr/bin/perl

$STATUS_PASS     = 0;
$STATUS_FAIL     = 3;
$STATUS_SKIPPED  = 4;
$STATUS_ABORTED  = 5;
$STATUS_NOT_EXEC = 6;
$STATUS_TIMEOUT  = 7;
$STATUS_INVALID  = 8;

$EP  = TWISTER_EP();
$SUT = TWISTER_SUT();
$USER = TWISTER_USER();
$SUITE_NAME = TWISTER_SUITE_NAME();
$FILE_NAME  = TWISTER_FILE_NAME();
@CONFIG = %s;
%%PROPERTIES = %s;

""" % (perl_config, perl_props)

        text_tail = r"""
use Inline Python => <<"END_OF_PYTHON_CODE";

import os, sys
__file__ = '%s'
sys.argv = %s
sys.path.append('%s')
sys.path.append('%s/ce_libs')
from TscCommonLib import TscCommonLib

commonLib = TscCommonLib()

def TWISTER_USER():
    from ce_libs import USER as x
    return x

def TWISTER_EP():
    from ce_libs import EP as x
    return x

def TWISTER_SUT():
    return commonLib.SUT

def TWISTER_SUITE_NAME():
    return commonLib.SUITE_NAME

def TWISTER_FILE_NAME():
    return commonLib.FILE_NAME

def log_msg(*arg, **kw):
    return commonLib.log_msg(*arg, **kw)

def get_global(*arg, **kw):
    return commonLib.get_global(*arg, **kw)

def set_global(*arg, **kw):
    return commonLib.set_global(*arg, **kw)

def get_config(*arg, **kw):
    return commonLib.get_config(*arg, **kw)

def get_iter_value(*arg, **kw):
    return commonLib.get_iter_value(*arg, **kw)

def get_binding(*arg, **kw):
    return commonLib.get_binding(*arg, **kw)

def get_resource(*arg, **kw):
    return commonLib.get_resource(*arg, **kw)

def set_resource(*arg, **kw):
    return commonLib.set_resource(*arg, **kw)

def get_sut(*arg, **kw):
    return commonLib.get_sut(*arg, **kw)

def set_sut(*arg, **kw):
    return commonLib.set_sut(*arg, **kw)

END_OF_PYTHON_CODE
"""  %  (fpath, str([self.filename] + params), TWISTER_PATH, fdir)

        fname = open(fpath, 'wb')
        fname.write(text_head)
        fname.write(str_to_execute)
        fname.write(text_tail)
        fname.close()

        env = os.environ
        env.update({'TWISTER_PATH': TWISTER_PATH})

        print('~ Perl ~ Compiling Inline::Python ~\n')
        proc = subprocess.Popen('perl '+ fpath, env=env, shell=True, bufsize=1, stderr=PIPE)
        (_, stderr) = proc.communicate()
        time.sleep(0.5)

        try:
            os.remove(fpath)
        except Exception:
            pass

        # The _RESULT must be injected from within the perl script
        if stderr:
            print('~ Perl crashed with error code `{}`! ~\n\n{}'.format(proc.returncode, stderr.strip()))
        else:
            print('\n~ Perl returned code `{}` ~'.format(proc.returncode))
        return proc.returncode
        #

#

class TCRunJava(object):
    """
    Java runner class.
    """
    epname = None

    def _eval(self, str_to_execute, globs={}, params=[]):
        """
        Java test runner.
        """
        self.epname = globs['EP']

        _RESULT = None

        ret_code = {
            0: 'PASS',
            1: 'FAIL',
            2: 'ERROR'
        }

        # init
        runner_cfg_parser = SafeConfigParser()

        try:
            runner_cfg_parser.read(os.path.join(TWISTER_PATH, 'config/runner.ini'))

            java_compiler_path = runner_cfg_parser.get('javarunner', 'JAVAC_PATH')
            junit_class_path = runner_cfg_parser.get('javarunner', 'JUNIT_PATH')
            jython_class_path = runner_cfg_parser.get('javarunner', 'JYTHON_PATH')

            copyfile(os.path.join(TWISTER_PATH,\
            'common/jython/jythonExternalVariableClass.jpy'),\
            '{0}/.twister_cache/{1}/ce_libs/jythonExternalVariableClass.py'.\
            format(TWISTER_PATH, self.epname))

            copyfile(os.path.join(TWISTER_PATH, 'common/jython/tscJython.jar'),\
            '{0}/.twister_cache/{1}/ce_libs/tscJython.jar'.\
            format(TWISTER_PATH, self.epname))
            tsc_jython_path = '{0}/.twister_cache/{1}/ce_libs/tscJython.jar'.\
            format(TWISTER_PATH, self.epname)
        except Exception as exp_err:
            print 'Error: Compiler path not found'
            print 'Error: {}'.format(exp_err)
            return None

        # create test
        file_name = os.path.split(globs['FILE_NAME'])[1]
        files_path = '{}/.twister_cache/{}'.format(TWISTER_PATH, self.epname)
        file_path = os.path.join(files_path, file_name)

        with open(file_path, 'wb') as fname:
            fname.write(str_to_execute)


        # Compile java test
        subprocess.Popen('{jc} -classpath "{cl0}:{cl1}:{cl2}" {fl}'.\
        format(jc=java_compiler_path, cl0=junit_class_path,\
        cl1=tsc_jython_path, cl2=jython_class_path, fl=file_path), shell=True)


        # Run test
        compiled_file_path = os.path.join(files_path, '{fn}.class'.format(fn=os.path.splitext(file_name)[0]))
        jython_runner = os.path.join(TWISTER_PATH, 'common/jython/jythonRunner.jpy')
        jython_proc = subprocess.Popen('jython {jp} --classFilePath {cf} \
        --testFilePath {fl}'.format(jp=jython_runner, cf=junit_class_path,\
        fl=compiled_file_path), shell=True)
        jython_proc.wait()

        if not jython_proc.returncode in ret_code:
            print 'Unknown return code'
            return None

        _RESULT = ret_code[jython_proc.returncode]

        # The _RESULT must be injected from within the jython script
        return _RESULT


    def __del__(self):
        """
        On exit, cleanup.
        """
        file_names = '{}/.twister_cache/{}/*.java*'.format(TWISTER_PATH, self.epname)
        for file_path in glob.glob(file_names):
            # print('Cleanup Java file:',' file_path)
            try:
                os.remove(file_path)
            except Exception:
                pass


# Eof()
