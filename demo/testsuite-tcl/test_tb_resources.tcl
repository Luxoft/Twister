
#
# <title>Test Resource Allocator</title>
# <description>This test is checking the Resource Allocator.</description>
# <tags>testbed, resources, devices, SUTSs</tags>
#

proc Test {} {
    #set testName [lindex [info frame 0] [expr {[llength [info frame 0]] - 3}]]
    set testName "test_tb_resources.tcl"
    puts "\n**********\nStarting test: $testName\n"
    logMessage logTest "\n\nTestCase: $testName starting\n"

    set purpose "<title>Testing Resource Allocator connection</title>"
    set description "<description>This test should use all RA functions in order to test the functionality</description>"
    logMessage logTest "\nTest purpose: $purpose\nTest description: $description\n"

    set error_code "PASS"

    puts "Query Root... [getResource 1]"
    puts "Query Root... [getResource /]\n"

    set id1 [setResource tb_tcl1 / {{"meta1": "data1", "meta2": "data2"}}]
    puts "Create resource:: $id1\n"

    puts "Check info..."
    puts "Testbed 1:: [getResource /tb_tcl1]"
    puts "Testbed 1:: [getResource $id1]\n"

    puts "Update resource..."
    setResource "tb_tcl1" "/" {{"more-info": "y"}}
    puts "Check info:: [getResource $id1]\n"

    puts "Meta 1:: [getResource /tb_tcl1:meta1]"
    puts "Meta 2:: [getResource /tb_tcl1:meta2]\n"

    puts "Check status 1:: [getResourceStatus $id1]"
    puts "Reserve resource:: [reserveResource $id1]"
    puts "Check status 2:: [getResourceStatus $id1]\n"

    puts "Delete resource:: [deleteResource $id1]"
    puts "Delete resource:: [deleteResource /tb_tcl1]"
    puts "Check info:: [getResource $id1]\n"

    puts "\nFinished test $testName, exit code $error_code\n**********\n"
    logMessage logTest "TestCase: $testName $error_code\n"

    # This return is used by the framework!
    return $error_code
}

# Call the test !
# Must return one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout', 'invalid'
Test
