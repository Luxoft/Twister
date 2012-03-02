
proc T-001 {} {
    #set testName [lindex [info frame 0] [expr {[llength [info frame 0]] - 3}]]
    set testName "test001.tcl"
    puts "\n**********\nStarting test: $testName\n"
    logMessage logTest "\n\nTestCase: $testName starting\n"

    set purpose {Verify something and print the results}
    set description {Some description}
    logMessage logCli "\nTest purpose: $purpose\nTest description: $description\n"

    set error_code "FAIL"

    if {0} {
        set error_code "PASS"
    }

    for {set i 0} {$i < 10} {incr i} {
        # Python function:
        logMessage logRunning "TEST 1: working $i..."
        after 500
    }

    # Python function:
    logMessage logDebug "TEST: working even more ..."
    after 100

    puts "\nFinished test $testName, exit code $error_code\n**********\n"
    logMessage logTest "TestCase: $testName $error_code\n"

    # The return is used in the framework!
    return $error_code
}

# Call the test !
T-001
