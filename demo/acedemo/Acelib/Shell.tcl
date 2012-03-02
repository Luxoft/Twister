#############################################################
# Procedures relating to CES Shell 
# (Debug Shell. 'S' option fom Main Menu)
#
# EnterShell {host passwd}
# ExitShell {host}
# shell_GetMemFrag {host}
# GetFreeMemSharedHeap {memory_report}
# GetMaxBlockMemSharedHeap {memory_report}
# shell_CreateIpsecTunnels {host start_ip tunnels_number dut_public_ip user pass delay wait_time}
#
#############################################################


#############################################################
# EnterShell: Enter into CES Shell ('S' option from Main Menu)
#
# IN:  host:   (management IP)/(terminal server Ip:port)
#      passwd: password
#
# OUT: SUCCESS/ERROR
#############################################################
proc EnterShell {host passwd} {

   set err_count [GetGlobalErr]

   CliToMainMenu $host

   exp_send -- "S\r"

   expect {
      "Password" {
         exp_send "$passwd\r"
         exp_continue
      }

      "0 ->" {}

      timeout {
         ErrCheck "ERROR: fail to enter to CES Shell"
      }            
   }         

   return [CheckGlobalErr $err_count]
}


#############################################################
# ExitShell: Exit from CES Shell and enter into CLI
# 
# IN:  host:      (management IP)/(terminal server Ip:port)
#      wait_time: waiting time in seconds before conclude that 
#                 exit from Shell failed.
#                 default = 300 sec (5 min)
#
# OUT: SUCCESS/ERROR
#############################################################
proc ExitShell {host {wait_time 300}} {

   global spawn_id timeout cmdOut spawnId spawnPid

   set err_count [GetGlobalErr]

   set new_spawn_id $spawnId($host)
	
   ###############################
   # put messages in log files if command is executed on a different ces
   ###############################
   if {$new_spawn_id != $spawn_id} {
      
      set spawn_id $new_spawn_id
      logCliFile "\n---------------------------- ces: $host ----------------------------\n"
      puts "\n---------------------------- ces: $host ----------------------------\n"
   }

   set t 0

   exp_send -- "RestoreShellIo\r"
   expect {
      -re "Please select a menu choice \\(\[01] - 9,B,P,C,L,R,E\\): " {}      

      "0 ->" {
         exp_send -- "RestoreShellIo\r"
      }
    
      timeout {
         if {$t < $wait_time} {
            incr t $timeout
            exp_continue
         } else {
            ErrCheck "{ERROR: fail to exit from CES Shell}"
            return [CheckGlobalErr $err_count]
         }
      }
   }

   SetCliLevel "USER" $host

   return [CheckGlobalErr $err_count]
}


#############################################################
# shell_GetMemFrag: Uses MemFragShow CES Shell command to get
#                   the information relating to memory.
#                   Returns the MemFragShow output.
#             
#            You must be already in CES Shell in order to use
#            this procedure.
#
# IN:  host: (management IP)/(terminal server Ip:port)
#      all:  <YES/NO> define the output mode
#                     summary (if "NO") or detalied (if "YES")  
#
# OUT: ERROR / (The output of MemFragShow Shell command)
#############################################################
proc shell_GetMemFrag {host {all "NO"}} {

   global spawn_id timeout cmdOut spawnId spawnPid

   set timeout_back $timeout

   set timeout 60
   set cmdOut ""

   set err_count [GetGlobalErr]

   set new_spawn_id $spawnId($host)
	
   ###############################
   # put messages in log files if command is executed on a different ces
   ###############################
   if {$new_spawn_id != $spawn_id} {
      
      set spawn_id $new_spawn_id
      logCliFile "\n---------------------------- ces: $host ----------------------------\n"
      puts "\n---------------------------- ces: $host ----------------------------\n"
   }

   if {$all == "YES"} {
      exp_send "MemFragShow\r"
   } else {
      exp_send "__MemFragShow\r"
   }

   expect {
      "0 ->" {
         append cmdOut "0 ->" $expect_out(buffer)
      }

      timeout {
         ErrCheck "{ERROR: fail execute 'MemFragShow' CES Shell command}"
      }
   }

   set timeout $timeout_back

   if {[CheckGlobalErr $err_count] == "SUCCESS"} {
      return $cmdOut
   } else {
      return "ERROR"
   }

}


#############################################################
# GetFreeMemSharedHeap: Returns the free memory in bytes, from 
#                Shared Heap Statistics.
#
# IN:  memory_report: Data about CES memory returned by 'MemFragShow'
#
# OUT: ERROR / (free memory from Shared Heap Statistics - in bytes)
#############################################################
proc GetFreeMemSharedHeap {memory_report} {

   set free_mem "ERROR"
   set ok_line 0

   foreach line [split $memory_report "\n"] {

      # get 'Shared Heap Statistics:' line
      if {[regexp {Shared Heap Statistics:} $line]} {
         set ok_line 1
      }

      # check for free mem (in bytes) in 'Shared Heap Statistics:'
      if {$ok_line == 1} {
         if {[regexp {free[\ \t]*([0-9]+)} $line all free_mem] == 1} {
            break
         }
      }
   }

   return $free_mem
}


#############################################################
# GetMaxBlockMemSharedHeap: Returns the max block of free memory from 
#                Shared Heap Statistics.
#
# IN:  memory_report: Data about CES memory returned by 'MemFragShow'
#
# OUT: ERROR / (max block from Shared Heap Statistics - in bytes)
#############################################################
proc GetMaxBlockMemSharedHeap {memory_report} {

   set max_block "ERROR"
   set ok_line 0

   foreach line [split $memory_report "\n"] {

      # get 'Shared Heap Statistics:' line
      if {[regexp {Shared Heap Statistics:} $line]} {
         set ok_line 1
      }

      # check for max block (in bytes) in 'Shared Heap Statistics:'
      if {$ok_line == 1} {
         if {[regexp {free.*[\t\ ]([0-9]+)[\t\ \r\n]*$} $line all max_block] == 1} {
            break
         }
      }
   }

   return $max_block
}


#############################################################
# shell_CreateIpsecTunnels: This procedure is a wrapper for CreateIpsecTunnels
#                           call from CES Shell
#                           It waits for:
#                           'Tunnel creation in <X> seconds attempts <Y> successes <Z> failures 0'
#                           from Blaster.
#
# IN:  host:          (management IP)/(terminal server Ip:port)
#      start_ip:      A.B.C.D: starting network IP address that Blaster should use
#      tunels_number: the number of IPsec tunnels to be created
#      dut_public_ip: A.B.C.D the public IP address of the DUT
#      user:          user ID for all the IPsec tunnels
#      pass:          the password for user
#      delay:         in ticks means the delay between two consecutive user tunnels
#                     (setting it to 60 is OK)
#      wait_time: time to wait for succes message ('Tunnel creation in ...') from blaster
#
# OUT: SUCCESS: when succeded to create all tunnels (attempts = successes, failures = 0)
#      ERROR: otherwise
#############################################################
proc shell_CreateIpsecTunnels {host start_ip tunnels_number dut_public_ip user pass delay wait_time} {

   global spawn_id timeout cmdOut spawnId spawnPid

   set err_count [GetGlobalErr]

   set new_spawn_id $spawnId($host)

   set elapsed_time 0

   set rcode ""
	
   ###############################
   # put messages in log files if command is executed on a different ces
   ###############################
   if {$new_spawn_id != $spawn_id} {
      
      set spawn_id $new_spawn_id
      logCliFile "\n---------------------------- ces: $host ----------------------------\n"
      puts "\n---------------------------- ces: $host ----------------------------\n"
   }   

   set hex_start_ip [ipToHex $start_ip]
   set hex_dut_public_ip [ipToHex $dut_public_ip]

   exp_send "CreateIpsecTunnels\($hex_start_ip,$tunnels_number,$hex_dut_public_ip,\"$user\",\"$pass\",$delay\)\r"

   #Tunnel creation in 18 seconds attempts 5 successes 5 failures 0
   
   expect {      
      -re {Tunnel creation in ([0-9]+) seconds attempts ([0-9]+) successes ([0-9]+) failures ([0-9]+)[\ ]*} {
         append cmdOut $expect_out(buffer)
         #LogFile " *** Got the message 'Tunnel creation ... ' from BLASTER ***"         
         exp_send "\r"
         expect "0 -> " {}
      }

      timeout {
         incr elapsed_time $timeout
         if {$elapsed_time < $wait_time} {
            exp_continue
         } else {            
            ErrCheck "{ERROR: did not get response from the CES Shell call: 'CreateIpsecTunnels' after $elapsed_time seconds}"            
         }
         
      }

   }

   if {[CheckGlobalErr $err_count] == "SUCCESS"} {
      if {$expect_out(3,string) == $tunnels_number} {
         return "SUCCESS"
      } else {
         ErrCheck "ERROR:\n$cmdOut"         
         return "ERROR"
      }
   } else {
      return "ERROR"
   }   

}


#############################################################
# shell_CreatePptpTunnels: This procedure is a wrapper for CreatePptpTunnels
#                           call from CES Shell
#                           It waits for:
#                           'Done spawning <x> tunnels, successes = <y>, failures = <z>'
#                           from Blaster.
#
# IN:  host:          (management IP)/(terminal server Ip:port)
#      start_ip:      A.B.C.D: starting network IP address that Blaster should use
#      user:          user ID for all the IPsec tunnels
#      tunels_number: the number of IPsec tunnels to be created
#      dut_public_ip: A.B.C.D the public IP address of the DUT
#      wait_time:     time to wait for succes message ('Done spawning ...') from blaster
#
# OUT: SUCCESS: when succeded to create all tunnels (attempts = successes, failures = 0)
#      ERROR: otherwise
#############################################################
proc shell_CreatePptpTunnels {host start_ip user tunnels_number dut_public_ip wait_time} {

   global spawn_id timeout cmdOut spawnId spawnPid

   set err_count [GetGlobalErr]

   set new_spawn_id $spawnId($host)

   set elapsed_time 0

   set rcode ""
	
   ###############################
   # put messages in log files if command is executed on a different ces
   ###############################
   if {$new_spawn_id != $spawn_id} {
      
      set spawn_id $new_spawn_id
      logCliFile "\n---------------------------- ces: $host ----------------------------\n"
      puts "\n---------------------------- ces: $host ----------------------------\n"
   }   

   exp_send "CreatePptpTunnels\(\"$start_ip\",\"$user\",$tunnels_number,\"$dut_public_ip\"\)\r"

   # message for IPSec user tunnels
   #Tunnel creation in 18 seconds attempts 5 successes 5 failures 0

   # message for pptp user tunnels
   #Done spawning 8 tunnels, successes = 8, failures = 0

   expect {      
      -re {Done spawning ([0-9]+) tunnels, successes = ([0-9]+), failures = ([0-9]+)[\ ]*} {
         append cmdOut $expect_out(buffer)
         #LogFile " *** Got the message 'Tunnel creation ... ' from BLASTER ***"         
         exp_send "\r"
         expect "0 -> " {}
      }

      timeout {
         incr elapsed_time $timeout
         if {$elapsed_time < $wait_time} {
            exp_continue
         } else {            
            ErrCheck "{ERROR: did not get response from the CES Shell call: 'CreateIpsecTunnels' after $elapsed_time seconds}"            
         }
         
      }

   }

   if {[CheckGlobalErr $err_count] == "SUCCESS"} {
      if {$expect_out(2,string) == $tunnels_number} {
         return "SUCCESS"
      } else {
         ErrCheck "ERROR:\n$cmdOut"         
         return "ERROR"
      }
   } else {
      return "ERROR"
   }   

}


#############################################################
# shell_CreateL2tpMultTunnelClients: 
#                           This procedure is a wrapper for CreateL2tpMultTunnelClients
#                           call from CES Shell.
#
# IN:  host:          (management IP)/(terminal server Ip:port)
#      start_ip:      A.B.C.D: starting network IP address that Blaster should use
#      dut_public_ip: A.B.C.D the public IP address of the DUT
#      user:          user ID for all the IPsec tunnels
#      calls_number:  the number of 
#      wait_time:     time to wait for creating L2tp tunnels.
#                     
# NOTE: For CreateL2tpMultTunnelClients call, there is no success message from Blaster 
#       like for PPtp and Ipsec tunnels.
#       
#       The procedure will wait for a certain period of time before return.
#
# OUT: SUCCESS
#
# NOTE:
#       SUCCESS is the value always returned by this proc.
#       There is no guaranty that the tunnels were created, because
#       CreateL2tpMultTunnelClients provides no information about this.
#
#       The procedure just runs the Shell command and waits for a certain
#       amount of time, given by 'wait_time' parameter before return.
#      
#      
#############################################################
proc shell_CreateL2tpMultTunnelClients {host start_ip dut_public_ip user tunnels_number wait_time} {

   global spawn_id timeout cmdOut spawnId spawnPid

   set err_count [GetGlobalErr]

   set new_spawn_id $spawnId($host)

   set elapsed_time 0

   set rcode ""
	
   ###############################
   # put messages in log files if command is executed on a different ces
   ###############################
   if {$new_spawn_id != $spawn_id} {
      
      set spawn_id $new_spawn_id
      logCliFile "\n---------------------------- ces: $host ----------------------------\n"
      puts "\n---------------------------- ces: $host ----------------------------\n"
   }   

   exp_send "CreateL2tpMultTunnelClients\(\"$start_ip\",\"$dut_public_ip\",\"$user\",$tunnels_number\)\r"

   # message for IPSec user tunnels
   # 'Tunnel creation in 18 seconds attempts 5 successes 5 failures 0'

   # message for pptp user tunnels
   # 'Done spawning 8 tunnels, successes = 8, failures = 0'

   # message for l2tp tunnels:
   # - there is no success message in this case

   expect {      

      timeout {
         incr elapsed_time $timeout
         if {$elapsed_time < $wait_time} {            
            exp_continue
         } else {
            exp_send -- "\r"
         }
         
      }

   }

   
   return [CheckGlobalErr $err_count]
     

}



#############################################################
# shell_CreateL2fTunnelUsers: 
#                           This procedure is a wrapper for CreateL2fTunnelUsers.
#                           call from CES Shell.
#                           It waits for:
#                           'Tunnel creation in <X> seconds attempts <Y> successes <Z> failures 0'
#                           failures 0' from Blaster.
#
# IN:  host:          (management IP)/(terminal server Ip:port)
#      start_ip:      A.B.C.D: starting network IP address that Blaster should use
#      dut_public_ip: A.B.C.D the public IP address of the DUT
#      user1:         local ID
#      pass1:         local password
#      user2:         peer ID
#      pass2:         peer password
#      user3:         user ID of the L2f account in the LDAP on the contivity beeing blasted
#      tunels_number: the number of calls (MIDs) that should be brougth up inside the tunnel
#      wait_time:     time to wait for creating L2f tunnels.
#      
#
# OUT: SUCCESS
#############################################################
proc shell_CreateL2fTunnelUsers {host start_ip dut_public_ip user1 pass1 user2 pass2 user3 calls_number wait_time} {

   global spawn_id timeout cmdOut spawnId spawnPid

   set err_count [GetGlobalErr]

   set new_spawn_id $spawnId($host)

   set elapsed_time 0

   set rcode ""
	
   ###############################
   # put messages in log files if command is executed on a different ces
   ###############################
   if {$new_spawn_id != $spawn_id} {
      
      set spawn_id $new_spawn_id
      logCliFile "\n---------------------------- ces: $host ----------------------------\n"
      puts "\n---------------------------- ces: $host ----------------------------\n"
   }   

   exp_send "CreateL2fTunnelUsers\(\"$start_ip\",\"$dut_public_ip\",\"$user1\",\"$pass1\",\"$user2\",\"$pass2\",\"$user3\",$calls_number\)\r"

   # message for IPSec user tunnels
   # 'Tunnel creation in 18 seconds attempts 5 successes 5 failures 0'

   # message for pptp user tunnels
   # 'Done spawning 8 tunnels, successes = 8, failures = 0'

   # message for l2tp tunnels:
   # - there is no success message in this case

   expect {      

      timeout {
         incr elapsed_time $timeout
         if {$elapsed_time < $wait_time} {            
            exp_continue
         } else {
            exp_send -- "\r"
         }
         
      }

   }
   return [CheckGlobalErr $err_count]
}


#############################################################
# shell_GenerateTraffic: 
#                        This procedure is genetates traffic
#                        It is a wrapper for GenStart() call
#                        from CES shell
#
# IN:  host:          (management IP)/(terminal server Ip:port)
#      wait_time:     time to wait for creating L2f tunnels.
#      
#
# OUT: SUCCESS
#############################################################
proc shell_GenerateTraffic {host wait_time} {

   global spawn_id timeout cmdOut spawnId spawnPid

   set err_count [GetGlobalErr]

   set new_spawn_id $spawnId($host)

   set elapsed_time 0

   set rcode ""

   set old_timeout $timeout
   set timeout [expr $wait_time + 20]
	
   ###############################
   # put messages in log files if command is executed on a different ces
   ###############################
   if {$new_spawn_id != $spawn_id} {
      
      set spawn_id $new_spawn_id
      logCliFile "\n---------------------------- ces: $host ----------------------------\n"
      puts "\n---------------------------- ces: $host ----------------------------\n"
   }   

   exp_send "GenStart($wait_time)\r"

   expect {      
       "value = 0 = 0x0" {
           exp_continue
       }
       "loss total" {
       }
       timeout {           
           ErrCheck "{ERROR: did not get response from the CES Shell call: 'shell_GenerateTraffic' after $timeout seconds}"
       }
   }
   
   set timeout $old_timeout
   set cmd_out $expect_out(buffer)
   
   exp_send -- "\n"
   expect "0 -> " {}
   
   if { [CheckGlobalErr $err_count] == "ERROR" } {
       return "ERROR"
   } else {
       return $cmd_out
   }
}


proc shell_ShowAllProcessMemUsage { host } {

   global spawn_id timeout cmdOut spawnId spawnPid

   set timeout_back $timeout

   set timeout 60
   set cmdOut ""

   set err_count [GetGlobalErr]

   set new_spawn_id $spawnId($host)
	
   ###############################
   # put messages in log files if command is executed on a different ces
   ###############################
   if {$new_spawn_id != $spawn_id} {
      
      set spawn_id $new_spawn_id
      logCliFile "\n---------------------------- ces: $host ----------------------------\n"
      puts "\n---------------------------- ces: $host ----------------------------\n"
   }

   exp_send "ShowAllProcessMemUsage\r"

   expect {
      "0 ->" {
         append cmdOut "0 ->" $expect_out(buffer)
      }

      timeout {
         ErrCheck "{ERROR: fail execute 'ShowAllProcessMemUsage' CES Shell command}"
      }

   }

   set timeout $timeout_back

   if {[CheckGlobalErr $err_count] == "SUCCESS"} {
      return $cmdOut
   } else {
      return "ERROR"
   }
}

proc GetAllProcessMemUsage { report } {
   set process_mem "ERROR_MEMORY"
   set ok_line 0
   
   foreach line [split $report "\n"] {

      # get 'Subtotals:' line
      if {[regexp {Subtotals} $line]} {
         set ok_line 1
      }

      # check for free mem (in bytes) in 'Shared Heap Statistics:'
      if {$ok_line == 1} {
         if {[regexp {Subtotals[\ \t]*([0-9]+)} $line all process_mem] == 1} {
            break
         }
      }
   }

   return $process_mem   

}
