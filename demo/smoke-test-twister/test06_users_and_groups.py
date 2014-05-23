
#
# <ver>version: 2.004</ver>
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

#

def test(PROXY, USER):

    pprint( PROXY.usrManager('list params'), indent=2, width=100 )
    print('---')

    users = PROXY.usrManager('list users')
    pprint( users, indent=2, width=100 )
    print('---')

    groups = PROXY.usrManager('list groups')
    pprint( groups, indent=2, width=100 )
    print('---')

    roles = PROXY.usrManager('list roles')
    pprint( roles, indent=2, width=100 )
    print('---')

    time.sleep(0.5)

    tmp_groups = random.sample(groups.keys(), 2)
    r = PROXY.usrManager('set user', 'test1', ','.join(tmp_groups))
    if not r: return 'Fail'
    print('Created user `test1` with groups `{}`.'.format(tmp_groups))

    r = PROXY.usrManager('delete user', 'test1')
    if not r: return 'Fail'
    print('Deleted user `test1`.\n')

    time.sleep(0.5)

    tmp_groups = random.sample(groups.keys(), 2)
    r = PROXY.usrManager('set user', 'test2', ','.join(tmp_groups))
    if not r: return 'Fail'
    print('Created user `test2` with groups `{}`.'.format(tmp_groups))

    r = PROXY.usrManager('delete user', 'test2')
    if not r: return 'Fail'
    print('Deleted user `test2`.\n')

    time.sleep(0.5)

    tmp_roles = random.sample(roles, 2)
    r = PROXY.usrManager('set group', 'test1', ','.join(tmp_roles))
    if not r: return 'Fail'
    print('Created group `test1` with roles `{}`.'.format(tmp_roles))

    r = PROXY.usrManager('delete group', 'test1')
    if not r: return 'Fail'
    print('Deleted group `test1`.\n')

    time.sleep(0.5)

    tmp_roles = random.sample(roles, 2)
    r = PROXY.usrManager('set group', 'test2', ','.join(tmp_roles))
    if not r: return 'Fail'
    print('Created group `test2` with roles `{}`.'.format(tmp_roles))

    r = PROXY.usrManager('delete group', 'test2')
    if not r: return 'Fail'
    print('Deleted group `test2`.\n')

    print('Testing Central Engine encrypt / decrypt...\n')
    for i in range(10):
        d = binascii.hexlify(os.urandom(4))
        r1 = PROXY.encryptText(d)
        print('Encrypt:\n{} -> {}'.format(d, r1))
        r2 = PROXY.decryptText(r1)
        if r2 != d:
            print('Invalid decrypt!')
            return 'Fail'
        else:
            print('Decrypt:\n{} -> {}\n'.format(r1, r2))

    return 'Pass'

# Must have one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout'
_RESULT = test(PROXY, USER)

# Eof()
