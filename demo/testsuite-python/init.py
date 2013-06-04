
#
# version: 2.002
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
print 'Remote file:', FILE_NAME
print 'Local file:', __file__

_RESULT = 'PASS'

#
