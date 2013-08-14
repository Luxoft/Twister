
#
# version: 2.002
# <title>Users and Groups</title>
# <description>List users, groups, roles. To run this test, your user must be a twister ADMIN!</description>
#

import os
import time
import random
import binascii
from pprint import pprint

#

def test(PROXY, USER):

    pprint( PROXY.usersAndGroupsManager('list params'), indent=2, width=100 )
    print('---')

    users = PROXY.usersAndGroupsManager('list users')
    pprint( users, indent=2, width=100 )
    print('---')

    groups = PROXY.usersAndGroupsManager('list groups')
    pprint( groups, indent=2, width=100 )
    print('---')

    roles = PROXY.usersAndGroupsManager('list roles')
    pprint( roles, indent=2, width=100 )
    print('---')

    time.sleep(0.5)

    tmp_groups = random.sample(groups.keys(), 2)
    r = PROXY.usersAndGroupsManager('set user', 'test1', ','.join(tmp_groups))
    if not r: return 'Fail'
    print('Created user `test1` with groups `{}`.'.format(tmp_groups))

    r = PROXY.usersAndGroupsManager('delete user', 'test1')
    if not r: return 'Fail'
    print('Deleted user `test1`.\n')

    time.sleep(0.5)

    tmp_groups = random.sample(groups.keys(), 2)
    r = PROXY.usersAndGroupsManager('set user', 'test2', ','.join(tmp_groups))
    if not r: return 'Fail'
    print('Created user `test2` with groups `{}`.'.format(tmp_groups))

    r = PROXY.usersAndGroupsManager('delete user', 'test2')
    if not r: return 'Fail'
    print('Deleted user `test2`.\n')

    time.sleep(0.5)

    tmp_roles = random.sample(roles, 2)
    r = PROXY.usersAndGroupsManager('set group', 'test1', ','.join(tmp_roles))
    if not r: return 'Fail'
    print('Created group `test1` with roles `{}`.'.format(tmp_roles))

    r = PROXY.usersAndGroupsManager('delete group', 'test1')
    if not r: return 'Fail'
    print('Deleted group `test1`.\n')

    time.sleep(0.5)

    tmp_roles = random.sample(roles, 2)
    r = PROXY.usersAndGroupsManager('set group', 'test2', ','.join(tmp_roles))
    if not r: return 'Fail'
    print('Created group `test2` with roles `{}`.'.format(tmp_roles))

    r = PROXY.usersAndGroupsManager('delete group', 'test2')
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
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout', 'invalid'
_RESULT = test(PROXY, USER)

# Eof()
