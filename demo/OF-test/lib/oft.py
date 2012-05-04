#!/usr/bin/env python

import sys
from optparse import OptionParser
from subprocess import Popen,PIPE
from pprint import pprint
import cStringIO as IO
import logging
import unittest
import time
import os

import testutils

try:
    import scapy.all as scapy
except:
    try:
        import scapy as scapy
    except:
        sys.exit("Need to install scapy for packet parsing")

if os.getuid() != 0:
    print "ERROR: Super-user privileges required. Please re-run with sudo or as root."
    exit(1)


##@var DEBUG_LEVELS
# Map from strings to debugging levels
DEBUG_LEVELS = {
    'debug'              : logging.DEBUG,
    'verbose'            : logging.DEBUG,
    'info'               : logging.INFO,
    'warning'            : logging.WARNING,
    'warn'               : logging.WARNING,
    'error'              : logging.ERROR,
    'critical'           : logging.CRITICAL
}

##@var config_default
# The default configuration dictionary for OFT
config_default = {
    "param"              : None,
    "platform"           : "local",
    "controller_host"    : "10.9.6.220",
    "controller_port"    : 6633,
    "port_count"         : 4,
    "base_of_port"       : 1,
    "base_if_index"      : 1,
    "relax"              : False,
    "test_spec"          : "all",
    "test_dir"           : "/home/tscguest/twister/.twister_cache/ce_libs",
    "log_file"           : "oft.log",
    "list"               : False,
    "debug"              : "info",
    "dbg_level"          : logging.DEBUG,
    "port_map"           : {18 : "eth0", 19 : "eth0:0", 20 : "eth0:1", 21 : "eth0:2"},
    "caps_table_idx"     : 0,
    "test_params"        : "None",
    "profile"            : None
}

# Default test priority
TEST_PRIO_DEFAULT=100
TEST_PRIO_SKIP=-1

#@todo Set up a dict of config params so easier to manage:
# <param> <cmdline flags> <default value> <help> <optional parser>


# Map options to config structure
def config_get(opts):
    "Convert options class to OFT configuration dictionary"
    cfg = config_default.copy()
    for key in cfg.keys():
        cfg[key] = eval("opts." + key)

    # Special case checks
    if opts.debug not in DEBUG_LEVELS.keys():
        print "Warning:  Bad value specified for debug level; using default"
        opts.debug = "info"
    if opts.verbose:
        cfg["debug"] = "verbose"
    cfg["dbg_level"] = DEBUG_LEVELS[cfg["debug"]]

    return cfg


def config_setup(cfg_dflt):
    """
    Set up the configuration including parsing the arguments

    @param cfg_dflt The default configuration dictionary
    @return A pair (config, args) where config is an config
    object and args is any additional arguments from the command line
    """

    parser = OptionParser(version="%prog 0.1")

    #@todo parse port map as option?
    # Set up default values
    for key in cfg_dflt.keys():
        eval("parser.set_defaults("+key+"=cfg_dflt['"+key+"'])")

    #@todo Add options via dictionary
    plat_help = """Set the platform type.  Valid values include:
        local:  User space virtual ethernet pair setup
        remote:  Remote embedded Broadcom based switch
        Create a new_plat.py file and use --platform=new_plat on the command line
        """
    parser.add_option("-P", "--platform", help=plat_help)
    parser.add_option("-H", "--host", dest="controller_host", help="The IP/name of the test controller host")
    parser.add_option("-p", "--port", dest="controller_port", type="int", help="Port number of the test controller")
    test_list_help = """Indicate tests to run.  Valid entries are "all" (the
        default) or a comma separated list of:
        module            Run all tests in the named module
        testcase          Run tests in all modules with the name testcase
        module.testcase   Run the specific test case
        """

    parser.add_option("--test-spec", "--test-list", help=test_list_help)
    parser.add_option("--log-file",
                      help="Name of log file, empty string to log to console")
    parser.add_option("--debug",
                      help="Debug lvl: debug, info, warning, error, critical")
    parser.add_option("--port-count", type="int",
                      help="Number of ports to use (optional)")
    parser.add_option("--base-of-port", type="int",
                      help="Base OpenFlow port number (optional)")
    parser.add_option("--base-if-index", type="int",
                      help="Base interface index number (optional)")
    parser.add_option("--list", action="store_true",
                      help="List all tests and exit")
    parser.add_option("--verbose", action="store_true",
                      help="Short cut for --debug=verbose")
    parser.add_option("--relax", action="store_true",
                      help="Relax packet match checks allowing other packets")
    parser.add_option("--param", type="int",
                      help="Parameter sent to test (for debugging)")
    parser.add_option("--profile",
                      help="File listing tests to skip/run")
    parser.add_option("-t", "--test-params",
                      help="""Set test parameters: key=val;...
        NOTE:  key MUST be a valid Python identifier, egr_count not egr-count
        See --list""")

    # Might need this if other parsers want command line
    # parser.allow_interspersed_args = False
    (options, args) = parser.parse_args()
    config = config_get(options)
    return (config, args)


def test_list_generate(config):
    """Generate the list of all known tests indexed by module name

    Conventions:  Test files must implement the function test_set_init

    Test cases are classes that implement runTest

    @param config The oft configuration dictionary
    @returns An array of triples (mod-name, module, [tests]) where
    mod-name is the string (filename) of the module, module is the
    value returned from __import__'ing the module and [tests] is an
    array of strings giving the test cases from the module.
    """

    # Find and import test files
    p1 = Popen(["find", config["test_dir"], "-type", 'f'], stdout = PIPE)
    p2 = Popen(["xargs", "grep", "-l", "-e", "^def test_set_init"], stdin=p1.stdout, stdout=PIPE)

    all_tests = {}
    mod_name_map = {}

    # There's an extra empty entry at the end of the list
    filelist = p2.communicate()[0].split("\n")[:-1]

    for file in filelist:
        if file[-1:] == '~' or file[0] == '#':
            continue
        modfile = file.lstrip('./')[:-3]
        modfile = os.path.split(modfile)[1]
        try:
            mod = __import__(modfile)
        except:
            logging.warning("Could not import file " + file)
            continue
        mod_name_map[modfile] = mod
        added_fn = False
        for fn in dir(mod):
            if 'runTest' in dir(eval("mod." + fn)):
                if not added_fn:
                    mod_name_map[modfile] = mod
                    all_tests[mod] = []
                    added_fn = True
                all_tests[mod].append(fn)

    config["all_tests"] = all_tests
    config["mod_name_map"] = mod_name_map


def die(msg, exit_val=1):
    print msg
    logging.critical(msg)
    sys.exit(exit_val)


def _space_to(n, str):
    """
    Generate a string of spaces to achieve width n given string str
    If length of str >= n, return one space
    """
    spaces = n - len(str)
    if spaces > 0:
        return " " * spaces
    return " "


def test_prio_get(mod, test):
    """
    Return the priority of a test

    If test is in "skip list" from profile, return the skip value

    If set in the test_prio variable for the module, return
    that value.  Otherwise return 100 (default)
    """
    if 'test_prio' in dir(mod):
        if test in mod.test_prio.keys():
            return mod.test_prio[test]
    return TEST_PRIO_DEFAULT

#
# Main script
#

# Get configuration, set up logging, import platform from file
(config, args) = config_setup(config_default)

test_list_generate(config)

# Check if test list is requested; display and exit if so
if config["list"]:

    did_print = False
    mod_count = 0
    test_count = 0
    print "\nTest List:"

    for mod in config["all_tests"].keys():
        if config["test_spec"] != "all" and config["test_spec"] != mod.__name__:
            continue

        mod_count += 1
        did_print = True
        desc = mod.__doc__.strip()
        desc = desc.split('\n')[0]
        start_str = "  Module " + mod.__name__ + ": "
        print start_str + _space_to(22, start_str) + desc
        for test in config["all_tests"][mod]:
            try:
                desc = eval('mod.' + test + '.__doc__.strip()')
                desc = desc.split('\n')[0]
            except:
                desc = "No description"
            if test_prio_get(mod, test) < 0:
                start_str = "  * " + test + ":"
            else:
                start_str = "    " + test + ":"
            if len(start_str) > 22:
                desc = "\n" + _space_to(22, "") + desc
            print start_str + _space_to(22, start_str) + desc
            test_count += 1
        print

    if not did_print:
        print "No tests found for " + config["test_spec"]
    else:
        print "%d modules shown with a total of %d tests" % \
            (mod_count, test_count)
        print
        print "Tests preceded by * are not run by default"

    print "Tests marked (TP1) after name take --test-params including:"
    print "    'vid=N;strip_vlan=bool;add_vlan=bool'"
    print "Note that --profile may override which tests are run"
    sys.exit(0)

# Logging
_format = "%(asctime)s  %(name)-10s: %(levelname)-8s: %(message)s"
_datefmt = "%H:%M:%S"
logging.basicConfig(filename=config["log_file"], level=config["dbg_level"], format=_format, datefmt=_datefmt)
# Must also show in console
console = logging.StreamHandler()
console.setLevel(logging.NOTSET)
logging.getLogger('').addHandler(console)

logging.info("++++++++ " + time.asctime() + " ++++++++")

# Generate the test suite
suite = unittest.TestSuite()

#

def build_all_tests():
    '''
    Run when needed.
    '''

    print 'Build:: Building ALL tests...'
    #@todo Allow specification of priority to override prio check
    if config["test_spec"] == "all":
        for mod in config["all_tests"].keys():
           for test in config["all_tests"][mod]:
               # For now, a way to avoid tests
               if test_prio_get(mod, test) >= 0:
                   suite.addTest(eval("mod." + test)())

    else:
        for ts_entry in config["test_spec"].split(","):
            parts = ts_entry.split(".")

            # Either a module or test name
            if len(parts) == 1:
                # A module name
                if ts_entry in config["mod_name_map"].keys():
                    mod = config["mod_name_map"][ts_entry]
                    for test in config["all_tests"][mod]:
                        if test_prio_get(mod, test) >= 0:
                            suite.addTest(eval("mod." + test)())
                # Search for matching tests
                else:
                    test_found = False
                    for mod in config["all_tests"].keys():
                        if ts_entry in config["all_tests"][mod]:
                            suite.addTest(eval("mod." + ts_entry)())
                            test_found = True
                    if not test_found:
                        die("Could not find module or test: " + ts_entry)

            # module.test
            elif len(parts) == 2:
                if parts[0] not in config["mod_name_map"]:
                    die("Unknown module in test spec: " + ts_entry)
                mod = config["mod_name_map"][parts[0]]
                if parts[1] in config["all_tests"][mod]:
                    suite.addTest(eval("mod." + parts[1])())
                else:
                    die("No known test matches: " + ts_entry)

            else:
                die("Bad test spec: " + ts_entry)


def build_test_name(ts_entry):
    '''
    Add just 1 test.
    '''
    global suite
    suite = unittest.TestSuite()
    test_found = False

    for mod in config["all_tests"].keys():
        if ts_entry in config["all_tests"][mod]:
            print 'Build:: Found test::', eval("mod." + ts_entry), '!'
            suite.addTest(eval("mod." + ts_entry)())
            test_found = True
            break
    if test_found:
        print 'Build:: The suite: `%s`.\n' % suite
    else:
        print 'Build:: ERROR! Cannot find test::', ts_entry


def init_all_tests():
    '''
    Init the test sets
    '''
    global config
    for (modname, mod) in config["mod_name_map"].items():
        try:
            mod.test_set_init(config)
            logging.debug("Config done for module " + modname)
        except:
            logging.warning("Could not run test_set_init for " + modname)

#

if __name__ == "__main__":

    logging.info("*** TEST RUN START: " + time.asctime())

    build_all_tests()
    init_all_tests()

    unittest.TextTestRunner(verbosity=1).run(suite)

    if testutils.skipped_test_count > 0:
        ts = " tests"
        if testutils.skipped_test_count == 1: ts = " test"
        logging.info("Skipped " + str(testutils.skipped_test_count) + ts)
        print("Skipped " + str(testutils.skipped_test_count) + ts)

    logging.info("*** TEST RUN END  : " + time.asctime())

#
