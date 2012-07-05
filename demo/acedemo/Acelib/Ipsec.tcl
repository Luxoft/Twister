##############################
# Ipsec library
# 
# This file contains the Acelib procedures relating to Ipsec CLI commands
#
# 
# Procedures:
#
# EnaIpsecEncrType {host encryptType}
# DisIpsecEncrType {host encryptType}
# EnaIpsecIkeEncrType {host encryptType}
# DisIpsecIkeEncrType {host encryptType}
# 
##############################

proc EnaIpsecEncrType {host encryptType} {
   
   global cmdOut
   set cmdOut ""
   set encrList ""
   
   set err_count [GetGlobalErr]
   
   SetCliLevel "CONFIG" $host
   
   if {$encryptType == "all" } {
      Exec "ipsec encryption ?" "CES\\(config\\)\#ipsec encryption " $host 0 20 0
      foreach line [split $cmdOut "\n"] {
         if {[regexp -nocase {^[\r\t ]+([a-zA-Z0-9\-]+)[\t ]+.*} $line all encrType] == 1 &&\
                 $encrType != "ike"} {
            lappend encrList $encrType 
         }
      }
      
      Exec "[lindex $encrList 0]" "CONFIG" $host
      for {set i 1} {$i < [llength $encrList]} {incr i} {
         Exec "ipsec encryption [lindex $encrList $i]" "CONFIG" $host
      }

   } else {
      Exec "ipsec encryption $encryptType" "CONFIG" $host
   }

   return [CheckGlobalErr $err_count]
}

proc DisIpsecEncrType {host encryptType} {
   
   global cmdOut
   set cmdOut ""
   set encrList ""
   
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host  

   if {$encryptType == "all" } {
      Exec "no ipsec encryption ?" "CES\\(config\\)\#no ipsec encryption " $host 0 20 0
      foreach line [split $cmdOut "\n"] {
         if {[regexp -nocase {^[\r\t ]+([a-zA-Z0-9\-]+)[\t ]+.*} $line all encrType] == 1 &&\
                 $encrType != "ike"} {
            lappend encrList $encrType 
         }
      }
      
      Exec "[lindex $encrList 0]" "CONFIG" $host
      for {set i 1} {$i < [llength $encrList]} {incr i} {
         Exec "no ipsec encryption [lindex $encrList $i]" "CONFIG" $host
      }

   } else {
      Exec "no ipsec encryption $encryptType" "CONFIG" $host
   }

   #Exec "show ipsec" "CONFIG" $host
   return [CheckGlobalErr $err_count]
}

proc EnaIpsecIkeEncrType {host encryptType} {
   
   global cmdOut
   set cmdOut ""
   set encrList ""
   
   set err_count [GetGlobalErr]
   
   SetCliLevel "CONFIG" $host
   
   if {$encryptType == "all" } {
      Exec "ipsec encryption ike ?" "CES\\(config\\)\#ipsec encryption ike " $host 0 20 0
      foreach line [split $cmdOut "\n"] {
         if {[regexp -nocase {^[\r\t ]+([a-zA-Z0-9\-]+)[\t ]+.*} $line all encrType] == 1} {
            lappend encrList $encrType 
         }
      } 
      
      Exec "[lindex $encrList 0]" "CONFIG" $host
      for {set i 1} {$i < [llength $encrList]} {incr i} {
         Exec "ipsec encryption ike [lindex $encrList $i]" "CONFIG" $host
      }
      
   } else {
      Exec "ipsec encryption ike $encryptType" "CONFIG" $host
   }

   return [CheckGlobalErr $err_count]
}

proc DisIpsecIkeEncrType {host encryptType} {
   
   global cmdOut
   set cmdOut ""
   set encrList ""
   
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   
   Exec "no ipsec encryption ike $encryptType" "CONFIG" $host

   return [CheckGlobalErr $err_count]
}

