
proc T-004 {} {
    #set testName [lindex [info frame 0] [expr {[llength [info frame 0]] - 3}]]
    set testName "test004.tcl"
    puts "\n**********\nStarting test: $testName\n"
    logMessage logTest "\n\nTestCase: $testName starting\n"

    set purpose "<title>Testing Expect take 2</title>"
    set description "<description>Testing SSH</description>"
    logMessage logTest "\nTest purpose: $purpose\nTest description: $description\n"

    set error_code "PASS"

    # Testing Expect
    set timeout 100
    spawn ssh user@localhost

    #expect "Are you sure you want to continue connecting (yes/no)?"
    expect "*?assword:*"
    send "password\n"

    expect "user@localhost"
    send "cd twister\n"

    expect "user@localhost"
    send "ls -la\n"

    expect "user@localhost"
    send "exit\n"

    logMessage logDebug "Message from test $testName"

    puts "\nFinished test $testName, exit code $error_code\n**********\n"
    logMessage logTest "TestCase: $testName $error_code\n"

    # The return is used in the framework!
    return $error_code
}

# Call the test !
T-004
