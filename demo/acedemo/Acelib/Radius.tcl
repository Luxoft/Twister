######################################################
# Library procedures for RADIUS settings - CLI:
# RadiusServiceState { host state }
# EnableRadiusService { host }
# DisableRadiusService { host }
# RadiusDefaultClientPass { host password }
# RadiusDefaultClientState { host state }
# RadiusServerAuth { host type state }
# RadiusServerPrimaryState { host state }
# RadiusServerPrimaryHost { host ip_addr port }
# RadiusServerPrimaryInterface { host ifType if_addr }
# RadiusServerPrimaryKey { host key }
#######################################################

####################################################
# RadiusServiceState: Enable/Disable RADIUS globally
#
# IN:  host:  (management IP)/(terminal server Ip:port)
#      state: enable/disable
#
# OUT: SUCCESS/ERROR
####################################################
proc RadiusServiceState { host state } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   
   if { $state == "disable" } {
      Exec "radius service" "CONFIG" $host
   } else {
      Exec "no radius service" "CONFIG" $host
   }

   return [CheckGlobalErr $err_count]
}

####################################################
# EnableRadiusService: allow RADIUS as private/public service
#
# IN:  host:  (management IP)/(terminal server Ip:port)
#      state: public/private
#
# OUT: SUCCESS/ERROR
####################################################
proc EnableRadiusService { host state } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   
   if { $state == "public" } {
      Exec "ip radius source-interface public" "CONFIG" $host
   } else {
      Exec "ip radius source-interface private" "CONFIG" $host
   }

   return [CheckGlobalErr $err_count]

}

####################################################
# DisableRadiusService: deny RADIUS as private/public service
#
# IN:  host:  (management IP)/(terminal server Ip:port)
#      state: public/private
#
# OUT: SUCCESS/ERROR
####################################################
proc DisableRadiusService { host state } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   
   if { $state == "public" } {
      Exec "no ip radius source-interface public" "CONFIG" $host
   } else {
      Exec "no ip radius source-interface private" "CONFIG" $host
   }
   
   return [CheckGlobalErr $err_count]
}

####################################################
# RadiusDefaultClientPass: sets the password for default client
#
# IN:  host:     (management IP)/(terminal server Ip:port)
#      password: password
#
# OUT: SUCCESS/ERROR
#################################################### 
proc RadiusDefaultClientPass { host password } {
   set err_count [GetGlobalErr]
   SetCliLevel "CONFIG" $host
   Exec "radius-client default-client password $password" "CONFIG" $host
   return [CheckGlobalErr $err_count]
}

####################################################
# RadiusDefaultClientState: sets the defaul-client feature state for RADIUS server
#
# IN:  host:     (management IP)/(terminal server Ip:port)
#      state:    <enable/disable>
#
# OUT: SUCCESS/ERROR
#################################################### 
proc RadiusDefaultClientState { host state } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   
   if { $state == "enable" } {
      Exec "radius-client default-client enabled" "CONFIG" $host
   } else {
      Exec "radius-client default-client disabled" "CONFIG" $host
   }
   
   return [CheckGlobalErr $err_count]
}

####################################################
# RadiusServerAuth: sets the auth proto for RADIUS client
#
# IN:  host:  (management IP)/(terminal server Ip:port)
#      type:  <chap/mschap/pap/response>
#      state: <enable/disable> 
#
# OUT: SUCCESS/ERROR
#################################################### 
proc RadiusServerAuth { host type state } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   
   if { $state == "enable" } {
      Exec "radius-server authentication $type" "CONFIG" $host
   } else {
      Exec "no radius-server authentication $type" "CONFIG" $host
   }
   
   return [CheckGlobalErr $err_count]
}

####################################################
# RadiusServerPrimaryState: sets the state for primary server
#
# IN:  host:  (management IP)/(terminal server Ip:port)
#      state: <enable/disable> 
#
# OUT: SUCCESS/ERROR
#################################################### 
proc RadiusServerPrimaryState { host state } {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   
   if { $state == "enable" } {
      Exec "radius-server primary enabled" "CONFIG" $host
   } else {
      Exec "radius-server primary disabled" "CONFIG" $host
   }

   return [CheckGlobalErr $err_count]
}

####################################################
# RadiusServerPrimaryHost: sets the ip address of the primary server
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      ip_addr: ip address
#      port:    port
#
# OUT: SUCCESS/ERROR
#################################################### 
proc RadiusServerPrimaryHost { host ip_addr {port "1645"} } {
   set err_count [GetGlobalErr]
   SetCliLevel "CONFIG" $host
   Exec "radius-server primary host $ip_addr auth-port $port" "CONFIG" $host
   return [CheckGlobalErr $err_count]

}

####################################################
# RadiusServerPrimaryInterface: sets the interface that perform the request to server
#
# IN:  host:    (management IP)/(terminal server Ip:port)
#      ifType:    <public/private>
#      if_addr: ip address
#
# OUT: SUCCESS/ERROR
####################################################
proc RadiusServerPrimaryInterface { host ifType if_addr } {
   set err_count [GetGlobalErr]
   SetCliLevel "CONFIG" $host
   Exec "radius-server primary interface $ifType $if_addr" "CONFIG" $host
   return [CheckGlobalErr $err_count]

}

####################################################
# RadiusServerPrimaryKey: sets the password for client
#
# IN:  host: (management IP)/(terminal server Ip:port)
#      key:  password
#
# OUT: SUCCESS/ERROR
#################################################### 
proc RadiusServerPrimaryKey { host key } {
   set err_count [GetGlobalErr]
   SetCliLevel "CONFIG" $host
   Exec "radius-server primary key $key" "CONFIG" $host
   return [CheckGlobalErr $err_count]
}


