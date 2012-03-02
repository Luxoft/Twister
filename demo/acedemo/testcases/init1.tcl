
lappend auto_path $env(ACE_PATH)

package require Acelib
package require Expect

global dut1
global dut2


proc init_vars {} {
    global dut1
    global dut2

    set dut1 [createEmptyResource 0]
    set dut2 [createEmptyResource 0]
    #Set DUT1 variables
    setProperty $dut1 "TerminalServerIp"    "11.126.20.192"
    setProperty $dut1 "TerminalServerPort"  "5014"
    setProperty $dut1 "cesAdminName"        "admin"
    setProperty $dut1 "cesAdminPass"        "setup"
    setProperty $dut1 "dut1-mng-ip"         "11.1.1.1"
    setProperty $dut1 "dut1-mng-private-ip" "11.1.1.2"
    setProperty $dut1 "private-if"          "0/1"
    setProperty $dut1 "dut1-public-eth-ip"  "15.1.1.3"
    setProperty $dut1 "public-eth-if"       "1/1"
    setProperty $dut1 "dut1-ldap-file"      "CES1CERT.LDP"
    setProperty $dut1 "private-key-pass"    "contivity"
    setProperty $dut1 "calvin-build"        "V04_70.801"

    #Set DUT2 variables
    setProperty $dut2 "TerminalServerIp"    "11.126.20.192"
    setProperty $dut2 "TerminalServerPort"  "5013"
    setProperty $dut2 "cesAdminName"        "admin"
    setProperty $dut2 "cesAdminPass"        "setup"
    setProperty $dut2 "dut2-mng-ip"         "20.1.1.1"
    setProperty $dut2 "dut2-mng-private-ip" "20.1.1.2"
    setProperty $dut2 "private-if"          "0/1"
    setProperty $dut2 "dut2-public-eth-ip"  "15.1.1.2"
    setProperty $dut2 "public-eth-if"       "1/1"
    setProperty $dut2 "dut2-ldap-file"      "CES2CERT.LDP"
    setProperty $dut2 "private-key-pass"    "contivity"
    setProperty $dut2 "calvin-build"        "V04_70.801"
}


proc setup_ace {resetdefault} {
  #// Assign variables
  global DUT_SwVer
  global logDir
  global dut1
  global dut2
  #//start CLI LOG file
  ### Replace this by python API ### variable cliFileId [StartCLILog "CLI.log" $logDir]

  variable suiteName "BO"
  ### Replace this by python API ### suiteStartLog $suiteName

  ###Init resource allocator client variables
  init_vars

  #//interfaces IDs

  #//get from canvas the IP or IP:Port for management links
  set ces1_ip [getProperty $dut1 TerminalServerIp]
  set ces1_port [getProperty $dut1 TerminalServerPort]
  variable swAddr1 "$ces1_ip:$ces1_port"
  set ces2_ip [getProperty $dut2 TerminalServerIp]
  set ces2_port [getProperty $dut2 TerminalServerPort]
  variable swAddr2 "$ces2_ip:$ces2_port"
  puts $swAddr1
  puts $swAddr2

  variable ces1ManagementIp [getProperty $dut1 dut1-mng-ip]
  variable ces1MngIfIp [getProperty $dut1 dut1-mng-private-ip]
  variable ces1PrivateSlot [getProperty $dut1 private-if]
  variable ces1PublicIp [getProperty $dut1 dut1-public-eth-ip]
  variable ces1PublicSlot [getProperty $dut1 public-eth-if]

  #// variable ces1NatIp is used for Nat control tunnel test in Ces1 (T-106)
  variable ces1NatIp 1.1.1.1
  variable ces1_ldap_file [getProperty $dut1 dut1-ldap-file]

  ########
  # Uncomment the line below if you are using another card instead of management card as private interface
  ########
  #variable ces1PrivateIp [Global:getlist dut1-private-ip]
  ########
  # Comment the line below if you are using another card instead of management card as private interface
  ########
  variable ces1PrivateIp $ces1MngIfIp

  variable ces2ManagementIp [getProperty $dut2 dut2-mng-ip]
  variable ces2MngIfIp [getProperty $dut2 dut2-mng-private-ip]
  variable ces2PrivateSlot [getProperty $dut2 private-if]
  variable ces2PublicIp [getProperty $dut2 dut2-public-eth-ip]
  variable ces2PublicSlot [getProperty $dut2 public-eth-if]
  variable ces2_ldap_file [getProperty $dut2 dut2-ldap-file]
  ########
  # Uncomment the line below if you are using another card instead of management card as private interface
  ########
  #variable ces2PrivateIp [Global:getlist dut2-private-ip]
  ########
  # Comment the line below if you are using another card instead of management card as private interface
  ########
  variable ces2PrivateIp $ces2MngIfIp

  #//SW passwd and name
  variable cesAdminName [getProperty $dut1 cesAdminName]
  variable cesAdminPass [getProperty $dut1 cesAdminPass]

  variable arLicense "AR-7570301-DCCC029153-BF"

  variable boGroup "/Base/BOTest"
  variable boName_ces1 "tunnel_test_1"
  variable boName_ces2 "tunnel_test_2"
  variable textPass "abcdefgh"
  variable hexPass "ffaaff"
  variable initiator_uid "init_test"

  variable private_key_pass [getProperty $dut1 private-key-pass]

if $resetdefault {
    # This takes a looong time!
    CesConnectAndSetup $swAddr1 $ces1ManagementIp $ces1MngIfIp $ces1PrivateSlot $ces1PrivateIp $ces1PrivateSlot $ces1PublicIp $ces1PublicSlot $ces1_ldap_file
    AddBoGroup $boGroup $swAddr1

    EnaIpsecEncrType $swAddr1 "all"
    EnaIpsecIkeEncrType $swAddr1 "all"
    EnaBoGrpEncrType $swAddr1 $boGroup "3des-md5"

    # This takes a looong time!
    CesConnectAndSetup $swAddr2 $ces2ManagementIp $ces2MngIfIp $ces2PrivateSlot $ces2PrivateIp $ces1PrivateSlot $ces2PublicIp $ces2PublicSlot $ces2_ldap_file
    AddBoGroup $boGroup $swAddr2

    EnaIpsecEncrType $swAddr2 "all"
    EnaIpsecIkeEncrType $swAddr2 "all"

    EnaBoGrpEncrType $swAddr2 $boGroup "3des-md5"
} else {
    logCliFile "\n\n------------- CES $swAddr1 connect ---------------\n"
    Connect $cesAdminName $cesAdminPass $swAddr1
    SetCliLevel "CONFIG" $swAddr1
    logCliFile "\n\n------------- CES $swAddr2 connect ---------------\n"
    Connect $cesAdminName $cesAdminPass $swAddr2
    SetCliLevel "CONFIG" $swAddr2
}

  #// GET some info about CESs software version
  set DUT_SwVer [GetSwitchSWVerNum_exp $swAddr2]

  variable testedBuild $DUT_SwVer
  variable ces2_currentSwVer $testedBuild
  variable calvinBuild "none"
  set rdf_calvinBuild [getProperty $dut1 calvin-build]

  foreach version [GetSoftwareVersion $swAddr2] {
     if {$rdf_calvinBuild == $version} {
        set calvinBuild $version
        break
     }
  }

  #// variables used for tests with certificates
  variable certInstalled 0

  variable ces1ServCert [GetServerCertificate $swAddr1]
  variable ces2ServCert [GetServerCertificate $swAddr2]
  variable ces1CaCert [GetCACertificate $swAddr1]
  variable ces2CaCert [GetCACertificate $swAddr2]

  if {$ces1ServCert !=  "" && $ces2ServCert != "" && $ces1CaCert != "" && $ces1CaCert != "" && \
          $ces1CaCert == $ces2CaCert } {
     set certInstalled 1
  }

  return
}


proc CesConnectAndSetup {swAddr ManagementIp mngIfIp mngSlot prIfIp prIfSlot pbIfIp pbIfSlot ldap_file {reset no}} {

  variable cesAdminName
  variable cesAdminPass
  variable arLicense
  variable private_key_pass

  logCliFile "\n\n------------- CES $swAddr connect ---------------\n"
  Connect $cesAdminName $cesAdminPass $swAddr

  logFile "CES $swAddr: restart to default!"
  if {$reset=="yes"} {
     ResetSwitchFact $swAddr $cesAdminName $cesAdminPass
  } else {
     RestoreBasicCfg $swAddr "NONE.NON" $ldap_file $cesAdminName $cesAdminPass
  }

  SetPrivateKeyPass $swAddr $private_key_pass
  ArLicenseInstall $arLicense $swAddr

  #//Configure Private IPs - management IP and interface IP
  logFile "CES $swAddr - private interface setup"

  SetMngIpAddr $swAddr $ManagementIp
  SetIfIpAddr "fast" $mngSlot $mngIfIp "255.255.255.0" $swAddr

  SetIfIpAddr "fastEthernet" $pbIfSlot $pbIfIp "255.255.255.0" $swAddr
  ########
  # Uncoment the lines below if you are using another card instead of management card as private interface
  ########
  ############
  #       #//configure private IPs - static IP address
  #       logFile "CES $swAddr - public interfaces setup"
  #       SetIfIpAddr "fastEthernet" $prIfSlot $prIfIp "255.255.255.0" $swAddr

  #       #// set first interface to private
  #       logFile "CES $swAddr - set first interface to private"
  #       EnterConfigIfLevel "fastEthernet" $prIfSlot $swAddr
  #       Exec "no public" "CONFIGIF" $swAddr
  ###########

  #//configure filter "permit all" for all interfaces and enable "contivity interface filter" in CES
  logFile "CES $swAddr - sets filter \"permit all\" for all fastEthernet interfaces"
  SetInterfaceFilter "fastEthernet" $prIfSlot "\"permit all\"" $swAddr
  SetInterfaceFilter "fastEthernet" $pbIfSlot "\"permit all\"" $swAddr
  EnaContivityIfFilters $swAddr

  logFile "CES $swAddr - restart"
  RestartSwitch $swAddr

 ### Replace this by python API ###  logFile "CES $swAddr - sets parameters: proxy-arp, system forwarding and maximim path"
  #// sets CES parameters need for OSPF test
  SetCliLevel "CONFIG" $swAddr

  #// disable all proxy arp
  SetGlobalSysFwdArp "no_enable" "no_enable" "no_enable" $swAddr
  #// Ensure that Rip is not available on management interface
  DelRipNetwork $mngIfIp  255.255.255.0 $swAddr

}


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

#init_vars
setup_ace 1
return "PASS"
