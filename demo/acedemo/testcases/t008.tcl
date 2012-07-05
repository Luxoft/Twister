
   proc T-008 {} {

      set error_code "FAIL"
      set testName "t008.tcl"

      testStartLog $testName

      set purpose {Verify you can create a Static Peer to Peer IPSec Branch Office tunnel with Hex Pre-shared key and permit all filter}
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
      variable hexPass


      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static IPSEC BOT "
      ConfigIpSecBO $swAddr1 "tunnel_test_1" $boGroup "hex $hexPass" "p2p $ces1PublicIp $ces2PublicIp" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static IPSEC BOT"
      ConfigIpSecBO $swAddr2 "tunnel_test_2" $boGroup "hex $hexPass" "p2p $ces2PublicIp $ces1PublicIp" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      if {[VerifyBoConnection "IPSEC"] == "SUCCESS"} {
         set error_code "FAIL"
      }

      logFile "CES: $swAddr1 - delete IPSEC BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete IPSEC BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2

      testEndLog $testName $error_code
      return $error_code
   }

 T-008
