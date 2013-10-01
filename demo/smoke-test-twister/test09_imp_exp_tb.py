
#
# <ver>version: 2.002</ver>
# <title>Test Import/ Export XML</title>
# <description>This suite checks the most basic functionality of Twister.<br>
# This test tries to export the TB as XML, then import it again to see if the data is the same.</description>
#

import os
import time
import xmlrpclib
from binascii import hexlify

#

def cleanup(file):
    try: os.remove(file)
    except: 'Cannot cleanup file `{}`!'.format(file)


def check(ra, _xml_file):

    try:
        res = ra.getResource('/')
        sut = ra.getSut('/')
        try: del res['version']
        except: pass
        try: del res['name']
        except: pass
        print('Resource Allocator connection OK.\n')
    except:
        print('Cannot connect to Resource Allocator server!')
        return False

    r = ra.export_xml(_xml_file)
    if not r:
        print('Cannot export resources into XML!')
        cleanup(_xml_file)
        return False
    else:
        print('Resources exported with success in `{}`.'.format(_xml_file))

    time.sleep(0.5)

    r = ra.import_xml(_xml_file)
    if not r:
        print('Cannot import resources into XML!')
        cleanup(_xml_file)
        return False
    else:
        print('Resources imported with success in the Testbed!')

    time.sleep(0.5)

    print('Comparing the old resource, with the new resource...')
    # New resources must be the same as the old resources!
    new_res = ra.getResource('/')
    try: del new_res['version']
    except: pass
    try: del new_res['name']
    except: pass

    print('{} children [vs] {} children.'.format( len(res['children']), len(new_res['children']) ))

    logMsg('logDebug', '\n- Old resource :\n')
    logMsg('logDebug', repr(res))
    logMsg('logDebug', '\n----------\n')

    logMsg('logDebug', '\n- New resource :\n')
    logMsg('logDebug', repr(new_res))
    logMsg('logDebug', '\n----------\n')

    if res != new_res:
        print('Check failed! The resources are different after import/ export!')
        return False

    print('-' * 60 + '\n')

    return True


def test(PROXY, USER):

    logMsg('logRunning', 'Starting import...\n')

    _proxy = 'http://{}/ra/'.format(PROXY._ServerProxy__host)
    ra = xmlrpclib.ServerProxy(_proxy)

    _curr_dir = os.getcwd()
    _xml_file = _curr_dir + '/textbed.xml'

    # -----
    # Check at the beggining

    r = check(ra, _xml_file)
    if not r:
        return 'Fail'

    py_res = 'tb_' + hexlify(os.urandom(4))
    print('Create TB `{}`...'.format(py_res))
    res_id = setResource(py_res, '/', {'meta1': 1, 'meta2': 2, 'meta3': ''})
    print('Ok.\n')

    # -----
    # Check after creating a new element

    r = check(ra, _xml_file)
    if not r:
        return 'Fail'

    print('Delete TB :', deleteResource(res_id))

    # -----
    # Check after the delete of the element

    r = check(ra, _xml_file)
    if not r:
        return 'Fail'

    logMsg('logRunning', 'Finished import/ export.\n')

    cleanup(_xml_file)
    return 'Pass'

#

# Must have one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout'
_RESULT = test(PROXY, USER)

# Eof()
