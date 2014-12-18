#!/usr/bin/env python

# File: generate.py ; This file is part of Twister.

# version: 2.003

# Copyright (C) 2013 , Luxoft

# Authors:
#    Adrian Toader <adtoader@luxoft.com>
#    Andrei Costachi <acostachi@luxoft.com>
#    Andrei Toma <atoma@luxoft.com>
#    Cristi Constantin <crconstantin@luxoft.com>
#    Daniel Cioata <dcioata@luxoft.com>
#    Mihail Tudoran <mtudoran@luxoft.com>

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''
This file generates Ixia Library wrapper in Python, using TCL functions from IxTclHal.
Params: - IxOS TCL lib path
        - IP address of Ixia chassis
'''

from Tkinter import Tcl
from collections import OrderedDict
import re
import socket
import sys
import os

chassis_ip = '10.100.100.45'
tcl_lib_path = '/home/twister/ixos/ixia/lib/ixTcl1.0'

if len(sys.argv) < 3:
   print 'Usage: python generate.py <ixos_tcl_lib_path> <chassis_ip_address>'
   exit()

tcl_lib_path = sys.argv[1]
chassis_ip = sys.argv[2]

# some minimal checks on IP address
if chassis_ip.count('.') < 3:
    print 'ERROR: IP address not valid !'

try:
    socket.inet_aton(chassis_ip)
except socket.error:
    print 'ERROR: IP address not valid !'
    exit()

# check if IxOS tcl lib path exists
if tcl_lib_path[-1] == '/':
    tcl_lib_path = tcl_lib_path.rstrip('/')
if not os.path.isdir(tcl_lib_path):
    print 'ERROR: IxOS tcl lib path doesn\'t exists'
    exit()

tcl = Tcl()

tcl.eval('package req IxTclHal')
tcl.eval('ixConnectToTclServer ' + chassis_ip)
tcl.eval('ixConnectToChassis ' + chassis_ip)

# # # # # # # #

HEAD = """
from Tkinter import Tcl

t = Tcl()

t.eval('package req IxTclHal')

true  = True
false = False
yes   = True
no    = False
none  = None

"""

TAIL = """

def ix_exec(cmd):
    # This is used for executing custom TCL commands
    r = t.eval(cmd)
    return r


if __name__ == "__main__":
    chassis_ip = '%s'
    funcs = [x[0] for x in locals().items() if callable( x[1] )]
    # print sorted(funcs)
    print 'Found {} functions!'.format(len(funcs))

    print 'Is this UNIX?', isUNIX()
    print 'Connect to TCL Server:', ixConnectToTclServer(chassis_ip)
    print 'Connect to Chassis', ixConnectToChassis(chassis_ip)

    print 'Config chassis...'
    portList = ''
    chassis('get ' + chassis_ip)
    py_chassis = chassis('cget -id')
    print py_chassis

    print 'Config card...'
    py_card = 1
    card('setDefault')
    card('config -txFrequencyDeviation 0')
    print py_card

    print 'Config port...'
    py_port = 1
    port('setFactoryDefaults {} {} {}'.format(py_chassis, py_card, py_port))
    port('config -speed                100')
    port('config -duplex               full')
    port('config -flowControl          false')
    print py_port

    print 'Config stat...'
    stat('setDefault')
    stat('config -mode                      statNormal')
    stat('config -enableValidStats          false')
    stat('config -enableProtocolServerStats true')
    stat('config -enableArpStats            true')
    stat('config -enablePosExtendedStats    true')
    stat('config -enableDhcpStats           false')
    stat('config -enableDhcpV6Stats         false')
    stat('config -enableEthernetOamStats    false')
    print 'Done.'

    print 'Config flexibleTimestamp...'
    flexibleTimestamp('setDefault')
    flexibleTimestamp('config -type          timestampBeforeCrc')
    flexibleTimestamp('config -offset        23')
    print 'Done.'

    print 'Config filter...'
    ix_filter('setDefault')
    ix_filter('config -captureTriggerDA      anyAddr')
    ix_filter('config -captureTriggerSA      anyAddr')
    ix_filter('config -captureTriggerPattern anyPattern')
    ix_filter('config -captureTriggerError   errAnyFrame')
    print 'Done.'

    print 'Config filterPallette...'
    filterPallette('setDefault')
    filterPallette('config -DA1              "00 00 00 00 00 00"')
    filterPallette('config -DAMask1          "00 00 00 00 00 00"')
    filterPallette('config -DA2              "00 00 00 00 00 00"')
    filterPallette('config -DAMask2          "00 00 00 00 00 00"')
    filterPallette('config -SA1              "00 00 00 00 00 00"')
    filterPallette('config -SAMask1          "00 00 00 00 00 00"')
    filterPallette('config -SA2              "00 00 00 00 00 00"')
    filterPallette('config -SAMask2          "00 00 00 00 00 00"')
    filterPallette('config -pattern1         "DE ED EF FE AC CA"')
    filterPallette('config -patternMask1     "00 00 00 00 00 00"')
    print 'Done.'

    print 'Config capture...'
    capture('setDefault')
    capture('config -fullAction              lock')
    capture('config -sliceSize               8191')
    print 'Done.'

    print 'Config ipAddressTable...'
    ipAddressTable('setDefault')
    ipAddressTable('config -defaultGateway   "0.0.0.0"')
    print 'Done.'

    print 'Config arpServer...'
    arpServer('setDefault')
    arpServer('config -retries               3')
    arpServer('config -mode                  arpGatewayOnly')
    arpServer('config -rate                  208333')
    arpServer('config -requestRepeatCount    3')
    print 'Done.'

    print 'Config interfaceTable...'
    interfaceTable('setDefault')
    interfaceTable('config -dhcpV4RequestRate                0')
    interfaceTable('config -dhcpV6RequestRate                0')
    interfaceTable('config -dhcpV4MaximumOutstandingRequests 100')
    interfaceTable('config -dhcpV6MaximumOutstandingRequests 100')
    #interfaceTable('config -fcoeRequestRate                  500')
    print 'Done.'

    print 'Clear All Interfaces ...'
    interfaceTable('clearAllInterfaces')
    print 'Done.'

    print 'Config protocolServer...'
    protocolServer('setDefault')
    protocolServer('config -enableArpResponse                true')
    protocolServer('config -enablePingResponse               false')
    print 'Done.'

    print 'Config oamPort...'
    oamPort('setDefault')
    oamPort('config -enable                  false')
    oamPort('config -macAddress              "00 00 AB BA DE AD"')
    oamPort('config -enableLoopback          false')
    oamPort('config -enableLinkEvents        false')
    print 'Done.'

    print 'Call ixWritePortsToHardware and ixCheckLinkState ...'
    # lappend portList [list $chassis $card $port] # ???
    ixWritePortsToHardware(portList, None)
    ixCheckLinkState(portList)
    print 'Done.'

#

""" % (chassis_ip)

# # # # # # # #

def tcl_convert(variable):
    """
    This returns the TCL value converted into Pyton string repr.

    alnum
        Any Unicode alphabet or digit character.
    alpha
        Any Unicode alphabet character.
    ascii
        Any character with a value less than \u0080 (those that are in the 7-bit ascii range).
    boolean
        Any of the forms allowed to Tcl_GetBoolean.
        In the case of boolean, true and false, if the function will return 0, then the varname will always be set to 0,
        due to the varied nature of a valid boolean value.
    control
        Any Unicode control character.
    digit
        Any Unicode digit character. Note that this includes characters outside of the [0-9] range.
    double
        Any of the valid forms for a double in Tcl, with optional surrounding \
         whitespace. In case of under/overflow in the value,
        0 is returned and the varname will contain -1.
    false
        Any of the forms allowed to Tcl_GetBoolean where the value is false.
    graph
        Any Unicode printing character, except space.
    integer
        Any of the valid forms for an ordinary integer in Tcl, with optional \
         surrounding whitespace. In case of under/overflow in the value,
        0 is returned and the varname will contain -1.
    lower
        Any Unicode lower case alphabet character.
    print
        Any Unicode printing character, including space.
    punct
        Any Unicode punctuation character.
    space
        Any Unicode space character.
    true
        Any of the forms allowed to Tcl_GetBoolean where the value is true.
    upper
        Any upper case alphabet character in the Unicode character set.
    wordchar
        Any Unicode word character. That is any alphanumeric character, and \
        any Unicode connector punctuation characters (e.g. underscore).
    xdigit
        Any hexadecimal digit character ([0-9A-Fa-f]).
    """

    global tcl
    types = OrderedDict([
        ['integer', int],
        ['digit', int],
        ['double', float],
        ['true', bool],
        ['false', bool],
        ['boolean', bool],
        ['xdigit', str],
        ['alnum', str],
        ['alpha', str],
        ['ascii', str],
        ['control', str],
        ['graph', str],
        ['lower', str],
        ['print', str],
        ['punct', str],
        ['space', str],
        ['upper', str],
        ['wordchar', str],
        ])

    for tcl_type, py_type in types.iteritems():
        found = tcl.eval("string is {} -strict ${}".format(tcl_type, variable))
        found = int(found)

        if found:
            value = tcl.getvar('vDefaultArg')
            value = str(value)
            print 'Converting value `{}` into TCL type `{}`.'.format(value, tcl_type)
            if value == 'false' or value == 'no':
                return False
            elif py_type == str:
                return '"{}"'.format(value)
            else:
                return value

    return '!!!'

# # # # # # # #

IX_VARS = {
    'from':     'ix_from',
    'for':      'ix_for',
    'while':    'ix_while',
    'file':     'ix_file',
    'object':   'ix_object',
    'range':    'ix_range',
    'map':      'ix_map',
    'filter':   'ix_filter',
}

def fix_tcl_var(variable):
    """ replace TCL variable """
    global IX_VARS
    if variable in IX_VARS:
        return IX_VARS[variable]
    return variable

def fix_tcl_func(func):
    """ change TCL function """
    global IX_VARS
    func = func.replace('::', '_')
    if func in IX_VARS:
        return IX_VARS[func]
    return func

# # # # # # # #
'''
Get Ixia libray version from ixTclHal.tcl file
'''
ixos_version = ''
version_file = tcl_lib_path + '/ixTclHal.tcl'
try:
    with open(version_file, 'r') as v_file:
        for line in v_file:
            if line.startswith('package provide IxTclHal'):
                ixos_version = line.split()[-1]
                break
except:
    print 'ERROR: Cannot get IxOS version. Exiting !'
    exit()

# # # # # # # #
'''
Generate functions.txt file from file tclIndex
'''
FUNCTIONS = []
tcl_index_file = tcl_lib_path + '/tclIndex'
try:
    for line in open(tcl_index_file).readlines():
        if line.startswith('set auto_index(', 0):
            line = line.replace('set auto_index(','')
            FUNCTIONS.append(line.split(')')[0])
except:
    pass

# # # # # # # #
'''
Update functions.txt file from file ixTclSetup.tcl
'''
ix_tcl_setup =  tcl_lib_path + '/ixTclSetup.tcl'
try:
    file_content = open(ix_tcl_setup, 'r').read()

    # get entries from ixTclHal::noArgList
    no_arg_list = re.findall('set ixTclHal::noArgList(.*?)\{(.+?)\}',file_content, re.M | re.S) 
    FUNCTIONS.extend(no_arg_list[0][1].replace('\\','').split())

    # get entries from ixTclHal::pointerList
    pointer_list = re.findall('set ixTclHal::pointerList(.*?)\{(.+?)\}',file_content, re.M | re.S)
    FUNCTIONS.extend(pointer_list[0][1].replace('\\','').split())

    # get entries from ixTclHal::command
    command_list = re.findall('set ixTclHal::commandList(.*?)\{(.+?)\}',file_content, re.M | re.S)
    FUNCTIONS.extend(command_list[0][1].replace('\\','').split())
except:
    pass

try:
    with open('functions.txt', 'w') as OUTPUT:
        OUTPUT.write('\n'.join(FUNCTIONS))
except:
    pass

# # # # # # # #

FUNCTIONS = []

for line in open('functions.txt').readlines():

    if not line.strip():
        continue
    if '::' in line:
        continue

    func_name = line.strip() # TCL Function name

    tcl_args = []
    tcl_args_long = []
    pyc_args = []
    pyc_args_long = []

    tmpl = '# Function `{}` is invalid'.format(func_name) # Default string, sais the func is invalid
    tcl.eval('set vDefaultArg ""')

    defaultArgFound = False
    defaultArgs = [] # The list of mandatory arguments


    try:
        # Enable TCL Function. RISK excuting the function!
        try:
            tcl.eval(func_name)
        except:
            pass

        proc_args = tcl.eval('info args ' + func_name)

        for arg in proc_args.split():
            has_default = tcl.eval('info default %s %s vDefaultArg' % (func_name, arg))
            arg_fixed = fix_tcl_var(arg)

            # Args for executing
            tcl_args.append(arg)
            # Args for calling the TCL function
            pyc_args.append(arg_fixed)

            # If this argument has a default value
            if int(has_default) and tcl.getvar('vDefaultArg'):
                defaultArgFound = True
                # Args for comment
                tcl_args_long.append('%s {%s}' % (arg, str(tcl.getvar('vDefaultArg'))))
                # Args for defining Python functions
                pyc_args_long.append('%s=%s' % (arg_fixed, str(tcl_convert('vDefaultArg'))))
            else:
                tcl_args_long.append(arg)
                if not defaultArgFound:
                    pyc_args_long.append(arg_fixed)
                else:
                    defaultArgs.append(arg_fixed)
                    pyc_args_long.append('%s=None' % (arg_fixed))

            # Reset variable for the next cycle
            tcl.eval('set vDefaultArg ""')

        leng = len(tcl_args)
        tcl_args = ', '.join(tcl_args)
        tcl_args_long = ' '.join(tcl_args_long)
        pyc_args = ', '.join(pyc_args)
        pyc_args_long = ', '.join(pyc_args_long)

    except Exception, e:
        print('>>> Cannot create function `{}`, exception: `{}`!\n'.format(func_name, e))
        continue


    if defaultArgs:
        defaultArgs = '\n'.join([ '    if {0} is None: print "TCL argument ' \
        ' `{0}` cannot be empty!"; return False'.format(x) for x in defaultArgs ])
        tmpl = """
def {py}({py_arg_l}):
    '''\n     Method Name : {tcl}\n     Arguments   : {tcl_arg_l}
{def_arg}\n    '''
    r = t.eval("{tcl} {le}".format({py_arg}))
    return r
""".format(py=fix_tcl_func(func_name), tcl=func_name, py_arg=pyc_args, py_arg_l=pyc_args_long,
            tcl_arg=tcl_args, tcl_arg_l=tcl_args_long, le='{} '*leng, def_arg=defaultArgs)

    else:
        tmpl = """
def {py}({py_arg_l}):
    '''\n    Method Name : {tcl}\n    Arguments   : {tcl_arg_l} \n    '''
    r = t.eval("{tcl} {le}".format({py_arg}))
    return r
""".format(py=fix_tcl_func(func_name), tcl=func_name, py_arg=pyc_args, py_arg_l=pyc_args_long,
            tcl_arg=tcl_args, tcl_arg_l=tcl_args_long, le='{} '*leng)


    FUNCTIONS.append(tmpl)

#

output_file = 'TscIxPythonLib_v{}.py'.format(ixos_version)
OUTPUT = open(output_file, 'w')
OUTPUT.write(HEAD)
OUTPUT.write('\n'.join(FUNCTIONS))
OUTPUT.write(TAIL)
OUTPUT.close()

# Eof()
