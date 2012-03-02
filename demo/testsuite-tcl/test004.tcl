
proc T-004 {} {
    #set testName [lindex [info frame 0] [expr {[llength [info frame 0]] - 3}]]
    set testName "test004.tcl"
    puts "\n**********\nStarting test: $testName\n"
    logMessage logTest "\n\nTestCase: $testName starting\n"

    set purpose {Testing Expect take 1}
    set description {Some description}
    logMessage logCli "\nTest purpose: $purpose\nTest description: $description\n"

    set error_code "PASS"

    # Testing Expect
    set timeout 100
    spawn ssh tscguest@11.126.32.9

    #expect "Are you sure you want to continue connecting (yes/no)?"
    expect "*?assword:*"
    send "tscguest\n"

    expect "tscguest@tsc-server"
    send "cd twister\n"

    expect "tscguest@tsc-server"
    send "ls -la\n"

    expect "tscguest@tsc-server"
    send "exit\n"

    logMessage logDebug "Message from test $testName"

    puts "\nFinished test $testName, exit code $error_code\n**********\n"
    logMessage logTest "TestCase: $testName $error_code\n"

    # The return is used in the framework!
    return $error_code
}

# Call the test !
T-004
