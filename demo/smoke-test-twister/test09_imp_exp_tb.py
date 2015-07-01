
#
# <ver>version: 2.002</ver>
# <title>Test Import/ Export XML</title>
# <description>This suite checks the most basic functionality of Twister.<br>
# This test tries to export the TB as XML, then import it again to see if the data is the same.</description>
# <tags>testbed, SUT, import, export</tags>
# <test>import & export</test>
# <smoke>yes</smoke>
#

import os
import time
import xmlrpclib
from binascii import hexlify

#

def cleanup(file):
    try: os.remove(file)
    except: 'Cannot cleanup file `{}`!'.format(file)


def check(ra_tb, ra_sut, _xml_file):

    try:
        res = ra_tb.get_tb('/')
        sut = ra_sut.get_sut('/')
        try: del res['version']
        except: pass
        try: del res['name']
        except: pass
        print('Resource Allocator connection OK.\n')
    except:
        print('Cannot connect to Resource Allocator server!')
        return False

    r = ra_tb.export_tb_xml(_xml_file)
    if not r:
        print('Cannot export resources into XML!')
        cleanup(_xml_file)
        return False
    else:
        print('Resources exported with success in `{}`.'.format(_xml_file))

    time.sleep(0.5)

    r = ra_tb.import_tb_xml(_xml_file)
    if not r:
        print('Cannot import resources into XML!')
        cleanup(_xml_file)
        return False
    else:
        print('Resources imported with success in the Testbed!')

    time.sleep(0.5)

    print('Comparing the old resource, with the new resource...')
    # New resources must be the same as the old resources!
    new_res = ra_tb.get_tb('/')
    try: del new_res['version']
    except: pass
    try: del res['meta']
    except: pass
    try: del new_res['meta']
    except: pass
    try: del res['name']
    except: pass
    try: del new_res['name']
    except: pass

    print('{} children [vs] {} children.'.format( len(res['children']), len(new_res['children']) ))

    log_msg('logDebug', '\n- Old resource :\n')
    log_msg('logDebug', repr(res))
    log_msg('logDebug', '\n----------\n')

    log_msg('logDebug', '\n- New resource :\n')
    log_msg('logDebug', repr(new_res))
    log_msg('logDebug', '\n----------\n')

    if res != new_res:
        print('Check failed! The resources are different after import/ export!')
        return False

    print('-' * 60 + '\n')

    return True


def test(PROXY, USER):

    log_msg('logRunning', 'Starting import...\n')

    ip, port = PROXY.cherry_addr()
    print('Params: {} {} {}'.format(USER, ip, port))
    _proxy_tb = 'http://{}:EP@{}:{}/tb/'.format(USER, ip, port)
    ra_tb = xmlrpclib.ServerProxy(_proxy_tb)
    _proxy_sut = 'http://{}:EP@{}:{}/sut/'.format(USER, ip, port)
    ra_sut = xmlrpclib.ServerProxy(_proxy_sut)
    print ra_tb
    print ra_sut

    _curr_dir = os.getcwd()
    _xml_file = _curr_dir + '/testbed.xml'

    # -----
    # Check at the beggining

    r = check(ra_tb, ra_sut, _xml_file)
    if not r:
        return 'Fail'

    py_res = 'tb_' + hexlify(os.urandom(4))
    print('Create TB `{}`...'.format(py_res))
    res_id = set_resource(py_res, '/', {'meta1': 1, 'meta2': 2, 'meta3': ''})
    print('Ok.\n')

    # -----
    # Check after creating a new element

    r = check(ra_tb, ra_sut, _xml_file)
    if not r:
        return 'Fail'

    print('Delete TB :', delete_resource(res_id))

    # -----
    # Check after the delete of the element

    r = check(ra_tb, ra_sut, _xml_file)
    if not r:
        return 'Fail'

    log_msg('logRunning', 'Finished import/ export.\n')

    cleanup(_xml_file)
    return 'Pass'

#

# Must have one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout'
_RESULT = test(PROXY, USER)

# Eof()
