#############################################################
# Branch Office Connection relating procedures
#
# #########
# #NETWORK:
# #########
# AddNetwork {netName ip mask host}
# DelNetwork {netName host}
# ShowNetworks {host}
# ShowNetwork {netName host}
#
# ########
# #bo-conn
# ########
# AddBoConn {boName group host {control_tunnel "no_control_tunnel"} {conn_type ""}}
# DelBoConn {boName group host}
# ShowAllBoConn { host }
# ShowBoConn {boName group host}
#
# EnterBoConnLevel {boName group host}
# ExitBoConnLevel { host } -> OBSOLATED. USE SetCliLevel instead. 
# SetBoConnState {boName group state host}
# BoForcedLogOff {host {boName all} {group ""} }
# VerifyBoIsUp {connectionName host}
# GetBoType {connectionName host}
# AddBoConnRemoteNetwork { host boName boGroup network mask status cost }
# EditBoConnRemoteNetwork { host boName boGroup network mask status cost }
#
# #########################
# # MAIN BO SETUP PROCEDURES
# #########################
# ConfigIpSecBO {host boName group authentication_parameters
#                connection_parameters routing_parameters {state enable}}
# ConfigPPTPBO {host boName group authentication_parameters 
#               connection_parameters routing_parameters {state enable}}
# ConfigL2TPBO {host boName group authentication_parameters 
#               connection_parameters routing_parameters {state enable}}
# SetIPSecOverL2TP {host boName group ipsec_data_protection_type 
#                   ipsec_authentication_parameters}
# ConfigControlIpSecBO {host boName group authentication_parameters 
#                       connection_parameters routing_parameters {state enable}}
#
# #################################################
# # procedures used in MAIN BO SETUP PROCEDURES
# #  - should not be used in test scripts - 
# #################################################
# SetP2PBO  {host localEndPoint remoteEndPoint}
# SetInitiatorBO {host remoteEndPoint {localGw ""}}
# SetResponderBO {host}
# SetStaticBO {host localNet remoteIp remoteMask remoteState remoteCost}
# SetDynamicRipBO {host {cost 1}}
# SetDynamicOspfBO {host areaID {cost 100}}
#
#
# ######################################################
# # PROCEDURES FOR SETTING UP DIFFERENT PARAMETERS OF BO
# ######################################################
# SetBOCompression {host boName group boType {status enable}}
# SetBOEncryption {host boName group boType autenticationType}
# SetBOStatelessMode {host boName group boType {status enable}}
# SetIPSecAuthentication {host boName group authType authPass {initiator_id none}}
# SetBOMtu {host boName group mtu}
# SetBOMtuState {host boName group mtu_state}
# SetBODefaultMtu {host boName group}
# SetBOFilter {host boName group filter}
#
# EnableBoConnNatSet {natSet boName group host}
# DisableBoConnNat { boName group host }
#
# ########
# #bo-ospf
# ########
# SetBoConnOspfAreaId { boName group areaId host }
#
# ????????????? Obsolated. Not anymore in this file ?????????????
# ?? if needed could be retreived from previous versions of this file.
# ????????????????????????????????????????????????????????????????????
# # EnterBoConnRoutingStaticLevel { host }
# # SetBoConnRoutingStaticLocalNet { localNet host }
# # SetBoConnRoutingStaticRemoteNet { remoteNet mask state cost host }
# #
# # SetBoConnRipCost {cost host}
# # EnableBoConnRip {host}
# # DisableBoConnRip {host} 
# 
# ######
# #bo-ospf
# ######
#
#############################################################


#############
# NETWORK
#############

#############################################################
# AddNetwork: Adds a network object.
#
# IN:  netName: 
#      ip:      
#      mask:    
#      host:    (management IP)/(terminal server Ip:port)
# 
# OUT: SUCCESS/ERROR
#############################################################
proc AddNetwork {netName ip mask host} {
   SetCliLevel "CONFIG" $host
   Exec "network add $netName ip $ip mask $mask" "CONFIG" $host
}


#############################################################
# DelNetwork: Deletes a network object. 
#
# IN:  netName:
#      host:    (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc DelNetwork {netName host} {
   SetCliLevel "CONFIG" $host
   Exec "no network $netName" "CONFIG" $host    
}


#############################################################
# ShowNetworks: Shows the existing network objects.
#
# IN:  host: (management IP)/(terminal server Ip:port)
# 
# OUT: SUCCESS/ERROR
#############################################################
proc ShowNetworks {host} {
   SetCliLevel "CONFIG" $host
   Exec "show networks" "CONFIG" $host  
}


#############################################################
# ShowNetwork: Shows the data relating to a existing network
#              object.
#
# IN:  netName
#      host:   (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc ShowNetwork {netName host} {
   SetCliLevel "CONFIG" $host
   Exec "show networks $netName" "CONFIG" $host      
}


###########
# bo-conn
###########

#############################################################
# AddBoConn: Adds a BO Conn
#
# IN:  boName:         branch office name
#      group:          group name
#      host:           (management IP)/(terminal server Ip:port)
#      control_tunnel: control_tunnel/no_control_tunnel
#      conn_type:      type of BO connection. default "".
#
# OUT: SUCCESS/ERROR
#############################################################
proc AddBoConn {boName group host {control_tunnel "no_control_tunnel"} {conn_type ""}} {
   global cmdOut
   set cmdOut ""

   SetCliLevel "CONFIG" $host

   if {$conn_type == ""} {
      if {$control_tunnel =="control_tunnel"} {
         set okadd [Exec "bo-conn add $boName $group control-tunnel" "CONFIG" $host]
      } else {
         set okadd [Exec "bo-conn add $boName $group" "CONFIG" $host]
      }
   } else {
      if {$control_tunnel =="control_tunnel"} {
         set okadd [Exec "bo-conn add $boName $group control-tunnel conn-type $conn_type" "CONFIG" $host]
      } else {
         set okadd [Exec "bo-conn add $boName $group conn-type $conn_type" "CONFIG" $host]
      }
   }

    if { $okadd != "SUCCESS"} {
        return "ERROR"
    }

    if {[regexp -nocase "Group $group has incorrect format. Format is '/Base/<groupname>'" $cmdOut msg] == 1} {
        return [ErrCheck [list "ERROR: \n---$msg---"] "AddBoConn"]
    }

   return $okadd

}


#############################################################
# DelBoConn: Deletes a BO Conn
#
# IN:  boName: branch office name
#      group:  group name
#      host:   (management IP)/(terminal server Ip:port)
# 
# OUT: SUCCESS/ERROR
#############################################################
proc DelBoConn {boName group host} {
   SetCliLevel "CONFIG" $host
   return [Exec "no bo-conn $boName $group" "CONFIG" $host]
}


#############################################################
# ShowAllBoConn: Displays all the BO Connections configured
#                on DUT
#
# IN:  host
# 
# OUT: SUCCESS/ERROR
#############################################################
proc ShowAllBoConn { host } {
   SetCliLevel "CONFIG" $host
   return [Exec "show bo-conn" "CONFIG" $host]
}


#############################################################
# ShowBoConn: Displays the data relating to a BO Conn.
#
# IN:  boName:
#      group:
#      host:
#
# OUT: SUCCESS/ERROR
#############################################################
proc ShowBoConn {boName group host} {
   SetCliLevel "CONFIG" $host
   return [Exec "show bo-conn $boName $group" "CONFIG" $host]
}


#############################################################
# EnterBoConnLevel: enters to BO Conn setup CLI level.
#
# IN:  boName
#      group
#      host:  (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc EnterBoConnLevel {boName group host} {
   global cmdOut
   set cmdOut ""
   set rcode ""

   set prompt "CES\\(config/bo_conn\\)\#"
   SetCliLevel "CONFIG" $host
   if { [Exec "bo-conn $boName $group" $prompt $host] != "SUCCESS" } {
      lappend rcode "ERROR: \n---Branch Office Connection $group/$boName can not be set; verify if $group/$boName exist!---"
      return [ErrCheck $rcode "EnterBoConnLevel"]
   } 
	return "SUCCESS"
}


#############################################################
# OBSOLATED: use SetCliLevel instead !!!
# ExitBoConnLevel: gets out from BO conn setup CLI level.
# 
# IN:  host:  (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc ExitBoConnLevel { host } {
   return [Exec "exit" "CONFIG" $host]
}


#############################################################
# SetBoConnState: enable/disable BO Connection
#
# IN:  host:   (management IP)/(terminal server Ip:port)
#      boName: BO connection name
#      group:  BO group name
#      state:  <enable/disable>
#
# OUT: SUCESS/ERROR
#############################################################
proc SetBoConnState {boName group state host} {
   set err_count [GetGlobalErr]
   
   EnterBoConnLevel $boName $group $host
   set prompt "CES\\(config/bo_conn\\)\#"

   Exec "state $state" $prompt $host
   SetCliLevel "CONFIG" $host

   return [CheckGlobalErr $err_count]
}


#############################################################
# BoForcedLogOff:
#
# IN:  host:   (management IP)/(terminal server Ip:port)
#      boName: BO connection name. Default: 'all'
#      group:  BO group name. Default: ""
#
# OUT: SUCESS/ERROR
#############################################################
proc BoForcedLogOff {host {boName all} {group ""} } {
   
   set err_count [GetGlobalErr]

   global cmdOut
   set cmdOut ""

   SetCliLevel "PRIVILEGE" $host
   if { $boName == "all" } {
      Exec "forced-logoff bo-conn $boName" "PRIVILEGE" $host
   } else {
      Exec "forced-logoff bo-conn $boName $group" "PRIVILEGE" $host
   }
   if {[regexp -nocase "Connection does not exist for BO $boName in group $group" $cmdOut msg] == 1} {
      puts "\n msg = $msg\n"
      ErrCheck "ERROR: $msg" BoForcedLogOff
   }

   return [CheckGlobalErr $err_count]
}


#############################################################
# VerifyBoIsUp
#
# IN:  connectionName: BO Conn name
#      host:           (management IP)/(terminal server Ip:port)
# 
# OUT: YES/NO
#############################################################
#old version
#proc VerifyBoIsUp {connectionName host} {
#   global cmdOut
#   set cmdOut ""
#   
#   SetCliLevel "PRIVILEGE" $host
#   Exec "show branch-office sessions detail" "PRIVILEGE" $host "FORCERETURN"
#   if {[regexp -nocase "Connection:\[\t \ \]+$connectionName" $cmdOut] == 1} {
#      return "YES"
#   } else {
#      return "NO"
#   }
#}

#asterix: new version 24-04-2008
proc VerifyBoIsUp {connectionName host} {
   global cmdOut
   set cmdOut ""
   set count 0
   set response 0
        SetCliLevel "PRIVILEGE" $host
        while {($response==0)&&($count<4)} {
                Exec "show clock" "PRIVILEGE" $host "FORCERETURN"
                Exec "show branch-office sessions detail" "PRIVILEGE" $host "FORCERETURN"
                if {[regexp -nocase "Connection:\[\t \ \]+$connectionName" $cmdOut] == 1} {
                        set response 1
                } else {
                        incr count
                        sleep 10
                }
       }
       if {$response==1} {
       return "YES"
       } else {
       return "NO"
       }
}

#############################################################
# GetBoType: 
#
# IN:  connectionName:
#      host:           
#
# OUT:  
#############################################################
#old version 27-05-2008
#proc GetBoType {connectionName host} {
#   
#   global cmdOut
#   set cmdOut ""
#   set all ""
#   set rez ""
#   set ok_parse 0
#
#   SetCliLevel "PRIVILEGE" $host
#   Exec "show branch-office sessions detail" "PRIVILEGE" $host "FORCERETURN"
#
#   set bo_exist 0
#   foreach line [split $cmdOut "\n"] {
#      if {$bo_exist == 1} {
#         regexp -nocase {Account Type:[\ \t]+([a-zA-Z2/]+)} $line all rez
#         break
#      }
#      if {[regexp -nocase "Connection:\[\ \t\]+$connectionName" $line] == 1} {
#         set bo_exist 1
#      }
#   }
#   if {$rez != ""} {
#      return $rez
#   } else {
#      return "ERROR"
#   }
#}
#Asterix: new version 27-05-2008
proc GetBoType {connectionName host} {

	global cmdOut
	set cmdOut ""
	set all ""
	set rez ""
	set ok_parse 0
	set bo_exist 0
	set count 0
	
	SetCliLevel "PRIVILEGE" $host
	while {($bo_exist==0)&&($count<4)} {		
		Exec "show branch-office sessions detail" "PRIVILEGE" $host "FORCERETURN"
		foreach line [split $cmdOut "\n"] {
			if {$bo_exist == 1} {
				regexp -nocase {Account Type:[\ \t]+([a-zA-Z2/]+)} $line all rez
				break
			}
			if {[regexp -nocase "Connection:\[\ \t\]+$connectionName" $line] == 1} {
				set bo_exist 1
			}
		}
		if {$bo_exist == 0} {
			incr count
			sleep 10
		}
	}
	if {$rez != ""} {
		return $rez
	} else {
		return "ERROR"
	}
}

#############################################################
# AddBoConnRemoteNetwork: Add another remote network for a previously configured BO
#           Auxiliar procedure - this procedure is written because when a BO is created with a main procedure,
#                                it accept only one remote network. 
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      boName:  name of the existent BO
#      boGroup: name of the coresponding group
#      network: the network to be added
#      mask:    netmask
#      status:  status of the new added network <enable/disable>
#      cost:    the cost <1-200>
#      
# OUT: SUCESS/ERROR
#############################################################
proc AddBoConnRemoteNetwork { host boName boGroup network mask status cost } {
   set err_count [GetGlobalErr]
   EnterBoConnLevel $boName $boGroup $host
   set prompt "CES\\(config/bo_conn/routing_static\\)\#"
   Exec "routing static" $prompt $host
   Exec "remote-network $network mask $mask stat $status cost $cost" $prompt $host 
   SetCliLevel "CONFIG" $host
   return [CheckGlobalErr $err_count] 
}

#############################################################
# EditBoConnRemoteNetwork: Edit a remote network for a previously configured BO
#           Auxiliar procedure.
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      boName:  name of the existent BO
#      boGroup: name of the coresponding group
#      network: the network to be added
#      mask:    netmask
#      status:  status of the new added network <enable/disable>
#      cost:    the cost <1-200>
#      
# OUT: SUCESS/ERROR
#############################################################
proc EditBoConnRemoteNetwork { host boName boGroup network mask status cost } {
   set err_count [GetGlobalErr]
   EnterBoConnLevel $boName $boGroup $host
   set prompt "CES\\(config/bo_conn/routing_static\\)\#"
   Exec "routing static" $prompt $host
   Exec "edit remote-network $network mask $mask stat $status cost $cost" $prompt $host 
   SetCliLevel "CONFIG" $host
   return [CheckGlobalErr $err_count] 
}

#############################################################
#############################################################
# 
# MAIN BO SETUP PROCEDURES
#
#############################################################
#############################################################

#############################################################
# ConfigIpSecBO: Adds and configures a IpSec BO Conn
#
# IN:  
#
# OUT: 
#############################################################
proc ConfigIpSecBO {host boName group authentication_parameters connection_parameters routing_parameters {state enable}} {
   
   AddBoConn $boName $group $host
   EnterBoConnLevel $boName $group $host
   
   set prompt "CES\\(config/bo_conn\\)\#"
   Exec "tunnel-type ipsec" $prompt $host "FORCERETURN" 

   switch [lindex $connection_parameters 0] {
      "p2p" {
         SetP2PBO $host [lindex $connection_parameters 1] [lindex $connection_parameters 2]	    
      }
      "initiator" {
         SetInitiatorBO $host [lindex $connection_parameters 1] [lindex $connection_parameters 2]
      }
      "responder" {
         SetResponderBO $host
      }
      default {
         return [ErrCheck "ERROR: Invalid conn-type. Accepted values: \"p2p\", \"initiator\" or \"responder\"" ConfigIpSecBO]
      }
   }

   switch [lindex $authentication_parameters 0] {
      "text" {
         if {[llength $authentication_parameters] == 2} {
            Exec "ipsec authentication text-pre-shared-key [lindex $authentication_parameters 1]" $prompt $host "FORCERETURN"
         } elseif {[llength $authentication_parameters] == 3} {
            Exec "ipsec authentication initiator-uid [lindex $authentication_parameters 2] text-pre-shared-key [lindex $authentication_parameters 1]" $prompt $host "FORCERETURN"
         }
      }
      "hex" {
         if {[llength $authentication_parameters] == 2} {
            Exec "ipsec authentication hex-pre-shared-key [lindex $authentication_parameters 1]" $prompt $host "FORCERETURN"
         } elseif {[llength $authentication_parameters] == 3} {
            Exec "ipsec authentication initiator-uid [lindex $authentication_parameters 2] hex-pre-shared-key [lindex $authentication_parameters 1]" $prompt $host "FORCERETURN"
         }        
      }
      "certificate" {
            Exec "ipsec  authentication certificates" $prompt $host "FORCERETURN"
            Exec "ipsec issuer-ca \"[lindex $authentication_parameters 1]\"" $prompt $host "FORCERETURN"
            Exec "ipsec server-ca \"[lindex $authentication_parameters 2]\"" $prompt $host "FORCERETURN"
            Exec "ipsec subject-dn \"[lindex $authentication_parameters 3]\"" $prompt $host "FORCERETURN"
      }
      default {
         return [ErrCheck "ERROR: Invalid ipsec authentication. Accepted values: \"text\" or \"hex\" or \"certificate\"" ConfigIpSecBO]
      }
   }

   switch [lindex $routing_parameters 0] {
      "static" {
         SetStaticBO $host [lindex $routing_parameters 1] [lindex $routing_parameters 2] [lindex $routing_parameters 3] [lindex $routing_parameters 4] [lindex $routing_parameters 5]
      }
      "rip" {
         if {[llength $routing_parameters] == 1} {
            SetDynamicRipBO $host
         } elseif {[llength $routing_parameters] == 2} {
            SetDynamicRipBO $host [lindex $routing_parameters 1]
         }
      }
      "ospf" {
         if {[llength $routing_parameters] == 2} {
            SetDynamicOspfBO $host [lindex $routing_parameters 1]
         }  elseif {[llength $routing_parameters] == 3} {
            SetDynamicOspfBO $host [lindex $routing_parameters 1] [index $routing_parameters 2]
         }
      }	
      default {
         return [ErrCheck "ERROR: Invalid routing type. Accepted values: \"static\", \"rip\" or \"ospf\"" ConfigIpSecBO]
      }
   }

   Exec "state $state" $prompt $host "FORCERETURN"
   SetCliLevel "CONFIG" $host
   #    ShowBoConn "$boName" "$group" $host
}


#############################################################
# ConfigPPTPBO: Adds and configures a PPTP BO Conn
#
# IN:  
#
# OUT: 
#############################################################
proc ConfigPPTPBO {host boName group authentication_parameters connection_parameters routing_parameters {state enable}} {

   AddBoConn $boName $group $host
   EnterBoConnLevel $boName $group $host
   
   set prompt "CES\\(config/bo_conn\\)\#"

   Exec "tunnel-type pptp" $prompt $host "FORCERETURN"   
   Exec "pptp authentication local-uid [lindex $authentication_parameters 0] peer-uid [lindex $authentication_parameters 1] peer-password [lindex $authentication_parameters 2]" $prompt $host "FORCERETURN"
   
   switch [lindex $connection_parameters 0] {
      "p2p" {
         SetP2PBO $host [lindex $connection_parameters 1] [lindex $connection_parameters 2]

      }
      "initiator" {
         SetInitiatorBO $host [lindex $connection_parameters 1] [lindex $connection_parameters 2]
      }
      "responder" {
         SetResponderBO $host
      }
      default {
         return [ErrCheck "ERROR: Invalid conn-type. Accepted values: \"p2p\", \"initiator\" or \"responder\"" ConfigIpSecBO]
      }
   }

   switch [lindex $routing_parameters 0] {
      "static" {
         SetStaticBO $host [lindex $routing_parameters 1] [lindex $routing_parameters 2] [lindex $routing_parameters 3] [lindex $routing_parameters 4] [lindex $routing_parameters 5]
      }
      "rip" { 
         if {[llength $routing_parameters] == 1} {
            SetDynamicRipBO $host
         } elseif {[llength $routing_parameters] == 2} {
            SetDynamicRipBO $host [lindex $routing_parameters 1]
         }
      }
      "ospf" {
         if {[llength $routing_parameters] == 2} {
            SetDynamicOspfBO $host [lindex $routing_parameters 1]
         }  elseif {[llength $routing_parameters] == 3} {
            SetDynamicOspfBO $host [lindex $routing_parameters 1] [index $routing_parameters 2]
         }
      }	
      default {
         return [ErrCheck "ERROR: Invalid routing type. Accepted values: \"static\", \"rip\" or \"ospf\"" ConfigIpSecBO]
      }
   }

   Exec "state $state" $prompt $host "FORCERETURN"
   SetCliLevel "CONFIG" $host
   #    ShowBoConn "$boName" "$group" $host
}


#############################################################
# ConfigL2TPBO: Adds and configures a L2TP BO Conn
#
# IN:  
#
# OUT: 
#############################################################
proc ConfigL2TPBO {host boName group authentication_parameters connection_parameters routing_parameters {state enable}} {

   AddBoConn $boName $group $host
   EnterBoConnLevel $boName $group $host
   
   set prompt "CES\\(config/bo_conn\\)\#"

   Exec "tunnel-type l2tp" $prompt $host "FORCERETURN"   
   Exec "l2tp authentication local-uid [lindex $authentication_parameters 0] peer-uid [lindex $authentication_parameters 1] peer-password [lindex $authentication_parameters 2]" $prompt $host "FORCERETURN"
   
   switch [lindex $connection_parameters 0] {
      "p2p" {
         SetP2PBO $host [lindex $connection_parameters 1] [lindex $connection_parameters 2]

      }
      "initiator" {
         SetInitiatorBO $host [lindex $connection_parameters 1] [lindex $connection_parameters 2]
      }
      "responder" {
         SetResponderBO $host
      }
      default {
         return [ErrCheck "ERROR: Invalid conn-type. Accepted values: \"p2p\", \"initiator\" or \"responder\"" ConfigIpSecBO]
      }
   }

   switch [lindex $routing_parameters 0] {
      "static" {
         SetStaticBO $host [lindex $routing_parameters 1] [lindex $routing_parameters 2] [lindex $routing_parameters 3] [lindex $routing_parameters 4] [lindex $routing_parameters 5]
      }
      "rip" { 
         if {[llength $routing_parameters] == 1} {
            SetDynamicRipBO $host
         } elseif {[llength $routing_parameters] == 2} {
            SetDynamicRipBO $host [lindex $routing_parameters 1]
         }
      }
      "ospf" {
         if {[llength $routing_parameters] == 2} {
            SetDynamicOspfBO $host [lindex $routing_parameters 1]
         }  elseif {[llength $routing_parameters] == 3} {
            SetDynamicOspfBO $host [lindex $routing_parameters 1] [index $routing_parameters 2]
         }
      }	
      default {
         return [ErrCheck "ERROR: Invalid routing type. Accepted values: \"static\", \"rip\" or \"ospf\"" ConfigIpSecBO]
      }
   }

   Exec "state $state" $prompt $host "FORCERETURN"
   SetCliLevel "CONFIG" $host
   #    ShowBoConn "$boName" "$group" $host
}


#############################################################
# SetIPSecOverL2TP: Configures IPSec over L2TP
#
# IN:  
#
# OUT: 
#############################################################
proc SetIPSecOverL2TP {host boName group ipsec_data_protection_type ipsec_authentication_parameters} {

   EnterBoConnLevel $boName $group $host
   
   set prompt "CES\\(config/bo_conn\\)\#"

   Exec "no l2tp compress" $prompt $host "FORCERETURN"  
   Exec "no l2tp stateless-mode" $prompt $host "FORCERETURN"   
   Exec "l2tp ipsec-data-protection $ipsec_data_protection_type" $prompt $host "FORCERETURN" 

   switch [lindex $ipsec_authentication_parameters 0] {
      "text" {
         if {[llength $ipsec_authentication_parameters] == 2} {
            Exec "ipsec authentication text-pre-shared-key [lindex $ipsec_authentication_parameters 1]" $prompt $host "FORCERETURN"
         } elseif {[llength $ipsec_authentication_parameters] == 3} {
            Exec "ipsec authentication initiator-uid [lindex $ipsec_authentication_parameters 2] text-pre-shared-key [lindex $ipsec_authentication_parameters 1]" $prompt $host "FORCERETURN"
         }
      }
      "hex" {
         if {[llength $ipsec_authentication_parameters] == 2} {
            Exec "ipsec authentication hex-pre-shared-key [lindex $ipsec_authentication_parameters 1]" $prompt $host "FORCERETURN"
         } elseif {[llength $ipsec_authentication_parameters] == 3} {
            Exec "ipsec authentication initiator-uid [lindex $ipsec_authentication_parameters 2] hex-pre-shared-key [lindex $ipsec_authentication_parameters 1]" $prompt $host "FORCERETURN"
         }
      }
      "certificate" {
         Exec "ipsec  authentication certificates" $prompt $host "FORCERETURN"
         Exec "ipsec issuer-ca \"[lindex $ipsec_authentication_parameters 1]\"" $prompt $host "FORCERETURN"
         Exec "ipsec server-ca \"[lindex $ipsec_authentication_parameters 2]\"" $prompt $host "FORCERETURN"
         Exec "ipsec subject-dn \"[lindex $ipsec_authentication_parameters 3]\"" $prompt $host "FORCERETURN"
      }
      default {
         return [ErrCheck "ERROR: Invalid ipsec authentication. Accepted values: \"text\" or \"hex\" or \"certificate\"" ConfigIpSecBO]
      }
   }

   SetCliLevel "CONFIG" $host
   #    ShowBoConn "$boName" "$group" $host
}


#############################################################
# ConfigL2TPBO: Adds and configures a L2TP BO Conn
#
# IN:  
#
# OUT: 
#############################################################
proc ConfigControlIpSecBO {host boName group authentication_parameters connection_parameters routing_parameters {state enable}} {
   
   set prompt "CES\\(config/bo_conn\\)\#"
   
   switch [lindex $connection_parameters 0] {
      "p2p" {
         AddBoConn $boName $group $host "control_tunnel" "peer2peer"
         EnterBoConnLevel $boName $group $host
         Exec "local-endpoint [lindex $connection_parameters 1]" $prompt $host    
         Exec "remote-endpoint [lindex $connection_parameters 2]" $prompt $host 	    
      }
      "initiator" {
         AddBoConn $boName $group $host "control_tunnel" "initiator"
         EnterBoConnLevel $boName $group $host  
         Exec "remote-endpoint [lindex $connection_parameters 1]" $prompt $host
#         Exec "local-endpoint [lindex $connection_parameters 2]" $prompt $host  
      }
      "responder" {
         AddBoConn $boName $group $host "control_tunnel" "responder"
         EnterBoConnLevel $boName $group $host
      }
      default {
         return [ErrCheck "ERROR: Invalid conn-type. Accepted values: \"p2p\", \"initiator\" or \"responder\"" ConfigIpSecBO]
      }
   }

   switch [lindex $authentication_parameters 0] {
      "text" {
         if {[llength $authentication_parameters] == 2} {
            Exec "ipsec authentication text-pre-shared-key [lindex $authentication_parameters 1]" $prompt $host "FORCERETURN"
         } elseif {[llength $authentication_parameters] == 3} {
            Exec "ipsec authentication initiator-uid  [lindex $authentication_parameters 2] text-pre-shared-key [lindex $authentication_parameters 1]" $prompt $host "FORCERETURN"
         }
      }
      "hex" {
         if {[llength $authentication_parameters] == 2} {
            Exec "ipsec authentication hex-pre-shared-key [lindex $authentication_parameters 1]" $prompt $host "FORCERETURN"
         } elseif {[llength $authentication_parameters] == 3} {
            Exec "ipsec authentication initiator-uid  [lindex $authentication_parameters 2] hex-pre-shared-key [lindex $authentication_parameters 1]" $prompt $host "FORCERETURN"
         }
      }
      "certificate" {
         Exec "ipsec  authentication certificates" $prompt $host "FORCERETURN"
         Exec "ipsec issuer-ca \"[lindex $authentication_parameters 1]\"" $prompt $host "FORCERETURN"
         Exec "ipsec server-ca \"[lindex $authentication_parameters 2]\"" $prompt $host "FORCERETURN"
         Exec "ipsec subject-dn \"[lindex $authentication_parameters 3]\"" $prompt $host "FORCERETURN"
      }
      default {
         return [ErrCheck "ERROR: Invalid ipsec authentication. Accepted values: \"text\" or \"hex\"" ConfigIpSecBO]
      }
   }
   
   set prompt "CES\\(config/bo_conn/routing_static\\)\#"
   Exec "routing static" $prompt $host
   Exec "local-network [lindex $routing_parameters 1]" $prompt $host    
   Exec "remote-network [lindex $routing_parameters 2] mask [lindex $routing_parameters 3] stat [lindex $routing_parameters 4] cost [lindex $routing_parameters 5]" $prompt $host 
   Exec "exit" "CES\\(config/bo_conn\\)\#" $host 
   
   set prompt "CES\\(config/bo_conn\\)\#"
   Exec "state $state" $prompt $host "FORCERETURN"
   SetCliLevel "CONFIG" $host
   #    ShowBoConn "$boName" "$group" $host
}

#############################################################
#
# PRIVATE procedures - don't use the bellow procedures in test 
#                      scripts they are used by public procedures
#
# These procedures are used in MAIN BO SETUP PROCEDURES 
#
#############################################################

#############################################################
# SetP2PBO: Sets a peer to peer connection type for a branch office
#           Private procedures - used for other procedures in this file                
#
# IN:  host:           (management IP)/(terminal server Ip:port)
#      localEndPoint:  IP address of the public interface of the local CES
#      remoteEndPoint: IP address of the public interface of the remote CES
#      
# OUT: SUCESS/ERROR
#############################################################
proc SetP2PBO  {host localEndPoint remoteEndPoint} {
   set err_count [GetGlobalErr]

   set prompt "CES\\(config/bo_conn\\)\#"
   Exec "conn-type peer2peer" $prompt $host 
   Exec "local-endpoint $localEndPoint" $prompt $host    
   Exec "remote-endpoint $remoteEndPoint" $prompt $host 

   return [CheckGlobalErr $err_count]
}

#############################################################
# SetInitiatorBO: Sets a initiator connection type for a branch office
#                 Private procedures - used for other procedures in this file                
#
# IN:  host:           (management IP)/(terminal server Ip:port)
#      remoteEndPoint: IP address or name of BO interface in remote CES
#      localGW:        <0-6>/<1-4>  slot number / port number 
#                      - can be omitted       
#      
# OUT: SUCESS/ERROR
#############################################################
proc SetInitiatorBO {host remoteEndPoint {localGw ""}} {
   set err_count [GetGlobalErr]

   set prompt "CES\\(config/bo_conn\\)\#"
   Exec "conn-type initiator" $prompt $host 
   Exec "remote-endpoint $remoteEndPoint" $prompt $host
   if {$localGw != ""} {
      Exec "local-gateway $localGw" $prompt $host    
   }

   return [CheckGlobalErr $err_count]
}

#############################################################
# SetResponderBO: sets a responder connection type for a branch office
#                 Private procedures - used for other procedures in this file                
#
# IN:  host: (management IP)/(terminal server Ip:port)
#      
# OUT: SUCESS/ERROR
#############################################################
proc SetResponderBO {host} {
   set err_count [GetGlobalErr]

   set prompt "CES\\(config/bo_conn\\)\#"
   Exec "conn-type responder" $prompt $host

   return [CheckGlobalErr $err_count]
}

#############################################################
# SetStaticBO: Configures and enables static routing settings
#              Private procedures - used for other procedures in this file                
#
# IN:  host:        (management IP)/(terminal server Ip:port)
#      localNet:    name for a local network
#      remoteIp:    remote IP address
#      remoteMask:  remote network mask
#      remoteState: <enable/disable>
#      remoteCost:  <0-200> cost
#      
# OUT: SUCESS/ERROR
#############################################################
proc SetStaticBO {host localNet remoteIp remoteMask remoteState remoteCost} {
   set err_count [GetGlobalErr]
   set prompt "CES\\(config/bo_conn/routing_static\\)\#"

   Exec "routing type static" "CES\\(config/bo_conn\\)\#" $host
   Exec "routing static" $prompt $host
   Exec "local-network $localNet" $prompt $host    
   Exec "remote-network $remoteIp mask $remoteMask stat $remoteState cost $remoteCost" $prompt $host 
   Exec "exit" "CES\\(config/bo_conn\\)\#" $host 

   return [CheckGlobalErr $err_count]
}

#############################################################
# SetDynamicRipBO: Configures and enables RIP (dynamic) routing settings
#                  Private procedures - used for other procedures in this file                
#
# IN:  host: (management IP)/(terminal server Ip:port)
#      cost: <1-15>
#      
# OUT: SUCESS/ERROR
#############################################################
proc SetDynamicRipBO {host {cost 1}} {
   set err_count [GetGlobalErr]

   set prompt "CES\\(config/bo_conn\\)\#"
   Exec "routing type dynamic" $prompt $host
   Exec "routing rip cost $cost" $prompt $host 
   Exec "routing rip enable" $prompt $host
   Exec "routing ospf disable" $prompt $host 

   return [CheckGlobalErr $err_count]
}

#############################################################
# SetDynamicOspfBO: Configures and enables OSPF (dynamic) routing settings
#                  Private procedures - used for other procedures in this file                
#
# IN:  host:   (management IP)/(terminal server Ip:port)
#      areaID: A.B.C.D  Specified area-id, in IP address format
#      cost:   <1-65535>
#      
# OUT: SUCESS/ERROR
#############################################################
proc SetDynamicOspfBO {host areaID {cost 100}} {
   set err_count [GetGlobalErr]

   set prompt "CES\\(config/bo_conn\\)\#"    
   Exec "routing type dynamic" $prompt $host
   Exec "routing ospf area-id $areaID cost $cost" $prompt $host  
   Exec "routing ospf enable" $prompt $host 
   Exec "routing rip disable" $prompt $host

   return [CheckGlobalErr $err_count]
}










#############################################################
#############################################################
# 
# PROCEDURES FOR SETTING UP DIFFERENT PARAMETERS OF BO
#
#############################################################
#############################################################

#############################################################
# SetBOCompression: configure PPTP/L2TP BO compression.
#
# IN:  host:   (management IP)/(terminal server Ip:port)
#      boName: BO connection name
#      group:  BO group name
#      boType: <pptp/l2tp>
#      status: <enable/disable>
#      
# OUT: SUCESS/ERROR
#############################################################
proc SetBOCompression {host boName group boType {status enable}} { 
   set err_count [GetGlobalErr]

   EnterBoConnLevel $boName $group $host
   set prompt "CES\\(config/bo_conn\\)\#"

   if { $status == "enable" } {
      Exec "$boType compress" $prompt $host
   } elseif { $status == "disable" } {
      Exec "no $boType compress" $prompt $host  
   }
   SetCliLevel "CONFIG" $host

   return [CheckGlobalErr $err_count]
}

#############################################################
# SetBOEncryption: Enables authentication parameters
#                  only for PPTP/IPSEC tunnel type
#
# IN: host:              (management IP)/(terminal server Ip:port)
#     boName:            branch office name
#     group:             group name
#     boType:            <pptp/l2tp>
#     autenticationType: <none/rc4_40/rc4_128>
#
# OUT: SUCCESS/ERROR
#############################################################
proc SetBOEncryption {host boName group boType autenticationType} {
   set err_count [GetGlobalErr]

   EnterBoConnLevel $boName $group $host
   set prompt "CES\\(config/bo_conn\\)\#"

   Exec "$boType authentication $autenticationType" $prompt $host
   SetCliLevel "CONFIG" $host

   return [CheckGlobalErr $err_count]
}

#############################################################
# SetBOStatelessMode: configure PPTP/L2TP BO stateless mode.
#
# IN:  host:   (management IP)/(terminal server Ip:port)
#      boName: BO connection name
#      group:  BO group name
#      boType: pptp/l2tp
#      status: enable/disable
#      
# OUT: SUCESS/ERROR
#############################################################
proc SetBOStatelessMode {host boName group boType {status enable}} {
   set err_count [GetGlobalErr]
 
   EnterBoConnLevel $boName $group $host
   set prompt "CES\\(config/bo_conn\\)\#"
   
   if { $status == "enable" } {
      Exec "$boType stateless-mode" $prompt $host
   } elseif { $status == "disable" } {
      Exec "no $boType stateless-mode" $prompt $host  
   }
   SetCliLevel "CONFIG" $host

   return [CheckGlobalErr $err_count]
}

#############################################################
# SetIPSecAuthentication: configure IPSEC BO authentication.
#
# IN:  host:         (management IP)/(terminal server Ip:port)
#      boName:       BO connection name
#      group:        BO group name
#      authType:     <text/hex>
#      authPass:     password
#      initiator_id: initiator UID (for ABOT)
#      
# OUT: SUCESS/ERROR
#############################################################
proc SetIPSecAuthentication {host boName group authType authPass {initiator_id none}} { 
   
   set err_count [GetGlobalErr]
   
   EnterBoConnLevel $boName $group $host
   set prompt "CES\\(config/bo_conn\\)\#"

   switch $authType {
      "text" {
         if {$initiator_id == "none"} {
            Exec "ipsec authentication text-pre-shared-key $authPass" $prompt $host
         } else {
            Exec "ipsec authentication initiator-uid $initiator_id text-pre-shared-key $authPass" $prompt $host
         }
      }
      "hex" {
         if {$initiator_id == "none"} {
            Exec "ipsec authentication hex-pre-shared-key $authPass" $prompt $host
         } else {
            Exec "ipsec authentication initiator-uid $initiator_id hex-pre-shared-key $authPass" $prompt $host
         }
      }
      default {
         return [ErrCheck "ERROR: Invalid ipsec authentication. Accepted values: \"text\" or \"hex\"" ConfigIpSecBO]
      }
   }

   SetCliLevel "CONFIG" $host

   return [CheckGlobalErr $err_count]
}

#############################################################
# SetBOMtu: configure branch office mtu.
#
# IN:  host:   management IP/terminal server Ip:port
#      boName: BO connection name
#      group:  BO group name
#      mtu:    <576-1788>  MTU size in bytes
#
# OUT: SUCESS/ERROR
#############################################################
proc SetBOMtu {host boName group mtu} {
   
   set err_count [GetGlobalErr]
   
   EnterBoConnLevel $boName $group $host
   set prompt "CES\\(config/bo_conn\\)\#"   

   Exec "mtu $mtu" $prompt $host

   SetCliLevel "CONFIG" $host

   return [CheckGlobalErr $err_count]
}

#############################################################
# SetBOMtuState: Enable/Disable tunnel MTU usage
#
# IN:  host:     (management IP)/(terminal server Ip:port)
#      boName:   BO connection name  
#      group:    BO group name
#      mtuState: <enable/disable>
#
# OUT: SUCESS/ERROR
#############################################################
proc SetBOMtuState {host boName group mtu_state} {
   
   set err_count [GetGlobalErr]
   
   EnterBoConnLevel $boName $group $host
   set prompt "CES\\(config/bo_conn\\)\#"   

   if {[regexp -nocase "en" $mtu_state] == 1} {
      Exec "mtu enable" $prompt $host
   } elseif {[regexp -nocase "dis" $mtu_state] == 1} {
      Exec "no mtu enable" $prompt $host
   } else {
      ErrCheck "ERROR: bad parameter mtu_state: $mtu_state"
   }

   SetCliLevel "CONFIG" $host

   return [CheckGlobalErr $err_count]

}

#############################################################
# SetBODefaultMtu: Returns to default MTU value.
#
# IN:  host:   management IP/terminal server Ip:port
#      boName: BO connection name
#      group:  BO group name
#
# OUT: SUCESS/ERROR
#############################################################
proc SetBODefaultMtu {host boName group} {
   set err_count [GetGlobalErr]
   
   EnterBoConnLevel $boName $group $host
   set prompt "CES\\(config/bo_conn\\)\#"   

   Exec "no mtu" $prompt $host

   SetCliLevel "CONFIG" $host

   return [CheckGlobalErr $err_count]
}


#############################################################
# SetBOFilter: Enables a filter for this connection.
#
# IN:  host:   management IP/terminal server Ip:port
#      boName: BO connection name
#      group:  BO group name
#      filter: Filter name to be used
#
# OUT: SUCESS/ERROR
#############################################################
proc SetBOFilter {host boName group filter} {
   set err_count [GetGlobalErr]
   
   EnterBoConnLevel $boName $group $host
   set prompt "CES\\(config/bo_conn\\)\#"   

   Exec "filter \"$filter\"" $prompt $host

   SetCliLevel "CONFIG" $host

   return [CheckGlobalErr $err_count]
}



########
# BO NAT
########

proc EnableBoConnNatSet {natSet boName group host} {

   set prompt "CES\\(config/bo_conn\\)\#"
   EnterBoConnLevel $boName $group $host

   set execRes [Exec "nat $natSet" $prompt $host]
   
   ExitBoConnLevel $host

   return $execRes
}

proc DisableBoConnNat { boName group host } {
   set prompt "CES\\(config/bo_conn\\)\#"
   EnterBoConnLevel $boName $group $host

   set execRes [Exec "no nat" $prompt $host]
   
   ExitBoConnLevel $host
   
   return $execRes
}

#############################################################
# SetBoConnOspfAreaId:
#
# IN:  host:   management IP/terminal server Ip:port
#      boName: BO connection name
#      group:  BO group name
#      areaId: OSPF area ID
#
# OUT: SUCESS/ERROR
#############################################################
proc SetBoConnOspfAreaId { boName group areaId host } {
   set err_count [GetGlobalErr]

   set prompt "CES\\(config/bo_conn\\)\#"
   EnterBoConnLevel $boName $group $host
   
   Exec "routing ospf area-id $areaId" $prompt $host

   SetCliLevel "CONFIG" $host
   return [CheckGlobalErr $err_count]
}
