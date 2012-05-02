
import os, sys, time

if os.getenv('TWISTER_PATH'):
    sys.path.append(os.getenv('TWISTER_PATH') + '/.twister_cache/ce_libs/')

#

def openflow_init():
    '''
    <title>OpenFlow: INITIALIZATION</title>
    <description>This test removes ALL rules defined by the floodlite controller and adds the direct path.</description>
    '''

    from LibOpenFlow import log_debug, FloodLiteControl, StaticFlowPusher, initial_flow_path, changed_flow_path

    log_debug('\n=== Starting openflow init ===')

    restapi = FloodLiteControl('10.9.6.220', 8080)
    flowpusher = StaticFlowPusher('10.9.6.220')
    fl_switches = restapi.get_switches()

    # ----------------------------------------------------------------------------------------------
    # Removing settings for DIRECT DATAPATH
    # ----------------------------------------------------------------------------------------------
    fl_nr = 0
    tm_wait = 30
    fl_list = []

    for ifp in initial_flow_path:
        fl_nr += 1
        if ifp[2]:
            fl_dict={'switch':ifp[0], 'name':'flow-mod-%i' % fl_nr, 'cookie':'0', 'priority':'32768',
                'ingress-port':str(ifp[1]), 'active':'true', 'actions':'output=%i' % ifp[2]}
        else:
            fl_dict={'switch':ifp[0], 'name':'disable-%s' % str(ifp[1]), 'cookie':'0', 'priority':'32768',
                'ingress-port':str(ifp[1]), 'active':'true', 'actions':''}
        fl_list.append(fl_dict)

    log_debug('\nRemoving short datapath settings...\n')

    for fl in fl_list:
        flowpusher.remove(fl)
        time.sleep(0.5)
        log_debug('Flow removed:\n %s' % str(fl))

    # ----------------------------------------------------------------------------------------------
    # Removing settings for DIVERTED DATAPATH
    # ----------------------------------------------------------------------------------------------
    fl_nr = 0
    tm_wait = 30
    fl_list = []

    for ifp in changed_flow_path:
        fl_nr += 1
        if ifp[2]:
            fl_dict={'switch':ifp[0], 'name':'flow-mod-%i' % fl_nr, 'cookie':'0', 'priority':'32768',
                'ingress-port':str(ifp[1]), 'active':'true', 'actions':'output=%i' % ifp[2]}
        else:
            fl_dict={'switch':ifp[0], 'name':'disable-%s' % str(ifp[1]), 'cookie':'0', 'priority':'32768',
                'ingress-port':str(ifp[1]), 'active':'true', 'actions':''}
        fl_list.append(fl_dict)

    log_debug('\nRemoving changed datapath settings...\n')

    for fl in fl_list:
        flowpusher.remove(fl)
        time.sleep(0.5)
        log_debug('Flow removed:\n %s' % str(fl))

    #
    log_debug('\n--- ALL paths removed, the controller is clear ! ---\n')
    #

    # ----------------------------------------------------------------------------------------------
    # Add settings for DIRECT DATAPATH
    # ----------------------------------------------------------------------------------------------
    fl_nr = 0
    tm_wait = 30
    fl_list = []

    for ifp in initial_flow_path:
        fl_nr += 1
        if ifp[2]:
            fl_dict={'switch':ifp[0], 'name':'flow-mod-%i' % fl_nr, 'cookie':'0', 'priority':'32768',
                'ingress-port':str(ifp[1]), 'active':'true', 'actions':'output=%i' % ifp[2]}
        else:
            fl_dict={'switch':ifp[0], 'name':'disable-%s' % str(ifp[1]), 'cookie':'0', 'priority':'32768',
                'ingress-port':str(ifp[1]), 'active':'true', 'actions':''}
        fl_list.append(fl_dict)

    log_debug('\nAdding short datapath settings...\n')

    for fl in fl_list:
        flowpusher.set(fl)
        time.sleep(0.5)
        log_debug('Flow added:\n %s' % str(fl))

    #
    log_debug('\n--- Initialization done ! ---\n')
    #

    return 'PASS'

#

_RESULT = openflow_init()

#
