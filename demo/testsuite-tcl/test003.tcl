
proc T-003 {} {
    #set testName [lindex [info frame 0] [expr {[llength [info frame 0]] - 3}]]
    set testName "test003.tcl"
    puts "\n**********\nStarting test: $testName\n"
    logMessage logTest "\n\nTestCase: $testName starting\n"

    set purpose {Testing Expect take 1}
    set description {Some description}
    logMessage logCli "\nTest purpose: $purpose\nTest description: $description\n"

    set error_code "FAIL"

    # Testing Expect
    spawn ftp ftp.openbsd.org
    expect "Name .*: "
    send "anonymous\r"
    expect "Password:"
    send "noah@example.com\r"

    expect "530- " {
        set error_code "FAIL"
    }
    expect "ftp> " {
        set error_code "PASS"
    }

    send "ls /pub/OpenBSD/\r"
    expect "ftp> "

    send "quit\r"

    logMessage logDebug "Some message from test $testName ......."

    puts "\nFinished test $testName, exit code $error_code\n**********\n"
    logMessage logTest "TestCase: $testName $error_code\n"

    # The return is used in the framework!
    return $error_code
}

# Call the test !
T-003
