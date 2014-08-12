
#
# <ver>version: 3.001</ver>
# <title>Test Connect</title>
# <description>This suite checks the most basic functionality of Twister.<br>
# It checks if the EPs are running the tests successfully and it calls all CE functions, to ensure they work as expected.</description>
# <test>connect</test>
# <smoke>yes</smoke>
#

# `PROXY`, `USER`, `SUITE_NAME` and `FILE_NAME` are magic variables, injected by Twister.

# Must have one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout'
_RESULT = 'Pass'

try:
    print('Central engine connection: {}'.format( str(PROXY) ))
except:
    _REASON = 'This test should run from Twister! No CE connection!'
    print(_REASON)
    _RESULT = 'Fail'

try:
    print(PROXY.echo('Hello Central Engine! I am the user `{}`!\n'.format(USER)))
    print('This is suite `{}` and test `{}`.\n'.format(SUITE_NAME, FILE_NAME))
except:
    _REASON = 'This test should run from Twister! Cannot send echo!'
    print(_REASON)
    _RESULT = 'Fail'

print('Connection test finished.')

# Eof()
