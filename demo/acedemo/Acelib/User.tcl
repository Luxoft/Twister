########################################################################
# Library procedures relating to user configuration.
#
#
# AddUser { userName groupName host}
# DelUser { userName groupName host}
# EnterUserLevel { userName groupName host }
# OBSOLATED. Use SetCliLevel instead. ExitUserLevel { host }
# UserIpsecUidSet {host user group uid passwd}
# UserPptpUidSet {host user group uid passwd}
# UserL2tpUidSet {host user group uid passwd}
# UserL2fUidSet {host user group uid passwd}
# UserForcedLogOff {host {userName all} {group ""}
# ShowUserSessions {host sessions_type}
########################################################################



#############################################################
# AddUser: Adds a user.
#
# IN:  userName:
#      groupName:
#      host:      (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc AddUser {userName groupName host} {
   
   global cmdOut

   set err_count [GetGlobalErr]   

   SetCliLevel "CONFIG" $host   
   Exec "user add $userName $groupName" "CONFIG" $host

   if {[regexp "No entries found" $cmdOut] == 1} {
      lappend rcode "ERROR:\n$cmdOut"
      ErrCheck $rcode      
   }
   
   return [CheckGlobalErr $err_count]
}


#############################################################
# DelUser: Deletes a user.
#
# IN:  userName:
#      groupName:
#      host:      (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc DelUser {userName groupName host} {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host        
   Exec "no user $userName $groupName" "CONFIG" $host

   return [CheckGlobalErr $err_count]
}


#############################################################
# EnterUserLevel: Enters to user configuration CLI level.
#
# IN:  userName:
#      groupName:
#      host:      (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc EnterUserLevel {userName groupName host} {
   global cmdOut
   set rcode ""
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host        
   Exec "user $userName $groupName" "CES\\(config-user\\)\#" $host

   if {[regexp -nocase "No entries found" $cmdOut] == 1} {
      lappend rcode "ERROR:\n$cmdOut"
      ErrCheck $rcode
   }

   return [CheckGlobalErr $err_count]
}


#############################################################
# OBSOLATED. Use SetCliLevel instead.
# ExitUserLevel: Exit from user configuration CLI level.
#                Return to CONFIG - CES(config) - CLI mode.
#
# IN:  host: (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc ExitUserLevel {host} {
   set err_count [GetGlobalErr]
    
   Exec "exit" "CONFIG" $host

   return [CheckGlobalErr $err_count]
}


#############################################################
# UserIpsecUidSet: User IPSEC configuration for user ID and password
#
# IN:  host:   (management IP)/(terminal server Ip:port)
#      user:   User name.   
#      group:  Group name.
#      uid:    User ID.
#      passwd: User password.
#
# OUT: SUCCESS/ERROR
#############################################################
proc UserIpsecUidSet {host user group uid passwd} {
   set prompt "CES\\(config-user\\)\#"
   set err_count [GetGlobalErr]
      
   EnterUserLevel $user $group $host
   Exec "ipsec uid $uid password $passwd" $prompt $host
   SetCliLevel "CONFIG" $host
   
   return [CheckGlobalErr $err_count]
}


#############################################################
# UserPptpUidSet: User PPTP configuration for user ID and password
#
# IN:  host:   (management IP)/(terminal server Ip:port)
#      user:   User name.   
#      group:  Group name.
#      uid:    User ID.
#      passwd: User password.
#
# OUT: SUCCESS/ERROR
#############################################################
proc UserPptpUidSet {host user group uid passwd} {
   set prompt "CES\\(config-user\\)\#"
   set err_count [GetGlobalErr]
      
   EnterUserLevel $user $group $host
   Exec "pptp uid $uid password $passwd" $prompt $host
   SetCliLevel "CONFIG" $host
   
   return [CheckGlobalErr $err_count]
}


#############################################################
# UserL2tpUidSet: User L2tp configuration for user ID and password
#
# IN:  host:   (management IP)/(terminal server Ip:port)
#      user:   User name.   
#      group:  Group name.
#      uid:    User ID.
#      passwd: User password.
#
# OUT: SUCCESS/ERROR
#############################################################
proc UserL2tpUidSet {host user group uid passwd} {
   set prompt "CES\\(config-user\\)\#"
   set err_count [GetGlobalErr]
      
   EnterUserLevel $user $group $host
   Exec "l2tp uid $uid password $passwd" $prompt $host
   SetCliLevel "CONFIG" $host
   
   return [CheckGlobalErr $err_count]
}


#############################################################
# UserL2fUidSet: User L2f configuration for user ID and password
#
# IN:  host:   (management IP)/(terminal server Ip:port)
#      user:   User name.   
#      group:  Group name.
#      uid:    User ID.
#      passwd: User password.
#
# OUT: SUCCESS/ERROR
#############################################################
proc UserL2fUidSet {host user group uid passwd} {
   set prompt "CES\\(config-user\\)\#"
   set err_count [GetGlobalErr]
      
   EnterUserLevel $user $group $host
   Exec "l2f uid $uid password $passwd" $prompt $host
   SetCliLevel "CONFIG" $host
   
   return [CheckGlobalErr $err_count]
}


#############################################################
# UserForcedLogOff:
#
# IN:  host:   (management IP)/(terminal server Ip:port)
#      userName: User connection name. Default: 'all'
#      group:  User group name. Default: ""
#
# OUT: SUCESS/ERROR
#############################################################
proc UserForcedLogOff {host {userName all} {group ""} } {
   
   set err_count [GetGlobalErr]

   global cmdOut
   set cmdOut ""

   SetCliLevel "PRIVILEGE" $host
   if { $userName == "all" } {
      Exec "forced-logoff user all-non-admin" "PRIVILEGE" $host
   } else {
      Exec "forced-logoff user $userName $group" "PRIVILEGE" $host
   }
   if {[regexp -nocase "Connection does not exist for user $userName in group $group" $cmdOut msg] == 1} {
      #puts "\n msg = $msg\n"
      ErrCheck "ERROR: $msg" UserForcedLogOff
   }

   return [CheckGlobalErr $err_count]
}


#############################################################
# ShowUserSessions:
#
# IN:  host:   (management IP)/(terminal server Ip:port)
#      sessions_type: ipsec/l2tp/pptp
#
# OUT: No_of_Session/ERROR
#############################################################
proc ShowUserSessions {host sessions_type} {
   set err_count [GetGlobalErr]

   global cmdOut
   set cmdOut ""
   set all ""
   set rez ""
   set ok_parse 0

   SetCliLevel "PRIVILEGE" $host
   Exec "show $sessions_type sessions" "PRIVILEGE" $host

   set sessions 0
   foreach line [split $cmdOut "\n"] {
      if {$sessions == 1} {
          regexp -nocase "$sessions_type:\[\t\ \]*(\[0-9\]+)" $line all rez
         break
      }
      if {[regexp -nocase "Current Sessions:" $line] == 1} {
         set sessions 1
      }
   }
   if {$rez != ""} {
      return $rez
   } else {
      return "ERROR"
   }
    
}
