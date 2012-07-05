###########################################
# Procedures relating to VLAN subinterfaces setup
#
# SetDot1QState { host interface state }
# EnterVLANSubifLevel { host interface subinterface }
# SetVLANSubifId { host interface subinterface vlan_id }
# SetVLANSubifIp { host interface subinterface ip_address {netmask "255.255.255.0"} }
# SetVLANSubifFilter { host interface subinterface filtername }
# AddVLANSubif { host interface subinterface vlan_id ip_address filtername }
# EnableSubif { host interface subinterface }
# DelVLANSubif { host interface subinterface }
# SetIfQoSDSCPMapping { host if_type if_id  state flow {type ""} } 
# SetQoSDSCPDot1pMap { host word }
# SetQoSDot1pDSCPMap { host word }
###########################################

proc SetDot1QState { host interface state } {
   set err_count [GetGlobalErr]
   EnterConfigIfLevel "fastethernet" $interface $host
   switch $state {
      "enable" {
         Exec "dot1q enable" "CONFIGIF" $host
      }
      "disable" {
         Exec "no dot1q enable" "CONFIGIF" $host
      }
   }
   SetCliLevel "PRIVILEGE" $host
   return [CheckGlobalErr $err_count]
}

proc EnterVLANSubifLevel { host interface subinterface } {
   set err_count [GetGlobalErr]
   set prompt "CES\\(config-subif\\)\#"
   EnterConfigIfLevel "fastethernet" $interface $host
   Exec "subinterface $subinterface" $prompt $host
   return [CheckGlobalErr $err_count]
}


proc SetVLANSubifId { host interface subinterface vlan_id } {
   set err_count [GetGlobalErr]
   set prompt "CES\\(config-subif\\)\#"
   EnterVLANSubifLevel $host $interface $subinterface
   Exec "encapsulation dot1q $vlan_id" $prompt $host
   SetCliLevel "PRIVILEGE" $host
   return [CheckGlobalErr $err_count]
}

proc SetVLANSubifIp { host interface subinterface ip_address netmask } {
   set err_count [GetGlobalErr]
   set prompt "CES\\(config-subif\\)\#"
   EnterVLANSubifLevel $host $interface $subinterface
   Exec "ip address $ip_address $netmask" $prompt $host
   SetCliLevel "PRIVILEGE" $host
   return [CheckGlobalErr $err_count]
}

proc SetVLANSubifFilter { host interface subinterface filtername } {
   set err_count [GetGlobalErr]
   set prompt "CES\\(config-subif\\)\#"
   EnterVLANSubifLevel $host $interface $subinterface
   Exec "filter $filtername" $prompt $host
   SetCliLevel "PRIVILEGE" $host
   return [CheckGlobalErr $err_count]
}

proc AddVLANSubif { host interface subinterface vlan_id ip_address filtername {netmask "255.255.255.0"} } {
   set err_count [GetGlobalErr]
   EnterVLANSubifLevel $host $interface $subinterface
   SetVLANSubifId $host $interface $subinterface $vlan_id
   SetVLANSubifIp $host $interface $subinterface $ip_address $netmask
   SetVLANSubifFilter $host $interface $subinterface $filtername
   SetCliLevel "PRIVILEGE" $host
   return [CheckGlobalErr $err_count]
}

proc EnableSubif { host interface subinterface } {
   set err_count [GetGlobalErr] 
   EnterConfigIfLevel "fastethernet" $interface $host
   Exec "subinterface $subinterface enable" "CONFIGIF" $host
   SetCliLevel "PRIVILEGE" $host
   return [CheckGlobalErr $err_count]

}

proc DelVLANSubif { host interface subinterface } {
   set err_count [GetGlobalErr] 
   EnterConfigIfLevel "fastethernet" $interface $host
   Exec "no subinterface $subinterface" "CONFIGIF" $host
   SetCliLevel "PRIVILEGE" $host
   return [CheckGlobalErr $err_count]
}

#############################################################
# SetIfTagging: Set the interface tagging behaviour
#
# IN:  host:          (management IP)/(terminal server Ip:port)
#      interface:   <0-6>/<1-4>  slot number / port number
#      data_flux:   <egress/ingress>
#      state:       <tag/untag>
#    
# OUT: SUCCESS/ERROR
#############################################################
proc SetIfTagging { host interface data_flux state } {
   set err_count [GetGlobalErr]
   EnterConfigIfLevel "fastethernet" $interface $host
   switch $data_flux {
      "egress" {
         if { $state == "tag" } {
            Exec "no dot1q interface untag egress" "CONFIGIF" $host
         } else {
            Exec "dot1q interface untag egress" "CONFIGIF" $host
         }
      }
      
      "ingress" {
         if { $state == "tag" } {
            Exec "no dot1q interface untag ingress" "CONFIGIF" $host
         } else {
            Exec "dot1q interface untag ingress" "CONFIGIF" $host
         }
      }
   }

   SetCliLevel "PRIVILEGE" $host
   return [CheckGlobalErr $err_count]
}

#############################################################
# SetIfQoSDSCPMapping: Set the interface tagging behaviour
#
# IN:  host:   (management IP)/(terminal server Ip:port)
#      if_id:  <0-6>/<1-4>  slot number / port number
#      state:  <enable/disable>
#      flow:   <egress/ingress>
#      type:   <custom/standard>
#    
# OUT: SUCCESS/ERROR
#############################################################
proc SetIfQoSDSCPMapping { host if_id  state flow {type ""} } {
   set err_count [GetGlobalErr]
   EnterConfigIfLevel "fastethernet" $if_id $host
   switch $state {
      "enable" {
         if { $flow == "egress" } {
            Exec "qos egress-dscp-map $type" "CONFIGIF" $host
         } else {
            Exec "qos ingress-dscp-map $type" "CONFIGIF" $host
         }
      }
      "disable" {
         if { $flow == "egress" } {
            Exec "no qos egress-dscp-map" "CONFIGIF" $host
         } else {
            Exec "no qos ingress-dscp-map" "CONFIGIF" $host
         }
      }
   }
   
   SetCliLevel "Privilege" $host
   return [CheckGlobalErr $err_count]
}

#############################################################
# SetQoSDSCPDot1pMap: Set the interface tagging behaviour
#
# IN:  host:  (management IP)/(terminal server Ip:port)
#      word:  dscp-dot1p mapping
#    
# OUT: SUCCESS/ERROR
#############################################################
proc SetQoSDSCPDot1pMap { host word } {
   set err_count [GetGlobalErr]
   SetCliLevel "CONFIG" $host
   Exec "qos dscp-dot1p-map $word" "CONFIG" $host
   SetCliLevel "PRIVILEGE" $host
   return [CheckGlobalErr $err_count]
}

#############################################################
# SetQoSDot1pDSCPMap: Set the interface tagging behaviour
#
# IN:  host:  (management IP)/(terminal server Ip:port)
#      word:  dot1p-dscp mapping
#    
# OUT: SUCCESS/ERROR
#############################################################
proc SetQoSDot1pDSCPMap { host word } {
   set err_count [GetGlobalErr]
   SetCliLevel "CONFIG" $host
   Exec "qos dot1p-dscp-map $word" "CONFIG" $host
   SetCliLevel "PRIVILEGE" $host
   return [CheckGlobalErr $err_count]
}





