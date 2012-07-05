######################################################
# Library procedures for SNMB settings - CLI:  CES(config)#snmp-server ...
# SetSNMPTrapServerState { host traphost comunity state }
# SetSNMPTraps { host state group trap mode {interval "00:03:00"} }
#######################################################

####################################################
# SetSNMPTrapServerState: Enable/Disable SNMP trap server
#
# IN:  host:      (management IP)/(terminal server Ip:port)
#      trap-host: ip address or dns of trap listener
#      comunity:  public
#      state:     enable/disable
#
# OUT: SUCCESS/ERROR
####################################################
proc SetSNMPTrapServerState { host traphost comunity state } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   Exec "snmp-server host $traphost $comunity $state" "CONFIG" $host
   SetCliLevel "PRIVILEGE" $host
   
   return [CheckGlobalErr $err_count]

}

####################################################
# SetSNMPTraps: Enable/Disable SNMP trap server
#
# IN:  host:  (management IP)/(terminal server Ip:port)
#      state:    enable/disable
#      group:    trap groups
#      trap:     specific trap
#      mode:     interval/send-one/none
#      interval: hh:mm:ss     
#
# OUT: SUCCESS/ERROR
####################################################
proc SetSNMPTraps { host state group trap {mode "interval"} {int "00:03:00"} } {
   set err_count [GetGlobalErr]
   SetCliLevel "CONFIG" $host
   switch $state {
      "enable" {
         switch $mode {
            "none" {
               Exec "snmp-server enable traps $group $trap" "CONFIG" $host
            }
            "send-one" {
               Exec "snmp-server enable traps $group $trap send-one" "CONFIG" $host
            }
            "interval" {
               Exec "snmp-server enable traps $group $trap interval $int" "CONFIG" $host
            }
         }
      }
      "disable" {
         Exec "no snmp-server enable traps $group $trap" "CONFIG" $host
      }
      default {
         logFile "ERROR: state: $state is not a valid option"
         incr err_count
      }
   }
   
   SetCliLevel "PRIVILEGE" $host
   
   return [CheckGlobalErr $err_count]
}
