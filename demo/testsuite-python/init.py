
#
# version: 2.001
# <title>init file</title>
# <description>...</description>
#

# `USER`, `EP`, `SUITE_NAME` and `FILE_NAME` are magic variables,
# injected inside all Twister tests.

import os
import sys
import time

print 'I am init file.'
print 'I am not doing anything special, just printing some variables.'

print 'Hello, user', USER, '!'
print 'Test Bed:', currentTB
print 'Exec process:', EP
print 'Suite:', SUITE_NAME
print 'File:', FILE_NAME

_RESULT = 'PASS'

#
