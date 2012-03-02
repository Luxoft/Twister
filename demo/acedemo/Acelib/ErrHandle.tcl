###########################################################################
# Procedures used to handle test lib errors.
#
# Error handling mechanism. 
#
# A. Single error handling
#    
#    Single errors appear when a single action fails. 
#    Error handling mechanism throws error messages for each
#    single error and increments a global variable (testlib_error).
#
#    Single error example: 
#           fail to Exec cli command on DUT
#           fail to Connect to DUT
#           ...                 
#
#    Library procedures:  
#    - ErrCheck: this procedure should be called at the end of each Acelib procedure 
#                that does a single action.
#                E.q.
#                Exec procedure calls ErrCheck in order to report the result.
#
# B. Multiple error handling
# 
#    A multiple error is a group or single errors.
#    Multiple error appears into a complex procedure that
#    atempts to execute many single and/or complex actions.
#
#    Each single error is handled individualy. 
#    A complex procedure fails if any of the single actions
#    called by it fails.
#    The complex procedure verifies at the begining how many
#    errors are up to that moment - read testlib_error global 
#    variable.
#    At the end of complex procedure, the errors number is 
#    read again and compared with the initial number of errors.
#    If final_error_number > initial_error_number -> procedure failed
#    
#    Library procedurds:
#    - GetGlobalErr
#    - CheckGlobalErr
#
#
# C. Example of how to write a Acelib procedures with error handling.
#
#    Error handling for single errors is included basic Acelib procedures (Connect, Exec ...)
#    procedures.
#
#    Example of complex Acelib procedure with error handling:
#
#    proc Complex {} {
#
#       set err_count [GetGlobalErr]
#       
#       <run simple proc1>
#
#       <run simple proc2>
#
#       <run complex proc N>
#
#       ...
#
#       return [CheckGlobalErr $err_count]
#    } 
#
# ACELIB ERRORS TRACKING. 
#
# This Aceib feature is useful for the case when there 
# are more errors in a complex procedure and you need
# to access a particular one.
#                         
# testlib_error_info: an array global variable used to hold an history of
#                    Acelib errors.
#                    The ErrCheck uses this variable as a STAK for
#                    keeping the track of the last MAXHISTORY Acelib errors.
#                    The acelib_error_info entry with the index 1 is the
#                    newest acelib error.
#                    For each new Acelib error the index of the existing
#                    entries in the Stack is increased. The last entry is 
#                    dropped.
#                    The elements of acelib_error_info contain information
#                    about the procedure that failed and the failure cause.
# 
# MAXHISTORY:        A global variable that gives the size of the Acelib 
#                    errors history.
#                    Default value is 5.
#                    It is initialized in GlobVar.tcl file.
#
# The history mechanism in implemented in ErrCheck procedure.
#
#                   
# 
# Procedures:
#     ErrCheck {rcode callingFunction {returnTheValue "FALSE"}}
#     GetGlobalErr {}
#     CheckGlobalErr {err_count}
#
#
###########################################################################



###########################################################################
# ErrCheck - Procedure for handling simple errors.
#            Parses rcode message and if error:
#            - send error messages in log files;
#            - increment testlib_error global variable.
#
#            Contains the Acelib error tracking mechanism.
#            Up to 5 Acelib error messages are stored in testlib_error_info
#            global variable.            
#
# IN:  rcode             - string to parse
#      Obsolated parameters. NOT USE THEM ANYMORE. 
#          callingFunction   - procedure from which ErrCheck was called                              
#          returnTheValue    - return or not rcode (accepted values: TRUE, FALSE)
#
# OUT: SUCCESS
#      ERROR
#      rcode
#
# NOTE: need to review the error messages!
#
###########################################################################
proc ErrCheck {rcode {callingFunction ""} {returnTheValue "FALSE"}} {
   
   global testlib_error
   global testlib_error_info
   global MAXHISTORY

   set running_log 0
   
   set callingFunction [info level -1]
   
   if {[string match "*ERR*" $rcode] == 1} {
      set listLen [llength $rcode]
      
      incr testlib_error
      
      set dbg "\"$callingFunction\": FAILED.\n"
      
      for {set count 0} {$count < $listLen} {incr count} {
         if {[string match "*ERR*" [lindex $rcode $count]] == 1} {
            
            append dbg [lindex $rcode $count] "\n"
            
         }
      }
      
      # format dbg message
      set dbg [cesLogsSetup $dbg]
      #puts "ErrCheck dbg: $dbg"
      LogFile "ACELIB_ERROR: $dbg"
      logCliFile "\nACELIB_ERROR: $dbg"
      
      # Acelib error history (acelib error tracking mechanism)
      # Move backwords the existing entries in testlib_error_info
      
      foreach elem [lsort -decreasing [array names testlib_error_info]] {
         if {$elem >= $MAXHISTORY} {
            unset testlib_error_info($elem)
         } else {
            set new_index [expr $elem + 1]
            set testlib_error_info($new_index) $testlib_error_info($elem)
         }
      }
      set testlib_error_info(1) [list ACELIB_ERROR: $dbg]
                  
      return "ERROR"

   } elseif {$returnTheValue == "TRUE"} {
      return $rcode

   } else {
      return "SUCCESS"
   }
}

##########################################
# GetGlobalErr: Used by Multiple error handling mechanism.
#               Returns the current number of errors.
# 
# IN:
#
# OUT: testlib_error (global variable)
#
##########################################
proc GetGlobalErr {} {
   global testlib_error          
   return $testlib_error
}

##########################################
# CheckGlobalErr: Used by Multiple error handling mechanism.
#                 Compares the current value of testlib_error
#                 with a value got previously.
#                 Decides if failed actions between moment 0 - read first time the testlib_error
#                 and moment 1 - read testlib_error second time.
#
#
# IN: err_count: a number representing the errors count to which to compare the current 
#                value of testlib_error
#
# OUT: SUCCESS
#      ERROR
#
##########################################
proc CheckGlobalErr {err_count {log "NO"}} {

   global testlib_error

   if {$testlib_error > $err_count} {
      # message
      if {$log != "NO"} {
         LogFile "ACELIB_ERROR while running [info level -1]"
      }
      return "ERROR"
   } elseif {$testlib_error == $err_count} {
      return "SUCCESS"
   }

}
