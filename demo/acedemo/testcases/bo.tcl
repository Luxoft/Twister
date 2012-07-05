# -*- tcl -*-

#################
# Test: BO
# Author: Gheorghe Pitulan
#
# Tests Description:
#     This testing will test the functionality of setting up an IPSec, PPTP, and L2TP Tunnel
#     using either Pre-Shared Text Key or a Pre-Shared HEX key over Ethernet.
#
#
# REQUIREMENTS: HARDWARE & SOFTWARE
#
#       - Terminal server (1 device) - for connecting to switches
#
#       - Contivity switches (2 devices)
#           - CES1 - with 3 ethernet cards (Management + Private + Public)
#           - CES2 - with 3 ethernet cards (Management + Private + Public)
#
#       - Linux PC
#           -  ace PC - to run ace - with one network interface to connecting to terminal server
#
#  NOTE:
#   1. Because the certificates is losed in case of reset to default you must make an
#      manual restart to begining of the test
#      MUST have only one certificate installed
#
#   2. Be sure that CESs current software is the software that it must be tested;
#      also CES1 must have on hard disk the Calvin software indicated in rdf file
#
#
######################################################################
# MAIN: BO           "BO test suite Regression"
# TEST: T-001 "Verify you can create a Dynamic Peer to Peer IPSec Branch Office tunnel over Ethernet with Text Pre-shared key and permit all filter"
# TEST: T-002 "Verify you can create a Dynamic Peer to Peer IPSec Branch Office tunnel over Ethernet with Hex Pre-shared key and permit all filter"
# TEST: T-003 "Verify you can create a Dynamic Peer to Peer IPSec Branch Office tunnel with Cerificates (Entrust, Verisign, and Microsoft CA) and permit all filter"
# TEST: T-007 "Verify you can create a static Peer to Peer IPSec Branch Office tunnel with Text Pre-shared key and permit all filter"
# TEST: T-008 "Verify you can create a Static Peer to Peer IPSec Branch Office tunnel with Hex Pre-shared key and permit all filter"
# TEST: T-009 "Verify you can create a Static Peer to Peer IPSec Branch Office tunnel over Ethernet with Cerificates (Entrust, Verisign, and Microsoft CA) and permit all filter"
# TEST: T-012 "Verify you can create a Dynamic Peer to Peer PPTP Branch Office tunnel over Ethernet with Local/ Peer Authentication that includes MS-CHAPV2 and none encryption, enable compression, with permit all filter"
# TEST: T-013 "Verify you can create a Dynamic Peer to Peer PPTP Branch Office tunnel over Ethernet with Local/ Peer Authentication that includes MS-CHAPV2 and RC4-40 encryption, enable compression, with permit all filter"
# TEST: T-014 "Verify you can create a Dynamic Peer to Peer PPTP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-40 encryption with no compression/stateless mode compression and permit all filter"
# TEST: T-015 "Verify you can create a Dynamic Peer to Peer PPTP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-128 encryption with compression/stateless mode compression and permit all filter"
# TEST: T-016 "Verify you can create a Dynamic Peer to Peer PPTP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-128 encryption with no compression/stateless compression and permit all filter"
# TEST: T-023 "Verify you can create a Static Peer to Peer PPTP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and none encryption with no compression/stateless mode compression and permit all filter"
# TEST: T-024 "Verify you can create a Static Peer to Peer PPTP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-40 encryption with no compression/stateless mode compression and permit all filter"
# TEST: T-025 "Verify you can create a Static Peer to Peer PPTP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-128 encryption with no compression/stateless"
# TEST: T-029 "Verify you can create a Dynamic Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/ Peer Authentication that includes MS-CHAPV2 and none encryption, Enabled compression, compression stateless mode enabled, default L2TP concentrator with permit all filter"
# TEST: T-030 "Verify you can create a Dynamic Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/ Peer Authentication that includes MS-CHAPV2 and none encryption, Enabled compression, compression stateless mode disabled, default L2TP concentrator with permit all filter"
# TEST: T-031 "Verify you can create a Dynamic Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-40 encryption with Enabled compression and stateless mode compression enabled and permit all filter"
# TEST: T-032 "Verify you can create a Dynamic Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-128 encryption with Enabled compression and stateless mode compression enabled and permit all filter"
# TEST: T-033 "Verify you can create a Dynamic Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-40 encryption with Enabled compression and stateless mode compression disabled and permit all filter"
# TEST: T-034 "Verify you can create a Dynamic Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-128 encryption with Enabled compression and stateless mode compression disabled and permit all filter"
# TEST: T-035 "Verify you can create a Dynamic Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and? RC4-40 encryption with compression set to Disabled, set IPSec Encryption Not Required, with permit all filter "
# TEST: T-036 "Verify you can create a Dynamic Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and no L2TP encryption with compression set to Disabled, set IPSec Encryption Triple DES pre-shared text key, with permit all filter"
# TEST: T-037 "Verify you can create a Dynamic Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and no L2TP encryption with compression set to Disabled, set IPSec Encryption Triple DES pre-shared HEX key, with permit all filter"
# TEST: T-038 "Verify you can create a Dynamic Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and no L2TP encryption with compression set to Disabled, set IPSec Encryption Triple DES Certificates (Entrust, Verisign, and Microsoft CA), with permit all filter"
# TEST: T-039 "Verify you can create a Dynamic Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and no L2TP encryption with compression set to Disabled, set IPSec Encryption 56 bit DES Pre-shared text key, with permit all filter"
# TEST: T-040 "Verify you can create a Dynamic Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and no L2TP encryption with compression set to Disabled, set IPSec Encryption 56 bit DES Pre-shared HEX key, with permit all filter"
# TEST: T-041 "Verify you can create a Dynamic Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and no L2TP encryption with compression set to Disabled, set IPSec Encryption 56 bit DES Certificates (Entrust, Verisign, and Microsoft CA), with permit all filter"
# TEST: T-044 "Verify you can create a Static Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/ Peer Authentication that includes MS-CHAPV2 and none encryption, Enabled compression, compression stateless mode enabled, default L2TP concentrator with permit all filter"
# TEST: T-045 "Verify you can create a Static Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/ Peer Authentication that includes MS-CHAPV2 and none encryption, Enabled compression, compression stateless mode disabled, default L2TP concentrator with permit all filter"
# TEST: T-046 "Verify you can create a Static Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-40 encryption with Enabled compression and stateless mode compression enabled and permit all filter"
# TEST: T-047 "Verify you can create a Static Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-128 encryption with Enabled compression and stateless mode compression enabled and permit all filter"
# TEST: T-048 "Verify you can create a Static Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-40 encryption with Enabled compression and stateless mode compression disabled and permit all filter"
# TEST: T-049 "Verify you can create a Static Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-128 encryption with Enabled compression and stateless mode compression disabled and permit all filter"
# TEST: T-050 "Verify you can create a Static Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-40 encryption with compression set to Disabled, set IPSec Encryption Not Required, with permit all filter"
# TEST: T-051 "Verify you can create a Static Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and no L2TP encryption with compression set to Disabled, set IPSec Encryption Triple DES pre-shared text key, with permit all filter"
# TEST: T-052 "Verify you can create a Static Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and no L2TP encryption with compression set to Disabled, set IPSec Encryption Triple DES pre-shared HEX key, with permit all filter"
# TEST: T-053 "Verify you can create a Static Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and no L2TP encryption with compression set to Disabled, set IPSec Encryption Triple DES Certificates (Entrust, Verisign, and Microsoft CA), with permit all filter"
# TEST: T-054 "Verify you can create a Static Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and no L2TP encryption with compression set to Disabled, set IPSec Encryption 56 bit DES Pre-shared text key, with permit all filter"
# TEST: T-055 "Verify you can create a Static Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and no L2TP encryption with compression set to Disabled, set IPSec Encryption 56 bit DES Pre-shared HEX key, with permit all filter"
# TEST: T-056 "Verify you can create a Static Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and no L2TP encryption with compression set to Disabled, set IPSec Encryption 56 bit DES Certificates (Entrust, Verisign, and Microsoft CA), with permit all filter"
# TEST: T-060 "Verify you can create a Dynamic ABOT IPSec Branch Office tunnel over Ethernet with Text Pre-shared key and permit all filter"
# TEST: T-061 "Verify you can create a Dynamic ABOT IPSec Branch Office tunnel over Ethernet with Hex Pre-shared key and permit all filter"
# TEST: T-062 "Verify you can create a Dynamic ABOT IPSec Branch Office over Ethernet with Cerificates (Entrust, Verisign, and Microsoft CA) and permit all filter"
# TEST: T-065 "Verify you can create a Static ABOT IPSec Branch Office tunnel over Ethernet with Text Pre-shared key and permit all filter"
# TEST: T-066 "Verify you can create a Static ABOT IPSec Branch Office tunnel over Ethernet with Hex Pre-shared key and permit all filter"
# TEST: T-067 "Verify you can create a Static ABOT IPSec Branch Office over Ethernet with Cerificates (Entrust, Verisign, and Microsoft CA) and permit all filter"
# TEST: T-068 "Verify you can create a Dynamic ABOT PPTP Branch Office tunnel over Ethernet with Local/ Peer Authentication that includes MS-CHAPV2 and none encryption, enable compression, with permit all filter"
# TEST: T-069 "Verify you can create a Dynamic ABOT PPTP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and none encryption with no compression/stateless mode compression and permit all filter"
# TEST: T-070 "Verify you can create a Dynamic ABOT PPTP Branch Office tunnel over Ethernet with Local/ Peer Authentication that includes MS-CHAPV2 and RC4-40 encryption, enable compression, with permit all filter"
# TEST: T-071 "Verify you can create a Dynamic ABOT PPTP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-40 encryption with no compression/stateless mode compression and permit all filter"
# TEST: T-072 "Verify you can create a Dynamic ABOT PPTP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-128 encryption with compression/stateless mode compression and permit all filter"
# TEST: T-073 "Verify you can create a Dynamic ABOT PPTP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-128 encryption with no compression/stateless compression and permit all filter"
# TEST: T-076 "Verify you can create a Static ABOT PPTP Branch Office tunnel over Ethernet with Local/ Peer Authentication that includes MS-CHAPV2 and none encryption, enable compression, with permit all filter"
# TEST: T-077 "Verify you can create a Static ABOT PPTP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and none encryption with no compression/stateless mode compression and permit all filter"
# TEST: T-078 "Verify you can create a Static ABOT PPTP Branch Office tunnel over Ethernet with Local/ Peer Authentication that includes MS-CHAPV2 and RC4-40 encryption, enable compression, with permit all filter"
# TEST: T-079 "Verify you can create a Static ABOT PPTP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-40 encryption with no compression/stateless mode compression and permit all filter"
# TEST: T-080 "Verify you can create a Static ABOT PPTP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-128 encryption with compression/stateless mode compression and permit all filter"
# TEST: T-081 "Verify you can create a Static ABOT PPTP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-128 encryption with no compression/stateless compression and permit all filter"
# TEST: T-084 "Verify you can create a Dynamic ABOT L2TP Branch Office tunnel over Ethernet with Local/ Peer Authentication that includes MS-CHAPV2 and none encryption, Enabled compression, compression stateless mode enabled, default L2TP concentrator with permit all filter"
# TEST: T-085 "Verify you can create a Dynamic ABOT L2TP Branch Office tunnel over Ethernet with Local/ Peer Authentication that includes MS-CHAPV2 and none encryption, Enabled compression, compression stateless mode disabled, default L2TP concentrator with permit all filter"
# TEST: T-086 "Verify you can create a Dynamic ABOT L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-40 encryption with Enabled compression and stateless mode compression enabled and permit all filter"
# TEST: T-087 "Verify you can create a Dynamic ABOT L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-128 encryption with Enabled compression and stateless mode compression enabled and permit all filter"
# TEST: T-088 "Verify you can create a Dynamic ABOT L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-40 encryption with Enabled compression and stateless mode compression disabled and permit all filter"
# TEST: T-089 "Verify you can create a Dynamic ABOT L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-128 encryption with Enabled compression and stateless mode compression disabled and permit all filter"
# TEST: T-090 "Verify you can create a Dynamic ABOT L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-40 encryption with compression set to Disabled, set IPSec Encryption Not Required, with permit all filter"
# TEST: T-091 "Verify you can create a Dynamic ABOT L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and no L2TP encryption with compression set to Disabled, set IPSec Encryption Triple DES pre-shared text key, with permit all filter"
# TEST: T-092 "Verify you can create a Dynamic ABOT L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and no L2TP encryption with compression set to Disabled, set IPSec Encryption Triple DES pre-shared HEX key, with permit all filter"
# TEST: T-093 "Verify you can create a Dynamic ABOT L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and no L2TP encryption with compression set to Disabled, set IPSec Encryption Triple DES Certificates (Microsoft CA), with permit all filter"
# TEST: T-094 "Verify you can create a Dynamic ABOT L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and no L2TP encryption with compression set to Disabled, set IPSec Encryption 56 bit DES Pre-shared text key, with permit all filter"
# TEST: T-095 "Verify you can create a Dynamic ABOT L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and no L2TP encryption with compression set to Disabled, set IPSec Encryption 56 bit DES Pre-shared HEX key, with permit all filter"
# TEST: T-096 "Verify you can create a Dynamic ABOT L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and no L2TP encryption with compression set to Disabled, set IPSec Encryption 56 bit DES Certificates (Microsoft CA), with permit all filter"
# TEST: T-099 "Verify you can create a Static ABOT L2TP Branch Office tunnel over Ethernet with Local/ Peer Authentication that includes MS-CHAPV2 and none encryption, Enabled compression, compression stateless mode enabled, default L2TP concentrator with permit all filter"
# TEST: T-100 "Verify you can create a Static ABOT L2TP Branch Office tunnel over Ethernet with Local/ Peer Authentication that includes MS-CHAPV2 and none encryption, Enabled compression, compression stateless mode disabled, default L2TP concentrator with permit all filter"
# TEST: T-101 "Verify you can create a Static ABOT L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-128 encryption with Enabled compression and stateless mode compression disabled and permit all filter"
# TEST: T-102 "Verify you can create a Static ABOT L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and no L2TP encryption with compression set to Disabled, set IPSec Encryption Triple DES Certificates (Microsoft CA), with permit all filter"
# TEST: T-103 "Verify you can create a static Peer to Peer IPSec Branch Office Control Tunnel with Text Pre-shared key and permit all filter"
# TEST: T-104 "Verify you can create a Static Peer to Peer IPSec Branch Office Control Tunnel with Hex Pre-shared key and permit all filter"
# TEST: T-105 "Verify you can create a Static Peer to Peer IPSec Branch Office Control Tunnel with Cerificates (  Microsoft CA) and permit all filter"
# TEST: T-106 "Verify you can create a static Peer to Peer IPSec Branch Office NAT Control Tunnel with Text Pre-shared key and permit all filter"
# TEST: T-109 "Verify that creating Dynamic IPSec Peer to Peer Branch Office Tunnel with a mis-matched pre-shared key to see if the tunnel comes up"
# #TEST: - T-110 "Bouncing Tunnels IPSEC"
# #TEST: - T-111 "Bouncing Tunnels L2TP"
# #TEST: - T-112 "Bouncing Tunnels PPTP"
# TEST: T-114 "End/Close all sessions, including ping, to the remote network & remote CES"
# TEST: T-115 "Verify you can enter multiple characters within the Connection configuration fields and get the correct error if mis-configured tunnel"
# TEST: T-116 "Verify if you enter reserved IPs, 255.0.0.0, 127.0.0.1, and anything higher then 240.0.0.0, that you will get a correct error message"
# OBSOLETE_TEST: T-121 "Verify configuring a Dynamic Peer to Peer IPSec Branch Office Tunnel with OSPF enabled and RIP enabled"
# NEED_MOD_TEST: T-129 "Verify you can create a Dynamic, Peer to Peer IPSec Branch Office tunnel with Text Preshared key and permit all filter, between Calvin and Coolidge builds (V04_70.xxx and the latest software) Enable IKE Encryption and Diffie-Hellman Group 5 AES encryption with encryption ESP128SHA1 enabled"
# NEED_MOD_TEST: T-130 "Verify you can create a Static Peer to Peer IPSec Branch Office tunnel with Text Preshared key and permit all filter, between Calvin(V04_70.xxx) and the latest build.Enable IKE Encryption and Diffie Hellman Group 5 AES, and ESP Triple DES with MD5 integrity. Agressive mode enabled"
# NEED_MOD_TEST: T-131 "Verify you can create a Dynamic, ABOT IPSec Branch Office tunnel with Text Preshared key and permit all filter, between Calvin and Coolidge builds (V04_70.xxx and the latest build). Enable IKE encryption and Diffie-Hellman Group 5 AES encryption, with encryption ESP 128SHA1integrity. Agressive mode disabled."
# NEED_MOD_TEST: T-132 "Verify you can create a Dynamic, ABOT IPSec Branch Office tunnel with Text Preshared key and permit all filter, between Calvin and Coolidge builds (V04_70.xxx and the latest build) Enable IKE Encryption and Diffie-Hellman Group 5 AES encryption with encryption ESP128SHA1 enabled. Aggressive mode enabled."
# NEED_MOD_TEST: T-133 "Verify you can create a Static  ABOT IPSec Branch Office tunnel with Text Preshared key and permit all filter, between Calvin (V04_70.xxx) and the latest build. IKE encryption and Diffie-Hellman Group 5 AES with encryption ESP AES- 128SHA1 integrity enabled. Agressive mode disabled."
# NEED_MOD_TEST: T-134 "Verify you can create a Static  ABOT IPSec Branch Office tunnel with Text Preshared key and permit all filter, between Calvin and the latest build. Enable IKE encryption and Diffie-Hellman Group 5 AES with ESP AES 128 with SHA1 integrity. Aggressive mode enabled."
# NEED_MOD_TEST: T-136 "Verify you can create a Static ABOT IPSec Branch Office tunnel with Text Preshared key and permit all filter, between Calvin(V04_70.xxx) and the latest build. Enable IKE Encryption and Diffie Hellman Group 5 AES, and ESP Triple DES with MD5 integrity. Agressive mode enabled."
# NEED_MOD_TEST: T-137 "Verify you can create a Static ABOT IPSec Branch Office tunnel with Text Preshared key and permit all filter, between Calvin (V04_70.xxx) and the latest build. Enable IKE Encryption and Diffie Hellman Group 5 AES, and ESP- 56bit DES with SHA1 integrity. Aggressive mode enabled."
# NEED_MOD_TEST: T-138 "Verify you can create a Static ABOT IPSec Branch Office tunnel with Text Preshared key and permit all filter, between Calvin and Coolidge builds (V04_70.119 and the latest build). Enable IKE Encryption and Diffie Hellman Group 5 AES, and ESP- 56 bit DES with MD5 integrity. Agressive mode enabled."
# NEED_MOD_TEST: T-139 "Verify you can create a Static ABOT IPSec Branch Office tunnel with Text Preshared key and permit all filter, between Calvin and Coolidge builds (V04_70.119 and the latest build). Enable IKE Encryption and Diffie Hellman Group 5 AES, and ESP 40 bit DES with SHA1 integrity. Agressive mode enabled."
# NEED_MOD_TEST: T-140 "Verify you can create a Static ABOT IPSec Branch Office tunnel with Text Preshared key and permit all filter, between Calvin (V04_70.xxx) and the latest build. Enable IKE Encryption and Diffie Hellman Group 5 AES, and ESP 40 bit DES with MD5 integrity. Aggressive mode enabled."
# NEED_MOD_TEST: T-141 "Verify you can create a Static ABOT IPSec Branch Office tunnel with Text Preshared key and permit all filter, between Calvin (V04_70.xxx) and the latest build. Enable IKE Encryption and Diffie Hellman Group 5 AES, and ESP NULL (Authentication only) with SHA1 integrity. Agressive mode enabled."
# NEED_MOD_TEST: T-142 "Verify you can create a Static ABOT IPSec Branch Office tunnel with Text Preshared key and permit all filter, between Calvin(V04_70.xxx) and the latest build. Enable IKE Encryption and Diffie Hellman Group 5 AES, and ESP NULL (Authentication only) with MD5 integrity. Aggressive mode enabled."
# NEED_MOD_TEST: T-143 "Verify you can create a Static ABOT IPSec Branch Office tunnel with Text Preshared key and permit all filter, between Calvin and the latest build. Enable IKE Encryption and Diffie Hellman Group 5 AES, and AH Authentication only (HMAC-SHA1) Agressive mode enabled."
# NEED_MOD_TEST: T-144 "Verify you can create a Static ABOT IPSec Branch Office tunnel with Text Preshared key and permit all filter, between Calvin and the latest build. Enable IKE Encryption and Diffie Hellman Group 5 AES, and AH Authentication only (HMAC-MD5) Agressive mode enabled."
# NEED_MOD_TEST: T-145 "Verify a Static Peer to Peer IPSec Branch Office tunnel with Text Preshared key and permit all filter, between Calvin (V04_70.xxx) and the latest build can not be brought up when : Enable IKE encryption and Diffie Hellman Group 5 AES and encryption is ESP  AES 128 with SHA1 integrity. Vendor ID is disabled and aggressive mode is disabled."
# NEED_MOD_TEST: T-146 "Verify a branch office tunnel can not  be brought up when the branch office tunnel is configured as : Dynamic Peer to Peer, with IPSec and a Text Preshared key using a permit all filter. IKE Encryption and Diffie-Hellman Group 5 AES and ESP- AES 128SHA1 integrity. Between Calvin (V04_70.xxx) and the latest build. Vendor ID is disabled and aggressive mode is disabled."
# NEED_MOD_TEST: T-147 "Verify a branch office tunnel can not  be brought up when the branch office tunnel is configured as : Dynamic  Peer to Peer with IPSec and a Text Preshared key using a permit all filter. IKE Encryption and Diffie-Hellman Group 5 AES and ESP128 SHA1 encryption. Between Calvin (V04_70.xxx) and the latest build. Vendor ID is disabled and aggressive mode is enabled"
# NEED_MOD_TEST: T-148 "Verify an IPsec branch office tunnel fails when configured with mismatched Diffie-Hellman Encryptions. Configure a Static Peer to Peer with a Text Preshared key and permit all filter, between Calvin (V04_70.xxx) and the latest build. Enable IKE Encryption and Diffie Hellman Group 5 AES, and AH Authentication only (HMAC-SHA1) Enable other of tunnel with CES with IKE Encryption and Diffie-Hellman Group 8 AES-128 (ECC283-=bit field) Vendor ID enabled and aggressive mode enabled."
# TEST: T-158 "Verify CLI commands for an ABOT IPSec Tunnel using AES Group 8 and 5"
#######################################################################################


namespace eval BO {
   #// Set variables here and initialize them.

   ####################################################################################
   #  Proc SETUP, First procedure to be called by the program before any other
   #
   proc setup_ace {} {

      #// Assign variables..
      global DUT_SwVer
      global logDir

      #//start CLI LOG file
      variable cliFileId [StartCLILog "CLI.log" $logDir]

      variable suiteName "BO"
      suiteStartLog $suiteName

      #//interfaces IDs

      #//get from canvas the IP or IP:Port for management links
      variable swAddr1 [Global:getlist ces1]
      variable swAddr2 [Global:getlist ces2]

      variable ces1ManagementIp [Global:getlist dut1-mng-ip]
      variable ces1MngIfIp [Global:getlist dut1-mng-private-ip]
      variable ces1PrivateSlot [Global:getlist private-if]
      variable ces1PublicIp [Global:getlist dut1-public-eth-ip]
      variable ces1PublicSlot [Global:getlist public-eth-if]
      #// variable ces1NatIp is used for Nat control tunnel test in Ces1 (T-106)
      variable ces1NatIp 1.1.1.1
      variable ces1_ldap_file [Global:getlist dut1-ldap-file]
      ########
      # Uncomment the line below if you are using another card instead of management card as private interface
      ########
      #variable ces1PrivateIp [Global:getlist dut1-private-ip]
      ########
      # Comment the line below if you are using another card instead of management card as private interface
      ########
      variable ces1PrivateIp $ces1MngIfIp

      variable ces2ManagementIp [Global:getlist dut2-mng-ip]
      variable ces2MngIfIp [Global:getlist dut2-mng-private-ip]
      variable ces2PrivateSlot [Global:getlist private-if]
      variable ces2PublicIp [Global:getlist dut2-public-eth-ip]
      variable ces2PublicSlot [Global:getlist public-eth-if]
      variable ces2_ldap_file [Global:getlist dut2-ldap-file]
      ########
      # Uncomment the line below if you are using another card instead of management card as private interface
      ########
      #variable ces2PrivateIp [Global:getlist dut2-private-ip]
      ########
      # Comment the line below if you are using another card instead of management card as private interface
      ########
      variable ces2PrivateIp $ces2MngIfIp

      #//SW passwd and name
      variable cesAdminName [Global:getlist cesAdminName]
      variable cesAdminPass [Global:getlist cesAdminPass]

      variable arLicense "AR-7570301-DCCC029153-BF"

      variable boGroup "/Base/BOTest"
      variable boName_ces1 "tunnel_test_1"
      variable boName_ces2 "tunnel_test_2"
      variable textPass "abcdefgh"
      variable hexPass "ffaaff"
      variable initiator_uid "init_test"

      variable private_key_pass [Global:getlist private-key-pass]

      CesConnectAndSetup $swAddr1 $ces1ManagementIp $ces1MngIfIp $ces1PrivateSlot $ces1PrivateIp $ces1PrivateSlot $ces1PublicIp $ces1PublicSlot $ces1_ldap_file
      AddBoGroup $boGroup $swAddr1

      EnaIpsecEncrType $swAddr1 "all"
      EnaIpsecIkeEncrType $swAddr1 "all"

      EnaBoGrpEncrType $swAddr1 $boGroup "3des-md5"

      CesConnectAndSetup $swAddr2 $ces2ManagementIp $ces2MngIfIp $ces2PrivateSlot $ces2PrivateIp $ces1PrivateSlot $ces2PublicIp $ces2PublicSlot $ces2_ldap_file
      AddBoGroup $boGroup $swAddr2

      EnaIpsecEncrType $swAddr2 "all"
      EnaIpsecIkeEncrType $swAddr2 "all"

      EnaBoGrpEncrType $swAddr2 $boGroup "3des-md5"

      #// GET some info about CESs software version
      set DUT_SwVer [GetSwitchSWVerNum_exp $swAddr2]

      variable testedBuild $DUT_SwVer
      variable ces2_currentSwVer $testedBuild
      variable calvinBuild "none"
      set rdf_calvinBuild [Global:getlist calvin-build]

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


   proc T-001 {} {

      set error_code "FAIL"
      set testName "T-001"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic Peer to Peer IPSec Branch Office tunnel over Ethernet with Text Pre-shared key and permit all filter}
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
   }


   proc T-002 {} {

      set error_code "FAIL"
      set testName "T-002"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic Peer to Peer IPSec Branch Office tunnel over Ethernet with Hex Pre-shared key and permit all filter}
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

      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      logFile "CES: $swAddr1 - add dynamic rip IPSEC BOT"
      ConfigIpSecBO $swAddr1 $boName_ces1 $boGroup "hex $hexPass" "p2p $ces1PublicIp $ces2PublicIp" "rip"

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip IPSEC BOT"
      ConfigIpSecBO $swAddr2 $boName_ces2 $boGroup "hex $hexPass" "p2p $ces2PublicIp $ces1PublicIp" "rip"

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
   }


   proc T-003 {} {

      set testName "T-003"
      set error_code "FAIL"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic Peer to Peer IPSec Branch Office tunnel with Cerificates (Entrust, Verisign, and Microsoft CA) and permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable certInstalled
      if { $certInstalled != 1 } {
         logFile "The certificates are wrong or they are not installed"
         testEndLog $testName "ABORT"
         return
      }

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicIp

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2

      variable ces1ServCert
      variable ces2ServCert
      variable ces1CaCert
      variable ces2CaCert

      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      logFile "CES: $swAddr1 - add dynamic rip IPSEC BOT with Certificates"
      ConfigIpSecBO $swAddr1 $boName_ces1 $boGroup "certificate \"$ces1CaCert\" \"$ces1ServCert\" \"$ces2ServCert\"" "p2p $ces1PublicIp $ces2PublicIp" "rip"

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip IPSEC BOT with Certificates"
      ConfigIpSecBO $swAddr2 $boName_ces2 $boGroup "certificate \"$ces1CaCert\" \"$ces2ServCert\" \"$ces1ServCert\"" "p2p $ces2PublicIp $ces1PublicIp" "rip"

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
   }

#

   proc T-007 {} {

      set error_code "FAIL"
      set testName "T-007"

      testStartLog $testName

      set purpose {Verify you can create a static Peer to Peer IPSec Branch Office tunnel with Text Pre-shared key and permit all filter}
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
      variable textPass

      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static IPSEC BOT "
      ConfigIpSecBO $swAddr1 $boName_ces1 $boGroup "text $textPass" "p2p $ces1PublicIp $ces2PublicIp" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static IPSEC BOT"
      ConfigIpSecBO $swAddr2 $boName_ces2 $boGroup "text $textPass" "p2p $ces2PublicIp $ces1PublicIp" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      if {[VerifyBoConnection "IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete IPSEC BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete IPSEC BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2

      testEndLog $testName $error_code
   }


   proc T-008 {} {

      set error_code "FAIL"
      set testName "T-008"

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
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete IPSEC BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete IPSEC BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2

      testEndLog $testName $error_code
   }


   proc T-009 {} {

      set testName "T-009"
      set error_code "FAIL"

      testStartLog $testName

      set purpose {Verify you can create a Static Peer to Peer IPSec Branch Office tunnel over Ethernet with Cerificates (Entrust, Verisign, and Microsoft CA) and permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable certInstalled
      if { $certInstalled != 1 } {
         logFile "The certificates are wrong or they are not installed"
         testEndLog $testName "ABORT"
         return
      }

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicIp

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2

      variable ces1ServCert
      variable ces2ServCert
      variable ces1CaCert
      variable ces2CaCert

      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static IPSEC BOT with Certificates"
      ConfigIpSecBO $swAddr1 "tunnel_test_1" $boGroup "certificate \"$ces1CaCert\" \"$ces1ServCert\" \"$ces2ServCert\"" "p2p $ces1PublicIp $ces2PublicIp" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static IPSEC BOT with Certificates"
      ConfigIpSecBO $swAddr2 "tunnel_test_2" $boGroup "certificate \"$ces1CaCert\" \"$ces2ServCert\" \"$ces1ServCert\"" "p2p $ces2PublicIp $ces1PublicIp" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      if {[VerifyBoConnection "IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }
      logFile "CES: $swAddr1 - delete IPSEC BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete IPSEC BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2

      testEndLog $testName $error_code
   }

#

   proc T-012 {} {

      set error_code "FAIL"
      set testName "T-012"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic Peer to Peer PPTP Branch Office tunnel over Ethernet with Local/ Peer Authentication that includes MS-CHAPV2 and none encryption, enable compression, with permit all filter}
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
      logFile "CES: $swAddr1 - add dynamic rip PPTP BOT / no encryption / with compression"
      ConfigPPTPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "p2p $ces1PublicIp $ces2PublicIp" "rip"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "pptp" "none"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "pptp" "enable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "pptp" "enable"

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip PPTP BOT / no encryption / with compression"
      ConfigPPTPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "p2p $ces2PublicIp $ces1PublicIp" "rip"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "pptp" "none"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "pptp" "enable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "pptp" "enable"

      if {[VerifyBoConnection "PPTP"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete PPTP BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp  255.255.255.0 $swAddr1
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete PPTP BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp  255.255.255.0 $swAddr2
      DisableRip $swAddr2

      testEndLog $testName $error_code
   }


   proc T-013 {} {

      set error_code "FAIL"
      set testName "T-013"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic Peer to Peer PPTP Branch Office tunnel over Ethernet with Local/ Peer Authentication that includes MS-CHAPV2 and RC4-40 encryption, enable compression, with permit all filter}
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
      logFile "CES: $swAddr1 - add dynamic rip PPTP BOT / rc4-40 encryption / with compression"
      ConfigPPTPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "p2p $ces1PublicIp $ces2PublicIp" "rip"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "pptp" "rc4_40"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "pptp" "enable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "pptp" "enable"

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip PPTP BOT / rc4-40 encryption / with compression"
      ConfigPPTPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "p2p $ces2PublicIp $ces1PublicIp" "rip"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "pptp" "rc4_40"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "pptp" "enable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "pptp" "enable"

      if {[VerifyBoConnection "PPTP"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete PPTP BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp  255.255.255.0 $swAddr1
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete PPTP BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp  255.255.255.0 $swAddr2
      DisableRip $swAddr2

      testEndLog $testName $error_code
   }


   proc T-014 {} {

      set error_code "FAIL"
      set testName "T-014"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic Peer to Peer PPTP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-40 encryption with no compression/stateless mode compression and permit all filter}
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
      logFile "CES: $swAddr1 - add dynamic rip PPTP BOT / rc4-40 encryption / no compression"
      ConfigPPTPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "p2p $ces1PublicIp $ces2PublicIp" "rip"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "pptp" "rc4_40"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "pptp" "disable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "pptp" "disable"

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip PPTP BOT / rc4-40 encryption / no compression"
      ConfigPPTPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "p2p $ces2PublicIp $ces1PublicIp" "rip"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "pptp" "rc4_40"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "pptp" "disable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "pptp" "disable"

      if {[VerifyBoConnection "PPTP"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete PPTP BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp  255.255.255.0 $swAddr1
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete PPTP BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp  255.255.255.0 $swAddr2
      DisableRip $swAddr2

      testEndLog $testName $error_code
   }


   proc T-015 {} {

      set error_code "FAIL"
      set testName "T-015"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic Peer to Peer PPTP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-128 encryption with compression/stateless mode compression and permit all filter}
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
      logFile "CES: $swAddr1 - add dynamic rip PPTP BOT / rc4-128 encryption / with compression"
      ConfigPPTPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "p2p $ces1PublicIp $ces2PublicIp" "rip"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "pptp" "rc4_128"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "pptp" "enable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "pptp" "enable"

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip PPTP BOT / rc4-128 encryption / with compression"
      ConfigPPTPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "p2p $ces2PublicIp $ces1PublicIp" "rip"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "pptp" "rc4_128"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "pptp" "enable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "pptp" "enable"

      if {[VerifyBoConnection "PPTP"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete PPTP BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp  255.255.255.0 $swAddr1
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete PPTP BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp  255.255.255.0 $swAddr2
      DisableRip $swAddr2

      testEndLog $testName $error_code
   }


   proc T-016 {} {

      set error_code "FAIL"
      set testName "T-016"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic Peer to Peer PPTP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-128 encryption with no compression/stateless compression and permit all filter}
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
      logFile "CES: $swAddr1 - add dynamic rip PPTP BOT / rc4-128 encryption / no compression"
      ConfigPPTPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "p2p $ces1PublicIp $ces2PublicIp" "rip"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "pptp" "rc4_128"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "pptp" "disable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "pptp" "disable"

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip PPTP BOT / rc4-128 encryption / no compression"
      ConfigPPTPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "p2p $ces2PublicIp $ces1PublicIp" "rip"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "pptp" "rc4_128"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "pptp" "disable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "pptp" "disable"

      if {[VerifyBoConnection "PPTP"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete PPTP BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp  255.255.255.0 $swAddr1
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete PPTP BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp  255.255.255.0 $swAddr2
      DisableRip $swAddr2

      testEndLog $testName $error_code
   }






   proc T-023 {} {

      set error_code "FAIL"
      set testName "T-023"

      testStartLog $testName

      set purpose {Verify you can create a Static Peer to Peer PPTP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and none encryption with no compression/stateless mode compression and permit all filter}
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
      logFile "CES: $swAddr1 - add static PPTP BOT / no encryption / no compression"
      ConfigPPTPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "p2p $ces1PublicIp $ces2PublicIp" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "pptp" "none"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "pptp" "disable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "pptp" "disable"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static PPTP BOT / no encryption / no compression"
      ConfigPPTPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "p2p $ces2PublicIp $ces1PublicIp" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "pptp" "none"
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
   }


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
   }


   proc T-025 {} {

      set error_code "FAIL"
      set testName "T-025"

      testStartLog $testName

      set purpose {Verify you can create a Static Peer to Peer PPTP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-128 encryption with no compression/stateless}
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
      logFile "CES: $swAddr1 - add static PPTP BOT / rc4-128 encryption / no compression"
      ConfigPPTPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "p2p $ces1PublicIp $ces2PublicIp" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "pptp" "rc4_128"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "pptp" "disable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "pptp" "disable"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static PPTP BOT / rc4-128 encryption / no compression"
      ConfigPPTPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "p2p $ces2PublicIp $ces1PublicIp" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "pptp" "rc4_128"
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
   }





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
   }


   proc T-030 {} {

      set error_code "FAIL"
      set testName "T-030"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/ Peer Authentication that includes MS-CHAPV2 and none encryption, Enabled compression, compression stateless mode disabled, default L2TP concentrator with permit all filter}
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
      logFile "CES: $swAddr1 - add dynamic rip L2TP BOT / no encryption / with compression / no compression stateless mode"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 l2tpPass" "p2p $ces1PublicIp $ces2PublicIp" "rip"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "none"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip L2TP BOT / no encryption / with compression / no compression stateless mode"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 l2tpPass" "p2p $ces2PublicIp $ces1PublicIp" "rip"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "none"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"

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
   }


   proc T-031 {} {

      set error_code "FAIL"
      set testName "T-031"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-40 encryption with Enabled compression and stateless mode compression enabled and permit all filter}
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
      logFile "CES: $swAddr1 - add dynamic rip L2TP BOT / RC4-40 encryption / with compression"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 l2tpPass" "p2p $ces1PublicIp $ces2PublicIp" "rip"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "RC4_40"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "enable"

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip L2TP BOT / RC4-40 encryption / with compression"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 l2tpPass" "p2p $ces2PublicIp $ces1PublicIp" "rip"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "RC4_40"
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
   }


   proc T-032 {} {

      set error_code "FAIL"
      set testName "T-032"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-128 encryption with Enabled compression and stateless mode compression enabled and permit all filter}
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
      logFile "CES: $swAddr1 - add dynamic rip L2TP BOT / RC4-128 encryption / with compression"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 l2tpPass" "p2p $ces1PublicIp $ces2PublicIp" "rip"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "RC4_128"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "enable"

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip L2TP BOT / RC4-128 encryption / with compression"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 l2tpPass" "p2p $ces2PublicIp $ces1PublicIp" "rip"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "RC4_128"
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
   }


   proc T-033 {} {

      set error_code "FAIL"
      set testName "T-033"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-40 encryption with Enabled compression and stateless mode compression disabled and permit all filter}
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
      logFile "CES: $swAddr1 - add dynamic rip L2TP BOT / RC4-40 encryption / with compression / no compression stateless mode"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 l2tpPass" "p2p $ces1PublicIp $ces2PublicIp" "rip"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "RC4_40"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip L2TP BOT / RC4-40 encryption / with compression / no compression stateless mode"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 l2tpPass" "p2p $ces2PublicIp $ces1PublicIp" "rip"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "RC4_40"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"

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
   }


   proc T-034 {} {

      set error_code "FAIL"
      set testName "T-034"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-128 encryption with Enabled compression and stateless mode compression disabled and permit all filter}
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
      logFile "CES: $swAddr1 - add dynamic rip L2TP BOT / RC4-128 encryption / with compression / no compression stateless mode"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 l2tpPass" "p2p $ces1PublicIp $ces2PublicIp" "rip"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "RC4_128"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip L2TP BOT / RC4-128 encryption / with compression / no compression stateless mode"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 l2tpPass" "p2p $ces2PublicIp $ces1PublicIp" "rip"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "RC4_128"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"

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
   }


   proc T-035 {} {

      set error_code "FAIL"
      set testName "T-035"

      testStartLog $testName

      set purpose {}
      set description {Verify you can create a Dynamic Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-40 encryption with compression set to Disabled, set IPSec Encryption Not Required, with permit all filter}
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
      logFile "CES: $swAddr1 - add dynamic rip L2TP BOT / RC4-40 encryption / no compression"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 l2tpPass" "p2p $ces1PublicIp $ces2PublicIp" "rip"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "RC4_40"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip L2TP BOT / RC4-40 encryption / no compression"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 l2tpPass" "p2p $ces2PublicIp $ces1PublicIp" "rip"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "RC4_40"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"

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
   }


   proc T-036 {} {

      set error_code "FAIL"
      set testName "T-036"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and no L2TP encryption with compression set to Disabled, set IPSec Encryption Triple DES pre-shared text key, with permit all filter}
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
      variable textPass

      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      logFile "CES: $swAddr1 - add dynamic rip L2TP BOT / no encryption / no compression"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 l2tpPass" "p2p $ces1PublicIp $ces2PublicIp" "rip"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "none"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"
      logFile "CES: $swAddr1 - add IPSEC over L2TP BOT / 3des data protection / text authentication"
      SetIPSecOverL2TP $swAddr1 $boName_ces1 $boGroup "3des" "text $textPass"

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip L2TP BOT / no encryption / no compression"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 l2tpPass" "p2p $ces2PublicIp $ces1PublicIp" "rip"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "none"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"
      logFile "CES: $swAddr2 - add IPSEC over L2TP BOT / 3des data protection / text authentication"
      SetIPSecOverL2TP $swAddr2 $boName_ces2 $boGroup "3des" "text $textPass"

      if {[VerifyBoConnection "L2TP/IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete L2TP/IPSEC BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp  255.255.255.0 $swAddr1
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete L2TP/IPSEC BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp  255.255.255.0 $swAddr2
      DisableRip $swAddr2

      testEndLog $testName $error_code
   }


   proc T-037 {} {

      set error_code "FAIL"
      set testName "T-037"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and no L2TP encryption with compression set to Disabled, set IPSec Encryption Triple DES pre-shared HEX key, with permit all filter}
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

      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      logFile "CES: $swAddr1 - add dynamic rip L2TP BOT / no encryption / no compression"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 l2tpPass" "p2p $ces1PublicIp $ces2PublicIp" "rip"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "none"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"
      logFile "CES: $swAddr1 - add IPSEC over L2TP BOT / 3des data protection / hex authentication"
      SetIPSecOverL2TP $swAddr1 $boName_ces1 $boGroup "3des" "hex $hexPass"

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip L2TP BOT / no encryption / no compression"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 l2tpPass" "p2p $ces2PublicIp $ces1PublicIp" "rip"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "none"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"
      logFile "CES: $swAddr2 - add IPSEC over L2TP BOT / 3des data protection / hex authentication"
      SetIPSecOverL2TP $swAddr2 $boName_ces2 $boGroup "3des" "hex $hexPass"

      if {[VerifyBoConnection "L2TP/IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete L2TP/IPSEC BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp  255.255.255.0 $swAddr1
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete L2TP/IPSEC BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp  255.255.255.0 $swAddr2
      DisableRip $swAddr2

      testEndLog $testName $error_code
   }


   proc T-038 {} {

      set testName "T-038"
      set error_code "FAIL"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and no L2TP encryption with compression set to Disabled, set IPSec Encryption Triple DES Certificates (Entrust, Verisign, and Microsoft CA), with permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable certInstalled
      if { $certInstalled != 1 } {
         logFile "The certificates are wrong or they are not installed"
         testEndLog $testName "ABORT"
         return
      }

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicIp

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2

      variable ces1ServCert
      variable ces2ServCert
      variable ces1CaCert
      variable ces2CaCert

      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      logFile "CES: $swAddr1 - add dynamic rip L2TP BOT / no encryption / no compression"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 l2tpPass" "p2p $ces1PublicIp $ces2PublicIp" "rip"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "none"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"
      logFile "CES: $swAddr1 - add IPSEC over L2TP BOT with Certificates/ 3des data protection"
      SetIPSecOverL2TP $swAddr1 $boName_ces1 $boGroup "3des" "certificate \"$ces1CaCert\" \"$ces1ServCert\" \"$ces2ServCert\""

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip L2TP BOT / no encryption / no compression"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 l2tpPass" "p2p $ces2PublicIp $ces1PublicIp" "rip"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "none"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"
      logFile "CES: $swAddr2 - add IPSEC over L2TP BOT  with Certificates / 3des data protection"
      SetIPSecOverL2TP $swAddr2 $boName_ces2 $boGroup "3des" "certificate \"$ces1CaCert\" \"$ces2ServCert\" \"$ces1ServCert\""

      if {[VerifyBoConnection "L2TP/IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete L2TP/IPSEC BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp  255.255.255.0 $swAddr1
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete L2TP/IPSEC BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp  255.255.255.0 $swAddr2
      DisableRip $swAddr2

      testEndLog $testName $error_code
   }


   proc T-039 {} {

      set error_code "FAIL"
      set testName "T-039"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and no L2TP encryption with compression set to Disabled, set IPSec Encryption 56 bit DES Pre-shared text key, with permit all filter}
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
      variable textPass

      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      logFile "CES: $swAddr1 - add dynamic rip L2TP BOT / no encryption / no compression"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 l2tpPass" "p2p $ces1PublicIp $ces2PublicIp" "rip"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "none"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"
      logFile "CES: $swAddr1 - add IPSEC over L2TP BOT / des56 data protection / text authentication"
      SetIPSecOverL2TP $swAddr1 $boName_ces1 $boGroup "des56" "text $textPass"

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip L2TP BOT / no encryption / no compression"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 l2tpPass" "p2p $ces2PublicIp $ces1PublicIp" "rip"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "none"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"
      logFile "CES: $swAddr2 - add IPSEC over L2TP BOT / des56 data protection / text authentication"
      SetIPSecOverL2TP $swAddr2 $boName_ces2 $boGroup "des56" "text $textPass"

      if {[VerifyBoConnection "L2TP/IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete L2TP/IPSEC BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp  255.255.255.0 $swAddr1
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete L2TP/IPSEC BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp  255.255.255.0 $swAddr2
      DisableRip $swAddr2

      testEndLog $testName $error_code
   }


   proc T-040 {} {

      set error_code "FAIL"
      set testName "T-040"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and no L2TP encryption with compression set to Disabled, set IPSec Encryption 56 bit DES Pre-shared HEX key, with permit all filter}
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

      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      logFile "CES: $swAddr1 - add dynamic rip L2TP BOT / no encryption / no compression"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 l2tpPass" "p2p $ces1PublicIp $ces2PublicIp" "rip"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "none"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"
      logFile "CES: $swAddr1 - add IPSEC over L2TP BOT / des56 data protection / hex authentication"
      SetIPSecOverL2TP $swAddr1 $boName_ces1 $boGroup "des56" "hex $hexPass"

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip L2TP BOT / no encryption / no compression"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 l2tpPass" "p2p $ces2PublicIp $ces1PublicIp" "rip"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "none"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"
      logFile "CES: $swAddr2 - add IPSEC over L2TP BOT / des56 data protection / hex authentication"
      SetIPSecOverL2TP $swAddr2 $boName_ces2 $boGroup "des56" "hex $hexPass"

      if {[VerifyBoConnection "L2TP/IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete L2TP/IPSEC BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp  255.255.255.0 $swAddr1
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete L2TP/IPSEC BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp  255.255.255.0 $swAddr2
      DisableRip $swAddr2

      testEndLog $testName $error_code
   }


   proc T-041 {} {

      set testName "T-041"
      set error_code "FAIL"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and no L2TP encryption with compression set to Disabled, set IPSec Encryption 56 bit DES Certificates (Entrust, Verisign, and Microsoft CA), with permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable certInstalled
      if { $certInstalled != 1 } {
         logFile "The certificates are wrong or they are not installed"
         testEndLog $testName "ABORT"
         return
      }

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicIp

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2

      variable ces1ServCert
      variable ces2ServCert
      variable ces1CaCert
      variable ces2CaCert

      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      logFile "CES: $swAddr1 - add dynamic rip L2TP BOT / no encryption / no compression"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 l2tpPass" "p2p $ces1PublicIp $ces2PublicIp" "rip"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "none"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"

      logFile "CES: $swAddr1 - add IPSEC over L2TP BOT with Certificates/ des56 data protection"
      SetIPSecOverL2TP $swAddr1 $boName_ces1 $boGroup "des56" "certificate \"$ces1CaCert\" \"$ces1ServCert\" \"$ces2ServCert\""

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip L2TP BOT / no encryption / no compression"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 l2tpPass" "p2p $ces2PublicIp $ces1PublicIp" "rip"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "none"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"

      logFile "CES: $swAddr2 - add IPSEC over L2TP BOT  with Certificates / des56 data protection"
      SetIPSecOverL2TP $swAddr2 $boName_ces2 $boGroup "des56" "certificate \"$ces1CaCert\" \"$ces2ServCert\" \"$ces1ServCert\""

      if {[VerifyBoConnection "L2TP/IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete L2TP/IPSEC BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp  255.255.255.0 $swAddr1
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete L2TP/IPSEC BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp  255.255.255.0 $swAddr2
      DisableRip $swAddr2

      testEndLog $testName $error_code
   }





   proc T-044 {} {

      set error_code "FAIL"
      set testName "T-044"

      testStartLog $testName

      set purpose {Verify you can create a Static Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/ Peer Authentication that includes MS-CHAPV2 and none encryption, Enabled compression, compression stateless mode enabled, default L2TP concentrator with permit all filter}
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
      logFile "CES: $swAddr1 - add static L2TP BOT / no encryption / with compression"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 l2tpPass" "p2p $ces1PublicIp $ces2PublicIp" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "none"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "enable"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static L2TP BOT / no encryption / with compression"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 l2tpPass" "p2p $ces2PublicIp $ces1PublicIp" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "none"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "enable"

      if {[VerifyBoConnection "L2TP"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete L2TP BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete L2TP BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2

      testEndLog $testName $error_code
   }


   proc T-045 {} {

      set error_code "FAIL"
      set testName "T-045"

      testStartLog $testName

      set purpose {Verify you can create a Static Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/ Peer Authentication that includes MS-CHAPV2 and none encryption, Enabled compression, compression stateless mode disabled, default L2TP concentrator with permit all filter}
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
      logFile "CES: $swAddr1 - add static L2TP BOT / no encryption / with compression / no compression stateless mode"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 l2tpPass" "p2p $ces1PublicIp $ces2PublicIp" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "none"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static L2TP BOT / no encryption / with compression / no compression stateless mode"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 l2tpPass" "p2p $ces2PublicIp $ces1PublicIp" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "none"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"

      if {[VerifyBoConnection "L2TP"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete L2TP BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete L2TP BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2

      testEndLog $testName $error_code
   }


   proc T-046 {} {

      set error_code "FAIL"
      set testName "T-046"

      testStartLog $testName

      set purpose {Verify you can create a Static Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-40 encryption with Enabled compression and stateless mode compression enabled and permit all filter}
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
      logFile "CES: $swAddr1 - add static L2TP BOT / RC4-40 encryption / with compression"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 l2tpPass" "p2p $ces1PublicIp $ces2PublicIp" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "RC4_40"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "enable"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static L2TP BOT / RC4-40 encryption / with compression"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 l2tpPass" "p2p $ces2PublicIp $ces1PublicIp" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "RC4_40"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "enable"

      if {[VerifyBoConnection "L2TP"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete L2TP BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete L2TP BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2

      testEndLog $testName $error_code
   }


   proc T-047 {} {

      set error_code "FAIL"
      set testName "T-047"

      testStartLog $testName

      set purpose {Verify you can create a Static Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-128 encryption with Enabled compression and stateless mode compression enabled and permit all filter}
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
      logFile "CES: $swAddr1 - add static L2TP BOT / RC4-128 encryption / with compression"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 l2tpPass" "p2p $ces1PublicIp $ces2PublicIp" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "RC4_128"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "enable"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static L2TP BOT / RC4-128 encryption / with compression"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 l2tpPass" "p2p $ces2PublicIp $ces1PublicIp" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "RC4_128"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "enable"

      if {[VerifyBoConnection "L2TP"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete L2TP BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete L2TP BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2

      testEndLog $testName $error_code
   }


   proc T-048 {} {

      set error_code "FAIL"
      set testName "T-048"

      testStartLog $testName

      set purpose {Verify you can create a Static Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-40 encryption with Enabled compression and stateless mode compression disabled and permit all filter}
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
      logFile "CES: $swAddr1 - add static L2TP BOT / RC4-40 encryption / with compression / no compression stateless mode"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 l2tpPass" "p2p $ces1PublicIp $ces2PublicIp" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "RC4_40"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static L2TP BOT / RC4-40 encryption / with compression / no compression stateless mode"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 l2tpPass" "p2p $ces2PublicIp $ces1PublicIp" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "RC4_40"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"

      if {[VerifyBoConnection "L2TP"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete L2TP BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete L2TP BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2

      testEndLog $testName $error_code
   }


   proc T-049 {} {

      set error_code "FAIL"
      set testName "T-049"

      testStartLog $testName

      set purpose {Verify you can create a Static Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-128 encryption with Enabled compression and stateless mode compression disabled and permit all filter}
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
      logFile "CES: $swAddr1 - add static L2TP BOT / RC4-128 encryption / with compression / no compression stateless mode"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 l2tpPass" "p2p $ces1PublicIp $ces2PublicIp" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "RC4_128"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static L2TP BOT / RC4-128 encryption / with compression / no compression stateless mode"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 l2tpPass" "p2p $ces2PublicIp $ces1PublicIp" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "RC4_128"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"

      if {[VerifyBoConnection "L2TP"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete L2TP BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete L2TP BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2

      testEndLog $testName $error_code
   }


   proc T-050 {} {

      set error_code "FAIL"
      set testName "T-050"

      testStartLog $testName

      set purpose {Verify you can create a Static Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-40 encryption with compression set to Disabled, set IPSec Encryption Not Required, with permit all filter}
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
      logFile "CES: $swAddr1 - add static L2TP BOT / RC4-40 encryption / no compression"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 l2tpPass" "p2p $ces1PublicIp $ces2PublicIp" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "RC4_40"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static L2TP BOT / RC4-40 encryption / with compression"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 l2tpPass" "p2p $ces2PublicIp $ces1PublicIp" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "RC4_40"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"

      if {[VerifyBoConnection "L2TP"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete L2TP BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete L2TP BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2

      testEndLog $testName $error_code
   }


   proc T-051 {} {

      set error_code "FAIL"
      set testName "T-051"

      testStartLog $testName

      set purpose {Verify you can create a Static Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and no L2TP encryption with compression set to Disabled, set IPSec Encryption Triple DES pre-shared text key, with permit all filter}
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
      variable textPass

      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static L2TP BOT / no encryption / no compression"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 l2tpPass" "p2p $ces1PublicIp $ces2PublicIp" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "none"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"
      logFile "CES: $swAddr1 - add IPSEC over L2TP BOT / 3des data protection / text authentication"
      SetIPSecOverL2TP $swAddr1 $boName_ces1 $boGroup "3des" "text $textPass"


      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static L2TP BOT / no encryption / no compression"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 l2tpPass" "p2p $ces2PublicIp $ces1PublicIp" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "none"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"
      logFile "CES: $swAddr2 - add IPSEC over L2TP BOT / 3des data protection / text authentication"
      SetIPSecOverL2TP $swAddr2 $boName_ces2 $boGroup "3des" "text $textPass"


      if {[VerifyBoConnection "L2TP/IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete L2TP/IPSEC BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete L2TP/IPSEC BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2

      testEndLog $testName $error_code
   }


   proc T-052 {} {

      set error_code "FAIL"
      set testName "T-052"

      testStartLog $testName

      set purpose {Verify you can create a Static Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and no L2TP encryption with compression set to Disabled, set IPSec Encryption Triple DES pre-shared HEX key, with permit all filter}
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
      logFile "CES: $swAddr1 - add static L2TP BOT / no encryption / no compression"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 l2tpPass" "p2p $ces1PublicIp $ces2PublicIp" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "none"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"
      logFile "CES: $swAddr1 - add IPSEC over L2TP BOT / 3des data protection / hex authentication"
      SetIPSecOverL2TP $swAddr1 $boName_ces1 $boGroup "3des" "hex $hexPass"


      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static L2TP BOT / no encryption / with compression"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 l2tpPass" "p2p $ces2PublicIp $ces1PublicIp" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "none"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"
      logFile "CES: $swAddr2 - add IPSEC over L2TP BOT / 3des data protection / hex authentication"
      SetIPSecOverL2TP $swAddr2 $boName_ces2 $boGroup "3des" "hex $hexPass"


      if {[VerifyBoConnection "L2TP/IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete L2TP/IPSEC BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete L2TP/IPSEC BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2

      testEndLog $testName $error_code
   }


   proc T-053 {} {

      set testName "T-053"
      set error_code "FAIL"

      testStartLog $testName

      set purpose {Verify you can create a Static Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and no L2TP encryption with compression set to Disabled, set IPSec Encryption Triple DES Certificates (Entrust, Verisign, and Microsoft CA), with permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable certInstalled
      if { $certInstalled != 1 } {
         logFile "The certificates are wrong or they are not installed"
         testEndLog $testName "ABORT"
         return
      }

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicIp

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2

      variable ces1ServCert
      variable ces2ServCert
      variable ces1CaCert
      variable ces2CaCert

      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static L2TP BOT / no encryption / no compression"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 l2tpPass" "p2p $ces1PublicIp $ces2PublicIp" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "none"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"
      logFile "CES: $swAddr1 - add IPSEC over L2TP BOT with Certificates/ 3des data protection"
      SetIPSecOverL2TP $swAddr1 $boName_ces1 $boGroup "3des" "certificate \"$ces1CaCert\" \"$ces1ServCert\" \"$ces2ServCert\""

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static L2TP BOT / no encryption / with compression"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 l2tpPass" "p2p $ces2PublicIp $ces1PublicIp" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "none"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"
      logFile "CES: $swAddr2 - add IPSEC over L2TP BOT  with Certificates / 3des data protection"
      SetIPSecOverL2TP $swAddr2 $boName_ces2 $boGroup "3des" "certificate \"$ces1CaCert\" \"$ces2ServCert\" \"$ces1ServCert\""

      if {[VerifyBoConnection "L2TP/IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete L2TP/IPSEC BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete L2TP/IPSEC BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2

      testEndLog $testName $error_code
   }


   proc T-054 {} {

      set error_code "FAIL"
      set testName "T-054"

      testStartLog $testName

      set purpose {Verify you can create a Static Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and no L2TP encryption with compression set to Disabled, set IPSec Encryption 56 bit DES Pre-shared text key, with permit all filter}
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
      variable textPass

      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static L2TP BOT / no encryption / no compression"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 l2tpPass" "p2p $ces1PublicIp $ces2PublicIp" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "none"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"

      logFile "CES: $swAddr1 - add IPSEC over L2TP BOT / des56 data protection / text authentication"
      SetIPSecOverL2TP $swAddr1 $boName_ces1 $boGroup "des56" "text $textPass"


      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static L2TP BOT / no encryption / no compression"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 l2tpPass" "p2p $ces2PublicIp $ces1PublicIp" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "none"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"

      logFile "CES: $swAddr2 - add IPSEC over L2TP BOT / des56 data protection / text authentication"
      SetIPSecOverL2TP $swAddr2 $boName_ces2 $boGroup "des56" "text $textPass"


      if {[VerifyBoConnection "L2TP/IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete L2TP/IPSEC BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete L2TP/IPSEC BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2

      testEndLog $testName $error_code
   }


   proc T-055 {} {

      set error_code "FAIL"
      set testName "T-055"

      testStartLog $testName

      set purpose {Verify you can create a Static Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and no L2TP encryption with compression set to Disabled, set IPSec Encryption 56 bit DES Pre-shared HEX key, with permit all filter}
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
      logFile "CES: $swAddr1 - add static L2TP BOT / no encryption / no compression"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 l2tpPass" "p2p $ces1PublicIp $ces2PublicIp" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "none"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"

      logFile "CES: $swAddr1 - add IPSEC over L2TP BOT / des56 data protection / hex authentication"
      SetIPSecOverL2TP $swAddr1 $boName_ces1 $boGroup "des56" "hex $hexPass"


      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static L2TP BOT / no encryption / with compression"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 l2tpPass" "p2p $ces2PublicIp $ces1PublicIp" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "none"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"

      logFile "CES: $swAddr2 - add IPSEC over L2TP BOT / des56 data protection / hex authentication"
      SetIPSecOverL2TP $swAddr2 $boName_ces2 $boGroup "des56" "hex $hexPass"


      if {[VerifyBoConnection "L2TP/IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete L2TP/IPSEC BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete L2TP/IPSEC BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2

      testEndLog $testName $error_code
   }


   proc T-056 {} {

      set testName "T-056"
      set error_code "FAIL"

      testStartLog $testName

      set purpose {Verify you can create a Static Peer to Peer L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and no L2TP encryption with compression set to Disabled, set IPSec Encryption 56 bit DES Certificates (Entrust, Verisign, and Microsoft CA), with permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable certInstalled
      if { $certInstalled != 1 } {
         logFile "The certificates are wrong or they are not installed"
         testEndLog $testName "ABORT"
         return
      }

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicIp

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2

      variable ces1ServCert
      variable ces2ServCert
      variable ces1CaCert
      variable ces2CaCert

      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static L2TP BOT / no encryption / no compression"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 l2tpPass" "p2p $ces1PublicIp $ces2PublicIp" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "none"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"

      logFile "CES: $swAddr1 - add IPSEC over L2TP BOT with Certificates/ des56 data protection"
      SetIPSecOverL2TP $swAddr1 $boName_ces1 $boGroup "des56" "certificate \"$ces1CaCert\" \"$ces1ServCert\" \"$ces2ServCert\""

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static L2TP BOT / no encryption / with compression"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 l2tpPass" "p2p $ces2PublicIp $ces1PublicIp" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "none"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"

      logFile "CES: $swAddr2 - add IPSEC over L2TP BOT  with Certificates / des56 data protection"
      SetIPSecOverL2TP $swAddr2 $boName_ces2 $boGroup "des56" "certificate \"$ces1CaCert\" \"$ces2ServCert\" \"$ces1ServCert\""

      if {[VerifyBoConnection "L2TP/IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete L2TP/IPSEC BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete L2TP/IPSEC BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2

      testEndLog $testName $error_code
   }






   proc T-060 {} {

      set error_code "FAIL"
      set testName "T-060"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic ABOT IPSec Branch Office tunnel over Ethernet with Text Pre-shared key and permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicSlot

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2
      variable textPass
      variable initiator_uid

      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      logFile "CES: $swAddr1 - add dynamic rip IPSEC ABOT / initiator / text pre-shared key"
      ConfigIpSecBO $swAddr1 $boName_ces1 $boGroup "text $textPass $initiator_uid" "initiator $ces2PublicIp $ces1PublicSlot" "rip"

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip IPSEC ABOT / responder / text pre-shared key"
      ConfigIpSecBO $swAddr2 $boName_ces2 $boGroup "text $textPass $initiator_uid" "responder" "rip"

      if {[VerifyBoConnection "IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete IPSEC ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete IPSEC ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      DisableRip $swAddr2

      testEndLog $testName $error_code
   }


   proc T-061 {} {

      set error_code "FAIL"
      set testName "T-061"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic ABOT IPSec Branch Office tunnel over Ethernet with Hex Pre-shared key and permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicSlot

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2
      variable hexPass
      variable initiator_uid

      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      logFile "CES: $swAddr1 - add dynamic rip IPSEC ABOT / initiator / hex pre-shared key"
      ConfigIpSecBO $swAddr1 $boName_ces1 $boGroup "hex $hexPass $initiator_uid" "initiator $ces2PublicIp $ces1PublicSlot" "rip"

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip IPSEC ABOT / responder / hex pre-shared key"
      ConfigIpSecBO $swAddr2 $boName_ces2 $boGroup "hex $hexPass $initiator_uid" "responder" "rip"

      if {[VerifyBoConnection "IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete IPSEC ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete IPSEC ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      DisableRip $swAddr2

      testEndLog $testName $error_code
   }


   proc T-062 {} {

      set testName "T-062"
      set error_code "FAIL"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic ABOT IPSec Branch Office over Ethernet with Cerificates (Entrust, Verisign, and Microsoft CA) and permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable certInstalled
      if { $certInstalled != 1 } {
         logFile "The certificates are wrong or they are not installed"
         testEndLog $testName "ABORT"
         return
      }

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicSlot

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2

      variable ces1ServCert
      variable ces2ServCert
      variable ces1CaCert
      variable ces2CaCert

      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      logFile "CES: $swAddr1 - add dynamic rip IPSEC ABOT with Certificates / initiator"
      ConfigIpSecBO $swAddr1 $boName_ces1 $boGroup "certificate \"$ces1CaCert\" \"$ces1ServCert\" \"$ces2ServCert\"" "initiator $ces2PublicIp $ces1PublicSlot" "rip"

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip IPSEC ABOT with Certificates / responder"
      ConfigIpSecBO $swAddr2 $boName_ces2 $boGroup "certificate \"$ces1CaCert\" \"$ces2ServCert\" \"$ces1ServCert\"" "responder" "rip"

      if {[VerifyBoConnection "IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete IPSEC ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete IPSEC ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      DisableRip $swAddr2

      testEndLog $testName $error_code

   }





   proc T-065 {} {

      set error_code "FAIL"
      set testName "T-065"

      variable swAddr1
      variable swAddr2

      testStartLog $testName

      set purpose {Verify you can create a Static ABOT IPSec Branch Office tunnel over Ethernet with Text Pre-shared key and permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicSlot

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2
      variable textPass
      variable initiator_uid

      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static IPSEC ABOT / initiator / text pre-shared key "
      ConfigIpSecBO $swAddr1 $boName_ces1 $boGroup "text $textPass $initiator_uid" "initiator $ces2PublicIp $ces1PublicSlot" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static IPSEC ABOT / responder / text pre-shared key"
      ConfigIpSecBO $swAddr2 $boName_ces2 $boGroup "text $textPass $initiator_uid" "responder" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      if {[VerifyBoConnection "IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete IPSEC ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete IPSEC ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2


      testEndLog $testName $error_code
   }


   proc T-066 {} {

      set error_code "FAIL"
      set testName "T-066"

      testStartLog $testName

      set purpose {Verify you can create a Static ABOT IPSec Branch Office tunnel over Ethernet with Hex Pre-shared key and permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicSlot

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2
      variable hexPass
      variable initiator_uid

      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static IPSEC ABOT / initiator / hex pre-shared key"
      ConfigIpSecBO $swAddr1 "tunnel_test_1" $boGroup "hex $hexPass $initiator_uid" "initiator $ces2PublicIp $ces1PublicSlot" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static IPSEC ABOT / responder / hex pre-shared key"
      ConfigIpSecBO $swAddr2 "tunnel_test_2" $boGroup "hex $hexPass $initiator_uid" "responder" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      if {[VerifyBoConnection "IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete IPSEC ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete IPSEC ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2


      testEndLog $testName $error_code
   }


   proc T-067 {} {

      set testName "T-067"
      set error_code "FAIL"

      testStartLog $testName

      set purpose {Verify you can create a Static ABOT IPSec Branch Office over Ethernet with Cerificates (Entrust, Verisign, and Microsoft CA) and permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable certInstalled
      if { $certInstalled != 1 } {
         logFile "The certificates are wrong or they are not installed"
         testEndLog $testName "ABORT"
         return
      }

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicSlot

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2

      variable ces1ServCert
      variable ces2ServCert
      variable ces1CaCert
      variable ces2CaCert

      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static IPSEC ABOT with Certificates / initiator"
      ConfigIpSecBO $swAddr1 "tunnel_test_1" $boGroup "certificate \"$ces1CaCert\" \"$ces1ServCert\" \"$ces2ServCert\"" "initiator $ces2PublicIp $ces1PublicSlot" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static IPSEC ABOT with Certificates / responder"
      ConfigIpSecBO $swAddr2 "tunnel_test_2" $boGroup "certificate \"$ces1CaCert\" \"$ces2ServCert\" \"$ces1ServCert\"" "responder" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      if {[VerifyBoConnection "IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete IPSEC ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete IPSEC ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2

      testEndLog $testName $error_code
   }


   proc T-068 {} {

      set error_code "FAIL"
      set testName "T-068"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic ABOT PPTP Branch Office tunnel over Ethernet with Local/ Peer Authentication that includes MS-CHAPV2 and none encryption, enable compression, with permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicSlot

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2


      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      logFile "CES: $swAddr1 - add dynamic rip PPTP ABOT / initiator / no encryption / with compression"
      ConfigPPTPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "initiator $ces2PublicIp $ces1PublicSlot" "rip"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "pptp" "none"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "pptp" "enable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "pptp" "enable"

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip PPTP ABOT / responder / no encryption / with compression"
      ConfigPPTPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "responder" "rip"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "pptp" "none"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "pptp" "enable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "pptp" "enable"

      if {[VerifyBoConnection "PPTP"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete PPTP ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp  255.255.255.0 $swAddr1
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete PPTP ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp  255.255.255.0 $swAddr2
      DisableRip $swAddr2

      testEndLog $testName $error_code
   }


   proc T-069 {} {

      set error_code "FAIL"
      set testName "T-069"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic ABOT PPTP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and none encryption with no compression/stateless mode compression and permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicSlot

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2


      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      logFile "CES: $swAddr1 - add dynamic rip PPTP ABOT / initiator / no encryption / no compression"
      ConfigPPTPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "initiator $ces2PublicIp $ces1PublicSlot" "rip"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "pptp" "none"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "pptp" "disable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "pptp" "disable"

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip PPTP ABOT / responder / no encryption / no compression"
      ConfigPPTPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "responder" "rip"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "pptp" "none"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "pptp" "disable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "pptp" "disable"

      if {[VerifyBoConnection "PPTP"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete PPTP ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp  255.255.255.0 $swAddr1
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete PPTP ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp  255.255.255.0 $swAddr2
      DisableRip $swAddr2

      testEndLog $testName $error_code
   }


   proc T-070 {} {

      set error_code "FAIL"
      set testName "T-070"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic ABOT PPTP Branch Office tunnel over Ethernet with Local/ Peer Authentication that includes MS-CHAPV2 and RC4-40 encryption, enable compression, with permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicSlot

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2


      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      logFile "CES: $swAddr1 - add dynamic rip PPTP ABOT / initiator / RC4-40 encryption / with compression"
      ConfigPPTPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "initiator $ces2PublicIp $ces1PublicSlot" "rip"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "pptp" "RC4_40"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "pptp" "enable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "pptp" "enable"

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip PPTP ABOT / responder / RC4-40 encryption / with compression"
      ConfigPPTPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "responder" "rip"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "pptp" "RC4_40"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "pptp" "enable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "pptp" "enable"

      if {[VerifyBoConnection "PPTP"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete PPTP ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp  255.255.255.0 $swAddr1
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete PPTP ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp  255.255.255.0 $swAddr2
      DisableRip $swAddr2

      testEndLog $testName $error_code
   }


   proc T-071 {} {

      set error_code "FAIL"
      set testName "T-071"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic ABOT PPTP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-40 encryption with no compression/stateless mode compression and permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicSlot

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2


      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      logFile "CES: $swAddr1 - add dynamic rip PPTP ABOT / initiator / RC4-40 encryption / no compression "
      ConfigPPTPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "initiator $ces2PublicIp $ces1PublicSlot" "rip"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "pptp" "RC4_40"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "pptp" "disable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "pptp" "disable"

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip PPTP ABOT / responder / RC4-40 encryption / no compression"
      ConfigPPTPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "responder" "rip"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "pptp" "RC4_40"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "pptp" "disable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "pptp" "disable"

      if {[VerifyBoConnection "PPTP"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete PPTP ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp  255.255.255.0 $swAddr1
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete PPTP ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp  255.255.255.0 $swAddr2
      DisableRip $swAddr2

      testEndLog $testName $error_code
   }


   proc T-072 {} {

      set error_code "FAIL"
      set testName "T-072"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic ABOT PPTP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-128 encryption with compression/stateless mode compression and permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicSlot

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2


      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      logFile "CES: $swAddr1 - add dynamic rip PPTP ABOT / initiator / RC4-128 encryption / with compression"
      ConfigPPTPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "initiator $ces2PublicIp $ces1PublicSlot" "rip"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "pptp" "RC4_128"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "pptp" "enable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "pptp" "enable"

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip PPTP ABOT / responder / RC4-128 encryption / with compression"
      ConfigPPTPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "responder" "rip"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "pptp" "RC4_128"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "pptp" "enable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "pptp" "enable"

      if {[VerifyBoConnection "PPTP"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete PPTP ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp  255.255.255.0 $swAddr1
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete PPTP ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp  255.255.255.0 $swAddr2
      DisableRip $swAddr2

      testEndLog $testName $error_code
   }


   proc T-073 {} {

      set error_code "FAIL"
      set testName "T-073"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic ABOT PPTP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-128 encryption with no compression/stateless compression and permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicSlot

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2


      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      logFile "CES: $swAddr1 - add dynamic rip PPTP ABOT / initiator / RC4-128 encryption / no compression "
      ConfigPPTPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "initiator $ces2PublicIp $ces1PublicSlot" "rip"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "pptp" "RC4_128"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "pptp" "disable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "pptp" "disable"

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip PPTP ABOT / responder / RC4-128 encryption / no compression"
      ConfigPPTPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "responder" "rip"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "pptp" "RC4_128"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "pptp" "disable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "pptp" "disable"

      if {[VerifyBoConnection "PPTP"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete PPTP ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp  255.255.255.0 $swAddr1
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete PPTP ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp  255.255.255.0 $swAddr2
      DisableRip $swAddr2

      testEndLog $testName $error_code
   }




   proc T-076 {} {

      set error_code "FAIL"
      set testName "T-076"

      testStartLog $testName

      set purpose {Verify you can create a Static ABOT PPTP Branch Office tunnel over Ethernet with Local/ Peer Authentication that includes MS-CHAPV2 and none encryption, enable compression, with permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicSlot

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2

      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static PPTP  ABOT / initiator / no encryption / with compression"
      ConfigPPTPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "initiator $ces2PublicIp $ces1PublicSlot" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "pptp" "none"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "pptp" "enable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "pptp" "enable"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static PPTP ABOT / responder / no encryption / with compression"
      ConfigPPTPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "responder" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "pptp" "none"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "pptp" "enable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "pptp" "enable"



      if {[VerifyBoConnection "PPTP"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete PPTP ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete PPTP ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2

      testEndLog $testName $error_code
   }


   proc T-077 {} {

      set error_code "FAIL"
      set testName "T-077"

      testStartLog $testName

      set purpose {Verify you can create a Static ABOT PPTP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and none encryption with no compression/stateless mode compression and permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicSlot

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2

      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static PPTP  ABOT / initiator / no encryption / no compression"
      ConfigPPTPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "initiator $ces2PublicIp $ces1PublicSlot" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "pptp" "none"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "pptp" "disable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "pptp" "disable"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static PPTP ABOT / responder / no encryption / no compression"
      ConfigPPTPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "responder" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "pptp" "none"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "pptp" "disable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "pptp" "disable"

      if {[VerifyBoConnection "PPTP"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete PPTP ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete PPTP ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2

      testEndLog $testName $error_code
   }


   proc T-078 {} {

      set error_code "FAIL"
      set testName "T-078"

      testStartLog $testName

      set purpose {Verify you can create a Static ABOT PPTP Branch Office tunnel over Ethernet with Local/ Peer Authentication that includes MS-CHAPV2 and RC4-40 encryption, enable compression, with permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicSlot

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2

      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static PPTP  ABOT / initiator / RC4-40 encryption / with compression"
      ConfigPPTPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "initiator $ces2PublicIp $ces1PublicSlot" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "pptp" "RC4_40"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "pptp" "enable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "pptp" "enable"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static PPTP ABOT / responder / RC4-40 encryption / with compression"
      ConfigPPTPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "responder" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "pptp" "RC4_40"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "pptp" "enable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "pptp" "enable"

      if {[VerifyBoConnection "PPTP"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete PPTP ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete PPTP ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2

      testEndLog $testName $error_code
   }


   proc T-079 {} {

      set error_code "FAIL"
      set testName "T-079"

      testStartLog $testName

      set purpose {Verify you can create a Static ABOT PPTP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-40 encryption with no compression/stateless mode compression and permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicSlot

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2

      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static PPTP  ABOT / initiator / RC4-40 encryption / no compression"
      ConfigPPTPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "initiator $ces2PublicIp $ces1PublicSlot" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "pptp" "RC4_40"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "pptp" "disable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "pptp" "disable"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static PPTP ABOT / responder / RC4-40 encryption / no compression"
      ConfigPPTPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "responder" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "pptp" "RC4_40"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "pptp" "disable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "pptp" "disable"

      if {[VerifyBoConnection "PPTP"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete PPTP ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete PPTP ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2

      testEndLog $testName $error_code
   }


   proc T-080 {} {

      set error_code "FAIL"
      set testName "T-080"

      testStartLog $testName

      set purpose {Verify you can create a Static ABOT PPTP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-128 encryption with compression/stateless mode compression and permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicSlot

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2

      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static PPTP  ABOT / initiator / RC4-128 encryption / with compression"
      ConfigPPTPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "initiator $ces2PublicIp $ces1PublicSlot" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "pptp" "RC4_128"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "pptp" "enable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "pptp" "enable"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static PPTP ABOT / responder / RC4-128 encryption / with compression"
      ConfigPPTPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "responder" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "pptp" "RC4_128"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "pptp" "enable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "pptp" "enable"

      if {[VerifyBoConnection "PPTP"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete PPTP ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete PPTP ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2

      testEndLog $testName $error_code
   }


   proc T-081 {} {

      set error_code "FAIL"
      set testName "T-081"

      testStartLog $testName

      set purpose {Verify you can create a Static ABOT PPTP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-128 encryption with no compression/stateless compression and permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicSlot

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2

      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static PPTP  ABOT / initiator / RC4-128 encryption / no compression"
      ConfigPPTPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "initiator $ces2PublicIp $ces1PublicSlot" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "pptp" "RC4_128"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "pptp" "disable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "pptp" "disable"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static PPTP ABOT / responder / RC4-128 encryption / no compression"
      ConfigPPTPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "responder" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "pptp" "RC4_128"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "pptp" "disable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "pptp" "disable"

      if {[VerifyBoConnection "PPTP"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete PPTP ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete PPTP ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2

      testEndLog $testName $error_code
   }





   proc T-084 {} {

      set error_code "FAIL"
      set testName "T-084"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic ABOT L2TP Branch Office tunnel over Ethernet with Local/ Peer Authentication that includes MS-CHAPV2 and none encryption, Enabled compression, compression stateless mode enabled, default L2TP concentrator with permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicSlot

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2


      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      logFile "CES: $swAddr1 - add dynamic rip L2TP ABOT / initiator / no encryption / with compression"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "initiator $ces2PublicIp $ces1PublicSlot" "rip"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "none"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "enable"

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip L2TP ABOT / responder / no encryption / with compression"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "responder" "rip"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "none"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "enable"

      if {[VerifyBoConnection "L2TP"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete L2TP ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp  255.255.255.0 $swAddr1
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete L2TP ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp  255.255.255.0 $swAddr2
      DisableRip $swAddr2

      testEndLog $testName $error_code
   }


   proc T-085 {} {

      set error_code "FAIL"
      set testName "T-085"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic ABOT L2TP Branch Office tunnel over Ethernet with Local/ Peer Authentication that includes MS-CHAPV2 and none encryption, Enabled compression, compression stateless mode disabled, default L2TP concentrator with permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicSlot

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2


      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      logFile "CES: $swAddr1 - add dynamic rip L2TP ABOT / initiator / no encryption / with compression / no compression stateless mode"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "initiator $ces2PublicIp $ces1PublicSlot" "rip"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "none"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip L2TP ABOT / responder / no encryption / with compression / no compression stateless mode"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "responder" "rip"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "none"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"

      if {[VerifyBoConnection "L2TP"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete L2TP ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp  255.255.255.0 $swAddr1
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete L2TP ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp  255.255.255.0 $swAddr2
      DisableRip $swAddr2

      testEndLog $testName $error_code
   }


   proc T-086 {} {

      set error_code "FAIL"
      set testName "T-086"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic ABOT L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-40 encryption with Enabled compression and stateless mode compression enabled and permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicSlot

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2


      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      logFile "CES: $swAddr1 - add dynamic rip L2TP ABOT / initiator / RC4-40 encryption / with compression"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "initiator $ces2PublicIp $ces1PublicSlot" "rip"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "RC4_40"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "enable"

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip L2TP ABOT / responder / RC4-40 encryption / with compression"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "responder" "rip"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "RC4_40"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "enable"

      if {[VerifyBoConnection "L2TP"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete L2TP ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp  255.255.255.0 $swAddr1
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete L2TP ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp  255.255.255.0 $swAddr2
      DisableRip $swAddr2

      testEndLog $testName $error_code
   }


   proc T-087 {} {

      set error_code "FAIL"
      set testName "T-087"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic ABOT L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-128 encryption with Enabled compression and stateless mode compression enabled and permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicSlot

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2


      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      logFile "CES: $swAddr1 - add dynamic rip L2TP ABOT / initiator / RC4-128 encryption / with compression"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "initiator $ces2PublicIp $ces1PublicSlot" "rip"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "RC4_128"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "enable"

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip L2TP ABOT / responder / RC4-128 encryption / with compression"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "responder" "rip"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "RC4_128"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "enable"

      if {[VerifyBoConnection "L2TP"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete L2TP ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp  255.255.255.0 $swAddr1
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete L2TP ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp  255.255.255.0 $swAddr2
      DisableRip $swAddr2

      testEndLog $testName $error_code
   }


   proc T-088 {} {

      set error_code "FAIL"
      set testName "T-088"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic ABOT L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-40 encryption with Enabled compression and stateless mode compression disabled and permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicSlot

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2


      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      logFile "CES: $swAddr1 - add dynamic rip L2TP ABOT / initiator / RC4-40 encryption / with compression / no compression stateless mode"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "initiator $ces2PublicIp $ces1PublicSlot" "rip"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "RC4_40"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip L2TP ABOT / responder / RC4-40 encryption / with compression / no compression stateless mode"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "responder" "rip"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "RC4_40"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"

      if {[VerifyBoConnection "L2TP"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete L2TP ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp  255.255.255.0 $swAddr1
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete L2TP ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp  255.255.255.0 $swAddr2
      DisableRip $swAddr2

      testEndLog $testName $error_code
   }


   proc T-089 {} {

      set error_code "FAIL"
      set testName "T-089"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic ABOT L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-128 encryption with Enabled compression and stateless mode compression disabled and permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicSlot

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2


      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      logFile "CES: $swAddr1 - add dynamic rip L2TP ABOT / initiator / RC4-128 encryption / with compression / no compression stateless mode"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "initiator $ces2PublicIp $ces1PublicSlot" "rip"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "RC4_128"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip L2TP ABOT / responder / RC4-128 encryption / with compression / no compression stateless mode"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "responder" "rip"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "RC4_128"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"

      if {[VerifyBoConnection "L2TP"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete L2TP ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp  255.255.255.0 $swAddr1
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete L2TP ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp  255.255.255.0 $swAddr2
      DisableRip $swAddr2

      testEndLog $testName $error_code
   }


   proc T-090 {} {

      set error_code "FAIL"
      set testName "T-090"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic ABOT L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-40 encryption with compression set to Disabled, set IPSec Encryption Not Required, with permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicSlot

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2


      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      logFile "CES: $swAddr1 - add dynamic rip L2TP ABOT / initiator / no encryption / no compression"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "initiator $ces2PublicIp $ces1PublicSlot" "rip"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "none"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip L2TP ABOT / responder / no encryption / no compression"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "responder" "rip"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "none"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"

      if {[VerifyBoConnection "L2TP"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete L2TP ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp  255.255.255.0 $swAddr1
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete L2TP ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp  255.255.255.0 $swAddr2
      DisableRip $swAddr2

      testEndLog $testName $error_code
   }


   proc T-091 {} {

      set error_code "FAIL"
      set testName "T-091"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic ABOT L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and no L2TP encryption with compression set to Disabled, set IPSec Encryption Triple DES pre-shared text key, with permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicSlot

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2
      variable textPass
      variable initiator_uid


      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      logFile "CES: $swAddr1 - add dynamic rip L2TP ABOT / initiator / no encryption / no compression"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "initiator $ces2PublicIp $ces1PublicSlot" "rip"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "none"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"
      logFile "CES: $swAddr1 - add IPSEC over L2TP ABOT / 3des data protection / text authentication"
      SetIPSecOverL2TP $swAddr1 $boName_ces1 $boGroup "3des" "text $textPass $initiator_uid"


      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip L2TP ABOT / responder / no encryption / no compression"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "responder" "rip"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "none"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"
      logFile "CES: $swAddr2 - add IPSEC over L2TP ABOT / 3des data protection / text authentication"
      SetIPSecOverL2TP $swAddr2 $boName_ces2 $boGroup "3des" "text $textPass $initiator_uid"


      if {[VerifyBoConnection "L2TP/IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete L2TP/IPSEC ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp  255.255.255.0 $swAddr1
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete L2TP/IPSEC ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp  255.255.255.0 $swAddr2
      DisableRip $swAddr2

      testEndLog $testName $error_code
   }


   proc T-092 {} {

      set error_code "FAIL"
      set testName "T-092"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic ABOT L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and no L2TP encryption with compression set to Disabled, set IPSec Encryption Triple DES pre-shared HEX key, with permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicSlot

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2
      variable hexPass
      variable initiator_uid


      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      logFile "CES: $swAddr1 - add dynamic rip L2TP ABOT / initiator / no encryption / no compression"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "initiator $ces2PublicIp $ces1PublicSlot" "rip"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "none"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"
      logFile "CES: $swAddr1 - add IPSEC over L2TP ABOT / 3des data protection / hex authentication"
      SetIPSecOverL2TP $swAddr1 $boName_ces1 $boGroup "3des" "hex $hexPass $initiator_uid"

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip L2TP ABOT / responder / no encryption / no compression"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "responder" "rip"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "none"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"
      logFile "CES: $swAddr2 - add IPSEC over L2TP ABOT / 3des data protection / hex authentication"
      SetIPSecOverL2TP $swAddr2 $boName_ces2 $boGroup "3des" "hex $hexPass $initiator_uid"


      if {[VerifyBoConnection "L2TP/IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete L2TP/IPSEC ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp  255.255.255.0 $swAddr1
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete L2TP/IPSEC ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp  255.255.255.0 $swAddr2
      DisableRip $swAddr2

      testEndLog $testName $error_code
   }


   proc T-093 {} {

      set testName "T-093"
      set error_code "FAIL"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic ABOT L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and no L2TP encryption with compression set to Disabled, set IPSec Encryption Triple DES Certificates (Microsoft CA), with permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable certInstalled
      if { $certInstalled != 1 } {
         logFile "The certificates are wrong or they are not installed"
         testEndLog $testName "ABORT"
         return
      }

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicSlot

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2

      variable ces1ServCert
      variable ces2ServCert
      variable ces1CaCert
      variable ces2CaCert

      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      logFile "CES: $swAddr1 - add dynamic rip L2TP ABOT / initiator / no encryption / no compression"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "initiator $ces2PublicIp $ces1PublicSlot" "rip"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "none"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"
      logFile "CES: $swAddr1 - add IPSEC over L2TP ABOT with Certificates / 3des data protection"
      SetIPSecOverL2TP $swAddr1 $boName_ces1 $boGroup "3des" "certificate \"$ces1CaCert\" \"$ces1ServCert\" \"$ces2ServCert\""

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip L2TP ABOT / responder / no encryption / no compression"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "responder" "rip"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "none"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"
      logFile "CES: $swAddr2 - add IPSEC over L2TP ABOT with Certificates / 3des data protection"
      SetIPSecOverL2TP $swAddr2 $boName_ces2 $boGroup "3des" "certificate \"$ces1CaCert\" \"$ces2ServCert\" \"$ces1ServCert\""

      if {[VerifyBoConnection "L2TP/IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete L2TP/IPSEC ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp  255.255.255.0 $swAddr1
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete L2TP/IPSEC ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp  255.255.255.0 $swAddr2
      DisableRip $swAddr2

      testEndLog $testName $error_code
   }


   proc T-094 {} {

      set error_code "FAIL"
      set testName "T-094"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic ABOT L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and no L2TP encryption with compression set to Disabled, set IPSec Encryption 56 bit DES Pre-shared text key, with permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicSlot

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2
      variable textPass
      variable initiator_uid


      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      logFile "CES: $swAddr1 - add dynamic rip L2TP ABOT / initiator / no encryption / no compression"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "initiator $ces2PublicIp $ces1PublicSlot" "rip"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "none"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"
      logFile "CES: $swAddr1 - add IPSEC over L2TP BOT / des56 data protection / text authentication"
      SetIPSecOverL2TP $swAddr1 $boName_ces1 $boGroup "des56" "text $textPass $initiator_uid"

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip L2TP ABOT / responder / no encryption / no compression"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "responder" "rip"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "none"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"
      logFile "CES: $swAddr2 - add IPSEC over L2TP BOT / des56 data protection / text authentication"
      SetIPSecOverL2TP $swAddr2 $boName_ces2 $boGroup "des56" "text $textPass $initiator_uid"

      if {[VerifyBoConnection "L2TP/IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete L2TP/IPSEC ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp  255.255.255.0 $swAddr1
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete L2TP/IPSEC ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp  255.255.255.0 $swAddr2
      DisableRip $swAddr2

      testEndLog $testName $error_code
   }


   proc T-095 {} {

      set error_code "FAIL"
      set testName "T-095"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic ABOT L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and no L2TP encryption with compression set to Disabled, set IPSec Encryption 56 bit DES Pre-shared HEX key, with permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicSlot

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2
      variable hexPass
      variable initiator_uid


      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      logFile "CES: $swAddr1 - add dynamic rip L2TP ABOT / initiator / no encryption / no compression"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "initiator $ces2PublicIp $ces1PublicSlot" "rip"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "none"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"
      logFile "CES: $swAddr1 - add IPSEC over L2TP BOT / des56 data protection / hex authentication"
      SetIPSecOverL2TP $swAddr1 $boName_ces1 $boGroup "des56" "hex $hexPass $initiator_uid"

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip L2TP ABOT / responder / no encryption / no compression"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "responder" "rip"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "none"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"
      logFile "CES: $swAddr2 - add IPSEC over L2TP BOT / des56 data protection / hex authentication"
      SetIPSecOverL2TP $swAddr2 $boName_ces2 $boGroup "des56" "hex $hexPass $initiator_uid"

      if {[VerifyBoConnection "L2TP/IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete L2TP/IPSEC ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp  255.255.255.0 $swAddr1
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete L2TP/IPSEC ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp  255.255.255.0 $swAddr2
      DisableRip $swAddr2

      testEndLog $testName $error_code
   }


   proc T-096 {} {

      set testName "T-096"
      set error_code "FAIL"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic ABOT L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and no L2TP encryption with compression set to Disabled, set IPSec Encryption 56 bit DES Certificates (Microsoft CA), with permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable certInstalled
      if { $certInstalled != 1 } {
         logFile "The certificates are wrong or they are not installed"
         testEndLog $testName "ABORT"
         return
      }

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicSlot

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2

      variable ces1ServCert
      variable ces2ServCert
      variable ces1CaCert
      variable ces2CaCert

      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      logFile "CES: $swAddr1 - add dynamic rip L2TP ABOT / initiator / no encryption / no compression"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "initiator $ces2PublicIp $ces1PublicSlot" "rip"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "none"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"

      logFile "CES: $swAddr1 - add IPSEC over L2TP ABOT with Certificates / des56 data protection"
      SetIPSecOverL2TP $swAddr1 $boName_ces1 $boGroup "des56" "certificate \"$ces1CaCert\" \"$ces1ServCert\" \"$ces2ServCert\""


      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip L2TP ABOT / responder / no encryption / no compression"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "responder" "rip"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "none"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"

      logFile "CES: $swAddr2 - add IPSEC over L2TP ABOT with Certificates / des56 data protection"
      SetIPSecOverL2TP $swAddr2 $boName_ces2 $boGroup "des56" "certificate \"$ces1CaCert\" \"$ces2ServCert\" \"$ces1ServCert\""

      if {[VerifyBoConnection "L2TP/IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete L2TP/IPSEC ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp  255.255.255.0 $swAddr1
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete L2TP/IPSEC ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp  255.255.255.0 $swAddr2
      DisableRip $swAddr2

      testEndLog $testName $error_code
   }





   proc T-099 {} {

      set error_code "FAIL"
      set testName "T-099"

      testStartLog $testName

      set purpose {Verify you can create a Static ABOT L2TP Branch Office tunnel over Ethernet with Local/ Peer Authentication that includes MS-CHAPV2 and none encryption, Enabled compression, compression stateless mode enabled, default L2TP concentrator with permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicSlot

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2

      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static L2TP ABOT / initiator / no encryption / with compression"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "initiator $ces2PublicIp $ces1PublicSlot" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "none"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "enable"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static L2TP ABOT / responder / no encryption / with compression"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "responder" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "none"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "enable"

      if {[VerifyBoConnection "L2TP"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete L2TP ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete L2TP ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2

      testEndLog $testName $error_code
   }


   proc T-100 {} {

      set error_code "FAIL"
      set testName "T-100"

      testStartLog $testName

      set purpose {Verify you can create a Static ABOT L2TP Branch Office tunnel over Ethernet with Local/ Peer Authentication that includes MS-CHAPV2 and none encryption, Enabled compression, compression stateless mode disabled, default L2TP concentrator with permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicSlot

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2

      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static L2TP ABOT / initiator / no encryption / with compression / no compression stateless mode"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "initiator $ces2PublicIp $ces1PublicSlot" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "none"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static L2TP ABOT / responder / no encryption / with compression / no compression stateless mode"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "responder" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "none"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"

      if {[VerifyBoConnection "L2TP"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete L2TP ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete L2TP ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2

      testEndLog $testName $error_code
   }


   proc T-101 {} {

      set error_code "FAIL"
      set testName "T-101"

      testStartLog $testName

      set purpose {Verify you can create a Static ABOT L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and RC4-128 encryption with Enabled compression and stateless mode compression disabled and permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicSlot

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2

      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static L2TP ABOT / initiator / RC4-128 encryption / with compression / no compression stateless mode"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "initiator $ces2PublicIp $ces1PublicSlot" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "RC4_128"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static L2TP ABOT / responder / RC4-128 encryption / with compression / no compression stateless mode"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "responder" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "RC4_128"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "enable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"

      if {[VerifyBoConnection "L2TP"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete L2TP ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete L2TP ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2

      testEndLog $testName $error_code
   }


   proc T-102 {} {

      set testName "T-102"
      set error_code "FAIL"

      testStartLog $testName

      set purpose {Verify you can create a Static ABOT L2TP Branch Office tunnel over Ethernet with Local/Peer Authentication that includes MS-CHAPV2 and no L2TP encryption with compression set to Disabled, set IPSec Encryption Triple DES Certificates (Microsoft CA), with permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable certInstalled
      if { $certInstalled != 1 } {
         logFile "The certificates are wrong or they are not installed"
         testEndLog $testName "ABORT"
         return
      }

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicSlot

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2

      variable ces1ServCert
      variable ces2ServCert
      variable ces1CaCert
      variable ces2CaCert


      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static L2TP ABOT / initiator / no encryption / with compression"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "initiator $ces2PublicIp $ces1PublicSlot" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" "none"
      SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr1 $boName_ces1 $boGroup "l2tp" "disable"
      logFile "CES: $swAddr1 - add IPSEC over L2TP ABOT with Certificates / 3des data protection"
      SetIPSecOverL2TP $swAddr1 $boName_ces1 $boGroup "3des" "certificate \"$ces1CaCert\" \"$ces1ServCert\" \"$ces2ServCert\""

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static L2TP ABOT / responder / no encryption / with compression"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "responder" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
      SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" "none"
      SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"
      SetBOStatelessMode $swAddr2 $boName_ces2 $boGroup "l2tp" "disable"
      logFile "CES: $swAddr2 - add IPSEC over L2TP ABOT with Certificates / 3des data protection"
      SetIPSecOverL2TP $swAddr2 $boName_ces2 $boGroup "3des" "certificate \"$ces1CaCert\" \"$ces2ServCert\" \"$ces1ServCert\""

      if {[VerifyBoConnection "L2TP/IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete L2TP ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete L2TP ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2

      testEndLog $testName $error_code
   }


   proc T-103 {} {

      set error_code "FAIL"
      set testName "T-103"

      testStartLog $testName

      set purpose {Verify you can create a static Peer to Peer IPSec Branch Office Control Tunnel with Text Pre-shared key and permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable swAddr1
      variable swAddr2

      variable ces1ManagementIp
      variable ces1PublicIp

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2
      variable textPass

      #        AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static IPSEC BOT Control Tunnel"
      ConfigControlIpSecBO $swAddr1 $boName_ces1 $boGroup "text $textPass" "p2p $ces1PublicIp $ces2PublicIp" "static $ces1ManagementIp [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static IPSEC BOT"
      ConfigIpSecBO $swAddr2 $boName_ces2 $boGroup "text $textPass" "p2p $ces2PublicIp $ces1PublicIp" "static local_nets_2 $ces1ManagementIp 255.255.255.255 enable 0"

      if {[VerifyBoControlConnection  $ces1ManagementIp] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete IPSEC BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      #       DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete IPSEC BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2

      testEndLog $testName $error_code
   }


   proc T-104 {} {

      set error_code "FAIL"
      set testName "T-104"

      testStartLog $testName

      set purpose {Verify you can create a Static Peer to Peer IPSec Branch Office Control Tunnel with Hex Pre-shared key and permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable swAddr1
      variable swAddr2

      variable ces1ManagementIp
      variable ces1PublicIp

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2
      variable hexPass

      logFile "CES: $swAddr1 - add static IPSEC BOT Control Tunnel"
      ConfigControlIpSecBO $swAddr1 $boName_ces1 $boGroup "hex $hexPass" "p2p $ces1PublicIp $ces2PublicIp" "static $ces1ManagementIp [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static IPSEC BOT"
      ConfigIpSecBO $swAddr2 $boName_ces2 $boGroup "hex $hexPass" "p2p $ces2PublicIp $ces1PublicIp" "static local_nets_2 $ces1ManagementIp 255.255.255.255 enable 0"

      if {[VerifyBoControlConnection $ces1ManagementIp] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete IPSEC BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      #       DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete IPSEC BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2

      testEndLog $testName $error_code
   }


   proc T-105 {} {

      set testName "T-105"
      set error_code "FAIL"

      testStartLog $testName

      set purpose {Verify you can create a Static Peer to Peer IPSec Branch Office Control Tunnel with Cerificates (  Microsoft CA) and permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable certInstalled
      if { $certInstalled != 1 } {
         logFile "The certificates are wrong or they are not installed"
         testEndLog $testName "ABORT"
         return
      }

      variable swAddr1
      variable swAddr2

      variable ces1ManagementIp
      variable ces1PublicIp

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2

      variable ces1ServCert
      variable ces2ServCert
      variable ces1CaCert
      variable ces2CaCert

      logFile "CES: $swAddr1 - add static IPSEC BOT Control Tunnel with Certificates"
      ConfigControlIpSecBO $swAddr1 $boName_ces1 $boGroup "certificate \"$ces1CaCert\" \"$ces1ServCert\" \"$ces2ServCert\"" "p2p $ces1PublicIp $ces2PublicIp" "static $ces1ManagementIp [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static IPSEC BOT with Certificates"
      ConfigIpSecBO $swAddr2 $boName_ces2 $boGroup "certificate \"$ces1CaCert\" \"$ces2ServCert\" \"$ces1ServCert\"" "p2p $ces2PublicIp $ces1PublicIp" "static local_nets_2 $ces1ManagementIp 255.255.255.255 enable 0"

      if {[VerifyBoControlConnection $ces1ManagementIp] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete IPSEC BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      #       DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete IPSEC BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2

      testEndLog $testName $error_code
   }


   proc T-106 {} {

      set error_code "FAIL"
      set testName "T-106"

      testStartLog $testName

      set purpose {Verify you can create a static Peer to Peer IPSec Branch Office NAT Control Tunnel with Text Pre-shared key and permit all filter}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable swAddr1
      variable swAddr2

      variable ces1NatIp
      variable ces1PublicIp

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2
      variable textPass

      logFile "CES: $swAddr1 - add static IPSEC BOT NAT Control Tunnel"
      ConfigControlIpSecBO $swAddr1 $boName_ces1 $boGroup "text $textPass" "p2p $ces1PublicIp $ces2PublicIp" "static $ces1NatIp [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static IPSEC BOT"
      ConfigIpSecBO $swAddr2 $boName_ces2 $boGroup "text $textPass" "p2p $ces2PublicIp $ces1PublicIp" "static local_nets_2 $ces1NatIp 255.255.255.255 enable 0"

      if {[VerifyBoControlConnection $ces1NatIp] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete IPSEC BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1

      logFile "CES: $swAddr2 - delete IPSEC BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2

      testEndLog $testName $error_code
   }



   proc T-109 {} {

      set testName "T-109"

      set err_count 0
      set error_code "FAIL"

      testStartLog $testName

      set purpose {Verify that creating Dynamic IPSec Peer to Peer Branch Office Tunnel with a mis-matched pre-shared key to see if the tunnel comes up}
      set description {set different authentication for IPSEC BO}
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

      set ces1textPass "ces1Pass"
      set ces2textPass "ces2Pass"
      set ces1hexPass "aabbcc"
      set ces2hexPass "ababab"

      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2

      for {set i 1} {$i<=2} {incr i} {
         if {$i==1} {
            logFile "CES: $swAddr1 - add dynamic rip IPSEC BO with text pass: $ces1textPass"
            ConfigIpSecBO $swAddr1 $boName_ces1 $boGroup "text $ces1textPass" "p2p $ces1PublicIp $ces2PublicIp" "rip"

            logFile "CES: $swAddr2 - add dynamic rip IPSEC BO with text pass: $ces2textPass"
            ConfigIpSecBO $swAddr2 $boName_ces2 $boGroup "text $ces2textPass" "p2p $ces2PublicIp $ces1PublicIp" "rip"
         } else {

            logFile "CES: $swAddr1 - add dynamic rip IPSEC BO with hex pass: $ces1hexPass"
            SetIPSecAuthentication $swAddr1 $boName_ces1 $boGroup "hex" $ces1hexPass
            logFile "CES: $swAddr2 - add dynamic rip IPSEC BO with hex pass: $ces2hexPass"
            SetIPSecAuthentication $swAddr2 $boName_ces2 $boGroup "hex" $ces2hexPass
         }

         if {[VerifyNegativeBoConnection "IPSEC"] != "SUCCESS"} {
            incr err_count
         }
      }

      logFile "CES: $swAddr1 - delete IPSEC BO"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete IPSEC BO"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      DisableRip $swAddr2

      if {$err_count == 0} {
         set error_code "PASS"
      }

      testEndLog $testName $error_code
   }


   proc T-110 {} {

      set error_code "FAIL"
      set testName "T-110"
      set err_count 0

      testStartLog $testName

      set purpose {Bouncing Tunnels IPSEC}
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
      variable textPass

      set encrList_ces1 [GetAvailableBoGrpEncr $swAddr1 $boGroup]
      set encrList_ces2 $encrList_ces1

      set ikeEncrList [GetAvailableBoGrpIkeEncr $swAddr1 $boGroup]

      DisBoGrpEncrType $swAddr1 $boGroup "all"
      DisBoGrpEncrType $swAddr2 $boGroup "all"

      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static IPSEC BOT "
      ConfigIpSecBO $swAddr1 $boName_ces1 $boGroup "text $textPass" "p2p $ces1PublicIp $ces2PublicIp" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static IPSEC BOT"
      ConfigIpSecBO $swAddr2 $boName_ces2 $boGroup "text $textPass" "p2p $ces2PublicIp $ces1PublicIp" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      foreach ikeEncr $ikeEncrList {
         EnaBoGrpIkeEncrType $swAddr1 $boGroup $ikeEncr
         EnaBoGrpIkeEncrType $swAddr2 $boGroup $ikeEncr

         foreach encr_ces1 $encrList_ces1 {
            foreach encr_ces2 $encrList_ces2 {

               EnaBoGrpEncrType $swAddr1 $boGroup $encr_ces1
               logFile "CESs: $swAddr1 - IPSEC encryption type is set to \"$encr_ces1\""

               EnaBoGrpEncrType $swAddr2 $boGroup $encr_ces2
               logFile "CESs: $swAddr2 - IPSEC encryption type is set to \"$encr_ces2\""

               SetBoConnState $boName_ces1 $boGroup "enable" $swAddr1
               SetBoConnState $boName_ces2 $boGroup "enable" $swAddr2

               #aceWait 10000
               if {$encr_ces1==$encr_ces2 && [VerifyBoConnection] != "SUCCESS"} {
                  incr err_count
               } elseif {$encr_ces1!=$encr_ces2 &&  [VerifyNegativeBoConnection "" 2] != "SUCCESS"} {
                  incr err_count
               }

               SetBoConnState $boName_ces1 $boGroup "disable" $swAddr1
               SetBoConnState $boName_ces2 $boGroup "disable" $swAddr2

               DisBoGrpEncrType $swAddr1 $boGroup $encr_ces1
               DisBoGrpEncrType $swAddr2 $boGroup $encr_ces2

            }
            set encrList_ces2 [lrange $encrList_ces2 1 end]
         }
      }

      EnaBoGrpEncrType $swAddr1 $boGroup "all"
      EnaBoGrpEncrType $swAddr2 $boGroup "all"

      SetBoConnState $boName_ces1 $boGroup "disable" $swAddr1
      SetBoConnState $boName_ces2 $boGroup "disable" $swAddr2

      set ikeEncrList_ces2 $ikeEncrList

      foreach ikeEncr_ces1 $ikeEncrList {
         foreach ikeEncr_ces2 $ikeEncrList_ces2 {

            EnaBoGrpIkeEncrType $swAddr1 $boGroup $ikeEncr_ces1
            logFile "CESs: $swAddr1 - IPSEC IKE encryption type is set to \"$ikeEncr_ces1\""

            EnaBoGrpIkeEncrType $swAddr2 $boGroup $ikeEncr_ces2
            logFile "CESs: $swAddr2 - IPSEC IKE encryption type is set to \"$ikeEncr_ces2\""

            SetBoConnState $boName_ces1 $boGroup "enable" $swAddr1
            SetBoConnState $boName_ces2 $boGroup "enable" $swAddr2

            #aceWait 10000
            if {$ikeEncr_ces1==$ikeEncr_ces2 && [VerifyBoConnection] != "SUCCESS"} {
               incr err_count
            } elseif {$ikeEncr_ces1!=$ikeEncr_ces2 &&  [VerifyNegativeBoConnection "" 2] != "SUCCESS"} {
               incr err_count
            }

            SetBoConnState $boName_ces1 $boGroup "disable" $swAddr1
            SetBoConnState $boName_ces2 $boGroup "disable" $swAddr2
         }
         set ikeEncrList_ces2 [lrange $ikeEncrList_ces2 1 end]
      }

      if {$err_count==0} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete IPSEC ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete IPSEC ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2

      testEndLog $testName $error_code
   }


   proc T-111 {} {

      set error_code "FAIL"
      set testName "T-111"
      set err_count 0

      testStartLog $testName

      set purpose {Bouncing Tunnels L2TP}
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
      variable textPass

      set encrList_ces1 {rc4_128  rc4_40 none}
      set encrList_ces2 $encrList_ces1

      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static PPTP BOT / no encryption / no compression"
      ConfigL2TPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "p2p $ces1PublicIp $ces2PublicIp" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static PPTP BOT / no encryption / no compression"
      ConfigL2TPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "p2p $ces2PublicIp $ces1PublicIp" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"


      foreach state {enable disable} {

         SetBOCompression $swAddr1 $boName_ces1 $boGroup "l2tp" $state
         SetBOCompression $swAddr2 $boName_ces2 $boGroup "l2tp" $state

         foreach encr_ces1 $encrList_ces1 {
            foreach encr_ces2 $encrList_ces2 {

               SetBOEncryption $swAddr1 $boName_ces1 $boGroup "l2tp" $encr_ces1
               logFile "CESs: $swAddr1 - L2TP encryption type is set to \"$encr_ces1\""

               SetBOEncryption $swAddr2 $boName_ces2 $boGroup "l2tp" $encr_ces2
               logFile "CESs: $swAddr2 - L2TP encryption type is set to \"$encr_ces2\""

               SetBoConnState $boName_ces1 $boGroup "enable" $swAddr1
               SetBoConnState $boName_ces2 $boGroup "enable" $swAddr2

               #aceWait 10000
               if {$encr_ces1==$encr_ces2 && [VerifyBoConnection] != "SUCCESS"} {
                  incr err_count
               } elseif {$encr_ces1!=$encr_ces2 &&  [VerifyNegativeBoConnection "" 2] != "SUCCESS"} {
                  incr err_count
               }

               SetBoConnState $boName_ces1 $boGroup "disable" $swAddr1
               SetBoConnState $boName_ces2 $boGroup "disable" $swAddr2
            }
            set encrList_ces2 [lrange $encrList_ces2 1 end]
         }
      }

      if {$err_count==0} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete IPSEC ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete IPSEC ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2

      testEndLog $testName $error_code
   }


   proc T-112 {} {

      set error_code "FAIL"
      set testName "T-112"
      set err_count 0

      testStartLog $testName

      set purpose {Bouncing Tunnels PPTP }
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
      variable textPass

      set encrList_ces1 {rc4_128  rc4_40 none}
      set encrList_ces2 $encrList_ces1

      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static PPTP BOT / no encryption / no compression"
      ConfigPPTPBO $swAddr1 $boName_ces1 $boGroup "id1 id2 PptpPass" "p2p $ces1PublicIp $ces2PublicIp" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
#      SetBOCompression $swAddr1 $boName_ces1 $boGroup "pptp" "disable"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static PPTP BOT / no encryption / no compression"
      ConfigPPTPBO $swAddr2 $boName_ces2 $boGroup "id2 id1 PptpPass" "p2p $ces2PublicIp $ces1PublicIp" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"
#      SetBOCompression $swAddr2 $boName_ces2 $boGroup "pptp" "disable"

      foreach encr_ces1 $encrList_ces1 {
         foreach encr_ces2 $encrList_ces2 {

            SetBOEncryption $swAddr1 $boName_ces1 $boGroup "pptp" $encr_ces1
            logFile "CESs: $swAddr1 - PPTP encryption type is set to \"$encr_ces1\""

            SetBOEncryption $swAddr2 $boName_ces2 $boGroup "pptp" $encr_ces2
            logFile "CESs: $swAddr2 - PPTP encryption type is set to \"$encr_ces2\""

            SetBoConnState $boName_ces1 $boGroup "enable" $swAddr1
            SetBoConnState $boName_ces2 $boGroup "enable" $swAddr2

            #aceWait 10000
            if {$encr_ces1==$encr_ces2 && [VerifyBoConnection] != "SUCCESS"} {
               incr err_count
            } elseif {$encr_ces1!=$encr_ces2 &&  [VerifyNegativeBoConnection "" 2] != "SUCCESS"} {
               incr err_count
            }

            SetBoConnState $boName_ces1 $boGroup "disable" $swAddr1
            SetBoConnState $boName_ces2 $boGroup "disable" $swAddr2
         }
         set encrList_ces2 [lrange $encrList_ces2 1 end]
      }

      if {$err_count==0} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete IPSEC ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete IPSEC ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2

      testEndLog $testName $error_code
   }


   proc T-114 {} {

      set error_code "FAIL"
      set testName "T-114"
      set err_count 0

      testStartLog $testName

      set purpose {End/Close all sessions, including ping, to the remote network & remote CES}
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
      variable textPass

      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static IPSEC BOT "
      ConfigIpSecBO $swAddr1 $boName_ces1 $boGroup "text $textPass" "p2p $ces1PublicIp $ces2PublicIp" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static IPSEC BOT"
      ConfigIpSecBO $swAddr2 $boName_ces2 $boGroup "text $textPass" "p2p $ces2PublicIp $ces1PublicIp" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      if {[VerifyBoConnection "IPSEC"] != "SUCCESS"} {
         incr err_count
      } else {
         logFile "CES: $swAddr1 - BOT is forced off"
         BoForcedLogOff $swAddr1 $boName_ces1 $boGroup
         #BoForcedLogOff $swAddr1 all
         logFile "CES: $swAddr2 - BOT is forced off"
         #BoForcedLogOff $swAddr2 $boName_ces2 $boGroup
         BoForcedLogOff $swAddr2 all
         for {set i 1} { $i<=2} {incr i} {
            aceWait 5000
            if {[VerifyBoIsUp $boName_ces1 $swAddr1] != "NO"} {
               logFile "CES: $swAddr1 - BOT is up" "FAIL"
               incr err_count
               break
            } else {
               logFile "CES: $swAddr1 - BOT is not up" "PASS"
            }
            if {[VerifyBoIsUp $boName_ces2 $swAddr2] != "NO"} {
               logFile "CES: $swAddr2 - BOT is up" "FAIL"
               incr err_count
               break
            } else {
               logFile "CES: $swAddr2 - BOT is not up" "PASS"
            }
         }
      }

      if {$err_count == 0} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete IPSEC BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete IPSEC BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2

      testEndLog $testName $error_code
   }



   proc T-115 {} {

      set error_code "FAIL"
      set testName "T-115"
      set err_count 0

      testStartLog $testName

      set purpose {Verify you can enter multiple characters within the Connection configuration fields and get the correct error if mis-configured tunnel}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable swAddr2

      variable ces2PrivateIp
      variable ces2PublicIp

      variable ces1PublicIp

      variable boGroup
      variable boName_ces2
      variable textPass

      set textPass1 "1234567890123456789012345678901234567890"
      set hexPass1 "abcde"

      global cmdOut

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip IPSEC BOT"
      ConfigIpSecBO $swAddr2 $boName_ces2 $boGroup "text $textPass" "p2p $ces2PublicIp $ces1PublicIp" "rip"

      EnterBoConnLevel $boName_ces2 $boGroup $swAddr2

      Exec "ipsec authentication text-pre-shared-key $textPass1" "CES\\(config/bo_conn\\)\#" $swAddr2
       if {[regexp -nocase {Password cannot exceed 32 characters} $cmdOut] != 1} {
          incr err_count
      }

      Exec "ipsec authentication hex-pre-shared-key $hexPass1" "CES\\(config/bo_conn\\)\#" $swAddr2
      if {[regexp -nocase {Hex password must contain an even number of digits} $cmdOut] !=1} {
          incr err_count
      }
      if { $err_count == 0} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr2 - delete IPSEC BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      DisableRip $swAddr2

      testEndLog $testName $error_code

   }


   proc T-116 {} {

      set error_code "FAIL"
      set testName "T-116"
      set err_count 0

      testStartLog $testName

      set purpose {Verify if you enter reserved IPs, 255.0.0.0, 127.0.0.1, and anything higher then 240.0.0.0, that you will get a correct error message}
      set description {}
      testPurposeLog $purpose $description

      variable testedBuild
      bootBuild $testedBuild

      variable swAddr2

      variable ces2PrivateIp
      variable ces2PublicIp

      variable ces1PublicIp

      variable boGroup
      variable boName_ces2
      variable textPass

      set ipAddr1 "255.0.0.0"
      set ipAddr2 "127.0.0.1"
      set ipAddr3 "240.0.0.1"
      global cmdOut

      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip IPSEC BOT"
      ConfigIpSecBO $swAddr2 $boName_ces2 $boGroup "text $textPass" "p2p $ces2PublicIp $ces1PublicIp" "rip"

      EnterBoConnLevel $boName_ces2 $boGroup $swAddr2

      Exec "remote-endpoint $ipAddr1" "CES\\(config/bo_conn\\)\#" $swAddr2
      if {[regexp -nocase {Invalid remote IP address(.*)255.0.0.0 is reserved for multicast or future use} $cmdOut] != 1} {
         logFile "CES: $swAddr2 - set remote IP address: $ipAddr1 - didn't get an correct error message" "FAIL"
         incr err_count
      } else {
         logFile "CES: $swAddr2 - set remote IP address: $ipAddr1 - got an correct error message" "PASS"
      }

      Exec "remote-endpoint $ipAddr2" "CES\\(config/bo_conn\\)\#" $swAddr2
      if {[regexp -nocase {Invalid remote IP address(.*)127.0.0.1 is reserved for loopback} $cmdOut] != 1} {
         logFile "CES: $swAddr2 - set remote IP address: $ipAddr2 - didn't get an correct error message" "FAIL"
         incr err_count
      } else {
         logFile "CES: $swAddr2 - set remote IP address: $ipAddr2 - got an correct error message" "PASS"
      }

      Exec "remote-endpoint $ipAddr3" "CES\\(config/bo_conn\\)\#" $swAddr2
      if {[regexp -nocase {Invalid remote IP address(.*)240.0.0.1 is reserved for multicast or future use} $cmdOut] != 1} {
         logFile "CES: $swAddr2 - set remote IP address: $ipAddr3 - didn't get an correct error message" "FAIL"
         incr err_count
      } else {
         logFile "CES: $swAddr2 - set remote IP address: $ipAddr3 - got an correct error message" "PASS"
      }

      if { $err_count == 0} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr2 - delete IPSEC BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      DisableRip $swAddr2

      testEndLog $testName $error_code
   }


   proc T-121 {} {

      set error_code "FAIL"
      set testName "T-121"
      set err_count 0

      testStartLog $testName

      set purpose {Verify configuring a Dynamic Peer to Peer IPSec Branch Office Tunnel with OSPF enabled and RIP enabled}
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
      variable textPass

      EnableOspf $swAddr1
      SetOspfNetwork $swAddr1 0.0.0.0 $ces1PrivateIp 0.0.0.255
      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1

      logFile "CES: $swAddr1 - add dynamic rip IPSEC BOT"
      ConfigIpSecBO $swAddr1 $boName_ces1 $boGroup "text $textPass" "p2p $ces1PublicIp $ces2PublicIp" "ospf 0.0.0.0"
#      ConfigIpSecBO $swAddr1 $boName_ces1 $boGroup "text $textPass" "p2p $ces1PublicIp $ces2PublicIp" "rip"
      EnterBoConnLevel $boName_ces1 $boGroup $swAddr1
      Exec "routing rip enable" "CES\\(config/bo_conn\\)\#" $swAddr1
      Exec "exit" "CONFIG" $swAddr1

      EnableOspf $swAddr2
      SetOspfNetwork $swAddr2 0.0.0.0 $ces2PrivateIp 0.0.0.255
      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2

      logFile "CES: $swAddr2 - add dynamic rip IPSEC BOT"
      ConfigIpSecBO $swAddr2 $boName_ces2 $boGroup "text $textPass" "p2p $ces2PublicIp $ces1PublicIp" "ospf 0.0.0.0"
#      ConfigIpSecBO $swAddr2 $boName_ces2 $boGroup "text $textPass" "p2p $ces2PublicIp $ces1PublicIp" "rip"
      EnterBoConnLevel $boName_ces2 $boGroup $swAddr2
      Exec "routing rip enable" "CES\\(config/bo_conn\\)\#" $swAddr2
      Exec "exit" "CONFIG" $swAddr2

      if {[VerifyBoConnection "IPSEC"] != "SUCCESS"} {
         incr err_count
      }

      if {[GetIpRouteNextHop $swAddr1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 "OSPF"] != "$ces2PublicIp"} {
         logFile "CES: $swAddr1 - OSPF route  does't appear in routing table" "FAIL"
         incr err_count
      } else {
         logFile "CES: $swAddr1 - OSPF route appear in routing table" "PASS"
      }

      if {[GetIpRouteNextHop $swAddr1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 "RIP"] != "$ces2PublicIp"} {
         logFile "CES: $swAddr1 - RIP route  does't appear in routing table" "FAIL"
         incr err_count
      } else {
         logFile "CES: $swAddr1 - RIP route appear in routing table" "PASS"
      }

      if {[GetIpRouteNextHop $swAddr2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 "OSPF"] != "$ces1PublicIp"} {
         logFile "CES: $swAddr2 - OSPF route  does't appear in routing table" "FAIL"
         incr err_count
      } else {
         logFile "CES: $swAddr2 - OSPF route appear in routing table" "PASS"
      }

      if {[GetIpRouteNextHop $swAddr2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 "RIP"] != "$ces1PublicIp"} {
         logFile "CES: $swAddr2 - RIP route  does't appear in routing table" "FAIL"
         incr err_count
      } else {
         logFile "CES: $swAddr2 - RIP route appear in routing table" "PASS"
      }

      if  {$err_count == 0} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete IPSEC BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      DisableRip $swAddr1
      DelOspfNetwork $swAddr1 0.0.0.0 $ces1PrivateIp 0.0.0.255
      DisableOspf $swAddr1

      logFile "CES: $swAddr2 - delete IPSEC BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      DisableRip $swAddr2
      DelOspfNetwork $swAddr2 0.0.0.0 $ces2PrivateIp 0.0.0.255
      DisableOspf $swAddr2

      testEndLog $testName $error_code
   }



#######################################
#
# Test with Calvin and the latest build
#
#######################################



   proc T-129 {} {

      set error_code "FAIL"
      set testName "T-129"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic, Peer to Peer IPSec Branch Office tunnel with Text Preshared key and permit all filter, between Calvin and Coolidge builds (V04_70.xxx and the latest software) Enable IKE Encryption and Diffie-Hellman Group 5 AES encryption with encryption ESP128SHA1 enabled}
      set description {}
      testPurposeLog $purpose $description

      variable swAddr1
      variable swAddr2

      variable calvinBuild
      if {$calvinBuild == "none"} {
         logFile "The Calvin build doesn't exist in CES ($swAddr2)"
         testEndLog $testName "ABORT"
         return
      }

      bootBuild $calvinBuild


      variable ces1PrivateIp
      variable ces1PublicIp

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2
      variable textPass

      DisBoGrpEncrType $swAddr1 $boGroup "all"
      EnaBoGrpEncrType $swAddr1 $boGroup "aes128-sha1"
      EnaBoGrpIkeEncrType $swAddr1 $boGroup "128aes-group5"
      EnaAggressiveMode $swAddr1 $boGroup

      DisBoGrpEncrType $swAddr2 $boGroup "all"
      EnaBoGrpEncrType $swAddr2 $boGroup "aes128-sha1"
      EnaBoGrpIkeEncrType $swAddr2 $boGroup "128aes-group5"
      EnaAggressiveMode $swAddr2 $boGroup

      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      logFile "CES: $swAddr1 - add dynamic rip IPSEC BOT"
      ConfigIpSecBO $swAddr1 $boName_ces1 $boGroup "text $textPass" "p2p $ces1PublicIp $ces2PublicIp" "rip"

#      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip IPSEC BOT"
      ConfigIpSecBO $swAddr2 $boName_ces2 $boGroup "text $textPass" "p2p $ces2PublicIp $ces1PublicIp" "rip"

      if {[VerifyBoConnection "IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete IPSEC BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      EnaBoGrpEncrType $swAddr1 $boGroup "all"
      DisAggressiveMode $swAddr1 $boGroup
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete IPSEC BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      EnaBoGrpEncrType $swAddr2 $boGroup "all"
      DisAggressiveMode $swAddr2 $boGroup
#      DisableRip $swAddr2

      testEndLog $testName $error_code
   }


   proc T-130 {} {

      set error_code "FAIL"
      set testName "T-130"

      testStartLog $testName

      set purpose {Verify you can create a Static Peer to Peer IPSec Branch Office tunnel with Text Preshared key and permit all filter, between Calvin(V04_70.xxx) and the latest build.Enable IKE Encryption and Diffie Hellman Group 5 AES, and ESP Triple DES with MD5 integrity. Agressive mode enabled}
      set description {}
      testPurposeLog $purpose $description

      variable swAddr1
      variable swAddr2

      variable calvinBuild
      if {$calvinBuild == "none"} {
         logFile "The Calvin build doesn't exist in CES ($swAddr1)"
         testEndLog $testName "ABORT"
         return
      }
      bootBuild $calvinBuild

      variable ces1PrivateIp
      variable ces1PublicIp

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2
      variable textPass

      DisBoGrpEncrType $swAddr1 $boGroup "all"
      EnaBoGrpEncrType $swAddr1 $boGroup "3des-md5"
      EnaBoGrpIkeEncrType $swAddr1 $boGroup "128aes-group5"
      EnaAggressiveMode $swAddr1 $boGroup

      DisBoGrpEncrType $swAddr2 $boGroup "all"
      EnaBoGrpEncrType $swAddr2 $boGroup "3des-md5"
      EnaBoGrpIkeEncrType $swAddr2 $boGroup "128aes-group5"
      EnaAggressiveMode $swAddr2 $boGroup


      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static IPSEC BOT "
      ConfigIpSecBO $swAddr1 $boName_ces1 $boGroup "text $textPass" "p2p $ces1PublicIp $ces2PublicIp" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static IPSEC BOT"
      ConfigIpSecBO $swAddr2 $boName_ces2 $boGroup "text $textPass" "p2p $ces2PublicIp $ces1PublicIp" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      if {[VerifyBoConnection "IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete IPSEC BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelNetwork "local_nets_1" $swAddr1
      EnaBoGrpEncrType $swAddr1 $boGroup "all"
      DisAggressiveMode $swAddr1 $boGroup

      logFile "CES: $swAddr2 - delete IPSEC BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelNetwork "local_nets_2" $swAddr2
      EnaBoGrpEncrType $swAddr2 $boGroup "all"
      DisAggressiveMode $swAddr2 $boGroup

      testEndLog $testName $error_code
   }


   proc T-131 {} {

      set error_code "FAIL"
      set testName "T-131"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic, ABOT IPSec Branch Office tunnel with Text Preshared key and permit all filter, between Calvin and Coolidge builds (V04_70.xxx and the latest build). Enable IKE encryption and Diffie-Hellman Group 5 AES encryption, with encryption ESP 128SHA1integrity. Agressive mode disabled.}
      set description {}
      testPurposeLog $purpose $description

      variable swAddr1
      variable swAddr2

      variable calvinBuild
      if {$calvinBuild == "none"} {
         logFile "The Calvin build doesn't exist in CES ($swAddr1)"
         testEndLog $testName "ABORT"
         return
      }
      bootBuild $calvinBuild

      variable ces1PrivateIp
#      variable ces1PublicSlot

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2
      variable textPass
      variable initiator_uid

      DisBoGrpEncrType $swAddr1 $boGroup "all"
      EnaBoGrpEncrType $swAddr1 $boGroup "aes128-sha1"
      EnaBoGrpIkeEncrType $swAddr1 $boGroup "128aes-group5"
      DisAggressiveMode $swAddr1 $boGroup

      DisBoGrpEncrType $swAddr2 $boGroup "all"
      EnaBoGrpEncrType $swAddr2 $boGroup "aes128-sha1"
      EnaBoGrpIkeEncrType $swAddr2 $boGroup "128aes-group5"
      DisAggressiveMode $swAddr2 $boGroup

      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      logFile "CES: $swAddr1 - add dynamic rip IPSEC ABOT / initiator / text pre-shared key"
      ConfigIpSecBO $swAddr1 $boName_ces1 $boGroup "text $textPass $initiator_uid" "initiator $ces2PublicIp" "rip"

#      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip IPSEC ABOT / responder / text pre-shared key"
      ConfigIpSecBO $swAddr2 $boName_ces2 $boGroup "text $textPass $initiator_uid" "responder" "rip"

      if {[VerifyBoConnection "IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete IPSEC ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      EnaBoGrpEncrType $swAddr1 $boGroup "all"
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete IPSEC ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      EnaBoGrpEncrType $swAddr2 $boGroup "all"
#      DisableRip $swAddr2

      testEndLog $testName $error_code
   }


   proc T-132 {} {

      set error_code "FAIL"
      set testName "T-132"

      testStartLog $testName

      set purpose {Verify you can create a Dynamic, ABOT IPSec Branch Office tunnel with Text Preshared key and permit all filter, between Calvin and Coolidge builds (V04_70.xxx and the latest build) Enable IKE Encryption and Diffie-Hellman Group 5 AES encryption with encryption ESP128SHA1 enabled. Aggressive mode enabled.}
      set description {}
      testPurposeLog $purpose $description

      variable swAddr1
      variable swAddr2

      variable calvinBuild
      if {$calvinBuild == "none"} {
         logFile "The Calvin build doesn't exist in CES ($swAddr1)"
         testEndLog $testName "ABORT"
         return
      }
      bootBuild $calvinBuild

      variable ces1PrivateIp

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2
      variable textPass
      variable initiator_uid

      DisBoGrpEncrType $swAddr1 $boGroup "all"
      EnaBoGrpEncrType $swAddr1 $boGroup "aes128-sha1"
      EnaBoGrpIkeEncrType $swAddr1 $boGroup "128aes-group5"
      EnaAggressiveMode $swAddr1 $boGroup

      DisBoGrpEncrType $swAddr2 $boGroup "all"
      EnaBoGrpEncrType $swAddr2 $boGroup "aes128-sha1"
      EnaBoGrpIkeEncrType $swAddr2 $boGroup "128aes-group5"
      EnaAggressiveMode $swAddr2 $boGroup

      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      logFile "CES: $swAddr1 - add dynamic rip IPSEC ABOT / initiator / text pre-shared key"
      ConfigIpSecBO $swAddr1 $boName_ces1 $boGroup "text $textPass $initiator_uid" "initiator $ces2PublicIp" "rip"

#      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip IPSEC ABOT / responder / text pre-shared key"
      ConfigIpSecBO $swAddr2 $boName_ces2 $boGroup "text $textPass $initiator_uid" "responder" "rip"

      if {[VerifyBoConnection "IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete IPSEC ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      EnaBoGrpEncrType $swAddr1 $boGroup "all"
      DisAggressiveMode $swAddr1 $boGroup
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete IPSEC ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      EnaBoGrpEncrType $swAddr2 $boGroup "all"
      DisAggressiveMode $swAddr2 $boGroup
#      DisableRip $swAddr2

      testEndLog $testName $error_code
   }


   proc T-133 {} {

      set error_code "FAIL"
      set testName "T-133"

      testStartLog $testName

      set purpose {Verify you can create a Static  ABOT IPSec Branch Office tunnel with Text Preshared key and permit all filter, between Calvin (V04_70.xxx) and the latest build. IKE encryption and Diffie-Hellman Group 5 AES with encryption ESP AES- 128SHA1 integrity enabled. Agressive mode disabled.}
      set description {}
      testPurposeLog $purpose $description

      variable swAddr1
      variable swAddr2

      variable calvinBuild
      if {$calvinBuild == "none"} {
         logFile "The Calvin build doesn't exist in CES ($swAddr1)"
         testEndLog $testName "ABORT"
         return
      }
      bootBuild $calvinBuild

      variable ces1PrivateIp

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2
      variable textPass
      variable initiator_uid

      DisBoGrpEncrType $swAddr1 $boGroup "all"
      EnaBoGrpEncrType $swAddr1 $boGroup "aes128-sha1"
      EnaBoGrpIkeEncrType $swAddr1 $boGroup "128aes-group5"
      DisAggressiveMode $swAddr1 $boGroup

      DisBoGrpEncrType $swAddr2 $boGroup "all"
      EnaBoGrpEncrType $swAddr2 $boGroup "aes128-sha1"
      EnaBoGrpIkeEncrType $swAddr2 $boGroup "128aes-group5"
      DisAggressiveMode $swAddr2 $boGroup

      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static IPSEC ABOT / initiator / text pre-shared key"
      ConfigIpSecBO $swAddr1 $boName_ces1 $boGroup "text $textPass $initiator_uid" "initiator $ces2PublicIp" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static IPSEC ABOT / responder / text pre-shared key"
      ConfigIpSecBO $swAddr2 $boName_ces2 $boGroup "text $textPass $initiator_uid" "responder" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      if {[VerifyBoConnection "IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete IPSEC ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      EnaBoGrpEncrType $swAddr1 $boGroup "all"
      DelNetwork "local_nets_1" $swAddr1

      logFile "CES: $swAddr2 - delete IPSEC ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      EnaBoGrpEncrType $swAddr2 $boGroup "all"
      DelNetwork "local_nets_2" $swAddr2

      testEndLog $testName $error_code
   }


   proc T-134 {} {

      set error_code "FAIL"
      set testName "T-134"

      testStartLog $testName

      set purpose {Verify you can create a Static  ABOT IPSec Branch Office tunnel with Text Preshared key and permit all filter, between Calvin and the latest build. Enable IKE encryption and Diffie-Hellman Group 5 AES with ESP AES 128 with SHA1 integrity. Aggressive mode enabled.}
      set description {}
      testPurposeLog $purpose $description

      variable swAddr1
      variable swAddr2

      variable calvinBuild
      if {$calvinBuild == "none"} {
         logFile "The Calvin build doesn't exist in CES ($swAddr1)"
         testEndLog $testName "ABORT"
         return
      }
      bootBuild $calvinBuild

      variable ces1PrivateIp

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2
      variable textPass
      variable initiator_uid

      DisBoGrpEncrType $swAddr1 $boGroup "all"
      EnaBoGrpEncrType $swAddr1 $boGroup "aes128-sha1"
      EnaBoGrpIkeEncrType $swAddr1 $boGroup "128aes-group5"
      EnaAggressiveMode $swAddr1 $boGroup

      DisBoGrpEncrType $swAddr2 $boGroup "all"
      EnaBoGrpEncrType $swAddr2 $boGroup "aes128-sha1"
      EnaBoGrpIkeEncrType $swAddr2 $boGroup "128aes-group5"
      EnaAggressiveMode $swAddr2 $boGroup

      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static IPSEC ABOT / initiator / text pre-shared key"
      ConfigIpSecBO $swAddr1 $boName_ces1 $boGroup "text $textPass $initiator_uid" "initiator $ces2PublicIp" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static IPSEC ABOT / responder / text pre-shared key"
      ConfigIpSecBO $swAddr2 $boName_ces2 $boGroup "text $textPass $initiator_uid" "responder" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      if {[VerifyBoConnection "IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete IPSEC ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      EnaBoGrpEncrType $swAddr1 $boGroup "all"
      DelNetwork "local_nets_1" $swAddr1
      DisAggressiveMode $swAddr1 $boGroup

      logFile "CES: $swAddr2 - delete IPSEC ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      EnaBoGrpEncrType $swAddr2 $boGroup "all"
      DelNetwork "local_nets_2" $swAddr2
      DisAggressiveMode $swAddr2 $boGroup

      testEndLog $testName $error_code
   }


   proc T-136 {} {

      set error_code "FAIL"
      set testName "T-136"

      testStartLog $testName

      set purpose {Verify you can create a Static ABOT IPSec Branch Office tunnel with Text Preshared key and permit all filter, between Calvin(V04_70.xxx) and the latest build. Enable IKE Encryption and Diffie Hellman Group 5 AES, and ESP Triple DES with MD5 integrity. Agressive mode enabled.}
      set description {}
      testPurposeLog $purpose $description

      variable swAddr1
      variable swAddr2

      variable calvinBuild
      if {$calvinBuild == "none"} {
         logFile "The Calvin build doesn't exist in CES ($swAddr1)"
         testEndLog $testName "ABORT"
         return
      }
      bootBuild $calvinBuild

      variable ces1PrivateIp

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2
      variable textPass
      variable initiator_uid

      DisBoGrpEncrType $swAddr1 $boGroup "all"
      EnaBoGrpEncrType $swAddr1 $boGroup "3des-md5"
      EnaBoGrpIkeEncrType $swAddr1 $boGroup "128aes-group5"
      EnaAggressiveMode $swAddr1 $boGroup

      DisBoGrpEncrType $swAddr2 $boGroup "all"
      EnaBoGrpEncrType  $swAddr2 $boGroup "3des-md5"
      EnaBoGrpIkeEncrType $swAddr2 $boGroup "128aes-group5"
      EnaAggressiveMode $swAddr2 $boGroup

      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static IPSEC ABOT / initiator / text pre-shared key"
      ConfigIpSecBO $swAddr1 $boName_ces1 $boGroup "text $textPass $initiator_uid" "initiator $ces2PublicIp" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static IPSEC ABOT / responder / text pre-shared key"
      ConfigIpSecBO $swAddr2 $boName_ces2 $boGroup "text $textPass $initiator_uid" "responder" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      if {[VerifyBoConnection "IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete IPSEC ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      EnaBoGrpEncrType $swAddr1 $boGroup "all"
      DelNetwork "local_nets_1" $swAddr1
      DisAggressiveMode $swAddr1 $boGroup

      logFile "CES: $swAddr2 - delete IPSEC ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      EnaBoGrpEncrType $swAddr2 $boGroup "all"
      DelNetwork "local_nets_2" $swAddr2
      DisAggressiveMode $swAddr2 $boGroup

      testEndLog $testName $error_code
   }


   proc T-137 {} {

      set error_code "FAIL"
      set testName "T-137"

      testStartLog $testName

      set purpose {Verify you can create a Static ABOT IPSec Branch Office tunnel with Text Preshared key and permit all filter, between Calvin (V04_70.xxx) and the latest build. Enable IKE Encryption and Diffie Hellman Group 5 AES, and ESP- 56bit DES with SHA1 integrity. Aggressive mode enabled.}
      set description {}
      testPurposeLog $purpose $description

      variable swAddr1
      variable swAddr2

      variable calvinBuild
      if {$calvinBuild == "none"} {
         logFile "The Calvin build doesn't exist in CES ($swAddr1)"
         testEndLog $testName "ABORT"
         return
      }
      bootBuild $calvinBuild

      variable ces1PrivateIp

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2
      variable textPass
      variable initiator_uid

      DisBoGrpEncrType $swAddr1 $boGroup "all"
      EnaBoGrpEncrType  $swAddr1 $boGroup "des56-sha1"
      EnaBoGrpIkeEncrType $swAddr1 $boGroup "128aes-group5"
      EnaAggressiveMode $swAddr1 $boGroup

      DisBoGrpEncrType $swAddr2 $boGroup "all"
      EnaBoGrpEncrType $swAddr2 $boGroup "des56-sha1"
      EnaBoGrpIkeEncrType $swAddr2 $boGroup "128aes-group5"
      EnaAggressiveMode $swAddr2 $boGroup

      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static IPSEC ABOT / initiator / text pre-shared key"
      ConfigIpSecBO $swAddr1 $boName_ces1 $boGroup "text $textPass $initiator_uid" "initiator $ces2PublicIp" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static IPSEC ABOT / responder / text pre-shared key"
      ConfigIpSecBO $swAddr2 $boName_ces2 $boGroup "text $textPass $initiator_uid" "responder" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      if {[VerifyBoConnection "IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete IPSEC ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      EnaBoGrpEncrType $swAddr1 $boGroup "all"
      DelNetwork "local_nets_1" $swAddr1
      DisAggressiveMode $swAddr1 $boGroup

      logFile "CES: $swAddr2 - delete IPSEC ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      EnaBoGrpEncrType $swAddr2 $boGroup "all"
      DelNetwork "local_nets_2" $swAddr2
      DisAggressiveMode $swAddr2 $boGroup

      testEndLog $testName $error_code
   }


   proc T-138 {} {

      set error_code "FAIL"
      set testName "T-138"

      testStartLog $testName

      set purpose {Verify you can create a Static ABOT IPSec Branch Office tunnel with Text Preshared key and permit all filter, between Calvin and Coolidge builds (V04_70.119 and the latest build). Enable IKE Encryption and Diffie Hellman Group 5 AES, and ESP- 56 bit DES with MD5 integrity. Agressive mode enabled.}
      set description {}
      testPurposeLog $purpose $description

      variable swAddr1
      variable swAddr2

      variable calvinBuild
      if {$calvinBuild == "none"} {
         logFile "The Calvin build doesn't exist in CES ($swAddr1)"
         testEndLog $testName "ABORT"
         return
      }
      bootBuild $calvinBuild

      variable ces1PrivateIp

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2
      variable textPass
      variable initiator_uid

      DisBoGrpEncrType $swAddr1 $boGroup "all"
      EnaBoGrpEncrType $swAddr1 $boGroup "des56-md5"
      EnaBoGrpIkeEncrType $swAddr1 $boGroup "128aes-group5"
      EnaAggressiveMode $swAddr1 $boGroup

      DisBoGrpEncrType $swAddr2 $boGroup "all"
      EnaBoGrpEncrType $swAddr2 $boGroup "des56-md5"
      EnaBoGrpIkeEncrType $swAddr2 $boGroup "128aes-group5"
      EnaAggressiveMode $swAddr2 $boGroup

      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static IPSEC ABOT / initiator / text pre-shared key"
      ConfigIpSecBO $swAddr1 $boName_ces1 $boGroup "text $textPass $initiator_uid" "initiator $ces2PublicIp" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static IPSEC ABOT / responder / text pre-shared key"
      ConfigIpSecBO $swAddr2 $boName_ces2 $boGroup "text $textPass $initiator_uid" "responder" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      if {[VerifyBoConnection "IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete IPSEC ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      EnaBoGrpEncrType $swAddr1 $boGroup "all"
      DelNetwork "local_nets_1" $swAddr1
      DisAggressiveMode $swAddr1 $boGroup

      logFile "CES: $swAddr2 - delete IPSEC ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      EnaBoGrpEncrType $swAddr2 $boGroup "all"
      DelNetwork "local_nets_2" $swAddr2
      DisAggressiveMode $swAddr2 $boGroup

      testEndLog $testName $error_code
   }


   proc T-139 {} {

      set error_code "FAIL"
      set testName "T-139"

      testStartLog $testName

      set purpose {Verify you can create a Static ABOT IPSec Branch Office tunnel with Text Preshared key and permit all filter, between Calvin and Coolidge builds (V04_70.119 and the latest build). Enable IKE Encryption and Diffie Hellman Group 5 AES, and ESP 40 bit DES with SHA1 integrity. Agressive mode enabled.}
      set description {}
      testPurposeLog $purpose $description

      variable swAddr1
      variable swAddr2

      variable calvinBuild
      if {$calvinBuild == "none"} {
         logFile "The Calvin build doesn't exist in CES ($swAddr1)"
         testEndLog $testName "ABORT"
         return
      }
      bootBuild $calvinBuild

      variable ces1PrivateIp

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2
      variable textPass
      variable initiator_uid

      DisBoGrpEncrType $swAddr1 $boGroup "all"
      EnaBoGrpEncrType $swAddr1 $boGroup "des40-sha1"
      EnaBoGrpIkeEncrType $swAddr1 $boGroup "128aes-group5"
      EnaAggressiveMode $swAddr1 $boGroup

      DisBoGrpEncrType $swAddr2 $boGroup "all"
      EnaBoGrpEncrType $swAddr2 $boGroup "des40-sha1"
      EnaBoGrpIkeEncrType $swAddr2 $boGroup "128aes-group5"
      EnaAggressiveMode $swAddr2 $boGroup

      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static IPSEC ABOT / initiator / text pre-shared key "
      ConfigIpSecBO $swAddr1 $boName_ces1 $boGroup "text $textPass $initiator_uid" "initiator $ces2PublicIp" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static IPSEC ABOT / responder / text pre-shared key"
      ConfigIpSecBO $swAddr2 $boName_ces2 $boGroup "text $textPass $initiator_uid" "responder" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      if {[VerifyBoConnection "IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete IPSEC ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      EnaBoGrpEncrType $swAddr1 $boGroup "all"
      DelNetwork "local_nets_1" $swAddr1
      DisAggressiveMode $swAddr1 $boGroup

      logFile "CES: $swAddr2 - delete IPSEC ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      EnaBoGrpEncrType $swAddr2 $boGroup "all"
      DelNetwork "local_nets_2" $swAddr2
      DisAggressiveMode $swAddr2 $boGroup

      testEndLog $testName $error_code
   }


   proc T-140 {} {

      set error_code "FAIL"
      set testName "T-140"

      testStartLog $testName

      set purpose {Verify you can create a Static ABOT IPSec Branch Office tunnel with Text Preshared key and permit all filter, between Calvin (V04_70.xxx) and the latest build. Enable IKE Encryption and Diffie Hellman Group 5 AES, and ESP 40 bit DES with MD5 integrity. Aggressive mode enabled.}
      set description {}
      testPurposeLog $purpose $description

      variable swAddr1
      variable swAddr2

      variable calvinBuild
      if {$calvinBuild == "none"} {
         logFile "The Calvin build doesn't exist in CES ($swAddr1)"
         testEndLog $testName "ABORT"
         return
      }
      bootBuild $calvinBuild

      variable ces1PrivateIp

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2
      variable textPass
      variable initiator_uid

      DisBoGrpEncrType $swAddr1 $boGroup "all"
      EnaBoGrpEncrType $swAddr1 $boGroup "des40-md5"
      EnaBoGrpIkeEncrType $swAddr1 $boGroup "128aes-group5"
      EnaAggressiveMode $swAddr1 $boGroup

      DisBoGrpEncrType $swAddr2 $boGroup "all"
      EnaBoGrpEncrType $swAddr2 $boGroup "des40-md5"
      EnaBoGrpIkeEncrType $swAddr2 $boGroup "128aes-group5"
      EnaAggressiveMode $swAddr2 $boGroup

      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static IPSEC ABOT / initiator / text pre-shared key "
      ConfigIpSecBO $swAddr1 $boName_ces1 $boGroup "text $textPass $initiator_uid" "initiator $ces2PublicIp" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static IPSEC ABOT / responder / text pre-shared key"
      ConfigIpSecBO $swAddr2 $boName_ces2 $boGroup "text $textPass $initiator_uid" "responder" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      if {[VerifyBoConnection "IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete IPSEC ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      EnaBoGrpEncrType $swAddr1 $boGroup "all"
      DelNetwork "local_nets_1" $swAddr1
      DisAggressiveMode $swAddr1 $boGroup

      logFile "CES: $swAddr2 - delete IPSEC ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      EnaBoGrpEncrType $swAddr2 $boGroup "all"
      DelNetwork "local_nets_2" $swAddr2
      DisAggressiveMode $swAddr2 $boGroup

      testEndLog $testName $error_code
   }


   proc T-141 {} {

      set error_code "FAIL"
      set testName "T-141"

      testStartLog $testName

      set purpose {Verify you can create a Static ABOT IPSec Branch Office tunnel with Text Preshared key and permit all filter, between Calvin (V04_70.xxx) and the latest build. Enable IKE Encryption and Diffie Hellman Group 5 AES, and ESP NULL (Authentication only) with SHA1 integrity. Agressive mode enabled.}
      set description {}
      testPurposeLog $purpose $description

      variable swAddr1
      variable swAddr2

      variable calvinBuild
      if {$calvinBuild == "none"} {
         logFile "The Calvin build doesn't exist in CES ($swAddr1)"
         testEndLog $testName "ABORT"
         return
      }
      bootBuild $calvinBuild

      variable ces1PrivateIp

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2
      variable textPass
      variable initiator_uid

      DisBoGrpEncrType $swAddr1 $boGroup "all"
      EnaBoGrpEncrType $swAddr1 $boGroup "sha1"
      EnaBoGrpIkeEncrType $swAddr1 $boGroup "128aes-group5"
      EnaAggressiveMode $swAddr1 $boGroup

      DisBoGrpEncrType $swAddr2 $boGroup "all"
      EnaBoGrpEncrType $swAddr2 $boGroup "sha1"
      EnaBoGrpIkeEncrType $swAddr2 $boGroup "128aes-group5"
      EnaAggressiveMode $swAddr2 $boGroup

      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static IPSEC ABOT / initiator / text pre-shared key "
      ConfigIpSecBO $swAddr1 $boName_ces1 $boGroup "text $textPass $initiator_uid" "initiator $ces2PublicIp" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static IPSEC ABOT / responder / text pre-shared key"
      ConfigIpSecBO $swAddr2 $boName_ces2 $boGroup "text $textPass $initiator_uid" "responder" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      if {[VerifyBoConnection "IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete IPSEC ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      EnaBoGrpEncrType $swAddr1 $boGroup "all"
      DelNetwork "local_nets_1" $swAddr1
      DisAggressiveMode $swAddr1 $boGroup

      logFile "CES: $swAddr2 - delete IPSEC ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      EnaBoGrpEncrType $swAddr2 $boGroup "all"
      DelNetwork "local_nets_2" $swAddr2
      DisAggressiveMode $swAddr2 $boGroup

      testEndLog $testName $error_code
   }


   proc T-142 {} {

      set error_code "FAIL"
      set testName "T-142"

      testStartLog $testName

      set purpose {Verify you can create a Static ABOT IPSec Branch Office tunnel with Text Preshared key and permit all filter, between Calvin(V04_70.xxx) and the latest build. Enable IKE Encryption and Diffie Hellman Group 5 AES, and ESP NULL (Authentication only) with MD5 integrity. Aggressive mode enabled.}
      set description {}
      testPurposeLog $purpose $description

      variable swAddr1
      variable swAddr2

      variable calvinBuild
      if {$calvinBuild == "none"} {
         logFile "The Calvin build doesn't exist in CES ($swAddr1)"
         testEndLog $testName "ABORT"
         return
      }
      bootBuild $calvinBuild

      variable ces1PrivateIp

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2
      variable textPass
      variable initiator_uid

      DisBoGrpEncrType $swAddr1 $boGroup "all"
      EnaBoGrpEncrType $swAddr1 $boGroup "md5"
      EnaBoGrpIkeEncrType $swAddr1 $boGroup "128aes-group5"
      EnaAggressiveMode $swAddr1 $boGroup

      DisBoGrpEncrType $swAddr2 $boGroup "all"
      EnaBoGrpEncrType $swAddr2 $boGroup "md5"
      EnaBoGrpIkeEncrType $swAddr2 $boGroup "128aes-group5"
      EnaAggressiveMode $swAddr2 $boGroup

      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static IPSEC ABOT / initiator / text pre-shared key "
      ConfigIpSecBO $swAddr1 $boName_ces1 $boGroup "text $textPass $initiator_uid" "initiator $ces2PublicIp" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static IPSEC ABOT / responder / text pre-shared key"
      ConfigIpSecBO $swAddr2 $boName_ces2 $boGroup "text $textPass $initiator_uid" "responder" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      if {[VerifyBoConnection "IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete IPSEC ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      EnaBoGrpEncrType $swAddr1 $boGroup "all"
      DelNetwork "local_nets_1" $swAddr1
      DisAggressiveMode $swAddr1 $boGroup

      logFile "CES: $swAddr2 - delete IPSEC ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      EnaBoGrpEncrType $swAddr2 $boGroup "all"
      DelNetwork "local_nets_2" $swAddr2
      DisAggressiveMode $swAddr2 $boGroup

      testEndLog $testName $error_code
   }


   proc T-143 {} {

      set error_code "FAIL"
      set testName "T-143"

      testStartLog $testName

      set purpose {Verify you can create a Static ABOT IPSec Branch Office tunnel with Text Preshared key and permit all filter, between Calvin and the latest build. Enable IKE Encryption and Diffie Hellman Group 5 AES, and AH Authentication only (HMAC-SHA1) Agressive mode enabled.}
      set description {}
      testPurposeLog $purpose $description

      variable swAddr1
      variable swAddr2

      variable calvinBuild
      if {$calvinBuild == "none"} {
         logFile "The Calvin build doesn't exist in CES ($swAddr1)"
         testEndLog $testName "ABORT"
         return
      }
      bootBuild $calvinBuild

      variable ces1PrivateIp

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2
      variable textPass
      variable initiator_uid

      DisBoGrpEncrType $swAddr1 $boGroup "all"
      EnaBoGrpEncrType $swAddr1 $boGroup "hmac-sha1"
      EnaBoGrpIkeEncrType $swAddr1 $boGroup "128aes-group5"
      EnaAggressiveMode $swAddr1 $boGroup

      DisBoGrpEncrType $swAddr2 $boGroup "all"
      EnaBoGrpEncrType $swAddr2 $boGroup "hmac-sha1"
      EnaBoGrpIkeEncrType $swAddr2 $boGroup "128aes-group5"
      EnaAggressiveMode $swAddr2 $boGroup

      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static IPSEC ABOT / initiator / text pre-shared key "
      ConfigIpSecBO $swAddr1 $boName_ces1 $boGroup "text $textPass $initiator_uid" "initiator $ces2PublicIp" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static IPSEC ABOT / responder / text pre-shared key"
      ConfigIpSecBO $swAddr2 $boName_ces2 $boGroup "text $textPass $initiator_uid" "responder" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      if {[VerifyBoConnection "IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete IPSEC ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      EnaBoGrpEncrType $swAddr1 $boGroup "all"
      DelNetwork "local_nets_1" $swAddr1
      DisAggressiveMode $swAddr1 $boGroup

      logFile "CES: $swAddr2 - delete IPSEC ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      EnaBoGrpEncrType $swAddr2 $boGroup "all"
      DelNetwork "local_nets_2" $swAddr2
      DisAggressiveMode $swAddr2 $boGroup

      testEndLog $testName $error_code
   }


   proc T-144 {} {

      set error_code "FAIL"
      set testName "T-144"

      testStartLog $testName

      set purpose {Verify you can create a Static ABOT IPSec Branch Office tunnel with Text Preshared key and permit all filter, between Calvin and the latest build. Enable IKE Encryption and Diffie Hellman Group 5 AES, and AH Authentication only (HMAC-MD5) Agressive mode enabled.}
      set description {}
      testPurposeLog $purpose $description

      variable swAddr1
      variable swAddr2

      variable calvinBuild
      if {$calvinBuild == "none"} {
         logFile "The Calvin build doesn't exist in CES ($swAddr1)"
         testEndLog $testName "ABORT"
         return
      }
      bootBuild $calvinBuild

      variable ces1PrivateIp

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2
      variable textPass
      variable initiator_uid

      DisBoGrpEncrType $swAddr1 $boGroup "all"
      EnaBoGrpEncrType $swAddr1 $boGroup "hmac-md5"
      EnaBoGrpIkeEncrType $swAddr1 $boGroup "128aes-group5"
      EnaAggressiveMode $swAddr1 $boGroup

      DisBoGrpEncrType $swAddr2 $boGroup "all"
      EnaBoGrpEncrType $swAddr2 $boGroup "hmac-md5"
      EnaBoGrpIkeEncrType $swAddr2 $boGroup "128aes-group5"
      EnaAggressiveMode $swAddr2 $boGroup

      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static IPSEC ABOT / initiator / text pre-shared key "
      ConfigIpSecBO $swAddr1 $boName_ces1 $boGroup "text $textPass $initiator_uid" "initiator $ces2PublicIp" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static IPSEC ABOT / responder / text pre-shared key"
      ConfigIpSecBO $swAddr2 $boName_ces2 $boGroup "text $textPass $initiator_uid" "responder" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      if {[VerifyBoConnection "IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete IPSEC ABOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      EnaBoGrpEncrType $swAddr1 $boGroup "all"
      DelNetwork "local_nets_1" $swAddr1
      DisAggressiveMode $swAddr1 $boGroup

      logFile "CES: $swAddr2 - delete IPSEC ABOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      EnaBoGrpEncrType $swAddr2 $boGroup "all"
      DelNetwork "local_nets_2" $swAddr2
      DisAggressiveMode $swAddr2 $boGroup

      testEndLog $testName $error_code
   }


   proc T-145 {} {

      set error_code "FAIL"
      set testName "T-145"

      testStartLog $testName

      set purpose {Verify a Static Peer to Peer IPSec Branch Office tunnel with Text Preshared key and permit all filter, between Calvin (V04_70.xxx) and the latest build can not be brought up when : Enable IKE encryption and Diffie Hellman Group 5 AES and encryption is ESP  AES 128 with SHA1 integrity. Vendor ID is disabled and aggressive mode is disabled.}
      set description {}
      testPurposeLog $purpose $description

      variable swAddr1
      variable swAddr2

      variable calvinBuild
      if {$calvinBuild == "none"} {
         logFile "The Calvin build doesn't exist in CES ($swAddr1)"
         testEndLog $testName "ABORT"
         return
      }
      bootBuild $calvinBuild

      variable ces1PrivateIp
      variable ces1PublicIp

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2
      variable textPass

      DisBoGrpEncrType $swAddr1 $boGroup "all"
      EnaBoGrpEncrType $swAddr1 $boGroup "aes128-sha1"
      EnaBoGrpIkeEncrType $swAddr1 $boGroup "128aes-group5"
      DisAggressiveMode $swAddr1 $boGroup
      DisVendorId $swAddr1 $boGroup

      DisBoGrpEncrType $swAddr2 $boGroup "all"
      EnaBoGrpEncrType $swAddr2 $boGroup "aes128-sha1"
      EnaBoGrpIkeEncrType $swAddr2 $boGroup "128aes-group5"
      DisAggressiveMode $swAddr2 $boGroup
      DisVendorId $swAddr2 $boGroup

      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static IPSEC BOT "
      ConfigIpSecBO $swAddr1 $boName_ces1 $boGroup "text $textPass" "p2p $ces1PublicIp $ces2PublicIp" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static IPSEC BOT"
      ConfigIpSecBO $swAddr2 $boName_ces2 $boGroup "text $textPass" "p2p $ces2PublicIp $ces1PublicIp" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      if {[VerifyNegativeBoConnection "IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete IPSEC BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      EnaBoGrpEncrType $swAddr1 $boGroup "all"
      DelNetwork "local_nets_1" $swAddr1
      EnaVendorId $swAddr1 $boGroup

      logFile "CES: $swAddr2 - delete IPSEC BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      EnaBoGrpEncrType $swAddr2 $boGroup "all"
      DelNetwork "local_nets_2" $swAddr2
      EnaVendorId $swAddr2 $boGroup

      testEndLog $testName $error_code
   }


   proc T-146 {} {

      set error_code "FAIL"
      set testName "T-146"

      testStartLog $testName

      set purpose {Verify a branch office tunnel can not  be brought up when the branch office tunnel is configured as : Dynamic Peer to Peer, with IPSec and a Text Preshared key using a permit all filter. IKE Encryption and Diffie-Hellman Group 5 AES and ESP- AES 128SHA1 integrity. Between Calvin (V04_70.xxx) and the latest build. Vendor ID is disabled and aggressive mode is disabled.}
      set description {}
      testPurposeLog $purpose $description

      variable swAddr1
      variable swAddr2

      variable calvinBuild
      if {$calvinBuild == "none"} {
         logFile "The Calvin build doesn't exist in CES ($swAddr1)"
         testEndLog $testName "ABORT"
         return
      }
      bootBuild $calvinBuild

      variable ces1PrivateIp
      variable ces1PublicIp

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2
      variable textPass

      DisBoGrpEncrType $swAddr1 $boGroup "all"
      EnaBoGrpEncrType $swAddr1 $boGroup "aes128-sha1"
      EnaBoGrpIkeEncrType $swAddr1 $boGroup "128aes-group5"
      DisAggressiveMode $swAddr1 $boGroup
      DisVendorId $swAddr1 $boGroup

      DisBoGrpEncrType $swAddr2 $boGroup "all"
      EnaBoGrpEncrType $swAddr2 $boGroup "aes128-sha1"
      EnaBoGrpIkeEncrType $swAddr2 $boGroup "128aes-group5"
      DisAggressiveMode $swAddr2 $boGroup
      DisVendorId $swAddr2 $boGroup

      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      logFile "CES: $swAddr1 - add dynamic rip IPSEC BOT"
      ConfigIpSecBO $swAddr1 $boName_ces1 $boGroup "text $textPass" "p2p $ces1PublicIp $ces2PublicIp" "rip"

#      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip IPSEC BOT"
      ConfigIpSecBO $swAddr2 $boName_ces2 $boGroup "text $textPass" "p2p $ces2PublicIp $ces1PublicIp" "rip"

      if {[VerifyNegativeBoConnection "IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete IPSEC BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      EnaBoGrpEncrType $swAddr1 $boGroup "all"
      EnaVendorId $swAddr1 $boGroup
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete IPSEC BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      EnaBoGrpEncrType $swAddr2 $boGroup "all"
      EnaVendorId $swAddr2 $boGroup
#      DisableRip $swAddr2

      testEndLog $testName $error_code
   }


   proc T-147 {} {

      set error_code "FAIL"
      set testName "T-147"

      testStartLog $testName

      set purpose {Verify a branch office tunnel can not  be brought up when the branch office tunnel is configured as : Dynamic  Peer to Peer with IPSec and a Text Preshared key using a permit all filter. IKE Encryption and Diffie-Hellman Group 5 AES and ESP128 SHA1 encryption. Between Calvin (V04_70.xxx) and the latest build. Vendor ID is disabled and aggressive mode is enabled}
      set description {}
      testPurposeLog $purpose $description

      variable swAddr1
      variable swAddr2

      variable calvinBuild
      if {$calvinBuild == "none"} {
         logFile "The Calvin build doesn't exist in CES ($swAddr1)"
         testEndLog $testName "ABORT"
         return
      }
      bootBuild $calvinBuild

      variable ces1PrivateIp
      variable ces1PublicIp

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2
      variable textPass

      DisBoGrpEncrType $swAddr1 $boGroup "all"
      EnaBoGrpEncrType $swAddr1 $boGroup "aes128-sha1"
      EnaBoGrpIkeEncrType $swAddr1 $boGroup "128aes-group5"
      EnaAggressiveMode $swAddr1 $boGroup
      DisVendorId $swAddr1 $boGroup

      DisBoGrpEncrType $swAddr2 $boGroup "all"
      EnaBoGrpEncrType $swAddr2 $boGroup "aes128-sha1"
      EnaBoGrpIkeEncrType $swAddr2 $boGroup "128aes-group5"
      EnaAggressiveMode $swAddr2 $boGroup
      DisVendorId $swAddr2 $boGroup

      EnableRip $swAddr1
      SetRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      logFile "CES: $swAddr1 - add dynamic rip IPSEC BOT"
      ConfigIpSecBO $swAddr1 $boName_ces1 $boGroup "text $textPass" "p2p $ces1PublicIp $ces2PublicIp" "rip"

#      EnableRip $swAddr2
      SetRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      logFile "CES: $swAddr2 - add dynamic rip IPSEC BOT"
      ConfigIpSecBO $swAddr2 $boName_ces2 $boGroup "text $textPass" "p2p $ces2PublicIp $ces1PublicIp" "rip"

      if {[VerifyNegativeBoConnection "IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete IPSEC BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      DelRipNetwork $ces1PrivateIp "255.255.255.0" $swAddr1
      EnaBoGrpEncrType $swAddr1 $boGroup "all"
      DisAggressiveMode $swAddr1 $boGroup
      EnaVendorId $swAddr1 $boGroup
      DisableRip $swAddr1

      logFile "CES: $swAddr2 - delete IPSEC BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      DelRipNetwork $ces2PrivateIp "255.255.255.0" $swAddr2
      EnaBoGrpEncrType $swAddr2 $boGroup "all"
      DisAggressiveMode $swAddr2 $boGroup
      EnaVendorId $swAddr2 $boGroup
#      DisableRip $swAddr2

      testEndLog $testName $error_code
   }


   proc T-148 {} {

      set error_code "FAIL"
      set testName "T-148"

      testStartLog $testName

      set purpose {Verify an IPsec branch office tunnel fails when configured with mismatched Diffie-Hellman Encryptions. Configure a Static Peer to Peer with a Text Preshared key and permit all filter, between Calvin (V04_70.xxx) and the latest build. Enable IKE Encryption and Diffie Hellman Group 5 AES, and AH Authentication only (HMAC-SHA1) Enable other of tunnel with CES with IKE Encryption and Diffie-Hellman Group 8 AES-128 (ECC283-=bit field) Vendor ID enabled and aggressive mode enabled.}
      set description {}
      testPurposeLog $purpose $description

      variable swAddr1
      variable swAddr2

      variable calvinBuild
      if {$calvinBuild == "none"} {
         logFile "The Calvin build doesn't exist in CES ($swAddr1)"
         testEndLog $testName "ABORT"
         return
      }
      bootBuild $calvinBuild

      variable ces1PrivateIp
      variable ces1PublicIp

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boGroup
      variable boName_ces1
      variable boName_ces2
      variable textPass

      DisBoGrpEncrType $swAddr1 $boGroup "all"
      EnaBoGrpEncrType $swAddr1 $boGroup "aes128-sha1"
      EnaBoGrpIkeEncrType $swAddr1 $boGroup "128aes-group5"
      EnaAggressiveMode $swAddr1 $boGroup
      EnaVendorId $swAddr1 $boGroup

      DisBoGrpEncrType $swAddr2 $boGroup "all"
      EnaBoGrpEncrType $swAddr2 $boGroup "aes128-sha1"
      EnaBoGrpIkeEncrType $swAddr2 $boGroup "128aes-group8"
      EnaAggressiveMode $swAddr2 $boGroup
      EnaVendorId $swAddr2 $boGroup


      AddNetwork "local_nets_1" [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 $swAddr1
      logFile "CES: $swAddr1 - add static IPSEC BOT "
      ConfigIpSecBO $swAddr1 $boName_ces1 $boGroup "text $textPass" "p2p $ces1PublicIp $ces2PublicIp" "static local_nets_1 [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      AddNetwork "local_nets_2" [getNet $ces2PrivateIp 255.255.255.0] 255.255.255.0 $swAddr2
      logFile "CES: $swAddr2 - add static IPSEC BOT"
      ConfigIpSecBO $swAddr2 $boName_ces2 $boGroup "text $textPass" "p2p $ces2PublicIp $ces1PublicIp" "static local_nets_2 [getNet $ces1PrivateIp 255.255.255.0] 255.255.255.0 enable 0"

      if {[VerifyNegativeBoConnection "IPSEC"] == "SUCCESS"} {
         set error_code "PASS"
      }

      logFile "CES: $swAddr1 - delete IPSEC BOT"
      DelBoConn $boName_ces1 $boGroup $swAddr1
      EnaBoGrpEncrType $swAddr1 $boGroup "all"
      DelNetwork "local_nets_1" $swAddr1
      DisAggressiveMode $swAddr1 $boGroup

      logFile "CES: $swAddr2 - delete IPSEC BOT"
      DelBoConn $boName_ces2 $boGroup $swAddr2
      EnaBoGrpEncrType $swAddr2 $boGroup "all"
      DelNetwork "local_nets_2" $swAddr2
      DisAggressiveMode $swAddr2 $boGroup

      testEndLog $testName $error_code
   }


   proc T-158 {} {

      set error_code "FAIL"
      set testName "T-158"

      set err_count 0

      testStartLog $testName

      set purpose {Verify CLI commands for an ABOT IPSec Tunnel using AES Group 8 and 5}
      set description {}
      testPurposeLog $purpose $description

      variable swAddr2

      variable boGroup

      set encrList {aes128-sha1 3des-sha1 3des-md5 des56-sha1 des56-md5 des40-sha1 des40-md5}

      foreach encrType $encrList {
         if {[EnaBoGrpEncrType $swAddr2 $boGroup $encrType] != "SUCCESS" || \
                 [DisBoGrpEncrType $swAddr2 $boGroup $encrType] != "SUCCESS"} {
            incr err_count
         }
      }

      if { $err_count == 0 } {
         set error_code "PASS"
      }

      testEndLog $testName $error_code
   }


   proc {CLEANUP} {} {

      global logDir
      variable suiteName
      variable cliFileId

      suiteEndLog $suiteName

      variable swAddr1
      variable swAddr2
      variable boGroup

      variable testedBuild
      bootBuild $testedBuild

      DelBoGroup $boGroup $swAddr1
      DelBoGroup $boGroup $swAddr2

      Disconnect all

      #close CLI LOG file
      EndCliLog $cliFileId
      CLILogFormat "CLI.log" $logDir

      return

   }; #end CLEANUP proc



   #################################################################################################
   # common use procedures
   #################################################################################################

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

      logFile "CES $swAddr - sets parameters: proxy-arp, system forwarding and maximim path"
      #// sets CES parameters need for OSPF test
      SetCliLevel "CONFIG" $swAddr

      #// disable all proxy arp
      SetGlobalSysFwdArp "no_enable" "no_enable" "no_enable" $swAddr
      #// Ensure that Rip is not available on management interface
      DelRipNetwork $mngIfIp  255.255.255.0 $swAddr

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


   proc VerifyNegativeBoConnection {{bo_type ""} {number 4}} {

      variable swAddr1
      variable swAddr2

      variable ces1PrivateIp
      variable ces1PublicIp

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boName_ces1
      variable boName_ces2

      if {[VerifyTunnel $swAddr1 $ces2PrivateIp $ces1PrivateIp $number] == "SUCCESS"} {
         logFile "CES: $swAddr1 - ping to $ces2PrivateIp from $ces1PrivateIp - got reply!" "FAIL"
         return "ERROR"
      } else {
         logFile "CES: $swAddr1 - ping to $ces2PrivateIp from $ces1PrivateIp - no reply!" "PASS"
      }

      if {[VerifyTunnel $swAddr2 $ces1PrivateIp $ces2PrivateIp $number] == "SUCCESS"} {
         logFile "CES: $swAddr2 - ping to $ces1PrivateIp from $ces2PrivateIp - got reply!" "FAIL"
         return "ERROR"
      } else {
         logFile "CES: $swAddr2 - ping to $ces1PrivateIp from $ces2PrivateIp - no reply!" "PASS"
      }

      if {$bo_type != ""} {
         if {[VerifyBoIsUp $boName_ces1 $swAddr1] == "YES"} {
            logFile "CES: $swAddr1 - BO is up" "FAIL"
            return "ERROR"
         } else {
            logFile "CES: $swAddr1 - BO is not up" "PASS"
         }

         if {[VerifyBoIsUp $boName_ces2 $swAddr2] == "YES"} {
            logFile "CES: $swAddr2 - BO is up" "FAIL"
            return "ERROR"
         } else {
            logFile "CES: $swAddr2 - BO is not up" "PASS"
         }
      }

      return "SUCCESS"
   }


   proc VerifyBoControlConnection {ces1Ip {number 4}} {

      variable swAddr1
      variable swAddr2

      variable ces1PublicIp

      variable ces2PrivateIp
      variable ces2PublicIp

      variable boName_ces1
      variable boName_ces2

      #         if {[VerifyTunnel $swAddr1 $ces2PrivateIp $ces1PrvIp $number] != "SUCCESS"} {
      #             logFile "CES: $swAddr1 - ping to $ces2PrivateIp from $ces1PrvIp - no reply!" "FAIL"
      #             incr err_count
      #         } else {
      #             logFile "CES: $swAddr1 - ping to $ces2PrivateIp from $ces1PrvIp - got reply!" "PASS"
      #         }

      if {[VerifyTunnel $swAddr2 $ces1Ip $ces2PrivateIp $number] != "SUCCESS"} {
         logFile "CES: $swAddr2 - ping to $ces1Ip from $ces2PrivateIp - no reply!" "FAIL"
         return "ERROR"
      } else {
         logFile "CES: $swAddr2 - ping to $ces1Ip from $ces2PrivateIp - got reply!" "PASS"
      }

      if {[VerifyBoIsUp $boName_ces1 $swAddr1] != "YES"} {
         logFile "CES: $swAddr1 - BOT is not up" "FAIL"
         return "ERROR"
      } elseif {[GetBoType $boName_ces1 $swAddr1] != "IPSEC"} {
         logFile "CES: $swAddr1 - BOT is up but type is not IPSEC" "FAIL"
         return "ERROR"
      } else {
         logFile "CES: $swAddr1 - BOT is up and type is IPSEC" "PASS"
      }

      if {[VerifyBoIsUp $boName_ces2 $swAddr2] != "YES"} {
         logFile "CES: $swAddr2 - BOT is not up" "FAIL"
         return "ERROR"
      } elseif {[GetBoType $boName_ces2 $swAddr2] != "IPSEC"} {
         logFile "CES: $swAddr2 - BOT is up but type is not IPSEC" "FAIL"
         return "ERROR"
      } else {
         logFile "CES: $swAddr2 - BOT is up and type is IPSEC" "PASS"
      }

      return "SUCCESS"
   }


   proc aceWait {time {message ""}} {
      puts "\n"
      for {set i $time} {$i>0} {incr i -1000} {
         puts -nonewline " $message - wait [expr $i/1000] seconds  \r"
         flush stdout
         after 1000
      }
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

};
