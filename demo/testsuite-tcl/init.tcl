
#
# Initialize the global variables needed for running the tests and ...
# Prepair the phisical equipment for running the tests.
# This involves setting/ resetting/ restarting the equipment a few times.
# It can take a long time ...
#

# Load a few sources
set DEMO_PATH "/home/tscguest/twister/demo/testsuite-tcl/"
lappend auto_path $DEMO_PATH
puts "\nTCL debug: Autopath is: $auto_path"

logMessage logTest "\n\nTestCase: init.tcl starting\n"

# Load Expect and some demo library
package require Expect
package require DemoLib

# Set a few global variables
global logRunning
global logDebug
global logTest
global logCli

proc demo_setup {} {
    #// Some variables.
    global variable1
    global variable2
    global variable3

    variable suiteName       "DemoSuite"
    variable varManagementIp "192.168.0.1"
    variable varPrivateSlot  "..."
    variable varPublicIp     "74.125.43.99"
    variable varPublicSlot   "..."

    variable varAdminName   "demo-admin"
    variable varAdminPass   "demo-password"
    variable varLicense     "LIC-12345-12345-LIC"
    variable varServCert    0
    variable varCaCert      0

    #// Connect and setup ...
    connect_and_setup_function1
    connect_and_setup_function2
    connect_and_setup_function3

    logMessage logDebug "TCL Setup done."
    return
}

proc connect_and_setup_function1 {} {
    logMessage logDebug "Running setup 1."
    after 1000
}

proc connect_and_setup_function2 {} {
    logMessage logDebug "Running setup 2.."
    after 1000
}

proc connect_and_setup_function3 {} {
    logMessage logDebug "Running setup 3..."
    after 1000
}

demo_setup

puts "\nTCL init done.\n"
