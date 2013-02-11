
proc T-002 {} {
    #set testName [lindex [info frame 0] [expr {[llength [info frame 0]] - 3}]]
    set testName "test002.tcl"
    puts "\n**********\nStarting test: $testName\n"
    logMessage logTest "\n\nTestCase: $testName starting\n"

    set purpose "<title>Verify something 2 and print the results</title>"
    set description "<description> This test doesn't do anything spectacular, it just counts to 10, in 10 seconds. </description>"
    logMessage logTest "\nTest purpose: $purpose\nTest description: $description\n"

    set error_code "FAIL"

    if {1} {
        set error_code "PASS"
    }

    for {set i 0} {$i < 10} {incr i} {
        # Python function:
        logMessage logRunning "Tcl TEST 2: working $i...\n"
        after 500
    }

    # Python function:
    logMessage logDebug "Tcl TEST: working even more ...\n"
    after 100

    puts "\nFinished test $testName, exit code $error_code\n**********\n"
    logMessage logTest "TestCase: $testName $error_code\n"

    # The return is used in the framework!
    return $error_code
}

# Call the test !
T-002
