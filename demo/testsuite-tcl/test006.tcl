
proc T-006 {} {
    #set testName [lindex [info frame 0] [expr {[llength [info frame 0]] - 3}]]
    set testName "test006.tcl"
    puts "\n**********\nStarting test: $testName\n"
    logMessage logTest "\n\nTestCase: $testName starting\n"

    set purpose "<title>Global Params test example</title>"
    set description "<description>Testing Global Params</description>"
    logMessage logTest "\nTest purpose: $purpose\nTest description: $description\n"

    set error_code "PASS"

    global gparam

    puts $gparam(Level_1/global2)

    puts "$gparam(Level_1/Level_2/global2.3)\n"

    puts [array names gparam]

    puts "\nFinished test $testName, exit code $error_code\n**********\n"
    logMessage logTest "TestCase: $testName $error_code\n"

    # This return is used by the framework!
    return $error_code
}

# Call the test !
T-006
