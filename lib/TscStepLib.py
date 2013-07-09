
# File: TscStepLib.py ; This file is part of Twister.

# version: 2.002

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
"Step" is used to create steps inside tests.
The idea is to organize one test into smaller steps, that will be executed in order.
Before each step, you can call other functions, to setup something before execution.
After the step runs, all the CLI log is searched using regular expressions
and if any of the expressions is found, the matching functions are called.

For example:
You have a permanent connection, called `conn1`.
You need to test some commands on this connection.
The step function has 3 parameters: a function that will be tested, pre hooks and post hooks.

Pre-hooks are 1 or more simple functions that prepare the connection. They are optional.
Post-hooks are 1 or more pairs of strings + functions. They are also optional.
If one of the strings is found inside the CLI resulted from executed the main function,
the hook is executed. All the matches are executed, in order.


def test_feature1():
    """ This is a big feature. """
    conn1.send('some command you need to test')

def test_feature2(param1, param2):
    """ This is another big feature. """
    conn1.send('some command you need to test')

def prepare_connection1():
    # do something, before sending command 1

def prepare_connection2():
    # do something, before sending command 2

def in_case_of_fail():
    # do something if the connection failed

def in_case_of_crash():
    # treat this...

def in_case_of_success():
    # Enjoy the success


STEP(
    test_feature1,
    prepare_connection1,
    [
        ('general failure', in_case_of_fail),
        ('CORE DUMP', in_case_of_crash),
        ('done', in_case_of_success)
    ]
)

STEP(
    [test_feature1, 'value1', 'value2'],
    [
        prepare_connection1,
        prepare_connection2
    ],
    [
        ('general failure', in_case_of_fail),
        ('CORE DUMP', in_case_of_crash),
        ('done', in_case_of_success)
    ]
)

'''

import os
import sys
import re
from cStringIO import StringIO

_step_nr = 0

#

def exec_pre_hooks(hooks):
    # For 1 hook, without params
    if callable(hooks):
        try:
            hooks()
        except Exception, e:
            print('Pre-Hook `{}` crashed! error: `{}`!'.format(hook, e))
            return False
        return True

    # For more hooks, with or withoud params...
    for hook in hooks:
        if callable(hook):
            try:
                hook()
            except Exception, e:
                print('Pre-Hook `{}` crashed! error: `{}`!'.format(hook, e))
                continue
        elif (isinstance(hook, list) or isinstance(hook, tuple)):
            hfunc = hook[0]
            hpara = hook[1:]
            try:
                hfunc(*hpara)
            except Exception, e:
                print('Pre-Hook `{}` crashed! error: `{}`!'.format(hfunc, e))
                continue
        else:
            print('Invalid Pre-Hook `{}`! Cannot execute!'.format(hook))
            continue

    return True

#

def exec_post_hooks(hooks, cli):
    # For 1 hook
    try:
        if len(hooks)==2 and callable(hooks[1]):
            hstrg = hooks[0]
            if hstrg and (not hstrg in cli):
                return True
            hfunc = hooks[1]
            hpara = hooks[2:]
            try:
                hfunc(*hpara)
            except Exception, e:
                print('Post-Hook `{}` crashed! error: `{}`!'.format(hfunc, e))
                return False
            return True
    except:
        pass

    # For a list of hooks ...
    for hook in hooks:
        if (isinstance(hook, list) or isinstance(hook, tuple)):
            hstrg = hook[0]
            if hstrg and (not hstrg in cli):
                continue
            hfunc = hook[1]
            hpara = hook[2:]
            try:
                hfunc(*hpara)
            except Exception, e:
                print('Post-Hook `{}` crashed! error: `{}`!'.format(hfunc, e))
                continue
        else:
            print('Invalid Post-Hook `{}`! Cannot execute!'.format(hook))
            continue

    return True

#

def STEP(function, pre_hooks=None, post_hooks=None):
    global _step_nr
    _step_nr += 1

    stdout = StringIO()
    stderr = StringIO()

    # Line...
    if _step_nr != 1: print
    print(('~'*30 + ' Step nr {} ' + '~'*30).format(_step_nr))

    if not (callable(function) or (isinstance(function, list) or isinstance(function, tuple))):
        print('Invalid Step function `{}`! Cannot execute!'.format(function))
        print('~'*71) # Ending line...
        return False

    # Print function documentation, as description
    if callable(function):
        if function.__doc__:
            print(function.__doc__)
            print('-'*71)
    # If the function has parameters...
    elif (isinstance(function, list) or isinstance(function, tuple)):
        if function[0].__doc__:
            print(function[0].__doc__)
            print('-'*71)

    # Execute pre functions
    if pre_hooks:
        # print('Pre hooks: `{}`.'.format(pre_hooks))
        exec_pre_hooks(pre_hooks)
        print

    # Redirect stdout and stderr
    old_o = sys.stdout
    old_e = sys.stderr
    sys.stdout = stdout
    sys.stderr = stderr
    e = None

    if callable(function):
        try:
            function()
        except Exception, e:
            pass
    elif (isinstance(function, list) or isinstance(function, tuple)):
        try:
            function[0](*function[1:])
        except Exception, e:
            pass

    # Restore stdout and stderr
    sys.stdout = old_o
    sys.stderr = old_e

    cli = stdout.getvalue() + stderr.getvalue()
    print(cli.strip())

    # Print the exceptions, if any and exit
    if e:
        print('Function `{}` crashed! error: `{}`!'.format(function, e))
        print('~'*71) # Ending line...
        return False # If the function crashed, the post-hooks are useless

    # Execute post functions
    if post_hooks:
        # print('\nPost hooks: `{}`.'.format(post_hooks))
        exec_post_hooks(post_hooks, cli)

    print('~'*71) # Ending line...
    return True

# Eof()
