########################################################################
# Client Address Redistribution (CAR) library
#
#
#
########################################################################

proc EnterCarLevel {host} {

    set prompt "CES\\(config-car\\)\#"
    SetCliLevel "CONFIG" $host

    Exec "router car" $prompt $host
}

proc ExitCarLevel {host} {

    Exec "exit" "CONFIG" $host
}
