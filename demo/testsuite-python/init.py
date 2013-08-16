
#
# version: 2.003
# <title>init file</title>
# <description>...</description>
# <tags>tag1!tag2, tag3@tag4; **&&$$</tags>
# <meta1><Dudu><Testing inside></test></meta1>
# <meta2>###
# ###</meta2>
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
