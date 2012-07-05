
   proc T-024 {} {

      set error_code "FAIL"
      set testName "T-024"

      testStartLog $testName

      set purpose {Verify you can create a Static Peer to Peer PPTP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-40 encryption with no compression/stateless mode compression and permit all filter}
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

      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static PPTP BOT / rc4-40 encryption / no compression"
      ConfigPPTPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "p2p $ces1PublicIp $ces2PublicIp" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "pptp" "rc4_40"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "pptp" "disable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "pptp" "disable"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static PPTP BOT / rc4-40 encryption / no compression"
      ConfigPPTPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "p2p $ces2PublicIp $ces1PublicIp" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "pptp" "rc4_40"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "pptp" "disable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "pptp" "disable"

      if {[VerifyBoConnection "PPTP"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete PPTP BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete PPTP BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2

      testEndLog $testName $error_code
      return $error_code
   }
   T-024
