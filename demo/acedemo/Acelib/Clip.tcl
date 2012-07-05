######################################################
# Library procedures for CLIP settings - CLI:  CES(config)#clip ...
# ClipGlobalState {host state}
# ClipIpAdd {host ipaddr}
# ClipIpDel {host ipaddr}
# ClipIpIfType {host ipaddr iftype}
# ClipIpState {host ipaddr state}
# ClipIpServices {host ipaddr service interface}
#######################################################

####################################################
# ClipGlobalState: Enable/Disable CLIP globally
#
# IN:  host:  (management IP)/(terminal server Ip:port)
#      state: enable/disable
#
# OUT: SUCCESS/ERROR
####################################################
proc ClipGlobalState { host state } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   
   if { $state == "disable" } {
      Exec "no clip enable" "CONFIG" $host
   } else {
      Exec "clip $state" "CONFIG" $host
   }

   return [CheckGlobalErr $err_count]
      
}   


####################################################
# ClipIpAdd {host ipaddr}: Add a CLIP address to switch
#
# IN:  host:   (management IP)/(terminal server Ip:port)
#      ipaddr: CLIP ip address
#
# OUT: SUCCESS/ERROR
####################################################
proc ClipIpAdd { host ipaddr } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   
   Exec "clip ip $ipaddr" "CONFIG" $host

   return [CheckGlobalErr $err_count]
   
}



####################################################
# ClipIpDel {host ipaddr}: Delete a CLIP address from switch
#
# IN:  host:   (management IP)/(terminal server Ip:port)
#      ipaddr: CLIP ip address
#
# OUT: SUCCESS/ERROR
####################################################
proc ClipIpDel { host ipaddr } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   
   Exec "no clip ip $ipaddr" "CONFIG" $host

   return [CheckGlobalErr $err_count]
}



#################################################
# ClipIpIfType {host ipaddr iftype}: Sets the type of CLIP address (private/public)
#
# IN:  host:   (management IP)/(terminal server Ip:port)
#      ipaddr:     CLIP ip address
#      iftype: private/public/both/none
#
# OUT: SUCCESS/ERRORR
##################################################
proc ClipIpIfType { host ipaddr iftype } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host

   Exec "clip ip $ipaddr interface-type $iftype" "CONFIG" $host

   return [CheckGlobalErr $err_count]
}



####################################################
# ClipIpState { host ipaddr state }: sets the state of CLIP address (enable/disable)
#
# IN:  host:   (management IP)/(terminal server Ip:port)
#      ipaddr: CLIP ip address
#      state:  enable/disable
#
# OUT: SUCCESS/ERROR
##################################################### 
proc ClipIpState { host ipaddr state } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host

   Exec "clip ip $ipaddr state $state" "CONFIG" $host

   return [CheckGlobalErr $err_count]   
}


#####################################################
# ClipIpServices { host ipaddr service iftype }: sets the allowed services on CLIP interface
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      ipaddr:  CLIP ip address
#      service: ipsec/pptp/l2tp/fwua
#      iftype   private/public/both/none
#
# OUT: SUCCESS/ERROR
#####################################################
proc ClipIpServices { host ipaddr service iftype } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host

   Exec "clip ip $ipaddr services $service $iftype" "CONFIG" $host

   return [CheckGlobalErr $err_count]   
}
