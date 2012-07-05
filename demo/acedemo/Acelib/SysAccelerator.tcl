##############################
# Procedures relating to System Accelerator
#
# VerifySysAccelerator { host }
#
#############################


proc VerifySysAccelerator { host } {

    global spawn_id timeout mdOut spawnId spawnPid    

    set spawn_id $spawnId($host)
   
    set timeout 10

    set rcode ""
    set cmdOut ""
 
    SetCliLevel "PRIVILEGE" $host

    exp_send "show system accelerator\r"
    expect {
        -- "\rCES\#$" {           
            set cmdOut $expect_out(buffer)
            if {[regexp -nocase {Invalid input detected} $cmdOut ] == 1} {
                return "NONE"       
            }
        } 
        timeout {
            return "ERROR"
        }

    }

    set deviceNumbers ""
    foreach line [ split $cmdOut "\n" ] {
        if {[regexp -nocase "\[\t\ \]+Device\[\t\ \]+:\[\t\ \]*\(\[0-9\]\)+" $line all devNo] == 1} {
            lappend deviceNumbers $devNo
        }
    }
    return $deviceNumbers
}

#############################################################
# ShowSysAccelerator: shows sistem accelerator
#
# IN:  
#      host:          (management IP)/(terminal server Ip:port)
#      device_number: device number (0,1,2)
#      show_type:        <detail/statistics>
#
# OUT: NONE/ERROR/output
#############################################################
proc ShowSysAccelerator {host {device_number ""} {show_type ""}} {

    global cmdOut 

    set rcode ""
    set cmdOut ""
 
    SetCliLevel "PRIVILEGE" $host

    if {[Exec "show system accelerator $device_number $show_type" "PRIVILEGE" $host] != "SUCCESS"} {
        return "ERROR"
    }
    if {[regexp -nocase {Invalid input detected} $cmdOut ] == 1} {
        return "NONE"
    } else {
        return $cmdOut
    }
    
}


#############################################################
# StatusSysAccelerator: sets sistem accelerator status
#
# IN:  
#      host:        (management IP)/(terminal server Ip:port)
#      device_no:   device number (0,1,2)
#      status:      <enable/disable>
#
# OUT: SUCCESS/ERROR
#############################################################
proc StatusSysAccelerator {host device_no status} {

    set err_count [GetGlobalErr]

    SetCliLevel "CONFIG" $host

    if {[Exec "system accelerator $device_no $status" "CONFIG" $host] != "SUCCESS"} {
        return "ERROR"
    }
    
    return [CheckGlobalErr $err_count]
}

#############################################################
# ShowSysAccSessions: Shows current encode sessions for current SA
#
# IN:  
#      host:        (management IP)/(terminal server Ip:port)
#      device_no:   device number (0,1,2)
#
# OUT: SUCCESS/ERROR
#############################################################
proc ShowSysAccSessions {host device_no} {

    global cmdOut 

    set cmdOut ""
 
    SetCliLevel "PRIVILEGE" $host

    if {[Exec "show system accelerator $device_no statistics" "PRIVILEGE" $host] != "SUCCESS"} {
        return "ERROR"
    }

    set sessionsNo ""
    foreach line [ split $cmdOut "\n" ] {
        if {[regexp -nocase "\[\t\ \]+Current encode sessions\[\t\ \]*:\[\t\ \]*\(\[0-9\]+\)" $line all sessionsNo] == 1} {
            return $sessionsNo
        }
    }
}


#############################################################
# SetStatusSysAcc: Enables/Disables SA
#
# IN:  
#      host:      (management IP)/(terminal server Ip:port)
#      device_no: device number (0,1,2)
#      status:    enable/disable  
#
# OUT: SUCCESS/ERROR
#############################################################
proc SetStatusSysAcc {host device_no status} {

    global cmdOut 
    SetCliLevel "CONFIG" $host

    if { $status == "enable" } {
        return [Exec "system accelerator $device_no enable" "CONFIG" $host 0 60]
    } elseif { $status == "disable"} {
        return [Exec "no system accelerator $device_no enable" "CONFIG" $host 0 60]
    } else {
        return [ErrCheck "the status parameter must be \"enable\" or \"disable\", not \"$status\"" "SetStatusSysAcc"]
    }
}

#############################################################
# SetAutoRecoverySysAcc: Enables/Disables auto-recovery for SA
#
# IN:  
#      host:      (management IP)/(terminal server Ip:port)
#      device_no: device number (0,1,2)
#      status:    enable/disable  
#
# OUT: SUCCESS/ERROR
#############################################################
proc SetAutoRecoverySysAcc {host device_no status} {

    global cmdOut 
    SetCliLevel "CONFIG" $host

    if { $status == "enable" } {
        return [Exec "system accelerator $device_no auto-recovery enable" "CONFIG" $host]
    } elseif { $status == "disable"} {
        return [Exec "no system accelerator $device_no auto-recovery enable" "CONFIG" $host]
    } else {
        return [ErrCheck "the status parameter must be \"enable\" or \"disable\", not \"$status\"" "SetAutoRecoverySysAcc"]
    }
}
