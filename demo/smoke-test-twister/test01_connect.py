
#
# <ver>version: 2.004</ver>
# <title>Test Connect</title>
# <description>This suite checks the most basic functionality of Twister.<br>
# It checks if the EPs are running the tests successfully and it calls all CE functions, to ensure they work as expected.</description>
#

# `PROXY`, `USER`, `SUITE_NAME` and `FILE_NAME` are magic variables, injected by Twister.

# Must have one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout', 'invalid'
_RESULT = 'Invalid'

try:
    print('Central engine connection: {}'.format( str(PROXY) ))
except:
    print('This test should run from Twister!\n')
    _RESULT = 'Pass'

try:
    print(PROXY.echo('Hello Central Engine! I am the user `{}`!\n'.format(USER)))
    print('This is suite `{}` and test `{}`.\n'.format(SUITE_NAME, FILE_NAME))
except:
    print('This test should run from Twister!\n')
    _RESULT = 'Fail'

print('Connection test finished.')

# Eof()
