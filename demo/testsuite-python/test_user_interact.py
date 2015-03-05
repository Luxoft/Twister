
#
# version: 1.000
# <title>test_user_interact file</title>
# <description>...</description>
# <tags>tag1!tag2, tag3@tag4; **&&$$</tags>
# <meta1><Dudu><Testing inside></test></meta1>
# <meta2>###
# ###</meta2>
#

# `USER`, `EP`, `SUITE_NAME` and `FILE_NAME` are magic variables,
# injected inside all Twister tests.


import time

print 'I am test_user_interact file.'

# interact(`interact type`, `message`, `timeout in seconds as integer`, `options, only for options interact type`)
# TscCommonLib library must be set
interact('msg', 'This is first message! {}'.format(EP), 10)
time.sleep(3)

interact('input', 'This is first input!', 8)
time.sleep(3)

interact('decide', 'Please decide first!', 8)
time.sleep(3)

options = {'options':[1,2,3,4,5], 'default':5}
interact('options', 'Select the option1!', 20, options)

_RESULT = 'PASS'

#
