###########################################################################################
# This file ExpectZebra.tcl implements procedures for comunicating with a Zebra network device
# based on TCL/Expect package
#
# ConnectZebra
# ExecZebra
# GetZebraCliLevel
# GetZebraConnState
# SetZebraCliLevel
#
###########################################################################################

########
# opens a connection to switch and enters in CLI
########

proc ConnectZebra { prompt pass host } {

    global spawn_id timeout spawnId spawnPid

    set backupTimeout $timeout
    set timeout 30

    if {[info exists spawnPid($host)] == 1} {
        catch {Disconnect $host}
        sleep 2
    }

    if { [regexp "(.*)(:)(.*)" $host all m1 m2 m3] == 1 } {
        set port $m3
        set ip $m1
    } else {
        set rcode "ERR: bad host parameter format; must be IP:port"
        return [ErrCheck $rcode ConnectZebra]
    }
    
    #exp_internal 1

    set pid [spawn telnet $ip $port]

    match_max 100000

    set notConnected 1

    expect {
        -re "Password: " {
            exp_send -- "$pass\r"
            expect {
                -re  "$prompt> " {
                    set notConnected 0
                }
            }
        }
    }

    if {$notConnected == 0} {

        set spawnPid($host) $pid
        set spawnId($host)  $spawn_id
        #SetCliLevel "USER" $host

    } else {
        set timeout $backupTimeout
        set rcode ""
        Disconnect $host
        lappend rcode "ERROR: connection failure"
        return [ErrCheck $rcode ConnectZebra]
    }

    set timeout $backupTimeout

    return $pid
}



proc ExecZebra { prompt cmdStr cliLevel host {sendReturn 1} {timeOut 20} {infCallingProc YES} {errMsg YES} } {
    global spawn_id timeout cmdOut spawnId spawnPid
    
    set new_spawn_id $spawnId($host)
    
    ###############################
    # put messages in log files if command is executed on a different ces
    ###############################
    if {$new_spawn_id != $spawn_id} {

        set spawn_id $new_spawn_id
        logCliFile "\n---------------------------- ces: $host ----------------------------\n"
    }

    switch $cliLevel {
        "USER"      { set expStr "$prompt> " }
        "PRIVILEGE" { set expStr "$prompt\# " }
        "CONFIG"    { set expStr "$prompt\\(config\\)\# " }
        "CONFIGIF"  { set expStr "$prompt\\(config-if\\)\# " }
        "CONFIGROUTER"  { set expStr "$prompt\\(config-router\\)\# " }
        default     { set expStr $cliLevel }
    }

    set rcode ""
    set cmdOut ""
    
    set timeoutBack $timeout
    set timeout $timeOut

    exp_send "$cmdStr"
    if { $sendReturn == 1 } {
        exp_send "\r"
    }
    expect {
        -- "${expStr}$" {
            #puts " -*- AceTest: Got the prompt -*- "            
            set cmdOut $expect_out(buffer)
            if {[regexp -nocase {Unknown command.} $cmdOut ] == 1 || \
                    [regexp -nocase {Ambiguous command.} $cmdOut ] == 1  || \
                    [regexp -nocase {Command incomplete.} $cmdOut ] == 1} {
                if {[string match -nocase "yes" $errMsg] == 1} {
                    lappend rcode "ERROR: Invalid CLI command for $prompt: $cmdStr\n----\n$cmdOut\n----"
                } else {
                    lappend rcode "Invalid CLI command for $prompt: $cmdStr\n----\n$cmdOut\n----"
                }

            }
        }
        -- "--More-- " {
            exp_send "\n"
            exp_continue
        }    

        -regexp {[a-zA-z0-9\.\ ,]+\(.+\)\?$} {
            lappend rcode "ANSWREQ: This CLI command requires an answer !!!"            
        } 

        timeout {
            lappend rcode "ERROR: ExecZebra: timeout"
        }
    }
    set timeout $timeoutBack

    #get the calling procedure name
    set callingProc [info level -1]
    if {$callingProc != "" && [string match -nocase YES $infCallingProc] == 1} {
        set procInfo "ExecZebra call from $callingProc procedure"
    } else {
        procInfo "ExecZebra"
    }

    if {[regexp "ANSWREQ" $rcode] == 1 } {
        return "ANSWREQ"
    }

    return [ErrCheck $rcode $procInfo]
}

proc GetZebraCliLevel {prompt  host} {
    global spawn_id spawnId spawnPid

    set rcode ""
    set new_spawn_id $spawnId($host)

    ###############################
    # put messages in log files if command is executed on a different ces
    ###############################
    if {$new_spawn_id != $spawn_id} {

        set spawn_id $new_spawn_id
        logCliFile "\n---------------------------- ces: $host ----------------------------\n"
    }
    
    #   exp_internal 1

    exp_send "\n"
    expect {
        -re "\r\n.+\[>\#\\)\] $" {
            set cli_prompt $expect_out(buffer)            
        }
        timeout {
            lappend rcode "ERR: did not match the prompt"
            return [ErrCheck $rcode GetZebraCliLevel]
        }
    }

    if { [regexp "$prompt> " $cli_prompt] == 1 } {
        return "USER"
    } elseif { [regexp "$prompt\# " $cli_prompt] == 1 } {
        return "PRIVILEGE"
    } elseif { [regexp "$prompt\\(config\\)\# " $cli_prompt] == 1 } {
        return "CONFIG"
    } else {
        return "UNKNOWN"
    }
}

#########################
# Supported levels:
# - USER
# - PRIVILEGE
# - CONFIG
#
# Regardless of the CLI level or MainMenu menu you are at the moment you call this proc it will exit from this level and 
# will enter in the level passed as parameter.
# 
##########################
proc SetZebraCliLevel { prompt level host } {
    global spawnId spawnPid spawn_id

    #    set spawn_id $spawnId($host)
    set currLevel [GetZebraCliLevel $prompt $host]
    
    # exp_internal 1

    if {$currLevel == "UNKNOWN"} {
        exp_send "end\n"
        expect {
            -re "$prompt\# " {
                set currLevel "PRIVILEGE"
            }              
            timeout {
                lappend rcode "ERROR: unknown zebra cli level"
                return [ErrCheck $rcode SetZebraCliLevel]
            }
        }
    }
    

    switch $level {
        "USER" {
            if { $currLevel == "PRIVILEGE" } {
                ExecZebra $prompt "disable" "USER" $host                
            } elseif { $currLevel == "CONFIG" } {
                ExecZebra $prompt "end" "PRIVILEGE" $host
                ExecZebra $prompt "disable" "USER" $host
            }
            if { [GetZebraCliLevel $prompt $host] == "USER" } {
                return 1
            } else {
                return 0
            }
        }
        "PRIVILEGE" {
            if { $currLevel == "USER" } {
                ExecZebra $prompt "enable" "PRIVILEGE" $host
            } elseif { $currLevel == "CONFIG" } {
                ExecZebra $prompt "end" "PRIVILEGE" $host
            }
            if { [GetZebraCliLevel $prompt $host] == "PRIVILEGE" } {
                return 1
            } else {
                return 0
            }
        }
        "CONFIG" {
            if { $currLevel == "USER" } {
                ExecZebra $prompt "enable" "PRIVILEGE" $host
                ExecZebra $prompt "configure terminal" "CONFIG" $host
            }
            if { $currLevel == "PRIVILEGE" } {
                ExecZebra $prompt "configure terminal" "CONFIG" $host
            }
            if { [GetZebraCliLevel $prompt $host] == "CONFIG" } {
                return 1
            } else {
                return 0
            }
        }        
    }
}
