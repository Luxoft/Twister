############################################################
# Library procedures relating to L2F service setup
#
# L2fNasUid {}
# L2fAuth {}
#
############################################################

proc L2fAddNasUid {host uid passwd switch_uid passwd} {

   global cmdOut
   
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host

   Exec "l2f nas-uid add $uid password $passwd switch-uid $switch_uid password $passwd" "CONFIG" $host

   return [CheckGlobalErr $err_count]
}


proc L2fAuth {host auth_method} {
   set err_count [GetGlobalErr]

   SetCliLevel "CONFIG" $host
   
   switch -- $auth_method {
      "chap" {
         Exec "l2f authentication $auth_method" "CONFIG" $host
      }
      "pap" {
         Exec "l2f authentication $auth_method" "CONFIG" $host
      }
      "no_chap" {
         Exec "no l2f authentication chap" "CONFIG" $host
      }
      "no_pap" {
         Exec "no l2f authentication pap" "CONFIG" $host
      }
   }
  
   return [CheckGlobalErr $err_count]
}
