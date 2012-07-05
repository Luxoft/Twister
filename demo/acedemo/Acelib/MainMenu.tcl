###########################################################################################
# This file mainmenu.tcl implements procedures for comunicating with a CES network device
# based on TCL/Expect package
#  
# NOTE: - all the procedures starting with     "mm_"     can be used only from Main Menu;
#         other procedured that can be used only from Main Menu:
#               MainMenuToCli
#               BackToMainMenu
#
#       
#
# ----- public procedures ----- 
# ResetSwitchFact {host {usr "admin"} {pass "setup"}}
# ExitSaveInvoke { host {usr "admin"} {pass "setup"} }
# # OBSOLATED: SetPrivInterface { host managementIp interfaceIp {interfaceID 0} {mask "255.255.255.0"}}
# # use instead
# SetMngInterface { host managementIp interfaceIp {interfaceID 0} {mask "255.255.255.0"}}
# SetPublicInterface { host interfaceIp {interfaceID 1} {mask "255.255.255.0"}} {
# GetInterface { host }
# RestartSwitch { host {usr "admin"} {pass "setup"}}
# SetPublicDefaultGw { host gw {gwId "new"} {cost 10}}
# SetPrivateDefaultGw { host gw {gwId "new"} {cost 10}}
#
# ----- Main Menu procedures -used by public procedures ------
# CliToMainMenu {host}
# MainMenuToCli {host}
# BackToMainMenu { host {safeCount 10}}
#
# mm_ResetSwitchFact {host {usr "admin"} {pass "setup"}}
# mm_ExitSaveInvoke { host {usr "admin"} {pass "setup"} }
# # OBSOLATED: mm_SetPrivInterface { host managementIp interfaceIp {interfaceID 0} {mask "255.255.255.0"}}
# # use instead
# mm_SetMngInterface { host managementIp interfaceIp {interfaceID 0} {mask "255.255.255.0"}}
# mm_SetPublicInterface { host interfaceIp {interfaceID 1} {mask "255.255.255.0"}}
# mm_GetInterface { host }
# mm_RestartSwitch { host }
# mm_SetPublicDefaultGw { host gw gwId cost}
# mm_SetPrivateDefaultGw { host gw gwId cost}
#
###########################################################################################
#
# MultiResetSwitchFact { hosts {usr "admin"} {pass "setup"} }
# MultiReload { hosts {usr "admin"} {pass "setup"} }
# MultiRetrieve { hosts server version path ftp_uid ftp_pass {recurse "YES"} {usr "admin"} {pass "setup"} }
# MultiBoot { hosts version {usr "admin"} {pass "setup"} }
###########################################################################################




################################################################
# ResetSwitchFact - go to Main Menu resets the switch to factory defaults using Main Menu options and then enter again to CLI
#
# !WARNING - call this procedure only from CLI (any CLI level)
#
# Variables:
#
#   OUT: 
#          SUCCESS or ERROR
# 
################################################################
proc ResetSwitchFact {host {usr "admin"} {pass "setup"}} {
   
   set errCode "ERROR"
   set errCount 0
   
   if {[CliToMainMenu $host] == "SUCCESS"} {    
      if {[mm_ResetSwitchFact $host $usr $pass] != "SUCCESS"} {
         incr errCount
      } 

      if {[MainMenuToCli $host] != "SUCCESS"} {
         incr errCount
      }
      if {$errCount == 0} {
         set errCode "SUCCESS"
      }
   }

   return $errCode
}

##############################################################
# ExitSaveInvoke
#
# !WARNING - call this procedure only from CLI (any CLI level)
# It will go to Main Menu, will Exit Save Invoke changes and then will enter again into CLI
#
# Variables:
#
#   OUT: 
#          SUCCESS or ERROR
#
##############################################################
proc ExitSaveInvoke { host {usr "admin"} {pass "setup"} } {
   set errCode "ERROR"
   set errCount 0
   
   if {[CliToMainMenu $host] == "SUCCESS"} {    
      if {[mm_ExitSaveInvoke $host $usr $pass] != "SUCCESS"} {
         incr errCount
      }
      if {[MainMenuToCli $host] != "SUCCESS"} {
         incr errCount
      }
      if {$errCount == 0} {
         set errCode "SUCCESS"
      }
   }

   return $errCode
}


###############################################################
# SetMngInterface - enters to main menu, configures a private interface using Main Menu options and enters back to CLI
#
# !WARNING - call this procedure only from CLI (any CLI level)
# 
# Variables:
#
#   OUT: 
#          SUCCESS or ERROR
#
###############################################################
proc SetMngInterface { host managementIp {interfaceIp ""} {interfaceID 0} {mask "255.255.255.0"}} {
    SetPrivInterface $host $managementIp $interfaceIp $interfaceID $mask
}


###############################################################
# SetPrivInterface - enters to main menu, configures a private interface using Main Menu options and enters back to CLI
#
# !WARNING - call this procedure only from CLI (any CLI level)
# 
# Variables:
#
#   OUT: 
#          SUCCESS or ERROR
#
###############################################################
proc SetPrivInterface { host managementIp interfaceIp {interfaceID 0} {mask "255.255.255.0"}} {
    set errCode "ERROR"
    set errCount 0
   
    if {[CliToMainMenu $host] == "SUCCESS"} {
        if {[Get_MM_Type $host] == "old_mm_type"} {
            if {[mm_SetPrivInterface $host $managementIp $interfaceIp $interfaceID $mask] != "SUCCESS"} {
            }
        } else {
            if {[mm_new_SetMngInterface $host $managementIp] != "SUCCESS"} {
                incr errCount
            }
        }
        if {[MainMenuToCli $host] != "SUCCESS"} {
            incr errCount
        }
        if {$errCount == 0} {
            set errCode "SUCCESS"
        }
    }   
    return $errCode    
}

###############################################################
# SetPublicInterface - enters to main menu, configures a public interface using Main Menu options and enters back to CLI
#
# !WARNING - call this procedure only from CLI (any CLI level)
# 
# Variables:
#
#   OUT: 
#          SUCCESS or ERROR
#
###############################################################
proc SetPublicInterface { host interfaceIp {interfaceID 1} {mask "255.255.255.0"}} {
   set errCode "ERROR"
   set errCount 0
   
   if {[CliToMainMenu $host] == "SUCCESS"} {    
      if {[mm_SetPublicInterface $host $interfaceIp $interfaceID $mask] != "SUCCESS"} {
         incr errCount
      }
      if {[MainMenuToCli $host] != "SUCCESS"} {
         incr errCount
      }
      if {$errCount == 0} {
         set errCode "SUCCESS"
      }
   }

   return $errCode    
}

###############################################################
# GetInterface - enters to main menu from CLI, displas the interfaces and goes back to CLI
#
# !WARNING - call this procedure only from CLI (any CLI level)
# 
# Variables:
#
#   IN:    host = the DUT IP address (or ip_address:port) 
#
#   OUT: 
#          SUCCESS or ERROR
#
###############################################################
proc GetInterface { host } {
   set errCode "ERROR"
   set errCount 0
   
   if {[CliToMainMenu $host] == "SUCCESS"} {    
      if {[mm_GetInterface $host] != "SUCCESS"} {
         incr errCount
      }
      if {[MainMenuToCli $host] != "SUCCESS"} {
         incr errCount
      }
      if {$errCount == 0} {
         set errCode "SUCCESS"
      }
   }

   return $errCode    
}


##############################################################
# RestartSwitch - enters in Main Menu (from CLI) and restarts the Box.
# 
# !WARNING - call this procedure only from CLI (any CLI level)
#
#   IN:    host = the DUT IP address (or ip_address:port) 
#
#   OUT: 
#          SUCCESS or ERROR
##############################################################
proc RestartSwitch { host {usr "admin"} {pass "setup"}} {
   set errCode "ERROR"
   set errCount 0
   
   if {[CliToMainMenu $host] == "SUCCESS"} {    
      if {[mm_RestartSwitch $host $usr $pass] != "SUCCESS"} {
         incr errCount
      }
      if {[MainMenuToCli $host] != "SUCCESS"} {            
         incr errCount            
      }
      if {$errCount == 0} {
         set errCode "SUCCESS"
      }
   }

   return $errCode

}

proc SetPublicDefaultGw { host gw {gwId "new"} {cost 10}} {
   set errCode "ERROR"
   set errCount 0
   
   if {[CliToMainMenu $host] == "SUCCESS"} {    
      if {[mm_SetPublicDefaultGw $host $gw $gwId $cost] != "SUCCESS"} {
         incr errCount
      }
      if {[MainMenuToCli $host] != "SUCCESS"} {            
         incr errCount            
      }
      if {$errCount == 0} {
         set errCode "SUCCESS"
      }
   }

   return $errCode

}

proc SetPrivateDefaultGw { host gw {gwId "new"} {cost 10}} {
   set errCode "ERROR"
   set errCount 0
   
   if {[CliToMainMenu $host] == "SUCCESS"} {    
      if {[mm_SetPrivateDefaultGw $host $gw $gwId $cost] != "SUCCESS"} {
         incr errCount
      }
      if {[MainMenuToCli $host] != "SUCCESS"} {            
         incr errCount            
      }
      if {$errCount == 0} {
         set errCode "SUCCESS"
      }
   }

   return $errCode

}

##########################################################################################################################################
###
# Main Menu procedures
###

#############
# Exits from CLI level and gets back in Main Menu 
#
# Ensure that you are in CLI level before calling this proc
#
#############
proc CliToMainMenu {host} {
   global spawnId spawnPid spawn_id

   global timeout

   set rcode ""

   ###############################
   # put messages in log files if command is executed on a different CES
   ###############################
   if {$spawnId($host) != $spawn_id} {
      
      logCliFile "\n---------------------------- ces: $host ----------------------------\n"
      puts "\n---------------------------- ces: $host ----------------------------\n"
   }

   set spawn_id $spawnId($host)

   #//ensure that curent CLI level = USER
   if {[GetCliLevel $host] != "USER"} {
      if {[SetCliLevel "USER" $host] != "SUCCESS"} {
         lappend rcode "ERROR: fail to set CLI level: USER"
         return [ErrCheck $rcode CliToMainMenu]
      }
   }
   
   set timeoutBack $timeout
   set timeout 30
   
   #//move to mai menu
   exp_send "exit\r"
   expect {
      -re "Please select a menu choice \\(\[01] - 9,B,P,C,L,R,E\\): " {
         set prompt $expect_out(buffer)  
         return "SUCCESS"
      }
      timeout {
         set timeout $timeoutBack
         lappend rcode "ERROR: exit CLI - timeout"
         return [ErrCheck $rcode CliToMainMenu]
      }
   }           

}; #end CliToMainMenu



#################################################
# MainMenuToCli - enters to CLI from Main Menu
#                 When the switch is restarted, the first attempts to enter to CLI mai fail because 
#                 the DUT may not be fully initialized.
#                 For cases like that, the procedure will make up to five attempts to enter to CLI. 
#                 It returns SUCCESS at the first successfull attempt to enter to CLI
# VARIABLES:
#     IN:  host  - the IP address of the DUT (or IP:Port)
#
#    OUT:  SUCCESS
#          ERROR
#
#################################################
proc MainMenuToCli {host} {
   global spawnId spawnPid spawn_id 

   set rcode ""

   set spawn_id $spawnId($host)    

   for {set i 1} {$i <= 5} {incr i} {
      set MainMenuToCliRoutineResult [MainMenuToCliRoutine $host]
      if {$MainMenuToCliRoutineResult == "ERROR"} {
         return "ERROR"
      } elseif {$MainMenuToCliRoutineResult == "SUCCESS"} {
         return "SUCCESS"
      }
   }

   lappend rcode "ERR: fail to enter to CLI (L Main Menu option)"
   return [ErrCheck $rcode MainMenuToCli]

}; #end MainMenuToCli


#############################################
# MainMenuToCliRoutine - used by MainMenuToCli proc to enter to CLI from Main Menu
# 
# VARIABLES:
#     IN: host - the DUT IP address (or IP:Port)
#
#    OUT: SUCCESS
#         ERROR
#         ERRTIMEOUT
#
#############################################
proc MainMenuToCliRoutine { host } {
   global timeout

   set timeoutBack $timeout
   set timeout 30

   exp_send -- "L\r"
   expect { 
      "CES>" {
         set prompt $expect_out(buffer)
         if {[Exec "terminal paging off" "CES>" $host 0 $timeout] != "SUCCESS"} {
            set timeout $timeoutBack
            return "ERROR"
         } else {         
            set timeout $timeoutBack       
            return "SUCCESS"
         }
      } 

      timeout {
         set timeout $timeoutBack
         return "ERRTIMEOUT"
      }
   }
   
}




###############################################
# BackToMainMenu - attempts to go back to main menu from any sub menu of main menu
# 
# Variables:
#   IN:
# 
#   OUT:
#
###############################################
proc BackToMainMenu { host {safeCount 10}} {

   global spawnId spawnPid spawn_id timeout

   set spawn_id $spawnId($host)    
   
   set backTimeout $timeout

   set timeout 4

   set i 1
   
   while {$i <= $safeCount} {

      incr i

      exp_send -- "\r"
      expect {
         -re "Please select a menu choice \\(\[01] - 9,B,P,C,L,R,E\\): " {
            #puts "------ already in Main menu ------"
            #restore timeout
            set timeout $backTimeout
            return "SUCCESS"                
         }   
         "Please select a menu choice*: "  {
            set cmdOut $expect_out(buffer)
            if {[regexp {R\)[\ \t]* Return to the Main Menu} $cmdOut] == 1} {
               exp_send -- "R\r"
               expect {
                  -re "Please select a menu choice \\(\[01] - 9,B,P,C,L,R,E\\): " {
                     #restore timeout
                     set timeout $backTimeout                        
                     return "SUCCESS"
                  }
                  timeout {
                     if {$i == $safeCount} {
                        lappend rcode "ERROR: unexpected response for R option"
                        #restore timeout
                        set timeout $backTimeout
                        return [ErrCheck $rcode BackToMainMenu]
                     }
                  }
               }
            } else {
               exp_send -- "\r"
               expect {
                  -re "Please select a menu choice \\(\[01] - 9,B,P,C,L,R,E\\): " {
                     #restore timeout
                     set timeout $backTimeout                        
                     return "SUCCESS"
                  }
                  
                  timeout {
                     if {$i == $safeCount} {
                        lappend rcode "ERROR: unexpected response for R option"
                        #restore timeout
                        set timeout $backTimeout
                        return [ErrCheck $rcode BackToMainMenu]
                     }
                  }
               }                    
            }                                
         }
         timeout {}           
      }        
   }; #end while

   #restore timeout
   set timeout $backTimeout 
   lappend rcode "ERROR: fail to go back to main menu after $safeCount atempts"
   return [ErrCheck $rcode BackToMainMenu]

}; #end proc BackToMainMenu




############
# priv_ResetSwitchFact - resets the switch to factory defaults and enters in Main Menu
#
# !WARNING - you must call this proc from Main Menu 
#
############
proc mm_ResetSwitchFact {host {usr "admin"} {pass "setup"}} {

   global spawnId spawnPid spawn_id timeout

   set spawn_id $spawnId($host)

   set rcode ""

   exp_send -- "R\r"
   expect { 
      "(YES or NO): " {            
         exp_send -- "YES\r"             
         set backTimeout $timeout
         set timeout 480

         expect  {
            -re "Please enter the administrator's user name: " {
               exp_send -- "$usr\r"
               expect "Please enter the administrator's password: "
               exp_send -- "$pass\r"
               expect {
                  -re "Please select a menu choice \\(\[01] - 9,B,P,C,L,R,E\\): " {
                     set timeout $backTimeout
                     return "SUCCESS"
                  }                
                  timeout {
                     set timeout $backTimeout
                     lappend rcode "ERROR: did not got the prompt: \"Please select a menu choice (1 - 9,B,P,C,L,R,E): \" or \"Please select a menu choice (1 - 9,B,P,C,L,R,E): \""
                     return [ErrCheck $rcode ResetSwitchFact]
                  }
               }   
            }
				-re "Please enter the administrator's password: " {
					exp_send -- "\r"
					exp_continue
				}				
            timeout {
               set timeout $backTimeout
               lappend rcode "ERROR: did not got the prompt: \"Please enter the administrator's user name: \""
               return [ErrCheck $rcode ResetSwitchFact]
            }
         }                                                    
      }
      timeout {            
         lappend rcode "ERROR: go to switch reset menu - R Main Menu option -: timeout"
         return [ErrCheck $rcode ResetSwitchFact]
      }
   }            
}; #end proc switchIP


##############################################################
# mm_ExitSaveInvoke - exit option of Main Menu and then enters back to Main Menu
#
# !WARNING - you must call this proc from Main Menu 
#
##############################################################
proc mm_ExitSaveInvoke { host {usr "admin"} {pass "setup"} } {

   global spawnId spawnPid spawn_id timeout

   set spawn_id $spawnId($host)

   set backupTimeout $timeout
   set timeout 60

   set rcode ""

   exp_send -- "E\r"
   expect { 
      -re "Please enter the administrator's user name: " {
         exp_send -- "$usr\r"
         expect "Please enter the administrator's password: "
         exp_send -- "$pass\r"
         expect {
            -re "Please select a menu choice \\(\[01] - 9,B,P,C,L,R,E\\): " {
               set timeout $backupTimeout
               return "SUCCESS"
            }                
            timeout {
               lappend rcode "ERROR: Exit, Save and Invoke Changes"                                        
            }
         }             
      }

      timeout {
         lappend rcode "ERROR: Exit, Save and Invoke Changes"
         set timeout $backupTimeout            
      }                   

   }               

   set timeout $backupTimeout
   return [ErrCheck $rcode MainMenuToCli]

}; #end ExitSaveInvoke



#################################
# mm_SetPrivInterface - configures the private management interface from MainMenu
#
# !WARNING - you must call this proc from Main Menu 
# 
#
#################################
proc mm_SetMngInterface { host managementIp interfaceIp {interfaceID 0} {mask "255.255.255.0"}} {
    mm_SetPrivInterface $host $managementIp $interfaceIp $interfaceID $mask
}



#################################
# mm_SetPrivInterface - configures the private management interface from MainMenu
#
# !WARNING - you must call this proc from Main Menu 
# 
#
#################################
proc mm_SetPrivInterface { host managementIp interfaceIp {interfaceID 0} {mask "255.255.255.0"}} {

   global spawnId spawnPid spawn_id timeout

   set spawn_id $spawnId($host)

   set rcode ""
   
   set backupTimeout $timeout
   set timeout 60

   set gotTimeout 0

   exp_send -- "1\r"
   expect {
      -re "Please select a menu choice: " {}
      timeout { 
         BackToMainMenu $host
         set gotTimeout 1
         lappend rcode "ERROR: fail to enter in Interface menu"             
      }
   }

   if {$gotTimeout == 0} {
      exp_send -- "$interfaceID\r"
      expect {
         "New Management IP Address* = " {}
         timeout {
            BackToMainMenu $host
            set gotTimeout 1
            lappend rcode "ERROR: timeout waiting for: \"New Management IP Address* = \""
         }
      }
   }

   if {$gotTimeout == 0} {
      exp_send -- "$managementIp\r"
      expect {
         "New Interface IP Address* = " {}
         timeout {
            BackToMainMenu $host
            set gotTimeout 1
            lappend rcode "ERROR: timeout waiting for: \"New Interface IP Address* = \"" 
         }
      }
   }

   if {$gotTimeout == 0} {
      exp_send -- "$interfaceIp\r"
      expect {
         "New Subnet Mask = " {}
         timeout {
            BackToMainMenu $host
            set gotTimeout 1
            lappend rcode "ERROR: timeout waiting for: \"New Subnet Mask = \"" 
         }
      }
   }

   if {$gotTimeout == 0} {
      exp_send -- "$mask\r" 
      expect {
         -exact "Please select a menu choice (1-5, <CR>): " {}
         timeout {
            BackToMainMenu $host
            set gotTimeout 1
            lappend rcode "ERROR: timeout waiting for: \"Please select a menu choice (1-5, <CR>): \""
         }
      }
   }

   if {$gotTimeout == 0} {
      exp_send -- "1\r"
      expect {
         "Please select a menu choice: " {}
         timeout {
            BackToMainMenu $host
            set gotTimeout 1
            lappend rcode "ERROR: timeout waiting for: \"Please select a menu choice: \""
         }                
      }
   }

   if {$gotTimeout == 0} {
      exp_send -- "R\r"
      expect {
         -re "Please select a menu choice \\(\[01] - 9,B,P,C,L,R,E\\): " {}      
         timeout {
            BackToMainMenu $host
            set gotTimeout 1
            lappend rcode "ERROR: timeout waiting for: \"Please select a menu choice ((0 or 1) - 9,B,P,C,L,R,E): \""
         }
      }
   }

   set timeout $backupTimeout
   return [ErrCheck $rcode SetPrivInterface]

}; #end mm_SetPrivInterface


#################################
# mm_new_SetMngInterface - configures the private management interface from MainMenu
#
# !WARNING - you must call this proc from Main Menu 
# 
#
#################################
proc mm_new_SetMngInterface {host managementIp} {

   global spawnId spawnPid spawn_id timeout

   set spawn_id $spawnId($host)

   set rcode ""
   
   set backupTimeout $timeout
   set timeout 60

   set gotTimeout 0

   exp_send -- "0\r"
   expect {
       -re "Please select a menu choice \\(M, R\\):" {}
      timeout { 
         BackToMainMenu $host
         set gotTimeout 1
         lappend rcode "ERROR: fail to enter in Management Ip Address menu"             
      }
   }

   if {$gotTimeout == 0} {
      exp_send -- "M\r"
      expect {
         "New Management IP Address* = " {}
         timeout {
            BackToMainMenu $host
            set gotTimeout 1
            lappend rcode "ERROR: timeout waiting for: \"New Management IP Address* = \""
         }
      }
   }

   if {$gotTimeout == 0} {
      exp_send -- "$managementIp\r"
      expect {
          -re "Please select a menu choice \\(M, R\\):" {}
         timeout {
            BackToMainMenu $host
            set gotTimeout 1
            lappend rcode "ERROR: timeout waiting for: \"Please select a menu choice (M, R): \""
         }
      }
   }

   if {$gotTimeout == 0} {
      exp_send -- "R\r"
      expect {
         -re "Please select a menu choice \\(\[01] - 9,B,P,C,L,R,E\\): " {}      
         timeout {
            BackToMainMenu $host
            set gotTimeout 1
            lappend rcode "ERROR: timeout waiting for: \"Please select a menu choice ((0 or 1) - 9,B,P,C,L,R,E): \""
         }
      }
   }

   set timeout $backupTimeout
   return [ErrCheck $rcode new_SetMngInterface]

}; #end mm_new_SetMngInterface


#################################
# mm_SetPublicInterface - configures a public interface from MainMenu
#
# !WARNING - you must call this proc from Main Menu 
# 
#
#################################
proc mm_SetPublicInterface {host interfaceIp {interfaceID 1} {mask "255.255.255.0"}} {

   global spawnId spawnPid spawn_id timeout

   set spawn_id $spawnId($host)

   set rcode ""
   
   set backupTimeout $timeout
   set timeout 60

   set gotTimeout 0

   exp_send -- "1\r"
   expect {
      -re "Please select a menu choice: " {}
      timeout { 
         BackToMainMenu $host
         set gotTimeout 1
         lappend rcode "ERROR: fail to enter in Interface menu"             
      }
   }

   if {$gotTimeout == 0} {
      exp_send -- "$interfaceID\r"
      expect {
         "New IP Address* = " {}
         
         -exact "Please select a menu choice (1-5, <CR>): " {
            set cmdOut $expect_out(buffer)
            set cmdOutLines [split $cmdOut "\n"]
            foreach line $cmdOutLines {
               if {[regexp {DHCP address cannot be changed in the serial menu, please use WEB browser} $line] == 1} {
                  lappend rcode "ERROR: the interface $interfaceID is configured by DHCP. Cannot be configured from Main Menu"
               }
            }
            if {$rcode == ""} {
               lappend rcode "ERROR: expected \"New Interface IP Address* = \" but got \"Please select a menu choice (1-5, <CR>):\""
            }
            
            #go back to main menu
            BackToMainMenu $host
            set gotTimeout 1
         }            
         timeout {
            BackToMainMenu $host
            set gotTimeout 1
            lappend rcode "ERROR: timeout waiting for: \"New IP Address* = \""
         }
      }
   }

   if {$gotTimeout == 0} {
      exp_send -- "$interfaceIp\r"
      expect {
         "New Subnet Mask = " {}
         timeout {
            BackToMainMenu $host
            set gotTimeout 1
            lappend rcode "ERROR: timeout waiting for: \"New Subnet Mask = \"" 
         }
      }
   }

   if {$gotTimeout == 0} {
      exp_send -- "$mask\r" 
      expect {
         -exact "Please select a menu choice (1-5, <CR>): " {}
         timeout {
            BackToMainMenu $host
            set gotTimeout 1
            lappend rcode "ERROR: timeout waiting for: \"Please select a menu choice (1-5, <CR>): \""
         }
      }
   }

   if {$gotTimeout == 0} {
      exp_send -- "1\r"
      expect {
         "Please select a menu choice: " {}
         timeout {
            BackToMainMenu $host
            set gotTimeout 1
            lappend rcode "ERROR: timeout waiting for: \"Please select a menu choice: \""
         }                
      }
   }

   if {$gotTimeout == 0} {
      exp_send -- "R\r"
      expect {
         -re "Please select a menu choice \\(\[01] - 9,B,P,C,L,R,E\\): " {}      
         timeout {
            BackToMainMenu $host
            set gotTimeout 1
            lappend rcode "ERROR: timeout waiting for: \"Please select a menu choice ((0 or 1) - 9,B,P,C,L,R,E): \""
         }
      }
   }

   set timeout $backupTimeout
   return [ErrCheck $rcode SetPublicInterface]

}; #end mm_SetPublicInterface


#########################################################
# mm_GetInterface - displays interfaces - Main Menu -> option 1
#
#
#########################################################
proc mm_GetInterface { host } {

   global spawnId spawnPid spawn_id timeout

   set spawn_id $spawnId($host)

   set rcode ""

   exp_send -- "1\r"
   expect {
      -re "Please select a menu choice: " {
         set prompt $expect_out(buffer)
         puts $prompt
         lappend rcode "SUCCESS"            
      }
      timeout {
         lappend rcode "ERROR: fail to enter in Interface Menu"             
      }
   }

   BackToMainMenu $host 
   return [ErrCheck $rcode GetInterface]

}; #end proc GetInterface


############
# mm_ResetSwitchFact - resets the switch to factory defaults and enters in Main Menu
#
# !WARNING - you must call this proc from Main Menu 
#
############
proc mm_RestartSwitch {host {usr "admin"} {pass "setup"}} {

   global spawnId spawnPid spawn_id timeout

   set spawn_id $spawnId($host)

   set rcode ""

   exp_send -- "9\r"
   expect { 
      -exact "Please select a menu choice (1, 2, R): " {            
         exp_send -- "2\r"
         expect -exact "-- Confirm: Shutdown and restart system in 10 seconds? (Y or N): "
         exp_send -- "Y\r"
         

         set backTimeout $timeout
         set timeout 480
         expect  {
            -re "Please enter the administrator's user name: " {
               exp_send -- "$usr\r"
               expect "Please enter the administrator's password: "
               exp_send -- "$pass\r"
               expect {
                  -re "Please select a menu choice \\(\[01] - 9,B,P,C,L,R,E\\): " {
                     set timeout $backTimeout
                     return "SUCCESS"
                  }                
                  timeout {
                     set timeout $backTimeout
                     lappend rcode "ERROR: did not got the prompt: \"Please select a menu choice ((0 or 1) - 9,B,P,C,L,R,E): \""
                     return [ErrCheck $rcode ResetSwitchFact]
                  }
               }   
            }
            timeout {
               set timeout $backTimeout
               lappend rcode "ERROR: did not got the prompt: \"Please enter the administrator's user name: \""
               return [ErrCheck $rcode ResetSwitchFact]
            }
         }                                                    
      }
      timeout {            
         lappend rcode "ERROR: go to switch reset menu - R Main Menu option -: timeout"
         return [ErrCheck $rcode ResetSwitchFact]
      }
   }            
}; #end proc ResetSwitch


#################################
#
#
# Description - adds a new default gw for the public interface - if gwId == "new"; or deletes the public gw pointed by gwId
#
#################################
proc mm_SetPublicDefaultGw { host gw gwId cost} {
   set errCode "ERROR"
   set errCount 0
   
   global spawnId spawnPid spawn_id timeout

   set spawn_id $spawnId($host)

   set rcode ""
   
   set backupTimeout $timeout
   set timeout 60

   set gotTimeout 0

   exp_send -- "4\r"
   expect {
      -re "Please select a menu choice\\(.* ?A, R\\): " {}
      timeout { 
         BackToMainMenu $host
         set gotTimeout 1
         lappend rcode "ERROR: fail to enter in Default Public Route Menu"             
      }
   }

   if {$gwId == "new"} {

      if {$gotTimeout == 0} {
         exp_send -- "A\r"
         expect {            
            
            -exact "Please enter the new gateway address (x.x.x.x): " { }            
            timeout {
               BackToMainMenu $host
               set gotTimeout 1
               lappend rcode "ERROR: timeout waiting for: \"Please enter the new gateway address (x.x.x.x): \""
            }
         }
      }

      if {$gotTimeout == 0} {
         exp_send -- "$gw\r"
         expect {
            -exact "Please enter the cost (Numeric, greater than zero): " {}                           
            timeout {
               BackToMainMenu $host
               set gotTimeout 1
               lappend rcode "ERROR: timeout waiting for: \"Please enter the cost (Numeric, greater than zero): \"" 
            }
         }
      }    

      if {$gotTimeout == 0} {
         exp_send -- "$cost\r"
         expect {
            -exact "Please select a menu choice(A, R): " {
               if {[regexp -nocase "Couldn't create" $expect_out(buffer)] == 1} {
                  lappend rcode "ERROR: bad gateway IP address"
                  lappend rcode "$expect_out(buffer)"
               }
            }
            
            -re "Please select a menu choice\\(.*, A, R\\): " {
               
            }

            timeout {
               BackToMainMenu $host
               set gotTimeout 1
               lappend rcode "ERROR: timeout waiting for: \"Please select a menu choice(.*, A, R): \"" 
            }
         }
      }    
      
      if {$gotTimeout == 0} {
         exp_send -- "R\r"
         expect {
            -re "Please select a menu choice \\(\[01] - 9,B,P,C,L,R,E\\): " {}      
            timeout {
               BackToMainMenu $host
               set gotTimeout 1
               lappend rcode "ERROR: timeout waiting for: \"Please select a menu choice ((0 or 1) - 9,B,P,C,L,R,E): \""
            }
         }
      }

   } else {

      if {$gotTimeout == 0} {
         exp_send -- "$gwId\r"
         expect {            
            
            -exact "New Gateway IP Address* = " { }            
            timeout {
               BackToMainMenu $host
               set gotTimeout 1
               lappend rcode "ERROR: timeout waiting for: \"New Gateway IP Address* = \""
            }
         }
      }

      if {$gotTimeout == 0} {
         exp_send -- "0.0.0.0\r"
         expect {
            -exact "Please select a menu choice(A, R): " {}                           
            timeout {
               BackToMainMenu $host
               set gotTimeout 1
               lappend rcode "ERROR: timeout waiting for: \"Please select a menu choice(A, R): \"" 
            }
         }
      }    
      
      if {$gotTimeout == 0} {
         exp_send -- "R\r"
         expect {
            -re "Please select a menu choice \\(\[01] - 9,B,P,C,L,R,E\\): " {}      
            timeout {
               BackToMainMenu $host
               set gotTimeout 1
               lappend rcode "ERROR: timeout waiting for: \"Please select a menu choice ((0 or 1) - 9,B,P,C,L,R,E): \""
            }
         }
      }        
   }

   set timeout $backupTimeout
   return [ErrCheck $rcode SetPublicDefaultGw]

}


#################################
#
#
# Description - adds a new default gw for the private interface - if gwId == "new"; or deletes the private gw pointed by gwId
#
#################################
proc mm_SetPrivateDefaultGw { host gw gwId cost} {
   set errCode "ERROR"
   set errCount 0
   
   global spawnId spawnPid spawn_id timeout

   set spawn_id $spawnId($host)

   set rcode ""
   
   set backupTimeout $timeout
   set timeout 60

   set gotTimeout 0

   exp_send -- "3\r"
   expect {
      -re "Please select a menu choice\\(.* ?A, R\\): " {}
      timeout { 
         BackToMainMenu $host
         set gotTimeout 1
         lappend rcode "ERROR: fail to enter in Default Private Route Menu"             
      }
   }

   if {$gwId == "new"} {

      if {$gotTimeout == 0} {
         exp_send -- "A\r"
         expect {            
            
            -exact "Please enter the new gateway address (x.x.x.x): " { }            
            timeout {
               BackToMainMenu $host
               set gotTimeout 1
               lappend rcode "ERROR: timeout waiting for: \"Please enter the new gateway address (x.x.x.x): \""
            }
         }
      }

      if {$gotTimeout == 0} {
         exp_send -- "$gw\r"
         expect {
            -exact "Please enter the cost (Numeric, greater than zero): " {}                           
            timeout {
               BackToMainMenu $host
               set gotTimeout 1
               lappend rcode "ERROR: timeout waiting for: \"Please enter the cost (Numeric, greater than zero): \"" 
            }
         }
      }    

      if {$gotTimeout == 0} {
         exp_send -- "$cost\r"
         expect {
            -exact "Please select a menu choice(A, R): " {
               if {[regexp -nocase "Couldn't create" $expect_out(buffer)] == 1} {
                  lappend rcode "ERROR: bad gateway IP address"
                  lappend rcode "$expect_out(buffer)"
               }
            }
            
            -re "Please select a menu choice\\(.*, A, R\\): " {
               
            }

            timeout {
               BackToMainMenu $host
               set gotTimeout 1
               lappend rcode "ERROR: timeout waiting for: \"Please select a menu choice(.*, A, R): \"" 
            }
         }
      }    
      
      if {$gotTimeout == 0} {
         exp_send -- "R\r"
         expect {
            -re "Please select a menu choice \\(\[01] - 9,B,P,C,L,R,E\\): " {}      
            timeout {
               BackToMainMenu $host
               set gotTimeout 1
               lappend rcode "ERROR: timeout waiting for: \"Please select a menu choice ((0 or 1) - 9,B,P,C,L,R,E): \""
            }
         }
      }

   } else {

      if {$gotTimeout == 0} {
         exp_send -- "$gwId\r"
         expect {            
            
            -exact "New Gateway IP Address* = " { }            
            timeout {
               BackToMainMenu $host
               set gotTimeout 1
               lappend rcode "ERROR: timeout waiting for: \"New Gateway IP Address* = \""
            }
         }
      }

      if {$gotTimeout == 0} {
         exp_send -- "0.0.0.0\r"
         expect {
            -exact "Please select a menu choice(A, R): " {}                           
            timeout {
               BackToMainMenu $host
               set gotTimeout 1
               lappend rcode "ERROR: timeout waiting for: \"Please select a menu choice(A, R): \"" 
            }
         }
      }    
      
      if {$gotTimeout == 0} {
         exp_send -- "R\r"
         expect {
            -re "Please select a menu choice \\(\[01] - 9,B,P,C,L,R,E\\): " {}      
            timeout {
               BackToMainMenu $host
               set gotTimeout 1
               lappend rcode "ERROR: timeout waiting for: \"Please select a menu choice ((0 or 1) - 9,B,P,C,L,R,E): \""
            }
         }
      }        
   }

   set timeout $backupTimeout
   return [ErrCheck $rcode SetPrivateDefaultGw]

}




################################################################
# MultiResetSwitchFact: go to Main Menu and perform a simultaneous reset to
#                       factory defaults using Main Menu options
#
#
# IN:  hosts: a list of DUTs that should be reseted in format 
#             <term_server_ip:port>
#      usr:   user name (default admin)
#      pass:  password (default setup)
#
# OUT: SUCCESS/ERROR 
################################################################
proc MultiResetSwitchFact { hosts {usr "admin"} {pass "setup"} } {
   
   global spawnId spawnPid spawn_id timeout

   set err_count [GetGlobalErr]
   
   set spawn_list ""
   set no_of_hosts [llength $hosts]
   set timeout_count 0

   foreach host $hosts {
      logCliFile "\n---------------------------- ces: $host ----------------------------\n"
      puts "\n---------------------------- ces: $host ----------------------------\n"
      Connect $usr $pass $host
      CliToMainMenu $host
      lappend spawn_list $spawnId($host)
   }
   
   foreach spawn $spawn_list {
      set spawn_id $spawn
      set arr($spawn) 0
      send -- "R\r"
   }
   
   puts "\n-----------------no of hosts: $no_of_hosts -----------------"
   
   set dut_count 0
   expect {
      -i $spawn_list "(YES or NO): " {
         set local_spawn $expect_out(spawn_id)
         foreach elem [array names spawnId] {
            if {$spawnId($elem) == $local_spawn} {
               logCliFile "\n---------------------------- ces: $elem ----------------------------\n"
               puts "\n---------------------------- ces: $elem ----------------------------\n"
            }
         }
         exp_send -i $expect_out(spawn_id) "YES\r"
         exp_continue
      }
      
      -i $spawn_list "Auto backup is in progress, please redo reset later." {
         set local_spawn $expect_out(spawn_id)
         foreach elem [array names spawnId] {
            if {$spawnId($elem) == $local_spawn} {
               logCliFile "\n---------------------------- ces: $elem ----------------------------\n"
               puts "\n---------------------------- ces: $elem ----------------------------\n"
            }
         }      
         sleep 5
         exp_send -i $expect_out(spawn_id) "R\r"
         exp_continue
      }
      
      -i $spawn_list "Please enter the administrator's user name: " {
         set local_spawn $expect_out(spawn_id)
         set hosts_array($local_spawn) 1
         foreach elem [array names spawnId] {
            if {$spawnId($elem) == $local_spawn} {
               logCliFile "\n---------------------------- ces: $elem ----------------------------\n"
               puts "\n---------------------------- ces: $elem ----------------------------\n"
            }
         }
         exp_send -i $expect_out(spawn_id) "$usr\r"
         set arr($expect_out(spawn_id)) 1
         exp_continue
      }
      
      
      -i $spawn_list "Please enter the administrator's password: " {
         set local_spawn $expect_out(spawn_id)
         foreach elem [array names spawnId] {
            if {$spawnId($elem) == $local_spawn} {
               logCliFile "\n---------------------------- ces: $elem ----------------------------\n"
               puts "\n---------------------------- ces: $elem ----------------------------\n"
            }
         }
         exp_send -i $expect_out(spawn_id) "$pass\r"         
         exp_continue
      }
      

      -i $spawn_list "Please select a menu choice \\(\[01] - 9,B,P,C,L,R,E\\): " {
         set local_spawn $expect_out(spawn_id)
         foreach elem [array names spawnId] {
            if {$spawnId($elem) == $local_spawn} {
               logCliFile "\n---------------------------- ces: $elem ----------------------------\n"
               puts "\n---------------------------- ces: $elem ----------------------------\n"
            }
         }
         if { $arr($local_spawn) == 1 } {
            incr dut_count
         }
         exp_continue
      }
      
      timeout {
         puts "---------------------dut_count:$dut_count-------------------"
         logCliFile "---------------------dut_count:$dut_count-------------------"
         if {$dut_count < $no_of_hosts && $timeout_count < 60 } {
            puts "Waiting...."
            incr timeout_count
            exp_continue
         } else {
            if { $dut_count == $no_of_hosts} {
               puts "\n\nEnd reset to factory defaults $dut_count CES boxes\n\n"
               logCliFile "\n\nEnd reset to factory defaults $dut_count CES boxes\n\n"
            } else {
               ErrCheck [list "ERROR: Failed to reset all $no_of_hosts CES BOXES"]
            }
         }
      }
   }

   return [CheckGlobalErr $err_count]
   
} 


################################################################
# MultiReload: perform a simultaneous reboot for a list of DUTs
#
#
# IN:  hosts: a list of DUTs that should be reseted in format 
#             <term_server_ip:port>
#      usr:   user name (default admin)
#      pass:  password (default setup)
#
# OUT: SUCCESS/ERROR 
################################################################
proc MultiReload { hosts {usr "admin"} {pass "setup"} } {
   global spawnId spawnPid spawn_id timeout

   set err_count [GetGlobalErr]
   
   set spawn_list ""
   set no_of_hosts [llength $hosts]
   set timeout_count 0
   
   foreach host $hosts {
      logCliFile "\n---------------------------- ces: $host ----------------------------\n"
      puts "\n---------------------------- ces: $host ----------------------------\n"
      SetCliLevel "PRIVILEGE" $host
      #Exec "reload" "PRIVILEGE" $host
      send -- "reload\r"
      lappend spawn_list $spawnId($host)
   }
   
   puts "\n-----------------no of hosts: $no_of_hosts -----------------"
   
   set dut_count 0
   expect {
      -i $spawn_list "(y/n)" {
         set local_spawn $expect_out(spawn_id)
         foreach elem [array names spawnId] {
            if {$spawnId($elem) == $local_spawn} {
               logCliFile "\n---------------------------- ces: $elem ----------------------------\n"
               puts "\n---------------------------- ces: $elem ----------------------------\n"
            }
         }                 
         exp_send -i $expect_out(spawn_id) "y\r"
         exp_continue
      }
      
      -i $spawn_list "Please enter the administrator's user name: " {
         set local_spawn $expect_out(spawn_id)
         set hosts_array($local_spawn) 1
         foreach elem [array names spawnId] {
            if {$spawnId($elem) == $local_spawn} {
               logCliFile "\n---------------------------- ces: $elem ----------------------------\n"
               puts "\n---------------------------- ces: $elem ----------------------------\n"
            }
         }
         exp_send -i $expect_out(spawn_id) "$usr\r"
         exp_continue
      }
      
      
      -i $spawn_list "Please enter the administrator's password: " {
         set local_spawn $expect_out(spawn_id)
         foreach elem [array names spawnId] {
            if {$spawnId($elem) == $local_spawn} {
               logCliFile "\n---------------------------- ces: $elem ----------------------------\n"
               puts "\n---------------------------- ces: $elem ----------------------------\n"
            }
         }
         exp_send -i $expect_out(spawn_id) "$pass\r"         
         exp_continue
      }
      

      -i $spawn_list "Please select a menu choice \\(\[01] - 9,B,P,C,L,R,E\\): " {
         set local_spawn $expect_out(spawn_id)
         foreach elem [array names spawnId] {
            if {$spawnId($elem) == $local_spawn} {
               logCliFile "\n---------------------------- ces: $elem ----------------------------\n"
               puts "\n---------------------------- ces: $elem ----------------------------\n"
            }
         }
         incr dut_count
         exp_continue
      }

      timeout {
         if {$dut_count < $no_of_hosts && $timeout_count < 60 } {
            puts "Waiting...."
            incr timeout_count
            exp_continue
         } else {
            if { $dut_count == $no_of_hosts} {
               puts "\n\nEnd reload $dut_count CES boxes\n\n"
               logCliFile "\n\nEnd reload $dut_count CES boxes\n\n"
            } else {
               ErrCheck [list "ERROR: Failed to reload all $no_of_hosts CES BOXES"]
            }
         }
      }
   }
   
   return [CheckGlobalErr $err_count]
}

################################################################
# MultiRetrieve: perform a simultaneous retrieval of a build for a list of DUTs
#
#
# IN:  hosts:    a list of DUTs that should be reseted in format 
#                <term_server_ip:port>
#      server:   address of the FTP server with builds in format <A.B.C.D>
#      version:  version to be loaded
#      path:     relative path on the FTP server
#      ftp_uid:  ftp user
#      ftp_pass: ftp password
#      recurse:  recurse mode (YES/NO)
#      usr:      user name (default admin)
#      pass:     password (default setup)
#
# OUT: SUCCESS/ERROR 
################################################################
proc MultiRetrieve { hosts server version path ftp_uid ftp_pass {recurse "YES"} {usr "admin"} {pass "setup"} } {
   global spawnId spawnPid spawn_id timeout
   
   set err_count [GetGlobalErr]
   
   set spawn_list ""
   set no_of_hosts [llength $hosts]
   set timeout_count 0
   
   foreach host $hosts {
      logCliFile "\n---------------------------- ces: $host ----------------------------\n"
      puts "\n---------------------------- ces: $host ----------------------------\n"
      #Connect $usr $pass $host
      SetCliLevel "PRIVILEGE" $host
      lappend spawn_list $spawnId($host)
   }
   
   foreach spawn $spawn_list {
      set spawn_id $spawn
      if {$recurse == "YES"} {
         send -- "retrieve software $server version $version path $path uid $ftp_uid password $ftp_pass recurse\r" 
      } else {
         send -- "retrieve software $server version $version path $path uid $ftp_uid password $ftp_pass\r" 
      }
      
   }
   puts "\n-----------------no of hosts: $no_of_hosts -----------------"
   log_user 0
   set dut_count 0
   expect {
      -i $spawn_list "Retrieving requested version $version.  Please wait." {
         set local_spawn $expect_out(spawn_id)
         foreach elem [array names spawnId] {
            if {$spawnId($elem) == $local_spawn} {
               logCliFile "\n---------------------------- CES: $elem ----------------------------\n"
               puts "\n---------------------------- CES: $elem ----------------------------\n"
               send_user "$expect_out(buffer)\n"
            }
         }                 
         exp_continue
      }
      
      -i $spawn_list "Version $version is already installed" {
         set local_spawn $expect_out(spawn_id)
         foreach elem [array names spawnId] {
            if {$spawnId($elem) == $local_spawn} {
               logCliFile "\n---------------------------- CES: $elem ----------------------------\n"
               puts "\n---------------------------- CES: $elem ----------------------------\n"
               send_user "$expect_out(buffer)\n"
            }
         }
         incr dut_count
         exp_continue
      }
      
      -i $spawn_list "Version $version already exists" {
         set local_spawn $expect_out(spawn_id)
         foreach elem [array names spawnId] {
            if {$spawnId($elem) == $local_spawn} {
               logCliFile "\n---------------------------- CES: $elem ----------------------------\n"
               puts "\n---------------------------- CES: $elem ----------------------------\n"
               send_user "$expect_out(buffer)\n"
            }
         }
         incr dut_count
         exp_continue
      }
      
      -i $spawn_list "Success" {
         set local_spawn $expect_out(spawn_id)
         foreach elem [array names spawnId] {
            if {$spawnId($elem) == $local_spawn} {
               logCliFile "\n---------------------------- CES: $elem ----------------------------\n"
               puts "\n---------------------------- CES: $elem ----------------------------\n"
               send_user "$expect_out(buffer)\n"
            }
         }
         incr dut_count
         exp_continue
      }
      
      timeout {  
         if {$dut_count < $no_of_hosts && $timeout_count < 60 } {
            puts "Waiting...."
            incr timeout_count
             exp_continue
         } else {
            if { $dut_count == $no_of_hosts} {
               puts "\n\nEnd retrieve version $version on $dut_count CES boxes\n\n"
               logCliFile "\n\nEnd retrieve version $version on $dut_count CES boxes\n\n"
            } else {
               ErrCheck [list "ERROR: Failed to retrieve version $version on all $no_of_hosts CES BOXES"]
            }
         }
      }      
   }
   log_user 1
   return [CheckGlobalErr $err_count] 
}

################################################################
# MultiBoot: perform a simultaneous boot with a specified version for a list of DUTs
#
#
# IN:  hosts:   a list of DUTs that should be reseted in format 
#               <term_server_ip:port>
#      version: software version
#      usr:     user name (default admin)
#      pass:    password (default setup)
#
# OUT: SUCCESS/ERROR 
################################################################
proc MultiBoot { hosts version {usr "admin"} {pass "setup"} } {

   global spawnId spawnPid spawn_id timeout

   set err_count [GetGlobalErr]
   
   set spawn_list ""
   set no_of_hosts [llength $hosts]
   set timeout_count 0
   
   foreach host $hosts {
      logCliFile "\n---------------------------- ces: $host ----------------------------\n"
      puts "\n---------------------------- ces: $host ----------------------------\n"
      SetCliLevel "PRIVILEGE" $host
      send -- "boot system $version\r"
      lappend spawn_list $spawnId($host)
   }

   set dut_count 0
   expect {
      -i $spawn_list "(Y/N)" {
         set local_spawn $expect_out(spawn_id)
         foreach elem [array names spawnId] {
            if {$spawnId($elem) == $local_spawn} {
               logCliFile "\n---------------------------- ces: $elem ----------------------------\n"
               puts "\n---------------------------- ces: $elem ----------------------------\n"
            }
         }                 
         exp_send -i $expect_out(spawn_id) "Y\r"
         exp_continue
      }
      
       -i $spawn_list "Version $version currently running on the Switch." {
         set local_spawn $expect_out(spawn_id)
         foreach elem [array names spawnId] {
            if {$spawnId($elem) == $local_spawn} {
               logCliFile "\n---------------------------- ces: $elem ----------------------------\n"
               puts "\n---------------------------- ces: $elem ----------------------------\n"
            }
         }
         incr dut_count
         exp_continue
      }
      
      -i $spawn_list "Please enter the administrator's user name: " {
         set local_spawn $expect_out(spawn_id)
         set hosts_array($local_spawn) 1
         foreach elem [array names spawnId] {
            if {$spawnId($elem) == $local_spawn} {
               logCliFile "\n---------------------------- ces: $elem ----------------------------\n"
               puts "\n---------------------------- ces: $elem ----------------------------\n"
            }
         }
         exp_send -i $expect_out(spawn_id) "$usr\r"
         exp_continue
      }
      
      
      -i $spawn_list "Please enter the administrator's password: " {
         set local_spawn $expect_out(spawn_id)
         foreach elem [array names spawnId] {
            if {$spawnId($elem) == $local_spawn} {
               logCliFile "\n---------------------------- ces: $elem ----------------------------\n"
               puts "\n---------------------------- ces: $elem ----------------------------\n"
            }
         }
         exp_send -i $expect_out(spawn_id) "$pass\r"         
         exp_continue
      }
      
      
      -i $spawn_list "Please select a menu choice \\(\[01] - 9,B,P,C,L,R,E\\): " {
         set local_spawn $expect_out(spawn_id)
         foreach elem [array names spawnId] {
            if {$spawnId($elem) == $local_spawn} {
               logCliFile "\n---------------------------- ces: $elem ----------------------------\n"
               puts "\n---------------------------- ces: $elem ----------------------------\n"
            }
         }
         incr dut_count
         exp_continue
      }
      
      timeout {
         if {$dut_count < $no_of_hosts && $timeout_count < 60 } {
            puts "Waiting...."
            incr timeout_count
            exp_continue
         } else {
            if { $dut_count == $no_of_hosts} {
               puts "\n\nEnd boot $version on  $dut_count CES boxes\n\n"
               logCliFile "\n\nEnd boot $version on $dut_count CES boxes\n\n"
            } else {
               ErrCheck [list "ERROR: Failed to boot all $no_of_hosts CES BOXES"]
            }
         }
      }
   }
   
   return [CheckGlobalErr $err_count] 
}


###############################################################
# Get_MM_Type - enters to main menu from CLI, and returns the type of main menu.
#               It is relating to first line of main menu,
#               if it is a separate line for management IP address.
#
# !WARNING - call this procedure only from CLI (any CLI level)
# 
# Variables:
#
#   IN:    host = the DUT IP address (or ip_address:port) 
#
#   OUT:   mm_new_type/mm_old_type or ERROR
#
###############################################################
proc Get_MM_Type { host } {
    set errCode "ERROR"
    set errCount 0
    
    if {[CliToMainMenu $host] == "SUCCESS"} { 
        set mm_type [mm_Get_MM_Type $host]
    } else {
        return "ERROR"
    }
        return $mm_type
#     if {[MainMenuToCli $host] != "SUCCESS"} {
#         return "ERROR"
#     } else {
#         return $mm_type
#     }
}

#################################
# mm_Get_MM_Type  - configures the private management interface from MainMenu
#
# !WARNING - you must call this proc from Main Menu 
# 
#################################
proc mm_Get_MM_Type {host} {

   exp_send -- "\r"
   expect {
       -re {0\) Management Address} { return "mm_new_type" }
       timeout { return "mm_old_type" }
   }
   
}
