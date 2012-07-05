#############################################################
# System forwarding
#
# SetSysFwdProxyArpBo { state host }
# SetSysFwdProxyArpIf { state host } 
# SetSysFwdGratuitousArp { state host }
# SetSysFwdProxyArpNAT { state host }
# SetGlobalSysFwdArp { stateProxyArpIf stateProxyArpBo stateGratuitousArp  host }
# ShowSysFwd { host }
# SetSysFwdEuToEu { host state }
# SetSysFwdEuToBo { host state }
# SetSysFwdBoToBo { host state }
# SetGlobalSysFwdTunnelToTunnel { host stateEuToEu stateEuToBo stateBoToBo }
#
##############################################################


##############################################################
# SetSysFwdProxyArpBo: enable/disable branch-office-tunnels proxy arp
#
# IN:  state: <enable/no_enable>
#      host:  (management IP)/(terminal server Ip:port)  
#
# OUT: SUCCCESS/ERROR
##############################################################
proc SetSysFwdProxyArpBo { state host } {

   set err_count [GetGlobalErr]

    SetCliLevel "CONFIG" $host

    switch $state {
        "enable" {
            Exec "system forwarding proxy-arp branch-office-tunnels enable" "CONFIG" $host
        }
        "no_enable" {
            Exec "no system forwarding proxy-arp branch-office-tunnels enable" "CONFIG" $host
        }
    }

   return [CheckGlobalErr $err_count]

}


#############################################################
# SetSysFwdProxyArpIf: Enables physical interfaces proxy-arp
#
# IN:  state: <enable/no_enable>
#      host:  (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc SetSysFwdProxyArpIf { state host } {

   set err_count [GetGlobalErr]

    SetCliLevel "CONFIG" $host

    switch $state {
        "enable" {
            Exec "system forwarding proxy-arp physical-interfaces enable" "CONFIG" $host
        }
        "no_enable" {
            Exec "no system forwarding proxy-arp physical-interfaces enable" "CONFIG" $host
        }
    }

   return [CheckGlobalErr $err_count]

}


#############################################################
# SetSysFwdProxyArpNAT: Enables NAT proxy-arp
#
# IN:  state: <enable/no_enable>
#      host:  (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc SetSysFwdProxyArpNAT { state host } {

   set err_count [GetGlobalErr]

    SetCliLevel "CONFIG" $host

    switch $state {
        "enable" {
            Exec "system forwarding proxy-arp nat enable" "CONFIG" $host
        }
        "no_enable" {
            Exec "no system forwarding proxy-arp nat enable" "CONFIG" $host
        }
    }

   return [CheckGlobalErr $err_count]
}



#############################################################
# SetSysFwdGratuitousArp: enable/disable gratuitous arp
#
# IN:  state: <enable/no_enable>
#      host:  management IP/terminal server Ip:port
#
# OUT: SUCCESS/ERROR
#############################################################
proc SetSysFwdGratuitousArp { state host } {

   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host

   switch $state {
      "enable" {
         Exec "system forwarding gratuitous-arp enable" "CONFIG" $host
      }
      "no_enable" {
         Exec "no system forwarding gratuitous-arp enable" "CONFIG" $host
      }
   }
   
   return [CheckGlobalErr $err_count]

}


#############################################################
# SetGlobalSysFwdArp: disable/enable CES global proxy arp 
#
# IN:  stateProxyArpIf:    <enable/no_enable>
#      stateProxyArpBo:    <enable/no_enable>
#      stateGratuitousArp: <enable/no_enable>
#      host:               (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc SetGlobalSysFwdArp { stateProxyArpIf stateProxyArpBo stateGratuitousArp host} {

   set err_count [GetGlobalErr]

   SetSysFwdProxyArpIf $stateProxyArpIf $host
   SetSysFwdProxyArpBo $stateProxyArpBo $host
   SetSysFwdGratuitousArp $stateGratuitousArp $host

   return [CheckGlobalErr $err_count]

}


#############################################################
# ShowSysFwd: Displays forwarding settings.
#
# IN:  host: (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc ShowSysFwd { host } {

    SetCliLevel "PRIVILEGE" $host
    
    Exec "show system forwarding" "PRIVILEGE" $host
    
}

#############################################################
# SetSysFwdEuToEu: disable/enable CES  Tunnel to Tunnel Traffic End User to End User
#
# IN:  state:    <enable/no_enable>     
#       host:     (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################

proc SetSysFwdEuToEu { host state } {
	set err_count [GetGlobalErr]

	SetCliLevel "CONFIG" $host

	switch $state {
		"enable" {
			Exec "system forwarding tunnel-to-tunnel-traffic EU-to-EU enable" "CONFIG" $host	    
		}	
		"no_enable" {
			Exec "no system forwarding tunnel-to-tunnel-traffic EU-to-EU enable" "CONFIG" $host	    
		}
	}

	return [CheckGlobalErr $err_count]

	}
	
#############################################################
# SetSysFwdEuToBo: disable/enable CES  Tunnel to Tunnel Traffic End User to Branch Office
#
# IN:  state:    <enable/no_enable>     
#       host:     (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################

proc SetSysFwdEuToBo { host state } {
	set err_count [GetGlobalErr]
	
	SetCliLevel "CONFIG" $host

	switch $state {
		"enable" {
			Exec "system forwarding tunnel-to-tunnel-traffic Eu-to-BO enable" "CONFIG" $host	    
		}
		"no_enable" {
			Exec "no system forwarding tunnel-to-tunnel-traffic Eu-to-BO enable" "CONFIG" $host	    
		}
	}
	

	return [CheckGlobalErr $err_count]

	}	
	
#############################################################
# SetSysFwdBoToBo: disable/enable CES  Tunnel to Tunnel Traffic Branch Office to Branch Office
#
# IN:  state:    <enable/no_enable>     
#       host:     (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################

proc SetSysFwdBoToBo { host state } {
	set err_count [GetGlobalErr]

	SetCliLevel "CONFIG" $host

	switch $state {
		"enable" {
			Exec "system forwarding tunnel-to-tunnel-traffic BO-to-BO enable" "CONFIG" $host	    
		}
		"no_enable" {
			Exec "no system forwarding tunnel-to-tunnel-traffic BO-to-BO enable" "CONFIG" $host	    
		}
	}

	return [CheckGlobalErr $err_count]

	}	

#############################################################
# SetGlobalSysFwdTunnelToTunnel: disable/enable CES  Global Tunnel to Tunnel Traffic
#
# IN:  stateEuToEu:    <enable/no_enable>
#	   stateEuToBo:    <enable/no_enable>
#	   stateBoToBo:    <enable/no_enable>
#       host:     (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################

proc SetGlobalSysFwdTunnelToTunnel { host stateEuToEu stateEuToBo stateBoToBo } {
	set err_count [GetGlobalErr]

	SetSysFwdEuToEu $host $stateEuToEu
	SetSysFwdEuToBo $host $stateEuToBo
	SetSysFwdBoToBo $host $stateBoToBo

	return [CheckGlobalErr $err_count]

	}