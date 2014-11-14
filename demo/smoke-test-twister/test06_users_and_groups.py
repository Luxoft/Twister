
#
# <ver>version: 3.002</ver>
# <title>Test Users, Groups, Roles</title>
# <description>This suite checks the most basic functionality of Twister.<br>
# It checks if the EPs are running the tests successfully and it calls all CE functions, to ensure they work as expected.</description>
# <test>users & groups</test>
# <smoke>yes</smoke>
#

import os
import time
import random
import binascii
from pprint import pprint

# ---------------------------------------------------------------------------- #

# Default test result will be PASS
# Any CRASH, or failed assert, will automatically FAIL the test

_RESULT = 'pass'

pprint( PROXY.usr_manager('list params'), indent=2, width=100 )
print('---')

users = PROXY.usr_manager('list users')
pprint( users, indent=2, width=100 )
print('---')

groups = PROXY.usr_manager('list groups')
pprint( groups, indent=2, width=100 )
print('---')

roles = PROXY.usr_manager('list roles')
pprint( roles, indent=2, width=100 )
print('---')

time.sleep(0.5)

tmp_groups = random.sample(groups.keys(), 2)
r = PROXY.usr_manager('set user', 'test1', ','.join(tmp_groups))
if not r:
    test_fail('cannot set user `test1` !')
print('Created user `test1` with groups `{}`.'.format(tmp_groups))

r = PROXY.usr_manager('delete user', 'test1')
if not r:
    test_fail('cannot delete user `test1` !')
print('Deleted user `test1`.\n')

time.sleep(0.5)

tmp_groups = random.sample(groups.keys(), 2)
r = PROXY.usr_manager('set user', 'test2', ','.join(tmp_groups))
if not r:
    test_fail('cannot set user `test2` !')
print('Created user `test2` with groups `{}`.'.format(tmp_groups))

r = PROXY.usr_manager('delete user', 'test2')
if not r:
    test_fail('cannot delete user `test2` !')
print('Deleted user `test2`.\n')

time.sleep(0.5)

tmp_roles = random.sample(roles, 2)
r = PROXY.usr_manager('set group', 'test1', ','.join(tmp_roles))
if not r:
    test_fail('cannot set group `test1` !')
print('Created group `test1` with roles `{}`.'.format(tmp_roles))

r = PROXY.usr_manager('delete group', 'test1')
if not r:
    test_fail('cannot delete group `test1` !')
print('Deleted group `test1`.\n')

time.sleep(0.5)

tmp_roles = random.sample(roles, 2)
r = PROXY.usr_manager('set group', 'test2', ','.join(tmp_roles))
if not r:
    test_fail('cannot set group `test2` !')
print('Created group `test2` with roles `{}`.'.format(tmp_roles))

r = PROXY.usr_manager('delete group', 'test2')
if not r:
    test_fail('cannot delete group `test2` !')
print('Deleted group `test2`.\n')


print('Testing Central Engine encrypt / decrypt...\n')

for i in range(10):
    d = binascii.hexlify(os.urandom(4))
    r1 = PROXY.encrypt_text(d)
    print('Encrypt:\n{} -> {}'.format(d, r1))
    r2 = PROXY.decrypt_text(r1)
    assert r2 == d, 'Invalid decrypt!'
    print('Decrypt:\n{} -> {}\n'.format(r1, r2))

# ---------------------------------------------------------------------------- #
