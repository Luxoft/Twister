
'''
    |----------------------------|
    | Spirent STC wrapper module |
    |----------------------------|

    This is a python wrapper other STC TCL library
    The TCLLIBPATH environment variable must be set to include the path to
    Spirent Test Center Application directory.
    Example:
    export TCLLIBPATH=/home/user/Spirent_TestCenter_4.44/Spirent_TestCenter_Application_Linux
'''

from Tkinter import Tcl

t = Tcl()

t.eval('package req SpirentTestCenter')

true  = True
false = False
yes   = True
no    = False
none  = None

def stc_apply():
    r = t.eval('stc::apply')
    return r

def stc_config(handle_string, attributes):
    r = t.eval('stc::config {} {}'.format(handle_string, attributes))
    return r

def stc_connect(chassis_address):
    r = t.eval('stc::connect {}'.format(chassis_address))
    return r

def stc_create(object_type_string, attributes=None):
    r = None
    if attributes is None:
        r = t.eval('stc::create {}'.format(object_type_string))
    else:
        r = t.eval('stc::create {} {}'.format(object_type_string, attributes))
    return r

def stc_delete(handle_string):
    r = t.eval('stc::delete {}'.format(handle_string))
    return r

def stc_disconnect(chassis_address):
    r = t.eval('stc::disconnect {}'.format(chassis_address))
    return r

def stc_get(handle_string, attributes=None):
    r = None
    if attributes is None:
        r = t.eval('stc::get {}'.format(handle_string))
    else:
        r = t.eval('stc::get {} {}'.format(handle_string, attributes))
    return r

def stc_perform(cmd, attributes=None):
    r = None
    if attributes is None:
        r = t.eval('stc::perform {}'.format(cmd))
    else:
        r = t.eval('stc::perform {} {}'.format(cmd, attributes))
    return r

def stc_release(port):
    r = t.eval('stc::release {}'.format(port))
    return r

def stc_reserve(port):
    r = t.eval('stc::reserve {}'.format(port))
    return r

def stc_sleep(seconds):
    r = t.eval('stc::sleep {}'.format(seconds))
    return r

def stc_subscribe(attributes):
    r = t.eval('stc::subscribe {}'.format(attributes))
    return r

def stc_unsubscribe(handle_string):
    r = t.eval('stc::unsubscribe {}'.format(handle_string))
    return r

def stc_waitUntilComplete(timeout):
    r = t.eval('stc::waitUntilComplete {}'.format(timeout))
    return r

def stc_exec(cmd):
    # This is used for executing custom TCL commands
    r = t.eval(cmd)
    return r

