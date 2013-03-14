
#
# <title>Testing Globals</title>
# <description>This test is getting some complex functions and classes.</description>
#

func1 = getGlobal('func1')
func2 = getGlobal('func2')
Class1 = getGlobal('Class1')
Class2 = getGlobal('Class2')
Class1i = getGlobal('Class1i')
Class2i = getGlobal('Class1i')

print '*** All functions and classes are pointers, defined in the previous test!!!'

print 'Calling function 1'
func1()
print '---'

print 'Calling function 1'
func2()
print '---'

print 'Calling class 1'
print Class1()
print '---'

print 'Calling class 2'
print Class2()
print '---'

print 'Checking instance 1'
print Class1i
print '---'

print 'Checking instance 2'
print Class2i
print '---'

# Must have one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout', 'invalid'
_RESULT = 'pass'
