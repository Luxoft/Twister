#############################################################
# Procedures for handling CES:
#    - logs
#    - sessions
#    - statistics
#    
# 
# GetLogEvents { host }
# SearchLogEvents {host string {wait_time 120}}
# SearchLogSyslog {host string {messages_type all} {wait_time 120}}
# ClearLogEvents { host }
# SessionsShow {host {detail "NO"}}
#############################################################


#############################################################
# GetLogEvents: Gets logging events buffer.
#
# IN:  host:    (management IP)/(terminal server Ip:port)  
#      timeOut: timeout for the CLI command (deafult - 120)
#        
# OUT: ERROR/(the content of logging events buffer)
#############################################################
# CLI call: CES#show logging events
proc GetLogEvents { host {timeOut 120}} {

    global cmdOut

    if { [SetCliLevel "PRIVILEGE" $host] != "SUCCESS" } {
        lappend rcode "ERROR: SetPrimaryDnsServer: Failed SetCliLevel"
        return [ErrCheck $rcode Exec] 
    } 
    
    # Exec uses timeout = 120 s - for large logging-events
    if {[Exec "show logging events" "PRIVILEGE" $host 0 $timeOut] == "SUCCESS"} {
        return $cmdOut
    } else {
        return "ERROR"
    }
}


##############################################################
# SearchLogEvents: Display logging events and stop when the string
#                  given as parameter is matched.
#
# IN:  host:      (management IP)/(terminal server Ip:port)
#      string:    The string to find in the logging events.
#      wait_time: how long to wait to find the string in the 
#                 logging events. 
#                 default: 120 seconds
#      mode	  original listing mode (0) or standard (1)
#
# OUT: SUCCESS  if the string is found in the logging events
#      ERROR - otherwise
##############################################################
proc SearchLogEvents {host string {wait_time 120} {mode 0}} {

   set err_count [GetGlobalErr]

   global timeout

   LogFile "\n\nSearchLogEvents: Attempt to get the string '$string' in the logging events."
   LogFile "                 The search stops after about $wait_time seconds if the string is not found.\n"
   logCliFile "\n\nSearchLogEvents: Attempt to get the string '$string' in the logging events."
   logCliFile "                 The search stops after about $wait_time seconds if the string is not found.\n"

   SetCliLevel "PRIVILEGE" $host
   Exec "terminal paging on" "PRIVILEGE" $host
   if {$mode == 0} {
   	exp_send "show logging events display-mode original\r"
   } else {
   	exp_send "show logging events display-mode standard\r"
   }
      
   set counter 0
   set ok_string 0

   set time0 [clock seconds]
   set time1 $time0

   expect {
      "$string" {
         LogFile "\n\n*************************"
         LogFile "Got the string: '$string' in the logging events"
         LogFile "*************************\n\n"
         logCliFile "\n\n*************************"
         logCliFile "Got the string: '$string' in the logging events"
         logCliFile "*************************\n\n"
         
         set ok_string 1
         if {$string == "CES#"} {
            puts "\n\nEND\n\n"
         } else {
            exp_continue
         }
      }
      "More" {
         set time1 [clock seconds]
         if {$ok_string == 1} {
            exp_send "q"
            exp_continue
         }
         if {$counter < $wait_time} {
            #puts "MORE, IF: counter = $counter"
            exp_send " "
            incr counter [expr $time1 - $time0]
            set time0 $time1
            #LogFile "\nelapsed $counter s\n"
            exp_continue
         } else {
            #puts "MORE, ELSE: counter = $counter"
            exp_send "q"
            exp_continue
         } 
      }
      "CES#" {         
         if {$ok_string != 1} {
                     
            if {$counter < $wait_time} {
               #puts "========== CES, IF: counter = $counter"
               LogFile "\n\nTotal time to wait: $wait_time s; elapsed: $counter s"
               LogFile "Wait $timeout seconds before read again the logging events\n"
               sleep $timeout
               incr counter $timeout
               
               exp_send "show logging events\r"                        
               exp_continue
	    } elseif {$mode == 0} {    
	       SearchLogEvents $host $string "120" "1"
	    } else {
               #puts "================CES, ELSE: counter = $counter"
               LogFile "\n$wait_time seconds passed. End check log message for the string '$string'"
               ErrCheck [list "ERROR: Cannot find the string '$string' in the logging events"]
            }

         }
      }
      timeout {
         #puts "timeout: counter = $counter"
         if {$counter < $wait_time} {
            LogFile "\n\nTotal time to wait: $wait_time s; elapsed: $counter s\n"
            incr counter $timeout
            exp_continue
         } else {
            ErrCheck [list "ERROR: Cannot find the string '$string' in the logging events after $wait_time seconds"]
         }
      }
   }

   #puts " ================= after expect ======================= "

   sleep 2
   Exec "terminal paging off" "PRIVILEGE" $host
   return [CheckGlobalErr $err_count]

}


##############################################################
# SearchLogSyslog:    Display system log and stop when the string
#                     given as parameter is matched.
#
# IN:  host:          (management IP)/(terminal server Ip:port)
#      string:        The string to find in the logging events.
#      messages_type: all/alert/crit/debug/emerg/err/info/notice/warning

#      wait_time:     how long to wait to find the string in the 
#                     logging events. 
#                     default: 120 seconds
#
# OUT: SUCCESS  if the string is found in the system log
#      ERROR - otherwise
##############################################################
proc SearchLogSyslog {host string {messages_type all} {wait_time 120}} {

   set err_count [GetGlobalErr]

   global timeout

   LogFile "\n\nSearchLogSyslog: Attempt to get the string '$string' in the system log."
   LogFile "                 The search stops after about $wait_time seconds if the string is not found.\n"
   logCliFile "\n\nSearchLogSyslog: Attempt to get the string '$string' in the system log."
   logCliFile "                 The search stops after about $wait_time seconds if the string is not found.\n"

   SetCliLevel "PRIVILEGE" $host
   Exec "terminal paging on" "PRIVILEGE" $host
   exp_send "show logging syslog $messages_type\r"
      
   set counter 0
   set ok_string 0

   set time0 [clock seconds]
   set time1 $time0

   expect {
      "$string" {
         LogFile "\n\n*************************"
         LogFile "Got the string: '$string' in the syslog log"
         LogFile "*************************\n\n"
         logCliFile "\n\n*************************"
         logCliFile "Got the string: '$string' in the syslog log"
         logCliFile "*************************\n\n"
         
         set ok_string 1
         if {$string == "CES#"} {
            puts "\n\nEND\n\n"
         } else {
            exp_continue
         }
      }
      "More" {
         set time1 [clock seconds]
         if {$ok_string == 1} {
            exp_send "q"
            exp_continue
         }
         if {$counter < $wait_time} {
            #puts "MORE, IF: counter = $counter"
            exp_send " "
            incr counter [expr $time1 - $time0]
            set time0 $time1
            LogFile "\nelapsed $counter s\n"
            exp_continue
         } else {
            #puts "MORE, ELSE: counter = $counter"
            exp_send "q"
            exp_continue
         } 
      }
      "CES#" {         
         if {$ok_string != 1} {
                     
            if {$counter < $wait_time} {
               #puts "========== CES, IF: counter = $counter"
               LogFile "\n\nTotal time to wait: $wait_time s; elapsed: $counter s"
               LogFile "Wait $timeout seconds before read again the syslog log\n"
               sleep $timeout
               incr counter $timeout
               
               exp_send "show logging syslog $messages_type\r"                        
               exp_continue
            } else {
               #puts "================CES, ELSE: counter = $counter"
               LogFile "\n$wait_time seconds passed. End check log message for the string '$string'"
               ErrCheck [list "ERROR: Cannot find the string '$string' in the syslog log"]
            }

         }
      }
      timeout {
         #puts "timeout: counter = $counter"
         if {$counter < $wait_time} {
            LogFile "\n\nTotal time to wait: $wait_time s; elapsed: $counter s\n"
            incr counter $timeout
            exp_continue
         } else {
            ErrCheck [list "ERROR: Cannot find the string '$string' in the syslog log after $wait_time seconds"]
         }
      }
   }

   #puts " ================= after expect ======================= "

   sleep 2
   Exec "terminal paging off" "PRIVILEGE" $host
   return [CheckGlobalErr $err_count]

}



#############################################################
# ClearLogEvents: Clears logging events buffer
# 
# IN:  host:  (management IP)/(terminal server Ip:port) 
#
# OUT: SUCCESS/ERROR
#############################################################
# CLI call: CES#show logging events clear
proc ClearLogEvents { host } {
    
    global cmdOut
    
    if { [SetCliLevel "PRIVILEGE" $host] != "SUCCESS" } {
        lappend rcode "ERROR: SetPrimaryDnsServer: Failed SetCliLevel"
        return [ErrCheck $rcode Exec] 
    }

    #set errCode [Exec "show logging events clear" "PRIVILEGE" $host]
    set errCode [Exec "clear logging events" "PRIVILEGE" $host]

    return $errCode

}


#############################################################
# SessionsShow: Gets the information about management sessions,
#               user connections and BO connections.
#
# IN:  host:   (management IP)/(terminal server Ip:port)
#      detail: <YES/NO> get detailed output for the specified session types
#
# OUT: ERROR/(the output of 'show sessions' CLI command)
#############################################################
proc SessionsShow {host {detail "NO"}} {
   global cmdOut
   
   set err_count [GetGlobalErr]

   SetCliLevel "PRIVILEGE" $host
   if {$detail == "YES"} {
      Exec "show sessions detail" "PRIVILEGE" $host
   } else {
      Exec "show sessions" "PRIVILEGE" $host
   }
   
   if {[CheckGlobalErr $err_count] == "SUCCESS"} {
      return $cmdOut
   } else {
      return "ERROR"
   }
}


#############################################################
# GetSession: Gets from the output of 'show sessions' CLI command
#             a speciffic a certain 
#
# IN:  sessions_report: The output of 'show sessions' CLI command
#                       (SessionsShow proc could be used to get it)
#      sessions_group:  <current/peak_for_today/total_since_boot>
#      sessions_type:   <"Branch Office" / "End User" / Total>
#                       The speciffic sessions number to get.
#
#############################################################
proc GetSession { sessions_report sessions_group sessions_type} {
   
   # ensure that only useful data is parsed
   set ok_line_no 10000

   set sess_gr_msg "NONE"

   set sessions_report [string tolower $sessions_report]
   set sessions_type [string tolower $sessions_type]

   set line_no 1
   foreach line [split $sessions_report "\n"] {
      
      if {[regexp "current sessions:" $line] == 1} {
         if {$sessions_group == "current"} {
            set sess_gr_msg "Current Sessions"
            set ok_line_no $line_no
         } else {
            set ok_line_no 10000
         }
      }

      if {[regexp "peak sessions for today:" $line] == 1} {
         if {$sessions_group == "peak_for_today"} {
            set sess_gr_msg "Peak Sessions for Today"
            set ok_line_no $line_no
         } else {
            set ok_line_no 10000
         }
      }

      if {[regexp "Total sessions since boot:" $line] == 1} {
         if {$sessions_group == "total_since_boot"} {
            set sess_gr_msg "Total Sessions Since Boot"
            set ok_line_no $line_no
         } else {
            set ok_line_no 10000
         }
      }
      
      if {$line_no > $ok_line_no} {
         if {[regexp "$sessions_type:\[\ \t\]*\(\[0-9\]+\)" $line all session_no]} {
            return $session_no
         }
      }
      
      incr line_no
   }
   
   set rcode ""
   lappend rcode "ERROR: not able to sessions: \"$sessions_type\" in: \"$sess_gr_msg\""
   ErrCheck $rcode
   return "ERROR"

}
