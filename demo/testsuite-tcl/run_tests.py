
# Check prerequisites, then run tests!

try:
    import Tkinter
except:
    print('*ERROR* Cannot import Python Tkinter! Exiting!')
    exit(1)

try:
    tcl = Tkinter.Tcl()
except:
    print('*ERROR* Cannot create TCL console! Exiting!')
    exit(1)

try:
    tcl.eval('package require Expect')
except:
    print('*ERROR* Cannot import Expect! Exiting!')
    exit(1)

#

import os
__file__ = os.path.abspath(__file__)
DIR = os.path.split(__file__)[0]

#

print 'Prerequisites OK... Preparing Python!'

tcl.eval('source {%s}' % (DIR + os.sep + 'init.tcl'))
tcl.eval('source {%s}' % (DIR + os.sep + 'setup.tcl'))

r = tcl.eval('source {%s}' % (DIR + os.sep + 'test001.tcl'))
print '>>> Py return code:', r

r = tcl.eval('source {%s}' % (DIR + os.sep + 'test002.tcl'))
print '>>> Py return code:', r

r = tcl.eval('source {%s}' % (DIR + os.sep + 'test003.tcl'))
print '>>> Py return code:', r

r = tcl.eval('source {%s}' % (DIR + os.sep + 'test004.tcl'))
print '>>> Py return code:', r

print 'Done from PYTHON!'
