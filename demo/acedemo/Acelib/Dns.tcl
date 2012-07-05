###############
# DNS library 
#
# SetDnsProxy { state host}
# GetDnsProxy { host }
# SetHostName { name host } 
# GetHostName { host } 
# SetDomainName { domainName host }
# GetDomainName { host }
# SetDnsServers { dnsIpList host }
# GetDnsServers { host }
# GetSupportedDnsServers { host }
# SetPrimaryDnsServer { serverIp host }
# SetSecondaryDnsServer { serverIp host }
# SetTertiaryDnsServer { serverIp host }
# SetFourthDnsServer { serverIp host }
# SetSplitDNS { state host }
# GetSplitDns { host }
# GetIpNameServerInfo { infoToGet host {state NO} }
###############


##############################################
# SetDnsProxy sets DNS-Proxy
#
# Variables:
#   IN:
#           state: dns proxy state; supported values: enabled, no_enabled
#           host : management IP address of the switch (or terminal server IP:port )
#   
#   OUT:
#           SUCCESS ERROR or ERRORBADINPUT. No variables are modified.          
#          
##############################################
proc SetDnsProxy { state host } {    
    set errCode "ERROR"
    set rcode ""
    
    set state [string tolower $state]

    if { [SetCliLevel "CONFIG" $host] != "SUCCESS" } {
        lappend rcode "ERROR: Failed SetCliLevel"
        return [ErrCheck $rcode SetDnsProxyState] 
    }
    
    if {$state == "enable"} {
        set errCode [Exec "dns-proxy enable" "CONFIG" $host]
    } elseif {$state == "no_enable"} {
        set errCode [Exec "no dns-proxy enable" "CONFIG" $host]
    } else {
        lappend rcode "ERROR: $state - unsupporter value; must be: enable/no_enable"
        ErrCheck $rcode SetDnsProxyState
        set errCode "ERRORBADINPUT"
    }
    
    return $errCode

}

proc GetDnsProxy { host } {
    global cmdOut

    set state "NOTGOT"

    if { [SetCliLevel "PRIVILEGE" $host] != "SUCCESS" } {
        lappend rcode "ERROR: Failed SetCliLevel"
        return [ErrCheck $rcode GetDnsProxyState] 
    }
    
    Exec "show running-config system identity" "PRIVILEGE" $host
    foreach line [split $cmdOut "\r"] {
        if { [regexp "(dns-proxy )(.*)" $line all m1 m2] == 1 } {
            set state $m2
        } 
    }

    if {$state == "NOTGOT"} {
        lappend rcode "ERROR: failed to get dns-proxy state.\n------ \n$cmdOut \n------"        
        return [ErrCheck $rcode GetDnsProxyState] 
    }

    return $state
}


proc SetHostName { name host } {    
    if { [SetCliLevel "CONFIG" $host] != "SUCCESS" } {
        lappend rcode "ERROR: SetHostName: Failed SetCliLevel"
        return [ErrCheck $rcode SetHostName] 
    }
    Exec "hostname $name" "CONFIG" $host
}

proc GetHostName { host } {
    global cmdOut
    if { [SetCliLevel "PRIVILEGE" $host] != "SUCCESS" } {
        lappend rcode "ERROR: GetHostName: Failed SetCliLevel"
        return [ErrCheck $rcode GetHostName] 
    }
    Exec "show hosts" "PRIVILEGE" $host
    foreach line [split $cmdOut "\r"] {
        if { [regexp "(DNS Host Name: )(.*)" $line all m1 m2] == 1 } {
            set hostName $m2
        }
    }
    return $hostName
}

proc SetDomainName { domainName host } {
    if { [SetCliLevel "CONFIG" $host] != "SUCCESS" } {
        lappend rcode "ERROR: SetDomainName: Failed SetCliLevel"
        return [ErrCheck $rcode SetDomainName] 
    }
    Exec "ip domain-name $domainName" "CONFIG" $host
}


proc GetDomainName { host } {
    global cmdOut    
    if { [SetCliLevel "PRIVILEGE" $host] != "SUCCESS" } {        
        lappend rcode "ERROR: GetDomainName: Failed SetCliLevel"
        return [ErrCheck $rcode GetDomainName] 
    }
    Exec "show hosts" "PRIVILEGE" $host
    foreach line [split $cmdOut "\r"] {
        if { [regexp "(DNS Domain Name: )(.*)" $line all m1 m2] == 1 } {
            set domainName $m2
        }
    }
    return $domainName
}

proc SetDnsServers { dnsIpList host } {
    if { [SetCliLevel "CONFIG" $host] != "SUCCESS" } {
        lappend rcode "ERROR: SetDnsServers: Failed SetCliLevel"
        return [ErrCheck $rcode GetDomainName] 
    }
    Exec "ip name-server $dnsIpList" "CONFIG" $host    
}

##################################################
# GetDnsServers - gets configured DNS servers using -show hosts- cli command
#
# Variables: 
#   IN:
#            host:        management IP address of the switch (or terminal server IP:port )
#            returnType:  values: YES/NO, default NO; specified the type of return code
#
#   OUT:     a list with IP addresses of the DNS servers (if returnType != ALL)
#            - if a certain DNS server (primary ... fourth) not exists in the output of the - show hosts - CLI command, 
#              the above list will contain NOT_SUPORT instead the IP address of the server;
#
#            the entire output of -show hosts- CLI command (returnType = ALL)
#
#            ERROR 
#
##################################################
proc GetDnsServers { host {returnType "DNSLIST"}} {
    global cmdOut
    if { [SetCliLevel "PRIVILEGE" $host] != "SUCCESS" } {
        lappend rcode "ERROR: GetDnsServers: Failed SetCliLevel"
        return [ErrCheck $rcode GetDomainName] 
    }
    if {[Exec "show hosts" "PRIVILEGE" $host] != "SUCCESS"} {
        return "ERROR"
    }

    if {$returnType == "ALL"} {
        return $cmdOut
    }

    set primary "NOT_SUPPORT"
    set secondary "NOT_SUPPORT"
    set tertiary "NOT_SUPPORT"
    set fourth "NOT_SUPPORT"

    foreach line [split $cmdOut "\r"] {

        if { [regexp "(primary: )(\[0-9\]+\.\[0-9\]+\.\[0-9\]+\.\[0-9\]+)" $line all m1 m2] == 1 } {            
            set primary $m2
        }
        if { [regexp "(secondary: )(\[0-9\]+\.\[0-9\]+\.\[0-9\]+\.\[0-9\]+)" $line all m1 m2] == 1 } {
            set secondary $m2
        }        
        if { [regexp "(tertiary: )(\[0-9\]+\.\[0-9\]+\.\[0-9\]+\.\[0-9\]+)" $line all m1 m2] == 1 } {
            set tertiary $m2
        } 
        if { [regexp "(fourth: )(\[0-9\]+\.\[0-9\]+\.\[0-9\]+\.\[0-9\]+)" $line all m1 m2] == 1 } {
            set fourth $m2
        } 
    }

    return [list $primary $secondary $tertiary $fourth]
    
}

######################################
# GetSupportedDnsServers uses the "show hosts" switch command in order to
#       get the number of DNS servers that can be configured on the swich
#
# Variables:
#   IN: 
#           host:   IP address of the switch (or terminal server IP:port)
#
#   OUT:
#           the number of DNS servers displayed by "show hosts" command
#
######################################
proc GetSupportedDnsServers { host } {

    set count 0

    set supportedDnsList [GetDnsServers $host]
    foreach elem $supportedDnsList {
        if {$elem != "NOT_SUPPORT"} {
            incr count
        }
    }
    
    return $count

}


proc SetPrimaryDnsServer { serverIp host } {
    if { [SetCliLevel "PRIVILEGE" $host] != "SUCCESS" } {
        lappend rcode "ERROR: SetPrimaryDnsServer: Failed SetCliLevel"
        return [ErrCheck $rcode SetPrimaryDnsServer] 
    }

    SetDnsServers $serverIp $host
}

proc SetSecondaryDnsServer { serverIp host } {
    if { [SetCliLevel "PRIVILEGE" $host] != "SUCCESS" } {
        lappend rcode "ERROR: SetSecondaryDnsServer: Failed SetCliLevel"
        return [ErrCheck $rcode SetSecondaryDnsServer] 
    }
    set currentServers [GetDnsServers $host]
    set newServers [list [lindex $currentServers 0] $serverIp]
    SetDnsServers $newServers $host
}

proc SetTertiaryDnsServer { serverIp host } {
    if { [SetCliLevel "PRIVILEGE" $host] != "SUCCESS" } {
        lappend rcode "ERROR: SetTertiaryDnsServer: Failed SetCliLevel"
        return [ErrCheck $rcode SetTertiaryDnsServer] 
    }
    set currentServers [GetDnsServers $host]
    set newServers [list [lindex $currentServers 0] [lindex $currentServers 1] $serverIp ]
    SetDnsServers $newServers $host
}

proc SetFourthDnsServer { serverIp host } {
    if { [SetCliLevel "PRIVILEGE" $host] != "SUCCESS" } {
        lappend rcode "ERROR: SetFourthDnsServer: Failed SetCliLevel"
        return [ErrCheck $rcode SetFourthDnsServer] 
    }
    set currentServers [GetDnsServers $host]
    set newServers [list [lindex $currentServers 0] [lindex $currentServers 1] [lindex $currentServers 2] $serverIp ]
    SetDnsServers $newServers $host
}


#######################################
# SetSplitDNS - configure Split DNS
#
# IN:  state: <enable/no_enable>; split DNS state
#      host : (management IP)/(terminal server Ip:port)
#   
# OUT: SUCCESS/ERROR/ERRORBADINPUT   
#######################################
proc SetSplitDns { state host } {

    set errCode "ERROR"
    set rcode ""

    set state [string tolower $state]

    if { [SetCliLevel "CONFIG" $host] != "SUCCESS" } {
        lappend rcode "ERROR: Failed SetCliLevel"
        return [ErrCheck $rcode SetSplitDNS] 
    }
    
    if {$state == "enable"} {
        set errCode [ Exec "split-dns enable" "CONFIG" $host]
    } elseif {$state == "no_enable"} {
        set errCode [Exec "no split-dns enable" "CONFIG" $host]
    } else {
        lappend rcode "ERROR: $state - unsupporter value; must be: enable/no_enable"
        ErrCheck $rcode SetSplitDNS
        set errCode "ERRORBADINPUT"
    }
    
    return $errCode

}


#############################################################
# GetSplitDns: Gets the Split Dns state.
#
# IN:  host: (management IP)/(terminal server Ip:port)
#
# OUT: ERROR / <Split DNS state>
#############################################################
proc GetSplitDns { host } {
   global cmdOut

   set err_count [GetGlobalErr]

   set state "NONE"

   SetCliLevel "PRIVILEGE" $host
   
   Exec "show running-config system identity" "PRIVILEGE" $host

   foreach line [split $cmdOut "\r"] {

      if {[regexp {split-dns[\ \t]+([a-zA-Z_-]+)} $line all state] == 1} {
         #puts "state = $state"
         #puts "line  = $line"         
      } 
   }

   if {$state == "NONE"} {
      ErrCheck "ERROR: failed to get split-dns state.\n------ \n$cmdOut \n------"        
   }

   if {[CheckGlobalErr $err_count] != "SUCCESS"} {
      return "ERROR"
   } else {
      return $state   
   }
}


##############################################################
# GetIpNameServerInfo - returns the specified information from the output displayed by 
#    CLI command: CES#show ip name-server
# 
# Variables: 
#   IN:    
#           infoToGet: the data you want to get 
#                      Supported values:
#                                        dnsProxyState/dnsSplitState/primary/secondary/tertiary/fourth/ISP/ALL                            
#           host:      management IP address of the switch (or terminal server IP:port )
#           status:    return also the status of the specified DNS server if available. 
#                      (usualy the status is not available for ISP proviced DSN servers)
#
#   OUT:
#          <dnsProxyState>
#          <dnsSplitState>
#          <DNS server IP> - wheh state = NO
#          {<DNS server IP> <DNS server status>} - when state = YES
#
#          ERROR 
#    
###############################################################
proc GetIpNameServerInfo { infoToGet host {state NO} } {

    global cmdOut
    
    set returnCode "NONE"
    set rcode ""

    set infoToGet [string tolower $infoToGet]    

    if { [SetCliLevel "PRIVILEGE" $host] != "SUCCESS" } {
        lappend rcode "ERROR: Failed SetCliLevel"
        return [ErrCheck $rcode SetSplitDNS] 
    }

    set ispCount 0
    set okIsp 0

    set proxyInfo "NO"
    set splitInfo "NO"
    set primaryInfo "NO"
    set secondInfo "NO"
    set thirdInfo "NO"
    set fourthInfo "NO"
    set ispInfo "NO"
    

    #issue CLI command: CES#show ip name-server    
    if {[Exec "show ip name-server" "PRIVILEGE" $host] != "SUCCESS"} {
        set returnCode "ERROR"
        return $returnCode
    }

    if {$infoToGet == "all"} {
        return $cmdOut
    }

    # else DO:
    set cmdOutLines [split $cmdOut "\n"]
    foreach line $cmdOutLines {
        #DNS proxy and split
        if {[regexp -nocase {DNS Proxy State[\ \t]*:[\ \t]*([A-Za-z]*)} $line all dns_Proxy_State] == 1} {
            set proxyInfo "YES"            
        }
        if {[regexp -nocase {Split DNS State[\ \t]*:[\ \t]*([A-Za-z]*)} $line all dns_Split_State] == 1} {
            set splitInfo "YES"            
        }

        #primary second third fourth DNS servers
        if {[regexp -nocase {Primary[\ \t]*:[\ \t]*(([0-9]+\.?)+)[\ \t]([A-Za-z\ \t]+)} $line all 1IP ipC 1State] == 1} {
            set primaryInfo "YES"
        }
        if {[regexp -nocase {Second Server[\ \t]*:[\ \t]*(([0-9]+\.?)+)[\ \t]([A-Za-z\ \t]+)} $line all 2IP ipC 2State] == 1} {
            set secondInfo "YES"
        }
        if {[regexp -nocase {Third Server[\ \t]*:[\ \t]*(([0-9]+\.?)+)[\ \t]([A-Za-z\ \t]+)} $line all 3IP ipC 3State] == 1} {            
            set thirdInfo "YES"
        }
        if {[regexp -nocase {Fourth Server[\ \t]*:[\ \t]*(([0-9]+\.?)+)[\ \t]([A-Za-z\ \t]+)} $line all 4IP ipC 4State] == 1} {
            set fourthInfo "YES"
        }

        #ISP provided DNS servers
        if {[regexp -nocase {ISP Provided DNS Servers} $line] == 1} {
            set okIsp 1
            
        }
        if {$okIsp > 0} {
            if {[regexp -nocase {DHCP Client Interface (([0-9]+\.?)+) Provided Servers:} $line] == 1} {
                incr ispCount
                set ispDnsList[set ispCount] ""
                continue
            }            
            if {$ispCount > 0} {
                set ispInfo "YES"
                if {[regexp {(([0-9]+\.?)+)} $line all ispIP[set ispCount]] == 1} {
                    #puts $line
                    lappend ispDnsList$ispCount [set ispIP$ispCount]                    
                }                
            }
        }        
    }
    
    switch $infoToGet {
        "dnsproxystate" {            
            if {$proxyInfo == "YES"} {
                set returnCode ${dns_Proxy_State}
            }
        }
        "dnssplitstate" {
            if {$splitInfo == "YES"} {
                set returnCode ${dns_Split_State}
            }
        }
        "primary" {
            if {$primaryInfo == "YES"} {
                if {$state == "YES"} {
                    set returnCode "$1IP $1State"
                } else {
                    set returnCode $1IP
                }
            }
        } 
        "secondary" {
            if {$secondInfo == "YES"} {
                if {$state == "YES"} {
                    set returnCode "$2IP $2State"
                } else {
                    set returnCode $2IP
                }
            }
        }
        "tertiary" {
            if {$thirdInfo == "YES"} {
                if {$state == "YES"} {
                    set returnCode "$3IP $3State"
                } else {
                    set returnCode $3IP
                }
            }
        }
        "fourth" {
            if {$fourthInfo == "YES"} {
                if {$state == "YES"} {
                    set returnCode "$4IP $4State"
                } else {
                    set returnCode $4IP
                }
            }
        }
        "isp" {
            if {$ispInfo == "YES"} {
                #puts "ispCount == $ispCount"
                set returnCode ""
                for {set i 1} {$i <= $ispCount} {incr i} {
                    lappend returnCode [set ispDnsList$ispCount]
                }
                if {$returnCode == ""} {
                    set returnCode "NONE"
                }
            }
        }
        default {
            LogFile "ERROR: proc GetIpNameServerInfo: unsupported option: infoToGet = $infoToGet; \
                    \nmust be one of: dnsProxyState, dnsSplitState, primary, secondary, tertiary, fourth, isp;\
                    " error            
            set returnCode "NOTSUPPORTED"
        }

    }          

    return $returnCode
}

##############################################################
# SaveSystemIdentity - saves the configuration relating to system identity into a file
#
# Variables:
#   IN:
#           file: the name of the file - without path;
#           host: management IP address of the switch (or terminal server IP:port )
#
#   OUT:    SUCCESS or ERROR
#
##############################################################
proc SaveSystemIdentity {file host} {
    if { [SetCliLevel "PRIVILEGE" $host] != "SUCCESS" } {
        lappend rcode "ERROR: Failed SetCliLevel"
        return [ErrCheck $rcode GetDnsProxyState] 
    }
    
    return [Exec "show running-config file-url $file system identity" "PRIVILEGE" $host]    

}

################################
# CLIDnsZeroSetup - restores the default DNS setup:
#     - all DNS IPs = 0.0.0.0
#     - dns Proxy   = enable
#     - dns Split   = disable
#
################################
proc CLIDnsZeroSetup { host } {

    SetDnsProxy "enable" $host
    SetSplitDNS "no_enable" $host  
    SetDnsServers "0.0.0.0 0.0.0.0 0.0.0.0 0.0.0.0" $host

}
