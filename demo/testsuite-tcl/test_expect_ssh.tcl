
proc Test {} {
    #set testName [lindex [info frame 0] [expr {[llength [info frame 0]] - 3}]]
    set testName "test_expect_ssh.tcl"
    puts "\n**********\nStarting test: $testName\n"
    logMessage logTest "\n\nTestCase: $testName starting\n"

    set purpose "<title>Testing Expect SSH</title>"
    set description "<description>Testing SSH</description>"
    logMessage logTest "\nTest purpose: $purpose\nTest description: $description\n"

    set error_code "PASS"

    # Testing Expect
    set timeout 10
    spawn ssh user@localhost

    expect "Are you sure you want to continue connecting (yes/no)?"
    send "yes\n"

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
# Must return one of the statuses:
# 'pass', 'fail', 'skipped', 'aborted', 'not executed', 'timeout', 'invalid'
Test
