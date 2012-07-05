###########################################
# Procedures relating to network cards setup
#
#
# GetInterfaceSlot { interfaceType host}
#
# EnterConfigIfLevel { interfaceType interfaceID host }
# ExitConfigIfLevel { host }
# SetIfIpAddrType { type host }
# SetIfIpAddr { interfaceType interfaceID ipAddr ipMask host }
# SetMngIpAddr {host ipAddr}
# GetMngIpAddr {host}
# DelIfIpAddr { interfaceType interfaceID ipAddr ipMask host }
# ExecIfIpDhcp { dhcpCmd host }
# SetIfIpDhcp { varName varValue host }
# ShowInterface {interfaceType interfaceId host } 
# EnableInterface {interfaceType interfaceId host}
# DisableInterface {interfaceType interfaceId host}
# SetIfPrivatePublic {interfaceType interfaceID host}
# SetIfMtu {interfaceType interfaceID mtu host}
# SetIfDefaultMtu {interfaceType interfaceID host}
# SetInterfaceFilter { interfaceType interfaceID filterName host }
# ResetInterfaceFilter {interfaceType interfaceID host}
# SetIfTcpMss {interfaceType interfaceID tcpMss host}
# SetIfDefaultTcpMss {interfaceType interfaceID host}
# SetIfTcpMssState {interfaceType interfaceID tcpMss host}
# SetEthIfDuplex {host interfaceID duplexType}
# SetEthIfSpeed {host interfaceID speed}
# SetIfDuplex {host interfaceType interfaceID duplexType}
# SetIfSpeed {host interfaceType interfaceID duplexType}
# GetIfEthMac {IfIpAddr host}
# GetEthInfo {host if_id data_to_get}
# GetIfPacketStats { host IfIpAddr }
# AddIfMultinetIp { host interfaceID ipAddr ipMask } 
# DelIfMultinetIp { host interfaceID ipAddr ipMask }
#
#
# #pppoe
# SetIfPppoeAdminState {host ifId adminState}
# EnableIfPppoe { ifId host }
# DisableIfPppoe { ifId host }
# SetIfPppoeAuth { ifId authType host }
# SetIfPppoeServiceName { ifId service_name host }
# EnableIfPppoeOnDemand { ifId host }
# DisableIfPppoeOnDemand { ifId host }
# SetPppoeIdleTimeOut { ifId time host }
# SetPppoeLcpEchoInterval { ifId time host }
# SetPppoeLcpEchoFaultThreshold { ifId time host }
# SetPppoeCost { ifId cost host }
# ConfigIfPppoeUserIdentif {ifId user passwd host }
#
# #- global pppoe config procs:
# CongfigIfPppod {ifId authType user passwd host }
# CleanIfPppoe { ifId host }
# ShowIfPppoe { ifId host } 
# GetPPPoEInfo {host if_id data_to_get}
#
#
# # WAN card
# SetWanState { host if_id state }
# SetWanEncapsulation {if_id enc_type host}
# GetWanInfo {host if_id data_to_get}
#
# #- ppp
#
# SetPppEncapsulation {ifId host} 
# SetPppAuthentication {ifId authType host} 
# SetPppIpLocal {ifId ip mask host}
# SetPppUsername {ifId username host} 
# SetPppPassword {ifId password host}
# SetPppIpRemote {ifId ip host} --- ip variable can be an IP address or "negotiated" string
# ConfigIpOverPPPLink {if_id auth_type user pass local_ip mask remote_ip host}
#
# #- frame-relay for serial interface
# EnterFrameRelaySubIfLevel { interfaceID subinterfaceID host }
# DelFrameRelaySubIf { interfaceID subinterfaceID host }
# ConfigIpOverFRLink {fr_if sub_if_id local_wan_ip netmask remote_wan_ip dlci conn_type lmi_type host}
# SetLineFormat { host if_id line_type {framing ""} }
# SetClockSource { host if_id line_type mode }
# SetHdlcPolarity { host if_id polarity }
#
# #-  rip
# EnableIfRip {interfaceID host}
# DisableIfRip {interfaceID host}
# IfRipSendVersionNone {interfaceID host}
# EnableIfRipExportOspf {interfaceID host}
# DisableIfRipExportOspf {interfaceID host}
# EnableIfRipExportBoStaticRoutes { host interfaceType interfaceID cost }
# Disable IfRipExportBoStaticRoutes { host interfaceType interfaceID }
# 
#
# #- ospf // interfaceType = fastethernet
# EnableIfOspf {interfaceID host}
# DisableIfOspf {interfaceID host}
#
# #- vrrp
# EnableIfVrrp { host interfaceType interfaceID }
# DisableIfVrrp { host interfaceType interfaceID }
# SetMasterIfVrrp { host interfaceType interfaceID }
# SetBackupIfVrrp { host interfaceType interfaceID vrrpIP {priority notSet}}
#
# #- group 
# AddInterfaceGroup {host ifGroupName} 
# DelInterfaceGroup {host ifGroupname}
# AddIPInterfaceGroup {host ifGroupName ip} 
# DelIPInterfaceGroup {host ifGroupName ip} 
# EnableInterfaceGroup {host ifGroupName}
# DisableInterfaceGroup {host ifGroupname}
###########################################



#############################################################
# GetInterfaceSlot:  Gets the slot number / port number for an interface
#                    or for a group of interfaces with type: 'interfaceType'
# 
# IN:  interfaceType: interface type in the format known by CES
#                     e.q. fast ethernet interface: FastEthernet
#                          wan interface:           serial
#      host         : (management IP)/(terminal server Ip:port)
#
# OUT: slot number / port number 
#      or a list with slot/port if there are many cards with the same type
#      or NULL or ERROR
#############################################################
proc GetInterfaceSlot { interfaceType host} {
   
   global cmdOut


   SetCliLevel "PRIVILEGE" $host

   set execResult [Exec "Show interface" "PRIVILEGE" $host]

   if {$execResult != "SUCCESS"} {
      return "ERROR"
   }

   set ifSlotPort ""

   foreach line [split $cmdOut "\n"] {
      if {[regexp -nocase "Slot\[\t\ \]+\(\[0-9\]+/\[0-9\]+)\[\t\ \]+-\[\t\ \]+$interfaceType" $line all slotId] == 1} {
         lappend ifSlotPort $slotId
      }
   }

   if {$ifSlotPort == ""} {
      return "NONE"
   }

   return $ifSlotPort
}


#############################################################
# EnterConfigIfLevel (SetCliLevelConfigIf) proc - enters in the config-if menu
# 
# IN:  interfaceType: interface type in the format known by CES
#                     e.q. fast ethernet interface: FastEthernet
#                          wan interface:           serial
#      interfaceID  : <0-6>/<1-4>  slot number / port number
#      host         : (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#
#############################################################
proc EnterConfigIfLevel { interfaceType interfaceID host } {
   if { [SetCliLevel "CONFIG" $host] != "SUCCESS" } {
      lappend rcode "ERROR: Failed SetCliLevel"
      return [ErrCheck $rcode EnterConfigIfLevel] 
   }
   
   #go to config-if menu
   return [Exec "interface $interfaceType $interfaceID" "CONFIGIF" $host]    
}


#############################################################
# OBSOLATED: use SetCliLevel instead
#
# ExitConfigIfLevel (GoBackToConfigLevel) - go back to CONFIG cli 
#                   level (CES(config)# prompt)
#
# IN:  host: (management IP)/(terminal server Ip:port)  
#
# OUT: SUCCESS or ERROR
#
#############################################################
proc ExitConfigIfLevel { host } {
   return [Exec "exit" "CONFIG" $host]
}


#############################################################
# SetIfIpAddrType: Sets IP address type.
#
# IN:  interfaceType: interface type in the format known by CES
#                     e.q. fast ethernet interface: FastEthernet
#                          wan interface:           serial
#      interfaceID:   <0-6>/<1-4>  slot number / port number
#      type:          <dhcp/static>  IP address type
#      host:          (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#
#############################################################
proc SetIfIpAddrType { interfaceType interfaceID type host } {
   
   set errCode "ERROR"
   set errCount 0


   if { [EnterConfigIfLevel $interfaceType $interfaceID $host] != "SUCCESS" } {
      lappend rcode "ERROR: failed EnterConfigIfLevel"
      return [ErrCheck $rcode SetIfIpAddrType] 
   }
   
   if {[Exec "ip address type $type" "CONFIGIF" $host] != "SUCCESS"} {
      incr errCount
   }
   
   if {[ExitConfigIfLevel $host] != "SUCCESS"} {
      incr errCount
   }

   if {$errCount == 0} {
      set errCode "SUCCESS"
   }

   return $errCode
}


#############################################################
# SetIfIpAddr: Sets interface IP address.
#
# IN:  interfaceType: interface type in the format known by CES
#                     e.q. fast ethernet interface: FastEthernet
#                          wan interface:           serial
#      interfaceID:   <0-6>/<1-4>  slot number / port number
#      ipAddr:        A.B.C.D  IP address
#      ipMask:        A.B.C.D  IP subnet mask
#      host:          (management IP)/(terminal server Ip:port) 
#
# OUT: SUCCESS/ERROR
#############################################################
proc SetIfIpAddr { interfaceType interfaceID ipAddr ipMask host } {
   global cmdOut
   
    set err_count [GetGlobalErr]
     
   if { [EnterConfigIfLevel $interfaceType $interfaceID $host] != "SUCCESS" } {
      lappend rcode "ERROR: failed EnterConfigIfLevel"
      return [ErrCheck $rcode SetIfIpAddr] 
   }
   
   if {[Exec "ip address $ipAddr $ipMask" "CONFIGIF" $host] == "SUCCESS"} {
	if { [regexp -nocase {Mask [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+ is not valid} $cmdOut msg] == 1 } {
		lappend rcode "ERROR: CES $host: the ip address is not configured:\n----\n$msg\n----"
		return [ErrCheck $rcode SetIfIpAddr] 
		}
    }
  ExitConfigIfLevel $host
  
  return [CheckGlobalErr $err_count]
}


#############################################################
# SetMngIpAddr: Set the Management IP address from CLI
#
# IN:  ipAddr: A.B.C.D   management IP address
#      host:   (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc SetMngIpAddr { host ipAddr } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   
   Exec "ip address $ipAddr" "CONFIG" $host    

   return [CheckGlobalErr $err_count]   
}

#############################################################
# GetMngIpAddr: Get the Management IP address or mask
#
# IN:      host:    (management IP)/(terminal server Ip:port)
#
# OUT:     mngAdd:  management address
#      or  ERROR
#############################################################
proc GetMngIpAddr {host} {    
    global cmdOut

    SetCliLevel "PRIVILEGE" $host
    
    Exec "show running-config system" "PRIVILEGE" $host    

    set mngAddr ""
    foreach line [split $cmdOut "\n"] {
        if {[regexp {ip address[ \t]+([0-9\.]+)[ \t\r]*$} $line all mngAddr] == 1} {
            if {$mngAddr != "0.0.0.0" && $mngAddr != ""} {
                return $mngAddr
            }
        }
    }
    return [ErrCheck "ERROR: IP for this CES was not set" "GetMngIpAddr"]
}

#############################################################
# DelIfIpAddr: Deletes the IP address of an interface.
#
# IN:  interfaceType: interface type in the format known by CES
#                     e.q. fast ethernet interface: FastEthernet
#                          wan interface:           serial
#      interfaceID:   <0-6>/<1-4>  slot number / port number
#      ipAddr:        A.B.C.D  IP address
#      ipMask:        A.B.C.D  IP subnet mask
#      host:          (management IP)/(terminal server Ip:port) 
#
# OUT: SUCCESS/ERROR
#############################################################
proc DelIfIpAddr { interfaceType interfaceID ipAddr ipMask host } {
   set errCode "ERROR"
   set errCount 0

   if { [EnterConfigIfLevel $interfaceType $interfaceID $host] != "SUCCESS" } {
      lappend rcode "ERROR: failed EnterConfigIfLevel"
      return [ErrCheck $rcode DelIfIpAddr] 
   }
   
   if {[Exec "no ip address $ipAddr $ipMask" "CONFIGIF" $host] != "SUCCESS"} {
      incr errCount
   }
   
   if {[ExitConfigIfLevel $host] != "SUCCESS"} {
      incr errCount
   }

   if {$errCount == 0} {
      set errCode "SUCCESS"
   }

   return $errCode        
}


#############################################################
# ExecIfIpDhcp: Runs cancel or require dhcp client actions.
#               
#
# IN:  interfaceType: interface type in the format known by CES
#                     e.q. fast ethernet interface: FastEthernet
#                          wan interface:           serial
#      interfaceID:   <0-6>/<1-4>  slot number / port number
#      dhcpCmd:       <cancel/reacquire>
#      host:          (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc ExecIfIpDhcp { interfaceType interfaceID dhcpCmd host } {
   set errCode "ERROR"
   set errCount 0

   if { [EnterConfigIfLevel $interfaceType $interfaceID $host] != "SUCCESS" } {
       lappend rcode "ERROR: failed EnterConfigIfLevel"
      return [ErrCheck $rcode ExecIfIpDhcp] 
   }
   
   if {[Exec "ip address dhcp $dhcpCmd" "CONFIGIF" $host] != "SUCCESS"} {
      incr errCount
   }
   
   if {[ExitConfigIfLevel $host] != "SUCCESS"} {
      incr errCount
   }

   if {$errCount == 0} {
      set errCode "SUCCESS"
   }

   return $errCode
}


#############################################################
# SetIfIpDhcp: Sets an dhcp parameter.
#
# IN:  interfaceType: interface type in the format known by CES
#                     e.q. fast ethernet interface: FastEthernet
#                          wan interface:           serial
#      interfaceID:   <0-6>/<1-4>  slot number / port number
#      varName:       cost  The cost of the route to the DHCP server
#      varValue:      <0-65535>
#      host:          (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc SetIfIpDhcp { interfaceType interfaceID varName varValue host } {
   set errCode "ERROR"
   set errCount 0

   if { [EnterConfigIfLevel $interfaceType $interfaceID $host] != "SUCCESS" } {
      lappend rcode "ERROR: failed EnterConfigIfLevel"
      return [ErrCheck $rcode SetIfIpDhcp] 
   }
   
   if {[Exec "ip address dhcp $varName $varValue" "CONFIGIF" $host] != "SUCCESS"} {
      incr errCount
   }
   
   if {[ExitConfigIfLevel $host] != "SUCCESS"} {
      incr errCount
   }

   if {$errCount == 0} {
      set errCode "SUCCESS"
   }

   return $errCode
}


#############################################################
# ShowInterface: Displays interface information.
#
# IN:  interfaceType: interface type in the format known by CES
#                     e.q. fast ethernet interface: FastEthernet
#                          wan interface:           serial
#      interfaceID:   <0-6>/<1-4>  slot number / port number#      
#      host:          (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc ShowInterface { interfaceType interfaceID host } {
   SetCliLevel "PRIVILEGE" $host
   Exec "show interface $interfaceType $interfaceID" "PRIVILEGE" $host 
}


#############################################################
# EnableInterface: Enables interface.
#
# IN:  interfaceType: interface type in the format known by CES
#                     e.q. fast ethernet interface: FastEthernet
#                          wan interface:           serial
#      interfaceID:   <0-6>/<1-4>  slot number / port number#      
#      host:          (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc EnableInterface {interfaceType interfaceId host} {
   SetCliLevel "CONFIG" $host
   Exec "interface $interfaceType $interfaceId enable" "CONFIG" $host
}


#############################################################
# DisableInterface: Disables interface.
#
# IN:  interfaceType: interface type in the format known by CES
#                     e.q. fast ethernet interface: FastEthernet
#                          wan interface:           serial
#      interfaceID:   <0-6>/<1-4>  slot number / port number#      
#      host:          (management IP)/(terminal server Ip:port)
# 
# OUT: SUCCESS/ERROR
#############################################################
proc DisableInterface {interfaceType interfaceId host} {
   SetCliLevel "CONFIG" $host
   Exec "no interface $interfaceType $interfaceId enable" "CONFIG" $host
}


#############################################################
# SetIfPrivatePublic: Set the interface as public or private
#                     CES is not rebooted after setting.
#
# IN:  interfaceType: interface type in the format known by CES
#                     e.q. fast ethernet interface: FastEthernet
#                          wan interface:           serial
#      interfaceID:   <0-6>/<1-4>  slot number / port number
#      type:          <public/private>
#      host:          (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR/NEEDREBOOT
#############################################################
proc SetIfPrivatePublic {interfaceType interfaceID type host} {
   global cmdOut
   set ret_code "ERROR"

   set err_count [GetGlobalErr]

   if {[EnterConfigIfLevel $interfaceType $interfaceID $host] != "SUCCESS"} {
      return [CheckGlobalErr $err_count]
   }   

   set cli_prompt "CES\\(config-if\\)\#"

   if {$type == "public"} {
      Exec "public" $cli_prompt $host  
   } elseif {$type == "private"} {
      Exec "no public" $cli_prompt $host  
   } else {
      ErrCheck [list "ERROR: bad parameter: type = $type. Allowed values: pubic/private"]
   }
   
   if {[regexp -nocase {restart} $cmdOut] == 1 || \
           [regexp -nocase {reboot} $cmdOut] == 1 } {
      set ret_code "NEEDREBOOT"
   }

   SetCliLevel "PRIVILEGE" $host  

   set ok_cli [CheckGlobalErr $err_count]
   if {$ok_cli == "SUCCESS" && $ret_code == "NEEDREBOOT"} {
      return $ret_code
   }
   return $ok_cli

}


#############################################################
# SetIfMtu: Set the Maximum Transmission Unit (packet size).
#
# IN:  interfaceType: interface type in the format known by CES
#                     e.q. fast ethernet interface: FastEthernet
#                          wan interface:           serial
#      interfaceID:   <0-6>/<1-4>  slot number / port number
#      mtu:           <576-1500>  the new value for MTU
#      host:          (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc SetIfMtu {interfaceType interfaceID mtu host} {   
   
   set err_count [GetGlobalErr]

   if {[EnterConfigIfLevel $interfaceType $interfaceID $host] != "SUCCESS"} {
      return [CheckGlobalErr $err_count]
   }   

   set cli_prompt "CES\\(config-if\\)\#"

   Exec "mtu $mtu" $cli_prompt $host  
   
   ExitConfigIfLevel $host   

   return [CheckGlobalErr $err_count]          

}

#############################################################
# SetIfDefaultMtu: Set mtu to default value.
# IN:  interfaceType: interface type in the format known by CES
#                     e.q. fast ethernet interface: FastEthernet
#                          wan interface:           serial
#      interfaceID:   <0-6>/<1-4>  slot number / port number
#      host:          (management IP) / (terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc SetIfDefaultMtu {interfaceType interfaceID host} {
   set err_count [GetGlobalErr]

   if {[EnterConfigIfLevel $interfaceType $interfaceID $host] != "SUCCESS"} {
      return [CheckGlobalErr $err_count]
   }
   
   set cli_prompt "CES\\(config-if\\)\#"

   Exec "no mtu" $cli_prompt $host  
   
   SetCliLevel "PRIVILEGE" $host   

   return [CheckGlobalErr $err_count]  
}


#############################################################
# SetInterfaceFilter: Define interface filter for this interface.
# IN:  interfaceType: interface type in the format known by CES
#                     e.q. fast ethernet interface: FastEthernet
#                          wan interface:           serial
#      interfaceID:   <0-6>/<1-4>  slot number / port number
#      host:          (management IP) / (terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc SetInterfaceFilter { interfaceType interfaceID filterName host } {
   
   set errCode "ERROR"
   set errCount 0

   if { [EnterConfigIfLevel $interfaceType $interfaceID $host] != "SUCCESS" } {
      lappend rcode "ERROR: failed EnterConfigIfLevel"
      return [ErrCheck $rcode SetInterfaceFilter] 
   }
   
   if {[Exec "filter $filterName" "CONFIGIF" $host] != "SUCCESS"} {
      incr errCount
   }
   
   if {[ExitConfigIfLevel $host] != "SUCCESS"} {
      incr errCount
   }

   if {$errCount == 0} {
      set errCode "SUCCESS"
   }

   return $errCode
   
}


#############################################################
# ResetInterfaceFilter: Sets interface filter for this interface 
#                       back to default.
#
# IN:  interfaceType: interface type in the format known by CES
#                     e.q. fast ethernet interface: FastEthernet
#                          wan interface:           serial
#      interfaceID:   <0-6>/<1-4>  slot number / port number
#      host:          (management IP) / (terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc ResetInterfaceFilter { interfaceType interfaceID host } {
   set errCode "ERROR"
   set errCount 0

   if { [EnterConfigIfLevel $interfaceType $interfaceID $host] != "SUCCESS" } {
      lappend rcode "ERROR: failed EnterConfigIfLevel"
      return [ErrCheck $rcode ResetInterfaceFilter] 
   }
   
   if {[Exec "no filter" "CONFIGIF" $host] != "SUCCESS"} {
      incr errCount
   }
   
   if {[ExitConfigIfLevel $host] != "SUCCESS"} {
      incr errCount
   }

   if {$errCount == 0} {
      set errCode "SUCCESS"
   }

   return $errCode   
}


#############################################################
# SetIfTcpMss: Sets the maximum amount of TCP data in a single IP datagram.
# IN:  interfaceType: interface type in the format known by CES
#                     e.q. fast ethernet interface: FastEthernet
#                          wan interface:           serial
#      interfaceID:   <0-6>/<1-4>  slot number / port number
#      tcpMss:        <536-1460>  Sets the value TCP packets are clamped to.
#      host:          (management IP) / (terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc SetIfTcpMss {interfaceType interfaceID tcpMss host} {
   set err_count [GetGlobalErr]

   if {[EnterConfigIfLevel $interfaceType $interfaceID $host] != "SUCCESS"} {
      return [CheckGlobalErr $err_count]
   }
   
   set cli_prompt "CES\\(config-if\\)\#"

   Exec "tcp-mss $tcpMss" $cli_prompt $host  
   
   SetCliLevel "PRIVILEGE" $host

   return [CheckGlobalErr $err_count]  
}


#############################################################
# SetIfDefaultTcpMss: Resets TCP MSS to defaults.
#
# IN:  interfaceType: interface type in the format known by CES
#                     e.q. fast ethernet interface: FastEthernet
#                          wan interface:           serial
#      interfaceID:   <0-6>/<1-4>  slot number / port number
#      host:          (management IP) / (terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc SetIfDefaultTcpMss {interfaceType interfaceID host} {
   set err_count [GetGlobalErr]

   if {[EnterConfigIfLevel $interfaceType $interfaceID $host] != "SUCCESS"} {
      return [CheckGlobalErr $err_count]
   }
   
   set cli_prompt "CES\\(config-if\\)\#"

   Exec "no tcp-mss" $cli_prompt $host  
   
   SetCliLevel "PRIVILEGE" $host   

   return [CheckGlobalErr $err_count]  
}


#############################################################
# SetIfTcpMssState: Enables/Disables TCP MSS Clamping on the interface.
# IN:  interfaceType: interface type in the format known by CES
#                     e.q. fast ethernet interface: FastEthernet
#                          wan interface:           serial
#      interfaceID:   <0-6>/<1-4>  slot number / port number 
#      state:         <enable/no_enable>
#      host:          (management IP) / (terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc SetIfTcpMssState {interfaceType interfaceID state host} {
   set err_count [GetGlobalErr]

   if {[EnterConfigIfLevel $interfaceType $interfaceID $host] != "SUCCESS"} {
      return [CheckGlobalErr $err_count]
   }
   
   set cli_prompt "CES\\(config-if\\)\#"

   if {$state == "enable"} {
       Exec "tcp-mss enable" $cli_prompt $host 
   } elseif {$state == "no_enable"} {
      Exec "no tcp-mss enable" $cli_prompt $host      
   } else {
      ErrCheck [list "ERROR: bad parameter - state: $state"]
   }
   
   SetCliLevel "PRIVILEGE" $host   

   return [CheckGlobalErr $err_count]
}

#############################################################
# SetEthIfDuplex: Configure duplex setting
#
# IN:  host:        (management IP) / (terminal server Ip:port)
#      interfaceID: <0-6>/<1-4>  slot number / port number 
#      duplexType:  full/half/auto
#
# OUT: SUCCESS/ERROR
#############################################################
proc SetEthIfDuplex {host interfaceID duplexType} {
   set err_count [GetGlobalErr]

   if {[EnterConfigIfLevel "fast" $interfaceID $host] != "SUCCESS"} {
      return [CheckGlobalErr $err_count]
   }
   set cli_prompt "CES\\(config-if\\)\#"

   Exec "duplex $duplexType" $cli_prompt $host 

   SetCliLevel "PRIVILEGE" $host   

   return [CheckGlobalErr $err_count]
}


#############################################################
# SetEthIfSpeed: Configures speed/duplex setting
#
# IN:  host:        (management IP) / (terminal server Ip:port)
#      interfaceID: <0-6>/<1-4>  slot number / port number 
#      speed:       10/100/auto
#
# OUT: SUCCESS/ERROR
#############################################################
proc SetEthIfSpeed {host interfaceID speed} {
   set err_count [GetGlobalErr]

   if {[EnterConfigIfLevel "fast" $interfaceID $host] != "SUCCESS"} {
      return [CheckGlobalErr $err_count]
   }
   set cli_prompt "CES\\(config-if\\)\#"

   Exec "speed $speed" $cli_prompt $host 

   SetCliLevel "PRIVILEGE" $host   

   return [CheckGlobalErr $err_count]
}


#############################################################
# GetIFEthMac: Gets the fast ethernet interface MAC address based on the
#              IP address configured on interface.
#
# IN:  IfIpAddr: fast ethernet interface IP address
#      host:     (management IP) / (terminal server Ip:port)
#
# OUT: ERROR:       if CLI errors
#      mac address: ethernet interface address
#      NONE:        when there is no ethernet interface configured with the given IfIpAddr
#############################################################
proc GetIfEthMac {IfIpAddr host} {
   global cmdOut
   set err_count [GetGlobalErr]

   SetCliLevel "USER" $host 

   Exec "show status statistics interfaces interfaces" "USER" $host

   if {[CheckGlobalErr $err_count] == "ERROR"} {
      return "ERROR"
   }

   set net_if_line 100000

   set count 0

   foreach line [split $cmdOut "\n"] {
      # get the number of the first line from a data block relating to a net interface       
      #puts "*** line = $line"
      if {[regexp {fei[\ \t]+\(unit number [0-9]+, index [0-9]+} $line] == 1} {         
         set net_if_line $count
         set ip_addr "NULL"
         set mac_addr "NULL"
         set all "NULL"
      }

      # inside the data relating to a net interface
      if {$count > $net_if_line} {

         regexp {Internet address:[\ \t]+(([0-9]+\.?)+)} $line all ip_addr         
         regexp {Ethernet address is (([0-9a-zA-Z]+:?)+)} $line all mac_addr                  

         if {$ip_addr == $IfIpAddr && $mac_addr != "" && $mac_addr != "NULL"} {
            return $mac_addr
         }
         
      }
      incr count

   }     

   return "NONE"

}


#############################################################
# GetEthInfo: Gets information relating to ethernet interface.
#
# IN:  if_id:       <0-6>/<1-4>  slot number / port number
#      data_to_get: Ethernet interface parameter.
#                   e.g.: "DHCP-relay"
#                         "Duplex"
#                         "Filter"
#                         "IP Address"
#                         "Mac Pause"
#                         "MTU"
#                         "PPPoE"                         
#                         "Public/Private"
#                         "DHCP Service"
#                         "Status"
#                         "Speed"
#                         "TCP-Maximum Segment Size Clamping:"
#                         "TCP-Maximum Segment Size \\\[bytes\\\]"
#                         ...
#                       
#      host:        (management IP) / (terminal server Ip:port)
#
# OUT: NONE/ERROR/<value of data_to_get>/NO_LAN_IF
#      
#############################################################
proc GetEthInfo {host if_id data_to_get} {

   global cmdOut

   set return_val ""
   
   set err_count [GetGlobalErr]

   SetCliLevel "PRIVILEGE" $host

   Exec "sh interface fast $if_id" "PRIVILEGE" $host
   
   # NO WAN IFLAN Interface 4/1 does not exist
   if {[regexp -nocase {(interface [0-9]+/[0-9]+ does not exist)|(LAN interface [0-9]+/[0-9]+ does not exist)}\
            $cmdOut]  == 1} {
      return "NO_LAN_IF"
   }

   # ret value
   foreach line [split $cmdOut "\n"] {
      if {[regexp -nocase "${data_to_get}\[\ \t\]*:\[\ \t\]*\(\[0-9a-zA-Z.\/\ \-\]+\)" $line all return_val] == 1} {         
         if {$return_val != ""} {
            return $return_val
         }
      }
   }
      
   # check for errors
   if {[CheckGlobalErr $err_count] == "ERROR"} {
      return "ERROR"
   }

   if {$return_val == ""} {
      return "NONE"
   }

}

proc GetIfPacketStats { host IfIpAddr } {
   global cmdOut
   set err_count [GetGlobalErr]

   SetCliLevel "USER" $host 

   Exec "show status statistics interfaces interfaces" "USER" $host

   if {[CheckGlobalErr $err_count] == "ERROR"} {
      return "ERROR"
   }

   set net_if_line 100000

   set count 0

   foreach line [split $cmdOut "\n"] {
      # get the number of the first line from a data block relating to a net interface       
      #puts "*** line = $line"
      if {[regexp {fei[\ \t]+\(unit number [0-9]+, index [0-9]+} $line] == 1} {         
         set net_if_line $count
         set ip_addr "NULL"
         set receive_packets "NULL"
         set sent_packets "NULL"
         set all "NULL"
      }

      # inside the data relating to a net interface
      if {$count > $net_if_line} {

         regexp {Internet address:[\ \t]+(([0-9]+\.?)+)} $line all ip_addr         
         regexp {([0-9]+)[\ \t]+packets received; ([0-9]+)[\ \t]+packets sent} $line all receive_packets sent_packets

         if {$ip_addr == $IfIpAddr && $receive_packets != "" && $receive_packets != "NULL"} {
            return [list $receive_packets $sent_packets]
         }
         
      }
      incr count

   }     

   return "NONE"

}

proc AddIfMultinetIp { host interfaceID ipAddr ipMask } {
   set err_count [GetGlobalErr]
   EnterConfigIfLevel "fastethernet" $interfaceID $host
   Exec "ip address $ipAddr $ipMask secondary" "CONFIGIF" $host
   SetCliLevel "CONFIG" $host
   return [CheckGlobalErr $err_count]
}

proc DelIfMultinetIp { host interfaceID ipAddr ipMask } {
   set err_count [GetGlobalErr]
   EnterConfigIfLevel "fastethernet" $interfaceID $host
   Exec "no ip address $ipAddr $ipMask secondary" "CONFIGIF" $host
   SetCliLevel "CONFIG" $host
   return [CheckGlobalErr $err_count]
}


#######################
# INTERFACE PPPOE 
#######################

###############################################
# SetIfPppoeAdminState: enable or disable pppoe interface
#                       admin state.
#
# IN:  adminState: enable/disable
#      ifId:       <0-6>/<1-4>  slot number / port number
#      host:       managemente IP/terminal server Ip:port
#
#
# OUT: SUCCESS/ERROR
###############################################
proc SetIfPppoeAdminState {host ifId adminState} {

   set rcode ""
   
   EnterConfigIfLevel "fast" $ifId $host
   
   if {[regexp -nocase "en" $adminState] == 1} {
      Exec "pppoe admin-state enable" "CONFIGIF" $host
   } elseif {[regexp -nocase "dis" $adminState] == 1} {
      Exec "no pppoe admin-state enable" "CONFIGIF" $host
   } else {
      lappend rcode "ERR: unknown parameter"
   }
   
   Exec "exit" "CONFIG" $host
   return [ErrCheck $rcode SetIfPppoeAdminState]
}

################################################
# EnableIfPppoe: enable interface PPPoE
#
################################################
proc EnableIfPppoe { ifId host } {
   
   EnterConfigIfLevel "fast" $ifId $host

   Exec "pppoe enable" "CONFIGIF" $host
}

################################################
# DisableIfPppoe: disable interface PPPoE
#
################################################
proc DisableIfPppoe { ifId host } {
   
   EnterConfigIfLevel "fast" $ifId $host

   Exec "no pppoe enable" "CONFIGIF" $host
}

#################################################
# SetIfPppoeAuth: set or unset pppoe authentication
#
# IN:  authType: pap/no pap, chap/no chap
#      host:     management IP/terminal server Ip:port
#
# OUT: SUCCESS/ERROR
#################################################
proc SetIfPppoeAuth { ifId authType host } {
   
   EnterConfigIfLevel "fast" $ifId $host

   if {[regexp {no [a-zA-A]+} $authType all auth] == 1} {
      Exec "no pppoe ppp authentication $auth" "CONFIGIF" $host
   } else {
      Exec "pppoe ppp authentication $authType" "CONFIGIF" $host
   }
}

#####################################################
# 
#
# 
#####################################################
proc ConfigIfPppoeUserIdentif { ifId user passwd host } {
   
   EnterConfigIfLevel "fast" $ifId $host

   Exec "pppoe ppp username $user password $passwd" "CONFIGIF" $host
}

proc {SetIfPppoeLocalIp} { ifId ip host } {
   
   EnterConfigIfLevel "fast" $ifId $host

   Exec "pppoe ip local $ip" "CONFIGIF" $host
}

proc {DelIfPppoeLocalIp} { ifId host } {
   
   EnterConfigIfLevel "fast" $ifId $host

   Exec "no pppoe ip local" "CONFIGIF" $host
}

proc {SetIfPppoeServiceName} { ifId service_name host } {
   
   EnterConfigIfLevel "fast" $ifId $host

   Exec "pppoe service-name $service_name" "CONFIGIF" $host
}


proc EnableIfPppoeOnDemand { ifId host } {
   
   EnterConfigIfLevel "fast" $ifId $host

   Exec "pppoe on-demand enable" "CONFIGIF" $host
}


proc DisableIfPppoeOnDemand { ifId host } {
   
   EnterConfigIfLevel "fast" $ifId $host

   Exec "no pppoe on-demand enable" "CONFIGIF" $host
}


proc SetPppoeIdleTimeOut { ifId time  host } {

   EnterConfigIfLevel "fast" $ifId $host

   Exec "pppoe idle-timeout $time" "CONFIGIF" $host
}

proc SetPppoeLcpEchoInterval { ifId time host } {

   EnterConfigIfLevel "fast" $ifId $host

   Exec "pppoe ppp lcp echo-interval $time" "CONFIGIF" $host
}

proc SetPppoeLcpEchoFaultThreshold { ifId time host } {

   EnterConfigIfLevel "fast" $ifId $host

   Exec "pppoe ppp lcp echo-fault-threshold $time" "CONFIGIF" $host
}

proc  SetPppoeCost {ifId cost host} {

   EnterConfigIfLevel "fast" $ifId $host

   Exec "pppoe cost $cost" "CONFIGIF" $host
}


# global pppoe procs
proc ShowIfPppoe { ifId host } {

   SetCliLevel "PRIVILEGE" $host
   
   Exec "show interface fast $ifId pppoe" "PRIVILEGE" $host
   
}


########################################################
# ConfigIfPppoe: 
#
########################################################
proc ConfigIfPppoe { ifId authType user passwd localIp host } {
   
   EnterConfigIfLevel "fast" $ifId $host

   Exec "pppoe enable" "CONFIGIF" $host
   Exec "pppoe ppp authentication $authType" "CONFIGIF" $host
   Exec "pppoe ppp username $user password $passwd" "CONFIGIF" $host


   if {$localIp != ""} {
   Exec "pppoe ip local $localIp" "CONFIGIF" $host
   }
   Exec "pppoe ppp ip default-route enabled" "CONFIGIF" $host
   Exec "pppoe admin-state enable" "CONFIGIF" $host

   SetCliLevel "CONFIG" $host

}

##################################################
# CleanIfPppoe:
#
##################################################
proc CleanIfPppoe { ifId host } {

   EnterConfigIfLevel "fast" $ifId $host

   Exec "no pppoe admin-state enable" "CONFIGIF" $host
#   Exec "no pppoe ppp authentication $authType" "CONFIGIF" $host
#   Exec "no pppoe ip local" "CONFIGIF" $host
   Exec "no pppoe enable" "CONFIGIF" $host

   SetCliLevel "CONFIG" $host
}


#############################################################
# GetPPPoEInfo: Gets information relating to PPPoE interface.
#
# IN:  if_id:       <0-6>/<1-4>  slot number / port number
#      data_to_get: PPPoE interface parameter.
#                   e.g.: "PPPoE"
#                         "Administrative state"
#                         "Cost"
#                         "Idle Time-out"
#                         "Local IP Address"
#                         "On-demand"
#                         "Use Default Route"
#                         "Authentication"                         
#                         "VJ Connect ID Compression Negotiation"
#                         "VJ Max Slots"
#                         "VJ Negotiation"
#                         "Echo Fault Threshold"
#                         "Echo Interval"
#                         "Protocol Field Compression"
#                         "User Name"
#                         "Service Name"
#                       
#      host:        (management IP) / (terminal server Ip:port)
#
# OUT: NONE/ERROR/<value of data_to_get>/NO_LAN_IF
#      
#############################################################
proc GetPPPoEInfo {host if_id data_to_get} {

   global cmdOut

   set return_val ""
   
   set err_count [GetGlobalErr]

   SetCliLevel "PRIVILEGE" $host

   Exec "sh interface fast $if_id pppoe" "PRIVILEGE" $host
   
   # NO WAN IFLAN Interface 4/1 does not exist
   if {[regexp -nocase {(interface [0-9]+/[0-9]+ does not exist)|(LAN interface [0-9]+/[0-9]+ does not exist)}\
            $cmdOut]  == 1} {
      return "NO_LAN_IF"
   }

   # ret value
   foreach line [split $cmdOut "\n"] {
      if {[regexp -nocase "${data_to_get}\[\ \t\]*:\[\ \t\]*\(\[0-9a-zA-Z._\/\ \-\]+\)" $line all return_val] == 1} {         
         if {$return_val != ""} {
            return $return_val
         }
      }
   }
      
   # check for errors
   if {[CheckGlobalErr $err_count] == "ERROR"} {
      return "ERROR"
   }

   if {$return_val == ""} {
      return "NONE"
   }

}



#############
# wan interface ppp/frame-relay
#############

############################################
# SetWanEncapsulation: configures wan interface encapsulation type
# 
# IN:  if_id: <0-6>/<1-4>  slot number / port number
#      state: <enable/disable>
#      host:  (management IP) / (terminal server Ip:port)
# 
# OUT: SUCCESS/ERROR
#
############################################
proc SetWanState { host if_id state } {

   global cmdOut
   set err_count [GetGlobalErr]
   
   SetCliLevel "CONFIG" $host
   switch $state {
      "enable" {
         Exec "interface serial $if_id enable" "CONFIG" $host
      }
      "disable" {
         Exec "no interface serial $if_id enable" "CONFIG" $host
      }
      default {
         return [ErrCheck "ERROR: Invalid state" SetWanState]
      }
   }
   
   SetCliLevel "PRIVILEGE" $host
   
   return [CheckGlobalErr $err_count]
}

############################################
# SetWanEncapsulation: configures wan interface encapsulation type
# 
# IN:  if_id:    <0-6>/<1-4>  slot number / port number
#      enc_type: <ppp/frame-relay>
#      host:     (management IP) / (terminal server Ip:port)
# 
# OUT: SUCCESS/ERROR
#
############################################
proc SetWanEncapsulation {if_id enc_type host} {
   
   global cmdOut
   set err_count [GetGlobalErr]

   EnterConfigIfLevel "serial" $if_id $host
   Exec "encapsulation $enc_type" "CONFIGIF" $host
   if {[regexp {reboot} $cmdOut] == 1} {      
      Reload $host; #reboot the system in order to activate the new encapsulation type
      
   }   
   return [CheckGlobalErr $err_count]

}


#############################################################
# GetWanInfo: Gets information relating to WAN interface.
#
# IN:  if_id:       <0-6>/<1-4>  slot number / port number
#      data_to_get: Wan interface parameter.
#                   e.g.: "State"
#                         "Circuit ID"
#                         "Description"
#                         "Filter"
#                         "Protocol Encapsulation"
#                         "Public/Private"
#                         "MTU"
#                         "TCP-Maximum Segment Size \\\[bytes\\\]"
#                         ...
#                       
#      host:        (management IP) / (terminal server Ip:port)
#
# OUT: NONE/ERROR/<value of data_to_get>/NO_WAN_IF
#      
#############################################################
proc GetWanInfo {host if_id data_to_get} {

   global cmdOut

   set return_val ""
   
   set err_count [GetGlobalErr]

   SetCliLevel "PRIVILEGE" $host

   Exec "sh interface serial $if_id" "PRIVILEGE" $host
   
   # NO WAN IF
   if {[regexp {(interface [0-9]+/[0-9]+ does not exist)|(interface [0-9]+/[0-9]+ is not a serial interface)}\
            $cmdOut]  == 1} {
      return "NO_WAN_IF"
   }

   # ret value
   foreach line [split $cmdOut "\n"] {
      if {[regexp -nocase "${data_to_get}:\[\ \t\]\(\[0-9a-zA-Z\/\ \-\]+\)" $line all return_val] == 1} {         
         if {$return_val != ""} {
            return $return_val
         }
      }
   }
      
   # check for errors
   if {[CheckGlobalErr $err_count] == "ERROR"} {
      return "ERROR"
   }

   if {$return_val == ""} {
      return "NONE"
   }

}



#############
# ppp
#############
proc SetPppAuthentication {ifId authType host} {
   set rcode ""

   EnterConfigIfLevel "serial" $ifId $host
   if {[Exec "ppp authentication $authType" "CONFIGIF" $host] != "SUCCESS"} {
      lappend rcode "ERROR: Failed to enable PPP Authentication $authType"
   }
   return [ErrCheck $rcode SetPppAuthentication]
}

proc SetPppIpLocal {ifId ip mask host} {
   set rcode ""

   EnterConfigIfLevel "serial" $ifId $host
   if {[Exec "ppp ip local $ip $mask" "CONFIGIF" $host] != "SUCCESS"} {
      lappend rcode "ERROR: Failed to configure the PPP local IP address"
   }
   return [ErrCheck $rcode SetPppIpLocal]
}

proc SetPppUsername {ifId username host} {
   set rcode ""

   EnterConfigIfLevel "serial" $ifId $host
   if {[Exec "ppp username $username" "CONFIGIF" $host] != "SUCCESS"} {
      lappend rcode "ERROR: Failed to set PPP username"
   }
   return [ErrCheck $rcode SetPppUsername]
}

proc SetPppPassword {ifId password host} {
   set rcode ""

   EnterConfigIfLevel "serial" $ifId $host
   if {[Exec "ppp password $password" "CONFIGIF" $host] != "SUCCESS"} {
      lappend rcode "ERROR: Failed to set PPP password"
   }
   return [ErrCheck $rcode SetPppPassword]
}

###############
# ip variable can be an IP address or "negotiated" string
proc SetPppIpRemote {ifId ip host} {
   set rcode ""

   EnterConfigIfLevel "serial" $ifId $host
   if {[Exec "ppp ip remote $ip " "CONFIGIF" $host] != "SUCCESS"} {
      lappend rcode "ERROR: Failed to configure the PPP remote IP address"
   }
   return [ErrCheck $rcode SetPppIpRemote]
}


##########################################################
# ConfigIpOverPPPLink: set up an IP over PPP link
#
# IN:  if_id:      <0-6>/<1-4>  slot number / port number 
#      auth_type:  <pap, chap>  ppp authentication
#      user:       user
#      pass:       password
#      local_ip:   local ip
#      mask:       local net mask
#      remote_ip:  remote ip/negotiated
#      host:       management IP/terminal server Ip:port
#      
# OUT: SUCCESS or ERROR
#
##########################################################
proc ConfigIpOverPPPLink {if_id auth_type user pass local_ip mask remote_ip host} {

   set err_count [GetGlobalErr]

   SetWanEncapsulation $if_id "ppp" $host

   EnterConfigIfLevel "serial" $if_id $host

   Exec "ppp authentication $auth_type" "CONFIGIF" $host
   Exec "ppp username $user" "CONFIGIF" $host
   Exec "ppp password $pass" "CONFIGIF" $host
   Exec "ppp ip local $local_ip $mask" "CONFIGIF" $host   
   Exec "ppp ip remote $remote_ip " "CONFIGIF" $host

   ExitConfigIfLevel $host

   return [CheckGlobalErr $err_count]

}



#############
# frame-relay
#############

###############################################
# EnterFrameRelaySubIfLevel: enters to frame relay subinterface menu.
#                            Encapsulation type must be set to "frame-relay"
#                            for the wan interface, in order to be able to
#                            enter to the subinterface menu.
#
# IN:  if_id:     <0-6>/<1-4>  slot number / port number
#      sub_if_id: <1-10>  Number of the sub-interface (virtual circuit)
#      host:      (management IP) / (terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#
###############################################
proc EnterFrameRelaySubIfLevel {if_id sub_if_id host} {

   set err_count [GetGlobalErr]
   global cmdOut
   
   EnterConfigIfLevel "serial" $if_id $host
   Exec "frame-relay subinterface $sub_if_id" "CES\\(config-subif\\)\#" $host

   return [CheckGlobalErr $err_count]

}

###############################################
# DelFrameRelaySubIf: deletes a frame-relay subinterface.
#                     Encapsulation type must be set to "frame-relay"
#                     for the wan interface, in order to be able to
#                     enter to the subinterface menu.
#
# IN:  if_id:     <0-6>/<1-4>  slot number / port number
#      sub_if_id: <1-10> or <1-255> (depends on sw version)  Number of the sub-interface (virtual circuit)
#      host:      (management IP) / (terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#
###############################################
proc DelFrameRelaySubIf { if_id sub_if_id host } {
   set err_count [GetGlobalErr]
   global cmdOut
   
   EnterConfigIfLevel "serial" $if_id $host
   Exec "no frame-relay subinterface $sub_if_id" "CONFIGIF" $host
   SetCliLevel "PRIVILEGE" $host

   return [CheckGlobalErr $err_count]

}
##########################################################
# ConfigIpOverFRLink: set up an IP over frame relay link
#
# IN:  if_id:     <0-6>/<1-4>  slot number / port number 
#      sub_if_id: <1-10>  Number of the sub-interface (virtual circuit) 
#      local_ip:  local IP address
#      mask:      net mask     
#      remote_ip: remote IP address
#      dlci:      virtual circuit Data Link Connection Identifier
#      conn_type: Frame Relay connection type
#      lmi_type:  LMI type (switch type)
#      host:      (management IP) / (terminal server Ip:port)
#      
# OUT: SUCCESS or ERROR
#
##########################################################
proc ConfigIpOverFRLink {if_id sub_if_id local_ip mask remote_ip dlci conn_type lmi_type host} {

   set err_count [GetGlobalErr]

   SetWanEncapsulation $if_id "frame-relay" $host

   EnterFrameRelaySubIfLevel $if_id $sub_if_id $host
   Exec "ip local $local_ip $mask" "CES\\(config-subif\\)\#" $host
   Exec "ip remote $remote_ip" "CES\\(config-subif\\)\#" $host
   Exec "dlci $dlci" "CES\\(config-subif\\)\#" $host
   Exec "exit" "CONFIGIF" $host
# Modified by Asterix
   Exec "frame-relay connection-type $conn_type" "*?CES\\(config-if\\)\#" $host
   Exec "frame-relay lmi-type $lmi_type" "*?CES\\(config-if\\)\#" $host
# Exec "frame-relay connection-type $conn_type" "CONFIGIF" $host 0 120
# Exec "frame-relay lmi-type $lmi_type" "CONFIGIF" $host

   SetCliLevel "CONFIG" $host

   return [CheckGlobalErr $err_count]

}

##########################################################
# SetLineFormat: set up the line format (T1/E1 framed/unframed)
#
# IN:  host:      (management IP) / (terminal server Ip:port)
#      if_id:     <0-6>/<1-4>  slot number / port number
#      line_type: <t1/e1>
#      framing:   <sf/esf> for T1 or <crc4/no-crc4/e1-uf> for E1
# 
# OUT: SUCCESS or ERROR
#
##########################################################
proc SetLineFormat { host if_id line_type {framing ""} } {
   
   set err_count [GetGlobalErr]
   
   SetCliLevel "CONFIG" $host
   Exec "controller $line_type $if_id" "CES\\(config-controller\\)\#" $host
   if { $framing != "" } {
      Exec "framing $framing" "CES\\(config-controller\\)\#" $host
   }
   SetCliLevel "PRIVILEGE" $host

   return [CheckGlobalErr $err_count]
   
}

##########################################################
# SetClockSource: set the clock source (loop/internal)
#
# IN:  host:      (management IP) / (terminal server Ip:port)
#      if_id:     <0-6>/<1-4>  slot number / port number
#      line_type: <t1/e1>
#      mode:      <loop/internal>
# 
# OUT: SUCCESS or ERROR
#
##########################################################
proc SetClockSource { host if_id line_type mode } {
   
   set err_count [GetGlobalErr]
   
   SetCliLevel "CONFIG" $host
   Exec "controller $line_type $if_id" "CES\\(config-controller\\)\#" $host
   Exec "clock source $mode" "CES\\(config-controller\\)\#" $host
   SetCliLevel "PRIVILEGE" $host

   return [CheckGlobalErr $err_count]
   

}

##########################################################
# SetHdlcPolarity: set the HDLC polarity for frame-relay interface
#
# IN:  host:     (management IP) / (terminal server Ip:port)
#      if_id:    <0-6>/<1-4>  slot number / port number
#      polarity: <normal/invert>
# 
# OUT: SUCCESS or ERROR
#
##########################################################
proc SetHdlcPolarity { host if_id polarity } {
   
   set err_count [GetGlobalErr]
   
   EnterConfigIfLevel "serial" $if_id $host
   switch $polarity {
      "normal" {
         Exec "no invert data" "CONFIGIF" $host
      }
      "invert" {
         Exec "invert data" "CONFIGIF" $host
      }
      default {
         return [ErrCheck "ERROR: Invalid state" SetHdlcPolarity]
      }
   }
   SetCliLevel "PRIVILEGE" $host

   return [CheckGlobalErr $err_count]
   
}

######
# rip
######

proc EnableIfRip {interfaceID host} {
   EnterConfigIfLevel "fastethernet" $interfaceID $host
   Exec "ip rip" "CONFIGIF" $host
   SetCliLevel "CONFIG" $host
}


proc DisableIfRip {interfaceID host} {
   EnterConfigIfLevel "fastethernet" $interfaceID $host
   Exec "no ip rip" "CONFIGIF" $host
   SetCliLevel "CONFIG" $host
}

proc IfRipSendVersionNone {interfaceID host} {
   EnterConfigIfLevel "fastethernet" $interfaceID $host
   Exec "ip rip send version none" "CONFIGIF" $host
   SetCliLevel "CONFIG" $host
}

proc EnableIfRipExportOspf {host interfaceID {metricNo 1}} {

   global cmdOut

   set err_count [GetGlobalErr]

   EnterConfigIfLevel "fastethernet" $interfaceID $host

   Exec "ip rip export-ospf-metric $metricNo" "CONFIGIF" $host

   if { [regexp -nocase {RIP is not configured on this interface} $cmdOut msg] == 1 } {
      set rcode "ERROR: CES $host - interface $interfaceID: redistribute OSPF can't be set:\n----\n$msg\n----"
      ErrCheck $rcode "EnableIfRipExportOspf"
   }

   SetCliLevel "CONFIG" $host

   return [CheckGlobalErr $err_count]
}


proc DisableIfRipExportOspf {host interfaceID} {
   global cmdOut

   set cmdOut ""
   set rcode ""
   EnterConfigIfLevel "fastethernet" $interfaceID $host
   if {[Exec "no ip rip export-ospf-metric" "CONFIGIF" $host] != "SUCCESS" } {
      return "ERROR"
   } elseif { [regexp -nocase {RIP is not configured on this interface} $cmdOut msg] == 1 } {
      lappend rcode "ERROR: CES $host - interface $interfaceID: redistribute OSPF can't be unset:\n----\n$msg\n----"
   }
   SetCliLevel "CONFIG" $host
   return [ErrCheck $rcode "DisableIfRipExportOspf"]
}

##########################################################
# EnableIfRipExportBoStaticRoutes: enables export of Static BO routes over OSPF for a certain interface at a specific cost
#
# IN:  host:          (management IP) / (terminal server Ip:port)
#      interfaceType: interface type in the format known by CES
#                     e.q. fast ethernet interface: FastEthernet
#                          wan interface:           serial
#      interfaceID:   <0-6>/<1-4>  slot number / port number
#      cost:          cost of the exported static route <1-15>
#      
# OUT: SUCCESS or ERROR
#
##########################################################
proc EnableIfRipExportBoStaticRoutes { host interfaceType interfaceID cost } {
   set err_count [GetGlobalErr]
   EnterConfigIfLevel $interfaceType $interfaceID $host
   Exec "ip rip export-bo-static-metric $cost" "CONFIGIF" $host
   SetCliLevel "CONFIG" $host
   return [CheckGlobalErr $err_count]
}



##########################################################
# DisableIfRipExportBoStaticRoutes: disables export of Static BO routes over OSPF for a certain interface
#
# IN:  host:          (management IP) / (terminal server Ip:port)
#      interfaceType: interface type in the format known by CES
#                     e.q. fast ethernet interface: FastEthernet
#                          wan interface:           serial
#      interfaceID:   <0-6>/<1-4>  slot number / port number
#      
# OUT: SUCCESS or ERROR
#
##########################################################
proc DisableIfRipExportBoStaticRoutes { host interfaceType interfaceID } {
   set err_count [GetGlobalErr]
   EnterConfigIfLevel $interfaceType $interfaceID $host
   Exec "no ip rip export-bo-static-metric" "CONFIGIF" $host
   SetCliLevel "CONFIG" $host
   return [CheckGlobalErr $err_count]  
}



######
# ospf
######

proc EnableIfOspf {interfaceID host} {
   EnterConfigIfLevel "fastethernet" $interfaceID $host
   Exec "ip ospf" "CONFIGIF" $host
   SetCliLevel "CONFIG" $host
}


proc DisableIfOspf {interfaceID host} {
   EnterConfigIfLevel "fastethernet" $interfaceID $host
   Exec "no ip ospf" "CONFIGIF" $host
   SetCliLevel "CONFIG" $host
}




######
# vrrp
######

##########################################################
# EnableIfVrrp: Enables interface VRRP
#
# IN:  host:          (management IP) / (terminal server Ip:port)
#      interfaceType: interface type in the format known by CES
#                     e.q. fast ethernet interface: FastEthernet
#                          wan interface:           serial
#      interfaceID:   <0-6>/<1-4>  slot number / port number
#      
# OUT: SUCCESS or ERROR
##########################################################
proc EnableIfVrrp { host interfaceType interfaceID } {
   set err_count [GetGlobalErr]
   EnterConfigIfLevel "fastethernet" $interfaceID $host
   Exec "ip vrrp" "CONFIGIF" $host
   SetCliLevel "CONFIG" $host
   return [CheckGlobalErr $err_count]
}

##########################################################
# DisableIfVrrp: Disables interface VRRP
#
# IN:  host:          (management IP) / (terminal server Ip:port)
#      interfaceType: interface type in the format known by CES
#                     e.q. fast ethernet interface: FastEthernet
#                          wan interface:           serial
#      interfaceID:   <0-6>/<1-4>  slot number / port number
#      
# OUT: SUCCESS or ERROR
##########################################################
proc DisableIfVrrp { host interfaceType interfaceID } {
   set err_count [GetGlobalErr]
   EnterConfigIfLevel "fastethernet" $interfaceID $host
   Exec "no ip vrrp" "CONFIGIF" $host
   SetCliLevel "CONFIG" $host
   return [CheckGlobalErr $err_count]
}

##########################################################
# SetMasterIfVrrp: Set interface Master VRRP
#
# IN:  host:          (management IP) / (terminal server Ip:port)
#      interfaceType: interface type in the format known by CES
#                     e.q. fast ethernet interface: FastEthernet
#                          wan interface:           serial
#      interfaceID:   <0-6>/<1-4>  slot number / port number
#      
# OUT: SUCCESS or ERROR
##########################################################
proc SetMasterIfVrrp { host interfaceType interfaceID } {
   set err_count [GetGlobalErr]
   EnterConfigIfLevel "fastethernet" $interfaceID $host
   Exec "ip vrrp master" "CONFIGIF" $host
   SetCliLevel "CONFIG" $host
   return [CheckGlobalErr $err_count]
}

##########################################################
# SetBackupIfVrrp: Set interface backup VRRP
#
# IN:  host:          (management IP) / (terminal server Ip:port)
#      interfaceType: interface type in the format known by CES
#                     e.q. fast ethernet interface: FastEthernet
#                          wan interface:           serial
#      interfaceID:   <0-6>/<1-4>  slot number / port number
#      
# OUT: SUCCESS or ERROR
##########################################################
proc SetBackupIfVrrp { host interfaceType interfaceID vrrpIP {priority notSet}} {
    set err_count [GetGlobalErr]
    EnterConfigIfLevel "fastethernet" $interfaceID $host

    if {$priority != "notSet"} {
        Exec "ip vrrp backup $vrrpIP priority $priority" "CONFIGIF" $host
    } else {
        Exec "ip vrrp backup $vrrpIP" "CONFIGIF" $host
    }

    SetCliLevel "CONFIG" $host
    return [CheckGlobalErr $err_count]
}

##########################################################
# AddInterfaceGroup:  Creates an interface group
#
# IN:  host:          (management IP) / (terminal server Ip:port)
#      ifGroupName:     name of the interface group 
# OUT: SUCCESS or ERROR
##########################################################
proc AddInterfaceGroup {host ifGroupName} {
    set err_count [GetGlobalErr]

    SetCliLevel "CONFIG" $host
    Exec "interface group $ifGroupName" "CONFIG"  $host

    return [CheckGlobalErr $err_count]
}

##########################################################
# DelInterfaceGroup: Delete an interface group
#
# IN:  host:          (management IP) / (terminal server Ip:port)
#      ifGroupName:     name of the interface group 
# OUT: SUCCESS or ERROR
##########################################################
proc DelInterfaceGroup {host ifGroupName} {
    set err_count [GetGlobalErr]

    SetCliLevel "CONFIG" $host
    Exec "no interface group $ifGroupName" "CONFIG"  $host

    return [CheckGlobalErr $err_count]

}

##########################################################
# AddIPInterfaceGroup: Adds an IP Address in an interface group
#
# IN:  host:          (management IP) / (terminal server Ip:port)
#      ifGroupName:     name of the interface group 
#      ip:            IP Address
#
# OUT: SUCCESS or ERROR
##########################################################
proc AddIPInterfaceGroup {host ifGroupName ip} {
    set err_count [GetGlobalErr]

    SetCliLevel "CONFIG" $host
    Exec "interface group $ifGroupName ip $ip" "CONFIG"  $host

    return [CheckGlobalErr $err_count]
}

##########################################################
# DelIPInterfaceGroup: Deletes an IP Address in an interface group
#
# IN:  host:          (management IP) / (terminal server Ip:port)
#      ifGroupName:     name of the interface group 
#      ip:            IP Address
#
# OUT: SUCCESS or ERROR
##########################################################
proc DelIPInterfaceGroup {host ifGroupName ip} {
    set err_count [GetGlobalErr]

    SetCliLevel "CONFIG" $host
    Exec "no interface group $ifGroupName ip $ip" "CONFIG"  $host

    return [CheckGlobalErr $err_count]
}

##########################################################
# EnableInterfaceGroup: Enables an interface group
#
# IN:  host:          (management IP) / (terminal server Ip:port)
#      ifGroupName:     name of the interface group 
# OUT: SUCCESS or ERROR
##########################################################
proc EnableInterfaceGroup {host ifGroupName} {
    set err_count [GetGlobalErr]

    SetCliLevel "CONFIG" $host
    Exec "interface group $ifGroupName enabled" "CONFIG"  $host

    return [CheckGlobalErr $err_count]
}

##########################################################
# DisableInterfaceGroup: Desables an interface group
#
# IN:  host:          (management IP) / (terminal server Ip:port)
#      ifGroupName:     name of the interface group 
# OUT: SUCCESS or ERROR
##########################################################
proc DisableInterfaceGroup {host ifGroupName} {
    set err_count [GetGlobalErr]

    SetCliLevel "CONFIG" $host
    Exec "interface group $ifGroupName disabled" "CONFIG"  $host

    return [CheckGlobalErr $err_count]
}
