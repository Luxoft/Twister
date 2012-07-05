###################################
# Filters library
# 
# This file contains the Acelib procedures relating to Filters CLI commands
#
# 
# Procedures:
#
# EnterFilterLevel { filterType filterName host }
# ExitFilterLevel { host }
#
# ####################
# #Filter Rules
# ####################
#
# AddFilterRuleName { filterType ruleName host }
# DelFilterRuleName { filterType ruleName host }
# EnterFilterRuleLevel { filterType ruleName host }
# ExitFilterRuleLevel { host }
# EnaLocalService { host filterType filterName service }
# DisLocalService { host filterType filterName service }
# ConfigTunnelFilterClient { host server status }
# ConfigTunnelFilterServer { host service status }
###################################

#############################################################
# EnterFilterLevel: Enter into filter configuration CLI level
#
# IN:  filterType: tunnel/interface
#      filterName: filter name
#      host:       (management IP)/(terminal server Ip:port)
#    
# OUT: SUCCESS/ERROR
#############################################################
proc EnterFilterLevel { filterType filterName host } {
   
   global cmdOut
   set prompt "CES\\(config-filter\\)\#"
   set err_count [GetGlobalErr]
   
   SetCliLevel "CONFIG" $host   
   Exec "filter $filterType $filterName" $prompt $host

   if {[regexp {not exist} $cmdOut] == 1} {
      ErrCheck {"ERROR: $cmdOut"}
   }
   
   return [CheckGlobalErr $err_count]
}


#############################################################
# OBSOLATED. Use SetCliLevel instead.
# ExitFilterLevel: Exit from filter configuration CLI level.
#
# IN:  host: (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc ExitFilterLevel { host } {
    Exec "exit" "CONFIG" $host    
}

# ####################
# #Filter Rules
# ####################

proc AddFilterRuleName { filterType ruleName host } {
    
    SetCliLevel "CONFIG" $host

    Exec "filter $filterType rule add $ruleName" "CONFIG" $host
}

proc DelFilterRuleName { filterType ruleName host } {
    
    SetCliLevel "CONFIG" $host

    Exec "no filter $filterType rule $ruleName" "CONFIG" $host
}

proc EnterFilterRuleLevel { filterType ruleName host } {
    set prompt "CES\\(config/rule\\)\#"
    
    SetCliLevel "CONFIG" $host

    Exec "filter $filterType rule $ruleName" $prompt $host
}

proc ExitFilterRuleLevel { host } {
    Exec "exit" "CONFIG" $host
}


###################################
# OBSOLATED. Use ConfigTunnelFilterServer instead.
#
# EnaLocalService
#
# Variables:
#    filterType: tunnel/interface
#    filterName: name of filetr
#    host:       the IP address (or IP:port) of the DUT
#    service:    which service should be enabled
###################################

proc EnaLocalService { host filterType filterName service } {
   set err_count [GetGlobalErr]
   
   EnterFilterLevel $filterType $filterName $host
   
   set prompt "CES\\(config-filter\\)\#"
   
   Exec "server $service" $prompt $host
   
   ExitFilterLevel $host
   
   return [CheckGlobalErr $err_count]
      
}


###################################
# OBSOLATED. Use ConfigTunnelFilterServer instead.
#
# DisLocalService
#
# Variables:
#    filterType: tunnel/interface
#    filterName: name of filetr
#    host:       the IP address (or IP:port) of the DUT
#    service:    which service should be disabled
###################################
proc DisLocalService { host filterType filterName service } {
   set err_count [GetGlobalErr]
   
   EnterFilterLevel $filterType $filterName $host
   
   set prompt "CES\\(config-filter\\)\#"
   
   Exec "no server $service" $prompt $host
   
   ExitFilterLevel $host
   
   return [CheckGlobalErr $err_count]
      
}


#############################################################
# ConfigTunnelFilterClient: Enable remote servers for filter.
#
# IN:  host:   (management IP)/(terminal server Ip:port)
#      server: all          all remote servers
#              cmp          
#              dns          
#              ftp          
#              ldap         
#              ntp          
#              radius       
#              tunnelguard
#      status: <enable/disable/no_enable>
#
# OUT: SUCCESS/ERROR
#############################################################
proc ConfigTunnelFilterClient { host filter_name server status } {
   set err_count [GetGlobalErr]
   set prompt "CES\\(config-filter\\)\#"

   EnterFilterLevel "tunnel" $filter_name $host
   if {$status == "enable"} {
      Exec "client $server" $prompt $host
   } elseif {$status == "disable" || $status == "no_enable"} {
      Exec "no client $server" $prompt $host
   }

   SetCliLevel "CONFIG" $host
   return [CheckGlobalErr $err_count]
}


#############################################################
# ConfigTunnelFilterServer: Enable local services for filter.
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      service: all             all local services.
#               dns             
#               ftp             
#               http            
#               https           
#               identification  
#               ping            
#               radius          
#               snmp            
#               ssh             
#               telnet          
#      status: <enable/disable/no_enable>
#
# OUT: SUCCESS/ERROR
#############################################################
proc ConfigTunnelFilterServer { host filter_name service status } {
   set err_count [GetGlobalErr]
   set prompt "CES\\(config-filter\\)\#"

   EnterFilterLevel "tunnel" $filter_name $host
   if {$status == "enable"} {
      Exec "server $service" $prompt $host
   } elseif {$status == "disable" || $status == "no_enable"} {
      Exec "no server $service" $prompt $host
   }
   
   SetCliLevel "CONFIG" $host
   return [CheckGlobalErr $err_count]
}
