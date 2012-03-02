
  proc T-001 {} {

      set error_code "FAIL"
      set testName "t001.tcl"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic Peer to Peer IPSec Branch Office tunnel over Ethernet with Text Pre-shared key and permit all filter}
      set description {}
      testPurposeLog $purpose $description


      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicIp

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2
      variable textPass

      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      logFile "CES: $swAddr1 - add dynamic rip IPSEC BOT"
      ConfigIpSecBO $swAddr1 $boName_ces1 $boGroup "text $textPass" "p2p $ces1PublicIp $ces2PublicIp" "rip"

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip IPSEC BOT"
      ConfigIpSecBO $swAddr2 $boName_ces2 $boGroup "text $textPass" "p2p $ces2PublicIp $ces1PublicIp" "rip"

      if {[VerifyBoConnection "IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete IPSEC BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete IPSEC BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      DisableRip $swAddr2

      testEndLog $testName $error_code
      return $error_code
   }

T-001
