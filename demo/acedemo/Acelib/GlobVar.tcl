global testlib_error
set testlib_error 0

global testlib_error_info
foreach elem [array names testlib_error_info] {
   unset testlib_error_info($elem)
}

global MAXHISTORY
set MAXHISTORY 5

global coredump_err
set coredump_err 0
