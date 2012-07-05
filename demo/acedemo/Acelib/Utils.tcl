##############
# BackupFileResolvConf {}                                             #
# ChangeNewResolvConf {DNSServer}                                     #
# RestoreResolvConf {}                                                #

# cesLogsSetup { logMesage }
# CLILogFormat { cliLogFile {dir logs} }
#
# AddNetStaticRoute {net mask gw}
# DelNetStaticRoute {net mask gw}
# AddHostStaticRoute {host gw}
# DelHostStaticRoute {host gw}
# DelArpEntry {host_ip} 
#
# PingHost {dstHost {srcIp NONE}}
# CheckFtpLs {dstHost}
# CheckTelnet {server user password}
#
# interfaceLocal:add {ipAddr {mask 255.255.255.0}}
# interfaceLocal:find {ipAddrToFind} 
# interfaceLocal:get {{alias none} {mask none}}
# interfaceLocal:remove {ipAddr}
# interfaceLocal:resolve {intf}
# interfaceLocal:return {}
# interfaceLocal:promisc {intf status}
#
# GenerateIp {prohibIpList}
#
# GetFileData {file_name}
# WriteFile {file_name file_data}
# DownloadCesFile {host file_name local_file {user admin} {pass setup}}
# GetCoreFiles {host}
#############



##################
#// procedures for handle the /etc/resolv.conf file of client PC
##################

############################################################################
#  Procedure BackupFileResolvConf                                          # 
#  This function will copy the /etc/resolv.conf file to                    #
#                              /etc/AceTest.resolv.conf  file              #
#  Variables                                                               #
#    none                                                                  #
#                                                                          #
#  Bugs:  None known.                                                      #
#                                                                          #
############################################################################
#//save resolv.conf before starting GSLB test cases

proc {BackupResolvConfFile} {} {
   if {[file exists /etc/resolv.conf] == 1} {
      file rename -force /etc/resolv.conf /etc/AceTest.resolv.conf
   }
}

############################################################################
#  Procedure  ChangeNewResolvConf                                          # 
#  This function will modify the content of file /etc/resolv.conf, on the  #
#  client computer                                                         #
#                                                                          #
#  Variables                                                               #
#      DNSServer:        IP of DNS server for client                       #
#                                                                          #
#  Bugs:  None known.                                                      #
#                                                                          #
############################################################################

proc {ChangeNewResolvConf} {DNSServer {search "ces"}} {  

   set fileID [open /etc/resolv.conf w]
   puts $fileID "search $search"
   puts $fileID "nameserver $DNSServer"
   close $fileID
}


############################################################################
#  Procedure RestoreResolvConf                                             # 
#  This function will copy the /etc/resolv.conf.backup file to             #
#                              /etc/resolv.conf file                       #
#  Variables                                                               #
#    none                                                                  #
#                                                                          #
#  Bugs:  None known.                                                      #
#                                                                          #
############################################################################

proc {RestoreResolvConf} {} {
   if {[file exists /etc/AceTest.resolv.conf] == 1} {
      file rename -force /etc/AceTest.resolv.conf /etc/resolv.conf
   }
}




###########################################################
## LOGS
###########################################################

##########################################
# cesLogsSetup replaces [\x000-\x01A] characters from "logging events" message
# \xXXX = hex code of the character
#
#
#
##########################################
proc cesLogsSetup { logMesage } {

   set modifiedLogs ""
   
   set contLine ""
   foreach line [split $logMesage "\n"] {

      regsub -all {[\x000-\x01A]} $line "" line 

      if {$line == "" || $line == " "} {
         continue
      } 
      if {[regexp {[0-9]+/[0-9]+/[0-9]+} $line] == 1} {
         set contLine $line
         continue
      }
      if {$contLine == ""} {
         #puts $line
         append modifiedLogs $line "\n"            
      } else {            
         append contLine $line                       
         append modifiedLogs $contLine "\n"
         set contLine ""            
      }
   }          
   return $modifiedLogs
}

#############################
#cesLogsSetup replaces [\x000-\x01F] characters from "logging events" message
# \xXXX = hex code of the character
#
# Formatting is handled different for windows and for unix
#
#############################
proc CLILogFormat { {cliLogFile "CLI.log"} {dir "logs"} } {

   global tcl_platform

   set fileID [open "$dir/$cliLogFile" r]    
   set fileData [read $fileID] 
   close $fileID
   set fileID [open "$dir/$cliLogFile" w]

   set prevLineNull 0

   if {$tcl_platform(platform) == "unix"} {
      foreach line [split $fileData "\n"] {
         regsub -all {[\x000-\x01F]} $line "" newLine
         if {$newLine == "" || $newLine == " "} {
            if {$prevLineNull == 1} {
               puts $fileID $newLine
               #puts "*** saved empty line"
            }
            #puts "----------------dropped empty line"
            set prevLineNull 1
         } else {
            set prevLineNull 0
            puts $fileID $newLine
            #puts "$newLine"
         }
      }
   }

   if {$tcl_platform(platform) == "windows"} {
      set prevLineNull 0
      foreach line [split $fileData "\n"] {

         #regsub -all {[\x000-\x01F]} $line "" newLine
         set newLine $line
         if {$newLine == "" || $newLine == " "} {
            if {$prevLineNull == 1} {
               puts $fileID $newLine
            }
            set prevLineNull 1
         } else {
            set prevLineNull 0
            puts $fileID $newLine
         }
      }
   }

   close $fileID

}


##############################
## STATIC routes on the AceTest PC
##############################

proc AddNetStaticRoute {net mask gw} {

   global staticRouteChanged    

   set rcode ""
   
   set routeAdd [catch {exec route add -net $net netmask $mask gw $gw} errRoute]
   #puts "\n\n $errRoute \n\n"
   if {$routeAdd != 0 && [regexp "SIGCHLD" $errRoute] != 1 && [regexp -nocase "file exists" $errRoute] != 1} {
      lappend rcode "ERR: $errRoute"
      set staticRouteChanged 1
   } else {
      logFile "\nAddNetStaticRoute: route add -net $net netmask $mask gw $gw"
      logCliFile "\n\nAddNetStaticRoute: route add -net $net netmask $mask gw $gw"
   }

   return [ErrCheck $rcode AddNetStaticRoute]
   
}


proc DelNetStaticRoute {net mask gw} {

   global staticRouteChanged
   
   set rcode ""
   
   #puts "net = $net; mask = $mask; gw = $gw"
   set routeDel [catch {exec route del -net $net netmask $mask gw $gw} errRoute]
   
   #puts "\n\n---------------DelNetStaticRoute errRoute = $errRoute"
   if {$routeDel != 0 && [regexp "SIGCHLD" $errRoute] != 1} {
      lappend rcode "ERR: $errRoute"
      set staticRouteChanged 0
   } else {
      logFile "\nDelNetStaticRoute: route del -net $net netmask $mask gw $gw"
      logCliFile "\n\nDelNetStaticRoute: route del -net $net netmask $mask gw $gw\n"
   }

   return [ErrCheck $rcode DelNetStaticRoute]    

}

proc AddHostStaticRoute {host gw} {

   global staticRouteChanged    

   set rcode ""
   set routeAdd 0
   
   catch {exec route add -host $host gw $gw} errRoute
   #//verify that the route was added
   catch {exec netstat -rn} netstatRes
   foreach line [split $netstatRes "\n"] {
      if {[regexp $host $line] == 1 && [regexp $gw $line] == 1} {
         set routeAdd 1
         set staticRouteChanged 1
         break
      }
   }

   if {$routeAdd != 1} {
      lappend rcode "ERR: $errRoute"        
   }

   return [ErrCheck $rcode AddHostStaticRoute]
   
}


proc DelHostStaticRoute {host gw} {

   global staticRouteChanged
   
   set rcode ""
   set routeDel 0
   catch {exec route del -host $host gw $gw} errRoute

   #//verify that the route was added
   catch {exec netstat -rn} netstatRes

   foreach line [split $netstatRes "\n"] {
      if {[regexp $host $line] == 1 && [regexp $gw $line] == 1} {
         set routeDel 1
         lappend rcode "ERR: $errRoute"
         break
      }
   }
   
   if {$routeDel == 0} {        
      set staticRouteChanged 0
   }

   return [ErrCheck $rcode DelHostStaticRoute]    

}

################################################
#  Procedure  DelArpEntry    - remove a entry from arp cache.
#                                                                          
#  Variables                                                               
#    IN:                                                                   
#           host_ip: the indicated host for removing
#                                                                          
#    OUT:                                                                  
#           SUCCESS - if remove is successfull
#           ERROR - otherwise                                                     
#################################################
proc DelArpEntry {host_ip} {
   
   set rcode ""
      set arpDel [catch {exec arp -d $host_ip} errDel]
   
   if {$arpDel != 0} {
      lappend rcode "ERR: $errDel"
   } else {
      logFile "\nDelArpEntry: arp -d $host_ip"
      logCliFile "\n\nDelArpEntry: arp -d $host_ip\n"
   }

   return [ErrCheck $rcode DelArpEntry] 
}


################################################
#  Procedure  PingHost    - attempts to ping the host given by dstHost.
#                         Works on both Windows and Unix platforms.
#                         You cannot specify the source address on Windows. There is no this option for Windows.
#                                                                          
#  Variables                                                               
#    IN:                                                                   
#           dsthost: IP address or name of the host you want to ping
#           srcIp:   IP interface from which you want to do ping (optional; default value = SYSDEFAULT)
#           iter_no:      number of iterations used. 
#                                                                          
#    OUT:                                                                  
#           SUCCESS - if ping to dsthost successfull
#           ERROR - otherwise                                                
#                                                                          
#  Bugs:  None known.                                                      
#################################################
proc PingHost {dstHost {srcIp "SYSDEFAULT"} {iter_no 1 }} {

   global tcl_platform
   set rcode ""

   if {[regexp -nocase "unix" $tcl_platform(platform)] == 1} {
        
      for {set i 1} {$i <= $iter_no} {incr i} {
          if {$srcIp == "SYSDEFAULT"} {
              catch {exec ping -c 5 $dstHost} result
          } else {
              catch {exec ping -c 5 $dstHost -I $srcIp} result
          }
            
          set icmpCount 0
          foreach line [split $result "\n"] {
              if { [regexp "64 bytes from" $line] == 1 } {
                  incr icmpCount
                }
          }
          if {$icmpCount == 5} {
                #        LogFile "OK ping host $dstHost"        
              break
          } else {
              if {$i == $iter_no} {
                  lappend rcode "ERROR: Fail to ping $dstHost\n$result"
                }
          }
      }
    }
    
   if {[regexp -nocase "windows" $tcl_platform(platform)] == 1} {
       
      set sent x
      set received y
      set icmpCount 0
      
      for {set i 1} {$i <= $iter_no} {incr i} {
          catch {exec ping $dstHost -n 5} result

          foreach line [split $result "\n"] {
         
              if {[regexp -nocase {Reply[\ \t]+from} $line]} {              
                  incr icmpCount
              }            
              
          }
          
          if {$icmpCount == 5} {
              #        LogFile "OK ping host $dstHost"       
              break       
          } else {
               if {$i == $iter_no} {
                   lappend rcode "ERROR: Fail to ping $dstHost\n$result"
               }
          }        
      }
  }
   return [ErrCheck $rcode PingHost]
   
}



################################################
# Procedure  CheckFtpLs    verifies both control and data ftp connections.
#                          Opens a control connection to server and then attempts to run ls command.
#                          FTP client is the PC from which this procedure is run.
#                                                                          
# Variables                                                               
#   IN:                                                                   
#          server:   IP address or name of the ftp server
#          user:     user ID for the FTP server
#          password: FTP server password
#                                                                          
#   OUT:                                                                  
#          SUCCESS - if both control and data ftp connections are OK
#          ERROR   - otherwise                                                
#                                                                          
# Bugs:  None known.                                                      
#################################################
proc CheckFtpLs {server user password} {
   
   set rcode ""
   set rcodeLs "ERROR: ftp session - ls command failed"
   #set rcodeClose "ERROR: fail to close ftp connection."    

   # verify first if ftp_lib is available
   if {[regexp {FTP::Open} [info command FTP::Open]] != 1 && [regexp {FTP::Open} [info proc FTP::Open]] != 1} {
      lappend rcode "ERROR: ftp_lib.tcl library not avaiable. Please check for this file in ./sources/ folder"
      # close ftp connection
#       FTP::Close
#       return [ErrCheck $rcode CheckFtpLs]
   }
   
   set okOpen [FTP::Open $server $user $password]
   if {$okOpen != 1} {
      lappend rcode "ERROR: fail to open ftp connection."
      # close ftp connection
#       FTP::Close
#       return [ErrCheck $rcode CheckFtpLs]
   }
   
   set listRes [FTP::List]
   if {$listRes != ""} {
      set okList 1        
      #foreach elem $listRes {
      #    LogFile "$elem"
      #}
      #        LogFile "OK ls command (ftp session to $server)"
   } else {
      set okList 0
      lappend rcode $rcodeLs
   }

   # close ftp connection
   FTP::Close
   
   return [ErrCheck $rcode CheckFtpLs]

}

################################################
# Procedure  CheckTelnet    attempts to open a telnet session to a CES
#                                                                                                     
# Variables                                                               
#   IN:                                                                   
#          server:  IP address or name of the ftp server
#          uid:      user ID for the telnet server
#          password: telnet server password
#                                                                          
#   OUT:                                                                  
#          SUCCESS - if telnet to CES succeded
#          ERROR   - otherwise                                                
#                                                                          
# Bugs:  None known.                                                      
#################################################
proc CheckTelnet {server user password} {

   set rcode ""

   if {[Connect $user $password $server] != "SUCCESS"} {
      #Just return ERROR. If connection fails, Connect proc throws an error message
      return "ERROR"
   }    
   Disconnect $server

   #    LogFile "OK telnet session to $server"
   
   return [ErrCheck $rcode CheckTelnet]    
}


##############
# Procedures relating to thd local IP interface setup.
###########################################################

#############################################################
# interfaceLocal:add
#############################################################
proc {interfaceLocal:add} {ipAddr {mask 255.255.255.0}} {
   global widget

   global card   

   #// COMMENT OUT THE ORIGINAL
   LogFile "-->> interfaceLocal:add" debug
   LogFile "      args: $ipAddr" debug
   LogFile "     -Adding $ipAddr as a local interface-" debug


   # - ce proj - new
   #//if ipAddr = the IP address or an other eth device, do not add an other local interface
   foreach configIP [interfaceLocal:get "all"] {
      if {$configIP == $ipAddr} {
         LogFile "     -Did not create the local interface $ipAddr because there is already an eth device with this IP address-" debug
         LogFile " <-- interfaceLocal:add" debug
         return SUCCESS
      }
   }

   #set card 0
   set cardDone FALSE
   set intf 0
   set intfDone FALSE
   while {$cardDone == "FALSE"} {
      catch {exec ifconfig $card} result
      if {[string match "*no such file or directory" $result] == 1} {
         return ERRORBADRIGHTS
      }
      set match ""
      regexp {addr:[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+} $result match
      if {$match == ""} {
         set cardDone TRUE
      }
      while {$cardDone == "FALSE" && $intfDone == "FALSE"} {
         catch {exec ifconfig $card:$intf} result
         set match ""
         regexp {addr:[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+} $result match
         if {$match == ""} {
            set intfDone TRUE
            set cardDone TRUE
         } else {
            set intf [expr $intf + 1]
         }
      }
   }

	#// calculate broadcast address based on IP address and MASK
	set broad [getBroadcast $ipAddr $mask]

	catch {exec ifconfig $card:$intf $ipAddr broadcast $broad netmask $mask} err
   
	if {$err == "" || [regexp "SIGCHLD" $err] == 1} {
		LogFile "     -Created local interface $ipAddr ok-" debug
		LogFile " <-- interfaceLocal:add" debug
		return SUCCESS
	} else {
		LogFile "     -Unable to Create local interface $ipAddr- $err" debug
		LogFile " <-- interfaceLocal:add" debug      
		return ERROR
	}


}


#############################################################
# interfaceLocal:find
#############################################################
proc {interfaceLocal:find} {ipAddrToFind} {
   global widget
   #// COMMENT OUT ORIGINAL
   LogFile "-->> interfaceLocal:find" debug
   LogFile "      args: $ipAddrToFind" debug
   LogFile "     -Get the local interface for address $ipAddrToFind-" debug

   set intfList [interfaceLocal:return]
   if {$intfList == "ERRORBADRIGHTS"} {
      LogFile "     -Running in non privelige mode can't get interface info-" debug
      LogFile " <-- interfaceLocal:find" debug
      return ERROR
   }
   foreach intf $intfList {
      catch {exec ifconfig $intf} result
      set match ""
      regexp {addr:[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+} $result match
      if {$match != ""} {
         set ipAddr [lindex [split $match :] 1]
         if {$ipAddr == $ipAddrToFind} {
            LogFile "     -Found $ipAddrToFind on interface $intf-" debug
            LogFile " <-- interfaceLocal:find" debug
            return $intf
         }
      }
   }
   LogFile "     -Cant find any local interfaces with address $ipAddrToFind-" debug
   LogFile " <-- interfaceLocal:find" debug
   return NOTFOUND
}


###########################################################
# Procedure:  interfaceLocal:get - returns different informations about ethernet interfaces.
# 
# IN: alias: all, <interface name>, real, virtual, none
#            mask:  none
#
# OUT: if: alias = interfaces: a list with all configured eth interfaces
#          alias = all: a list with all IP addresses for all eth interfaces
#          alias = <interface name>: the IP address of the specified interface if configured; 
#                      nothing if interface not configured
#          alias = real: a list with the IP addresses for all real eth interfaces
#          alias = virtual: a list with IP addresses for all virtual interfaces
#          alias = <interface name> & mask != none: return the IP Mask for the specified eth interface.
#
#          returns: ERRORBADRIGHTS -if it is called without root rights
############################################################                   
proc {interfaceLocal:get} {{alias none} {mask none}} {
   global widget
   set ipList ""
	set ipReal ""
	set ipVirt ""
   set intfList [LinuxGetConfiguredInterfaces]
   if {$intfList == "ERRORBADRIGHTS" || $alias == "interfaces"} {
      return $intfList
   }
   foreach intf $intfList {
      set result [LinuxGetInterfaceIP $intf]
      if {$result != "NOTCONFIGURED" && $result != "ERRORBADRIGHTS"} {
			if {$alias == $intf} {
				if {$mask != "none"} {
					return [LinuxGetInterfaceMask $intf]
				}
				return $result
			}
         lappend ipList $result
			if {[regexp ":" $intf] == 1} {
				lappend ipVirt $result
			} else {
				lappend ipReal $result
			}
      }
   }
   if {$alias == "all"} {
      return $ipList
   } elseif {$alias == "real"} {
		return $ipReal
	} elseif {$alias == "virtual"} {
		return $ipVirt
	} else {
      return [lindex $ipList 0]
	}

}


#############################################################
# Procedure:  interfaceLocal:remove
#############################################################
proc {interfaceLocal:remove} {ipAddr} {
   global widget

   global card

   #// COMMENT OUT ORIGINAL
   LogFile "-->> interfaceLocal:remove" debug
   LogFile "      args: $ipAddr" debug
   LogFile "     -Remove interface coresponding to IP Address $ipAddr-" debug

   set intf [interfaceLocal:find $ipAddr]
   if {$intf == "NOTFOUND"} {
      return SUCCESS
   } elseif {$intf == "ERRORBADRIGHTS"} {
      LogFile "     -Running in non privelige mode can't remove interface $ipAddr-" debug
      LogFile " <-- interfaceLocal:remove" debug
      return ERROR
   }
   if {[regexp "$card:\[0-9\]+" $intf]} {
      catch {exec ifconfig $intf down} err      
      if {$err == "" || [regexp "SIGCHLD" $err]} {
         LogFile "     -Successfully removed interface $ipAddr-" debug
         LogFile " <-- interfaceLocal:remove" debug
         return SUCCESS
      } else {
         LogFile "     -Could Not remove interface $ipAddr-" debug
         LogFile " <-- interfaceLocal:remove" debug
         return ERROR
      }
   }
}


#############################################################
# interfaceLocal:resolve
#############################################################
proc {interfaceLocal:resolve} {intf} {
   global widget

   catch {exec ifconfig $intf} result
   set match ""
   regexp {addr:[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+} $result match
   if {$match != ""} {
      set ipAddr [lindex [split $match :] 1]
      return $ipAddr
   }
   return NOTCONFIGURED
}


#############################################################
# interfaceLocal:return
#############################################################
proc {interfaceLocal:return} {} {
   catch {exec ifconfig | grep eth} result
   if {[string match "*no such file or directory" $result] == 1} {
      return ERRORBADRIGHTS
   }
   set lines [split $result "\n"]
   set len [llength $lines]
   for {set i 0} {$i < $len} {incr i} {
      lappend intf [lindex [lindex $lines $i] 0]
   }
   return $intf
}

proc interfaceLocal:promisc {intf status} {
   
   set rcode ""
   set result ""

   if {[regexp -nocase ena $status] == 1} {
      catch {exec ifconfig $intf promisc} result
   } elseif {[regexp -nocase dis $status] == 1} {
      catch {exec ifconfig $intf -promisc} result
   } else {
      lappend rcode "ERROR: Wrong value for status. It must be enable/disable"
      return [ErrCheck $rcode]
   }

   if {[string match "*unknown interface*" $result] == 1} {
      puts "result -- $result"
      lappend rcode "ERROR: $result"
      return [ErrCheck $rcode]
   }
   return "SUCCESS"
}


#############################################################
# interfaceLocal:getmac: Returns the MAC address for the given ethernet card
#
# IN: intf: <eth0/eth1/ ...> ethernet card name 
#
# OUT: MAC address (small letters)
#      ERROR  if cannot run 'ifconfig'
#############################################################
proc interfaceLocal:getmac {intf} {
   
   set err_count [GetGlobalErr]
   
   if {[catch {exec ifconfig $intf} result] != 0 && [regexp -nocase {error waiting for process to exit} $result] != 1} {
      ErrCheck [list "ERROR: cannot run 'ifconfig $intf'. Please verify that the command is correct and you have the appropriate rights"]
      logFile $result
      return [CheckGlobalErr $err_count]
   }

   if {[regexp -nocase {HWaddr ([0-9a-h]+:[0-9a-h]+:[0-9a-h]+:[0-9a-h]+:[0-9a-h]+:[0-9a-h]+)} \
            $result all mac_addr]} {
      return [string tolower $mac_addr]
   } else {
      ErrCheck [list "ERROR: no ethernet MAC address found for $intf. See below the output for 'ifconfig $intf'"]
      logFile $result
      return [CheckGlobalErr $err_count]
   }
   
}


#############################################################
# GenerateIp: This procedures returns an IP address different from
#             the IP addresses given by 'prohibIpList' and in the same
#             class with these IP addresses.
#             The procedure verifies that the new IP is not reachable
#             by ping.
#
# IMPORTANT:  The HOST which is used to run this proc MUST have 
#             configured anIP interface from the same class with
#             the IPs from 'prohibIpList', in order to be able to 
#             verify that the new IP is or is not reachable by ping.
#
#             If such an IP does not exists, create such an IP before
#             using GenerateIp with:
#             'interfaceLocal:add' proc
#             and remove this IP after using GenerateIp with:
#             'interfaceLocal:remove' proc
#
# IN:  prohibIpList: {A.B.C.D1 A.B.C.D2 ... A.B.C.Dn}: a list with 
#                    IP addresses all from the same subnet.
#
# OUT: A.B.C.Dx: an ip address that will be used by test procedures
#                which is different from the IP addresses from 
#                'prohibIpList', in the same subnet and which cannot
#                be reached by ping.
#############################################################
proc GenerateIp {prohibIpList} {

   set sortedProhibList [lsort -dictionary $prohibIpList]

   set startIp [lindex $sortedProhibList [expr [llength $sortedProhibList] -1]]
   
   #set newIp [incrHost1 $startIp 1]
   set newIp [incrHost $startIp 1]

   set safeCount 0
   
   while {1} {

      #puts $newIp

      #verify there is no other device in the network with the same IP address
      if {[PingHost $newIp] == "ERROR" } {

         if {[lsearch $prohibIpList $newIp] == -1} {
            LogFile "IP = $newIp (proc GenerateIp)"
            return $newIp
         } 

      } else {
         
         lappend prohibIpList $newIp
         set newIp [incrHost $newIp 1]

      }  
      incr safeCount

      if {$safeCount >= 15} {
         return [ErrCheck "ERR: GenerateIp: -  Cannot generate an IP address different then IPs: $prohibIpList"]         
      }
   }
   
}; #end GenerateIp


#############################################################
# Miscelaneous
#############################################################

###
# returns a list containing the lines from the file file_name
###
proc GetFileData {file_name} {
   if {[catch {set file_id [open $file_name r]} err_open] != 0} {
      logFile "ERROR GetFileData: $err_open"
      return ERROPEN
   }

   set file_data [read $file_id]

   close $file_id

   set file_data [split $file_data "\n"]

   return $file_data

}

#######
# file_data should be a list with the lines you want to put into the file
####### 
proc WriteFile {file_name file_data} {
   if {[catch {set file_id [open $file_name w]} err_open] != 0} {
      logFile "ERROR WriteFile: $err_open"
      return ERROPEN
   }

   foreach elem $file_data {
      puts $file_id $elem
   }

   close $file_id

   return $file_data
}
  
#######
# file_name is the name of the file in the CES
####### 
proc DownloadCesFile {host file_name local_file {user admin} {pass setup}} {
    set rcode ""

    LogFile "DUT:$host - The CORE DUMP will be saved in log file"

    set mngHost [GetMngIpAddr $host]
    
    if {$mngHost == "ERROR"} {
#        LogFile "CES: $host - The CES haven't set management IP"
        lappend rcode "ERROR: CES: $host - The CES haven't set management IP"
        return [ErrCheck $rcode "DownloadCesFile"]
    }

    LogFile "mngHost - $mngHost"

    set local_ip [GenerateIp [IncrHost $mngHost "15"]]  
    
    LogFile "local: add a virtual interface (IP: $local_ip) in private network"
    interfaceLocal:add $local_ip "255.255.0.0"
    
    LogFile "DUT:$host - Enable FTP service"
    ServiceCfgFtp "enable" $host
    
    if {[regexp {FTP::Open} [info command FTP::Open]] != 1 && [regexp {FTP::Open} [info proc FTP::Open]] != 1} {
        lappend rcode "ERROR: ftp_lib.tcl library not avaiable. Please check for this file in ./sources/ folder"
        interfaceLocal:remove $local_ip
        return [ErrCheck $rcode "DownloadCesFile"]
    }
    
    LogFile "Open FTP connection to $mngHost (user: $user, pass: $pass)"
    if {[FTP::Open $mngHost $user $pass] != 1} {
        lappend rcode "ERROR: The connection to FTP server can't be open"
        interfaceLocal:remove $local_ip
        return [ErrCheck $rcode "DownloadCesFile"]
    } else {
        if {[FTP::Get "$file_name" $local_file] != 1} {
            lappend rcode "ERROR: CES: $host: the file: $file_name doesn't exist"
            interfaceLocal:remove $local_ip
            FTP::Close
            return [ErrCheck $rcode "DownloadCesFile"]
        } else {
            LogFile "\n#####\nDownload successfull from CES: \n$host; get file: \"$file_name\" to local file: \"$local_file\"\n#####\n"
        }
        FTP::Close
    }
        #disable switch ftp server
        interfaceLocal:remove $local_ip
        ServiceCfgFtp no_enable $host
}



#############################################################
# GetCoreFiles: This procedures returns a list of CORE file
#		    existed on the CES
# IN:		    host - CES address
# OUT:              coreList - list of core files
#############################################################
proc GetCoreFiles {host} {
	global cmdOut

	set cmd "ls SYSTEM/CORE"
	set i 0
        set corePath ""
        array set coreFileName {}

        SetCliLevel "USER" $host
	Exec $cmd "USER" $host
	#Split the message by lines and parse the lines one by one
        foreach line [split $cmdOut "\n"] {
		#Extract the core filename
		if {[regexp {(CORE\d+\.GZ)} $line coreFile]} {
                        set coreFileName($i) $corePath$coreFile
                        incr i
		} elseif {[regexp {(/ide\d+/SYSTEM/CORE/)} $line path]} {
                  set corePath $path
                }
	}
        if {![info exists coreFileName(0)]} {
            set coreFileName(0) ""
        }
        if {![info exists coreFileName(1)]} {
            set coreFileName(1) ""
        } 
	return [array get coreFileName]
}

#############################################################
# CmpdwnCoreFiles: This procedures compare and decide if a
#                  a new core appeared on the ces and
#                  download it.
# IN:		   initialCoreFiles - array with the initial core files
#                  finalCoreFiles - array with the present core files
#                  dut - ces connection
#                  testName - the name of the test
# OUT:             1 if the core was found and 0 if not
#############################################################
proc CmpdwnCoreFiles {dut initialCoreFiless finalCoreFiless testName} {
   global logDir
   set result 0
   set coreWarning "CORE DUMP ON "
   set core_dir "${logDir}/CORE"
   set swVer [GetSwitchSWVerNum_exp $dut]
   upvar $initialCoreFiless initialCoreFiles
   upvar $finalCoreFiless finalCoreFiles
   variable blaster_build [Global:getlist "blaster-build"]
   
   # If the ces has a blaster build loaded we have to abort the core download, beacuse we don't need that file.
   if {[GetSwitchSWVerNum_exp $dut] == $blaster_build} {
		LogFile "$dut has a blaster build loaded. CORE download aborted."
		return 1
   }
   if {[info exists initialCoreFiles(0)] && [info exists finalCoreFiles(0)] && $initialCoreFiles(0) != $finalCoreFiles(0) && $initialCoreFiles(1) != $finalCoreFiles(1)} {
      logFile $coreWarning$testName
      set file_data [clock format [clock seconds] -format %Y_%m_%d_%H_%M_%S]
      # Get the core file name
      regexp {(CORE\d+\.GZ)} $finalCoreFiles(0) core]==0
      # Download the core file from the ces
      DownloadCesFile $dut $finalCoreFiles(0) ${core_dir}/${swVer}__${dut}__${file_data}_${core}
      set result 1
   } elseif {[info exists initialCoreFiles(1)] && [info exists finalCoreFiles(1)] && $initialCoreFiles(1) != $finalCoreFiles(1)} {
      logFile $coreWarning$testName
      set file_data [clock format [clock seconds] -format %Y_%m_%d_%H_%M_%S]
      # Get the core file name
      regexp {(CORE\d+\.GZ)} $finalCoreFiles(1) core
      # Download the core file from the ces
      DownloadCesFile $dut $finalCoreFiles(1) ${core_dir}/${swVer}__${dut}__${file_data}_${core}
      set result 1
   }
   return $result
}