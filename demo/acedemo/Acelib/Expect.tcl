###################################################################
#  This file Expect.tcl implements procedures for comunicating with
#  a CES network device based on TCL/Expect package
#
# Connect {usr pass host}
# Disconnect { host }
# Exec { cmdStr cliLevel host {forceReturn 0} {timeOut 20} {sendReturn 1} }
# GetCliLevel { host }
# SetCliLevel { level host } 
#
# ########
# # CLI log is created based on expect program logs.
# # This is the reason why the procedures relating 
# # to CLI log are keept in this file.
# ########
# StartCLILog { {filename CLI.log} {logDir logs}}
# EndCliLog { fileID }
# logCliFile { msg }
#
####################################################################

#############
# Marius procs
#############

########
# Connect: opens a connection to switch and enters into CLI
#
# IN:  usr  - login username
#      pass - login password
#      host - <management Ip> or <terminal server Ip>:<port>
#
# OUT: SUCCESS - if management connection established
#      ERROR   - otherwise
########
proc Connect {usr pass host} {

    global spawn_id timeout spawnId spawnPid

	set rcode ""

    set backupTimeout $timeout
    set timeout 60

	if {[info exists spawnPid($host)] == 1} {
		catch {Disconnect $host}
		sleep 2
	}
    
    if { [regexp "(.*)(:)(.*)" $host all m1 m2 m3] == 1 } {
        set port $m3
        set ip $m1
    } else {
        set port 23
        set ip $host
    }

    set pid [spawn telnet $ip $port]

    match_max 100000

    set notConnected 0

    if { $port == 23 } {
        expect {
            -re "Login: " {
                exp_send -- "$usr\r"
                expect "Password: "
                exp_send -- "$pass\r"
                expect "CES>"
            }
            timeout {
                set notConnected 1
            }
            eof {
                set notConnected 1
            }
        }
        
    } else {
        exp_send -- "\r"
        expect {
            -re "CES>" {	
            }
            -re "CES\#" {
            }
            -re "CES\\(.*\\)\#" {
            }
            -re "Please enter the administrator's user name: " {
                exp_send -- "$usr\r"
                expect "Please enter the administrator's password: "
                exp_send -- "$pass\r"
                expect -re "Please select a menu choice \\(\[01] - 9,B,P,C,L,R,E\\): "
                exp_send -- "L\r"
                expect "CES>"
            }
            -re "Please enter the administrator's password: " {
                exp_send -- "\r"
                exp_continue
            }
            -re "Please select a menu choice \\(\[01] - 9,B,P,C,L,R,E\\): " {
                exp_send -- "L\r"
                expect "CES>"
            }
            -re "Please select a menu choice *\\(.*R\\): " {
                exp_send -- "R\r"
                exp_continue
            }
            -re "Please select a menu choice: " {
                exp_send -- "R\r"
                exp_continue                
            }
            timeout {
                set notConnected 1
            }
            eof {
                set notConnected 1
            }
        }
    }

    if {!$notConnected} {

        set spawnPid($host) $pid
        set spawnId($host)  $spawn_id
        SetCliLevel "USER" $host
        Exec "terminal paging off" "CES>" $host

    } else {
        #set timeout $backupTimeout
        set rcode ""
        #catch {exec kill -9 $pid}
		Disconnect $host
        lappend rcode "ERROR: connection failure"
        #return [ErrCheck $rcode Connect]
    }

    set timeout $backupTimeout

    #return $pid
	return [ErrCheck $rcode Connect]

}

########################################
# Exec - executes a CLI command on switch
#
# IN:  cmdStr:      cli command to execute
#      cliLevel:    CLI level at which to execute the command
#      host:        <management Ip> or <terminal server Ip>:<port> 
#      forceReturn: if "FORCERETURN" - force the calling procedure to return ERROR
#      timeOut:     the time to wait to match the prompt (default value: 20 ms)
#      sendReturn:  if 1 - send \r after sending CLI command to switch         
#
#
# OUT: SUCCESS - if after running the CLI command the expected prompt is matched
#      ERROR   - if CLI command does not exist or the expected prompt is not matched
#      ANSWREQ - if after running the CLI command an answer is required
#           
########################################
proc Exec { cmdStr cliLevel host {forceReturn 0} {timeOut 20} {sendReturn 1} } {

    global spawn_id timeout cmdOut spawnId spawnPid  

    # if catch coredump while running Exec, set coredump_err to 1
    global coredump_err

    set new_spawn_id $spawnId($host)
	
    ###############################
    # put messages in log files if command is executed on a different ces
    ###############################
    if {$new_spawn_id != $spawn_id} {
        
        set spawn_id $new_spawn_id
        logCliFile "\n---------------------------- ces: $host ----------------------------\n"
        puts "\n---------------------------- ces: $host ----------------------------\n"
    }

    switch $cliLevel {
        "USER"      { set expStr "CES>" }
        "PRIVILEGE" { set expStr "CES\#" }
        "CONFIG"    { set expStr "CES\\(config\\)\#" }
        "CONFIGIF"  { set expStr "CES\\(config-if\\)\#" }
        "GROUPCON"  { set expStr "CES\\(config-group/con\\)\#" }
        default     { set expStr $cliLevel }
    }

    regsub -all "\\\\" $expStr "" prompt

    set rcode ""
    set cmdOut ""   

    set timeoutBack $timeout
    set timeout $timeOut

    exp_send "$cmdStr"
    if { $sendReturn == 1 } {
        exp_send "\r"
    }
    set core_file ""
    expect {
        -- "\r${expStr}$" {
            #puts " -*- AceTest: Got the prompt -*- "  
            
			# - cip - include prompt in log message
            append cmdOut $prompt $expect_out(buffer)

            if {[regexp -nocase {Invalid input detected} $cmdOut ] == 1 || \
                    [regexp -nocase {Ambiguous command} $cmdOut ] == 1 || \
                    [regexp -nocase {Incomplete command} $cmdOut ] == 1} {
                
                lappend rcode "\n----------\nERROR: -- Invalid CLI command -- detected while running \"$cmdStr\"CLI command. \
                               \nces mesage:\n$cmdOut\n----------\n"
            }           
        }
        -- "--More--" {
            exp_send "\r"
            exp_continue
        }    

        -regexp {CoreDump Kernel Version} {
            set timeout 300
            LogFile " COREDUMP! "
            append cmdOut $expect_out(0,string)
            set coredump_err 1
            exp_continue
        }  
        
        -regexp {(?i)writing memory content [0-9a-fx]+ to [0-9a-fx]+ to ([0-9a-z/_\-]+(core[0-9]+\.gz))} {
            set core_file $expect_out(1,string)
            set rel_core_file $expect_out(2,string)
            exp_continue
        }  

        -regexp {CoreDump Kernel Task Completed.} {

            # - cip - include $prompt in log message
            append cmdOut $prompt $expect_out(buffer)

            lappend rcode "\n----------\nERROR: -- COREDUMP -- detected while running \"$cmdStr\" CLI command.\
                           \nces message:\n$cmdOut\n\----------\n"
            set coredump_err 1
        }

        -regexp {([a-zA-Z0-9\.\ ,]+\(.+\)\ *\?$)|([a-zA-Z0-9\.\ ,]+\?\ *[\[\(].+[\)\]][:\ ]*$)} {
            lappend rcode "ANSWREQ: This CLI command requires an answer !!!"            
        }

        timeout {
            lappend rcode "ERROR: Exec: timeout"
        }
    }
    set timeout $timeoutBack

    #get the calling procedures stack	
    # 	set calling_proc_stack ""
    # 	set level [expr [info level] -1]
    # 	while {$level > 0} {
    # 		lappend calling_proc_stack [info level -$level] /
    # 		incr level -1
    # 	}

    # get the name and arguments of proc which calls Exec 
    set calling_proc ""
    if {[info level] > 2} {
        set calling_proc [info level -1]
    }

    if {$calling_proc != ""} {
        set procInfo "\nExec - invoked from within: $calling_proc -"
    } else {
        set procInfo "Exec"
    }

    if {[regexp "ANSWREQ" $rcode] == 1 } {
        set timeout $timeoutBack
        return "ANSWREQ"
    }
    

    #//
    #// BAD LOG MESSAGES. NEED TO BE REVIEWED
    #//
    if {[regexp "COREDUMP" $rcode] == 1 } {

        LogFile " COREDUMP! \nThe CES is restarting..."

        set timeoutBack $timeout
        set timeout 420

        expect {
            -re "Please enter the administrator's user name: " {
                #Ace:splash "Wait!" 1000
                exp_send -- "admin\r"
                expect "Please enter the administrator's password: "
                exp_send -- "setup\r"
                expect -re "Please select a menu choice \\(\[01\] - 9,B,P,C,L,R,E\\): "
            }
            timeout {
                LogFile "The CES can't be contacted.\nYou must restart it manually!"
                lappend  rcode "\n\n-- The CES can't be contacted. You must restart it manually! --\n"
                ErrCheck $rcode ""
            }
        }

        if {$core_file != ""} {
            global logDir

            set core_dir "."
            if {[info global logDir] != "" && $logDir != ""} {
                if {[catch {file mkdir "${logDir}/CORE"} err ] == 0} {
                    set core_dir "${logDir}/CORE"
                }
            } else {
                if {[catch {file mkdir "CORE"} err ] == 0} {
                    set core_dir "CORE"
                }
            }
            
            set file_data [clock format [clock seconds] -format %Y_%m_%d_%H_%M_%S]
            set swVer [GetSwitchSWVerNum_exp $host]

            LogFile "Download Core file: $core_file to ${core_dir}/${swVer}__${file_data}_${rel_core_file} file"
            DownloadCesFile $host $core_file ${core_dir}/${swVer}__${host}__${file_data}_${rel_core_file}

        }
        LogFile $cmdStr COREDUMP
#         set timeout $timeoutBack
    }

    set timeout $timeoutBack

    set return_code [ErrCheck $rcode $procInfo]

    if {$forceReturn == "FORCERETURN" && $return_code != "SUCCESS"} { 
        return -code return [ErrCheck $rcode $procInfo]
    } else {
        return $return_code
    }

}


#################################
# Disconnect - closes the connection to host
#              LINUX:   uses system kill command
#              WINDOWS: uses close command from expect 
#
#
# IN:  host: <management Ip> or <terminal server Ip>:<port>
#
#
# OUT:    
#
# Bugs: using expect close command on Windows in order to close a 
#       spawned process is not the best choice.
#       This usualy terminates the process but sometimes can close 
#       the application that uses Disconnect
#################################
proc Disconnect { host } {
    global spawnId spawnPid
	global tcl_platform

	switch -regexp $tcl_platform(platform) {
		"windows" {
			puts "WINDOWS"
			if {$host != "all"} {
				catch {close $spawnId($host)}
				catch {wait -nowait}
				catch {unset spawnId($host)}
				catch {unset spawnPid($host)}    		
			}
			
			if {$host == "all"} {
				foreach elem [array names spawnPid] {					
					catch {close $spawnId($elem)}
					set msg [wait -i $spawnId($elem) -nowait]
					LogFile "Disconnect: $msg" debug
					catch {unset spawnId($elem)}
					catch {unset spawnPid($elem)}                        
				}
				#wait -nowait
			}
		}
		default {
			if {$host != "all"} {
				#catch {exec kill -9 $spawnPid($host)}
                catch {set spawn_id $spawnId($host)}
				catch {close}
				catch {wait}
				catch {unset spawnId($host)}
				catch {unset spawnPid($host)}    		
			}
			
			if {$host == "all"} {
				foreach elem [array names spawnId] {
                    catch {set spawn_id $spawnId($elem)}               					
					catch {close}
                    catch {wait}
                    # 					catch {exec kill -9 $spawnPid($elem)}
                    #              catch {exec kill -9 $spawnPid($elem)}
                    LogFile "Disconnect: spawnId($elem) == $spawnId($elem)" debug
                    #close $spawnId($elem)
                    #set msg [wait -i $spawnId($elem)]
					#LogFile "Disconnect: $msg" debug
					catch {unset spawnId($elem)}
					catch {unset spawnPid($elem)}                        
				}
				#wait -nowait
			}
		}
	}
}

#####################################################
# GetCliLevel: Returns information about the current CLI level.
#              If one of the three Cli levels:
#                 CES> (USER)
#                 CES# (PRIVILEGE)
#                 CES(config)# (CONFIG)
#              return USER/PRIVILEGE/CONFIG
#
#              If main menu: 
#              return MAINMENU
#
#              Else:
#              return UNKNOWN
#
# IN:  host: <management Ip> or <terminal server Ip>:<port>
#
# OUT: info about the current CLI level
#
#
#####################################################
proc GetCliLevel { host {usr "admin"} {pass "setup"}} {
    global spawn_id spawnId spawnPid

    set rcode ""
    set new_spawn_id $spawnId($host)

	###############################
	# put messages in log files if command is executed on a different ces
	###############################
	if {$new_spawn_id != $spawn_id} {

		set spawn_id $new_spawn_id
		logCliFile "\n---------------------------- ces: $host ----------------------------\n"
		puts "\n---------------------------- ces: $host ----------------------------\n"
	}	

    
    exp_send "\r"
    expect {
        -re "\r\n\r\CES.*\[>\#\\)\]$" {
            set prompt $expect_out(buffer)            
        }
        -re "Please select a menu choice \\(\[01] - 9,B,P,C,L,R,E\\): " {
            set prompt "MAINMENU"
        }
        -re "Please enter the administrator's user name: " {
            exp_send -- "$usr\r"
            expect "Please enter the administrator's password: "
            exp_send -- "$pass\r"
            expect -re "Please select a menu choice \\(\[01] - 9,B,P,C,L,R,E\\): "
            set prompt "MAINMENU"
        }
        -re "Please enter the administrator's password: " {
            exp_send -- "\r"
            exp_continue
        }
        timeout {
            #lappend rcode "Exec: timeout"
            lappend rcode "ERR: did not match the prompt"
            return [ErrCheck $rcode GetCliLevel]
        }
    }

    if { [regexp "CES>" $prompt] == 1 } {
        return "USER"
    } elseif { [regexp "CES\#" $prompt] == 1 } {
        return "PRIVILEGE"
    } elseif { [regexp "CES\\(config\\)\#" $prompt] == 1 } {
        return "CONFIG"
    } elseif {$prompt == "MAINMENU"} {
        return "MAINMENU"
    }  else {
        return "UNKNOWN"
    }
}

#########################
# SetCliLevel: Procedure used to navigate from any CLI level or from
#              Main Menu back to one of three main CLI levels:
#                 CES> (USER)
#                 CES# (PRIVILEGE)
#                 CES(config)# (CONFIG)                 
#              
#              For each other speciffic CLI level (e.g. Branch Office, fast ethernet interface ...)
#              Acelib should contain a speciffic procedure to enter in this CLI level.
#              SetCliLevel doesn't handle this case.
#
# IN:  level: the CLI level you want to enter (must be one of USER/PRIVILEGE/CONFIG)
#      host:  <management Ip> or <terminal server Ip>:<port>
#
# OUT: SUCCESS: if expected prompt
#      ERROR    otherwise
# 
##########################
proc SetCliLevel { level host } {
    global cmdOut
    global spawnId spawnPid spawn_id

	set rcode ""
    set cmdOut ""
    #append cmdOut $prompt $expect_out(buffer)

    set currLevel [GetCliLevel $host]
    
    if {$currLevel == "MAINMENU"} {
        MainMenuToCli $host
        set currLevel [GetCliLevel $host]
    } elseif {$currLevel == "UNKNOWN"} {
        exp_send "exit\n"
        expect {
            -re "CES\\(config\\)\#" {
                append cmdOut "CES\\(config\\)\#" $expect_out(buffer)
                set currLevel [GetCliLevel $host]            
            }
            -re "CES\\(?.*\\)?\#" {
                exp_send "exit\r"
                exp_continue
            }                
            timeout {
                lappend rcode "ERROR: unknown cli level"
                return [ErrCheck $rcode SetCliLevel]
            }
        }
    }

    switch $level {
        "USER" {
            if { $currLevel == "PRIVILEGE" } {
                Exec "exit" "USER" $host                
            } elseif { $currLevel == "CONFIG" } {
                Exec "exit" "PRIVILEGE" $host
                Exec "exit" "USER" $host
            }
            if { [GetCliLevel $host] == "USER" } {
                return [ErrCheck $rcode SetCliLevel]
            } else {
                return [ErrCheck $rcode SetCliLevel]
            }
        }
        "PRIVILEGE" {
            if { $currLevel == "USER" } {
                Exec "enable" "Password: " $host
                Exec "setup" "PRIVILEGE" $host
            } elseif { $currLevel == "CONFIG" } {
                Exec "exit" "PRIVILEGE" $host
            }
            if { [GetCliLevel $host] == "PRIVILEGE" } {
                return [ErrCheck $rcode SetCliLevel]
            } else {
                return [ErrCheck $rcode SetCliLevel]
            }
        }
        "CONFIG" {
            if { $currLevel == "USER" } {
                Exec "enable" "Password: " $host
                Exec "setup" "PRIVILEGE" $host
                Exec "configure terminal" "CONFIG" $host
            }
            if { $currLevel == "PRIVILEGE" } {
                Exec "configure terminal" "CONFIG" $host
            }
            if { [GetCliLevel $host] == "CONFIG" } {
                return [ErrCheck $rcode SetCliLevel]
            } else {
                return [ErrCheck $rcode SetCliLevel]
            }
        }        
    }
}






#############################
# CLI log procedures
#############################

###############################
# StartCLILog - starts expect logging into $logs/$filename file
#
#
###############################
proc StartCLILog { {filename CLI.log} {logDir logs}} {

    #stop previous logging
    catch { log_file }

    #catch {log_file -open $cliLogId}
    catch {log_file ${logDir}/${filename}}
    
}

################################
# logCliFile - displays the message and also adds it in CLI LOG file
#
#
################################
proc logCliFile { msg } {

    #puts "$msg"
    send_log "$msg"

}

#################################
# EndCliLog - stops expect logging
#
# fileID parameter is not used anymore. It is keept just for backwards compatibility.
# Procedure should be called in the scripts without any parameter.
#
#################################
proc EndCliLog { {fileID ""} } {

    #stop logging - this will also close the logging files
    catch { log_file }

}
