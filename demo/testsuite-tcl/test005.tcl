
proc T-005 {} {
    #set testName [lindex [info frame 0] [expr {[llength [info frame 0]] - 3}]]
    set testName "test005.tcl"
    puts "\n**********\nStarting test: $testName\n"
    logMessage logTest "\n\nTestCase: $testName starting\n"

    set purpose "<title>Testing Resource Allocator Client</title>"
    set description "<description>This test should use all RAC functions in order to test the functionality</description>"
    logMessage logTest "\nTest purpose: $purpose\nTest description: $description\n"

    set error_code "PASS"

    puts "Query Root... [getResource 1]"
    puts "Query Root... [getResource /]\n"

    puts "Device 1:: [getResource /dev1]"
    puts "Device 1:: [getResource 101]\n"

    puts "Meta 1:: [getResource dev3/mod12:meta1]"
    puts "Meta 2:: [getResource dev3/mod12:meta2]\n"

    set id1 [setResource test1 dev3/mod12]
    puts "Create resource:: $id1"
    puts "Check info:: [getResource $id1]\n"

    puts "Update resource..."
    setResource "test1" "dev3/mod12" {{"more-info": "y"}}
    puts "Check info:: [getResource $id1]\n"

    puts "Check status 1:: [getResourceStatus $id1]"
    puts "Reserve resource:: [reserveResource $id1]"
    puts "Check status 2:: [getResourceStatus $id1]\n"

    puts "Delete resource:: [deleteResource $id1]"
    puts "Delete resource:: [deleteResource dev3/mod12/test1]"
    puts "Check info:: [getResource $id1]\n"

    puts "\nFinished test $testName, exit code $error_code\n**********\n"
    logMessage logTest "TestCase: $testName $error_code\n"

    # This return is used by the framework!
    return $error_code
}

# Call the test !
T-005
