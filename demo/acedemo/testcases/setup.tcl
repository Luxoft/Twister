
lappend auto_path $env(ACE_PATH)

package require Acelib
package require Expect


proc setup_ace {resetdefault} {
  #// Assign variables
  global DUT_SwVer
  global logDir

  #//start CLI LOG file
  ### Replace this by python API ### variable cliFileId [StartCLILog "CLI.log" $logDir]

  variable suiteName "BO"
  ### Replace this by python API ### suiteStartLog $suiteName

  #//interfaces IDs

  #//get from canvas the IP or IP:Port for management links
  set ces1_ip [getProperty DUT1 TerminalServerIp]
  set ces1_port [getProperty DUT1 TerminalServerPort]
  variable swAddr1 "$ces1_ip:$ces1_port"
  set ces2_ip [getProperty DUT2 TerminalServerIp]
  set ces2_port [getProperty DUT2 TerminalServerPort]
  variable swAddr2 "$ces2_ip:$ces2_port"
  puts $swAddr1
  puts $swAddr2

  variable ces1ManagementIp [getProperty DUT1 dut1-mng-ip]
  variable ces1MngIfIp [getProperty DUT1 dut1-mng-private-ip]
  variable ces1PrivateSlot [getProperty DUT1 private-if]
  variable ces1PublicIp [getProperty DUT1 dut1-public-eth-ip]
  variable ces1PublicSlot [getProperty DUT1 public-eth-if]

  #// variable ces1NatIp is used for Nat control tunnel test in Ces1 (T-106)
  variable ces1NatIp 1.1.1.1
  variable ces1_ldap_file [getProperty DUT1 dut1-ldap-file]

  ########
  # Uncomment the line below if you are using another card instead of management card as private interface
  ########
  #variable ces1PrivateIp [Global:getlist dut1-private-ip]
  ########
  # Comment the line below if you are using another card instead of management card as private interface
  ########
  variable ces1PrivateIp $ces1MngIfIp

  variable ces2ManagementIp [getProperty DUT2 dut2-mng-ip]
  variable ces2MngIfIp [getProperty DUT2 dut2-mng-private-ip]
  variable ces2PrivateSlot [getProperty DUT2 private-if]
  variable ces2PublicIp [getProperty DUT2 dut2-public-eth-ip]
  variable ces2PublicSlot [getProperty DUT2 public-eth-if]
  variable ces2_ldap_file [getProperty DUT2 dut2-ldap-file]
  ########
  # Uncomment the line below if you are using another card instead of management card as private interface
  ########
  #variable ces2PrivateIp [Global:getlist dut2-private-ip]
  ########
  # Comment the line below if you are using another card instead of management card as private interface
  ########
  variable ces2PrivateIp $ces2MngIfIp

  #//SW passwd and name
  variable cesAdminName [getProperty DUT1 cesAdminName]
  variable cesAdminPass [getProperty DUT1 cesAdminPass]

  variable arLicense "AR-7570301-DCCC029153-BF"

  variable boGroup "/Base/BOTest"
  variable boName_ces1 "tunnel_test_1"
  variable boName_ces2 "tunnel_test_2"
  variable textPass "abcdefgh"
  variable hexPass "ffaaff"
  variable initiator_uid "init_test"

  variable private_key_pass [getProperty DUT1 private-key-pass]

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
  set rdf_calvinBuild [getProperty DUT1 calvin-build]

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

setup_ace 0
testEndLog "setup.tcl" "PASS"
