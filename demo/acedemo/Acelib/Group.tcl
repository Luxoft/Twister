############################################################
# Library procedures for group relating settings.
#
# 
# AddGroup {groupName host}
# DelGroup {groupName host}
# ShowGroup {groupName host}
#
# #################
# #Group connectivity
# #################
# EnterGrConnectivity {host group}
# OBSOLATED. Use EnterGrConnectivity instead. EnterGrpConnectivity {groupName host}
# OBSOLATED. Use SetCliLevel instead. ExitGrpConnectivity {host}
# GrConnShow {host group}
# GrConnSetLogins {host group number_of_logins}
# GrConnSetIdleTimeout {host group idle_timeout}
# GrConnSetPppLinks {host group max_number}
# GrConnIpPool {host group address_pool}
# GrConnIpPoolDisable {host group}
# GrConnIpAddrSrc {host group address_src}
# GrConnSetExcessRate {host group excess_rate}
# GrConnSetCommitRate {host group commited_rate}
# GrConnSetCallPriority {host group call_priority}
# EnaGrConnAccessNetwork {host group net_name} 
# DisGrConnAccessNetwork {host group}
#
# #################
# #Group Ipsec
# #################
# EnterGrIpsecLevel { host {group "/Base"}}
# EnterGroupIpsecLevel { host {grName "/Base"}}
# OBSOLATED. Use SetCliLevel instead.  ExitGroupIpsecLevel { host }
# EnaGrIpsecEncr {host group encryptType}
# DisGrIpsecEncr {host group encryptType}
# EnaGrIpsecIkeEncr {host group encryptType}
# DisGrIpsecIkeEncr {host group encryptType}
# GrIpsecShow {host group}
#
#
# ################
# # Group L2F
# ################
# EnterGrL2fLevel { host {group "/Base"}}
# GrL2fAuth {host group auth_type}
#
# ###############
# # Group PPTP
# ################
# EnterGrPptpLevel { host {group "/Base"}}
# GrPptpAuth {host group auth_type} 
#
#############################################################


#############################################################
# AddGroup: Add a new group.
#
# IN:  groupName
#      host
#
# OUT: 
#############################################################
proc AddGroup {groupName host} {

   global cmdOut
   set rcode ""

   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   
   Exec "group add $groupName" "CONFIG" $host

   if {[regexp "incorrect format" $cmdOut] == 1} {
      lappend rcode "ERROR:\n$cmdOut"
      ErrCheck $rcode
   }

   return [CheckGlobalErr $err_count]
   
}

proc DelGroup {groupName host} {

    SetCliLevel "CONFIG" $host
        
    Exec "no group $groupName" "CONFIG" $host
}

proc ShowGroup {groupName host} {

    SetCliLevel "CONFIG" $host
        
    Exec "show groups $groupName" "CONFIG" $host
}



#################
# Group connectivity
#################

#############################################################
# EnterGrConnectivity: Enter into Group Connectivity setup level.
#
# IN:  group:  Group name.
#      host:   (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc EnterGrConnectivity {host group} {

    set prompt "CES\\(config-group/con\\)\#"

    set err_count [GetGlobalErr]
    
    SetCliLevel "CONFIG" $host
        
    Exec "group connectivity $group" $prompt $host

    return [CheckGlobalErr $err_count]

}


#############################################################
# OBSOLATED. Use EnterGrConnectivity instead
# EnterGrpConnectivity: Enter into Group Connectivity setup level.
#
# IN:  group:  Group name.
#      host:   (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc EnterGrpConnectivity {group host} {

   EnterGrConnectivity $group $host

}


#############################################################
# OBSOLATED. Use SetCliLevel instead.
# ExitGrpConnectivity: Exit from Group Connectivity setup level.
#
# IN:  host:   (management IP)/(terminal server Ip:port)      
#
# OUT: SUCCESS/ERROR
#############################################################
proc ExitGrpConnectivity {host} {
   set err_count [GetGlobalErr]
   Exec "exit" "CONFIG" $host
   return [CheckGlobalErr $err_count]
}




#############################################################
# GrConnShow: Display group Connectivity configuration.
#             Returns the output of CLI command.
#
# IN:  host:  (management IP)/(terminal server Ip:port)
#      group: Group name.
#
# OUT: <CLI command output>/ERROR
#############################################################
proc GrConnShow {host group} {

   global cmdOut
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   Exec "show groups connectivity $group" "CONFIG" $host   
   
   if {[CheckGlobalErr $err_count] != "ERROR"} {
      return $cmdOut
   } else {
      return "ERROR"
   }

}

#############################################################
# GrConnSetLogins: Enable number logins.
#
# IN:  host:             (management IP)/(terminal server Ip:port)
#      group:            Group name.
#      number_of_logins: <0-65000>  Number of logins
#
# OUT: SUCCESS/ERROR
#############################################################
proc GrConnSetLogins {host group number_of_logins} {
   set prompt "CES\\(config-group/con\\)\#"

   set err_count [GetGlobalErr]
   
   EnterGrConnectivity $host $group

   Exec "logins $number_of_logins" $prompt $host

   SetCliLevel "CONFIG" $host

   return [CheckGlobalErr $err_count]
} 


#############################################################
# GrConnSetIdleTimeout: Set length of time a user may be idle before 
#                       being disconnected.
#
# IN:  host:             (management IP)/(terminal server Ip:port)
#      group:            Group name.
#      idle_timeout:     hh:mm:ss  Time
#
# OUT: SUCCESS/ERROR
#############################################################
proc GrConnSetIdleTimeout {host group idle_timeout} {
   set prompt "CES\\(config-group/con\\)\#"

   set err_count [GetGlobalErr]
   
   EnterGrConnectivity $host $group 

   Exec "idle-timeout $idle_timeout" $prompt $host

   SetCliLevel "CONFIG" $host

   return [CheckGlobalErr $err_count]   
}


#############################################################
# GrConnSetPppLinks: Enable maximum number of ppp links for the group
#
# IN:  host:             (management IP)/(terminal server Ip:port)
#      group:            Group name.
#      ppp_links:        <1-9999>  Maximum number of links
#
# OUT: SUCCESS/ERROR
#############################################################
proc GrConnSetPppLinks {host group max_number} {
   set prompt "CES\\(config-group/con\\)\#"

   set err_count [GetGlobalErr]
   
   EnterGrConnectivity $host $group   

   Exec "ppp-links max-number $max_number" $prompt $host

   SetCliLevel "CONFIG" $host

   return [CheckGlobalErr $err_count]
}


#############################################################
# GrConnIpPool: Configures the IP addres Pool for a group.
#                       
# IN:  host:             (management IP)/(terminal server Ip:port)
#      group:            Group name.
#      address_pool:     IP address Pool name
#
# OUT: SUCCESS/ERROR
#############################################################
proc GrConnIpPool {host group address_pool} {
   global cmdOut
   set prompt "CES\\(config-group/con\\)\#"

   set err_count [GetGlobalErr]
   
   EnterGrConnectivity $host $group 

   Exec "ip address-pool $address_pool" $prompt $host

   if {[regexp "does not exist" $cmdOut] == 1} {
      lappend rcode "ERROR:\n$cmdOut"
      ErrCheck $rcode
   }

   SetCliLevel "CONFIG" $host

   return [CheckGlobalErr $err_count]
}

#############################################################
# GrConnIpPoolDisable: Disables the IP addres Pool for a group.
#                       
# IN:  host:  (management IP)/(terminal server Ip:port)
#      group: Group name.
#
# OUT: SUCCESS/ERROR
#############################################################
proc GrConnIpPoolDisable {host group} {
   global cmdOut
   set prompt "CES\\(config-group/con\\)\#"

   set err_count [GetGlobalErr]
   
   EnterGrConnectivity $host $group 

   Exec "no ip address-pool" $prompt $host

   SetCliLevel "CONFIG" $host

   return [CheckGlobalErr $err_count]
}


#############################################################
# GrConnIpAddrSrc: Configures the User IP Address Source.
#                       
# IN:  host:             (management IP)/(terminal server Ip:port)
#      group:            Group name.
#      address_src:      address-pool/default/dhcp-server
#
# OUT: SUCCESS/ERROR
#############################################################
proc GrConnIpAddrSrc {host group address_src} {

   set prompt "CES\\(config-group/con\\)\#"

   set err_count [GetGlobalErr]
   
   EnterGrConnectivity $host $group 

   Exec "ip address-src $address_src" $prompt $host

   SetCliLevel "CONFIG" $host

   return [CheckGlobalErr $err_count]
}

#############################################################
# GrConnSetExcessRate: Configures the user bandwidth policy 
#                      excess rate. 
#                       
# IN:  host:        (management IP)/(terminal server Ip:port)
#      group:       Group name.
#      excess_rate: user bandwidth policy excess rate value
#
# OUT: SUCCESS/ERROR
#############################################################
proc GrConnSetExcessRate {host group excess_rate} {
   global cmdOut
   set prompt "CES\\(config-group/con\\)\#"

   set err_count [GetGlobalErr]
   
   EnterGrConnectivity $host $group 

   Exec "excess rate $excess_rate" $prompt $host

   if {[regexp "does not exist" $cmdOut] == 1} {
      lappend rcode "ERROR:\n$cmdOut"
      ErrCheck $rcode
   }

   SetCliLevel "CONFIG" $host

   return [CheckGlobalErr $err_count]   
}


#############################################################
# GrConnSetExcessRate: Configures the user bandwidth policy  
#                      excess action.
#                       
# IN:  host:          (management IP)/(terminal server Ip:port)
#      group:         Group name.
#      excess_action: drop/mark  user bandwidth policy excess
#                                rate action
#
# OUT: SUCCESS/ERROR
#############################################################
proc GrConnSetExcessAction {host group excess_action} {
   global cmdOut
   set prompt "CES\\(config-group/con\\)\#"

   set err_count [GetGlobalErr]
   
   EnterGrConnectivity $host $group 

   Exec "excess action $excess_action" $prompt $host

   if {[regexp "does not exist" $cmdOut] == 1} {
      lappend rcode "ERROR:\n$cmdOut"
      ErrCheck $rcode
   }

   SetCliLevel "CONFIG" $host

   return [CheckGlobalErr $err_count]     
}


#############################################################
# GrConnSetCommitRate: .
#                       
# IN:  host:          (management IP)/(terminal server Ip:port)
#      group:         Group name.
#      commited_rate: user bandwidth policy committed rate value
#
# OUT: SUCCESS/ERROR
#############################################################
proc GrConnSetCommitRate {host group commited_rate} {
   global cmdOut
   set prompt "CES\\(config-group/con\\)\#"

   set err_count [GetGlobalErr]
   
   EnterGrConnectivity $host $group 

   Exec "committed rate $commited_rate" $prompt $host

   if {[regexp {[Ee]xcess rate must be greater than or equal to committed rate} $cmdOut] == 1 || \
           [regexp "does not exist" $cmdOut] == 1} {
      lappend rcode "ERROR:\n$cmdOut"
      ErrCheck $rcode
   }

   SetCliLevel "CONFIG" $host

   return [CheckGlobalErr $err_count]   
}


#############################################################
# GrConnSetCallPriority: Configures the call-admission priority 
#                        for a group.
#                       
# IN:  host:          (management IP)/(terminal server Ip:port)
#      group:         Group name.
#      call_priority: <highest, high, medium, low> call-admission priority.
#
# OUT: SUCCESS/ERROR
#############################################################
proc GrConnSetCallPriority {host group call_priority} {

   global cmdOut
   set prompt "CES\\(config-group/con\\)\#"

   set err_count [GetGlobalErr]
   
   EnterGrConnectivity $host $group 

   Exec "priority call-admission $call_priority" $prompt $host

   SetCliLevel "CONFIG" $host

   return [CheckGlobalErr $err_count]

}


#############################################################
# EnaGrConnAccessNetwork: Enable access network.
#
# IN:  host:           (management IP)/(terminal server Ip:port)
#      group:          Group name.
#      net_name:       Network name
#
# OUT: SUCCESS/ERROR
#############################################################
proc EnaGrConnAccessNetwork {host group net_name} {

    global cmdOut
    set prompt "CES\\(config-group/con\\)\#"
    
    set err_count [GetGlobalErr]
    
    EnterGrConnectivity $host $group
    Exec "access-network $net_name" $prompt $host
    
    if {[regexp "Network does not exists" $cmdOut] == 1} {
        set rcode "ERROR:\n$cmdOut"
        return [ErrCheck $rcode "EnaGrConnAccessNetwork"]
    }

    SetCliLevel "CONFIG" $host
    
    return [CheckGlobalErr $err_count]
} 

#############################################################
# DisGrConnAccessNetwork: Disable access network.
#
# IN:  host:           (management IP)/(terminal server Ip:port)
#      group:          Group name.
#
# OUT: SUCCESS/ERROR
#############################################################
proc DisGrConnAccessNetwork {host group} {
   set prompt "CES\\(config-group/con\\)\#"

   set err_count [GetGlobalErr]
   
   EnterGrConnectivity $host $group
   Exec "no access-network" $prompt $host

   SetCliLevel "CONFIG" $host

   return [CheckGlobalErr $err_count]
} 



#################
# Group Ipsec
#################

#############################################################
# EnterGrIpsecLevel: Enters into Group IPSEC setup level.
#
# IN:  host:   (management IP)/(terminal server Ip:port)
#      group:  Group name. default: '/Base'
#
# OUT: SUCCESS/ERROR
#############################################################
proc EnterGrIpsecLevel { host {group "/Base"}} {

   set prompt "CES\\(config-group/ipsec\\)\#"

   set err_count [GetGlobalErr]
    
   SetCliLevel "CONFIG" $host
   Exec "group ipsec $group" $prompt $host

   return [CheckGlobalErr $err_count]

}


#############################################################
# OBSOLATED. Use EnterGrIpsecLevel instead
# EnterGroupIpsecLevel: Enter into Group IPSEC setup level.
#
# IN:  host:   (management IP)/(terminal server Ip:port)
#      group:  Group name. default: '/Base'
#
# OUT: SUCCESS/ERROR
#############################################################
proc EnterGroupIpsecLevel { host {group "/Base"}} {

   EnterGrIpsecLevel $gost $group

}


#############################################################
# OBSOLATED. Use SetCliLevel instead.
# ExitGroupIpsecLevel: Exits from Group Ipsec setup level and enter
#                      to Config setup level.
#
# IN:  host: (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc ExitGroupIpsecLevel { host } {
   
   set err_count [GetGlobalErr]
   Exec "exit" "CONFIG" $host  
   return [CheckGlobalErr $err_count]
   
}


#############################################################
# EnaGrIpsecEncr: Enables the the encryption algorithm for IpSec Group.
#
# NOTE: The encryption type must be first enabled with CLI command: 
#       CES(config)#ipsec encryption ...
# 
# IN:  host:        (management IP)/(terminal server Ip:port)
#      group:       Group name.
#      encryptType: Encryption type: 
#                    3des-md5     Triple DES with MD5 Integrity
#                    3des-sha1    Triple DES with SHA1 Integrity
#                    aes128-sha1  ESP - AES 128 with SHA1 Integrity
#                    aes256-sha1  ESP - AES 256 with SHA1
#                    des40-md5    40bit DES with MD5 Integrity
#                    des40-sha1   40bit DES with SHA1 Integrity
#                    des56-md5    56bit DES with MD5 Integrity
#                    des56-sha1   56bit DES with SHA1 Integrity
#                    hmac-md5     Authentication Header Message
#                                 Code Message Digest
#                    hmac-sha1    Authentication Header Message
#                                 Code Secure Hash
#                    ike          Enables IKE encryption and Diffie-Hellman 
#                                 group for the IPSEC tunneling
#                    md5          Authentication Only with MD5 Integrity
#                    sha1         Authentication Only with SHA1 Integrity
#                    all          All the encryptions
#
# OUT: SUCCESS/ERROR
#############################################################
proc EnaGrIpsecEncr {host group encryptType} {

   global cmdOut
   set cmdOut ""
   set encrList ""
   set prompt "CES\\(config-group/ipsec\\)\#"

   set err_count [GetGlobalErr]
   EnterGrIpsecLevel $host $group

   if {$encryptType == "all" } {
      Exec "encryption ?" "${prompt}encryption " $host 0 20 0
      foreach line [split $cmdOut "\n"] {
         if {[regexp -nocase {^[\r\t ]+([a-zA-Z0-9\-]+)[\t ]+.*} $line all encrType] == 1 &&\
                 $encrType != "ike"} {
            lappend encrList $encrType 
         }
      } 
      Exec "[lindex $encrList 0]" $prompt $host
      for {set i 1} {$i < [llength $encrList]} {incr i} {
         Exec "encryption [lindex $encrList $i]" $prompt $host
      }

   } else {
       Exec "encryption $encryptType" $prompt $host
   }

   SetCliLevel "CONFIG" $host
   return [CheckGlobalErr $err_count]
}


#############################################################
# DisGrIpsecEncr: Disables the the encryption algorithm for IpSec Group.
#
# IN:  host:        (management IP)/(terminal server Ip:port)
#      group:       Group name.
#      encryptType: Encryption type: 
#                    3des-md5     Triple DES with MD5 Integrity
#                    3des-sha1    Triple DES with SHA1 Integrity
#                    aes128-sha1  ESP - AES 128 with SHA1 Integrity
#                    aes256-sha1  ESP - AES 256 with SHA1
#                    des40-md5    40bit DES with MD5 Integrity
#                    des40-sha1   40bit DES with SHA1 Integrity
#                    des56-md5    56bit DES with MD5 Integrity
#                    des56-sha1   56bit DES with SHA1 Integrity
#                    hmac-md5     Authentication Header Message
#                                 Code Message Digest
#                    hmac-sha1    Authentication Header Message
#                                 Code Secure Hash
#                    ike          Enables IKE encryption and Diffie-Hellman 
#                                 group for the IPSEC tunneling
#                    md5          Authentication Only with MD5 Integrity
#                    sha1         Authentication Only with SHA1 Integrity
#                    all          All the encryptions
#
# OUT: SUCCESS/ERROR
#############################################################
proc DisGrIpsecEncr {host group encryptType} {

   global cmdOut
   set cmdOut ""
   set encrList ""

   set prompt "CES\\(config-group/ipsec\\)\#"
   set err_count [GetGlobalErr]

   EnterGrIpsecLevel $host $group

   if {$encryptType == "all" } {
       Exec "no encryption ?" "${prompt}no encryption " $host 0 20 0
       foreach line [split $cmdOut "\n"] {
           if {[regexp -nocase {^[\r\t ]+([a-zA-Z0-9\-]+)[\t ]+.*} $line all encrType] == 1 &&\
                   $encrType != "ike"} {
               lappend encrList $encrType
           }
      } 
       
       Exec "[lindex $encrList 0]" $prompt $host
       for {set i 1} {$i < [llength $encrList]} {incr i} {
           Exec "no encryption [lindex $encrList $i]" $prompt $host
       }
       
   } else {
       Exec "no encryption $encryptType" $prompt $host
   }
       SetCliLevel "CONFIG" $host
   
   return [CheckGlobalErr $err_count]
}

#############################################################
# EnaGrIpsecIkeEncr: Enables the the encryption algorithm for IpSec Group.
#
# NOTE: The encryption type must be first enabled with CLI command: 
#       CES(config)#ipsec encryption ...
# 
# IN:  host:        (management IP)/(terminal server Ip:port)
#      group:       Group name.
#      encryptType: Encryption type:  
#                    128aes-group2  AES 128 with group 2 (1024-bit prime)
#                    128aes-group5  AES 128 with Group 5 (1536-bit prime)
#                    128aes-group8  AES 128 with Group 8 (ECC 283-bit field)
#                    256aes-group5  AES 256 with Group 5(1536-bit prime)
#                    256aes-group8  AES 256 with Group 8 (ECC 283-bit field)
#                    3des-group2    Triple DES with Group 2 (1024-bit prime)
#                    3des-group7    Triple DES with Group 7 (ECC 163-bit field)
#                    des56-group1   56bit DES with Group 1 (768-bit prime)
#                    all          All the encryptions
#
# OUT: SUCCESS/ERROR
#############################################################
proc EnaGrIpsecIkeEncr {host group encryptType} {

   global cmdOut
   set cmdOut ""
   set encrList ""
   set prompt "CES\\(config-group/ipsec\\)\#"

   set err_count [GetGlobalErr]
   EnterGrIpsecLevel $host $group

   if {$encryptType == "all" } {
      Exec "encryption ike ?" "${prompt}encryption ike " $host 0 20 0
      foreach line [split $cmdOut "\n"] {
         if {[regexp -nocase {^[\r\t ]+([a-zA-Z0-9\-]+)[\t ]+.*} $line all encrType] == 1} {
            lappend encrList $encrType 
         }
      } 
      Exec "[lindex $encrList 0]" $prompt $host
      for {set i 1} {$i < [llength $encrList]} {incr i} {
         Exec "encryption ike [lindex $encrList $i]" $prompt $host
      }

   } else {
       Exec "encryption ike $encryptType" $prompt $host
   }

   SetCliLevel "CONFIG" $host
   return [CheckGlobalErr $err_count]
}


#############################################################
# DisGrIpsecIkeEncr: Disables the the encryption algorithm for IpSec Group.
#
# IN:  host:        (management IP)/(terminal server Ip:port)
#      group:       Group name.
#      encryptType: Encryption type:  
#                    128aes-group2  AES 128 with group 2 (1024-bit prime)
#                    128aes-group5  AES 128 with Group 5 (1536-bit prime)
#                    128aes-group8  AES 128 with Group 8 (ECC 283-bit field)
#                    256aes-group5  AES 256 with Group 5(1536-bit prime)
#                    256aes-group8  AES 256 with Group 8 (ECC 283-bit field)
#                    3des-group2    Triple DES with Group 2 (1024-bit prime)
#                    3des-group7    Triple DES with Group 7 (ECC 163-bit field)
#                    des56-group1   56bit DES with Group 1 (768-bit prime)
#                    all          All the encryptions
#
# OUT: SUCCESS/ERROR
#############################################################
proc DisGrIpsecIkeEncr {host group encryptType} {

   global cmdOut
   set cmdOut ""
   set encrList ""

   set prompt "CES\\(config-group/ipsec\\)\#"
   set err_count [GetGlobalErr]

   EnterGrIpsecLevel $host $group

   if {$encryptType == "all" } {
       Exec "no encryption ike ?" "${prompt}no encryption ike " $host 0 20 0
       foreach line [split $cmdOut "\n"] {
           if {[regexp -nocase {^[\r\t ]+([a-zA-Z0-9\-]+)[\t ]+.*} $line all encrType] == 1} {
               lappend encrList $encrType
           }
      } 
       
       Exec "[lindex $encrList 0]" $prompt $host
       for {set i 1} {$i < [llength $encrList]} {incr i} {
           Exec "no encryption ike [lindex $encrList $i]" $prompt $host
       }
       
   } else {
       Exec "no encryption ike $encryptType" $prompt $host
   }
       SetCliLevel "CONFIG" $host
   
   return [CheckGlobalErr $err_count]
}


#############################################################
# GrIpsecShow: Display group IPSEC configuration.
#              Returns the output of CLI command.
#
# IN:  host:  (management IP)/(terminal server Ip:port)
#      group: Group name.
#
# OUT: <CLI command output>/ERROR
#############################################################
proc GrIpsecShow {host group} {

   global cmdOut
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   Exec "show groups ipsec $group" "CONFIG" $host   
   
   if {[CheckGlobalErr $err_count] != "ERROR"} {
      return $cmdOut
   } else {
      return "ERROR"
   }
}



################
# Group L2F
################

#############################################################
# EnterGrL2fLevel: Enter into Group L2F setup level.
# 
# IN:  host:  (management IP)/(terminal server Ip:port)
#      group: Group name.
#
# OUT: SUCCESS/ERROR
#############################################################
proc EnterGrL2fLevel { host {group "/Base"}} {
  
   set prompt "CES\\(config-group/l2f\\)\#"

   set err_count [GetGlobalErr]
   
   SetCliLevel "CONFIG" $host
   
   Exec "group l2f $group" $prompt $host

   return [CheckGlobalErr $err_count]

}


#############################################################
# GrL2fAuth: Enable authentication methods (chap, pap).
# 
# IN:  host:      (management IP)/(terminal server Ip:port)
#      group:     Group name.
#      auth_type: <pap, chap, no_pap, no_chap> authentication
#                 when no_pap or no_chap, disables the auth method
#
# OUT: SUCCESS/ERROR
#############################################################
proc GrL2fAuth {host group auth_type} {

   global cmdOut
   set prompt "CES\\(config-group/l2f\\)\#"

   set err_count [GetGlobalErr]
   
   EnterGrL2fLevel $host $group
   
   switch $auth_type {
      
      "pap" {
         Exec "auth pap" $prompt $host
      }
      "chap" {
         Exec "auth chap" $prompt $host
      }
      "no_pap" {
         Exec "no auth pap" $prompt $host
      }
      "no_chap" {
         Exec "no auth chap" $prompt $host
      }
      
   }

   SetCliLevel "CONFIG" $host

   return [CheckGlobalErr $err_count]   

}

#############################################################
# EnterGrPptpLevel: Enter into Group PPTP setup level.
# 
# IN:  host:  (management IP)/(terminal server Ip:port)
#      group: Group name.
#
# OUT: SUCCESS/ERROR
#############################################################
proc EnterGrPptpLevel { host {group "/Base"}} {
  
   set prompt "CES\\(config-group/pptp\\)\#"

   set err_count [GetGlobalErr]
   
   SetCliLevel "CONFIG" $host
   
   Exec "group pptp $group" $prompt $host

   return [CheckGlobalErr $err_count]

}

#############################################################
# GrL2fAuth: Enable authentication methods (chap, pap).
# 
# IN:  host:      (management IP)/(terminal server Ip:port)
#      group:     Group name.
#      auth_type: <pap, chap, no_pap, no_chap> authentication
#                 when no_pap or no_chap, disables the auth method
#
# OUT: SUCCESS/ERROR
#############################################################
proc GrPptpAuth {host group auth_type} {

   global cmdOut
   set prompt "CES\\(config-group/pptp\\)\#"

   set err_count [GetGlobalErr]
   
   EnterGrPptpLevel $host $group
   
   switch $auth_type {
      
      "pap" {
         Exec "auth pap" $prompt $host
      }
      "chap" {
         Exec "auth chap" $prompt $host
      }
      "no_pap" {
         Exec "no auth pap" $prompt $host
      }
      "no_chap" {
         Exec "no auth chap" $prompt $host
      }
      
   }

   SetCliLevel "CONFIG" $host

   return [CheckGlobalErr $err_count]   

}

#############################################################
# PptpAuth: Enable global authentication methods (chap, pap).
# 
# IN:  host:      (management IP)/(terminal server Ip:port)
#      auth_type: <pap, chap, no_pap, no_chap> authentication
#                 when no_pap or no_chap, disables the auth method
#
# OUT: SUCCESS/ERROR
#############################################################
proc PptpAuth {host auth_method} {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   
   switch -- $auth_method {
      "chap" {
         Exec "pptp authentication $auth_method" "CONFIG" $host
      }
      "pap" {
         Exec "pptp authentication $auth_method" "CONFIG" $host
      }
      "no_chap" {
         Exec "no pptp authentication chap" "CONFIG" $host
      }
      "no_pap" {
         Exec "no pptp authentication pap" "CONFIG" $host
      }
   }
  
   return [CheckGlobalErr $err_count]
}
