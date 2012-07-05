#############################################################
# Brance Office Group relating procedures
#
# ##
# #bo-grp
# ##################################
# Procedures:
#
# AddBoGroup {groupName host}
# DelBoGroup {groupName host}
# ShowBoGroup {groupName host}
#
##############################
# Acelib procedures related to BO Group Connectivity
#########
#EnterBoGroupConnLevel { host {grName "/Base"} }
#SetNailedUpState { host grName state }
#SetBoGroupIdleTmeout { host grName timeout }
#
#
############################## 
# Acelib procedures relating to BO Group Ipsec
#########
#
# EnterBoGroupIpsecLevel { host {grName "/Base"}}
# SetBoGroupIpsecDFBit { host gr_name df_bit}
# SetBoGroupCompresion { host gr_name compresion }
# # ExitBoGroupIpsecLevel { host }. OBSOLATD. Use SetCliLevel instead.
# EnaBoGrpEncrType {host groupName encryptType}
# DisBoGrpEncrType {host groupName encryptType}
# GetAvailableBoGrpEncr {host groupName}
# EnaBoGrpIkeEncrType {host groupName encryptType}
# GetAvailableBoGrpIkeEncr {host groupName}
# EnaAggressiveMode {host groupName}
# DisAggressiveMode {host groupName}
# EnaVendorId {host groupName}
# DisVendorId {host groupName}
# SetRekeyTimeout {host groupName timeout}
#############################################################
############################## 
# Acelib procedures relating to BO Group RIP
#########
# EnterBoGroupRipLevel {  host {grName "/Base"} }
# ExportBoGroupBoStaticRoutes { host boGroup cost }
# DisExportBoGroupBoStaticRoutes { host boGroup }
#############################################################
#############################################################
# AddBoGroup: Adds new branch office group.
#
# IN:  groupName: group name
#      host:      (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc AddBoGroup {groupName host} {
   global cmdOut
   set cmdOut ""

   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
        
   Exec "bo-group add $groupName" "CONFIG" $host
   if { [regexp -nocase {Incorrect Group Name Format} $cmdOut msg] == 1} {
      ErrCheck [list "ERROR: \n---$msg---"] "AddBoGroup"           
   }

   return [CheckGlobalErr $err_count]
}


#############################################################
# DelBoGroup: Deletes a branch office group.
#
# IN:  groupName: group name
#      host:      (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc DelBoGroup {groupName host} {

   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
        
   Exec "no bo-group $groupName" "CONFIG" $host

   return [CheckGlobalErr $err_count]

}


#############################################################
# ShowBoGroup: Displays all the settings for a BO Group.
#
# IN:  groupName: group name
#      host:      (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#
#############################################################
proc ShowBoGroup {groupName host} {

   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
        
   Exec "show bo-group $groupName" "CONFIG" $host

   return [CheckGlobalErr $err_count]
}


#############################################################
# EnterBoGroupConnLevel: enters to branch office group ipsec config CLI level
#
# IN:  host:   (management IP)/(terminal server Ip:port)
#      grName: group name. Default group: '/Base'
#
# OUT: SUCCESS/ERROR
#############################################################
proc EnterBoGroupconnLevel {  host {grName "/Base"}} {

   set err_count [GetGlobalErr]

   set prompt "CES\\(config-bo_group/con\\)\#"

   SetCliLevel "CONFIG" $host

   Exec "bo-group connectivity $grName" $prompt $host

   return [CheckGlobalErr $err_count] 
}

#############################################################
# SetNailedUpState: Enables/disables nailed up feature for a bo-group
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      grName: Group name
#      state:   <enable/disable>
#
# OUT: SUCCESS/ERROR
#############################################################
proc SetNailedUpState { host grName state } {

   set err_count [GetGlobalErr]

   EnterBoGroupconnLevel $host $grName
   
   set prompt "CES\\(config-bo_group/con\\)\#"
   
   switch $state {
      "enable" { Exec "nailed-up" $prompt $host }
      "disable" { Exec "no nailed-up" $prompt $host }
   }
   
   SetCliLevel "CONFIG" $host

   return [CheckGlobalErr $err_count]
}


#############################################################
# SetBoGroupIdleTimeout: Set the IdleTimeout for agroup
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      grName:  Group name
#      timeout: <hh:mm:ss> idle-timeout
#
# OUT: SUCCESS/ERROR
#############################################################
proc SetBoGroupIdleTimeout { host grName timeout } {
   set err_count [GetGlobalErr]

   EnterBoGroupconnLevel $host $grName
   
   set prompt "CES\\(config-bo_group/con\\)\#"
   
   Exec "idle-timeout $timeout" $prompt $host
   
   SetCliLevel "CONFIG" $host

   return [CheckGlobalErr $err_count]

}


#############################################################
# EnterBoGroupIpsecLevel: enters to branch office group ipsec config CLI level
#
# IN:  host:   (management IP)/(terminal server Ip:port)
#      grName: group name. Default group: '/Base'
#
# OUT: SUCCESS/ERROR
#############################################################
proc EnterBoGroupIpsecLevel { host {grName "/Base"}} {

   set err_count [GetGlobalErr]

   set prompt "CES\\(config-bo_group/ipsec\\)\#"
    
   SetCliLevel "CONFIG" $host

   Exec "bo-group ipsec $grName" $prompt $host

   return [CheckGlobalErr $err_count] 
}


#############################################################
# EnterBoGroupIpsecLevel: goes back to CONFIG CLI level from
#                         branch office group ipsec config CLI level
#
# IN:  host: (management IP)/(terminal server Ip:port)
# 
# OUT: SUCCESS/ERROR
#
# NOTE: OBSOLATED. Use instead SetCliLevel proc.
#############################################################
proc ExitBoGroupIpsecLevel { host } {
    Exec "exit" "CONFIG" $host    
}


#############################################################
# SetBoGroupIpsecDFBit: Specifies DF-bit usage for an ipsec bo-group
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      gr_name: Group name
#      df_bit:  <CLEAR/COPY/SET>.  Specifies DF-bit usage
#
# OUT: SUCCESS/ERROR
#############################################################
proc SetBoGroupIpsecDFBit { host gr_name df_bit} {
   set err_count [GetGlobalErr]

   EnterBoGroupIpsecLevel $host $gr_name
   set prompt "CES\\(config-bo_group/ipsec\\)\#"

   Exec "df-bit $df_bit" $prompt $host

   SetCliLevel "CONFIG" $host

   return [CheckGlobalErr $err_count]
}

#############################################################
# SetBoGroupCompress: Enables/disables compression for an ipsec bo-group
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      gr_name: Group name
#      df_bit:  <enable/no_enable>
#
# OUT: SUCCESS/ERROR
#############################################################
proc SetBoGroupCompress { host gr_name compress } {
   set err_count [GetGlobalErr]

   EnterBoGroupIpsecLevel $host $gr_name
   set prompt "CES\\(config-bo_group/ipsec\\)\#"

   if {$compress == "no_enable"} {
      Exec "no compress" $prompt $host
   } elseif {$compress == "enable"} {
      Exec "compress" $prompt $host
   } else {
      ErrCheck "ERROR bad parameter: compress = $compress"
   }

   SetCliLevel "CONFIG" $host

   return [CheckGlobalErr $err_count]
}


#############################################################
# EnaBoGrpEncrType: enables the encryption algorithm
#
# IN:  host:        (management IP)/(terminal server Ip:port)
#      groupName:   Group name
#      encryptType: (type of encryption)/all
#
# OUT: SUCCESS/ERROR
#############################################################
proc EnaBoGrpEncrType {host groupName encryptType} {

   global cmdOut
   set cmdOut ""
   set encrList ""

   set err_count [GetGlobalErr]

   set prompt "CES\\(config-bo_group/ipsec\\)\#"
   EnterBoGroupIpsecLevel $host $groupName

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
      Exec "exit" "CONFIG" $host
   }

   return [CheckGlobalErr $err_count]
}


#############################################################
# DisBoGrpEncrType: disables the encryption algorithm
#
# IN:  host:        (management IP)/(terminal server Ip:port)
#      groupName:   Group name
#      encryptType: (type of encryption)/all
#
# OUT: SUCCESS/ERROR
#############################################################
proc DisBoGrpEncrType {host groupName encryptType} {

   global cmdOut
   set cmdOut ""
   set encrList ""

   set err_count [GetGlobalErr]

   set prompt "CES\\(config-bo_group/ipsec\\)\#"
   EnterBoGroupIpsecLevel $host $groupName

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
      Exec "exit" "CONFIG" $host
   }

   return [CheckGlobalErr $err_count]
}


#############################################################
# GetAvailableBoGrpEncr: Gets the available encryption algorithms
#                        for a branch office group. 
#
# IN:  host:        (management IP)/(terminal server Ip:port)
#      groupName:   Group name
#
# OUT: NONE/ERROR/<list of encryption type>
#############################################################
proc GetAvailableBoGrpEncr {host groupName} {

   global cmdOut
   set cmdOut ""
   set encrList ""

   set err_count [GetGlobalErr]

   set prompt "CES\\(config-bo_group/ipsec\\)\#"
   EnterBoGroupIpsecLevel $host $groupName

   Exec "encryption ?" "${prompt}encryption " $host 0 20 0
   foreach line [split $cmdOut "\n"] {
      if {[regexp -nocase {^[\r\t ]+([a-zA-Z0-9\-]+)[\t ]+.*} $line all encrType] == 1 &&\
              $encrType != "ike"} {
         lappend encrList $encrType 
      }
   }
   Exec "\b\b\b\b\b\b\b\b\b\b\b\b\b" $prompt $host
   
   if {[CheckGlobalErr $err_count] == "ERROR"} {
      return "ERROR"
   } 
   if {[llength $encrList] == 0} {
      return "NONE"
   } else {
      return $encrList
   }
}


#############################################################
# EnaBoGrpIkeEncrType: sets IKE encryption algoritm and Diffie-Hellman
#                      group for the IPsec tunneling
#
# IN:  host:        (management IP)/(terminal server Ip:port)
#      groupName:   Group name
#      encryptType: (type of encryption)/all
#
# OUT: SUCCESS/ERROR
#############################################################
proc EnaBoGrpIkeEncrType {host groupName encryptType} {

   set err_count [GetGlobalErr]

   set prompt "CES\\(config-bo_group/ipsec\\)\#"
   EnterBoGroupIpsecLevel $host $groupName

   Exec "encryption ike $encryptType" $prompt $host
   Exec "exit" "CONFIG" $host

   return [CheckGlobalErr $err_count]
}

#############################################################
# GetAvailableBoGrpIkeEncr: Gets the available IKE encryption algorithms
#                           for a branch office group. 
#
# IN:  host:        (management IP)/(terminal server Ip:port)
#      groupName:   Group name
#
# OUT: NONE/ERROR/<list of encryption type>
#############################################################
proc GetAvailableBoGrpIkeEncr {host groupName} {

   global cmdOut
   set cmdOut ""
   set encrList ""

   set err_count [GetGlobalErr]

   set prompt "CES\\(config-bo_group/ipsec\\)\#"
   EnterBoGroupIpsecLevel $host $groupName

   Exec "encryption ike ?" "${prompt}encryption ike " $host 0 20 0
   foreach line [split $cmdOut "\n"] {
      if {[regexp -nocase {^[\r\t ]+([a-zA-Z0-9\-]+)[\t ]+.*} $line all encrType] == 1} {
         lappend encrList $encrType
      }
   }
   Exec "\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b" $prompt $host
   
   if {[CheckGlobalErr $err_count] == "ERROR"} {
      return "ERROR"
   } 
   if {[llength $encrList] == 0} {
      return "NONE"
   } else {
      return $encrList
   }
}


#############################################################
# EnaAggressiveMode: enable aggressive mode ISAKMP initial contact payload accept
#
# IN:  host:      (management IP)/(terminal server Ip:port)
#      groupName: Group name
#
# OUT: SUCCESS/ERROR
#############################################################
proc EnaAggressiveMode {host groupName} {

   set prompt "CES\\(config-bo_group/ipsec\\)\#"

   set err_count [GetGlobalErr]

   EnterBoGroupIpsecLevel $host $groupName
   Exec "initial-contact enable" $prompt $host
   Exec "exit" "CONFIG" $host

   return [CheckGlobalErr $err_count]
}


#############################################################
# DisAggressiveMode: disable aggressive mode ISAKMP initial contact payload accept
#
# IN:  host:      (management IP)/(terminal server Ip:port)
#      groupName: Group name
#
# OUT: SUCCESS/ERROR
#############################################################
proc DisAggressiveMode {host groupName} {

   set prompt "CES\\(config-bo_group/ipsec\\)\#"

   set err_count [GetGlobalErr]

   EnterBoGroupIpsecLevel $host $groupName
   Exec "no initial-contact enable" $prompt $host
   Exec "exit" "CONFIG" $host

   return [CheckGlobalErr $err_count]
}


#############################################################
# EnaVendorId: enables vendor ID
#
# IN:  host:        (management IP)/(terminal server Ip:port)
#      groupName:   Group name
#
# OUT: SUCCESS/ERROR
#############################################################
proc EnaVendorId {host groupName} {

   set prompt "CES\\(config-bo_group/ipsec\\)\#"

   set err_count [GetGlobalErr]

   EnterBoGroupIpsecLevel $host $groupName
   Exec "vendor-id" $prompt $host
   Exec "exit" "CONFIG" $host

   return [CheckGlobalErr $err_count]
}


#############################################################
# DisVendorId: disables vendor ID
#
# IN:  host:        (management IP)/(terminal server Ip:port)
#      groupName:   Group name
#
# OUT: SUCCESS/ERROR
#############################################################
proc DisVendorId {host groupName} {

   set prompt "CES\\(config-bo_group/ipsec\\)\#"

   set err_count [GetGlobalErr]

   EnterBoGroupIpsecLevel $host $groupName
   Exec "no vendor-id" $prompt $host
   Exec "exit" "CONFIG" $host

   return [CheckGlobalErr $err_count]
}

#############################################################
# SetRekeyTimeout: sets rekey timeout
#
# IN:  host:        (management IP)/(terminal server Ip:port)
#      groupName:   Group name
#      timeout:     <00:02:00 - 23:59:59>  - the limit of 
#            the lifetime of a single key for encryption data
#
# OUT: SUCCESS/ERROR
#############################################################
proc SetRekeyTimeout {host groupName timeout} {

   set prompt "CES\\(config-bo_group/ipsec\\)\#"

   set err_count [GetGlobalErr]

   EnterBoGroupIpsecLevel $host $groupName
   Exec "rekey timeout $timeout" $prompt $host
   Exec "exit" "CONFIG" $host

   return [CheckGlobalErr $err_count]
}

#############################################################
# EnterBoGroupRipLevel: entering rip level configuration for a BO group
#
# IN:  host:        (management IP)/(terminal server Ip:port)
#      grName:   Group name
#
# OUT: SUCCESS/ERROR
#############################################################
proc EnterBoGroupRipLevel {  host {grName "/Base"}} {

   set err_count [GetGlobalErr]

   set prompt "CES\\(config-bo_group/rip\\)\#"

   SetCliLevel "CONFIG" $host

   Exec "bo-group rip $grName" $prompt $host

   return [CheckGlobalErr $err_count] 
}


#############################################################
# ExportBoGroupBoStaticRoutes: enables exporting of BO static routes and establish a cost for them
#
# IN:  host:      (management IP)/(terminal server Ip:port)
#      boGroup:   Group name
#      cost:      cost <1-15>
#
# OUT: SUCCESS/ERROR
#############################################################
proc ExportBoGroupBoStaticRoutes { host boGroup cost } {

   set err_count [GetGlobalErr]

   EnterBoGroupRipLevel $host $boGroup

   set prompt "CES\\(config-bo_group/rip\\)\#"
   
   Exec "export bo-static-metric $cost" $prompt $host
   
   SetCliLevel "CONFIG" $host
   
}


proc DisExportBoGroupBoStaticRoutes { host boGroup } {
   
   set err_count [GetGlobalErr]

   EnterBoGroupRipLevel $host $boGroup

   set prompt "CES\\(config-bo_group/rip\\)\#" 
    
   Exec "no export bo-static-routes-metric" $prompt $host
   
   SetCliLevel "CONFIG" $host
}
