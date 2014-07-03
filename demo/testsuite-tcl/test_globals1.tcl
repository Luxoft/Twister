
proc Test {} {
    #set testName [lindex [info frame 0] [expr {[llength [info frame 0]] - 3}]]
    set testName "test_globals.tcl"
    puts "\n**********\nStarting test: $testName\n"
    logMessage logTest "\n\nTestCase: $testName starting\n"

    set purpose "<title>Testing global params 1</title>"
    set description "<description>Testing Global Params</description>"
    logMessage logTest "\nTest purpose: $purpose\nTest description: $description\n"

    set error_code "FAIL"

    puts "Query Globals Level 1... [get_global /Level_1]\n"

    puts "Query Globals Level 1/ global1... [get_global Level_1/global1]"
    puts "Query Globals Level 1/ global2... [get_global Level_1/global2]\n"

    set_global "some_global1" "some string"
    set_global "some_global2" 9999

    puts "Query Global 1... [get_global /some_global1]"
    puts "Query Global 2... [get_global /some_global2]"

    puts "\nFinished test $testName, exit code $error_code\n**********\n"
    logMessage logTest "TestCase: $testName $error_code\n"

    # This return is used by the framework!
    set error_code "PASS"
    return $error_code
}

# Call the test !
# Must return one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout', 'invalid'
Test
