######################################################
# Library procedures for Demand settings
# DemandGlobalState { host state }
# DemandAddIf { host if_Name }
# DemandDelIf { host if_Name }
# DemandIfState { host if_Name state }
# EnterDemandIfConfigLevel { host if_Name }
# DemandConfigInterface { host if_Name slot }
# DemandConfigTrigger { host if_Name trigger }
# DemandConfigPing { host if_Name dest_ip source parameter {retry 3} {wait 5} }
# DemandConfigIfGroup { host if_Name ifgroup_Name }
# DemandConfigTimeout { host if_Name timeout }
# DemandConfigWait { host if_Name wait }
# DemandConfigHours { host if_Name value }
# DemandConfigPriority { host if_Name level }
# DemandConfigRouteUnreachable { host if_Name value }
#######################################################

####################################################
# DemandGlobalState: Enable/Disable Demand service globally
#
# IN:  host:  (management IP)/(terminal server Ip:port)
#      state: enable/disable
#
# OUT: SUCCESS/ERROR
####################################################
proc DemandGlobalState { host state } {
   set err_count [GetGlobalErr]
   SetCliLevel "CONFIG" $host
   if { $state == "disable" } {
      Exec "no demand enable" "CONFIG" $host
   } else {
      Exec "demand enable" "CONFIG" $host
   }
   return [CheckGlobalErr $err_count]  
}

####################################################
# DemandAddIf: add a demand interface
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      if_Name: interface name
#
# OUT: SUCCESS/ERROR
####################################################
proc DemandAddIf { host if_Name } {
   set err_count [GetGlobalErr]
   SetCliLevel "CONFIG" $host
   Exec "demand add $if_Name" "CONFIG" $host
   return [CheckGlobalErr $err_count]
}

####################################################
# DemandDelIf: delete a demand interface
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      if_Name: interface name
#
# OUT: SUCCESS/ERROR
####################################################
proc DemandDelIf { host if_Name } {
   set err_count [GetGlobalErr]
   SetCliLevel "CONFIG" $host
   Exec "no demand $if_Name" "CONFIG" $host
   return [CheckGlobalErr $err_count]
}

####################################################
# DemandIfState: enable/disable a demand interface
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      if_Name: interface name
#      state:   <enable/disable>
#
# OUT: SUCCESS/ERROR
####################################################
proc DemandIfState { host if_Name state } {
   set err_count [GetGlobalErr]
   SetCliLevel "CONFIG" $host
   if { $state == "enable" } {
      Exec "demand $if_Name enable" "CONFIG" $host
   } else {
      Exec "demand $if_Name enable" "CONFIG" $host
   }
   return [CheckGlobalErr $err_count]
}

####################################################
# EnterDemandIfConfigLevel: Enter demand config mode
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      if_Name: interface name
#
# OUT: SUCCESS/ERROR
####################################################
proc EnterDemandIfConfigLevel { host if_Name } {
   set err_count [GetGlobalErr]
   SetCliLevel "CONFIG" $host
   set prompt "CES\\(config-demand\\)\#"
   Exec "demand $if_Name" $prompt $host
   return [CheckGlobalErr $err_count]
}

####################################################
# DemandConfigInterface: Specifies the physical interface
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      if_Name: interface name
#      slot:    <0-7>/<1-4>  (slot number) / (interface number)
#
# OUT: SUCCESS/ERROR
####################################################
proc DemandConfigInterface { host if_Name slot } {
   set err_count [GetGlobalErr]
   SetCliLevel "CONFIG" $host
   set prompt "CES\\(config-demand\\)\#"
   EnterDemandIfConfigLevel $host $if_Name
   Exec "interface $slot" $prompt $host
   SetCliLevel "CONFIG" $host
   return [CheckGlobalErr $err_count]
}

####################################################
# DemandConfigTrigger: Sets the trigger type
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      if_Name: interface name
#      trigger: <ping/hours/route-unreachable/interface-group/traffic>
#
# OUT: SUCCESS/ERROR
####################################################
proc DemandConfigTrigger { host if_Name trigger } {
   set err_count [GetGlobalErr]
   SetCliLevel "CONFIG" $host
   set prompt "CES\\(config-demand\\)\#"
   EnterDemandIfConfigLevel $host $if_Name
   Exec "trigger $trigger" $prompt $host
   SetCliLevel "CONFIG" $host
   return [CheckGlobalErr $err_count]
}

####################################################
# DemandConfigTrigger: Sets the ping parameters
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      if_Name:   interface name
#      dest_ip:   destination ip
#      source:    source type (ip/interface)
#      parameter: source id (ip address/slot)
#      retry:     number of retries
#      wait:      delay before raise the demand interface
#
# OUT: SUCCESS/ERROR
####################################################
proc DemandConfigPing { host if_Name dest_ip source parameter {retry 3} {wait 5} } {
   set err_count [GetGlobalErr]
   SetCliLevel "CONFIG" $host
   set prompt "CES\\(config-demand\\)\#"
   EnterDemandIfConfigLevel $host $if_Name
   Exec "ping $dest_ip source $source $parameter retry $retry wait $wait" $prompt $host
   SetCliLevel "CONFIG" $host
   return [CheckGlobalErr $err_count]
}

####################################################
# DemandConfigIfGroup: Sets the trigger type
#
# IN:  host:         (management IP)/(terminal server Ip:port)
#      if_Name:      interface name
#      ifgroup_Name: name of interface group
#
# OUT: SUCCESS/ERROR
####################################################
proc DemandConfigIfGroup { host if_Name ifgroup_Name } {
   set err_count [GetGlobalErr]
   SetCliLevel "CONFIG" $host
   set prompt "CES\\(config-demand\\)\#"
   EnterDemandIfConfigLevel $host $if_Name
   Exec "interface-group $ifgroup_Name" $prompt $host
   SetCliLevel "CONFIG" $host
   return [CheckGlobalErr $err_count]
}

####################################################
# DemandConfigTimeout: Sets the timeout for traffic trigger
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      if_Name: interface name
#      timeout: <1-86400>  Number of seconds to timeout
#
# OUT: SUCCESS/ERROR
####################################################
proc DemandConfigTimeout { host if_Name timeout } {
   set err_count [GetGlobalErr]
   SetCliLevel "CONFIG" $host
   set prompt "CES\\(config-demand\\)\#"
   EnterDemandIfConfigLevel $host $if_Name
   Exec "timeout $timeout" $prompt $host
   SetCliLevel "CONFIG" $host
   return [CheckGlobalErr $err_count]
}

####################################################
# DemandConfigWait: Sets the waiting time between re-dials
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      if_Name: interface name
#      wait:    <60-255>  seconds
#
# OUT: SUCCESS/ERROR
####################################################
proc DemandConfigWait { host if_Name wait } {
   set err_count [GetGlobalErr]
   SetCliLevel "CONFIG" $host
   set prompt "CES\\(config-demand\\)\#"
   EnterDemandIfConfigLevel $host $if_Name
   Exec "wait $wait" $prompt $host
   SetCliLevel "CONFIG" $host
   return [CheckGlobalErr $err_count]
}

####################################################
# DemandConfigHours: Specifies which operating hours are permitted
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      if_Name: interface name
#      value:   a word listed in the Hours table
#
# OUT: SUCCESS/ERROR
####################################################
proc DemandConfigHours { host if_Name value } {
   set err_count [GetGlobalErr]
   SetCliLevel "CONFIG" $host
   set prompt "CES\\(config-demand\\)\#"
   EnterDemandIfConfigLevel $host $if_Name
   Exec "hours $value" $prompt $host
   SetCliLevel "CONFIG" $host
   return [CheckGlobalErr $err_count]
}

####################################################
# DemandConfigPriority: Sets the priority level
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      if_Name: interface name
#      level:   <1-99>
#
# OUT: SUCCESS/ERROR
####################################################
proc DemandConfigPriority { host if_Name level } {
   set err_count [GetGlobalErr]
   SetCliLevel "CONFIG" $host
   set prompt "CES\\(config-demand\\)\#"
   EnterDemandIfConfigLevel $host $if_Name
   Exec "priority $level" $prompt $host
   SetCliLevel "CONFIG" $host
   return [CheckGlobalErr $err_count]
}

####################################################
# DemandConfigRedial: Sets the number of re-dials before the connection is declared unreachable
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      if_Name: interface name
#      value:   <1-255>
#
# OUT: SUCCESS/ERROR
####################################################
proc DemandConfigRedial { host if_Name value } {
   set err_count [GetGlobalErr]
   SetCliLevel "CONFIG" $host
   set prompt "CES\\(config-demand\\)\#"
   EnterDemandIfConfigLevel $host $if_Name
   Exec "redial $value" $prompt $host
   SetCliLevel "CONFIG" $host
   return [CheckGlobalErr $err_count]
}

####################################################
# DemandConfigRouteUnreachable: Defines the unreachable network (route)
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      if_Name: interface name
#      value:   name of route
#
# OUT: SUCCESS/ERROR
####################################################
proc DemandConfigRouteUnreachable { host if_Name value } {
   set err_count [GetGlobalErr]
   SetCliLevel "CONFIG" $host
   set prompt "CES\\(config-demand\\)\#"
   EnterDemandIfConfigLevel $host $if_Name
   Exec "route-unreachable $value" $prompt $host
   SetCliLevel "CONFIG" $host
   return [CheckGlobalErr $err_count]
}





