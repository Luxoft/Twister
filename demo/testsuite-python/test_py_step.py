
# version: 2.001

import os
from TscStepLib import STEP

"""
<title>Testing Step Library</title>
<description>This test is checking the Step.</description>
"""

def func1():
    print 'Hello world.'

def func2():
    """Testing main function crash."""
    print 'This function will crash!'
    print x

def func3(device=None, command=None):
    """Testing function with optional parameters."""
    print 'Testing params :', device, command

#

def func4(device, command):
    """Testing some function with mandatory parameters."""
    print 'Executing command `{}` on device `{}`...'.format(command, device)

def pre1(*k, **v):
    print 'I am pre hook 1!'
    print 'My params are:', k, v

def post1(x=''):
    print 'I am post hook 1! {}'.format(x)

#

# Simple step
STEP(func1)

# Crash, with description
STEP(func2)

# Simple function with description and 1 pre + 1 post
STEP(
    func3,
    pre1,
    ('*', post1) # This hook will not match
)

# Simple function, with 1 pre and 1 post
STEP(
    func3,
    pre1,
    ('Testing', post1) # This hook will match
)

# Function with params, multiple pre and multiple post
# The post hooks will NOT match
STEP(
    [func4, 'some_device', 'some_command'],
    pre_hooks = [
        pre1,
        (pre1, 'param1', 'param2')
    ],
    post_hooks = [
        ('xxx', post1),
        ('yyy', post1, '1'),
        ('zzz', post1, 'other parameter'),
    ]
)

# Function with params, multiple pre and multiple post
# All post hooks will match
STEP(
    [func4, 'other_device', 'other_command'],
    pre_hooks = [
        pre1,
        (pre1, 'param1', 'param2')
    ],
    post_hooks = [
        ('Executing', post1),
        ('command', post1, '1'),
        ('device', post1, 'other parameter'),
    ]
)

#

# Must have one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout'
_RESULT = 'pass'
