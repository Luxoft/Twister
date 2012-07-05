##################
#
#
#
#
##################


#####################################
#
# FIREWALL PROCS
#
#####################################

#######################################################
# SetFirewallForSilk - configures a firewall on the PC running AceTest.
#                     This PC will work as a router for Silk PC that must allow Silk PC to see switches private interfaces but 
#                     but must not allow access between private networks and public and private networks.
#
# Variables: 
#     silkIp:    IP address of the Silk PC 
#     prNet1If:  AceTest PC, Ip address of the interface from Private 1 net
#     prNet2If:  AceTest PC, Ip address of the interface from Private 2 net 
#
#
#######################################################
proc SetFirewallForSilk {silkIp prNet1If prNet2If} {


    #set prNet1 "10.9.34.0/24"
    #set prNet2 "10.9.35.0/24"

    #generate netIP
    set pr1BreakIp [split $prNet1If "."]
    set pr2BreakIp [split $prNet2If "."]
    
    set prNet1 "[lindex $pr1BreakIp 0].[lindex $pr1BreakIp 1].[lindex $pr1BreakIp 2].0/24"
    set prNet2 "[lindex $pr2BreakIp 0].[lindex $pr2BreakIp 1].[lindex $pr2BreakIp 2].0/24"


    #CLEANUP FIRST
    RemoveFirewallForSilk

    #filter policies
    exec iptables -P INPUT ACCEPT
    exec iptables -P FORWARD DROP
    exec iptables -P OUTPUT ACCEPT

    #enable forwarding on AceTest running PC
    exec echo "1" > /proc/sys/net/ipv4/ip_forward

    #forwarding rules
    exec iptables -A FORWARD -s $silkIp -d $prNet1 -j ACCEPT
    exec iptables -A FORWARD -d $silkIp -s $prNet1 -j ACCEPT

    exec iptables -A FORWARD -s $silkIp -d $prNet2 -j ACCEPT
    exec iptables -A FORWARD -d $silkIp -s $prNet2 -j ACCEPT

    #nat
    exec iptables -t nat -A POSTROUTING -s $silkIp -d $prNet1 -j SNAT --to-source $prNet1If
    exec iptables -t nat -A POSTROUTING -s $silkIp -d $prNet2 -j SNAT --to-source $prNet2If


}

########################################################################
# RemoveFirewallForSilk - removes the firewall setup from the AceTest PC
#
#
########################################################################
proc RemoveFirewallForSilk {} {
    exec iptables -Z
    exec iptables -X
    exec iptables -F
    exec iptables -F -t nat
    exec iptables -F -t mangle
    #disable forwarding
    exec echo "0" > /proc/sys/net/ipv4/ip_forward
}





################################
#
# CREATE START FILE
#
################################

###############################################################
# CreateStartFile - creates the silk.start file = the file used to communicate with Silk;
#                   This file contains test that need to be started by Silk and the test parameters
#
# Variables: args = paramName paramValue [paramName paramValue] ...
#            if  args = stop ->  stops the silk engine running on Silk PC
#
#
#
###############################################################
proc CreateStartFile { args } {

    set fileID [open ./tmp/silk.start w]

    fconfigure $fileID -translation crlf

    if {[string match -nocase "start" [lindex $args 0]]} {
        puts $fileID "stop"
    } else {
        set newLine 0
        foreach arg $args {
            if {$newLine == 0} {
                puts -nonewline $fileID $arg
                set newLine 1
            } else {
                puts -nonewline $fileID " "
                puts $fileID $arg
                set newLine 0
            }
        }
    }

    close $fileID
}



############################
#
# Move silk.start file from ./tmp to ./tmp/AceDir folder. This will start silk test.
#
#
############################
proc MoveStartFile {} {
    set okMove 0
    set rcode ""
    set okMove [catch {file rename -force ./tmp/silk.start ./tmp/AceDir/silk.start} mvErr]

    if {$okMove != 0} {
        set rcode "ERROR: $mvErr"
    }

    return [ErrCheck $rcode MoveStartFile]    
}


####################################
####################################
#
# Communication mechanism between Silk and AceTest based on SMBMOUNT
#
#####################################
#####################################


##################
# MOUNT AND UMOUNT AceDir folder
##################

###################################
# MountSilkPcAceDir - attempts to mount AceDir folder from the SilkPC and verifies that this action was successful
#                     This folder will be mounted in <AceTest folder>/tmp/AceDir
# Variables:
#     winIP:       IP address of the PC running SILK
#     workgroup:   Silk PC workgroup   
#     user:        user
#     passwd:      password
#
#
###################################
proc MountSilkPcAceDir { winIP workgroup user passwd } {

    set rcode ""
    set rcode1 ""
    set fail 0

    #//ensure that AceDir is not already mounted
    if {[string match -nocase *ERR* [UmountSilkPcAceDir]] == 1} {
        LogFile "MountSilkPcAceDir ERR: AceDir already exists"
        return
    }

    #//create ./tmp/AceDir folder (current directory is <Ace Test dirctory>)

    file mkdir ./tmp/AceDir

    #//puts "smbmount //$winIP/AceDir ./tmp/AceDir -o workgroup=$workgroup,username=$user,password=$passwd"

    set mnt [catch {exec smbmount //$winIP/AceDir ./tmp/AceDir -o workgroup=$workgroup,username=$user,password=$passwd} errMount]   

    if {$mnt != 0} {
        set rcode1 "ERR smbmount: $errMount"
        incr fail
    }

    #//verify above actions. AceDir must contain: silktest and silkresult folders        
    set aceDir [glob -nocomplain tmp/AceDir]
    if {[string match -nocase "*AceDir*" $aceDir] != 1}  {        
        incr fail
    }    
    
    if {$fail != 0} {
        lappend rcode "$rcode1\n"
        lappend rcode "ERR: AceDir folder not mounted. Please verify that smbmount program is available on AceTest PC \n \
                            or/and c:\\_Projects\\sqa\\AceDir is fully shared with writing access"    
        return [ErrCheck $rcode MountSilkPcAceDir]
    }

    return [ErrCheck $rcode MountSilkPcAceDir]

}



#################################################################
# UmountSilkPcAceDir - umounts AceDir folder and removes it form <AceTest folder>/tmp
#
# Variables:
#
#
#################################################################
proc UmountSilkPcAceDir { } {

    set rcode ""
    set rcode1 ""
    set rcode2 ""

    set umnt [catch {exec smbumount ./tmp/AceDir} errUmount]

    if {$umnt != 0} {
        set rcode1 "ERR smbumount: $errUmount"
    }
        
    after 1000

    if {[catch {file delete -force ./tmp/AceDir} errDel] != 0} {
        set rcode2 "ERR del AceDir: $errDel"
    }

    #//verify above actions. ./tmp must not contain anymore AceDir folder
    set aceDirList [glob -nocomplain -path tmp/ AceDir]

    if {$aceDirList != ""} {

        lappend rcode "$rcode1\n"
        lappend rcode "$rcode1\n"        

    }

    return [ErrCheck $rcode UmountSilkPcAceDir]

}


############
# PROCEDURES USED FOR FILE EXCHANGE BETWEEN AceWin PC (Linux) and Silk PC (Windows)
############

###############################################
# CheckForRes - check for $testname.run file in <AceTest folder>/AceDir folder (the folder mounted from Silk PC)               
#             - if timeout expires and still no $testname.res file - return ERROR
#               
# Variables: 
#     testname
#     timeout 
#       
###############################################
proc CheckForRes { testname {timeout 60000} } {

    set resfile "$testname.result"

    for {set i 0} {$i <= $timeout} {incr i 1000} {        
        set resFile [glob -nocomplain ./tmp/AceDir/$testname.result]

#        puts "CheckForRes --- $i ---"

        if {[string match -nocase "*$resfile" $resFile] == 1} {                        
            return "SUCCESS"            
        }

        if {[info proc Ace:splash] != ""} {
            Ace:splash "Wait for $resfile ..." 1000
        } else {
            after 1000
            LogFile "Wait for $resfile ..."
        }

    }    

    lappend rcode "ERR: result file - $resfile - not generated after [expr $timeout/1000] seconds"
    return [ErrCheck $rcode CheckForRes]

}


###############################################
# CheckForRun - verifies that Silk test was successfully started by checking for $testname.run file in <AceTest folder>/AceDir folder 
#               (the folder mounted from Silk PC)                     
#             - if timeout expires and still no $testname.run file - returns ERROR
#               
# VARIABLES:
#     IN:
#     testname
#     timeout 
#
###############################################
proc CheckForRun { testname {timeout 60000} } {

    set rcode ""
    set resfile "$testname.run"  

    for {set i 0} {$i <= $timeout} {incr i 1000} {

#        puts "CheckForRun --- $i ---"

        set runFile [glob -nocomplain ./tmp/AceDir/$testname.run]

        if {[string match -nocase "*$resfile*" $runFile] == 1} {
            LogFile "Silk script - $testname - launched"
            return "SUCCESS"            
        }

        if {[info proc Ace:splash] != ""} {
            Ace:splash "Wait for $resfile ..." 1000
        } else {
            after 1000
            LogFile "Wait for $resfile ..."
        }

    }

    lappend rcode "ERR: Silk test $testname not started"
    return [ErrCheck $rcode CheckForRun]

}


################################################
# DelFile - deletes the $testname.result or $testname.run file (if any) from 
#           both Silk PC and AceTest PC. 
#           (it will delete the file from the folder mounted to the AceTest PC from the Silk PC)
#
# VARIABLES:
#     testname: the test name
#     filetype: type of the file you want to delete
#               Accepted values: result
#                                run
#
################################################
proc DelFile { testname filetype} {

    set rcode ""
    set resfile "$testname.$filetype"

    
    file delete -force "./tmp/AceDir/$resfile"

    if {[glob -nocomplain ./tmp/AceDir/$resfile] != ""} {
        set rcode "ERROR: fail to the remove $resfile file from ./tmp/AceDir"
    } else {
        set rcode "file $resfile - deleted from ./tmp/AceDir"
    }

    return [ErrCheck $rcode DelFile] 

}



########################################
# VerifyResFile - checks for error or success messages in sils result file
#                 Each silk test need to put a message : ===SUCCESS===SILK=== or ===ERROR===SILK=== in result file
#
########################################
proc VerifyResFile {testname} {

    set rcode ""
    set okFile [catch {set fileID [open ./tmp/AceDir/$testname.result r]} errOpen]
    if {$okFile != 0} {
        lappend rcode "ERR: $errOpen"
    } else {
        set results [read $fileID]
        foreach line $results {
            if {[regexp {===SUCCESS===SILK===} $line] == 1} {
                LogFile "Silk script - $testname.t - ended successfully"
            } elseif {[regexp {===ERROR===SILK===} $line] == 1} {
                lappend rcode "Silk script - $testname.t - BUG:\n$results"
            }
        }
    }
    
    catch {close $fileID}
    
    return [ErrCheck $rcode VerifyResFile]

}



######################################
# AceToSilkMsg
#
# sends a notification to Silk
#
######################################
proc AceToSilkMsg {} {
    set rcode ""
    if {[catch {close [open ./tmp/AceDir/acetosilk.ace w]} errOpen] != 0} {
        set rcode "ERR sending the notification to Silk:\n$errOpen"
    }
    
    return [ErrCheck $rcode AceToSilkMsg]

}


###########################
# WaitForSilkMsg
#
# waits for a notification from Silk
# AceTest considers that it got the notification when it finds the file - silktoace.silk -  
# 
# The prcedure will delete then the above file and will return.
#
# RETURN values:
#        SUCCESS - if AceTest gets the notification before the timeout expires
#        ERROR   - otherwise
#
###########################
proc WaitForSilkMsg { {timeout 300000} } {

    set rcode ""  

    for {set i 0} {$i <= $timeout} {incr i 1000} {

#        puts "CheckForRun --- $i ---"

        set msgFile [glob -nocomplain ./tmp/AceDir/silktoace.silk]

        if {[string match -nocase "*silktoace.silk*" $msgFile] == 1} {
            LogFile "Got the notification from Silk"
            set rcode "SUCCESS"            

            if {[info proc Ace:splash] != ""} {
                Ace:splash "Wait 5 seconds before delete the file - silktoace.silk -" 5000
            } else {
                after 3000
                LogFile "Wait 5 seconds before delete the file - silktoace.silk -"
                afteer 2000
            }            

            file delete -force "./tmp/AceDir/silktoace.silk"

            return [ErrCheck $rcode WaitForSilkMsg]
            
        }

        if {[info proc Ace:splash] != ""} {
            Ace:splash "Wait for a notification from Silk  ..." 1000
        } else {
            after 1000
            LogFile "Wait for a notification from Silk  ..."
        }

    }

    lappend rcode "ERR: the $timeout timeout expired and no notification from Silk"
    return [ErrCheck $rcode WaitForSilkMsg]
   
    

}



# ####################################
# ####################################
# #
# # Communication mechanism between Silk and AceTest based on FTP
# #
# #####################################
# #####################################


# ###################################
# #
# # START SILK TEST - by puting start file in the folder verified by silk main procedure
# #
# ###################################

# ############################
# #
# # Variables:
# #     folder - destination folder
# #     method - smbmnt or ftp
# #     host
# #     name
# #     pass
# #     
# #     
# #
# ############################
# proc PutStartFile {folder {method smbmnt} {host "NONE"} {name "NONE"} {pass "NONE"}} {
#     if {[string match -nocase "ftp" $method]} {
#         Open $host $name $pass
        
#         Put "./tmp/silk.start" "$folder/silk.start"
        
#         Close
#     } elseif {[string match -nocase "smbmnt" $method]} {
#         puts "PutStartFile WARNING: NOT YET IMPLEMENTED"
#     } else {
#         puts "PutStartFile ERROR: UNKNOWN METHOD"
#     }
# }


# ###############################################
# # CheckForRes - opens a FTP connection to the PC running Silk and waits until $testname.res file is put in
# #               ftproot\silkresults\ folder; get the file after Silk test ends and then delete the file (only on WIN PC)
# #             - if timeout expires and still no $testname.res file - return ERROR
# #               
# # Variables: 
# #     testname
# #     winIP
# #     name
# #     passwd
# #     timeout        
# #
# #
# #
# ###############################################
# proc CheckForRes { testname winIP name passwd {timeout 60000} } {

#     set resfile "$testname.result"

#     Open $winIP $name $passwd

#     Cd silkresults    

#     for {set i 1} {$i <= $timeout} {incr i 1000} {
#         set resfiles [List]
#         if {[regexp "$testname\.result" $resfiles] == 1} {            
#             LogFile "Get $resfile from Silk PC and put it in ./tmp/$resfile file"
#             Get $resfile ./tmp/$resfile            
#             return "SUCCESS"            
#         }
        
#         if {[info proc Ace:splash] != ""} {
#             Ace:splash "Wait for $resfile ..." 1000
#         } else {
#             after 1000
#             LogFile "Wait for $resfile ..."
#         }
#     }
    
#     LogFile "CheckForRes ERROR - exit without getting res file"
#     return "ERROR"

# }

# ###############################################
# # CheckForRun - opens a FTP connection to the PC running Silk and waits until $testname.res file is put in
# #               ftproot\silkresults\ folder; get the file after Silk test ends and then delete the file (only on WIN PC)
# #             - if timeout expires and still no $testname.res file - return ERROR
# #               
# # VARIABLES:
# #     testname
# #     winIP
# #     name
# #     passwd
# #     timeout 
# #
# #
# #
# ###############################################
# proc CheckForRun { testname winIP name passwd {timeout 60000} } {

#     set resfile "$testname.run"

#     Open $winIP $name $passwd

#     Cd silkresults    

#     for {set i 1} {$i <= $timeout} {incr i 1000} {
#         set resfiles [List]
#         if {[regexp "$testname\.run" $resfiles] == 1} {            
#             LogFile "Silk test $testname - is running"
#             return "SUCCESS"            
#         }
        
#         if {[info proc Ace:splash] != ""} {
#             Ace:splash "Wait for $resfile ..." 1000
#         } else {
#             after 1000
#             LogFile "Wait for $resfile ..."
#         }
#     }
    
#     return "ERROR"

# }


# ################################################
# # DelResFile - delete $testname.result (if any) even from Silk PC C:\...\silkresults folder
# #                                                 or from AceTest PC, <AceTest folder>/tmp folder
# #
# ################################################
# proc DelResFile { testname {winIP NONE} {name NONE} {passwd NONE}} {

#     set retCode "ERROR"
#     set resfile "$testname.result"

#     if {$winIP != "NONE"} {

#         Open $winIP $name $passwd
#         Cd silkresults
#         Delete $resfile

#         set resfiles [List]
#         if {[regexp $resfile $resfiles] == 1} {
#             set retCode "ERROR"
#         } else {
#             set retCode "SUCCESS"
#         }
        
#         Close

#     } elseif {$winIP == "NONE"} {
#         file delete -force "./tmp/$resfile"

#         if {[glob -nocomplain ./tmp/$resfile] != ""} {
#             set retCode "ERROR"
#         } else {
#             set retCode "SUCCESS"
#         }
#     }

#     return $retCode    
# } 


# ################################################
# # DelResFile - delete $testname.result (if any) even from Silk PC C:\...\silkresults folder
# #                                                 or from AceTest PC, <AceTest folder>/tmp folder
# #
# ################################################
# proc DelRunFile { testname winIP name passwd } {

#     set retCode "ERROR"
#     set runfile "$testname.run"

#     if {$winIP != "NONE"} {

#         Open $winIP $name $passwd
#         Cd silkresults
#         Delete $runfile

#         set resfiles [List]
#         if {[regexp $runfile $resfiles] == 1} {
#             set retCode "ERROR"
#         } else {
#             set retCode "SUCCESS"
#         }
        
#         Close
#     }

#     return $retCode    
# } 


