 proc T-029 {} {

      set error_code "FAIL"
      set testName "T-029"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/ Peer Authentication that includes MS-CHAPV2 and none encryption, Enabled compression, compression stateless mode enabled, default L2TP concentrator with permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicIp

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2

      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      logFile "CES: $swAddr1 - add dynamic rip L2TP BOT / no encryption / with compression"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 l2tpPass" "p2p $ces1PublicIp $ces2PublicIp" "rip"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "none"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "enable"

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip L2TP BOT / no encryption / with compression"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 l2tpPass" "p2p $ces2PublicIp $ces1PublicIp" "rip"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "none"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "enable"

      if {[VerifyBoConnection "L2TP"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete L2TP BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp  255.255.255.0 $swAddr1
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete L2TP BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp  255.255.255.0 $swAddr2
      DisableRip $swAddr2

      testEndLog $testName $error_code
      return $error_code
   }
T-029
