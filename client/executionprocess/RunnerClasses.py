
# File: TestCaseRunnerClasses.py ; This file is part of Twister.

# version: 3.002

# Copyright (C) 2012-2013 , Luxoft

# Authors:
#    Adrian Toader <adtoader@luxoft.com>
#    Andrei Costachi <acostachi@luxoft.com>
#    Andrei Toma <atoma@luxoft.com>
#    Cristi Constantin <crconstantin@luxoft.com>
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
REQUIRED Python 2.7.
This file contains classes that will run TCL/ Python/ Perl test cases.
This script CANNOT run separately, it must be called from TestCaseRunner.
'''

import os
import sys
import time
import glob
from shutil import copyfile

import subprocess # For running Perl
from collections import OrderedDict # For dumping TCL

from ConfigParser import SafeConfigParser

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print('TWISTER_PATH environment variable is not set! Exiting!')
    exit(1)

#

class TCRunTcl(object):

    def __init__(self):

        try:
            import Tkinter
        except Exception:
            print('*ERROR* Cannot import Python Tkinter! Exiting!')
            exit(1)

        try:
            tcl = Tkinter.Tcl()
        except Exception:
            print('*ERROR* Cannot create TCL console! Exiting!')
            exit(1)

        DEFAULT_INFO_VARS = ['_tkinter_skip_tk_init', 'argc', 'argv', 'argv0', 'auto_index', 'auto_oldpath',
            'auto_path', 'env', 'errorCode', 'errorInfo', 'tcl_interactive', 'tcl_libPath', 'tcl_library',
            'tcl_patchLevel', 'tcl_pkgPath', 'tcl_platform', 'tcl_rcFileName', 'tcl_version', 'exp_library',
            'expect_library', 'exp_exec_library']

        DEFAULT_INFO_PROCS = ['auto_execok', 'auto_import', 'auto_load', 'auto_load_index', 'auto_qualify',
            'clock', 'history', 'tclLog', 'unknown', 'pkg_mkIndex']

        self.epname = ''
        self.all_vars = 0
        self.all_vars_values = 0
        self.all_procs = 0
        self.all_procs_values = 0

        self.tcl = Tkinter.Tcl()

        if os.path.exists(os.getcwd()+'/__recomposed.tcl'):
            # Restore all variables and functions
            self.tcl.evalfile(os.getcwd()+'/__recomposed.tcl')

        # self.tcl.eval('package require Tcl')
        # self.tcl.eval('package require Expect')

    def __del__(self):
        #
        # On exit delete all recomposed and Tcl files
        del self.tcl
        open(os.getcwd()+'/__recomposed.tcl', 'w').close()
        try: os.remove('__recomposed.tcl')
        except Exception: pass
        global TWISTER_PATH
        fnames = '{}/.twister_cache/{}/*.tcl'.format(TWISTER_PATH, self.epname)
        for fname in glob.glob(fnames):
            # print 'Cleanup TCL file:', fname
            try: os.remove(fname)
            except Exception: pass
        #

    def _eval(self, str_to_execute, globs={}, params=[]):
        '''
        After executing a TCL statement, the last value will be used
        as return value.
        '''
        self.epname = globs['EP']

        # Inject variables
        self.tcl.setvar('USER',       globs['USER'])
        self.tcl.setvar('EP',         globs['EP'])
        self.tcl.setvar('SUT',        globs['SUT'])
        self.tcl.setvar('SUITE_ID',   globs['SUITE_ID'])
        self.tcl.setvar('SUITE_NAME', globs['SUITE_NAME'])
        self.tcl.setvar('FILE_ID',    globs['FILE_ID'])
        self.tcl.setvar('FILE_NAME',  globs['FILE_NAME'])
        self.tcl.setvar('CONFIG', ';'.join(globs['CONFIG']))

        # Inject common functions
        self.tcl.createcommand('logMessage',  globs['logMsg'])
        self.tcl.createcommand('getGlobal',   globs['getGlobal'])
        self.tcl.createcommand('setGlobal',   globs['setGlobal'])
        self.tcl.createcommand('py_exec',     globs['py_exec'])

        self.tcl.createcommand('getResource',    globs['getResource'])
        self.tcl.createcommand('setResource',    globs['setResource'])
        self.tcl.createcommand('renameResource', globs['renameResource'])
        self.tcl.createcommand('deleteResource', globs['deleteResource'])
        self.tcl.createcommand('getResourceStatus', globs['getResourceStatus'])
        self.tcl.createcommand('allocResource',     globs['allocResource'])
        self.tcl.createcommand('reserveResource',   globs['reserveResource'])
        self.tcl.createcommand('freeResource',      globs['freeResource'])

        to_execute = str_to_execute
        to_execute = '\nset argc %i\n' % len(params) + to_execute
        to_execute = 'set argv {%s}\n' % str(params)[1:-1] + to_execute

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
                    except Exception: pass
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

class TCRunPython(object):

    def _eval(self, str_to_execute, globs={}, params=[]):
        """
        Variable `_RESULT` must be injected inside the exec,
        or else the return will always be None.
        """
        self.epname = globs['EP']
        self.filename = os.path.split(globs['FILE_NAME'])[1]
        fpath = '{}/.twister_cache/{}/{}'.format(TWISTER_PATH, self.epname, self.filename)

        # Start injecting inside tests
        globs_copy = dict(globs)
        globs_copy['os']   = os
        globs_copy['sys']  = sys
        globs_copy['time'] = time

        to_execute = r"""
__file__ = '%s'
sys.argv = %s
""" % (fpath, str([self.filename] + params))

        f = open(fpath, 'wb')
        f.write(to_execute)
        f.write(str_to_execute)
        f.close() ; del f

        execfile(fpath, globs_copy)

        # The _RESULT must be injected from within the python script
        return globs_copy.get('_RESULT')
        #


    def __del__(self):
        #
        # On exit delete all Python files
        global TWISTER_PATH
        fnames = '{}/.twister_cache/{}/*.py*'.format(TWISTER_PATH, self.epname)
        for fname in glob.glob(fnames):
            # print 'Cleanup Python file:', fname
            try: os.remove(fname)
            except Exception: pass
        #

#

class TCRunPerl(object):
    """
    Perl test runner.
    """

    def _eval(self, str_to_execute, globs={}, params=[]):
        """
        Variable `_RESULT` must be injected inside the exec,
        or else the return will always be None.
        """
        self.epname = globs['EP']
        self.filename = os.path.split(globs['FILE_NAME'])[1]
        fdir  = '{}/.twister_cache/{}'.format(TWISTER_PATH, self.epname)
        fpath = fdir + os.sep + self.filename

        # String begins with #!/usr/bin/perl ?
        if  str_to_execute[0] == '#':
            str_to_execute = '\n'.join( str_to_execute.split('\n')[1:] )

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

"""

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

def logMsg(*arg, **kw):
    return commonLib.logMsg(*arg, **kw)

def getGlobal(*arg, **kw):
    return commonLib.getGlobal(*arg, **kw)

def setGlobal(*arg, **kw):
    return commonLib.setGlobal(*arg, **kw)

def getConfig(*arg, **kw):
    return commonLib.getConfig(*arg, **kw)

def getBinding(*arg, **kw):
    return commonLib.getBinding(*arg, **kw)

def getResource(*arg, **kw):
    return commonLib.getResource(*arg, **kw)

def setResource(*arg, **kw):
    return commonLib.setResource(*arg, **kw)

def getSut(*arg, **kw):
    return commonLib.getSut(*arg, **kw)

def setSut(*arg, **kw):
    return commonLib.setSut(*arg, **kw)

END_OF_PYTHON_CODE
"""  %  (fpath, str([self.filename] + params), TWISTER_PATH, fdir)

        f = open(fpath, 'wb')
        f.write(text_head)
        f.write(str_to_execute)
        f.write(text_tail)
        f.close() ; del f

        env = os.environ
        env.update({'TWISTER_PATH': TWISTER_PATH})

        print('~ Perl ~ Compiling Inline::Python ~\n')
        proc = subprocess.Popen('perl '+ fpath, env=env, shell=True, bufsize=1)
        ret = proc.communicate()
        time.sleep(0.5)

        try: os.remove(fpath)
        except Exception: pass

        # The _RESULT must be injected from within the perl script
        print('\n~ Perl returned code `{}` ~'.format(proc.returncode))
        return proc.returncode
        #

#

class TCRunJava(object):
    """
    Java Runner.
    """

    def _eval(self, str_to_execute, globs={}, params=[]):
        """ Java test runner """

        global TWISTER_PATH
        self.epname = globs['EP']

        _RESULT = None

        returnCode = {
            0: 'PASS',
            1: 'FAIL',
            2: 'ERROR'
        }

        # init
        runnerConfigParser = SafeConfigParser()

        try:
            runnerConfigParser.read(os.path.join(TWISTER_PATH, 'config/runner.ini'))

            javaCompilerPath = runnerConfigParser.get('javarunner', 'JAVAC_PATH')
            junitClassPath = runnerConfigParser.get('javarunner', 'JUNIT_PATH')
            jythonClassPath = runnerConfigParser.get('javarunner', 'JYTHON_PATH')

            copyfile(os.path.join(TWISTER_PATH, 'common/jython/jythonExternalVariableClass.jpy'),
                '{0}/.twister_cache/{1}/ce_libs/jythonExternalVariableClass.py'.format(
                                                                TWISTER_PATH, self.epname))
            copyfile(os.path.join(TWISTER_PATH, 'common/jython/tscJython.jar'),
                '{0}/.twister_cache/{1}/ce_libs/tscJython.jar'.format(TWISTER_PATH, self.epname))
            tscJythonPath = '{0}/.twister_cache/{1}/ce_libs/tscJython.jar'.format(
                                                                    TWISTER_PATH, self.epname)
        except Exception, e:
            print 'Error: Compiler path not found'
            print 'Error: {er}'.format(er=e)

            return _RESULT

        # create test
        fileName = os.path.split(globs['FILE_NAME'])[1]
        filesPath = '{}/.twister_cache/{}'.format(TWISTER_PATH, self.epname)
        filePath = os.path.join(filesPath, fileName)

        with open(filePath, 'wb+') as f:
            f.write(str_to_execute)


        # compile java test
        #command = [javaCompilerPath, '-classpath', junitClassPath, testFile]
        javacProcess = subprocess.Popen('{jc} -classpath "{cl0}:{cl1}:{cl2}" {fl}'.format(
                        jc=javaCompilerPath, cl0=junitClassPath, cl1=tscJythonPath,
                        cl2=jythonClassPath, fl=filePath), shell=True)


        # run test
        compiledFilePath = os.path.join(filesPath,
                            '{fn}.class'.format(fn=os.path.splitext(fileName)[0]))
        jythonRunner = os.path.join(TWISTER_PATH, 'common/jython/jythonRunner.jpy')
        #command = [jythonRunner, '--testFilePath', testFile]
        jythonProcess = subprocess.Popen('jython {jp} --classFilePath {cf} '\
            '--testFilePath {fl}'.format(jp=jythonRunner,
            cf=junitClassPath, fl=compiledFilePath), shell=True)
        jythonProcess.wait()
        if not jythonProcess.returncode in returnCode:
            print 'unknown return code'

            return _RESULT

        _RESULT = returnCode[jythonProcess.returncode]

        # The _RESULT must be injected from within the jython script
        return _RESULT


    def __del__(self):
        """ cleanup """

        global TWISTER_PATH

        # On exit delete all Java files
        fileNames = '{}/.twister_cache/{}/*.java*'.format(TWISTER_PATH, self.epname)
        for filePath in glob.glob(fileNames):
            # print 'Cleanup Java file: filePath
            try:
                os.remove(filePath)
            except Exception:
                pass

# Eof()
