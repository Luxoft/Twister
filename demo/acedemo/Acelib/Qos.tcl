###################################
# Qos library
# 
# This file contains the Acelib procedures relating to Qos CLI commands
#
# QosAdmissionControl {host status}
# QosBwm {host status}
# QosBwRate {host bw_rate}
#
# #- MF Class
# AddQosMfClass { mfClass host }
# DelQosMfClass { mfClass host }
# ShowQosMfClass { host }
# EnterQosMfClassLevel { mfClass host }
# ExitQosMfClassLevel { host }; OBSOLATED. Use SetCliLevel instead
# QosMfClassAddRule {host mf_class mf_rule}
# QosMfClassRemoveRule {host mf_class mf_rule}
# QosMfClassMoveRule {host mf_class mf_rule up_down}
# 
# #- MF Class rules
# AddQosMfClassRule { rule host }
# DelQosMfClassRule { rule host }
# ShowQosMfClassRules { host }
# EnterQosMfClassRuleLevel { rule host }
# ExitQosMfClassRuleLevel { host }; OBSOLATED. Use SetCliLevel instead
# QosMfRuleDstAddr {host mf_rule addr_name addr_ip addr_mask {delete "NO"}}
# QosMfRuleSrcAddr {host mf_rule addr_name addr_ip addr_mask {delete "NO"}}
# QosMfRuleProto {host mf_rule proto_name proto_number {delete "NO"}}
# QosMfRuleSrcPort {host mf_rule port_name prot_number {delete "NO"}}
# QosMfRuleDstPort {host mf_rule port_name prot_number {delete "NO"}}
# QosMfRuleDscpValues {host mf_rule dscp_name dscp_value {dscp_mask 63}}
# QosMfRuleDsMark {host mf_rule ds_mark}
# QosMfRuleUse {host attribute name}
# 
# #- QoS settings relating to interface
# IfQosOSRatio {host if_id os_ratio}
# IfQosMfClass {host if_type if_id action}
# IfQosMfClassEgress {host if_type if_id mf_class {disable "NULL"}}
# IfQosMfClassIngress {host if_type if_id mf_class {disable "NULL"}}
# IfQosStatReset {host if_type if_id}
# IfQosEgressQueuingMode {host if_type if_id q_mode}
# ShowIfQosStat {host if_type if_id}
# ParseIfQosStat {qos_stats info_to_get arr_rez_stat}
###################################


#############################################################
# QosAdmissionControl: Enables/Disables admission control.
#
# IN:  host:   (management IP)/(terminal server Ip:port)
#      status: enable / (no_enable/disable) - QoS admission 
#              control status
#
# OUT: SUCCESS/ERROR
#############################################################
proc QosAdmissionControl {host status} {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host   
   if {[regexp "dis" $status] || [regexp "no_ena" $status]} {
      Exec "no qos admission-control enable" "CONFIG" $host
   } else {
      Exec "qos admission-control $status" "CONFIG" $host
   }

   return [CheckGlobalErr $err_count]
}


#############################################################
# QosBwm: Enables/Disables bandwidth management
#
# IN:  host:   (management IP)/(terminal server Ip:port)
#      status: enable / (no_enable/disable) - QoS bandwidth 
#              management status
#
# OUT: SUCCESS/ERROR
#############################################################
proc QosBwm {host status} {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host   
   if {[regexp "dis" $status] || [regexp "no_ena" $status]} {
      Exec "no qos bandwidth-management enable" "CONFIG" $host
   } else {
      Exec "qos bandwidth-management $status" "CONFIG" $host
   }

   return [CheckGlobalErr $err_count]
}


#############################################################
# QosBwRate: Enables user to create specific bandwidth rate
#
# IN:  host:    (management IP)/(terminal server Ip:port)  
#      bw_rate: <0-100000000>
#
# OUT: SUCCESS/ERROR
#############################################################
proc QosBwRate {host bw_rate} {
   set err_count [GetGlobalErr]
 
   SetCliLevel "CONFIG" $host     
   Exec "qos bandwidth-rate $bw_rate" "CONFIG" $host

   return [CheckGlobalErr $err_count]
}


#############################################################
# AddQosMfClass: Add qos classifier.
#
# IN:  mfClass: name of classifier
#      host:    (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc AddQosMfClass { mfClass host } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   Exec "qos mf-class add $mfClass" "CONFIG" $host

   return [CheckGlobalErr $err_count]
}


#############################################################
# DelQosMfClass: Delete qos classifier.
#
# IN:  mfClass: name of classifier
#      host:    (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc DelQosMfClass { mfClass host } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   Exec "no qos mf-class $mfClass" "CONFIG" $host
   
   return [CheckGlobalErr $err_count]
}


#############################################################
# ShowQosMfClass: Display qos classifiers.
#
# IN:  host: (management IP)/(terminal server Ip:port)
#
# OUT: ERROR/(the output of 'show qos mf-class' CLI command)
#############################################################
proc ShowQosMfClass { host } {
   global cmdOut
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   Exec "show qos mf-class" "CONFIG" $host

   if {[CheckGlobalErr $err_count] == "SUCCESS"} {
      return [cesLogsSetup $cmdOut]
   } else {
      return "ERROR"
   }      
}


#############################################################
# EnterQosMfClassLevel: Enter into config-mfclass CLI level.
#
# IN:  mfClass: name of classifier
#      host:    (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR 
#############################################################
proc EnterQosMfClassLevel { mfClass host } {
   global cmdOut

   set prompt "CES\\(config-mfclass\\)\#"
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   Exec "qos mf-class $mfClass" $prompt $host

   return [CheckGlobalErr $err_count]
}



##############################################################
# OBSOLATED. Use 'SetCliLevel "CONFIG" $host' instead
# ExitQosMfClassLevel: Exit from mf-class CLI level and go back 
#                      config level.
#
# IN:  host: (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
##############################################################
proc ExitQosMfClassLevel { host } {
    Exec "exit" "CONFIG" $host    
}


#############################################################
# QosMfClassAddRule: Add a rule to the classifier
#
# IN:  host:     (management IP)/(terminal server Ip:port)
#      mf_class: name of classifier
#      mf_rule:  rule name
#
# OUT: SUCCESS/ERROR
#############################################################
proc QosMfClassAddRule {host mf_class mf_rule} {
   global cmdOut
   
   set prompt "CES\\(config-mfclass\\)\#"
   set err_count [GetGlobalErr]

   EnterQosMfClassLevel $mf_class $host
   Exec "add-rule $mf_rule" $prompt $host

   if {[regexp "does not exist" $cmdOut] == 1} {
      lappend rcode "ERROR:\n$cmdOut"
      ErrCheck $rcode
   }

   return [CheckGlobalErr $err_count]   
}


#############################################################
# QosMfClassRemoveRule: Delete a rule from the classifier
#
# IN:  host:     (management IP)/(terminal server Ip:port)
#      mf_class: name of classifier
#      mf_rule:  rule name
#
# OUT: SUCCESS/ERROR
#############################################################
proc QosMfClassRemoveRule {host mf_class mf_rule} {
   global cmdOut
   
   set prompt "CES\\(config-mfclass\\)\#"
   set err_count [GetGlobalErr]

   EnterQosMfClassLevel $mf_class $host
   Exec "remove-rule $mf_rule" $prompt $host

   if {[regexp "does not exist" $cmdOut] == 1} {
      lappend rcode "ERROR:\n$cmdOut"
      ErrCheck $rcode
   }

   return [CheckGlobalErr $err_count]    
}


#############################################################
# QosMfClassMoveRule: Move a rule up or down (change priority)
#
# IN:  host:     (management IP)/(terminal server Ip:port)
#      mf_class: name of classifier
#      mf_rule:  rule name
#      up_down:  up/down  
#
# OUT: SUCCESS/ERROR
#############################################################
proc QosMfClassMoveRule {host mf_class mf_rule up_down} {
   global cmdOut

   set prompt "CES\\(config-mfclass\\)\#"
   set err_count [GetGlobalErr]

   EnterQosMfClassLevel $mf_class $host
   Exec "move-rule $mf_rule $up_down" $prompt $host

   if {[regexp "does not exist" $cmdOut] == 1} {
      lappend rcode "ERROR:\n$cmdOut"
      ErrCheck $rcode
   }

   return [CheckGlobalErr $err_count]   
}



####################
#- MF Class rules
####################

#############################################################
# AddQosMfClassRule: Add new rule.
#
# IN:  rule: Name of rule
#      host: (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc AddQosMfClassRule { rule host } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   Exec "qos mf-class rule add $rule" "CONFIG" $host    
   
   return [CheckGlobalErr $err_count]
}


#############################################################
# DelQosMfClassRule: Delete a rule.
#
# IN:  rule: Name of rule
#      host: (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc DelQosMfClassRule { rule host } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host   
   Exec "no qos mf-class rule $rule" "CONFIG" $host        

   return [CheckGlobalErr $err_count]
}


#############################################################
# ShowQosMfClassRules: Display the MF Classes rules.
#
# IN:  host: (management IP)/(terminal server Ip:port)
#
# OUT: ERROR/(the output of 'show qos mf-class rule' CLI command)
#############################################################
proc ShowQosMfClassRules { host } {
   global cmdOut
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host   
   Exec "show qos mf-class rule" "CONFIG" $host

   if {[CheckGlobalErr $err_count] == "SUCCESS"} {
      return [cesLogsSetup $cmdOut]
   } else {
      return "ERROR"
   }
}


#############################################################
# EnterQosMfClassRuleLevel: Enter to 'CES(config-mfrule)' CLI level.
#
# IN:  rule: Name of rule
#      host: (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc EnterQosMfClassRuleLevel { rule host } {
   set prompt "CES\\(config-mfrule\\)\#"
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host

   Exec "qos mf-class rule $rule" $prompt $host
   return [CheckGlobalErr $err_count]
}


#############################################################
# OBSOLATED. Use 'SetCliLevel "CONFIG" $host' instead.
# ExitQosMfClassRuleLevel: Exit from 'config-mfrule' CLI level
#                          and go back to config level.
#
# IN:  host:  (management IP)/(terminal server Ip:port)
#
# OUT: SUCCESS/ERROR
#############################################################
proc ExitQosMfClassRuleLevel { host } {
    Exec "exit" "CONFIG" $host 
}


#############################################################
# QosMfRuleDstAddr: Create/Modifie classifier's destination address
#
# IN:  host:      (management IP)/(terminal server Ip:port)
#      mf_rule:   Name of rule
#      addr_name: Name of address
#      addr_ip:   A.B.C.D  IP Address of source
#      addr_mask: A.B.C.D  Mask address of the source
#
# OUT: SUCCESS/ERROR
#############################################################
proc QosMfRuleDstAddr {host mf_rule addr_name addr_ip addr_mask {delete "NO"}} {
   set prompt "CES\\(config-mfrule\\)\#"
   set err_count [GetGlobalErr]   

   EnterQosMfClassRuleLevel $mf_rule $host
   if {$delete == "NO"} {         
      Exec "destination-address $addr_name ip $addr_ip mask $addr_mask" $prompt $host
   } else {
      Exec "no destination-address $addr_name" $prompt $host
   }
   return [CheckGlobalErr $err_count]
}


#############################################################
# QosMfRuleSrcAddr: Create/Modifie classifier's source address
#
# IN:  host:      (management IP)/(terminal server Ip:port)
#      mf_rule:   Name of rule
#      addr_name: Name of address
#      addr_ip:   A.B.C.D  IP Address of source
#      addr_mask: A.B.C.D  Mask address of the source
#
# OUT: SUCCESS/ERROR
#############################################################
proc QosMfRuleSrcAddr {host mf_rule addr_name addr_ip addr_mask {delete "NO"}} {
   set prompt "CES\\(config-mfrule\\)\#"
   set err_count [GetGlobalErr]   

   EnterQosMfClassRuleLevel $mf_rule $host
   if {$delete == "NO"} {
      Exec "source-address $addr_name ip $addr_ip mask $addr_mask" $prompt $host
   } else {
      Exec "no source-address $addr_name" $prompt $host
   }

   return [CheckGlobalErr $err_count]
}


#############################################################
# QosMfRuleProto: Defines the protocols.
#
# IN:  host:         (management IP)/(terminal server Ip:port)
#      mf_rule:      Name of rule
#      proto_name:   Name of Protocol
#      proto_number: <0-255>  Protocol number
#      delete:       if not "NO" disable the protocol
#
#      Predefined Protocols on CES:
#        icmp: 1
#        ip:   255
#        tcp:  6
#        udp:  17

#
# OUT: SUCCESS/ERROR
#############################################################
proc QosMfRuleProto {host mf_rule proto_name proto_number {delete "NO"}} {
   set prompt "CES\\(config-mfrule\\)\#"
   set err_count [GetGlobalErr]

   EnterQosMfClassRuleLevel $mf_rule $host
   if {$delete == "NO"} {
      Exec "protocol $proto_name $proto_number" $prompt $host
   } else {
      Exec "no protocol $proto_name" $prompt $host
   }

   return [CheckGlobalErr $err_count]  
}


#############################################################
# QosMfRuleSrcPort: Create/Modify source port values.
#
# IN:  host:        (management IP)/(terminal server Ip:port)
#      mf_rule:     Name of rule
#      port_name:   Name of source port
#      prot_number: <0-65535> Port number
#      delete:      if not "NO" delete the source port
#
# OUT: SUCCESS/ERROR
#############################################################
proc QosMfRuleSrcPort {host mf_rule port_name port_number {delete "NO"}} {
   set prompt "CES\\(config-mfrule\\)\#"
   set err_count [GetGlobalErr]

   EnterQosMfClassRuleLevel $mf_rule $host
   if {$delete == "NO"} {
      Exec "tcp-udp-source-port $port_name $port_number" $prompt $host
   } else {
      Exec "no tcp-udp-source-port $port_name" $prompt $host
   }

   return [CheckGlobalErr $err_count] 
}


#############################################################
# QosMfRuleDstPort: Destination port value.
#
# IN:  host:        (management IP)/(terminal server Ip:port)
#      mf_rule:     Name of rule
#      port_name:   Name of destination port
#      prot_number: <0-65535> Port number
#      delete:      if not "NO" delete the destination port 
#
# OUT: SUCCES/ERROR
#############################################################
proc QosMfRuleDstPort {host mf_rule port_name port_number {delete "NO"}} {
   set prompt "CES\\(config-mfrule\\)\#"
   set err_count [GetGlobalErr]

   EnterQosMfClassRuleLevel $mf_rule $host
   if {$delete == "NO"} {
      Exec "tcp-udp-destination-port $port_name $port_number" $prompt $host
   } else {
      Exec "tcp-udp-destination-port $port_name" $prompt $host
   }

   return [CheckGlobalErr $err_count] 
}


#############################################################
# QosMfRuleDscpValues: Set the Dscp Values for classifer
#
# IN:  host:       (management IP)/(terminal server Ip:port)
#      mf_rule:    Name of rule
#      dscp_name:  Name of dscp value;
#      dscp_value: <0-255> Value of the dscp;
#      dscp_mask:  <0-255> Mask for dscp.
#
# Standard DSCP values:
#     name      value  mask
#  ------------------------
#  AF1HighDrop : 14    63
#  AF1LowDrop :  10    63
#  AF1MedDrop :  12    63
#  AF2HighDrop : 22    63
#  AF2LowDrop :  18    63
#  AF2MedDrop :  20    63
#  AF3HighDrop : 30    63
#  AF3LowDrop :  26    63
#  AF3MedDrop :  28    63
#  AF4HighDrop : 38    63
#  AF4LowDrop :  34    63
#  AF4MedDrop :  36    63
#  any :          0    63
#  EF :          46    63
# 
#  (63 = 00111111)
#
# OUT: SUCCESS/ERROR
#############################################################
proc QosMfRuleDscpValues {host mf_rule dscp_name dscp_value {dscp_mask 63}} {
   set prompt "CES\\(config-mfrule\\)\#"
   set err_count [GetGlobalErr]

   EnterQosMfClassRuleLevel $mf_rule $host   
   Exec "dscp-values $dscp_name value $dscp_value mask $dscp_mask" $prompt $host   

   return [CheckGlobalErr $err_count] 
}


#############################################################
# QosMfRuleDsMark: Set the Differential Services markings for 
#                  classifers.
#
# IN:  host:       (management IP)/(terminal server Ip:port)
#      mf_rule:    Name of rule
#      ds_mark:    Differential Services markings for classifers
#                  Supported values:
#                    AF1  Diffserv-marking is set to AF1
#                    AF2  Diffserv-marking is set to AF2
#                    AF3  Diffserv-marking is set to AF3
#                    AF4  Diffserv-marking is set to AF4
#                    EF   Diffserv-marking is set to EF

#
# OUT: SUCCESS/ERROR
#############################################################
proc QosMfRuleDsMark {host mf_rule ds_mark} {
   set prompt "CES\\(config-mfrule\\)\#"
   set err_count [GetGlobalErr]

   EnterQosMfClassRuleLevel $mf_rule $host   
   Exec "diffserv-marking $ds_mark" $prompt $host

   return [CheckGlobalErr $err_count]   
}


#############################################################
# QosMfRuleUse: Enable user to assign values to different
#               attributes of a rule.
#
# IN:  host:      (management IP)/(terminal server Ip:port)
#      mf_rule:   Name of rule
#      attribute: 
#      name:      a name already defined on CES for the attribute 
#                 (e.g. any (for any attribute), tcp (for protocol),
#                 (     telnet for tcp_udp_destination_port) ...).
#
#      Allowed attributes:
#        destination_address
#        diffserv_marking
#        dscp
#        protocol
#        source_address
#        tcp_udp_destination_port
#        tcp_udp_source_port
#
# OUT: SUCCESS/ERROR
#############################################################
proc QosMfRuleUse {host mf_rule attribute name} {
   global cmdOut

   set prompt "CES\\(config-mfrule\\)\#"
   set err_count [GetGlobalErr]

   EnterQosMfClassRuleLevel $mf_rule $host   
   Exec "use $attribute $name" $prompt $host

   set cmdOut [string tolower $cmdOut]
   if {[regexp -nocase {no such[0-9a-z\ ]+exists} $cmdOut]} {
      ErrCheck "{ERROR: Bad parameters: attribute = $attribute;  name = $name}"
   }

   return [CheckGlobalErr $err_count]   
}



#############################################################
# QoS settings relating to interface
#############################################################

#############################################################
# IfQosOSRatio: Configures 'over-subscription-ratio' for the 
#               selected physical interface.
#
# IN:  host:     (management IP) / (terminal server Ip:port)
#      if_type:  interface type in the format known by CES
#                     e.g. fast ethernet interface: FastEthernet
#                          wan interface:           serial
#      if_id:    <0-6>/<1-4>  slot number / port number
#      os_ratio: <1-42>  Over subscribtion ratio
#
# OUT: SUCCESS/ERROR
#############################################################
proc IfQosOSRatio {host if_type if_id os_ratio} {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host

   set prompt "CES\\(config-if\\)\#"   
   EnterConfigIfLevel $if_type $if_id $host
   Exec "qos over-subscription-ratio $os_ratio" $prompt $host

   SetCliLevel "USER" $host
   return [CheckGlobalErr $err_count]
}


#############################################################
# IfQosMfClass: Configure mf class for interface.
#
# IN:  host:     (management IP) / (terminal server Ip:port)
#      if_type:  interface type in the format known by CES
#                     e.g. fast ethernet interface: FastEthernet
#                          wan interface:           serial
#      if_id:    <0-6>/<1-4>  slot number / port number
#      action:   <enable/no_enable/disable>
#
# OUT: SUCCESS/ERROR
#############################################################
proc IfQosMfClass {host if_type if_id action} {
   set prompt "CES\\(config-if\\)\#"
   set err_count [GetGlobalErr]

   EnterConfigIfLevel $if_type $if_id $host
   

   if {[string match -nocase "e*" $action]} {
      Exec "qos mf-class enable" $prompt $host 
   } elseif {[string match -nocase "no*" $action] || [string match -nocase "d*" $action]} {
      Exec "no qos mf-class enable" $prompt $host
   } else {
      ErrCheck "{ERROR: bad parameter: action = $action}"
   }
   
   return [CheckGlobalErr $err_count]
}


#############################################################
# IfQosMfClassEgress: Enable/Disable egress mf-class.                    
# 
# IN:  host:     (management IP) / (terminal server Ip:port)
#      if_type:  interface type in the format known by CES
#                     e.g. fast ethernet interface: FastEthernet
#                          wan interface:           serial
#      if_id:    <0-6>/<1-4>  slot number / port number
#      mf_class: name of classifier
#      disable:  <NULL/disable/no enable> 
#
# OUT: SUCCESS/ERROR
#############################################################
proc IfQosMfClassEgress {host if_type if_id mf_class {disable "NULL"}} {
   set prompt "CES\\(config-if\\)\#"
   set err_count [GetGlobalErr]

   EnterConfigIfLevel $if_type $if_id $host
   
   if {[string match -nocase "no*" $disable] || [string match -nocase "d*" $disable]} {
      Exec "no qos mf-class egress-mf-class" $prompt $host
   } elseif {$disable == "NULL"} {
      Exec "qos mf-class egress-mf-class $mf_class" $prompt $host
   } else {
      ErrCheck "{ERROR: bad parameter: disable = $disable}"
   }
   
   return [CheckGlobalErr $err_count]
}


#############################################################
# IfQosMfClassIngress: Enable/Disable ingress mf-class.   
# 
# IN:  host:     (management IP) / (terminal server Ip:port)
#      if_type:  interface type in the format known by CES
#                     e.g. fast ethernet interface: FastEthernet
#                          wan interface:           serial
#      if_id:    <0-6>/<1-4>  slot number / port number
#      mf_class: name of classifier
#      disable:  <NULL/disable/no enable>
#
# OUT: SUCCESS/ERROR
#############################################################
proc IfQosMfClassIngress {host if_type if_id mf_class {disable "NULL"}} {
   set prompt "CES\\(config-if\\)\#"
   set err_count [GetGlobalErr]

   EnterConfigIfLevel $if_type $if_id $host
   
   if {[string match -nocase "no*" $disable] || [string match -nocase "d*" $disable]} {
      Exec "no qos mf-class ingress-mf-class" $prompt $host
   } elseif {$disable == "NULL"} {
      Exec "qos mf-class ingress-mf-class $mf_class" $prompt $host
   } else {
      ErrCheck "{ERROR: bad parameter: disable = $disable}"
   }
   
   return [CheckGlobalErr $err_count]
}


#############################################################
# IfQosStatReset: Reset qos statistics on all qos counters.
#
# IN:  host:     (management IP) / (terminal server Ip:port)
#      if_type:  interface type in the format known by CES
#                     e.g. fast ethernet interface: FastEthernet
#                          wan interface:           serial
#      if_id:    <0-6>/<1-4>  slot number / port number 
# 
# OUT: SUCCESS/ERROR
#############################################################
proc IfQosStatReset {host if_type if_id} {
   set prompt "CES\\(config-if\\)\#"
   set err_count [GetGlobalErr]

   EnterConfigIfLevel $if_type $if_id $host
   Exec "qos statistics reset" $prompt $host

   return [CheckGlobalErr $err_count]
}


#############################################################
# IfQosEgressQueuingMode: Enable the entered queing mode.
#
# IN:  host:    (management IP) / (terminal server Ip:port)
#      if_type: interface type in the format known by CES
#                    e.g. fast ethernet interface: FastEthernet
#                         wan interface:           serial
#      if_id:   <0-6>/<1-4>  slot number / port number
#      q_mode:  <ds-phb/legacy> diffServ per hop queing mode or
#                               legacy forwarding priority mode
#
# OUT: SUCCESS/ERROR
#############################################################
proc IfQosEgressQueuingMode {host if_type if_id q_mode} {
   set prompt "CES\\(config-if\\)\#"
   set err_count [GetGlobalErr]

   EnterConfigIfLevel $if_type $if_id $host      
   Exec "qos egress-queuing-mode $q_mode" $prompt $host

   return [CheckGlobalErr $err_count]   
}


#############################################################
# ShowIfQosStat: Display qos statistics.
#                Return the output of 'show interface statistics'
#                CLI command.
#
# IN: host:    (management IP) / (terminal server Ip:port)
#     if_type: interface type in the format known by CES
#                    e.g. fast ethernet interface: FastEthernet
#                          wan interface:           serial
#     if_id:   <0-6>/<1-4>  slot number / port number
#
# OUT: ERROR/('show interface statistics' CLI command output)
#############################################################
proc ShowIfQosStat {host if_type if_id} {
   global cmdOut
   
   set prompt "CES\\(config-if\\)\#"
   set err_count [GetGlobalErr]

   EnterConfigIfLevel $if_type $if_id $host
   Exec "show qos statistics" $prompt $host

   if {[CheckGlobalErr $err_count] == "SUCCESS"} {
      return [cesLogsSetup $cmdOut]
   } else {
      return "ERROR"
   }   
}


#############################################################
# ParseIfQosStat: Gets different information from interface qos statistics
#                 These data will be available in the calling scope by the
#                 elements of $arr_rez_stat array
#                 
# Note: Support just for DiffServ queuing mode statistics.
#       Parse the data relating to 'Traffic Conditioning:' EF, AF1 - AF4
#       Parse
#       
#                 
# IN:  qos_stats:    interface qos statistics - returned by GetIfQosStat
#      data_group:   which group of information should be parsed from qos_stats
#                    supported values: 
#                        "Traffic Conditioning": parse the data relating to 
#                                                traffic conditionning
#                        "Queue": parse the data relating to interface queues.
#
#                                       
#      data_type:    which kind of data to get from the 'data_group'
#                    EF:        - get the statistics relating to EF queue
#                    AF1 - AF4: -        - || -                  AF1 - AF4 queue
#
#      arr_rez_stat: the name of an array which will be available in the calling
#                    scope after running ParseIfQosStat
#                    the indexes of this array are:
#                    - p_rec;
#                    - p_drop.
#                   
# 
# OUT: Nothing
# Modify variables: arr_stat_array
#
# Eq: Parse the data relating to EF from interface qos statistics
#     The ef_stat array will contain the results of this parsing.
#
# %ParseIfQosStat $qos_stat "Traffic Conditionning" "EF" ef_stat 
# %
# %puts $ef_stat(p_rec)
# %76
# %puts $ef_stat(p_drop)
# %0
#############################################################
proc ParseIfQosStat {qos_stats data_group data_type arr_rez_stat} {

   upvar $arr_rez_stat stat

   set line_buffer ""      
   set marked_line_no 99999
   set line_no 0

   set stat_lines ""

   # initialize the stat array
   foreach elem [array names stat] {
      unset stat($elem)
   }

   #Traffic Conditioning

   switch $data_group {

      "Traffic Conditioning" {         

         # group the data relating to each queue when split into many rows
         foreach line [split $qos_stats "\n"] {
            #puts $line
            incr line_no
            foreach mark {"EF*" "AF1*" "AF2*" "AF3*" "AF4*" "BE*" "*Interface Data Rate*"} {
               if {[string match $mark $line]} {
                  #puts "line = * $line *"
                  set marked_line_no $line_no
                  if {$line_buffer != ""} {               
                     lappend stat_lines $line_buffer
                  }
                  set line_buffer ""
                  break
               }
            }

            if {[regexp {Interface Data Rate} $line]} {
               set marked_line_no 99999
            }

            if {$line_no >= $marked_line_no} {
               set line_buffer "$line_buffer$line"         
               continue
            }
            
         }

         # now, get the date list required by info_to_get
         foreach elem $stat_lines {
            if {[regexp $info_to_get $elem]} {
               #puts $elem
               if {[regexp {Total Packets received=([0-9]+), dropped=([0-9]+)} $elem all rec drop]} {
                  #puts $rec
                  #puts $drop
                  set stat(p_rec) $rec
                  set stat(p_drop) $drop
               }         
            }
         }      
      }
      
      "Queue" {         
         foreach line [split $qos_stats "\n"] {
            incr line_no
            if {[string match "*Queue*" $line]} {

               set marked_line_no 99999

               switch $data_type {
                  "EF" {
                     #Expedited Forwarding
                     if {[regexp {Expedited Forwarding} $line]} {                        
                        set marked_line_no $line_no                        
                        continue
                     }
                  }
                  "AF1" {
                     #Assured Forwarding 1
                     if {[regexp {Assured Forwarding 1} $line]} {
                        set marked_line_no $line_no
                        continue
                     }
                  }
                  "AF2" {
                     #Assured Forwarding 2
                     if {[regexp {Assured Forwarding 2} $line]} {
                        set marked_line_no $line_no
                        continue
                     }
                  }
                  "AF3" {
                     #Assured Forwarding 3
                     if {[regexp {Assured Forwarding 3} $line]} {
                        set marked_line_no $line_no
                        continue
                     }
                  }
                  "AF4" {
                     #Assured Forwarding 4
                     if {[regexp {Assured Forwarding 4} $line]} {
                        set marked_line_no $line_no
                        continue
                     }
                  }
                  "BE" {
                     #Best Effort
                     if {[regexp {Best Effort} $line]} {
                        set marked_line_no $line_no
                        continue
                     }                     
                  }
               }
            }
            
            if {$line_no > $marked_line_no} {
               puts $line
               if {[regexp {pktReceived=([0-9]+)} $line all rec]} {
                  set stat(p_rec) $rec
                  continue
               } 
               if {[regexp {pktDropped=([0-9]+)} $line all drop]} {
                  set stat(p_drop) $drop
                  continue
               }
            }               
         }                             
      }
   }; #end switch data_group

   # set 'NULL' the elements of the array which were not set above
   foreach id {p_rec p_drop} {
      if {[info exists stat($id)] == 0} {
         set stat($id) "NULL"
      }
   }

}
