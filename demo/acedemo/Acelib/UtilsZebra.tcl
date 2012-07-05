# Procedures relative to Zebra application
#
#########
# ospfd
#########
# ZebraSetNetworkAreaId {prompt network ariaId}
# ZebraDelNetworkAreaId {prompt network ariaId}
# OspfZebraAreaStub {prompt ariaId host}
# OspfZebraAreaNoStub {prompt ariaId host}
# RipZebraNoRedistributeConnected {prompt host}
# RipZebraRedistributeConnected {prompt host}
# OspfZebraVerifyLSID {prompt lsidType lsid routerID areaId host}
########################################################

proc ZebraSetNetworkAreaId {prompt network ariaId host} {
    SetZebraCliLevel $prompt "CONFIG" $host
    ExecZebra $prompt "router ospf" "CONFIGROUTER" $host
    ExecZebra $prompt "network $network area $ariaId" "CONFIGROUTER" $host
    SetZebraCliLevel $prompt "USER" $host
}

proc ZebraDelNetworkAreaId {prompt network ariaId host} {
    SetZebraCliLevel $prompt "CONFIG" $host
    ExecZebra $prompt "router ospf" "CONFIGROUTER" $host
    ExecZebra $prompt "no network $network area $ariaId" "CONFIGROUTER" $host
    SetZebraCliLevel $prompt "USER" $host
}

proc OspfZebraAreaStub {prompt ariaId host} {
    SetZebraCliLevel $prompt "CONFIG" $host
    ExecZebra $prompt "router ospf" "CONFIGROUTER" $host
    ExecZebra $prompt "area $ariaId stub" "CONFIGROUTER" $host
    SetZebraCliLevel $prompt "USER" $host
}

proc OspfZebraAreaNoStub {prompt ariaId host} {
    SetZebraCliLevel $prompt "CONFIG" $host
    ExecZebra $prompt "router ospf" "CONFIGROUTER" $host
    ExecZebra $prompt "no area $ariaId stub" "CONFIGROUTER" $host
    SetZebraCliLevel $prompt "USER" $host
}

proc RipZebraNoRedistributeConnected {prompt host} {
    SetZebraCliLevel $prompt "CONFIG" $host
    ExecZebra $prompt "router rip" "CONFIGROUTER" $host
    ExecZebra $prompt "no redistribute connected" "CONFIGROUTER" $host
    SetZebraCliLevel $prompt "USER" $host
}

proc RipZebraRedistributeConnected {prompt host} {
    SetZebraCliLevel $prompt "CONFIG" $host
    ExecZebra $prompt "router rip" "CONFIGROUTER" $host
    ExecZebra $prompt "redistribute connected" "CONFIGROUTER" $host
    SetZebraCliLevel $prompt "USER" $host
}


proc OspfZebraVerifyLSID {prompt lsidType lsid routerID areaId host} {
    global cmdOut

    set cmdOut ""
    set linkState ""
    set rcode ""

    SetZebraCliLevel $prompt "PRIVILEGE" $host
    ExecZebra $prompt "show ip ospf database" "PRIVILEGE" $host

    regexp "$lsidType Link States \\(Area $areaId\( \\\[Stub\\\])\?\\).*?\(States\)" $cmdOut linkState

    if {$linkState == ""} {
        regexp "$lsidType Link States \\(Area $areaId\( \\\[Stub\\\]\)?\\).*" $cmdOut linkState
    }
    
    if {$lsidType == "AS External"} {
        regexp "$lsidType Link States.*" $cmdOut linkState
    }

    if {$linkState == ""} {
        lappend rcode "ERROR: LSID type or Area ID don't exist!"
        return [ErrCheck $rcode "OspfZebraVerifyLSID"]
    }

    foreach line [split $linkState "\n"] {
        if { [regexp -nocase "$lsid\[\t\ \]+$routerID" $line] == 1} {
            return "YES"
        }
    }
    return "NO"
}
