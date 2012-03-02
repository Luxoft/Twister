##########################################
# 
#
# RemoteStaticRoute { action dest mask gateway host {port 10500} }
# ClientReader_RemoteRoute { sock }
#
# 
#
##########################################


##########################
# remote static route
################################################################################

##########################################
# RemoteStaticRoute
#
# Description: - tells the AceAgent running on the $host PC to add or delete a static route
# 
# Variables: 
#    IN: action: "route add", route del"
#
#
###########################################
proc RemoteStaticRoute { action dest mask gateway host {port 10500} } {
    global okRemoteRoute

    set rcode ""

    if {[catch {set sockID [socket $host $port]} sockErr] != 0} {                       
        lappend rcode "ERROR: - Fail to open the connections to AceAgent server running on $host, port $port"        
        lappend rcode "$sockErr"
        return [ErrCheck $rcode AddRStaticRoute]
    }    

    fconfigure $sockID -blocking 0
    fileevent $sockID readable [list ClientReader_RemoteRoute $sockID]
    


    #//send the info relating to static route
    puts $sockID "action: $action"
    puts $sockID "dest: $dest"
    puts $sockID "mask: $mask"
    puts $sockID "gateway: $gateway"

    flush $sockID

    #safe guard
    set afterID [after 20000 {set okRemoteRoute "no"}]

    set okRemoteRoute 0

    vwait okRemoteRoute
    after cancel $afterID

    #//close the socket
    catch {close $sockID}

    #verify remote route 

    switch $action {

        "route add" {
            switch $okRemoteRoute {
                "OK" {
                    lappend rcode "OK adding the static route on host $host"
                }
                default {
                    lappend rcode "ERR: fail to add the route on host $host"
                }        
            }
        }

        "route del" {
            switch $okRemoteRoute {
                "noRoute" {
                    lappend rcode "OK: delete the static route on host $host"
                }
                default {
                    lappend rcode "ERR: fail to delete the static route on host $host"
                }        
            }            
        }

        
    }


    return [ErrCheck $rcode AddRStaticRoute]

}

###############################
# ClientReader_RemoteRoute - the procedure called in RemoteStaticRoute proc when the socket becomes readable 
# 
#
#
###############################
proc ClientReader_RemoteRoute { sock } {
    global okRemoteRoute

    set rcvStr ""

    while { [set data [read $sock]] != "" } {
        append rcvStr $data
    }
    LogFile "AceAgentClient: received message:\n-----\n$rcvStr\n-----"    

    if {[regexp "okRoute" $rcvStr]} {
        set okRemoteRoute "OK"
        return
    }

    if {[regexp "noRoute" $rcvStr]} {
        set okRemoteRoute "noRoute"
        return
    }
        
    set okRemoteRoute "who knows"
    return

}


##########################
# remote pppoe-server
################################################################################
##########################################
# RemotePppoeServer
#
# Description: - tells the AceAgent running on the $host PC to start/stop the pppoe-server
#                If action = pppoe-server stop, the Ace Agent stops all the pppoe servers and all the pppoe processes.
#                 The parameters: - interface, local and remote - are not important in this case. 
#                 Set each of them to "all"
#
# Variables: 
#    IN: action:    the thing to do: "pppoe-server start", "pppoe-server stop"
#        interface: the Ethernet interface to use
#        local:     the IP  address to use by the pppoe-server. This  is passed to spawned pppd processes.  
#        remote:    the IP address from which the pppoe-server starts to assign IP addresses.
#        host:      the IP address of the Linux PC running the pppoe-server
#
#
###########################################
proc RemotePppoeServer { action interface local remote host {port 10500} } {
    global okRemote

    set rcode ""

    if {[catch {set sockID [socket $host $port]} sockErr] != 0} {                       
        lappend rcode "ERROR: - Fail to open the connections to AceAgent server running on $host, port $port"        
        lappend rcode "$sockErr"
        return [ErrCheck $rcode AddRStaticRoute]
    }    

    fconfigure $sockID -blocking 0
    fileevent $sockID readable [list ClientReader_RemotePppoe $sockID]
    

    #//send the info relating to static route        
    puts $sockID "action: $action"
    
    switch $action {
        "pppoe-server start" {            
            puts $sockID "I: $interface"
            puts $sockID "L: $local"
            puts $sockID "R: $remote"
        }
        "pppoe-server stop" {
            #//just action is used at this moment
        }

    }

    flush $sockID

    #safe guard
    set afterID [after 20000 {set okRemoteServer "no"}]

    set okRemote 0

    vwait okRemote
    after cancel $afterID

    #//close the socket
    catch {close $sockID}

    #verify remote route 

    switch $action {

        "pppoe-server start" {
            switch $okRemote {
                "ok" {
                    lappend rcode "OK: started pppoe-server on host $host"
                }
                default {
                    lappend rcode "ERR: fail to start pppoe-server on host $host"
                }        
            }
        }

        "pppoe-server stop" {
            switch $okRemote {
                "no" {
                    lappend rcode "OK: stopped pppoe-server on host $host"
                }
                default {
                    lappend rcode "ERR: fail to stop pppoe-server on host $host"
                }        
            }            
        }

        
    }


    return [ErrCheck $rcode RemotePppoeServer]

}

###############################
# ClientReader_RemoteRoute - the procedure called in RemoteStaticRoute proc when the socket becomes readable 
# 
#
#
###############################
proc ClientReader_RemotePppoe { sock } {
    global okRemote

    set rcvStr ""

    while { [set data [read $sock]] != "" } {
        append rcvStr $data
    }
    LogFile "AceAgentClient: received message:\n-----\n$rcvStr\n-----"    

    if {[regexp "ok" $rcvStr]} {
        set okRemote "ok"
        return
    }

    if {[regexp "no" $rcvStr]} {
        set okRemote "no"
        return
    }
        
    set okRemote "who knows"
    return

}
