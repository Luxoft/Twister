############################################################
# Library procedures for IP settings - CLI:  CES(config)#ip ...
#
# ServiceDhcp {host status}
# InterfaceServiceDhcp {host ifType ifID status}
# IpAddressPoolType {host type}
# IpAddressPoolTypev8 {host type} 
# GetDhcpStatus {host lease_type}
# ShowDhcpServer {host parameter {subnet no_subnet} {dhcpHost no_host}}
#
# ###############
# # ip local pool
# ############### 
# 
# IpLocalPoolAdd {host name ipaddrL ipaddrH {mask "NO"}}
# IpLocalPoolAddv8 {host name ipaddrL ipaddrH {mask "NO"}}
# IpLocalPoolDel {host name}
# IpLocalPoolDelv8 {host name}
# IpLocalPoolEdit {host name ipaddrL ipaddrH {mask "NO"}}
# IpLocalPoolDefault {host ipaddrL ipaddrH {mask "NO"}}
# IpLocalPoolDefaultv8 {host ipaddrL ipaddrH {mask "NO"}}
# IpLocalPoolUnavailable {host action}
# IpLocalPoolUnavailablev8 {host action}
# IpLocalPoolBlackout { host value }
# IpLocalPoolBlackoutv8 { host value }
#
# IpDhcpProxyServerAddrRelease { host state }
# IpDhcpProxyServerAddrReleasev8 { host state }
# IpDhcpProxyServer { host value {address ""} }
# IpDhcpProxyServerv8 { host value {address ""} }
# IpDhcpProxyServerCacheSize { host value }
# IpDhcpProxyServerCacheSizev8 { host value }
# IpDhcpProxyServerBlackoutInterval { host value }
# IpDhcpProxyServerBlackoutIntervalv8 { host value }
# EnterDhcpServerConfig { host }
# ConfigDhcpLease { host type value }
# DisableDhcpLease { host type }
# EnterDhcpServerPoolConfig { host network mask }
# DhcpServerPoolIncludedAddr { host network mask lowest highest }
# DhcpServerPoolExcludedAddr { host network mask lowest {highest ""}}
# DhcpServerPoolName { host network mask name }
# DisableDhcpServerPool { host network mask }
# DeleteDhcpServerPool {host network}
#
# ConfigDhcpPoolOption {host network mask option value}
# EnterDhcpServerPoolHostConfig {host network hostname}
# DeleteDhcpServerPoolHost {host network hostname}
# DhcpServerPoolHostConfig {host network hostname param_list}
#
# SetDhcpRelayState {host state}
# ConfigDhcpRelayIf {host interfaceIP {state ""}}
# DelDhcpRelayIf {host interfaceIP}
# ConfigDhcpRelayHelper {host interfaceIP server_no serverIP}
#
# DeleteArpCache {host}
#############################################################


#############################################################
# ServiceDhcp: Enable/Disable dhcp service.
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      status:  enable/disable/restart
#
# OUT: SUCCESS/ERROR
#############################################################
proc ServiceDhcp {host status}  {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host

   if {[regexp -nocase "^ena" $status] == 1} {
      Exec "service dhcp enable" "CONFIG" $host
   } elseif {[regexp -nocase "^dis" $status] == 1} {
      Exec "no service dhcp enable" "CONFIG" $host
   } elseif {[regexp -nocase "restart" $status] == 1} {
      Exec  "service dhcp restart" "CONFIG" $host
   } else {
      return [ErrCheck "{ERROR: bad parameter: status = $status}" ServiceDhcp]
   }

   return [CheckGlobalErr $err_count]
}

#############################################################
# InterfaceServiceDhcp: Enable/Disable dhcp service at an interface
#               
# IN:  host:          (management IP)/(terminal server Ip:port)
#      ifType: interface type in the format known by CES
#                     e.q. fast ethernet interface: FastEthernet
#      ifID:   <0-6>/<1-4>  slot number / port number
#      status       <enable/disable>
#
# OUT: SUCCESS/ERROR
#############################################################
proc InterfaceServiceDhcp {host ifType ifID status} {
   set err_count [GetGlobalErr]

   EnterConfigIfLevel $ifType $ifID $host
   
   if {[regexp -nocase "^ena" $status] == 1} {
      Exec "service dhcp enable" "CONFIGIF" $host
   } elseif {[regexp -nocase "^dis" $status] == 1} {
      Exec "no service dhcp enable" "CONFIGIF" $host
   } else {
      return [ErrCheck "{ERROR: bad parameter: status = $status}" InterfaceServiceDhcp]
   }

   SetCliLevel "CONFIG" $host
  
   return [CheckGlobalErr $err_count]
}

#############################################################
#IpAddressPoolType: Enables an address pooling mechanism (internal
#               address pool or external DHCP server)
# IN:  host:    (management IP)/(terminal server Ip:port)
#      type:    local/dhcp
#
# OUT: SUCCESS/ERROR
#############################################################
proc IpAddressPoolType {host type} {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   
   if {$type == "local"} {
      Exec "ip address-pool local" "CONFIG" $host
   } elseif {$type == "dhcp"} {
      Exec "ip address-pool dhcp" "CONFIG" $host
   } else {
      return [ErrCheck "{ERROR: bad parameter: type = $type}" IpAddressPoolType]
   }

   SetCliLevel "PRIVILEGE" $host
   
   return [CheckGlobalErr $err_count]
}

#############################################################
#IpAddressPoolTypeV8: Enables an address pooling mechanism (internal
#               address pool or external DHCP server)
# IN:  host:    (management IP)/(terminal server Ip:port)
#      type:    local/dhcp
#
# OUT: SUCCESS/ERROR
#############################################################
proc IpAddressPoolTypeV8 {host type} {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   
   EnterGrConnectivity $host "/Base"
   
   if {$type == "local"} {
      Exec "ip address-src address-pool" "CES\\(config-group/con\\)\#" $host
   } elseif {$type == "dhcp"} {
      Exec "ip address-src external-dhcp" "CES\\(config-group/con\\)\#" $host
   } else {
      return [ErrCheck "{ERROR: bad parameter: type = $type}" IpAddressPoolTypeV8]
   }

   SetCliLevel "PRIVILEGE" $host
   
   return [CheckGlobalErr $err_count]
}

#############################################################
#  GetDhcpStatus: Gets DHCP status statistics
#
# IN:  host:       (management IP) / (terminal server Ip:port)
#      lease_type: available/in-use/abandoned/reserved
#
# OUT: ERROR:      if CLI errors or lease_type is wrong
#      VALUE:      the value for appropriate lease_type 
#      NONE:       if there is no value for lease_type
#############################################################
proc GetDhcpStatus {host lease_type} {
   global cmdOut
   set err_count [GetGlobalErr]

   if {$lease_type != "available" && $lease_type != "in-use" && $lease_type != "abandoned" && $lease_type != "reserved"} {
      return [ErrCheck "{ERROR: bad parameter: lease type = $lease_type; \nit must be available/in-use/abandoned/reserved}" GetDhcpStatus]
   }

   SetCliLevel "PRIVILEGE" $host
   Exec "terminal paging off" "PRIVILEGE" $host

   Exec "show status statistics network dhcp-stats" "PRIVILEGE" $host 0 360

   if {[CheckGlobalErr $err_count] == "ERROR"} {
      return "ERROR"
   }

   foreach line [split $cmdOut "\n\r"] {
#puts "\nline = $line\n"
      if {[regexp {Lease Totals: ([0-9]+) available, ([0-9]+) in-use, ([0-9]+) abandoned, ([0-9]+) reserved} \
               $line all available in-use abandoned reserved] == 1} {
         
         return [set [set lease_type]]
      }
   }
   return "NONE"
}




#############################################################
# ShowDhcpServer: Gets DHCP server config
#
# IN:  host:       (management IP) / (terminal server Ip:port)
#      parameter:  service/<Default Lease Time>/<Maximum Lease Time>/
#                  <Included Addresses>/<Excluded Addresses>/
#                  <Host Address>/<Hardware Address>/<Server Name> and other
#      subnet:     pool network IP which contain the parameter
#      dhcpHost:   host name in a pool network IP which contain the parameter
#
# OUT: ERROR:      if CLI errors or lease_type is wrong
#      VALUE:      the value for appropriate parameter 
#      NONE:       if there is no value for parameter
#############################################################
proc ShowDhcpServer {host parameter {subnet no_subnet} {dhcpHost no_host}} {
   global cmdOut
   set err_count [GetGlobalErr]

#    if {$lease_type != "available" && $lease_type != "in-use" && $lease_type != "abandoned" && $lease_type != "reserved"} {
#       return [ErrCheck "{ERROR: bad parameter: lease type = $lease_type; \nit must be available/in-use/abandoned/reserved}" GetDhcpStatus]
#    }

   SetCliLevel "PRIVILEGE" $host
   Exec "terminal paging off" "PRIVILEGE" $host

   Exec "show ip dhcp server" "PRIVILEGE" $host 0 60

   if {[CheckGlobalErr $err_count] == "ERROR"} {
      return "ERROR"
   }

   set lines ""
   set add_line 0
   set add_line_1 0
   
   foreach line [split $cmdOut "\n\r"] {
      
      if {$subnet == "no_subnet" && $dhcpHost == "no_host"} {
         set add_line 1
         if {[regexp -nocase "^\[\ \t\]*Subnet:" $line == 1]} {
            break 
         }
      }

      if  {$subnet != "no_subnet" && $dhcpHost == "no_host"} {
         if { $add_line == 1 && [regexp -nocase "^\[\ \t\]*Subnet:" $line == 1]} {
            break
         }
         if {[regexp -nocase "^\[\ \t\]*Subnet:\[\ \t\]*$subnet" $line == 1]} {
            set add_line 1
         }
      }

      if  {$subnet != "no_subnet" && $dhcpHost != "no_host"} {
         if { $add_line == 1 && [regexp -nocase "^\[\ \t\]*Subnet:" $line == 1]} {
            break
         }
         if {[regexp -nocase "^\[\ \t\]*Subnet:\[\ \t\]*$subnet" $line == 1]} {
            set add_line_1 1
         }
         if {$add_line_1 == 1 && [regexp -nocase "^\[\ \t\]*Host:\[\ \t\]*$dhcpHost" $line == 1]} {
            set add_line 1
         }
      }

      if {$add_line == 1} {
         lappend lines $line
      }
   }

#   puts "\nlines= $lines \n"

   foreach line $lines {
      if {[regexp -nocase "^\[\ \t\]*$parameter:(.*)" $line all value] == 1} {
         return [string trim $value]
      }
   }

   return "NONE"
}



  






###############
# ip local pool
############### 

#############################################################
# IpLocalPoolAdd: Add a new local pool.
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      name:    Name of a specific local pool
#      ipaddrL: Lowest IP address in the pool
#      ipaddrH: Highest IP address in the pool
#      mask:    Subnet mask - optional for IPSec tunnels only
#               Default = 'NO' - add a local pool without setting 
#               the mask value (for the cases when mask is optional).
#
# OUT: SUCCESS/ERROR
#############################################################
proc IpLocalPoolAdd {host name ipaddrL ipaddrH {mask "NO"}} {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   
   # the case when mask is not required
   if {$mask == "NO"} {
      Exec "ip local pool add $name $ipaddrL $ipaddrH" "CONFIG" $host
   } else {
      Exec "ip local pool add $name $ipaddrL $ipaddrH $mask" "CONFIG" $host
   }

   SetCliLevel "PRIVILEGE" $host
   
   return [CheckGlobalErr $err_count]
}

#############################################################
# IpLocalPoolAddv8: Add a new local pool.
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      name:    Name of a specific local pool
#      ipaddrL: Lowest IP address in the pool
#      ipaddrH: Highest IP address in the pool
#      mask:    Subnet mask - optional for IPSec tunnels only
#               Default = 'NO' - add a local pool without setting 
#               the mask value (for the cases when mask is optional).
#
# OUT: SUCCESS/ERROR
#############################################################
proc IpLocalPoolAddv8 {host name ipaddrL ipaddrH {mask "NO"}} {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   
   # the case when mask is not required
   if {$mask == "NO"} {
      Exec "ip address-pool local-pool add $name $ipaddrL $ipaddrH" "CONFIG" $host
   } else {
      Exec "ip address-pool local-pool add $name $ipaddrL $ipaddrH $mask" "CONFIG" $host
   }

   SetCliLevel "PRIVILEGE" $host
   
   return [CheckGlobalErr $err_count]
}

#############################################################
# IpLocalPoolDel: Disable a pool.
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      name:    Name of a specific local pool
#
# OUT: SUCCESS/ERROR
#############################################################
proc IpLocalPoolDel {host name} {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
      
   Exec "no ip local pool $name" "CONFIG" $host   

   return [CheckGlobalErr $err_count]   
}

#############################################################
# IpLocalPoolDelv8: Disable a pool.
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      name:    Name of a specific local pool
#
# OUT: SUCCESS/ERROR
#############################################################
proc IpLocalPoolDelv8 {host name} {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
      
   Exec "no ip address-pool local-pool $name" "CONFIG" $host   

   return [CheckGlobalErr $err_count]   
}

#############################################################
# IpLocalPoolEdit: Edit a specific local pool
#
# IN:  host:       (management IP)/(terminal server Ip:port)
#      name:       Name of a specific local pool
#      ipaddrL:    Lowest IP address in the pool
#      ipaddrH:    Highest IP address in the pool
#      newIpAddrL: New lowest IP address in the pool
#      newIpAddrH: New highest IP address in the pool
#      mask:       Subnet mask - optional for IPSec tunnels only
#                  Default = 'NO' - add a local pool without setting 
#                  the mask value (for the cases when mask is optional).
#
# OUT: SUCCESS/ERROR
#############################################################
proc IpLocalPoolEdit {host name ipAddrL ipAddrH newIpAddrL newIpAddrH {mask "NO"}} {
   
   global cmdOut
   set rcode ""

   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   
   # the case when mask is not required
   if {$mask == "NO"} {
      Exec "ip local pool $name $ipAddrL $ipAddrH $newIpAddrL $newIpAddrH" "CONFIG" $host
   } else {
      Exec "ip local pool $name $ipAddrL $ipAddrH $newIpAddrL $newIpAddrH $mask" "CONFIG" $host
   }

   if {[regexp "does not exist" $cmdOut] == 1} {
      lappend rcode "ERROR:\n$cmdOut"
      ErrCheck $rcode
   }

   return [CheckGlobalErr $err_count]
}


#############################################################
# IpLocalPoolShow: Uses 'show ip local pool' CLI command to disply
#                  the local pools. 
#                  Returns the output of the CLI command. This can
#                  be used to get more details regarding IP pools.
#
# IN:  host: (management IP)/(terminal server Ip:port)
#
# OUT: <'show ...' CLI command output>/ERROR
#############################################################
proc IpLocalPoolShow {host} {
   global cmdOut
   
   set err_count [GetGlobalErr]
   SetCliLevel "PRIVILEGE" $host
   Exec "show ip local pool" "PRIVILEGE" $host
   
   if {[CheckGlobalErr $err_count] != "ERROR"} {
      return $cmdOut
   } else {
      return "ERROR"
   }
   
}

#############################################################
# IpLocalPoolDefault: Defines the default local pool.
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      ipaddrL: Lowest IP address in the pool
#      ipaddrH: Highest IP address in the pool
#      mask:    Subnet mask - optional for IPSec tunnels only
#               Default = 'NO' - add a local pool without setting 
#               the mask value (for the cases when mask is optional).
#
# OUT: SUCCESS/ERROR
#############################################################
proc IpLocalPoolDefault {host ipaddrL ipaddrH {mask "NO"}} {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   
   # the case when mask is not required
   if {$mask == "NO"} {
      Exec "ip local pool default $ipaddrL $ipaddrH" "CONFIG" $host
   } else {
      Exec "ip local pool default $ipaddrL $ipaddrH $mask" "CONFIG" $host
   }

   return [CheckGlobalErr $err_count]
}

#############################################################
# IpLocalPoolDefaultv8: Defines the default local pool.
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      ipaddrL: Lowest IP address in the pool
#      ipaddrH: Highest IP address in the pool
#      mask:    Subnet mask - optional for IPSec tunnels only
#               Default = 'NO' - add a local pool without setting 
#               the mask value (for the cases when mask is optional).
#
# OUT: SUCCESS/ERROR
#############################################################
proc IpLocalPoolDefaultv8 {host ipaddrL ipaddrH {mask "NO"}} {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   
   # the case when mask is not required
   if {$mask == "NO"} {
      Exec "ip address-pool local-pool default $ipaddrL $ipaddrH" "CONFIG" $host
   } else {
      Exec "ip address-pool local-pool default $ipaddrL $ipaddrH $mask" "CONFIG" $host
   }

   return [CheckGlobalErr $err_count]
}

#############################################################
# IpLocalPoolUnavailable: Sets the action if a specific local pool is not defined.
#
# IN:  host:   (management IP)/(terminal server Ip:port)
#      action: action to take <failover/deny-address>
#
# OUT: SUCCESS/ERROR
#############################################################
proc IpLocalPoolUnavailable { host action } {
   set err_count [GetGlobalErr]
   set rcode ""
   SetCliLevel "CONFIG" $host
   
   switch $action {
      "failover" {
         Exec "ip local pool unavailable failover" "CONFIG" $host
      }
   
      "deny-address" {
         Exec "ip local pool unavailable deny-address" "CONFIG" $host
      }
      
      default {
         lappend rcode "ERROR: Option $action does not exist!"
         ErrCheck $rcode
      }
   }
   
   return [CheckGlobalErr $err_count]
   
}

#############################################################
# IpLocalPoolUnavailablev8: Sets the action if a specific local pool is not defined.
#
# IN:  host:   (management IP)/(terminal server Ip:port)
#      action: action to take <failover/deny-address>
#
# OUT: SUCCESS/ERROR
#############################################################
proc IpLocalPoolUnavailablev8 { host action } {
   set err_count [GetGlobalErr]
   set rcode ""
   SetCliLevel "CONFIG" $host
   
   switch $action {
      "failover" {
         Exec "ip address-pool local-pool unavailable failover" "CONFIG" $host
      }
   
      "deny-address" {
         Exec "ip address-pool local-pool unavailable deny-address" "CONFIG" $host
      }
      
      default {
         lappend rcode "ERROR: Option $action does not exist!"
         ErrCheck $rcode
      }
   }
   
   return [CheckGlobalErr $err_count]
   
}

#############################################################
# IpLocalPoolBlackout: Sets the blackout interval for internal address pool
#
# IN:  host:  (management IP)/(terminal server Ip:port)
#      value: value of the blackout interval in seconds <0-86400>
#
# OUT: SUCCESS/ERROR
#############################################################
proc IpLocalPoolBlackout { host value } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   
   Exec "ip local pool blackout-interval $value" "CONFIG" $host
   SetCliLevel "PRIVILEGE" $host
   
   return [CheckGlobalErr $err_count]
   
}

#############################################################
# IpLocalPoolBlackoutv8: Sets the blackout interval for internal address pool
#
# IN:  host:  (management IP)/(terminal server Ip:port)
#      value: value of the blackout interval in seconds <0-86400>
#
# OUT: SUCCESS/ERROR
#############################################################
proc IpLocalPoolBlackoutv8 { host value } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   
   Exec "ip address-pool local-pool blackout-interval $value" "CONFIG" $host

   SetCliLevel "PRIVILEGE" $host
   
   return [CheckGlobalErr $err_count]
   
}

#############################################################
# IpDhcpProxyServerAddrRelease: Set the immediate address release state <enable/disable>
#
# IN:  host:  (management IP)/(terminal server Ip:port)
#      state: <enable/disable>
#
# OUT: SUCCESS/ERROR
#############################################################
proc IpDhcpProxyServerAddrRelease { host state } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   
   switch $state {
      "enable" {
         Exec "ip dhcp proxy-server address-release" "CONFIG" $host
      }
      "disable" {
         Exec "no ip dhcp proxy-server address-release" "CONFIG" $host
      }
      default {
         lappend rcode "ERROR: Option should be enable/disable!"
         ErrCheck $rcode
      }
   }
   
   return [CheckGlobalErr $err_count]
}

#############################################################
# IpDhcpProxyServerAddrReleasev8: Set the immediate address release state <enable/disable>
#
# IN:  host:  (management IP)/(terminal server Ip:port)
#      state: <enable/disable>
#
# OUT: SUCCESS/ERROR
#############################################################
proc IpDhcpProxyServerAddrReleasev8 { host state } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   
   switch $state {
      "enable" {
         Exec "ip address-pool external-dhcp address-release" "CONFIG" $host
      }
      "disable" {
         Exec "no ip address-pool external-dhcp address-release" "CONFIG" $host
      }
      default {
         lappend rcode "ERROR: Option should be enable/disable!"
         ErrCheck $rcode
      }
   }
   
   return [CheckGlobalErr $err_count]
}

#############################################################
# IpDhcpProxyServer: Set the type of DHCP server that is used
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      value:   type of DHCP server that is used <any/internal/primary/secondary/tertiary>
#      address: IP address for <primary/secondary/tertiary> servers 
#
# OUT: SUCCESS/ERROR
#############################################################
proc IpDhcpProxyServer { host value {address ""} } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   
   switch $value {
      "any" {
         Exec "ip dhcp proxy-server any" "CONFIG" $host
      }
      "internal" {
         Exec "ip dhcp proxy-server internal" "CONFIG" $host
      }
      default {
         Exec "ip dhcp proxy-server $value $address" "CONFIG" $host
      }
   }

   return [CheckGlobalErr $err_count]
}

#############################################################
# IpDhcpProxyServerv8: Set the type of DHCP server that is used
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      value:   type of DHCP server that is used <any/internal/primary/secondary/tertiary>
#      address: IP address for <primary/secondary/tertiary> servers 
#
# OUT: SUCCESS/ERROR
#############################################################
proc IpDhcpProxyServerv8 { host {value ""} {address ""} } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   
   switch $value {
      "any" {
         Exec "ip address-pool external-dhcp any" "CONFIG" $host
      }
      "internal" {
         Exec "ip address-pool internal-dhcp" "CONFIG" $host
      }
      default {
         Exec "ip address-pool external-dhcp $value $address" "CONFIG" $host
      }
   }

   return [CheckGlobalErr $err_count]
}

#############################################################
# IpDhcpProxyServerV8: Set the type of DHCP server that is used
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      value:   type of DHCP server that is used <any/internal/primary/secondary/tertiary>
#      address: IP address for <primary/secondary/tertiary> servers 
#
# OUT: SUCCESS/ERROR
#############################################################
proc IpDhcpProxyServerV8 { host {value ""} {address ""} } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   
   switch $value {
      "any" {
         Exec "ip address-pool external-dhcp any" "CONFIG" $host
      }
      "internal" {
         Exec "ip address-pool internal-dhcp" "CONFIG" $host
      }
      "default" {
         Exec "ip address-pool external-dhcp $value $address" "CONFIG" $host
      }
      
   }

   return [CheckGlobalErr $err_count]
}

#############################################################
# IpDhcpProxyServerNewCmd: Set the type of DHCP server that is used
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      value:   type of DHCP server that is used <any/internal/primary/secondary/tertiary>
#      address: IP address for <primary/secondary/tertiary> servers 
#
# OUT: SUCCESS/ERROR
#############################################################
proc IpDhcpProxyServerNewCmd { host value {address ""} } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   
   switch $value {
      "any" {
         Exec "ip address-pool external-dhcp any" "CONFIG" $host
      }
      "internal" {
         Exec "ip address-pool external-dhcp internal" "CONFIG" $host
      }
      default {
         Exec "ip address-pool external-dhcp $value $address" "CONFIG" $host
      }
   }

   return [CheckGlobalErr $err_count]
}

#############################################################
# IpDhcpProxyServerCacheSize: Sets cache-size for DHCP proxy server
#
# IN:  host:  (management IP)/(terminal server Ip:port)
#      value: value of cache-size (number of IP addresses) <1-5000>
#
# OUT: SUCCESS/ERROR
#############################################################
proc IpDhcpProxyServerCacheSize { host value } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   
   Exec "ip dhcp proxy-server cache-size $value" "CONFIG" $host
   
   return [CheckGlobalErr $err_count]
}

#############################################################
# IpDhcpProxyServerCacheSizev8: Sets cache-size for DHCP proxy server
#
# IN:  host:  (management IP)/(terminal server Ip:port)
#      value: value of cache-size (number of IP addresses) <1-5000>
#
# OUT: SUCCESS/ERROR
#############################################################
proc IpDhcpProxyServerCacheSizev8 { host value } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   
   Exec "ip address-pool external-dhcp cache-size $value" "CONFIG" $host
   
   return [CheckGlobalErr $err_count]
}

#############################################################
# IpDhcpProxyServerBlackoutInterval: Sets the blackout interval for internal address pool
#
# IN:  host:  (management IP)/(terminal server Ip:port)
#      value: value of the blackout interval in seconds <300-86400> or override
#
# OUT: SUCCESS/ERROR
#############################################################
proc IpDhcpProxyServerBlackoutInterval { host value } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   
   Exec "ip dhcp  proxy-server blackout-interval $value" "CONFIG" $host
   
   return [CheckGlobalErr $err_count]
}

#############################################################
# IpDhcpProxyServerBlackoutIntervalv8: Sets the blackout interval for external DHCP
#
# IN:  host:  (management IP)/(terminal server Ip:port)
#      value: value of the blackout interval in seconds <300-86400> or override
#
# OUT: SUCCESS/ERROR
#############################################################
proc IpDhcpProxyServerBlackoutIntervalv8 { host value } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   
   Exec "ip address-pool external-dhcp blackout-interval $value" "CONFIG" $host
   
   return [CheckGlobalErr $err_count]
}

#############################################################
# EnterDhcpServerConfig: Enter into dhcp server config mode.
#
# IN:  host: (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc EnterDhcpServerConfig { host } {
   set prompt "CES\\(config-dhcp\\)\#"

   set err_count [GetGlobalErr] 
   
   SetCliLevel "CONFIG" $host
   
   Exec "ip dhcp server pool" $prompt $host

   return [CheckGlobalErr $err_count]
}

#############################################################
# ConfigDhcpLease: Configure lease time for dhcp server.
#
# IN:  host:  (management IP)/(terminal server Ip:port)
#      type:  <default/maximum>.
#      value: <0-999>  Number of logins
#
# OUT: SUCCESS/ERROR
#############################################################
proc ConfigDhcpLease { host type value } {
   set prompt "CES\\(config-dhcp\\)\#"

   set err_count [GetGlobalErr] 
   
   EnterDhcpServerConfig $host 
   
   Exec "lease $type $value" $prompt $host

   SetCliLevel "CONFIG" $host

   return [CheckGlobalErr $err_count]
}

#############################################################
# DisableDhcpLease: Disable lease time for dhcp server.
#
# IN:  host:  (management IP)/(terminal server Ip:port)
#      type:  <default/maximum>.
#
# OUT: SUCCESS/ERROR
#############################################################
proc DisableDhcpLease { host type } {
   set prompt "CES\\(config-dhcp\\)\#"

   set err_count [GetGlobalErr] 
   
   EnterDhcpServerConfig $host 
   
   Exec "no lease $type" $prompt $host

   SetCliLevel "CONFIG" $host

   return [CheckGlobalErr $err_count]
}

#############################################################
# EnterDhcpServerPoolConfig: Enter into dhcp server pool config mode.
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      network: network from which the server will asign addresses <A.B.C.D>
#      mask:    network mask <A.B.C.D>
#
# OUT: SUCCESS/ERROR
#############################################################
proc EnterDhcpServerPoolConfig { host network mask } {
   set prompt "CES\\(config-dhcp\\)\#"

   set err_count [GetGlobalErr] 
   
   SetCliLevel "CONFIG" $host
   
   Exec "ip dhcp server pool network $network mask $mask" $prompt $host
   
   return [CheckGlobalErr $err_count]   
}

#############################################################
# DhcpServerPoolIncludedAddr: Add an address pool for dhcp server.
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      network: network from which the server will asign addresses <A.B.C.D>
#      mask:    network mask <A.B.C.D>
#      lowest:  lowest address from network <A.B.C.D>
#      highest: highest address from network <A.B.C.D>
#
# OUT: SUCCESS/ERROR
#############################################################
proc DhcpServerPoolIncludedAddr { host network mask lowest highest } {
   set prompt "CES\\(config-dhcp\\)\#"

   set err_count [GetGlobalErr] 
   
   EnterDhcpServerPoolConfig $host $network $mask

   Exec "included-address $lowest $highest" $prompt $host
   
   SetCliLevel "CONFIG" $host

   return [CheckGlobalErr $err_count]
}


#############################################################
# DhcpServerPoolExcludedAddr: Exclude an (or more) address for dhcp server pool.
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      network: network from which the server will asign addresses <A.B.C.D>
#      mask:    network mask <A.B.C.D>
#      lowest:  lowest address from network <A.B.C.D>
#      highest: highest address from network <A.B.C.D>
#               can be omitted.
#
# OUT: SUCCESS/ERROR
#############################################################
proc DhcpServerPoolExcludedAddr { host network mask lowest {highest ""}} {
   set prompt "CES\\(config-dhcp\\)\#"

   set err_count [GetGlobalErr] 
   
   EnterDhcpServerPoolConfig $host $network $mask

   Exec "excluded-address $lowest $highest" $prompt $host
   
   SetCliLevel "CONFIG" $host

   return [CheckGlobalErr $err_count]
}



#############################################################
# DhcpServerPoolName: Add a name for this pool.
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      network: network from which the server will asign addresses <A.B.C.D>
#      mask:    network mask <A.B.C.D>
#      name:    subnet name
#
# OUT: SUCCESS/ERROR
#############################################################
proc DhcpServerPoolName { host network mask name } {
   set prompt "CES\\(config-dhcp\\)\#"

   set err_count [GetGlobalErr] 
   
   EnterDhcpServerPoolConfig $host $network $mask

   Exec "name $name" $prompt $host
   
   SetCliLevel "CONFIG" $host

   return [CheckGlobalErr $err_count]
}

#############################################################
# ConfigDhcpPoolOption: Configure option for dhcp server.
#
# IN:  host:   (management IP)/(terminal server Ip:port)
#      option:  client-identifier    Client identifier
#               default-router       Default router
#               dns-server           DNS server
#               domain-name          Domain name
#               netbios-name-server  WINS server
#               netbios-node-type    Netbios node type
#               <1-254>              refer to the RFC
#
#      value:   option's value:
#               WORD for client-identifier, domain-name
#               <A.B.C.D> for default-router, dns-server, netbios-name-server
#               <b-node/h-node/m-node/p-node> for netbios-node-type
#               peer <type value> for <1-254> option,
#                   with type <ascii/hex/integer/ip>
#               eq: ConfigDhcpPoolOption 10.2.1.1 1.1.1.0 255.255.255.0 2 "integer 21"
#              
# OUT: SUCCESS/ERROR
#############################################################
proc ConfigDhcpPoolOption {host network mask option value} {
   set prompt "CES\\(config-dhcp\\)\#"

   set err_count [GetGlobalErr] 

   EnterDhcpServerPoolConfig $host $network $mask
   Exec "option $option $value" $prompt $host

   SetCliLevel "CONFIG" $host

   return [CheckGlobalErr $err_count]
}

#############################################################
# EnterDhcpServerPoolHostConfig: Enter into dhcp server pool 
#                                host config mode.
#
# IN:  host:     (management IP)/(terminal server Ip:port)
#      network:  network from which the server will asign addresses <A.B.C.D>
#      hostname: hostname or IP
#
# OUT: SUCCESS/ERROR
#############################################################
proc EnterDhcpServerPoolHostConfig {host network hostname} {
   set prompt "CES\\(config-dhcp\\)\#"

   set err_count [GetGlobalErr] 
   
   SetCliLevel "CONFIG" $host
   
   Exec "ip dhcp server pool network $network host $hostname" $prompt $host
   
   return [CheckGlobalErr $err_count]
}


#############################################################
# DhcpServerPoolHostConfig: Config a list of parameters for
#                                dhcp server pool host
#
# IN:  host:       (management IP)/(terminal server Ip:port)
#      network:    network from which the server will asign addresses <A.B.C.D>
#      hostname:   hostname or IP
#      param_list: list of peer {<name of parameter> <value>}
#                  You can use "-" if you want to unconfig a parameter.
#                  parameters:
#                    bootfile/-bootfile                Boot image file name
#                    hardware-address/-hardware-addres Mac address (Example: 0:0:c0:5d:bd:9)
#                    host/-host                        Host IP address (A.B.C.D)
#                    lease/-lease                      Lease time: default <0-999>
#                                                                   default infinite
#                                                                   maximum <0-999>
#                                                                   maximum infinite
#                    next-server/-next-server          Next server IP address (A.B.C.D)
#                    option/-option                    DHCP option: 
#                                                       any dhcp option and value existing in CES CLI  
#                    server-name/-server-name          Server name
#
#               You can use "-" if you want to unconfig a parameter. 
#               In this case you need a second parameter, only for "lease" and "option"
#               Example: EnterDhcpServerPoolHostConfig 10.9.9.10 10.2.5.0 hostname {-host -lease default -option 10}
#
#   IMPORTANT:  Every value for a parameter which have more than 1 word need to put it in brace {}
#               Example: EnterDhcpServerPoolHostConfig 10.9.9.10 10.2.5.0 hostname {{host 10.2.5.11 lease {default infinite}}
#
# OUT: SUCCESS/ERROR
#############################################################
proc DhcpServerPoolHostConfig {host network hostname param_list} {
   set prompt "CES\\(config-dhcp\\)\#"

   set err_count [GetGlobalErr]
   
   EnterDhcpServerPoolHostConfig $host $network $hostname
   
   # Get and set possible options
   set i 1
   foreach parameter $param_list {
      if {[regexp "^-\[bhns\](.*)" $parameter ] == 1} {
         set param_list [linsert $param_list $i {}]
         incr i
      }
      incr i
   }

#puts "\n\nparam list: $param_list\n\n"
   set parameters {bootfile -bootfile hardware-address -hardware-address host -host \
                       lease -lease next-server -next-server option -option server-name -server-name}

#puts "\n\nparam: $parameters\n\n"
#puts "\n\nparam list: $param_list\n\n"

   foreach {parameter value} $param_list {
   #      puts "\nparam=$parameter value=$value\n"
      if { [lsearch -exact $parameters $parameter] == "-1" } {
         ErrCheck "{ERROR: bad parameter: parameter = $parameter \n This parameter will not be set}" DhcpServerPoolHostConfig

      } elseif {[regexp "^-(.*)" $parameter all  real_param] ==1} {
         Exec "no $real_param $value" $prompt $host
      } else {
         Exec "$parameter $value" $prompt $host
      }
   }
   
   SetCliLevel "CONFIG" $host

   return [CheckGlobalErr $err_count]
}


proc DisableDhcpServerPool { host network } {
   set err_count [GetGlobalErr] 
   
   SetCliLevel "CONFIG" $host
   
   Exec "no ip dhcp server pool network $network" "CONFIG" $host
   
   return [CheckGlobalErr $err_count]
}

#############################################################
# DeleteDhcpServerPool: Delete dhcp server network pool.
#
# IN:  host:     (management IP)/(terminal server Ip:port)
#      network:  network from which the server will asign addresses <A.B.C.D>
#      mask   :  mask
#
# OUT: SUCCESS/ERROR
#############################################################
proc DeleteDhcpServerPool {host network} {

   set err_count [GetGlobalErr] 
   
   SetCliLevel "CONFIG" $host
   
   Exec "no ip dhcp server pool network $network" "CONFIG" $host
   
   return [CheckGlobalErr $err_count]
}

#############################################################
# DeleteDhcpServerPoolHost: Delete dhcp server pool host.
#
# IN:  host:     (management IP)/(terminal server Ip:port)
#      network:  network from which the server will asign addresses <A.B.C.D>
#      hostname: hostname or IP
#
# OUT: SUCCESS/ERROR
#############################################################
proc DeleteDhcpServerPoolHost {host network hostname} {

   set err_count [GetGlobalErr] 
   
   SetCliLevel "CONFIG" $host
   
   Exec "no ip dhcp server pool network $network host $hostname" "CONFIG" $host
   
   return [CheckGlobalErr $err_count]
}


#############################################################
# DeleteDhcpServerPoolHost: Delete dhcp server pool host.
#
# IN:  host:     (management IP)/(terminal server Ip:port)
#      network:  network from which the server will asign addresses <A.B.C.D>
#      hostname: hostname or IP
#
# OUT: SUCCESS/ERROR
#############################################################
proc DeleteDhcpServerPoolHost {host network hostname} {

   set err_count [GetGlobalErr] 
   
   SetCliLevel "CONFIG" $host
   
   Exec "no ip dhcp server pool network $network host $hostname" "CONFIG" $host
   
   return [CheckGlobalErr $err_count]
}

#############################################################
# SetDhcpRelayState: Enable/disable Dhcp-relay.
#
# IN:  host:   (management IP)/(terminal server Ip:port)
#      state:  enable/disable
#
# OUT: SUCCESS/ERROR
#############################################################
proc SetDhcpRelayState {host state} {
   set err_count [GetGlobalErr] 

   SetCliLevel "CONFIG" $host
   
   if {$state == "enable"} {
      Exec "ip forward-protocol dhcp-relay" "CONFIG" $host
   } elseif {$state == "disable"} {
      Exec "no ip forward-protocol dhcp-relay" "CONFIG" $host
   } else {
      return [ErrCheck "{ERROR: bad parameter: state = $state}" SetDhcpRelayState]
   }
   return [CheckGlobalErr $err_count]
}


#############################################################
# ConfigDhcpRelayIf: Configures DHCP relay.
#
# IN:  host:        (management IP)/(terminal server Ip:port)
#      interfaceIP: A.B.C.D  Interface IP address
#      state:  enable/disable/"" 
#                "" - for setting a dhcp-relay interface - the state will be disable
#
# OUT: SUCCESS/ERROR
#############################################################
proc ConfigDhcpRelayIf {host interfaceIP {state ""}} {
   set err_count [GetGlobalErr] 
   
   SetCliLevel "CONFIG" $host
   
   Exec "ip dhcp-relay $interfaceIP $state" "CONFIG" $host
   
   return [CheckGlobalErr $err_count]
}


#############################################################
# DelDhcpRelayIf: Delete DHCP relay for an interface.
#
# IN:  host:        (management IP)/(terminal server Ip:port)
#      interfaceIP: A.B.C.D  Interface IP address
#
# OUT: SUCCESS/ERROR
#############################################################
proc DelDhcpRelayIf {host interfaceIP} {
   set err_count [GetGlobalErr] 
   
   SetCliLevel "CONFIG" $host
   
   Exec "no ip dhcp-relay $interfaceIP" "CONFIG" $host
   
   return [CheckGlobalErr $err_count]
}


#############################################################
# ConfigDhcpRelayHelper: Specifies a DHCP relay server IP address.
#
# IN:  host:        (management IP)/(terminal server Ip:port)
#      interfaceIP: A.B.C.D  Interface IP address
#      server_no:   <1/2/3>
#      serverIP:    A.B.C.D  Destination host address to be used 
#                            when forwarding DHCP broadcasts
#
# OUT: SUCCESS/ERROR
#############################################################
proc ConfigDhcpRelayHelper {host interfaceIP server_no serverIP} {

   set err_count [GetGlobalErr] 
   
   SetCliLevel "CONFIG" $host
   
   Exec "ip helper-address $interfaceIP server $server_no $serverIP" "CONFIG" $host
   Exec "ip helper-address $interfaceIP server $server_no" "CONFIG" $host
   
   return [CheckGlobalErr $err_count]
}

#############################################################
# DeleteArpCache: Delete arp cache
#
# IN:  host:  (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc DeleteArpCache {host} {
   set err_count [GetGlobalErr]

   SetCliLevel "PRIVILEGE" $host
   
   Exec "clear arp-cache" "PRIVILEGE" $host
   
   return [CheckGlobalErr $err_count]
}
