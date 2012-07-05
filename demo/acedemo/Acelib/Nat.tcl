############################
# NAT setup related function
#
# EnterPolicyObjectLevel { host }
# ExitPolicyObjectLevel { host }
# AddIpRangeNetObj { objName startingIp endingIp host }
# AddHostNetObj {objName ip host}
# AddNetworkNetObj {objName NetIp mask host}
# DelNetObj {objName host}
#
# ShowPolicyNat { host }
# AddPolicyNat { policyName host }
# DelPolicyNat { policyName host }
# EnterPolicyNatLevel {policyName host}
# OBSOLATED. Use SetCliLevel instead. ExitPolicyNatLevel { host } 
# EditPolicyNatRule { host policyName ruleNo actionType srcNetObj destNetObj translatedNetObj}
# OBSOLATED. Use EditPolicyNatRule instead. EditPolicyNatStaticRule { host policyName ruleNo srcNetObj destNetObj translatedSource}
# EnaInterfaceNat {host}
# DisInterfaceNat {host}
# AssignNatIf {host policyName}
# NotAssignNatIf {host}
# GetNatTranslationStatus {host nat_place nat_type ip}
#############################


proc EnterPolicyObjectLevel { host } {
   set prompt "CES\\(config-policyobj\\)\#"
   SetCliLevel "CONFIG" $host
   Exec "policy object" $prompt $host
}

proc ExitPolicyObjectLevel { host } {
   Exec "exit" "CONFIG" $host
}

proc AddIpRangeNetObj { objName startingIp endingIp host } {

   set prompt "CES\\(config-policyobj\\)\#"

   EnterPolicyObjectLevel $host

   set execResult [Exec "netobj add $objName ip-range $startingIp $endingIp" $prompt $host]
   
   ExitPolicyObjectLevel $host

   return $execResult
}

proc DelNetObj {objName host} {

   set prompt "CES\\(config-policyobj\\)\#"

   EnterPolicyObjectLevel $host

   set execResult [Exec "no netobj $objName" $prompt $host]
   
   if { $execResult == "ANSWREQ" } {
      set execResult  [Exec "yes" $prompt $host]
   }

   ExitPolicyObjectLevel $host

   return $execResult   
}

#############################################################
# AddHostNetObj: add a new host NAT object
#
# IN:  host:    (management IP) / (terminal server Ip:port)
#      objName: name of object
#      ip:      host ip
#    
# OUT: SUCCESS/ERROR
#############################################################
proc AddHostNetObj {objName ip host} {

   set err_count [GetGlobalErr]

   set prompt "CES\\(config-policyobj\\)\#"
   
   EnterPolicyObjectLevel $host
   
   Exec "netobj add $objName host $ip" $prompt $host
   
   SetCliLevel "CONFIG" $host
   
   return [CheckGlobalErr $err_count]
}

#############################################################
# AddNetworkNetObj: add a new host NAT object
#
# IN:  host:    (management IP) / (terminal server Ip:port)
#      objName: name of object
#      NetIp:   network ip
#      mask:    <0-32>
#
# OUT: SUCCESS/ERROR
#############################################################
proc AddNetworkNetObj {objName NetIp mask host} {

   set err_count [GetGlobalErr]

   set prompt "CES\\(config-policyobj\\)\#"
   
   EnterPolicyObjectLevel $host
   
   Exec "netobj add $objName network $NetIp/$mask" $prompt $host
   
   SetCliLevel "CONFIG" $host
   
   return [CheckGlobalErr $err_count]
}


#############################
# ShowPolicyNat - returns a string with all nat policies existing on the switch
#
#############################
proc ShowPolicyNat { host } {

   global cmdOut

   set natPolicies ""

   SetCliLevel "CONFIG" $host
   Exec "show policy nat" "CONFIG" $host    
   

   foreach line [split $cmdOut "\n"] {

      #puts $line
      set policyName ""

      if {[regexp {[a-zA-Z0-9\-]+} $line policyName] == 1 && \
              [regexp {NAT Policies} $line] != 1 && \
              [regexp {show policy nat} $line] != 1 && \
              [regexp {CES\(config\)\#} $line] != 1} {
         
         lappend natPolicies $policyName       

      }
   }

   return $natPolicies
}

proc AddPolicyNat { policyName host } {

   SetCliLevel "CONFIG" $host
   Exec "policy nat add $policyName" "CONFIG" $host   
}

proc DelPolicyNat { policyName host } {

   SetCliLevel "CONFIG" $host
   Exec "no policy nat $policyName" "CONFIG" $host
   
}

proc EnterPolicyNatLevel {policyName host} {
   set prompt "CES\\(config-natpolicy\\)\#"
   SetCliLevel "CONFIG" $host
   Exec "policy nat $policyName" $prompt $host
}

proc ExitPolicyNatLevel { host } {
   Exec "exit" "CONFIG" $host    
}


#############################################################
# EditPolicyNatRule: configures a NAT rule
#
# IN:  host:             (management IP) / (terminal server Ip:port)
#      policyName:       NAT set name to assign
#      ruleNo:           the rule you want to configure or "add" if you want to create a new rule  
#      actionType:       none/pooled/port/port-fwd/static
#      srcNetObj:        any/Net_object_name
#      destNetObj:       any/Net_object_name
#      translatedNetObj: Net_object_name. It is:
#                         - translated-source for actionType: static, port and pooled;
#                         - translated-destination for port-fwd.
#      service           Service Object for service
#    
# OUT: SUCCESS/ERROR
#############################################################
proc EditPolicyNatRule { host policyName ruleNo actionType srcNetObj destNetObj translatedNetObj {service any}} {
   
   global cmdOut
   set rcode ""

   set err_count [GetGlobalErr]
   
   set prompt "CES\\(config-natpolicy\\)\#"
   EnterPolicyNatLevel $policyName $host
   
   if {$actionType == "port-fwd"} {
      Exec "rule $ruleNo action $actionType source $srcNetObj destination $destNetObj translated-destination $translatedNetObj service $service" \
          $prompt $host
   } else {
      Exec "rule $ruleNo action $actionType source $srcNetObj destination $destNetObj translated-source $translatedNetObj service $service" \
          $prompt $host
   }
   if {[regexp -nocase {is not a valid NAT Network Object} $cmdOut] == 1} {
      set errMsg ""
      set errMsg1 ""
      regsub -all {\b\b } $cmdOut "" errMsg1
      regsub -all {\b} $errMsg1 "" errMsg
      lappend rcode "ERROR:\n$errMsg"
      ErrCheck $rcode
    } elseif {[regexp -nocase {Original Source and Translated Source range\/host can not overlap} $cmdOut] == 1} {
	set errMsg ""
	set errMsg1 ""
	regsub -all {\b\b } $cmdOut "" errMsg1
	regsub -all {\b} $errMsg1 "" errMsg
	lappend rcode "ERROR:\n$errMsg"
	ErrCheck $rcode
    }

   ExitPolicyLevel $host
   
   return [CheckGlobalErr $err_count]
}

############################################################
# DelPolicySecurityRule:
#
# IN:  host:             (management IP) / (terminal server Ip:port)
#      policyName:       policy NAT name
#      ruleNo:           the rule you want to delete
#
# OUT: SUCCESS/ERROR
############################################################
proc DelPolicyNATRule { host policyName ruleNo } {
   
   set err_count [GetGlobalErr]
   
   set prompt "CES\\(config-natpolicy\\)\#"
   EnterPolicyNatLevel $policyName $host
   Exec "no rule $ruleNo" $prompt $host   
   SetCliLevel "CONFIG" $host

   return [CheckGlobalErr $err_count]
}

#############################################################
# OBSOLATED. Use EditPolicyNatRule instead with parameter $actionType = "static"
# EditPolicyNatStaticRule:
#
# Description: configures a static NAT rule
#
# Variables: 
#     IN:  host
#          policyName
#          ruleNo - the rule you want to configure or "add" if you want to create a new rule  
#          srcNetObj
#          destNetObj
#          translatedSource
#    
#    OUT: SUCCESS or ERROR
#
# NOTE: at this moment this proc don't know to configure the description, service and status parameters
#
#############################################################
proc EditPolicyNatStaticRule { host policyName ruleNo srcNetObj destNetObj translatedSource} {
   
   global cmdOut
   set rcode ""
   
   set prompt "CES\\(config-natpolicy\\)\#"
   EnterPolicyNatLevel $policyName $host
   
   Exec "rule $ruleNo action static source $srcNetObj destination $destNetObj translated-source $translatedSource" \
       $prompt $host
   
   if {[regexp -nocase {is not a valid NAT Network Object} $cmdOut] == 1} {
      set errMsg ""
      set errMsg1 ""
      regsub -all {\b\b } $cmdOut "" errMsg1
      regsub -all {\b} $errMsg1 "" errMsg
      lappend rcode "ERR: fail to configure Static NAT policy rule:\n$errMsg"
   }
   
   ExitPolicyLevel $host
   
   return [ErrCheck $rcode EditPolicyNatStaticRule]
}

#############################################################
# EnaInterfaceNat: enable interface NAT.
#
# NOTE: Need to reboot the system in order to activate 
#       this setting.
#
# IN:  host: (management IP) / (terminal server Ip:port)
#    
# OUT: SUCCESS/ERRO
#############################################################
proc EnaInterfaceNat {host} {

   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   Exec "policy nat interface enable" "CONFIG" $host

   return [CheckGlobalErr $err_count]
}

#############################################################
# DisInterfaceNat: disable interface NAT
#
# NOTE: Need to reboot the system in order to activate 
#       this setting.
#
# IN:  host: (management IP) / (terminal server Ip:port)
#    
# OUT: SUCCESS/ERROR
#
#############################################################
proc DisInterfaceNat {host} {

   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   Exec "no policy nat interface enable" "CONFIG" $host

   return [CheckGlobalErr $err_count]
}

#############################################################
# AssignNatIf: Assign a NAT set to Interface NAT
#
# IN:  host: (management IP) / (terminal server Ip:port)
#      policyName: NAT set name to assign
#    
# OUT: SUCCESS/ERROR
#
#############################################################
proc AssignNatIf {host policyName} {

   set err_count [GetGlobalErr]
   SetCliLevel "CONFIG" $host

   Exec "policy nat interface assign $policyName" "CONFIG" $host

   return [CheckGlobalErr $err_count]
}

#############################################################
# NotAssignNatIf: Removes a policy from interface NAT
#
# IN:  host: (management IP) / (terminal server Ip:port)
#    
# OUT: SUCCESS/ERROR
#
#############################################################
proc NotAssignNatIf {host} {

   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   Exec "no policy nat interface assign" "CONFIG" $host

   return [CheckGlobalErr $err_count]
}


#############################################################
#  GetNatTranslationStatus: Gets NAT translations
#
# IN:  host:       (management IP) / (terminal server Ip:port)
#      nat_place:  interfaces/<bo_name>
#      nat_type:   source-port/source-pooled/source-static/destination-portForwarding/destination-static
#      ip:         the IP for translating
#
# OUT: ERROR:      if CLI errors
#      VALUE:      the value for appropriate translated IP
#      NONE:       if is not any nat translation
# #############################################################
proc GetNatTranslationStatus {host nat_place nat_type ip} {
    global cmdOut
    set err_count [GetGlobalErr]

    SetCliLevel "PRIVILEGE" $host
    Exec "terminal paging off" "PRIVILEGE" $host

    Exec "show status statistics security nat-translations" "PRIVILEGE" $host 0 60

    if {[CheckGlobalErr $err_count] == "ERROR"} {
        return "ERROR"
    }

    set new_nat_type [split $nat_type "-"]
#puts "new_nat_type $new_nat_type"
    set nat_type ""
#puts "lindex \$new_nat_type 1:  [lindex $new_nat_type 1]"
    if {[lindex $new_nat_type 1] == "portForwarding"} {
        set new_nat_type [lreplace $new_nat_type 1 1 forwarding]
    }
append nat_type [lindex $new_nat_type 0] ".*" [lindex $new_nat_type 1]
#puts "nat_type:    *$nat_type*"

set f 0
set n 0
foreach line [split $cmdOut "\r"] {
    if {$f==0 && [regexp -nocase "$nat_place"  $line] == 1} {
        set f 1
        continue
    }
    if { $f==1 && [regexp -nocase "$nat_type" $line] == 1} {
        set n 1
        continue
    }
    if { $f==1 && [regexp -nocase "Physical Interfaces|BO Tunnel" $line] == 1 && [regexp -nocase "$nat_place"  $line] != 1} {
        set f 0
        set n 0
        continue
    }
    
    if { $n==1 && [regexp -nocase "Translate" $line] == 1} {
        set n 0
        continue
    }

    if {$n==1 && [regexp "($ip)\[:0-9\]*\[\ =>\]+(\[0-9\.\]+)\[:0-9\]*" $line all first_ip last_ip] == 1} {
        set translt_ip_array($first_ip) $last_ip
        #puts " $first_ip $last_ip"
        return $last_ip
    }
}
return "NONE"
}



