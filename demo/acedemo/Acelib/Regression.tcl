#############################################################
# Procedures regarding automated regression based on ace.
#
# RegCleanup {suiteName}
#############################################################

#############################################################
# RegCleanup: Reset all the duts got with getRegDuts proc from
#             textlib.tcl (the DUTs declared in reg_duts.txt file)
#             The proc returns without reset if the global variable
#             regression is "NO"
#
#             This global variable is set default to "NO"
#             The execution engine sets it to "YES" if "-r" option 
#             is used in the command line.
#
# |||||||||| add more comments ! -------------------------
#
#############################################################
proc RegCleanup {suite} {
   global auto_reg
   
   if {$auto_reg != "YES"} {
      return
   }

   set reg_duts [getRegDuts]
   if {$reg_duts == "ERROR"} {
      # cause the test suite to be SKIPPED        
      error "SKIPP test suite $suite. Configuration file problem"
   }
   
   set err_count [GetGlobalErr]
   
   MultiResetSwitchFact [getRegDuts]
   Disconnect "all"   

   # wait some time before reconnect
   sleep 5

   if {[CheckGlobalErr $err_count] == "ERROR"} {
      error "SKIPP test suite $suite. DUTs connection problems"
   }
}
