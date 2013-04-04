
proc Test {} {
    # This test REQUIRES that you run test_py_globals2.py,
    # so that you have defined func1, func2, Class1 and Class2

    set testName "test_globals.tcl"
    puts "\n**********\nStarting test: $testName\n"
    logMessage logTest "\n\nTestCase: $testName starting\n"

    set purpose "<title>Testing global params 2</title>"
    set description "<description>Testing Global Params</description>"
    logMessage logTest "\nTest purpose: $purpose\nTest description: $description\n"

    set error_code "FAIL"

    puts "Calling function 1 [py_exec func1]"
    puts "---"

    puts "Calling function 1 [py_exec func2]"
    puts "---"

    puts "Calling class 1 [py_exec Class1]"
    puts "---"

    puts "Calling class 2 [py_exec Class2]"
    puts "---"

    puts "Checking instance 1  [py_exec Class1i.__str__]"
    puts "---"

    puts "Checking instance 2 [py_exec Class2i.x]"
    puts "---"

    puts "\nFinished test $testName, exit code $error_code\n**********\n"
    logMessage logTest "TestCase: $testName $error_code\n"

    # This return is used by the framework!
    set error_code "FAIL"
    return $error_code
}

# Call the test !
# Must return one of the statuses:
# "pass", "fail", "skipped", "aborted", "not executed", "timeout", "invalid"
Test
