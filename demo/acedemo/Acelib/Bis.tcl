########################################################################
# Backup Interface Services (BIS) library
#
#
#
########################################################################

proc EnterBisLevel {ifName host} {

    set prompt "CES\\(config-bis\\)\#"
    SetCliLevel "CONFIG" $host
        
    Exec "bis $ifName" $prompt $host
}

proc ExitBisLevel { host} {
    Exec "exit" "CONFIG" $host
}
