
proc logFile {args} {
    logMessage logDebug "$args\n"
}
proc testStartLog { testName } {
    logMessage logTest "\n\nTestCase:$testName starting\n"
}
proc testEndLog {args } {
    logMessage logTest "TestCase:$args\n"
}
proc testPurposeLog { purpose description } {
    logMessage logTest "Decription: $purpose\n"
    logMessage logTest "$description"
}
proc logCliFile { msg } {
    puts $msg
}


proc VerifyBoConnection {{bo_type ""} {number 4}} {

  variable swAddr1
  variable swAddr2

  variable ces1PrivateIp
  variable ces1PublicIp

  variable ces2PrivateIp
  variable ces2PublicIp

  variable boName_ces1
  variable boName_ces2

  if {[VerifyTunnel $swAddr1 $ces2PrivateIp $ces1PrivateIp $number] != "SUCCESS"} {
     logFile "CES: $swAddr1 - ping to $ces2PrivateIp from $ces1PrivateIp - no reply!" "FAIL"
     return "ERROR"
  } else {
     logFile "CES: $swAddr1 - ping to $ces2PrivateIp from $ces1PrivateIp - got reply!" "PASS"
  }

  if {[VerifyTunnel $swAddr2 $ces1PrivateIp $ces2PrivateIp $number] != "SUCCESS"} {
     logFile "CES: $swAddr2 - ping to $ces1PrivateIp from $ces2PrivateIp - no reply!" "FAIL"
     return "ERROR"
  } else {
     logFile "CES: $swAddr2 - ping to $ces1PrivateIp from $ces2PrivateIp - got reply!" "PASS"
  }

  if {$bo_type != ""} {
     if {[VerifyBoIsUp $boName_ces1 $swAddr1] != "YES"} {
        logFile "CES: $swAddr1 - BOT is not up" "FAIL"
        return "ERROR"
     } elseif {[GetBoType $boName_ces1 $swAddr1] != $bo_type} {
        logFile "CES: $swAddr1 - BOT is up but type is not $bo_type" "FAIL"
        return "ERROR"
     } else {
        logFile "CES: $swAddr1 - BOT is up and type is $bo_type" "PASS"
     }

     if {[VerifyBoIsUp $boName_ces2 $swAddr2] != "YES"} {
        logFile "CES: $swAddr2 - BOT is not up" "FAIL"
        return "ERROR"
     } elseif {[GetBoType $boName_ces2 $swAddr2] != $bo_type} {
        logFile "CES: $swAddr2 - BOT is up but type is not $bo_type" "FAIL"
        return "ERROR"
     } else {
        logFile "CES: $swAddr2 - BOT is up and type is $bo_type" "PASS"
     }
  }

  return "SUCCESS"

}

proc VerifyTunnel {swAddr destinationIp sourceIp {number 4}} {
  for {set i 1} { $i <= $number } {incr i} {
     if {[CesPing $swAddr $destinationIp $sourceIp] == "SUCCESS"} {
        return "SUCCESS"
     }
     if {$i != $number} {
        aceWait 10000
     }
  }
  return "ERRPING"
}

proc aceWait {time {message ""}} {
  puts "\n"
  for {set i $time} {$i>0} {incr i -1000} {
     puts -nonewline " $message - wait [expr $i/1000] seconds  \r"
     flush stdout
     after 1000
  }
}

proc bootBuild {build} {

  variable swAddr2

  variable ces2ManagementIp
  variable ces2MngIfIp
  variable ces2PrivateIp
  variable ces2PrivateSlot
  variable ces2PublicIp
  variable ces2PrivateSlot
  variable ces2PublicSlot

  variable ces2_ldap_file

  variable boGroup

  variable calvinBuild

  variable ces2_currentSwVer

  if {[GetSwitchSWVerNum_exp $swAddr2] != $build} {
     if {[BootSystem $swAddr2 $build] == "SUCCESS"} {
        if { $build == $calvinBuild } {
           CesConnectAndSetup $swAddr2 $ces2ManagementIp $ces2MngIfIp $ces2PrivateSlot $ces2PrivateIp $ces2PrivateSlot $ces2PublicIp $ces2PublicSlot $ces2_ldap_file "yes"
        } else {
           CesConnectAndSetup $swAddr2 $ces2ManagementIp $ces2MngIfIp $ces2PrivateSlot $ces2PrivateIp $ces2PrivateSlot $ces2PublicIp $ces2PublicSlot $ces2_ldap_file
        }

        AddBoGroup $boGroup $swAddr2

        EnaIpsecEncrType $swAddr2 "all"
        EnaIpsecIkeEncrType $swAddr2 "all"

        EnaBoGrpEncrType $swAddr2 $boGroup "3des-md5"
        set ces2_currentSwVer $build
     }
  }
}

testEndLog "ceslib.tcl" "PASS"
return "PASS"
