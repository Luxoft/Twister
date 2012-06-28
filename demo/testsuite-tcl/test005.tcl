
proc T-005 {} {
    #set testName [lindex [info frame 0] [expr {[llength [info frame 0]] - 3}]]
    set testName "test005.tcl"
    puts "\n**********\nStarting test: $testName\n"
    logMessage logTest "\n\nTestCase: $testName starting\n"

    set purpose {Testing Resource Allocator Client}
    set description {This test should use all RAC functions in order to test the functionality}
    logMessage logTest "\nTest purpose: $purpose\nTest description: $description\n"

    set error_code "PASS"

    puts queryResource "devicevendor:Avaya&&devicetype:PBX,moduletype:?"
    puts queryResource "devicetype:Contivity&&devicefamily:27XX&&devicemodel:2750SY"

    set resid [createEmptyResource 0]

    setPropertyLocal $resid "prop_1" "value_1"
    setPropertyLocal $resid "prop_2" "value_2"

    puts getPropertyLocal $resid "prop_1"
    puts getPropertyLocal $resid "prop_2"

    delResource $resid

    puts "\nFinished test $testName, exit code $error_code\n**********\n"
    logMessage logTest "TestCase: $testName $error_code\n"

    # This return is used by the framework!
    return $error_code
}

# Call the test !
T-005
