
# version: 2.001

import os
from random import randint
from binascii import hexlify

"""
<title>Testing Globals</title>
<description>This test is checking the globals.
The global variable `global1` will be updated several times to see if it's working!</description>
"""

# Print all root level parameters
print 'Root level params:', getGlobal('/').keys()

# Print some parameters
print 'All params for Level_1:', getGlobal('Level_1')
print 'All params for Level_1/Level_2:', getGlobal('Level_1/Level_2'), '\n'

# Print Level-1 / global1 param
global1 = getGlobal('Level_1/global1')
print 'First level global #1:', global1, '\n'

# Run this 10 times
for i in range(10):
	# Generate a random number, between 2 and 20
	random_nr = randint(2, 20)
	# Generate a random string, of random length
	new_value = "value_{0}_{1}".format( random_nr, hexlify(os.urandom(random_nr)) )

	print 'Will set new value to::', new_value
	# Set the value of Level-1 / global1, with the random string
	# This will make the test to show all kinds of values,
	# Everytime it is run
	setGlobal('Level_1/global1', new_value)

	# Value is changed in this test and tests that follow
	print 'Check value changed::', getGlobal('Level_1/global1')

#

# Must have one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout', 'invalid'
_RESULT = 'pass'
