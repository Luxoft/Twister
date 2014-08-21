
#
# <ver>version: 3.003</ver>
# <title>Test libraries</title>
# <description>This suite checks the most basic functionality of Twister.<br>
# </description>
# <tags>libs, userlibs</tags>
# <test>lib</test>
# <smoke>yes</smoke>
#

sid = SUITE_ID
fid = FILE_ID

# Import * overwrites everything !!
from ce_libs import *
from TscCommonLib import *

# ----- Imagine this is a library you derive from Common Lib :) -------------- #

class Derived01(TscCommonLib):

    def __init__(self):
        # TscCommonLib.__init__(self)
        print('-- Derived01 ! --')
        # Derive the CE connection
        self.ra_proxy1 = self.ce_proxy


class Derived02(Derived01):

    def __init__(self):
        Derived01.__init__(self)
        print('-- Derived02 ! --')

    @property
    def ra_proxy2(self):
        # Derive the CE connection
        return self.ce_proxy


class Derived03(Derived02):

    def __init__(self):
        Derived02.__init__(self)
        print('-- Derived03 ! --')


class Derived04(Derived03):

    def __init__(self):
        Derived03.__init__(self)
        print('-- Derived04 ! --')

# ---------------------------------------------------------------------------- #

# Default test result will be PASS
# Any CRASH, or failed assert, will automatically FAIL the test

_RESULT = 'pass'


log_msg('logRunning', '\nStarting lib test...\n')

d = Derived04()

print

assert sid == d.SUITE_ID, 'Invalid suite id `{}` vs `{}`!'.format(d.SUITE_ID, sid)
print 'Suite ID matches:', sid

assert fid == d.FILE_ID, 'Invalid file id `{}` vs `{}`!'.format(d.FILE_ID, fid)
print 'Suite ID matches:', fid

print
print 'Instance from Common Lib?', isinstance(d, TscCommonLib)
assert isinstance(d, TscCommonLib), 'Invalid derivation from Common Lib!'

print
set_global('test', 'testxxx')
assert get_global('test') == 'testxxx', 'Error on get + set globals!'
print 'Get + Set global ok.', get_global('test'), '==', 'testxxx'

print
assert get_global('test') == d.get_global('test'), 'Error on get + set globals derivation!'
print 'Get + Set global derivation ok.', get_global('test'), '==', d.get_global('test')

print
print 'Files in the project:', count_project_files()
print 'File index in the project:', current_file_index()
print 'Files in This suite:', count_suite_files()
print 'File index in the suite:', current_fsuite_index()

print
print d.ra_proxy1, '==', PROXY, d.ra_proxy1 == PROXY
assert d.ra_proxy1 == PROXY, 'Central Engine connection does not match!'

print
print d.ra_proxy2, '==', PROXY, d.ra_proxy2 == PROXY
assert d.ra_proxy2 == PROXY, 'Central Engine connection does not match!'

log_msg('logRunning', 'Finished lib test. Everything OK.\n')

# ---------------------------------------------------------------------------- #
