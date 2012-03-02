############################################################################
#  This file, Scotty.tcl is a collection of functions used to send SNMP    #
#  commands to a host switch using the Scotty extension.  Most of the      #
#  functions are only used within this file for error checking purposes    #
#  and are not meant for public use.  The functions that are for public    #
#  use are listed below:                                                   #
#                                                                          #
#     scotty {action command host {checkErr ALL} {timeout 5}}              #
#     ScottyGetNext {curCommand host}                                      #
#     ErrCheck {rcode callingFunction {returnTheValue "FALSE"}}            #
#     DumpStackTrace {}                                                    #
#                                                                          #
#  For more detail on each function, see the comments above the function.  #
#  All functions included in this file work with devices that use SNMP.    #
#                                                                          #
############################################################################


proc {ScottyVer} {} {
   set ver 1.3
   LogFile "Scotty version $ver"
   return "$ver"
}



############################################################################
#  Procedure scotty takes in the necessary parameters to make an SNMP MIB  #
#  call to the specified switch.  For set actions, the procedure will      #
#  check return codes and make get checks to verify that the set worked.   #
#  The level of error checking depends on the parameter checkErr.  For     #
#  get actions, the procedure will return ERRNORESPONSE or will return the #
#  mib value returned by the switch.                                       #
#                                                                          #
#  Variables                                                               #
#    IN:                                                                   #
#         action:       String spectifying the SNMP action (set/get)       #
#         command:      String specifying the MIB objects and any          #
#                       parameters being assigned to that object           #
#         host:         IP address of the switch or list containing the    #
#                       IP address of the switch, the read community       #
#                       string, and the write community string in this     #
#                       order.  If this variable is only the IP address    #
#                       of the switch, the read and write communities must #
#                       be globally set in the variables readcommunity and #
#                       writecommunity.                                    #
#         checkErr:     String specifying the level of error checking to   #
#                       do (all/set/none).  The level "set" will verify    #
#                       that the parameter set to the mib object equals    #
#                       the return value from the call.  The level "all"   #
#                       will verify the return value from the set, and     #
#                       then perform a get to ensure that the switch       #
#                       reports the change.  Level "none" executes the     #
#                       MIB call and then returns SUCCESS regardless of    #
#                       the resulting return codes.  These error code      #
#                       levels have no effect on SNMP get requests.        #
#                                                                          #
#    OUT:                                                                  #
#         Function returns the following error codes for "set" actions:    #
#                                                                          #
#         ERRNOSUCHNAME             MIB value does not exist or is not set #
#         ERRSETDOESNOTMATCH        Return code did not match value MIB    #
#                                   being assigned                         #
#         ERRGETDOESNOTMATCH        Return code from set matched, but the  #
#                                   return code from the get did not match #
#         ERRSETANDGETDONOTMATCH    Return code from both set and get did  #
#                                   did not match                          #
#         ERRGETCHECKFAILED         The get call following the set failed  #
#         ERRBADACTION              The action was not "set" or "get"      #
#         ERRNORESPONSE             There was no response                  #
#         ERRBADRCODE               The variable rcode did not get set,    #
#                                   so this indicates a programming error  #
#         SUCCESS                   There were no errors encountered or    #
#                                   the error check level was set to none  #
#                                                                          #
#         Function returns the following error codes for "get" actions:    #
#                                                                          #
#         ERRNORESPONSE             There was no response                  #
#         <return value>            The value of the mib returned by the   #
#                                   switch                                 #
#                                                                          #
#  Bugs:  Cannot switch MIBs transparently, so tools that use this         #
#         function can only configure one switch type per wish instance.   #
#                                                                          #
############################################################################

proc scotty {action command host {checkErr ALL} {timeout 5}} {
   global noResponseCount

   set rcode SUCCESS

   set action [string toupper $action]
   if {$checkErr != "ALL" && $checkErr != "SET" && $checkErr != "NONE"} {
      set checkErr ALL
   }

   set resetErrorLogFlag FALSE
   set count 0
   set maxLoops 3
   while {$count < $maxLoops} {
      if {$action == "SET"} {
         catch {ScottySet $command $host $timeout} setResult 
         if {$checkErr == "NONE"} {
            CleanUpSNMPSessions
            return SUCCESS
         }
         set rcode [CheckScottySetResults $command $setResult $checkErr $timeout $host]
         set count $maxLoops
      } elseif {$action == "GET"} {
         set startTime [clock seconds]
         catch {ScottyGet $command $host $timeout} getResult 
         set endTime [clock seconds]
         set totalTime [expr $endTime - $startTime]
         if {$getResult == "" && $totalTime >= 5} {
            set getResult noResponse
            set rcode ERRNORESPONSE
            incr count
            DisableGlobalErrorLogging
            set resetErrorLogFlag TRUE
         } elseif {$getResult == "" && $totalTime < 5} {
            set rcode ""
            set count $maxLoops
         } elseif {$getResult == "noSuchName"} {
            set rcode ERRORNOSUCHNAME
            set count $maxLoops
	    if {[catch {mib name $command} str] == 0} {
               LogFile "scotty: Error - The mib used in the get is invalid or not configured (noSuchName).  command=[mib name $command], getResult=$getResult, host info=$host" ERROR
            } else {
               LogFile "scotty: Error - The mib used in the get is invalid or not configured (noSuchName).  command=$command, getResult=$getResult, host info=$host" ERROR
            }
         } elseif {[string match "*invalid object identifier*" $getResult] == 1} {
            set rcode ERRORINVALIDMIB
            set count $maxLoops
	    if {[catch {mib name $command} str] == 0} {
               LogFile "scotty: Error - The mib used in the get is invalid or not configured.  command=[mib name $command], getResult=$getResult, host info=$host" ERROR
            } else {
               LogFile "scotty: Error - The mib used in the get is invalid or not configured.  command=$command, getResult=$getResult, host info=$host" ERROR
            }
         } else {
            set rcode $getResult
            set count $maxLoops
         }
      } else {
         LogFile "scotty: Error - Incorrect action: $action.  Use either \"SET\" or \"GET\"" ERROR
         set rcode ERRBADACTION
         set count $maxLoops
      }
   }

   if {$resetErrorLogFlag == "TRUE"} {
      EnableGlobalErrorLogging
   }

   CleanUpSNMPSessions
   if {$rcode == "ERRNORESPONSE" && $action == "get"} {
      LogFile "scotty: Error - The get request timed out.  command=[mib name $command], getResult=$getResult, host info=$host" ERROR
   }
   if {[string match "*ERR*" $rcode] == 1} {
      LogFile "scotty: Calling stack dump because of error $rcode" DEBUG
      DumpStackTrace
   }
   if {[string match "*ERRNORESPONSE*" $rcode] == 1 && [IsSwitchAlive $host] == "FALSE"} {
      if {[info exists noResponseCount] == 1 && $noResponseCount >= 5} {
         LogFile "The switch $host can not be reached!" ERROR
         exit
      } else {
         if {[info exists noResponseCount] == 0} {
            set noResponseCount 1
         } else {
            incr noResponseCount
         }
      }
   } else {
      set noResponseCount 0
   }
   return $rcode
}

proc CheckScottySetResults {command result checkErr timeout host} {
   if {$result == "ERRORODDNUMPARAMETERS" || $result == "ERRORUNDEFINEDCOMMUNITIES"} {
      return $result
   }
   set len [expr [llength $command] / 2]
   set i 0
   set rcodeList ""
   while {$i < $len} {
      set setResult [lindex $result $i]
      set setCommand [lindex $command [expr $i * 2]]
      set expected [lindex $command [expr ($i * 2) + 1]]
      if {$setResult == "invalid" && [string match "*invalid object identifier*" $result] == 1} {
         set badmib [FindBadMibCall $command $timeout $host]
         LogFile "scotty: Error - The mib being set is invalid.  setCommand=$badmib, setResult=$result, host info=$host" ERROR
         set rcode ERRINVALIDMIB
         set setResult $rcode
         # When an error of this nature occurs, there are no successful results, only the one failure.
         set i $len
      }
      if {$setResult == "noSuchName"} {
         set badmib [FindBadMibCall $command $timeout $host]
         LogFile "scotty: Error - The mib being set is invalid (noSuchName).  setCommand=$badmib, setResult=$setResult, host info=$host" ERROR
         set rcode ERRNOSUCHNAME
         set setResult $rcode
         # When an error of this nature occurs, there are no successful results, only the one failure.
         set i $len
      }
      if {$setResult == "badValue"} {
         set badmib [FindBadMibCall $command $timeout $host]
         LogFile "scotty: Error - The value being configured is invalid.  command=$badmib, result=$result, host info=$host" ERROR
         set rcode ERRBADVALUE
         set setResult $rcode
         # When an error of this nature occurs, there are no successful results, only the one failure.
         set i $len
      }
      if {[string match "*expected*" $setResult] == 1} {
         set setNextResult "[lindex $result [expr $i + 2]] [lindex $result [expr $i+ 3]]"
         set resultErrLen [llength $result]
         if {[string match "*but got*" $setNextResult] == 1} {
            set badmib [FindBadMibCall $command $timeout $host]
            LogFile "scotty: Error - The type of the value being configured is invalid.  setCommand=$badmib, result=$result, host info=$host" ERROR
            set rcode ERRBADPARAMETER
            set setResult $rcode
            # When an error of this nature occurs, there are no successful results, only the one failure.
            set i $len
         }
      }
      if {$setResult == "" && $expected != ""} {
         set setResult [ScottySet "$setCommand $expected" $host $timeout]
         if {$setResult == "" && $expected != ""} {
            set setResult [ScottySetRaw "$setCommand $expected" $host]
            if {$setResult == "noResponse"} {
               set rcode ERRNORESPONSE
               set setResult $rcode
               LogFile "scotty: Error - The set attempt timed out.  setCommand=[mib name $setCommand], host info=$host" ERROR
            }
         }
      }
      if {[string match "*ERR*" $setResult] != 1 && $setResult != "noResponse" && $setResult != "badValue"} {
         # None of the standard SNMP errors occurred, so check to see whether the return value equals the value being set
         if {$setResult == $expected} {
            set rcode SUCCESS
         } else {
            # Checking all possible integers mapped to corresponding strings with the string that was returned (apply = 2)
            set possibleMibResults [lindex [mib -exact tc [lindex [split $setCommand .] 0]] 3]
            set rcode ""
            foreach possibleMibResult $possibleMibResults {
               if {[lsearch $possibleMibResult $setResult] != -1 && [lsearch $possibleMibResult $expected] != -1} { 
                  set rcode SUCCESS
               }
            }
	    if {$rcode != "SUCCESS"} {
               # Checking to see whether the strings match but have different case (00:34:ff:24:ab:01 == 00:34:FF:24:AB:01)
               if {[string toupper $expected] == [string toupper $setResult]} {
                  set rcode SUCCESS
               } else {
                  LogFile "scotty: Error - The set mib call [mib name $setCommand] did not return the expected value.  Set result=$setResult, expected result=$expected, host info=$host" ERROR
                  set rcode ERRSETDOESNOTMATCH
               }
            }
         }
         if {$checkErr == "ALL"} {
            set getCommand $setCommand
            catch {ScottyGet $getCommand $host $timeout} getResult
            if {[string match "*invalid object identifier*" $getResult] == 1 || [string match "*ERR*" $getResult] == 1} {
               LogFile "scotty: Error - The command scotty issued returned an error.  getCommand=[mib name $getCommand], getResult=$getResult, host info=$host" ERROR
               set rcode ERRGETCHECKFAILED
            } else {
               if {[string toupper $expected] == [string toupper $getResult] && $rcode != "ERRSETDOESNOTMATCH"} {
                  set rcode SUCCESS
               } elseif {$getResult == $expected && $rcode == "ERRSETDOESNOTMATCH"} {
                  set rcode ERRSETFAILEDGETSUCCEEDED
               } elseif {$rcode != "ERRSETDOESNOTMATCH"} {
                  LogFile "scotty: Error - Result from the Set does not match the result from the Get!  getCommand=$getCommand, getResult=$getResult, expected=$expected, host info=$host" ERROR
                  set rcode ERRGETDOESNOTMATCH
               }
            }
         }
      }
      lappend rcodeList $rcode
      incr i
   }

   # When an error of this nature occurs, there are no successful results, only the one failure.
   if {$rcode == "ERRBADPARAMETER" || $rcode == "ERRBADVALUE" || $rcode == "ERRNOSUCHNAME"} {
      for {set i [llength $rcodeList]} {$i < $len} {incr i} {
         lappend rcodeList $rcode
      }
   }
   return $rcodeList
}


############################################################################
#  Procedure FindBadMibCall takes in the list of commands and will execute #
#  each MIB call individually to determine which MIB call errored out.     #
#  The MIBs that errored out are returned.  Ideally, this function should  #
#  not be used except by calls from the procedure "scotty".                #
#                                                                          #
#  Variables                                                               #
#    IN:                                                                   #
#         command:      String list specifying the MIB objects             #
#         timeout:      Integer specifying time to wait for a response     #
#         host:         IP address of the switch or list containing the    #
#                       IP address of the switch, the read community       #
#                       string, and the write community string in this     #
#                       order.  If this variable is only the IP address    #
#                       of the switch, the read and write communities must #
#                       be globally set in the variables readcommunity and #
#                       writecommunity.                                    #
#                                                                          #
#    OUT:                                                                  #
#         Due to limitations not yet overcome, the function will only      #
#         return the value of the MIB returned by the switch.  If an       #
#         error occurs, there is no way to return the error back to the    #
#         calling function.                                                #
#                                                                          #
#  Bugs:  Limited error checking and inablility to return error codes.     #
#                                                                          #
############################################################################

proc FindBadMibCall {command timeout host} {
   set i 0
   set len [expr [llength $command]/2]

   set badmibs ""
   while {$i < $len} {
      set setCommand "[lindex $command [expr $i * 2]] [lindex $command [expr ($i * 2) + 1]]"
      catch {ScottySet $setCommand $host $timeout} setResult 
      if {$setResult == "noSuchName" || $setResult == "noResponse" || $setResult == "badValue" || [string match "*expected*" $setResult] == 1} {
         lappend badmibs "[mib name [lindex $setCommand 0]] [lindex $setCommand 1] $setResult"
      } elseif {[string match "*invalid object identifier*" $setResult] == 1} {
         lappend badmibs "[lindex $setCommand 0] [lindex $setCommand 1] $setResult"
      }
      incr i
   }
   return $badmibs
}


############################################################################
#  Procedure ScottyGet takes in the necessary parameters to make an SNMP   #
#  MIB call to the specified switch.  The session is setup, the command    #
#  executed, and the session is torn down.  Ideally, this function should  #
#  not be used except by calls from the procedure "scotty".  If it is ever #
#  possible to switch MIBs in the background, there needs to be a locking  #
#  mechanism to prevent one process from switching MIBs while another      #
#  process is using them.  The function "scotty" takes care of this, but   #
#  this function does not.                                                 #
#                                                                          #
#  Variables                                                               #
#    IN:                                                                   #
#         command:      String specifying the MIB object                   #
#         host:         IP address of the switch or list containing the    #
#                       IP address of the switch, the read community       #
#                       string, and the write community string in this     #
#                       order.  If this variable is only the IP address    #
#                       of the switch, the read and write communities must #
#                       be globally set in the variables readcommunity and #
#                       writecommunity.                                    #
#         timeout:      Integer specifying time to wait for a response     #
#                                                                          #
#    OUT:                                                                  #
#         Due to limitations not yet overcome, the function will only      #
#         return the value of the MIB returned by the switch.  If an       #
#         error occurs, there is no way to return the error back to the    #
#         calling function.                                                #
#                                                                          #
#  Bugs:  Limited error checking and inablility to return error codes.     #
#                                                                          #
############################################################################

proc ScottyGet {command host {timeout 5}} {
   global readcommunity writecommunity
   DebugDump

   if {[llength $host] > 1} {
      set readCommunity [lindex $host 1]
      set writeCommunity [lindex $host 2]
   } elseif {[info exists readcommunity] != 1 || [info exists writecommunity] != 1} {
      return ERRORUNDEFINEDCOMMUNITIES
   } else {
      set readCommunity $readcommunity
      set writeCommunity $writecommunity
   }

   if {[IsSwitch8600 $host] == "TRUE"} {
      catch {snmp session -timeout $timeout -community $readCommunity -writecommunity $writeCommunity -address [lindex $host 0] -version SNMPv2C} s
   } else {
      catch {snmp session -timeout $timeout -community $readCommunity -writecommunity $writeCommunity -address [lindex $host 0]} s
   }

   set switchType [GetSwitchMIBType $host]
   set command [ConvertCommandToOID $command $switchType]

   $s get $command {
      if {"%E" == "noError"} {
         set scottystringtoreturn [lindex [lindex {%V} 0] 2]
         return "$scottystringtoreturn"
      } else {
         return "%E"
      }
      %S destroy
   }
   snmp wait
}

proc ConvertMIBToOID {command switchType} {
   global mibArray

   set commandEnd [join [lrange [split $command .] 1 [llength [split $command .]]] .]
   set command [lindex [split $command .] 0]
   if {[info exists mibArray($switchType,$command)] == 1} {
      if {$commandEnd != ""} {
         return "$mibArray($switchType,$command).$commandEnd"
      } else {
         return "$mibArray($switchType,$command)"
      }
   } else {
      if {$commandEnd != ""} {
         return "$command.$commandEnd"
      } else {
         return "$command"
      }
   }
}

proc ConvertCommandToOID {command switchType} {
   set len [llength $command]
   set index 0
   while {$index < $len} {
      lappend newCommand [ConvertMIBToOID [lindex $command $index] $switchType]
      incr index
      if {$len > 1} {
         lappend newCommand [lindex $command $index]
         incr index
      }
   }
   return $newCommand
}

############################################################################
#  Procedure ScottySet takes in the necessary parameters to make an SNMP   #
#  MIB call to the specified switch.  The session is setup, the command    #
#  executed, and the session is torn down.  Ideally, this function should  #
#  not be used except by calls from the procedure "scotty".  If it is ever #
#  possible to switch MIBs in the background, there needs to be a locking  #
#  mechanism to prevent one process from switching MIBs while another      #
#  process is using them.  The function "scotty" takes care of this, but   #
#  this function does not.                                                 #
#                                                                          #
#  Variables                                                               #
#    IN:                                                                   #
#         command:      String specifying the MIB object and any           #
#                       parameters being assigned to that object           #
#         host:         IP address of the switch or list containing the    #
#                       IP address of the switch, the read community       #
#                       string, and the write community string in this     #
#                       order.  If this variable is only the IP address    #
#                       of the switch, the read and write communities must #
#                       be globally set in the variables readcommunity and #
#                       writecommunity.                                    #
#         timeout:      Integer specifying time to wait for a response     #
#                                                                          #
#    OUT:                                                                  #
#         Due to limitations not yet overcome, the function will only      #
#         return the value of the MIB returned by the switch.  If an       #
#         error occurs, there is no way to return the error back to the    #
#         calling function.                                                #
#                                                                          #
#  Bugs:  Limited error checking and inablility to return error codes.     #
#                                                                          #
############################################################################

proc ScottySet {command host {timeout 5}} {
   global readcommunity writecommunity
   DebugDump

   if {[llength $host] > 1} {
      set readCommunity [lindex $host 1]
      set writeCommunity [lindex $host 2]
   } elseif {[info exists readcommunity] != 1 || [info exists writecommunity] != 1} {
      return ERRORUNDEFINEDCOMMUNITIES
   } else {
      set readCommunity $readcommunity
      set writeCommunity $writecommunity
   }

   if {[expr [llength $command]%2] == 1} {
      return ERRORODDNUMPARAMETERS
   }

   set switchType [GetSwitchMIBType $host]
   set command [ConvertCommandToOID $command $switchType]

   if {[IsSwitch8600 $host] == "TRUE"} {
      catch {snmp session -timeout $timeout -community $readCommunity -writecommunity $writeCommunity -address [lindex $host 0] -version SNMPv2C} s
   } elseif {[string match "*agReset.0*" $command] == 1} {
      catch {snmp session -retries 0 -timeout 1 -community $readCommunity -writecommunity $writeCommunity -address [lindex $host 0]} s
   } elseif {[string match "*agTftpAction.0*" $command] == 1} {
      catch {snmp session -timeout 500 -community $readCommunity -writecommunity $writeCommunity -address [lindex $host 0]} s
   } else {
      catch {snmp session -timeout $timeout -community $readCommunity -writecommunity $writeCommunity -address [lindex $host 0]} s
   }

   set i 0
   set len [llength $command]
   set commandList [list [list [lindex $command $i] [lindex $command [expr $i + 1]]]]
   incr i 2
   while {$i < $len} {
      lappend commandList [list [lindex $command $i] [lindex $command [expr $i + 1]]]
      incr i 2
   }

   $s set $commandList {
      if {"%E" == "noError"} {
         set scottystringtoreturn ""
         for {set scottycountervariable 0} {$scottycountervariable < [llength {%V}]} {incr scottycountervariable} {
            lappend scottystringtoreturn [lindex [lindex {%V} $scottycountervariable] 2]
         }
         unset scottycountervariable
         return $scottystringtoreturn
      } else {
         return "%E"
      }
      %S destroy
   }
   snmp wait
}


############################################################################
#  Procedure ScottySetRaw takes in the necessary parameters to make an     #
#  SNMP MIB call to the specified switch.  This function is nearly         #
#  identicle to the procedure "ScottySet" except that this procedure does  #
#  not use asynchronous calls.  The trade-off is that it does have better  #
#  ability to return error codes.  Like ScottySet, this procedure should   #
#  only be used by "scotty" and not for general purpose.                   #
#                                                                          #
#  Variables                                                               #
#    IN:                                                                   #
#         command:      String specifying the MIB object and any           #
#                       parameters being assigned to that object           #
#         host:         IP address of the switch or list containing the    #
#                       IP address of the switch, the read community       #
#                       string, and the write community string in this     #
#                       order.  If this variable is only the IP address    #
#                       of the switch, the read and write communities must #
#                       be globally set in the variables readcommunity and #
#                       writecommunity.                                    #
#                                                                          #
#    OUT:                                                                  #
#         Procedure returns the result of the SNMP MIB call.  This can be  #
#         an error or the value of the MIB object.                         #
#                                                                          #
#  Bugs:  None known.                                                      #
#                                                                          #
############################################################################

proc ScottySetRaw {command host} {
   global readcommunity writecommunity

   if {[llength $host] > 1} {
      set readCommunity [lindex $host 1]
      set writeCommunity [lindex $host 2]
   } elseif {[info exists readcommunity] != 1 || [info exists writecommunity] != 1} {
      return ERRORUNDEFINEDCOMMUNITIES
   } else {
      set readCommunity $readcommunity
      set writeCommunity $writecommunity
   }

   set switchType [GetSwitchMIBType $host]
   set command [ConvertCommandToOID $command $switchType]

   if {[IsSwitch8600 $host] == "TRUE"} {
      catch {snmp session -timeout 5 -community $readCommunity -writecommunity $writeCommunity -address [lindex $host 0]} s
   } else {
      catch {snmp session -timeout 5 -community $readCommunity -writecommunity $writeCommunity -address [lindex $host 0]} s
   }

   set listCommand [list $command]
   catch {[$s set $listCommand]} scottystringtoreturn
   $s destroy
   return $scottystringtoreturn
}


############################################################################
#  Procedure ScottyGetNext will return the value of the next configured    #
#  MIB as specified by the MIB contained in the variable curCommand.  If   #
#  the operation is successful, the curCommand variable is altered so that #
#  the next call of ScottyGetNext will result in the next configured MIB   #
#  after what was returned by the current ScottyGetNext function call.     #
#  Errors returned include ERRORUNDEFINEDCOMMUNITIES (global community     #
#  variables not set and host variable only contained host IP address),    #
#  ERRORNOSUCHNAME (SNMP noSuchName error occured), ERRORINVALIDOBJECT     #
#  (SNMP reported that the MIB given is not valid), or ERRORNORESPONSE     #
#  (SNMP did not get a response back from the host).                       #
#                                                                          #
#  Variables                                                               #
#    IN:                                                                   #
#         curCommand:   String specifying the MIB object to get            #
#         host:         IP address of the switch or list containing the    #
#                       IP address of the switch, the read community       #
#                       string, and the write community string in this     #
#                       order.  If this variable is only the IP address    #
#                       of the switch, the read and write communities must #
#                       be globally set in the variables readcommunity and #
#                       writecommunity.                                    #
#                                                                          #
#    OUT:                                                                  #
#         Procedure returns the result of the SNMP MIB call and sets the   #
#         curCommand to be the next MIB if successful.  Otherwise, an      #
#         error is returned and the value of curCommand is not changed.    #
#                                                                          #
#  Bugs:  None known.                                                      #
#                                                                          #
############################################################################

proc ScottyGetNext {curCommand host {showErrors FALSE}} {
   global readcommunity writecommunity
   DebugDump

   upvar $curCommand command

   if {[llength $host] > 1} {
      set readCommunity [lindex $host 1]
      set writeCommunity [lindex $host 2]
   } elseif {[info exists readcommunity] != 1 || [info exists writecommunity] != 1} {
      LogFile "ScottyGetNext: Communities are not defined for host $host" ERROR
      DumpStackTrace
      return ERRORUNDEFINEDCOMMUNITIES
   } else {
      set readCommunity $readcommunity
      set writeCommunity $writecommunity
   }

   set switchType [GetSwitchMIBType $host]
   set commandOID [ConvertCommandToOID $command $switchType]

   catch {snmp session -timeout 5 -community $readCommunity -address [lindex $host 0]} s

   set rcode SUCCESS

   catch {$s getnext $commandOID} nextCommand 
   if {[lindex $nextCommand 0] == "noSuchName"} {
      set rcode ERRORNOSUCHNAME
   } elseif {[lindex $nextCommand 0] == "invalid"} {
      set rcode ERRORINVALIDOBJECT
   } elseif {([lindex $nextCommand 0] == "noResponse") || ([string match "*network is unreachable*" $nextCommand] == 1)} {
      set rcode ERRORNORESPONSE
   }

   if {[string match "*ERR*" $rcode] == 1} {
      if {$showErrors == "TRUE"} {
         LogFile "ScottyGetNext: An error occurred while getting the next $curCommand ($commandOID): $rcode" DEBUG
         DumpStackTrace
      }
      set value $rcode
   } else {
      set value [lindex [lindex $nextCommand 0] 2]
      set command [mib name [lindex [lindex $nextCommand 0] 0]]
   }
   catch {$s destroy} err
   return $value
}


############################################################################
#  Procedure CleanUpSNMPSessions deletes any SNMP sessions remaining after #
#  the scotty call completes.  By running this procedure, the memory leak  #
#  within scotty is cleaned up.                                            #
#                                                                          #
#  Bugs:  None known.                                                      #
#                                                                          #
############################################################################

proc {CleanUpSNMPSessions} {} {
   set temp [snmp info]
   foreach value $temp {
      $value destroy
   }
}

# proc ErrCheck {rcode callingFunction {returnTheValue "FALSE"}} {

# 	global testlib_error

#     if {[string match "*ERR*" $rcode] == 1} {
#         set listLen [llength $rcode]

# 		set acelib_error 1

#         #set dbg "$callingFunction failed on the following scotty calls:"
#         set dbg "$callingFunction failed on the following calls:"
#         set firstError ""
#         for {set count 0} {$count < $listLen} {incr count} {
#             if {[string match "*ERR*" [lindex $rcode $count]] == 1} {
#                 append dbg " $count ([lindex $rcode $count])"
#                 if {$firstError == ""} {
#                     set firstError [lindex $rcode $count]
#                 }
#             }
#         }
#         LogFile "$dbg" ERROR
#         #return $firstError
#         return "ERROR"
#     } elseif {$returnTheValue == "TRUE"} {
#         return $rcode
#     } else {
#         return "SUCCESS"
#     }
# }

proc DumpStackTrace {} {
   global globalLogErrorFlag
   if {[info exists globalLogErrorFlag] != 1} {
      set globalLogErrorFlag 1
   }
   if {$globalLogErrorFlag == 1} {
      for {set level [expr [info level] - 1]} {$level > 0} {incr level -1} {
         LogFile "Stack call level $level: [info level $level]" DEBUG
      }
   }
}


proc DebugDump {} {
   return
   set thelist ""
   for {set level [expr [info level] - 1]} {$level > 0} {incr level -1} {
      if {$thelist == ""} {
         set thelist [info level $level]
      } else {
         set thelist "[lindex [info level $level] 0] -> $thelist"
      }
   }
   LogFile "$thelist" DEBUG
}


