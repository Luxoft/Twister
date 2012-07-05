#########################################
# Firewall setup relating procedures
#
#
# Procedures:
# 
# FwLicenseInstall {licence host}. OBSOLATED. Use InstallLicense instead.
# EnaContivityStatefulFirewall { host }
# EnaContivityIfFilters { host }
# EnaContivityFwAndIfFilters { host }
# EnaTunelFilter { host }
# EnaTunnelMngFilter { host }
# DisFirewall { host }
# DisTunnelFilter { host }
# DisTunnelMngFilter { host }
# ShowFirewall { type host }
# AddPolicySecurity { policyName host }
# DelPolicySecurity { policyName host }
# ShowPolicySecurity { type host }
# AssignPolicySecurity { policyName host }
# EnterPolicyLevel { host }
# ExitPolicyLevel { host }. OBSOLATED: Use SetCliLevel instead
# AddPolicySecurityServiceIcmp {  host policyName serviceName code type }
# DelPolicySecurityService { policyName serviceName host }
# EditPolicySecurityServiceIcmp { host policyName serviceName code type }
# GetPolicySecurityRulesNo { policyName ruleType host }
# DelPolicySecurityRule { policyName ruleNo host }
# DelAllPolicySecurityRules {policyName ruleType host}
# EditPolicySecurityRule { host policyName ruleType ruleNo action service}
#
# FirewallAntiSpoof { host action }
# FirewallScanDetection { host action }
# FirewallScanDetection { host parameter value }
#########################################

#############################################################
# OBSOLATED. Use InstallLicense proc from GenSwExpect.tcl
# FwLicenseInstall: install the firewall license.
#
# IN:  licence: fw license key string
#      host:    (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc FwLicenseInstall {licence host} {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   Exec "license install fw $licence" "CONFIG" $host

   return [CheckGlobalErr $err_count]
}


##############################################################
# EnaContivityStatefulFirewall: Enable the contivity statefull firewall.
#
# IN:  host: (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS - when CLI commands OK and no reboot needed.
#      ERROR   - when fail to execute CLI commands.
#      NEEDREBOOT - when after enable feature, restart is needed.
##############################################################
proc EnaContivityStatefulFirewall { host } {
   
   global cmdOut
   set err_count [GetGlobalErr]
   set ret_code "ERROR"

   SetCliLevel "CONFIG" $host
   Exec "firewall policy" "CONFIG" $host 

   if {[regexp {requires a valid license} $cmdOut] == 1} {
      ErrCheck "{ERROR: stateful firewall not enabled. No FW license key installed}"
   }

   if {[regexp -nocase {restart} $cmdOut] == 1} {
      set ret_code "NEEDREBOOT"
   }

   set ok_cli [CheckGlobalErr $err_count]
   if {$ok_cli == "SUCCESS" && $ret_code == "NEEDREBOOT"} {     
      return $ret_code
   }
   return $ok_cli
   
}


#############################################################
# EnaContivityIfFilters: Enable contivity interface filters.
#
# IN:  host: (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS - when CLI commands OK and no reboot needed.
#      ERROR   - when fail to execute CLI commands.
#      NEEDREBOOT - when after enable feature, restart is needed.
#############################################################
proc EnaContivityIfFilters { host } {
   global cmdOut
   set ret_code "ERROR"
   set err_count [GetGlobalErr]
   
   SetCliLevel "CONFIG" $host
   Exec "firewall contivity" "CONFIG" $host

   if {[regexp -nocase {restart} $cmdOut] == 1 || \
           [regexp -nocase {reboot} $cmdOut] == 1} {
      set ret_code "NEEDREBOOT"
   }

   set ok_cli [CheckGlobalErr $err_count]
   if {$ok_cli == "SUCCESS" && $ret_code == "NEEDREBOOT"} {
      return $ret_code
   }
   return $ok_cli
   
}


#############################################################
# EnaContivityIfFilters: Enable both  contivity statefull firewall and 
#                        contivity interface filters.
#
# IN:  host: (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS - when CLI commands OK and no reboot needed.
#      ERROR   - when fail to execute CLI commands.
#      NEEDREBOOT - when after enable feature, restart is needed.
#############################################################
proc EnaContivityFwAndIfFilters { host } {
   global cmdOut
   set err_count [GetGlobalErr]
   set ret_code "ERROR"

   SetCliLevel "CONFIG" $host
   Exec "firewall policy-contivity" "CONFIG" $host 

   if {[regexp {requires a valid license} $cmdOut] == 1} {
      ErrCheck "{ERROR: stateful firewall not enabled. No FW license key installed}"
   }

   if {[regexp -nocase {restart} $cmdOut] == 1} {
      set ret_code "NEEDREBOOT"
   }

   set ok_cli [CheckGlobalErr $err_count]
   if {$ok_cli == "SUCCESS" && $ret_code == "NEEDREBOOT"} {     
      return $ret_code
   }
   return $ok_cli 
}


#############################################################
# EnaTunelFilter: Enable contivity tunnel filter.
#
# IN:  host: (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc EnaTunnelFilter { host } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   Exec "firewall tunnel-filter" "CONFIG" $host

   return [CheckGlobalErr $err_count]
}


#############################################################
# EnaTunelMngFilter: Enable contivity tunnel management filter.
#
# IN:  host: (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS - when CLI commands OK.
#      ERROR   - when fail to execute CLI commands.
#############################################################
proc EnaTunnelMngFilter { host } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   Exec "firewall tunnel-management-filter" "CONFIG" $host

   return [CheckGlobalErr $err_count]
}


#############################################################
# DisFirewall: Disable both contivity interface filters and 
#              contivity statefull firewall.
# 
# IN:  host: (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS - when CLI commands OK and no reboot needed.
#      ERROR   - when fail to execute CLI commands.
#      NEEDREBOOT - when after disable feature, restart is needed.
#############################################################
proc DisFirewall { host } {
   set err_count [GetGlobalErr]
   set ret_code "ERROR"
   global cmdOut

   SetCliLevel "CONFIG" $host
   Exec "no firewall" "CONFIG" $host

   if {[regexp -nocase {restart} $cmdOut] == 1} {
      set ret_code "NEEDREBOOT"
   }

   set ok_cli [CheckGlobalErr $err_count]
   if {$ok_cli == "SUCCESS" && $ret_code == "NEEDREBOOT"} {
      return $ret_code
   }
   return $ok_cli
}


#############################################################
# DisTunnelFilter: Disable contivity tunnel filter.
#
# IN:  host: (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc DisTunnelFilter { host } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   Exec "no firewall tunnel-filter" "CONFIG" $host    

   return [CheckGlobalErr $err_count]
}


#############################################################
# DisTunnelMngFilter: Disable contivity tunnel management filter.
#
# IN:  host: (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc DisTunnelMngFilter { host } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   Exec "no firewall tunnel-management-filter" "CONFIG" $host    

   return [CheckGlobalErr $err_count]   
}


#############################################################
# ShowFirewall: 
#
# IN:  type: the type of the firewall relating information to display  
#            available types:
#              alg                       Displays Firewall ALG status
#              all                       Displays all available firewalls
#              anti-spoof                Displays global anti-spoof setting
#              connection-number         Displays number of boxes to be connected
#              enabled                   Displays enabled firewall
#              logging                   Displays firewall logging information
#              scan-detection            Displays Scan Detection settings
#              strict-tcp-rules          Displays TCP conversation creation rules
#              tunnel-filter             Displays tunnel filter setting
#              tunnel-management-filter  Displays tunnel management filter sett
#      host: (management IP)/(terminal server Ip:port)
#
# OUT: the output of 'show firewall type' 
#      ERROR
#############################################################
proc ShowFirewall { type host } {
   global cmdOut
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   Exec "show firewall $type" "CONFIG" $host        

   if {[CheckGlobalErr $err_count] == "SUCCESS"} {
      return $cmdOut
   } else {
      return "ERROR"
   }
}


#############################################################
# AddPolicySecurity: 
#
# IN:  policyName: 
#      host: 
#
# OUT: SUCCESS/ERROR
#############################################################
proc AddPolicySecurity { policyName host } {
   set err_count [GetGlobalErr] 

   SetCliLevel "CONFIG" $host
   Exec "policy security add $policyName" "CONFIG" $host

   return [CheckGlobalErr $err_count]
}


#############################################################
# DelPolicySecurity: 
#
# IN:  policyName: 
#      host: 
#
# OUT: SUCCESS/ERROR
#############################################################
proc DelPolicySecurity { policyName host } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   Exec "no policy security $policyName" "CONFIG" $host

   return [CheckGlobalErr $err_count]
}


#############################################################
# ShowPolicySecurity: 
#
# IN:  type: 
#      host: 
#
# OUT: SUCCESS/ERROR
#############################################################
proc ShowPolicySecurity { type host } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   Exec "show policy security $type" "CONFIG" $host

   return [CheckGlobalErr $err_count]
}


#############################################################
# AssignPolicySecurity: 
#
# IN:  policyName: 
#      host: 
#
# OUT: SUCCESS/ERROR
#############################################################
proc AssignPolicySecurity { policyName host } {
   set err_count [GetGlobalErr]

   global cmdOut   

   SetCliLevel "CONFIG" $host
   set execResult [Exec "policy security assign \"$policyName\"" "CONFIG" $host]
   if {$execResult == "SUCCESS"} {
      if {[regexp -nocase "fail" $cmdOut] == 1 || [regexp -nocase "cannot" $cmdOut] == 1} {
         ErrCheck [list "ERROR: the policy $policyName cannot be assigned"]
      }
   }
   
   return [CheckGlobalErr $err_count]
}


#############################################################
# EnterPolicySecurityLevel: 
#
# IN:  policyName: 
#      host: 
#
# OUT: SUCCESS/ERROR
#############################################################
proc EnterPolicySecurityLevel { policyName host } {
   set err_count [GetGlobalErr]
   
   set prompt "CES\\(config-fwpolicy\\)\#"
   SetCliLevel "CONFIG" $host
   Exec "policy security $policyName" $prompt $host

   return [CheckGlobalErr $err_count]
}


#############################################################
# OBSOLATED. Use SetCliLevel instead.
# ExitPolicyLevel:
#
# IN:  host: 
#
# OUT: SUCCESS/ERROR
#############################################################
proc ExitPolicyLevel { host } {    
   Exec "exit" "CONFIG" $host
}

#//??? - not sure if it is needed
proc ExitPolicySecurityLevel { host } {    
   Exec "exit" "CONFIG" $host
}


#############################################################
# AddPolicySecurityServiceIcmp: 
# 
# IN:  host:
#      policyName:
#      serviceName:
#      code:
#      type:
#
# OUT: SUCCESS/ERROR
#############################################################
proc AddPolicySecurityServiceIcmp {  host policyName serviceName code type } {
   set prompt "CES\\(config-fwpolicy\\)\#"

   EnterPolicySecurityLevel $policyName $host

   if {$code == "any"} {
      Exec "service add $serviceName icmp code $code" $prompt $host
   } else {
      Exec "service add $serviceName icmp code $code type $type" $prompt $host
   }       
   
   ExitPolicyLevel $host
   
}


#############################################################
# DelPolicySecurityService: 
#
# IN:  policyName:
#      serviceName:
#      host:
#
# OUT: SUCCESS/ERROR
#############################################################
proc DelPolicySecurityService { policyName serviceName host } {
   set prompt "CES\\(config-fwpolicy\\)\#"

   EnterPolicySecurityLevel $policyName $host
   
   Exec "no service $serviceName" $prompt $host
   
   ExitPolicyLevel $host    
}

proc EditPolicySecurityServiceIcmp { host policyName serviceName code type } {
   
   set prompt "CES\\(config-fwpolicy\\)\#"

   EnterPolicySecurityLevel $policyName $host
   if {$code == "any"} {
      Exec "service $serviceName icmp code $code" $prompt $host
   } else {
      Exec "service $serviceName icmp code $code type $type" $prompt $host
   }

   ExitPolicyLevel $host

}


############################################################
# GetPolicySecurityRulesNo:
#
# IN:  
#
# OUT: 
############################################################
proc GetPolicySecurityRulesNo { policyName ruleType host } {

   global cmdOut

   set prompt "CES\\(config-fwpolicy\\)\#"

   EnterPolicySecurityLevel $policyName $host

   Exec "show rule $ruleType" $prompt $host

   set rulesCounts 0
   
   foreach line [split $cmdOut "\n"] {
      if {[regexp {rule_number[\ \t]*:[\ \t]*[0-9]+} $line] == 1} {
         incr rulesCounts
      }
   }
   
   ExitPolicyLevel $host  

   return $rulesCounts
   
}


############################################################
# DelPolicySecurityRule:
#
# IN:  
#
# OUT: 
############################################################
proc DelPolicySecurityRule { host policy_name rule_type  rule_no } {
   
   set err_count [GetGlobalErr]
   
   set prompt "CES\\(config-fwpolicy\\)\#"   
   EnterPolicySecurityLevel $policy_name $host
   Exec "no rule $rule_type $rule_no" $prompt $host   
   SetCliLevel "CONFIG" $host

   return [CheckGlobalErr $err_count]
}


############################################################
# DelAllPolicySecurityRules:
#
# IN:  
#
# OUT: 
############################################################
proc DelAllPolicySecurityRules {policyName ruleType host} {

   set prompt "CES\\(config-fwpolicy\\)\#"

   set policyNo [GetPolicySecurityRulesNo $policyName $ruleType $host]

   EnterPolicySecurityLevel $policyName $host
   for {set i $policyNo} {$i >= 1} {incr i -1} {
      Exec "no rule $ruleType $i" $prompt $host         
   }
   ExitPolicyLevel $host

}

#############################################################
# EditPolicySecurityRule: configures a NAT rule
#
# IN:  host:       (management IP) / (terminal server Ip:port)
#      policyName: Security set name to assign
#      ruleType:   default/interface/override
#      ruleNo:     the rule you want to configure or "add" if you want to create a new rule  
#      action:     accept/drop/reject/user-auth
#      src_addr:   any/Net_object_name
#      src_if:     any/branch:any/system/trusted/tunnel:any/untrusted/user:any
#      dst_addr:   any/Net_object_name
#      dst_if:     any/branch:any/system/trusted/tunnel:any/untrusted/user:any
#      service:    Service object name
#      status:     enable/disable
#      log:        none/brief/detail/trap
#
# OUT: SUCCESS/ERROR
#############################################################
proc EditPolicySecurityRule { host policyName ruleType ruleNo action {service any} \
                                  {src_addr any} {src_if any} {dst_addr any} {dst_if any}\
                                  {status enable} {log "none"}} {

   global cmdOut
   set rcode ""
   
   set err_count [GetGlobalErr]

   set prompt "CES\\(config-fwpolicy\\)\#"
   EnterPolicySecurityLevel $policyName $host

   Exec "rule $ruleType $ruleNo action $action service $service src-address $src_addr src-interface $src_if dst-address $dst_addr dst-interface $dst_if status $status log $log" $prompt $host
   
   if {[regexp -nocase {is not a valid Network Object} $cmdOut] == 1} {
      set errMsg ""
      set errMsg1 ""
      regsub -all {\b\b } $cmdOut "" errMsg1
      regsub -all {\b} $errMsg1 "" errMsg
      lappend rcode "ERROR:\n$errMsg"
      ErrCheck $rcode
   }
   
   SetCliLevel "CONFIG" $host

   return [CheckGlobalErr $err_count]
}



#############################################################
# FirewallAntiSpoof: Enable/diable anti-spoofing
#
# IN:  host:   (management IP) / (terminal server Ip:port)
#      action: <enable/disable/no_enable>
#
# OUT: SUCCESS/ERROR
#############################################################
proc FirewallAntiSpoof { host {action "enable"}} {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   if {$action == "enable"} {
      Exec "firewall anti-spoof" "CONFIG" $host
   } elseif {$action == "disable" || $action == "no_enable"} {
      Exec "no firewall anti-spoof" "CONFIG" $host
   } else {
      ErrCheck {"ERROR: bad parameter: action = $action. Supported values: <enable/disable/no_enable>"}
   }

   return [CheckGlobalErr $err_count]
}


#############################################################
# FirewallScanDetection: Enable/disable Malicious Scan Detection.
#
# IN:  host:   (management IP) / (terminal server Ip:port)
#      action: <enable/disable/no_enable>
#
# OUT: SUCCESS/ERROR
#############################################################
proc FirewallScanDetection { host {action "enable"}} {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   if {$action == "enable"} {
      Exec "firewall scan-detection" "CONFIG" $host
   } elseif {$action == "disable" || $action == "no_enable"} {
      Exec "no firewall scan-detection" "CONFIG" $host
   } else {
      ErrCheck {"ERROR: bad parameter: action = $action. Supported values: <enable/disable/no_enable>"}
   }

   return [CheckGlobalErr $err_count]   
}


#############################################################
# FirewallScanDetectionParam: Set different parameters for scan-detection.
#
# IN:  host:      (management IP) / (terminal server Ip:port)   
#      parameter: interval           Specifies Detection Interval
#                 threshold-network  Network Scan Threshold
#                 threshold-port     Port Scan Threshold
#      value: for interval:          <1-60>  Detection Interval (in minutes)
#             for threshold-network: <1-10000>
#             for threshold-port:    <1-10000>
#
# OUT: SUCCESS/ERROR
#############################################################
proc FirewallScanDetectionParam { host parameter value } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host   
   Exec "firewall $parameter $value" "CONFIG" $host

   return [CheckGlobalErr $err_count]
}


#############################################################
# FirewallLogging: Enable/disable firewall logging.
#
# IN:  host:    (management IP) / (terminal server Ip:port)
#      logging: all        Enables firewall, NAT, traffic and Policy Manager loggings
#               debug      Enables debug logging
#               firewall   Enables firewall logging               
#               nat        Enables NAT logging
#               polmgr     Enables policy manager logging
#               traffic    Enables traffic logging
#      action:  <enable/disable/no_enable>
#
# OUT: 
#############################################################
proc FirewallLogging { host logging {action "enable"} } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   if {$action == "enable"} {
      Exec "firewall logging $logging" "CONFIG" $host
   } elseif {$action == "disable" || $action == "no_enable"} {
      Exec "no firewall logging $logging" "CONFIG" $host
   } else {
      ErrCheck {"ERROR: bad parameter: action = $action. Supported values: <enable/disable/no_enable>"}
   }

   return [CheckGlobalErr $err_count]  
}
