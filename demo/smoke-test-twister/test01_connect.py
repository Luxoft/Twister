
#
# <title>test 01</title>
# <description>This suite checks a lot of things.
# It checks if the EPs are running the tests successfully and it calls all CE functions, to ensure they work as expected.
# This file is checking if the suite runs from Twister.</description>
#

# `PROXY`, `USER`, `SUITE_NAME` and `FILE_NAME` are magic variables, from the Runner.

_RESULT = 'Pass'

try:
    print('Central engine connection: %s', PROXY)
except:
    print('This test should run from Twister!\n')
    _RESULT = 'Fail'

try:
    print(PROXY.echo('Hello Central Engine! I am a user `%s`!\n' % USER))
    print('This is suite `%s` and test `%s`.\n' % (SUITE_NAME, FILE_NAME))
except:
    print('This test should run from Twister!\n')
    _RESULT = 'Fail'

print('Connection test finished.')

# Eof()
