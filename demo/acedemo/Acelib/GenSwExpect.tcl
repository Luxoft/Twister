###########################################################################
###########################################################################
#
# Procedures: 
#
#       GetSwitchSWVerNum_exp {host}
#       DelSwBuild {host {build all}}
#       ListFile {file host}
#       CDir {host dst_dir}
#       CopyFile {host src_file dst_file}
#       SwitchDelFile {file host}
#       ServiceCfgFtp {state host}
#       ServiceCfgTelnet {state host}
#       CesPing {host dstIp {srcIp ""}}
#       GetSoftwareVersion {host}
#       RetrieveSoftware {host ftpserver version path uid password {recurse YES}}
#       BootSystem {host version}
#       WaitForReboot {host {usr admin} {pass setup}}
#       Reload {host}
#       ReloadConfig {host config_file}
#       RemoveLicense {host feature}
#       InstallLicense {host feature key}
#       RestoreBasicCfg {host config_file ldap_file {usr "admin"} {pass "setup"}}
#       LoadLdap {host ldap_file}
#       SaveLdap { host ldap_file }
#       GetSwTime {host}
#       SetSwTime {host time month day year} 
############################################################################
############################################################################

############################################################################
#  Procedure GetSwitchSWVerNum_exp will return the switch running software #
#  version.                                                                #
#                                                                          #
#  Variables                                                               #
#    IN:                                                                   #
#         host:         IP address of the switch (or ip:port)              #
#                                                                          #
#    OUT:                                                                  #
#         Function returns the switch software version or "ERROR" if an    #
#         error occurred.                                                  #
#                                                                          #
#  Bugs:  None known.                                                      #
#                                                                          #
############################################################################

proc GetSwitchSWVerNum_exp {host} {

   global cmdOut

   SetCliLevel "PRIVILEGE" $host

#   Exec "\n" "USER" $host
   Exec "show version" "PRIVILEGE" $host
   
   if {[regexp -nocase {Software Version:[\ \t]*([VB][0-9]+_[0-9]+\.[0-9]+)} $cmdOut all swVer] == 1} {       
      return $swVer
   } else {
      #return [ErrCheck $cmdOut GetSwitchSWVerNum_exp]
      return "ERROR"
   }
}


############################################################################
#  Procedure DelSwBuild will delete a software version or all versions     #
#  from the CES                                                            #
#                                                                          #
#  Variables                                                               #
#    IN:                                                                   #
#         host:         IP address of the switch (or ip:port)              #
#         build:        build name; default is "all"; in this case the     #
#                       procedure will delete all builds from the switch   #
#                                                                          #
#    OUT:                                                                  #
#         procedure will return SUCCESS or ERROR                           #
#                                                                          #
#  Bugs:  None known.                                                      #
#                                                                          #
############################################################################

proc DelSwBuild {host {build all}} {

   global cmdOut
   set rcode ""

   if { [SetCliLevel "PRIVILEGE" $host] != "SUCCESS" } {
      lappend rcode "ERROR: Failed SetCliLevel"
      return [ErrCheck $rcode DelSwBuild] 
   }

   set execResult [Exec "ls" "PRIVILEGE" $host]

   if {$execResult != "SUCCESS"} {
      return "ERROR"
   }
   
   set lines [split $cmdOut "\n"]

   if {$build=="all"} {
      foreach line $lines {
         if {[regexp {[VB][0-9][0-9]_[0-9][0-9]\.[0-9][0-9][0-9]} $line build] ==1} {
            Exec "rmdir $build" "PRIVILEGE" $host 0 120
         }
      }
   } elseif {[regexp {[VB][0-9][0-9]_[0-9][0-9]\.[0-9][0-9][0-9]} $build] != 1} {
      lappend rcode "ERROR: \"$build\" is not a build directory!"
   } else  {      
      set cmdOut ""
      Exec "rmdir $build" "PRIVILEGE" $host 0 120
      if {[regexp {Directory does not exist:} $cmdOut msg] == 1} {
         lappend rcode "ERROR: \"$build\" directory does not exist!"            
      }
   }
   return [ErrCheck $rcode DelSwBuild]
}




########################################################################################
# ListFile - reads the content of <file> into a variable and returns this variable.
#
# Variables:
#   IN:
#           file:    absolute path and the name of the file you want to read
#           host     management IP address of the switch (or terminal server IP:port )
#
#   OUT: the content of the file 
#        ERROR                   - if a CLI command fails
#        ERRFILENOTEXIST         - if the file doesn't exists
#
########################################################################################
proc ListFile {file host} {
   global cmdOut

   if { [SetCliLevel "PRIVILEGE" $host] != "SUCCESS" } {
      lappend rcode "ERROR: Failed SetCliLevel"
      return [ErrCheck $rcode ListFile] 
   }
   
   set execResult [Exec "more $file" "PRIVILEGE" $host]
   if {$execResult != "SUCCESS"} {
      return "ERROR"
   }

   if {[regexp -nocase {file does not exist:} $cmdOut] == 1} {
      LogFile $cmdOut ERROR
      return "ERRFILENOTEXIST"
   }

   return $cmdOut
}


########################################################################################
# CDir - change directory.
#
# Variables:
#   IN:
#           host      management IP address of the switch (or terminal server IP:port )
#           dst_dir   destination directory
#
#   OUT: SUCCESS
#        ERROR        - if a CLI command fails
#        ERRDIR       - if the directory doesn't exists
#
########################################################################################
proc CDir {host dst_dir} {
   set err_count [GetGlobalErr]
   global cmdOut
   
   SetCliLevel "PRIVILEGE" $host
   Exec "cd $dst_dir" "PRIVILEGE" $host

   if {[regexp -nocase {Directory does not exist:} $cmdOut] == 1} {
      LogFile $cmdOut ERROR
      return "ERRDIR"
   }

   return [CheckGlobalErr $err_count]
}

########################################################################################
# CopyFile - copy a folder or a file.
#
# Variables:
#   IN:
#           src_file:  absolute/relative path and the name of the file you want to copy
#                      The file name shouldn't contain more than 8 characters.  
#           dst_file:  absolute/relative path and the name of the file where you want to copy
#           host       management IP address of the switch (or terminal server IP:port )
#
#   OUT: SUCCESS
#        ERROR           - if a CLI command fails
#        ERRCOPY         - if it is a error to copy file or directory
#
########################################################################################
proc CopyFile {host src_file dst_file} {
   set err_count [GetGlobalErr]
   global cmdOut
   
   SetCliLevel "PRIVILEGE" $host
   Exec "copy $src_file $dst_file" "PRIVILEGE" $host 0 90

   if {[regexp -nocase {No such file or directory:} $cmdOut] == 1 || \
           [regexp -nocase {Destination path is invalid:} $cmdOut] == 1 || \
           [regexp -nocase {Source and destination conflict:} $cmdOut] == 1 || \
           [regexp -nocase {The extenstion for the file name shouldn't contain more than 3 characters} $cmdOut] == 1 || \
           [regexp -nocase {The file name shouldn't contain more than 8 characters} $cmdOut] == 1} {
      LogFile $cmdOut ERROR
      return "ERRCOPY"
   }

   return [CheckGlobalErr $err_count]

}

##############################################
# switchDelFile - delete the file "file"
#
# Variables:
#   IN:      file:  absolute path and file name
#            host:  management IP address of the switch (or terminal server IP:port )
#
#   OUT:     SUCCESS or ERROR
#
##############################################
proc SwitchDelFile {file host} {
   if { [SetCliLevel "PRIVILEGE" $host] != "SUCCESS" } {
      lappend rcode "ERROR: Failed SetCliLevel"
      return [ErrCheck $rcode SwitchDelFile] 
   }
   
   return [Exec "delete $file" "PRIVILEGE" $host]
}


###################################################
# ServiceCfgFtp - configures FTP service on switch
#
# Variables:
#   IN:
#            state:    ftp-server state: enable/no_enable
#            host:     management IP address of the switch (or terminal server IP:port )
#
#   OUT:    
#            SUCCESS or ERROR
#
###################################################
proc ServiceCfgFtp {state host} {
   if { [SetCliLevel "CONFIG" $host] != "SUCCESS" } {
      lappend rcode "ERROR: Failed SetCliLevel"
      return [ErrCheck $rcode ServiceCfgFtp] 
   }

   switch $state {
      "enable" {
         return [Exec "ftp-server enable" "CONFIG" $host]
      }
      "no_enable" {
         return [Exec "no ftp-server enable" "CONFIG" $host]
      }        
   }    
}

##############################################
# ServiceCfgTelnet - configures telnet service on switch
#
# Variables:
#   IN:
#            state:    telnet-server state: enable/no_enable
#            host:     management IP address of the switch (or terminal server IP:port )
#
#   OUT:    
#            SUCCESS or ERROR
##############################################
proc ServiceCfgTelnet {state host} {
   if { [SetCliLevel "CONFIG" $host] != "SUCCESS" } {
      lappend rcode "ERROR: Failed SetCliLevel"
      return [ErrCheck $rcode ServiceCfgTelnet] 
   }

   switch $state {
      "enable" {
         return [Exec "telnet enable" "CONFIG" $host]
      }
      "no_enable" {
         return [Exec "no telnet enable" "CONFIG" $host]
      }        
   }    
}


##############################################
# CesPing - attempts to ping dstIp
#
# Variables:
#   IN:
#           host: management IP address of the switch (or terminal server IP:port )
#           dstIp: the IP address to ping
#           srcIp: - optional - the IP address from which to run ping          
#   OUT:
#           ERROR - if ping CLI command fails
#           ERRPING - if ping to dstIp fails
#           SUCCESS - if ping to dstIp successfull
#
##############################################
proc CesPing {host dstIp {srcIp ""}} {
   global cmdOut
   #//Try to ping dstIp from the srcIp.  
   SetCliLevel "PRIVILEGE" $host
   for {set i 1} {$i <= 5} {incr i} {
      if { [Exec "ping $dstIp $srcIp 5" "PRIVILEGE" $host] != "SUCCESS" } {
         return "ERROR"
      }
      set icmpCount 0
      foreach line [split $cmdOut "\n"] {
         if { [regexp "64 bytes from" $line] == 1 } {
            incr icmpCount
         }
      }
      if {$icmpCount == 5} {
         return "SUCCESS"
      }
      after 5000
   }
   return "ERRPING"
}

##############################################
# GetSoftwareVersion - gets software versions loaded on the CES
#
# Variables:
#   IN:
#           host: management IP address of the switch (or terminal server IP:port )
#                 
#   OUT:
#           a list with software versions loaded on the CES
#           ERROR
#
##############################################
proc GetSoftwareVersion {host} {
   global cmdOut

	set verList ""
   
   SetCliLevel "PRIVILEGE" $host

	if {[Exec "show software version" "PRIVILEGE" $host] != "SUCCESS" } {
		return "ERROR"
	}

	foreach line [split $cmdOut "\n"] {
		if {[regexp {[A-Z][0-9_\.]+} $line swVersion] == 1} {						
			lappend verList $swVersion
		}
	}

	return $verList

}

##############################################
# RetrieveSoftware - retrieves a software image for the switch
#
# Variables:
#   IN:
#           host: management IP address of the switch (or terminal server IP:port)
#           ftpserver: hostname or A.B.C.D  IP addr of the host remote server
#           version: software image file version
#           path: path to the directory where the software is stored
#           uid: user ID for the FTP server 
#           password: FTP server password
#           recurse: do it anyway if present; accepted values: YES, NO
#                 
#   OUT:
#           SUCCESS - if image is retrieved
#           ERROR - otherwise
#
##############################################
proc RetrieveSoftware {host ftpServer version path uid password {recurse YES}} {
   global cmdOut
	set rcode ""
   
   SetCliLevel "PRIVILEGE" $host

	if {$recurse == "YES"} {
		set errRetrieve [Exec "retrieve software $ftpServer version $version path $path uid $uid password $password recurse" \
                           "PRIVILEGE" $host 1 1800]
	} elseif {$recurse == "NO"} {
		set errRetrieve [Exec "retrieve software $ftpServer version $version path $path uid $uid password $password" \
                           "PRIVILEGE" $host 1 1800]
	}

	if {$errRetrieve != "SUCCESS"} {		
		return "ERROR"
	}

	if {[regexp -nocase {Success} $cmdOut] || \
           [regexp  -nocase "already installed" $cmdOut] || \
           [regexp  -nocase "already exists" $cmdOut]} {			
		return "SUCCESS"
	} else {
      #		LogFile "ERROR: RetrieveSoftware - fails to retrieve the software image: $version"
		return "ERROR"
	}	
}

##############################################
# BootSystem - Restarts the CES using specific loaded image
#
# Variables:
#   IN:
#           host: management serial connection IP:port
#           version: software image file version
#                 
#   OUT:
#           SUCCESS - if switch restarted successfuly with specified load image
#           ERROR - otherwise
#
##############################################
proc BootSystem {host version {user admin} {passwd setup}} {
   global cmdOut

	set rcode ""

   SetCliLevel "PRIVILEGE" $host
	
	Exec "boot system $version" "PRIVILEGE" $host "NO" 360	
	set err_code [Exec "y" "PRIVILEGE" $host "NO" 360]

   while {$err_code == "ANSWREQ"} {
      set err_code [Exec "y" "PRIVILEGE" $host "NO" 360]
	} 

   if {$err_code != "SUCCESS"} {	
		lappend rcode "ERROR: failed to reboot with software image $version"
		return [ErrCheck $rcode BootSystem]
	}	   

	if {[regexp -nocase {Please wait\. System will reboot\.} $cmdOut] == 1} {		
		if {[WaitForReboot $host] != "SUCCESS"} {
			lappend rcode "ERROR: failed to reboot with software image $version"
		}
      if {[GetSwitchSWVerNum_exp $host] != $version} {	
			lappend rcode "ERROR: failed to reboot with software image $version"					
		}
	} else {
		if {[GetSwitchSWVerNum_exp $host] != $version} {         
			lappend rcode "ERROR: failed to reboot with software image $version"					
		}
	}

	return [ErrCheck $rcode BootSystem]

}

#######################################
# WaitForReboot - If the CES is rebooting, waits to reboot and then enters to CLI.
#                 Otherwise, waits 10 seconds for reboot and if the switch is not rebooting after 
#                 this time, returns.
#
# IN:  host: management serial connection IP:port
#                 
# OUT: SUCCESS: if the switch rebooted successfuly or it is not forced to reboot
#      ERROR:   if the switch failed to reboot after 6 minutes
#######################################
proc WaitForReboot {host {usr admin} {pass setup}} {
   global spawn_id spawnId
	global timeout

   set rcode ""
   set spawn_id $spawnId($host)
   
	set loop_count 0

	set backTimeout $timeout
	set timeout 300

   exp_send "\r"
   expect {
      -re "\r\n\rCES.*\[>\#\\)\]$" {
         set prompt $expect_out(buffer)            
         incr loop_count
         if {$loop_count < 10} {
            sleep 3
            exp_send "\r"
            exp_continue				
         } else {
            set timeout $backTimeout
            return
         }
      }
      -re "Nortel Networks System Boot" {
         set timeout 360
         exp_continue
      }
      -re "Please enter the administrator's user name: " {
			set timeout 40
			exp_send -- "$usr\r"
			expect "Please enter the administrator's password: "
			exp_send -- "$pass\r"
			expect {
				-re "Please select a menu choice \\(\[01] - 9,B,P,C,L,R,E\\): " {										
				}                
				timeout {
					set timeout $backTimeout
					lappend rcode "ERROR: did not got the prompt: \"Please select a menu choice ((0 or 1) - 9,B,P,C,L,R,E): \""
					return [ErrCheck $rcode ResetSwitchFact]
				}
			}   
		}
		-re "Please enter the administrator's password: " {
			set timeout 40
			exp_send -- "\r"
			exp_continue
		}

      timeout {
			set timeout $backTimeout
			lappend rcode "ERR: did not match the prompt"
			return [ErrCheck $rcode WaitForReboot]
      }
   }		
	set timeout $backTimeout
	return [MainMenuToCli $host]
}

##########################################
# Reload: reboot the DUT using reload command.
#
#
#
##########################################
proc Reload {host {usr "admin"} {pass "setup"}} {

   set err_count [GetGlobalErr]
   
   SetCliLevel "PRIVILEGE" $host
   Exec "reload" "PRIVILEGE" $host

   set err_code [Exec "y" "PRIVILEGE" $host "NO" 360]		
   
   while {$err_code == "ANSWREQ"} {
      set err_code [Exec "y" "PRIVILEGE" $host "NO" 360]
   } 
   

   WaitForReboot $host $usr $pass

   return [CheckGlobalErr $err_count]

}


#############################################################
# ReloadConfig: Halt and perform a cold restart using the given
#               config file.
#
# IN:  host:        (management IP)/(terminal server Ip:port)
#      config_file: the config file to use at reboot
#
# OUT: SUCCESS/ERROR
#############################################################
proc ReloadConfig {host config_file {usr "admin"} {pass "setup"}} {

   global cmdOut

   set err_count [GetGlobalErr]
   
   SetCliLevel "PRIVILEGE" $host
   Exec "reload config-file $config_file" "PRIVILEGE" $host
   
   if {[regexp -nocase "Configuration file does not exist" $cmdOut] == 1} {
      ErrCheck "ERROR: Configuration file: $config_file -  does not exist"
      return [CheckGlobalErr $err_count]
   }
   
   set err_code [Exec "y" "PRIVILEGE" $host "NO" 360]		
   
   while {$err_code == "ANSWREQ"} {
      set err_code [Exec "y" "PRIVILEGE" $host "NO" 360]
   } 
   
   WaitForReboot $host $usr $pass

   return [CheckGlobalErr $err_count]
}

#############################################################
# InstallLicense: Install license key for a feature.
# 
# IN:  host:    (management IP)/(terminal server Ip:port)
#      feature: <ar/dw/fw>
#      key:     the license key string
#
# OUT: SUCCESS/ERROR
#############################################################
proc InstallLicense {host feature key} {
   set err_count [GetGlobalErr]   
   
   SetCliLevel "CONFIG" $host
   Exec "license install $feature $key" "CONFIG" $host   

   return [CheckGlobalErr $err_count]
}


#############################################################
# RemoveLicense: Removes license key for paid feature.
# 
# IN:  host:    (management IP)/(terminal server Ip:port)
#      feature: <ar/dw/fw>
#
# OUT: SUCCESS/ERROR
#############################################################
proc RemoveLicense {host feature} {

   global cmdOut   
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host   
   Exec "no license $feature" "CONFIG" $host

   if {[regexp {Contivity Statefull Firewall must be disabled before removing key} $cmdOut] == 1} {
      ErrCheck "{ERROR: Feature enabled. Cannot remove the license key}"
   }

   return [CheckGlobalErr $err_count]

}


#############################################################
# RestoreBasicCfg: Halt and perform a cold restart using the
#                    given configuration file, if exists. 
#                    Otherwise reset to factory defaults.
#                  After reboot, reload the given ldap file.
#                   
#                  Reload the given configuration and LDAB base.
#
# IN:  host:        (management IP)/(terminal server Ip:port)
#      config_file: the config file to use at reboot
#      ldap_file:   the ldap file to load.
#
# OUT: SUCCESS/ERROR
#      ERROR is return when neither CES reload nor CES reset to
#            factory defaults succeded, or ldap_file could not be 
#            loaded.
#############################################################
proc RestoreBasicCfg {host config_file ldap_file {usr "admin"} {pass "setup"}} {
   global cmdOut

   set err_count [GetGlobalErr]

   SetCliLevel "PRIVILEGE" $host
   Exec "reload config-file $config_file" "PRIVILEGE" $host
   
   if {[regexp -nocase "Configuration file does not exist" $cmdOut] == 1} {
      ResetSwitchFact $host $usr $pass
      
      LoadLdap $host $ldap_file

      return [CheckGlobalErr $err_count]
   }
   
   set err_code [Exec "y" "PRIVILEGE" $host "NO" 360]		
   
   while {$err_code == "ANSWREQ"} {
      set err_code [Exec "y" "PRIVILEGE" $host "NO" 360]
   } 
   
   WaitForReboot $host $usr $pass

   LoadLdap $host $ldap_file

   return [CheckGlobalErr $err_count]   
}


#############################################################
# LoadLdap: Loads a saved ldap file.
#
# IN:  host:        (management IP)/(terminal server Ip:port)
#      ldap_file:   ldap file to load.
#
# OUT: SUCCESS/ERROR
#############################################################
proc LoadLdap {host ldap_file} {

   global cmdOut

   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host

   Exec "ldap stop" "CONFIG" $host
   
   Exec "ldap import $ldap_file" "CONFIG" $host
   if {[regexp -nocase "Ldap file $ldap_file does not exist" $cmdOut] == 1} {
      ErrCheck "ERROR: Ldap file $ldap_file does not exist"
   }

   set count 1
   Exec "ldap start" "CONFIG" $host
   while {[regexp -nocase "Internal LDAP Server cannot be started while a restore is in progress" $cmdOut] == 1} {
      after 10000
      Exec "ldap start" "CONFIG" $host
      incr count
      
      if {$count > 1450} {
         ErrCheck "ERROR: Fail to restart LDAP server after 4 hours"
      }

   }
   

   return [CheckGlobalErr $err_count]

}


proc SaveLdap { host ldap_file } {
   
   global cmdOut
   
   set err_count [GetGlobalErr]
   
   SetCliLevel "CONFIG" $host

   Exec "ldap stop" "CONFIG" $host
   
   Exec "ldap export $ldap_file" "CONFIG" $host

   set count 1
   Exec "ldap start" "CONFIG" $host
   while {[regexp -nocase "Internal LDAP Server cannot be started while a restore is in progress" $cmdOut] == 1} {
      after 10000
      Exec "ldap start" "CONFIG" $host
      incr count
      
      if {$count > 1450} {
         ErrCheck "ERROR: Fail to restart LDAP server after 4 hours"
      }

   }
   
   return [CheckGlobalErr $err_count]
   
}


#############################################################
# GetSwTime: Gets switch's date and time
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#
# OUT: TIME/ERROR
#
#      Format TIME : hh:mm:ss GMT Day Month dd year
#           Example: 01:01:02 GMT Mon Feb 14 2004
#############################################################
proc GetSwTime {host} {

    global cmdOut
    
    SetCliLevel "PRIVILEGE" $host
    Exec "show clock" "PRIVILEGE" $host

    if {[regexp -nocase {[0-9]+:[0-9]+:[0-9]+.*[12][901][0-9][0-9]} $cmdOut all] == 1} {       
        return $all
    } else {
        #return [ErrCheck $cmdOut GetSwitchSWVerNum_exp]
        return "ERROR"
    }
}

#############################################################
# SetSwTime: Sets time.
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      time:    <hh:mm:ss> 
#      day:     <1-31> 
#      month:   MONTH  Month of the year
#      year:    <1970-2105>
#
# OUT: SUCCESS/ERROR
#############################################################
proc SetSwTime {host time month day year} {

    set err_count [GetGlobalErr]
    
    SetCliLevel "PRIVILEGE" $host
    set result ""
    set result [Exec "clock set $time $month $day  $year" "PRIVILEGE" $host]

    return [CheckGlobalErr $err_count]
}
  
