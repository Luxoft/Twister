
#
# <title>test 01</title>
# <description>This suite checks a lot of things.
# It checks if the EPs are running the tests successfully and it calls all CE functions, to ensure they work as expected.
# This file is checking if the suite runs from Twister.</description>
#

# `proxy` and `username` are variables from the Runner.

_RESULT = 'Pass'

try:
    print('Central engine connection: %s', proxy)
except:
    print('This test should run from Twister!\n')
    _RESULT = 'Fail'

try:
    print(proxy.echo('Hello Central Engine! I am a user `%s`!\n' % userName))
except:
    print('This test should run from Twister!\n')
    _RESULT = 'Fail'

print('Connection test finished.')

# Eof()
