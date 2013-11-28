
#
# <ver>version: 3.001</ver>
# <title>Test libraries</title>
# <description>This suite checks the most basic functionality of Twister.<br>
# </description>
#

from ce_libs import *
from TscCommonLib import *

# ----- Image that this is a library you derive from Common Lib :) ----------- #

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

def test():

    logMsg('logRunning', '\nStarting lib test...\n')

    d = Derived04()

    print

    assert isinstance(d, TscCommonLib), 'Invalid derivation from Common Lib!'
    print 'Instance from Common Lib?', isinstance(d, TscCommonLib)

    assert d.ra_proxy1 == PROXY, 'Central Engine connection does not match!'
    print d.ra_proxy1, '==', PROXY, d.ra_proxy1 == PROXY

    assert d.ra_proxy2 == PROXY, 'Central Engine connection does not match!'
    print d.ra_proxy2, '==', PROXY, d.ra_proxy2 == PROXY

    print

    setGlobal('test', 'testxxx')
    assert getGlobal('test') == 'testxxx', 'Error on get + set globals!'
    print 'Get + Set global ok.', getGlobal('test'), '==', 'testxxx'

    assert getGlobal('test') == d.getGlobal('test'), 'Error on get + set globals derivation!'
    print 'Get + Set global derivation ok.', getGlobal('test'), '==', d.getGlobal('test')

    print

    print 'Files in the project:', d.countProjectFiles()
    print 'File index in the project:', d.currentFileIndex()
    print 'Files in This suite:', d.countSuiteFiles()
    print 'File index in the suite:', d.currentFSuiteIndex()

    logMsg('logRunning', 'Finished lib test. Everything OK.\n')

    return 'Pass'

# ---------------------------------------------------------------------------- #

# Must have one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout'
_RESULT = test()

# Eof()
