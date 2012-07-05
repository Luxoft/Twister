######################################
# Router config procedures
#
# EnaRouterPolicy {host}
# DisRouterPolicy {host}
#
# InsertStaticRoute {host ipDest netMask ipGateway cost ena_dis}
# DeleteStaticRoute {host ipDest netMask ipGateway}
# GetIpRouteCost {host ipAddress mask {protocol ""}}
# GetIpRouteNextHop {host ipAddress mask {protocol ".*"}}
# AddDefGw { gw_ip host } 
# DelDefGw { gw_ip host }
# AddPrDefGw { host gw_ip {cost 5} {state "enable"}}
# DelPrDefGw { host gw_ip }
# GetRouteTable {host {proto ""} }
#
# ##
# rip
# ##
# EnableRip { host }
# DisableRip { host }
# EnterRouterRipCLILevel { host }
# SetRipUpdateInterval { time host }
# SetRipNetwork {networkIP networkMask host}
# DelRipNetwork {networkIP networkMask host}
# EnableRipRedistribute {redistributingType host}
# DisableRipRedistribute {redistributingType host}
# CheckRipDatabaseRoute {host address {mask "255.255.255.0"} {gw "no"}}
#
# ##
# osfp
# ##
# ArLicenseInstall {licence host}
# EnterRouterOspfCLILevel {host}
# ExitRouterOspfCLILevel {host}
# EnableOspf {host}
# DisableOspf {host}
# SetOspfRouterId {host routerId}
# SetOspfNetwork {host areaId networkIP {reverseMask "0.0.0.255"}}
# DelOspfNetwork {host areaId networkIP {reverseMask "0.0.0.255"}}
# EnableOspfRedistribute {redistributingType host}
# DisableOspfRedistribute {redistributingType host}
# OspfAddArea {areaId host}
# OspfDelArea {areaId host}
# OspfAddAreaRange {areaId network mask host}
# OspfDelAreaRange {areaId network mask host}
# EnableAreaStub {areaId host}
# DisableAreaStub {areaId host}
# OspfCompat3_6 {host}
# OspfNoCompat3_6 {host}
# OspfAutoVLink {host}
# OspfNoAutoVLink {host}
# OspfSetExtMetricType {host {extMetricType 1}}
# CheckOspfAdjacency {host routerId ipAddrRemote ipAddrLocal {virtual "no_virtual"}}
# GetDR {interface areaId host}
# VerifyLSID {lsidType lsid routerDR areaId host}
# VerifyASExtMetricType {lsid routerDR host}
# GetLSIDSequenceNo {lsidType lsid routerDR areaId  host}
# EnableAsbr { host }
# DisableAsbr { host }
#
# ##
# Access lists
# ##
# AccessList { host name action {network "any"} {netmask ""} {type ""} }
# DelAccessList { host name }
# List AccessList { host name }
# MoveAccessListRule { host name rule1 rule2 }
# RipDistributeList { host name type interfaceIp status }
# RipDelDistributeList { host name type interfaceIp }
# OspfDistributeList { host name type interfaceIp status }
# OspfDelDistributeList { host name type interfaceIp }
#
# ##
# CAR
# ##
# SetCarState { host state }
# EnterCarConfigLevel { host }
# SetCarAggregation { host state }
# ##
#
# VRRP
# ##
# EnableVrrp {host}
# DisableVrrp {host}
# EnterRouterVrrpCLILevel {host}
# ConfigVrrpAddress {host vrrpIP vrrpID {authentication none}}
# DeleteVrrpAddress {host vrrpIP}
# AddInterfaceToVrrp {host VrrpIP}
# DelInterfaceFromVrrp {host VrrpIP}
# AssignIfGroupVrrp {host ipMasterVrrp ifGrNo ifGroupName} 
# DisableIfGroupVrrp {host ipMasterVrrp ifGrNo ifGroupName} 
# DeleteIfGroupVrrp {host ipMasterVrrp ifGrNo
######################################




##########################
# EnterRouterRipCLILevel
#
# Description:
#     -enables RIP and enters in the config-rip CLI level 
#
##########################

proc EnaRouterPolicy {host} {

    SetCliLevel "CONFIG" $host
    Exec "route-policy" "CONFIG" $host
}


proc DisRouterPolicy {host} {

    SetCliLevel "CONFIG" $host
    Exec "no route-policy" "CONFIG" $host
}


################
# STATIC ROUTES
################

proc InsertStaticRoute {host ipDest netMask ipGateway {cost "no_cost"} {ena_dis "no"} } {
    global cmdOut

    set cmdOut ""
    set rcode ""

    SetCliLevel "CONFIG" $host

    if { $cost == "no_cost" && $ena_dis == "no" } {
        Exec "ip route $ipDest $netMask $ipGateway" "CONFIG" $host
    } elseif {$ena_dis == "no"} {
        Exec "ip route $ipDest $netMask $ipGateway $cost" "CONFIG" $host
    } else {
        Exec "ip route $ipDest $netMask $ipGateway $cost $ena_dis" "CONFIG" $host
    }

    if { [regexp -nocase {Invalid Gateway - can't be one of our LAN or Mgmt IP addresses} $cmdOut msg] == 1 || \
             [regexp -nocase {Mask [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+ is not valid} $cmdOut msg] == 1 || \
             [regexp -nocase {Invalid Gateway - Static Route gateway needs to be on directly attached netwo[\s\n\r]*rks} $cmdOut msg] == 1 || \
             [regexp -nocase {IP address and subnet mask are incompatible} $cmdOut msg] == 1 } {
        lappend rcode "ERROR: CES $host: Static route: $ipDest $netMask $ipGateway can't be set:\n----\n$msg\n----"
    }
        return [ErrCheck $rcode "InsertStaticRoute"]
}


proc DeleteStaticRoute {host ipDest netMask ipGateway} {
   global cmdOut

    set cmdOut ""
    set rcode ""

    SetCliLevel "CONFIG" $host

    Exec "no ip route $ipDest $netMask $ipGateway" "CONFIG" $host

    if { [regexp -nocase {Static Route [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+, [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+, [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+ does not exist} $cmdOut msg] == 1 } {
        lappend rcode "ERROR: CES $host: Static route: $ipDest $netMask $ipGateway can't be delete:\n----\n$msg\n----"
    }
        return [ErrCheck $rcode "DeleteStaticRoute"]
}


proc GetIpRouteCost {host ipAddress mask {protocol ".*"}} {
    global cmdOut

    set cmdOut ""
    set cost ""

    SetCliLevel "PRIVILEGE" $host
    Exec "show ip route" "PRIVILEGE" $host

    foreach line [split $cmdOut "\n"] {
        if { [regexp -nocase "$protocol\[\ \t\]+$ipAddress\[\ \t\]+$mask\[\ \t\]+\\\[\(\[0-9\]+\)\\\]" $line all cost] == 1} {
            return "$cost"
        }
    }
    return "NOROUTE"
}

proc GetIpRouteNextHop {host ipAddress mask {protocol ".*"}} {
    global cmdOut

    set cmdOut ""
    set cost ""

    SetCliLevel "PRIVILEGE" $host
    Exec "show ip route all" "PRIVILEGE" $host

    foreach line [split $cmdOut "\n"] {
        if { [regexp -nocase "$protocol\[\ \t\]+$ipAddress\[\ \t\]+$mask\[\ \t\]+\\\[\[0-9\]+\\\]\[\ \t\]+\(\[0-9.\]+\)" $line all nextHop] == 1} {
            return "$nextHop"
        }
    }
    return "NOROUTE"
}


#############################################
# AddDefGw: add a default gateway on CES
#           
# IN:  gw_ip: IP address of the gateway or ip address of outgoing WAN interface
#      host:  management IP / terminal server IP:port
#
# OUT: SUCCESS/ERROR
#
#############################################
proc AddDefGw { gw_ip host } {

   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host   
   Exec "ip route 0.0.0.0 255.255.255.255 $gw_ip" "CONFIG" $host
   
   return [CheckGlobalErr $err_count]
}

#############################################
# DelDefGw: delete a default gateway from CES
#
# IN:  gw_ip: IP address of the gateway or ip address of outgoing WAN interface
#      host:  management IP / terminal server IP:port
#
# OUT: SUCCESS/ERROR
#
#############################################
proc DelDefGw { gw_ip host } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host   
   Exec "no ip route 0.0.0.0 255.255.255.255 $gw_ip" "CONFIG" $host
   
   return [CheckGlobalErr $err_count]
}

#############################################
# AddPrDefGw: add a private default gateway on CES
#           
# IN:  host:  management IP / terminal server IP:port
#      gw_ip: IP address of the gateway or ip address of outgoing WAN interface
#      cost:  
#      state: 
#
# OUT: SUCCESS/ERROR
#
#############################################
proc AddPrDefGw { host gw_ip {cost 5} {state "enable"}} {

   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host   
   Exec "ip route 0.0.0.0 0.0.0.0 $gw_ip $cost $state" "CONFIG" $host
   
   return [CheckGlobalErr $err_count]
}

#############################################
# DelDefGw: delete a default gateway from CES
#
# IN:  host:  management IP / terminal server IP:port
#      gw_ip: IP address of the gateway or ip address of outgoing WAN interface
#
# OUT: SUCCESS/ERROR
#
#############################################
proc DelPrDefGw { host gw_ip } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host   
   Exec "no ip route 0.0.0.0 0.0.0.0 $gw_ip" "CONFIG" $host
   
   return [CheckGlobalErr $err_count]
}

###################################
#GetRouteTable: show route table on a specific host
#
#IN:   host:  management IP / terminal server IP:port
#      proto: all/rip/ospf/static/clip
#
#OUT: route table/ERROR
#
########################################

proc GetRouteTable { host { proto "" } } {
   set err_count [GetGlobalErr]
   global cmdOut
   set route_table ""
   SetCliLevel "PRIVILEGE" $host
   
   if { $proto != "" } {
      Exec "show ip route $proto" "PRIVILEGE" $host 0 120
      set route_table $cmdOut
   } else {
      Exec "show ip route" "PRIVILEGE" $host 0 120
      set route_table $cmdOut
   }

   if { [CheckGlobalErr $err_count] != "SUCCESS" } {
      return "ERROR"
   }
   return $route_table
}





##########
# rip
##########

proc EnableRip { host } { 
    
    SetCliLevel "CONFIG" $host

    Exec "router rip enable" "CONFIG" $host
}

proc DisableRip { host } {
    SetCliLevel "CONFIG" $host

    Exec "no router rip enable" "CONFIG" $host    
}


proc EnterRouterRipCLILevel { host } {
    set prompt "CES\\(config-rip\\)\#"  
    
    SetCliLevel "CONFIG" $host

    Exec "router rip" $prompt $host

}

proc ExitRouterRipCLILevel {host} {
    Exec "exit" "CONFIG" $host
}


proc SetRipUpdateInterval { time host } {
    set prompt "CES\\(config-rip\\)\#"

    EnterRouterRipCLILevel $host

    Exec "timers basic $time" $prompt $host

}

proc SetRipNetwork {networkIP networkMask host} {
    global cmdOut

    set cmdOut ""
    set rcode ""

    set prompt "CES\\(config-rip\\)\#"

    EnterRouterRipCLILevel $host

    if {[Exec "network $networkIP $networkMask" $prompt $host] != "SUCCESS" } {
        return "ERROR"
    } elseif { [regexp -nocase {This interface and mask does not exist} $cmdOut msg] == 1 || \
                   [regexp -nocase {This interface does not exist} $cmdOut msg] == 1 || \
                   [regexp -nocase {Mask [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+ is not valid} $cmdOut msg] == 1 || \
                   [regexp -nocase {Rip cannot be configured on a public interface} $cmdOut msg] == 1 } {
        lappend rcode "ERROR: CES $host: Interface: $networkIP $networkMask:\n----\n$msg\n----"
    }
    ExitRouterRipCLILevel $host
    return [ErrCheck $rcode "SetRipNetwork"]
}

proc DelRipNetwork {networkIP networkMask host} {
    global cmdOut

    set cmdOut ""
    set rcode ""

    set prompt "CES\\(config-rip\\)\#"

    EnterRouterRipCLILevel $host

    if {[Exec "no network $networkIP $networkMask" $prompt $host] != "SUCCESS" } {
        return "ERROR"
    } elseif { [regexp -nocase {Mask [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+ is not valid} $cmdOut msg] == 1} {
        lappend rcode "ERROR: CES $host: Interface: $networkIP $networkMask:\n----\n$msg\n----"
    }
    ExitRouterRipCLILevel $host
    return [ErrCheck $rcode "DelRipNetwork"]
}

proc EnableRipRedistribute {redistributingType host} {

    set prompt "CES\\(config-rip\\)\#"

    EnterRouterRipCLILevel $host

    Exec "redistribute $redistributingType" $prompt $host

    ExitRouterRipCLILevel $host
}


proc DisableRipRedistribute {redistributingType host} {

    set prompt "CES\\(config-rip\\)\#"

    EnterRouterRipCLILevel $host

    Exec "no redistribute $redistributingType" $prompt $host
    
    ExitRouterRipCLILevel $host
}


#############################################################
# VerifyRipDatabaseRoute: Verifies a route in RIP DataBase
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      address: A.B.C.D - IP
#      mask:    A.B.C.D
#      gw:      no/A.B.C.D 
#
#############################################################
proc CheckRipDatabaseRoute { host address {mask "255.255.255.0"} {gw "no"} } {

    global cmdOut
    set cmdOut ""

    SetCliLevel "PRIVILEGE" $host
    Exec "show ip rip database" "PRIVILEGE" $host
    if {$gw == "no"} {
        foreach line [split $cmdOut "\n"] {       
            if {[regexp -nocase "\[0-9\]\[\t\ \]+$address\[\t\ \]+$mask\[\t\ \]+\[A-Z\]+\[\t\ \]+\[0-9\]+\[\t\ \]+\[0-9\]+\[\t\ \]+\[0-9\.\]+" $line] == 1} {
                return "SUCCESS"
            }
        }
    } else {
        foreach line [split $cmdOut "\n"] {  
            if {[regexp -nocase "\[0-9\]\[\t\ \]+$address\[\t\ \]+$mask\[\t\ \]+\[A-Z\]+\[\t\ \]+\[0-9\]+\[\t\ \]+\[0-9\]+\[\t\ \]+$gw" $line] == 1} {
                return "SUCCESS"
            }
        }
    }
    return "ERROR"
}


########
# OSFP
########
proc ArLicenseInstall {license host} {
    SetCliLevel "CONFIG" $host
    Exec "license install ar $license" "CONFIG" $host
}

proc EnterRouterOspfCLILevel {host} {
    set prompt "CES\\(config-ospf\\)\#"

    SetCliLevel "CONFIG" $host

    Exec "router ospf" $prompt $host
        
}

proc ExitRouterOspfCLILevel {host} {
    Exec "exit" "CONFIG" $host
}

proc EnableOspf {host} {
   global cmdOut
   set err_count [GetGlobalErr]
   
   SetCliLevel "CONFIG" $host
   Exec "router ospf enable" "CONFIG" $host

   if {[regexp {This feature is not enabled} $cmdOut]} {
      ErrCheck [list "ERROR: This feature is not enabled"]
   }

   return [CheckGlobalErr $err_count]
}

proc DisableOspf {host} {
    SetCliLevel "CONFIG" $host
    Exec "no router ospf enable" "CONFIG" $host
}

##########################################################
# SetOspfRouterId: Sets router id
#
# IN:  host:       (management IP) / (terminal server Ip:port)
#      routerId:   A.B.C.D
# OUT: SUCCESS or ERROR
##########################################################
proc SetOspfRouterId {host routerId} {
    set err_count [GetGlobalErr]
    set prompt "CES\\(config-ospf\\)\#"

    EnterRouterOspfCLILevel $host
    Exec "router-id $routerId" $prompt $host

    return [CheckGlobalErr $err_count]
}

proc SetOspfNetwork {host areaId networkIP {reverseMask "0.0.0.255"}} {
    global cmdOut

    set cmdOut ""
    set rcode ""

    set prompt "CES\\(config-ospf\\)\#"

    EnterRouterOspfCLILevel $host

    if {[Exec "network $networkIP $reverseMask area $areaId" $prompt $host] != "SUCCESS" } {
        return "ERROR"
    } elseif { [regexp -nocase {Wild card bits [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+ are not valid} $cmdOut msg] == 1 || \
                   [regexp -nocase {Area [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+ does not exist} $cmdOut msg] == 1 || \
                   [regexp -nocase {Interface [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+ doesn't exist} $cmdOut msg] == 1 || \
                   [regexp -nocase {Network [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+ is already configured for ospf with area [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+} $cmdOut msg] == 1 } {
        lappend rcode "ERROR: CES $host: Network $networkIP $reverseMask area $areaId can't be set:\n----\n$msg\n----"
    }
    ExitRouterOspfCLILevel $host
    return [ErrCheck $rcode "SetOspfNetwork"]
}

proc DelOspfNetwork {host areaId networkIP {reverseMask "0.0.0.255"}} {
    global cmdOut

    set cmdOut ""
    set rcode ""

    set prompt "CES\\(config-ospf\\)\#"

    EnterRouterOspfCLILevel $host

    if {[Exec "no network $networkIP $reverseMask area $areaId" $prompt $host] != "SUCCESS" } {
        return "ERROR"
    } elseif { [regexp -nocase {No OSPF is configured on [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+} $cmdOut msg] == 1 || \
                   [regexp -nocase {Area [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+ does not exist} $cmdOut msg] == 1 || \
                   [regexp -nocase {This IP address [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+ is not associated with area [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+} $cmdOut msg] == 1 || \
                   [regexp -nocase {Wild card bits [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+ are not valid} $cmdOut msg] == 1} {
        lappend rcode "ERROR: CES $host: Network $networkIP $reverseMask area $areaId can't be deleted:\n----\n$msg\n----"
    }
    ExitRouterOspfCLILevel $host
    return [ErrCheck $rcode "DelOspfNetwork"]
}

proc EnableOspfRedistribute {redistributingType host} {
    global cmdOut

    set cmdOut ""
    set rcode ""

    set prompt "CES\\(config-ospf\\)\#"

    EnterRouterOspfCLILevel $host

    if {[Exec "redistribute $redistributingType" $prompt $host] != "SUCCESS" } {
        return "ERROR"
    } elseif { [regexp -nocase {CES needs to be configured as ASBR in OSPF to make redistribution effective} $cmdOut msg] == 1 } {
        lappend rcode "ERROR: CES $host: OSPF Redistribute can't be set:\n----\n$msg\n----"
    }
    ExitRouterOspfCLILevel $host
    return [ErrCheck $rcode "EnableOspfRedistribute"]
}

proc DisableOspfRedistribute {redistributingType host} {

    set prompt "CES\\(config-ospf\\)\#"

    EnterRouterOspfCLILevel $host

    Exec "no redistribute $redistributingType" $prompt $host
    
    ExitRouterOspfCLILevel $host
}

proc OspfAddArea {areaId host} {
    global cmdOut

    set cmdOut ""
    set rcode ""

    set prompt "CES\\(config-ospf\\)\#"

    EnterRouterOspfCLILevel $host

    if {[Exec "area $areaId" $prompt $host] != "SUCCESS" } {
        return "ERROR"
    }
    ExitRouterOspfCLILevel $host
    return "SUCCESS"
}

proc OspfDelArea {areaId host} {
  global cmdOut

    set cmdOut ""
    set rcode ""

    set prompt "CES\\(config-ospf\\)\#"

    EnterRouterOspfCLILevel $host

    if {[Exec "no area $areaId" $prompt $host] != "SUCCESS" } {
        return "ERROR"
    }
    if { [regexp -nocase {Backbone area cannot be deleted in CES} $cmdOut msg] == 1 || \
         [regexp -nocase {Area [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+ does not exist} $cmdOut msg] == 1 || \
         [regexp -nocase {Move interface [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+ to a different area before deleting [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+} $cmdOut msg] == 1 }  {
        lappend rcode "ERROR: CES $host: Area $areaId can't be deleted:\n----\n$msg\n----"
    }
    ExitRouterOspfCLILevel $host
    return [ErrCheck $rcode "OspfDelArea"]
}

proc OspfAddAreaRange {areaId network mask host} {
    global cmdOut

    set cmdOut ""
    set rcode ""

    set prompt "CES\\(config-ospf\\)\#"

    EnterRouterOspfCLILevel $host

    if {[Exec "area $areaId range $network $mask" $prompt $host] != "SUCCESS" } {
        return "ERROR"
    }
    if { [regexp -nocase {Mask [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+ is not valid} $cmdOut msg] == 1 || \
         [regexp -nocase {Area [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+  does not exist} $cmdOut msg] == 1 || \
         [regexp -nocase {Invalid Range: Another interface in another area also belongs to this range} $cmdOut msg] == 1 || \
         [regexp -nocase {Network Address or Mask may be in error} $cmdOut msg] == 1 } {
        lappend rcode "ERROR: CES $host: Area $areaId can't add the range :\n----\n$msg\n----"
    }

    ExitRouterOspfCLILevel $host
    return [ErrCheck $rcode "OspfAddAreaRange"]

}

proc OspfDelAreaRange {areaId network mask host} {
  global cmdOut

    set cmdOut ""
    set rcode ""

    set prompt "CES\\(config-ospf\\)\#"

    EnterRouterOspfCLILevel $host

    if {[Exec "no area $areaId range $network $mask" $prompt $host] != "SUCCESS" } {
        return "ERROR"
    }
    if { [regexp -nocase {Mask [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+ is not valid} $cmdOut msg] == 1 || \
         [regexp -nocase {Area [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+  does not exist} $cmdOut msg] == 1 || \
         [regexp -nocase {Range: Addr [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+ Mask [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+ doesn't exist within Area [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+} $cmdOut msg] == 1}  {
        lappend rcode "ERROR: CES $host: Area $areaId can't delete the range :\n----\n$msg\n----"
    }
    ExitRouterOspfCLILevel $host
    return [ErrCheck $rcode "OspfDelAreaRange"]
}

proc EnableAreaStub {host areaId {no_summary "no"}} {
    global cmdOut

    set cmdOut ""
    set rcode ""

    set prompt "CES\\(config-ospf\\)\#"

    EnterRouterOspfCLILevel $host

    if {$no_summary == "no"} {
        if {[Exec "area $areaId stub" $prompt $host] != "SUCCESS" } {
         return "ERROR"
        }
     } else {
         if {[Exec "area $areaId stub $no_summary" $prompt $host] != "SUCCESS" } {
            return "ERROR"
        }
     }
    if { [regexp -nocase {This Backbone parameter cannot be modified in CES} $cmdOut msg] == 1 } {
        lappend rcode "ERROR: CES $host: Area $areaId can't be stub: \n----\n$msg\n----"
    }
    ExitRouterOspfCLILevel $host
    return [ErrCheck $rcode "EnableAreaStub"]
}


proc DisableAreaStub {host areaId} {
    global cmdOut

    set cmdOut ""
    set rcode ""

    set prompt "CES\\(config-ospf\\)\#"

    EnterRouterOspfCLILevel $host

    if {[Exec "no area $areaId stub" $prompt $host] != "SUCCESS" } {
        return "ERROR"
    }
    if { [regexp -nocase {This Backbone parameter cannot be modified in CES} $cmdOut msg] == 1  || \
         [regexp -nocase {Area [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+ does not exist} $cmdOut msg] == 1 }  {
        lappend rcode "ERROR: CES $host: Area $areaId can't be \"no stub\":\n----\n$msg\n----"
    }
    ExitRouterOspfCLILevel $host
    return [ErrCheck $rcode "DisableAreaStub"]
}


proc OspfCompat3_6 {host} {
    set prompt "CES\\(config-ospf\\)\#"

    EnterRouterOspfCLILevel $host
    Exec "compat-3-6 enable" $prompt $host
    ExitRouterOspfCLILevel $host
}


proc OspfNoCompat3_6 {host} {
    set prompt "CES\\(config-ospf\\)\#"

    EnterRouterOspfCLILevel $host
    Exec "no compat-3-6 enable" $prompt $host
    ExitRouterOspfCLILevel $host
}


proc OspfAutoVLink {host} {
    set prompt "CES\\(config-ospf\\)\#"

    EnterRouterOspfCLILevel $host
    Exec "auto-vlink" $prompt $host
    ExitRouterOspfCLILevel $host
}


proc OspfNoAutoVLink {host} {
    set prompt "CES\\(config-ospf\\)\#"

    EnterRouterOspfCLILevel $host
    Exec "no auto-vlink" $prompt $host
    ExitRouterOspfCLILevel $host
}


proc OspfEnableAsbr {host} {
    set prompt "CES\\(config-ospf\\)\#"

    EnterRouterOspfCLILevel $host
    Exec "asbr" $prompt $host
    ExitRouterOspfCLILevel $host
}

proc OspfDisableAsbr {host} {
    set prompt "CES\\(config-ospf\\)\#"

    EnterRouterOspfCLILevel $host
    Exec "no asbr" $prompt $host
    ExitRouterOspfCLILevel $host
}

proc OspfSetExtMetricType {host {extMetricType 1}} {
    set prompt "CES\\(config-ospf\\)\#"

    EnterRouterOspfCLILevel $host
    Exec "external-metric type $extMetricType" $prompt $host
    ExitRouterOspfCLILevel $host
}


proc VerifyOspfAdjacency {host routerId ipRemoteAddr ipLocalAddr {virtual "no_virtual"}} {
    global cmdOut

    set cmdOut ""
    set neighbors ""
    set dynamicNeighbors ""
    set virtualNeighbors ""

    SetCliLevel "PRIVILEGE" $host
    if {[Exec "show ip ospf neighbor" "PRIVILEGE" $host] != "SUCCESS"} {
        return "ERROR"
    }

    regexp "(OSPF Dynamic Neighbors.*)(OSPF Virtual Neighbors.*)" $cmdOut neighbors dynamicNeighbors virtualNeighbors
    if {$neighbors == ""} {
        regexp "(OSPF Dynamic Neighbors.*)" $cmdOut neighbors dynamicNeighbors
    }

    if {$virtual == "no_virtual"} {
        foreach line [split $dynamicNeighbors "\n"] {
            if { [regexp -nocase "$routerId.*FULL.*$ipRemoteAddr\ +$ipLocalAddr" $line] == 1} {
                return "YES"
            }
        }
        return "NO"
    } elseif {$virtual == "virtual"} {
        foreach line [split $virtualNeighbors "\n"] {
            if { [regexp -nocase "$routerId.*FULL.*$ipRemoteAddr\ +$ipLocalAddr" $line] == 1} {
                return "YES"
            }
        }
        return "NO"
    }
}


proc GetDR {interface areaId host} {
    global cmdOut

    set cmdOut ""
    set routerId1 ""
    set routerId2 ""
    set i 0

    SetCliLevel "PRIVILEGE" $host
    Exec "show ip ospf interface" "PRIVILEGE" $host

    foreach line [split $cmdOut "\n"] {

        if { $i == 1} {
            regexp -nocase {^[\r0-9.]+$} $line routerId2
            break
        } 
        
        if { [regexp -nocase "$interface-.*$areaId.* (\[0-9.\]+)" $line all routerId1] == 1} {
            set i 1
        }
    } 

    return [append routerId1 [string trim $routerId2] ]
}


proc VerifyLSID {lsidType lsid routerDR areaId host} {
    global cmdOut

    set cmdOut ""
    set linkState ""

    SetCliLevel "PRIVILEGE" $host
    Exec "show ip ospf database" "PRIVILEGE" $host

    regexp "Displaying $lsidType Link States \\(Area $areaId\\).*?\(Displaying\)" $cmdOut linkState

    if {$linkState == ""} {
        regexp "Displaying $lsidType Link States \\(Area $areaId\\).*" $cmdOut linkState
    }

#    if {$linkState == ""} {
#        return [ErrCheck "LSID type or Area ID don't exist!" "OspfVerifyLSID"]
#    }

    foreach line [split $linkState "\n"] {
        if { [regexp -nocase "$lsid\[\t\ \]+$routerDR" $line] == 1} {
            return "YES"
        }
    }
    return "NO"
}

proc VerifyASExtMetricType {lsid routerDR host} {
    global cmdOut

    set cmdOut ""
    set linkState ""

    SetCliLevel "PRIVILEGE" $host
    Exec "show ip ospf database" "PRIVILEGE" $host

    regexp "Displaying AS Ext Link States \\(Area 0.0.0.0\\).*?\(Displaying\)" $cmdOut linkState

    if {$linkState == ""} {
        regexp "Displaying Ext Link Link States \\(Area 0.0.0.0\\).*" $cmdOut linkState
    }

    foreach line [split $linkState "\n"] {
        if { [regexp -nocase "$lsid\[\t\ \]+$routerDR.*\(Type\[12\]\)" $line all type] == 1} {
            return "$type"
        }
    }
    return "ERROR"
}

proc GetLSIDSequenceNo {lsidType lsid routerDR areaId  host} {

  global cmdOut

    set cmdOut ""
    set linkState ""

    SetCliLevel "PRIVILEGE" $host
    Exec "show ip ospf database" "PRIVILEGE" $host

    regexp "Displaying $lsidType Link States \\(Area $areaId\\).*?\(Displaying\)" $cmdOut linkState

    if {$linkState == ""} {
        regexp "Displaying $lsidType Link States \\(Area $areaId\\).*" $cmdOut linkState
    }
  
    foreach line [split $linkState "\n"] {
        if { [regexp -nocase "$lsid\[\t\ \]+$routerDR.*\(0x\[0-9a-f\]+\)\[\t\ \]+0x\[0-9a-f\]+" $line all sequence] == 1} {
            return "$sequence"
        }
    }
    return "ERROR"
}

proc EnableAsbr { host } {
   set err_count [GetGlobalErr]
   
   set prompt "CES\\(config-ospf\\)\#"

   EnterRouterOspfCLILevel $host
   Exec "asbr" $prompt $host
   ExitRouterOspfCLILevel $host

   return [CheckGlobalErr $err_count]

}

proc DisableAsbr { host } {
   set err_count [GetGlobalErr]
   
   set prompt "CES\\(config-ospf\\)\#"

   EnterRouterOspfCLILevel $host
   Exec "no asbr" $prompt $host
   ExitRouterOspfCLILevel $host

   return [CheckGlobalErr $err_count]

}

####################################################
# AccessList {host name action network {netmask ""} {type ""}}: Add a new rule to an AccessList and create the AccessList 
# if it does not exist
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      name:    name of the AccessList
#      action:  permit/deny
#      network: the network that is expected to be routed/any
#      netmask: network mask (none if network is any)
#      type:    range/exact
#
# OUT: SUCCESS/ERROR
####################################################
proc AccessList { host name action network {netmask ""} {type ""}} {
   set err_count [GetGlobalErr]
   SetCliLevel "CONFIG" $host
   Exec "access-list $name $action $network $netmask $type" "CONFIG" $host
   return [CheckGlobalErr $err_count]
   
}



####################################################
# DelAccessList {host name }: Delete an existing AccessList
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      name:    name of the AccessList
#
# OUT: SUCCESS/ERROR
####################################################
proc DelAccessList { host name } {
   set err_count [GetGlobalErr]
   SetCliLevel "CONFIG" $host 
   Exec "no access-list $name" "CONFIG" $host
   return [CheckGlobalErr $err_count]
}

####################################################
# ListAccessList {host name }: List the rules in an existing AccessList
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      name:    name of the AccessList
#
# OUT: SUCCESS/ERROR
####################################################
proc ListAccessList { host name } {
   set err_count [GetGlobalErr]
   SetCliLevel "CONFIG" $host 
   Exec "access-list $name list" "CONFIG" $host
   return [CheckGlobalErr $err_count]
}


####################################################
# AccessListRuleMove {host name rule1 rule2 }: Move rule1 in front of rule2
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      name:    name of the AccessList
#      rule1:   number of rule to be moved
#      rule2:   number of rule in front of will be moved
#
# OUT: SUCCESS/ERROR
####################################################
proc AccessListRuleMove { host name rule1 rule2 } {
   set err_count [GetGlobalErr]
   SetCliLevel "CONFIG" $host 
   Exec "access-list $name move rule $rule1 rule $rule2" "CONFIG" $host
   return [CheckGlobalErr $err_count]
}


####################################################
# RipDistributeList { host name type interfaceIp status } sets a distribute list policy for rip protocol
#
# IN:  host:        (management IP)/(terminal server Ip:port)
#      name:        name of the AccessList
#      type:        in/out (to be understanded as Accept/Anonce policy)
#      interfaceIp: rip interface on which the distribute list will be active;
#                   if instead of interface is a branch office then you can put:
#              "bo-conn <bo-conn name> <bo group>"  
#                   i.e. 
#                        RipDistributeList $host $name "in" "bo-conn Mybo /Base" enable;
#      status:      enable/disable
#
# OUT: SUCCESS/ERROR
####################################################
proc RipDistributeList { host name type interfaceIp status } {
   set err_count [GetGlobalErr]
   set prompt "CES\\(config-rip\\)\#"
   EnterRouterRipCLILevel $host
   Exec "distribute-list $name $type $interfaceIp $status" $prompt $host
   ExitRouterRipCLILevel $host
   return [CheckGlobalErr $err_count]
}


####################################################
# RipDelDistributeList { host name type interfaceIp } delete a distribute list policy for rip protocol
#
# IN:  host:        (management IP)/(terminal server Ip:port)
#      name:        name of the AccessList
#      type:        in/out (to be understanded as Accept/Anonce policy)
#      interfaceIp: rip interfecae on which the distribute list will be active
#
# OUT: SUCCESS/ERROR
####################################################
proc RipDelDistributeList { host name type interfaceIp } {
   set err_count [GetGlobalErr]
   set prompt "CES\\(config-rip\\)\#"
   EnterRouterRipCLILevel $host
   Exec "no distribute-list $name $type $interfaceIp" $prompt $host
   ExitRouterRipCLILevel $host
   return [CheckGlobalErr $err_count]
}


####################################################
# OspfDistributeList { host name type interfaceIp status } sets a distribute list policy for ospf protocol
#
# IN:  host:        (management IP)/(terminal server Ip:port)
#      name:        name of the AccessList
#      type:        in/out (to be understanded as Accept/Anonce policy)
#      interfaceIp: rip interfecae on which the distribute list will be active
#      status:      enable/disable
#
# OUT: SUCCESS/ERROR
####################################################
proc OspfDistributeList { host name type interfaceIp status } {
   set err_count [GetGlobalErr]
   set prompt "CES\\(config-ospf\\)\#"
   EnterRouterOspfCLILevel $host
   Exec "distribute-list $name $type $interfaceIp $status" $prompt $host
   ExitRouterOspfCLILevel $host
   return [CheckGlobalErr $err_count]
}

####################################################
# OspfDelDistributeList { host name type interfaceIp } delete a distribute list policy for ospf protocol
#
# IN:  host:        (management IP)/(terminal server Ip:port)
#      name:        name of the AccessList
#      type:        in/out (to be understanded as Accept/Anonce policy)
#      interfaceIp: rip interfecae on which the distribute list will be active
#
# OUT: SUCCESS/ERROR
####################################################
proc OspfDelDistributeList { host name type interfaceIp } {
   set err_count [GetGlobalErr]
   set prompt "CES\\(config-ospf\\)\#"
   EnterRouterOspfCLILevel $host
   Exec "no distribute-list $name $type $interfaceIp" $prompt $host
   ExitRouterOspfCLILevel $host
   return [CheckGlobalErr $err_count]
}

############################################
# SetCarState: enable/disable CAR
# 
# IN:  state: <enable/disable>
#      host:  (management IP) / (terminal server Ip:port)
# 
# OUT: SUCCESS/ERROR
#
############################################
proc SetCarState { host state } {
   set err_count [GetGlobalErr]
   SetCliLevel "CONFIG" $host
   switch $state {
      "enable" {
         Exec "router car enable" "CONFIG" $host
      }
      "disable" {
         Exec "no router car enable" "CONFIG" $host
      }
      default {
         return [ErrCheck "ERROR: Invalid state" SetCarState]
      }
   }
   SetCliLevel "PRIVILEGE" $host
   return [CheckGlobalErr $err_count]   
}

############################################
# EnterCarConfigLevel: enters CAR configuration level
# 
# IN:  host:  (management IP) / (terminal server Ip:port)
# 
# OUT: SUCCESS/ERROR
#
############################################
proc EnterCarConfigLevel { host } {
   set err_count [GetGlobalErr]
   SetCliLevel "CONFIG" $host
   set prompt "CES\\(config-car\\)\#"
   Exec "router car" $prompt $host
   return [CheckGlobalErr $err_count]  
}

############################################
# SetCarAggregation: configures aggregation for CAR
# 
# IN:  type: <dynamic/host/static>
#      host: (management IP) / (terminal server Ip:port)
# 
# OUT: SUCCESS/ERROR
#
############################################
proc SetCarAggregation { host type } {
   set err_count [GetGlobalErr]
   set prompt "CES\\(config-car\\)\#"
   EnterCarConfigLevel $host
   Exec "aggregation $type" $prompt $host
   SetCliLevel "PRIVILEGE" $host
   return [CheckGlobalErr $err_count]  
}

#########
# VRRP
#########

####################################################
# EnableVrrp {host} enable VRRP
#
# IN:  host:        (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
####################################################
proc EnableVrrp {host} {
   global cmdOut
   set err_count [GetGlobalErr]
   
   SetCliLevel "CONFIG" $host
   Exec "router vrrp enable" "CONFIG" $host

#    if {[regexp {This feature is not enabled} $cmdOut]} {
#       ErrCheck [list "ERROR: This feature is not enabled"]
#    }
   return [CheckGlobalErr $err_count]
}

####################################################
# DisableVrrp:  disable VRRP
#
# IN:  host:        (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
####################################################
proc DisableVrrp {host} {
    set err_count [GetGlobalErr]

    SetCliLevel "CONFIG" $host
    Exec "no router vrrp enable" "CONFIG" $host

    return [CheckGlobalErr $err_count]
}

####################################################
# EnterRouterVrrpCLILevel:  enter VRRP Configuration
#
# IN:  host:        (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
####################################################
proc EnterRouterVrrpCLILevel {host} {
    set err_count [GetGlobalErr]
    set prompt "CES\\(config-vrrp\\)\#"

    SetCliLevel "CONFIG" $host
    Exec "router vrrp" $prompt $host
    return [CheckGlobalErr $err_count]
}

####################################################
#  ConfigVrrpAddress: Configure global VRRP
#
# IN:  host:           (management IP)/(terminal server Ip:port)
#      vrrpIP:         "IP address"
#      vrrpID:         "vrrp id"
#      authentication: "none"/authentication string
#
# OUT: SUCCESS/ERROR
####################################################
proc ConfigVrrpAddress {host vrrpIP vrrpID {authentication none}} {
    global cmdOut
    set err_count [GetGlobalErr]

    set prompt "CES\\(config-vrrp\\)\#"

    EnterRouterVrrpCLILevel $host

    if {$authentication != "none"} {
        Exec "activate $vrrpIP vrid $vrrpID authentication simple $authentication" $prompt $host
    } else {
        Exec "activate $vrrpIP vrid $vrrpID authentication none" $prompt $host
    }
    SetCliLevel "CONFIG" $host

    return [CheckGlobalErr $err_count]
}

####################################################
#  DeleteVrrpAddress: Delete VRRP address
#
# IN:  host:           (management IP)/(terminal server Ip:port)
#      vrrpIP:         "IP address"
#      vrrpID:         "vrrp id"
#      authentication: "none"/authentication string
#
# OUT: SUCCESS/ERROR
####################################################
proc DeleteVrrpAddress {host vrrpIP} {
    global cmdOut
    set err_count [GetGlobalErr]

    set prompt "CES\\(config-vrrp\\)\#"

    EnterRouterVrrpCLILevel $host
    Exec "no activate $vrrpIP" $prompt $host
    SetCliLevel "CONFIG" $host

    return [CheckGlobalErr $err_count]
}

####################################################
# AddInterfaceToVrrp: Add private interface to VRRP
#
# IN:  host:           (management IP)/(terminal server Ip:port)
#      vrrpIP:         "IP address"
#
# OUT: SUCCESS/ERROR
####################################################
proc AddInterfaceToVrrp {host VrrpIP} {
   global cmdOut
   set err_count [GetGlobalErr]
   set prompt "CES\\(config-vrrp\\)\#"
   EnterRouterVrrpCLILevel $host
   set cmdOut ""
   Exec "network $VrrpIP" $prompt $host
   if {[regexp {VRRP is not supported on Multinet address} $cmdOut]} {
      ErrCheck [list "ERROR: VRRP is not supported on Multinet address"]
   }
   SetCliLevel "CONFIG" $host
   return [CheckGlobalErr $err_count]
}

####################################################
# DelInterfaceFromVrrp: Delete private interface from VRRP
#
# IN:  host:           (management IP)/(terminal server Ip:port)
#      vrrpIP:         "IP address"
#
# OUT: SUCCESS/ERROR
####################################################
proc DelInterfaceFromVrrp {host VrrpIP} {
    global cmdOut
    set err_count [GetGlobalErr]

    set prompt "CES\\(config-vrrp\\)\#"

    EnterRouterVrrpCLILevel $host
    Exec "no network $VrrpIP" $prompt $host    
    SetCliLevel "CONFIG" $host

    return [CheckGlobalErr $err_count]
}

##########################################################
# AssignIfGroupVrrp: Assigns interface group to critical VRRP and
#                    enables it
#
# IN:  host:          (management IP) / (terminal server Ip:port)
#      ipMasterVrrp: VRRP master IP address 
#      ifGrNo:       <1-3>  Critical Interface group number
#      ifGroupName:  name of the interface group
#      
# OUT: SUCCESS or ERROR
##########################################################
proc AssignIfGroupVrrp {host ipMasterVrrp ifGrNo ifGroupName} {
    global cmdOut

    set err_count [GetGlobalErr]

    EnterRouterVrrpCLILevel $host
    set prompt "CES\\(config-vrrp\\)\#"
    
    Exec "critical-interface-group $ipMasterVrrp $ifGrNo $ifGroupName enabled" $prompt $host

    if {[regexp {(Group does not exists)|(VRRP not enabled as master)} all $cmdOut]  == 1} {
        return [ErrCheck $all AssignIfGroupVrrp] 
    }
    
    SetCliLevel "CONFIG" $host
    return [CheckGlobalErr $err_count]
}

##########################################################
# DisableIfGroupVrrp: Disable interface group to critical VRRP
#
# IN:  host:          (management IP) / (terminal server Ip:port)
#      ipMasterVrrp: VRRP master IP address 
#      ifGrNo:       <1-3>  Critical Interface group number
#      ifGroupName:  name of the interface group
#      
# OUT: SUCCESS or ERROR
##########################################################
proc DisableIfGroupVrrp {host ipMasterVrrp ifGrNo ifGroupName} {
    global cmdOut

    set err_count [GetGlobalErr]

    EnterRouterVrrpCLILevel $host
    set prompt "CES\\(config-vrrp\\)\#"
    
    Exec "critical-interface-group $ipMasterVrrp $ifGrNo $ifGroupName disabled" $prompt $host

    if {[regexp {(Group does not exists)|(VRRP not enabled as master)} all $cmdOut]  == 1} {
        return [ErrCheck $all DisableIfGroupVrrp] 
    }
    
    SetCliLevel "CONFIG" $host
    return [CheckGlobalErr $err_count]
}

##########################################################
# DeleteIfGroupVrrp: Deletes interface group to critical VRRP
#
# IN:  host:          (management IP) / (terminal server Ip:port)
#      ipMasterVrrp: VRRP master IP address 
#      ifGrNo:       <1-3>  Critical Interface group number
#      ifGroupName:  name of the interface group
#      
# OUT: SUCCESS or ERROR
##########################################################
proc DeleteIfGroupVrrp {host ipMasterVrrp ifGrNo} {
    global cmdOut

    set err_count [GetGlobalErr]

    EnterRouterVrrpCLILevel $host
    set prompt "CES\\(config-vrrp\\)\#"
    
    Exec "no critical-interface-group $ipMasterVrrp $ifGrNo" $prompt $host

    if {[regexp {Invalid IP address} all $cmdOut]  == 1} {
        return [ErrCheck $all DeleteIfGroupVrrp] 
    }
    
    SetCliLevel "CONFIG" $host
    return [CheckGlobalErr $err_count]
}
