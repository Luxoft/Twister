########################################################################
#!/usr/bin/tclsh
# Procedures for generating and parsing TCP/IP packets
# 
# Packets can be captured with tcpdump or with snifftool.
# As packet generators can be used any programs that generates TCP/IP packets, as:
# sendip, hping2 ...
# 
# # packet capture procedures
# - OBSOLATED - traffic tools are started using tcl 'exec' command
# StartCapture {tool toolargs {time_out "NONE"}}
# StopCapture {pid}
#
# - start the traffic generating/capture tools wiht expect
# RunTool {tool_call}
#
#
# # packet analyze procedures for packet capture with TCPDUMP.
# IMPORTANT: USE ONLY '-env' options for tcpdump.
#            
#
# OBSOLATED:
# !!! IMPORTANT: packets should be captured with snifftool if you want to use this procedures for packet analize.
#
#                using snifftool you may capture other packets than IP. (Eq STP)
#                for each procedures related to some speciffic protocol, add the ptotocol name in the name of the procedure
#                e.g:   - Eth<proc name> - for procedures that handle ethernet header
#                       - Ip<proc name>  -      -//-                     IP header
#                       - Tcp<proc name> -      -//-                     TCP header
#
########################################################################



###################################################################################
# capture procedures
###################################################################################

#############################################################
# StartCapture: starts packet capture.
#
# IMPORTANT: USE ONLY '-env' options for tcpdump.
#
# IN:  tool:     <tcpdump/snifftool/ ...>  program used for packet capture
#      toolargs: Command line parameters nedded by tool  
#      time_out: <(time in miliseconds)/NONE> How long to wait until stop the capture program.
#                When 'NONE': return capture process PID and no stop the capture prior return.
#
# OUT: ERROR:   if no packet capture program 'tool' available
#      OKKILL:  if packet capture stopped after 'time_out' expired
#      too PID: PID of packet capture process.
#############################################################
proc StartCapture {tool toolargs {time_out "NONE"}} {

   if {[file executable $tool] || $tool == "tcpdump"} {
      if {$toolargs != ""} {
         foreach elem $toolargs {
            lappend tool $elem
         }
         set cmd "exec $tool &"
         LogFile "StartCapture: \n$cmd" debug
         set toolPID [eval $cmd]
      }
      #puts $toolPID
   } else {
      puts "packet capture tool: '$tool' not found, or not an executable file"
      return "ERROR"
   }

   if {$time_out != "NONE"} {
      after $time_out
      catch {exec kill $toolPID} out
      catch {exec kill $toolPID} out
      return "OKKILL"
   }

   return $toolPID
}

#############################################################
# StopCapture: Stops the packet capture process.
#
# IN:  pid: packet capture process ID.
#
# OUT: OKKILL
#
# NOTE: not handled errors which can appear at 'kill $pid'
#############################################################
proc StopCapture {pid} {
   catch {exec kill $pid} out
   #puts "out = $out"
   #catch {exec kill -s SIGTERM $toolPID} out
   return "OKKILL"   
}

# --- end capture procedures --- # 


#############################################################
# RunTool: Run a traffic capture or traffic generating external tool available
#          on the test PC (the PC running ace)
#          The tool is run using Expect calls (exp_spawn).
#
# IN:  tool_call: exactly the same call used to run the tool from shell command
#                 line must contain the tool name and the tool options.
#                 Ex: tool_call = tcpdump -i eth0 -v dst host 1.1.1.1
# OUT: the spawn ID for the spawned tool - if the succeded to start the tool
#      ERROR - otherwise
#############################################################
proc RunTool {tool_call} {
   set err_count [GetGlobalErr]

   global spawn_id

   # build the Expect call for running hping2.
   set tool_name [lindex $tool_call 0]
   set expect_call "exp_spawn"
   foreach elem $tool_call {         
      lappend expect_call $elem
   }  
   if {[catch {eval $expect_call} result] != 0} {         
      ErrCheck [list "ERROR: Cannot start $tool_name. Please check that $tool_name exists and you have the 'root' rights"]
      logFile $result
      return [CheckGlobalErr $err_count]
   } else {         
      set tool_id $spawn_id
      return $tool_id
   }      
}



#############################################################
# 
# PROCEDURES FOR PARSING TEXT CAPTURE FILES GOT USING TCPDUMP
#
# IMPORTANT:
#     Data relating packet must be in the format given by:
#
#     tcpdump -env ?filtering expression? ...
#
#     Packet parsing is not supported for other format of packet.
#
#############################################################

#############################################################
# TdPacketList: Creates a list which conatins the packets 
#               captured with tcpdump.
#               This proc assumes that the packets captured with tcpdump
#               was saved first into a file and then read from this file.
#
#               Each list element = data relating to a packet
#
# IN:  captured_packets: data got with tcpdump.
#     
# OUT: packet list
#############################################################
proc TdGetPacketList {captured_packets} {

   set packet_list ""   

   regsub -all {[0-9]+:[0-9]+:[0-9]+\.[0-9]+} $captured_packets {!} captured_packets

   foreach elem [split $captured_packets "!"] {      
      if {$elem != ""} {
         lappend packet_list $elem
      }

   }   
   
   return $packet_list

}


#############################################################
# TdParsePacketEth:   Gets the data relating to ethernet header
#                     from packet.                     
#                     Returns the data given by info_to_get 
#
# tcpdump output support: 	tcpdump version 3.7.2
#                        	libpcap version 0.7.2
#
#                        	tcpdump version 3.8.3
#                       	libpcap version 0.8.3
#
#
# IN:  packet:      The data relating to a captured packet, in the
#                   format given by 'tcpdump -env'
#      info_to_get: <src_mac/dst_mac/ether_proto/size/other>
#                   Which ethernet header relating data you want
#                   to get.
#                   When other - returns data after ehternet header.
#                   
# OUT: NONE/(the value for info to get)      
#############################################################
proc TdParsePacketEth {packet info_to_get} {

   set $info_to_get "NONE"

   if {[regexp {ethertype} $packet] == 1} {
      regexp {(([0-9a-fA-F]+:?)+) > (([0-9a-fA-F]+:?)+), ethertype ([0-9a-zA-Z]+) \(0x[0-9A-Fa-f]+\), length ([0-9]+): (.+)} \
          $packet \
          all src_mac 1_ dst_mac 1_ ether_proto size other
   } else {
      regexp {(([0-9a-fA-F]+:?)+) (([0-9a-fA-F]+:?)+) ([0-9a-zA-Z]+) ([0-9a-fA-F]+): (.+)} \
          $packet \
          all src_mac 1_ dst_mac 1_ ether_proto size other
   }

#    puts $all
#    puts "src_mac    : $src_mac"
#    puts "dst_mac    : $dst_mac"
#    puts "ether_proto: $ether_proto"   
#    puts "size       : $size"
#    puts "other      : $other"
   
   if {[set $info_to_get] == ""} {
      set $info_to_get "NONE"
   }
   
   return [set $info_to_get]

}


#############################################################
# TdParsePacketPPPoE: Gets the data relating to pppoe header from
#                     packet.
#                     Returns the data given by info_to_get 
#
#
# IN:  packet:      The data relating to a captured packet, in the
#                   format given by 'tcpdump -env'
#      info_to_get: <pppoe_ses/ppp_proto/pppoe_payload_size/other>
#                     
#                   which L2 or (ip address)/(ip address.port) you want to get
#                   
#
# OUT: the value for info to get.
#############################################################
proc TdParsePacketPPPoE {packet info_to_get} {
   
   # 'PPPoE  [ses 0x20] IP 42:' -  PPPoE, pppoe_ses, ppp_proto, pppoe_payload_size
   
   set all "NONE"
   set pppoe_sesion "NONE"

   set $info_to_get "NONE"

   #set data [TdParsePacketEth $packet "other"]

   #PPPoE \[ses ([0-9a-zA-Z]+)\] ([0-9a-zA-Z]+) ([0-9]+): (.*)
   regexp {PPPoE[\ \t]+\[ses ([0-9a-zA-Z]+)\] ([0-9a-zA-Z]+) ([0-9]+): (.*)} \
       $packet \
       all pppoe_ses ppp_proto pppoe_payload_size other

   if {[set $info_to_get] == ""} {
      set $info_to_get "NONE"
   }
   
   #puts "*** pppoe all = $all"
   #puts "*** pppoe_sesion = $pppoe_sesion"
   return [set $info_to_get]
   #return $all
}


#############################################################
# TdParsePacketIP:  Gets the data relating to ip header from
#                   packet.
#                   Returns the data given by info_to_get 
#
#
# IN:  packet:      The data relating to a captured packet, in the
#                   format given by 'tcpdump -env <filter expression>'
#      info_to_get: <src_ip_port/dst_ip_port/other>                                        
#
# OUT: NONE/(the value for info to get)
#############################################################
proc TdParsePacketIP {packet info_to_get} {

   set $info_to_get "NONE"

   regexp {(([0-9]+\.?)+) > (([0-9]+\.?)+): (.*)} \
       $packet \
       all src_ip_port 1_ dst_ip_port 1_ other  

   if {[set $info_to_get] == ""} {
      set $info_to_get "NONE"
   }
   
   return [set $info_to_get]
}


#############################################################
# TdParsePacketTcp:  Parses data relating to TCP header
#
# IN:  tcp_packet_data: TCP relating data from Captured packet data.
#      info_to_get:     <flag/tcp_sum/seq_no/ack_no/win/mss> 
#                       which data you want to get from TCP header                                                                     
#
# OUT: the value for info to get.
#############################################################
proc TdParsePacketTcp {tcp_packet_data info_to_get} {

   set $info_to_get "NONE"

   #{([S|P|F|R|\.]) ([0-9a-zA-Z\[\]\(\):\ ]+)(<mss ([0-9]+))?}
   regexp {([S|P|F|R|\.]) \[([a-zA-Z0-9\ ]+)\] ([0-9]+):([0-9]+)\([0-9]+\)\ ?(ack ([0-9]+))? win ([0-9]+)\ ?(<mss ([0-9]+))?} \
       $tcp_packet_data \
       all flag tcp_sum seq_no ack_no 1_ rst_ack win 1_ mss

   if {[set $info_to_get] == ""} {
      set $info_to_get "NONE"
   }

   return [set $info_to_get]

}












#############################################################
# 
# PROCEDURES FOR PARSING HEX CAPTURE FILES
#
#############################################################

####################################################################################
#   General 'capture file' and packets procedure
#   This procedures are to handle the file with captured packets:
#              - get a list with packets 
#              - for each packet get a list of bytes
#
####################################################################################
proc {GetPacketList} {captFile {displ no}} {
   set captFileID [open $captFile r]
   set captOut1 [read $captFileID]
   set packetList ""
   if {[regsub -all {\n====.?[0-9]+.?packet size: [0-9]+.?====} $captOut1 "!" captOut] >=1} {
      set packetList [split $captOut !]
      if {$displ != "no"} { 
         foreach packet  $packetList {
            if {$packet != "" && $packet != "\n" && $packet != " " && $packet != "\r"} {
               puts "===$packet"
            }
         }
      }
   }
   close $captFileID
   return $packetList
}; #end proc GetPacketList


proc {GetByteList} {packet} {
   set byteList ""
   foreach byte [split $packet] {
      if {$byte != "" && $byte != "\n" && $byte != "\r" && $byte != " "} {
         if {[string length $byte] == 1} {
            set x 0;
            set byte [append x $byte]
         }
         lappend byteList $byte
         #puts $byte
      }
   }
   return $byteList
}

# x * x *...*x by y times
proc {Power} {x y} {
   set power 1
   if {$x == 0} {
      set power 0
   } elseif {$y == 0} {
      set power 1
   } else {
      for {set i 1} {$i<=$y} {incr i} {
         set power [expr $power * $x]
      }
   }
   return $power
}

proc {ConvertHexDec} {hexNumber} {
   LogFile "ConvertHexDec: Duplicate function.  Please use HexToDec"
   puts "ConvertHexDec: Duplicate function.  Please use HexToDec"
   return [HexToDec $hexNumber]

   set i 1; set decNumber 0
   set listDigit [split $hexNumber ""]
   set lengthHex [llength $listDigit]
   foreach digit $listDigit {
      set decNumber [expr $decNumber + [Power 16 [expr $lengthHex -$i]] * [ConvertHexDecDigit $digit]]
      incr i
   }
   return $decNumber
}

proc {ConvertHexDecDigit} {hexDigit} {
   LogFile "ConvertHexDec: Duplicate function.  Please use HexToDec"
   puts "ConvertHexDec: Duplicate function.  Please use HexToDec"
   return [HexToDec $hexNumber]

   set decNb ""
   switch -regexp $hexDigit {
      "[aA]" {set decNb 10}
      "[bB]" {set decNb 11}
      "[cC]" {set decNb 12}
      "[dD]" {set decNb 13}
      "[eE]" {set decNb 14}
      "[fF]" {set decNb 15}
      default {set decNb $hexDigit}
   }
   return $decNb
}

# conversion from 0:4:76:d2:b6:ab  to  00:04:76:d2:b6:ab
proc convertMac_x_0x {mac} {
   set newMac ""
   foreach byte [split $mac ":"] {
      if {[string length $byte] == 1} {
         set x 0;
         lappend newMac [append x $byte]
      } elseif {[string length $byte] == 2} {
         lappend newMac $byte
      }
   }
   regsub -all " " $newMac ":" newMac
   return $newMac
}

# conversion from 00:04:76:d2:b6:ab  to  0:4:76:d2:b6:ab
proc convertMac_0x_x {mac} {
   set newMac ""
   foreach byte [split $mac ":"] {
      if {[string match "0?" $byte] == 1} {
         set byte_1 [string trimleft $byte "0"]
         if {$byte_1 == ""} {
            set byte_1 0
         }        
         lappend newMac $byte_1
      } else {
         lappend newMac $byte
      }
   }
   regsub -all " " $newMac ":" newMac
   return $newMac
}

# --- end general packet procedures --- #







####################################################################################
#   
#   Protocol related procedures
#
#
####################################################################################


##############################################################################
# procedures for ethernet packets
##############################################################################
proc {EthGetSourceMac} {ETHpacket} {
   set ethMac ""
   for {set i 6} {$i < 12} {incr i} {
      set macByte [lindex [GetByteList $ETHpacket] $i]
      lappend ethMac $macByte
   }
   regsub -all " " $ethMac ":" ethMac
   set ethMac [convertMac $ethMac]
   return $ethMac
}

proc {EthGetDestMac} {ETHpacket} {
   set ethMac ""
   for {set i 0} {$i < 6} {incr i} {
      set macByte [lindex [GetByteList $ETHpacket] $i]
      lappend ethMac $macByte
   }
   regsub -all " " $ethMac ":" ethMac
   set ethMac [convertMac $ethMac]
   return $ethMac
}

#############################################################
# HexParsePacketEth:  Gets the data relating to eth header from
#                    packet.
#                    Returns the data given by info_to_get 
#
#
# IN:  packet:       The data relating to a captured packet, in the
#                    hex format given by snifftool.
#      info_to_get:  <src_mac/dst_mac/ether_proto/other>
#                    The field from the ethernet header you want
#                    to get.
#                    When other - returns data after ehternet header.
# OUT: NONE/(the value for info to get)
#############################################################
proc HexParsePacketEth {packet info_to_get} {

   set byteList [GetByteList $packet]

   switch $info_to_get {
      src_mac {
         for {set i 0} {$i<6} {incr i} {
            set pkByte [lindex $byteList $i]
            append src_mac : $pkByte
         }
         set src_mac [string trimleft $src_mac ":"]
      }
      dst_mac {
         for {set i 6} {$i<12} {incr i} {
            set pkByte [lindex $byteList $i]
            append dst_mac : $pkByte
         }
         set dst_mac [string trimleft $dst_mac ":"]
      }
      ether_proto {
         for {set i 12} {$i<14} {incr i} {
            set pkByte [lindex $byteList $i]
            append ether_proto $pkByte
         }
      }
      other {
         for {set i 14} {$i< [llength $byteList]} {incr i} {
            set pkByte [lindex $byteList $i]
            lappend other $pkByte
         }
      }
      default {
         set  $info_to_get "NONE"
      }
   }

   return [set $info_to_get]   
}



#############################################################
# HexParsePacketPPPoE:  Gets the data relating to PPPoE header from
#                    packet.
#                    Returns the data given by info_to_get
#
# IN:  packet:       The data relating to a captured packet, in the
#                    hex format given by snifftool.
#      pppoeType:    <discovery/session>
#      info_to_get:  <version/type/code/session_id/length/tags> if 
#                    pppoeType id "discovery" or
#                    <version/type/code/session_id/length/pppProtoId/other> if 
#                    pppoeType id "session"
#                    The field from the PPPoE header you want
#                    to get.
#                    For "tags" option the result of procedure will
#                    be a list of lists with 3 elements:
#                    TAG_TYPE, LENGTH, VALUE.
# OUT: NONE/(the value for info to get)
#############################################################
proc HexParsePacketPPPoE {packet pppoeType info_to_get} {

   set byteList [GetByteList $packet]
# puts "byteList $byteList"

   switch $info_to_get {
      version { 
         set pkByte [lindex $byteList 14]
         set $info_to_get [string index $pkByte 0]
      }
      type {
         set pkByte [lindex $byteList 14]
         set $info_to_get [string index $pkByte 1]
      }
      code {
         set $info_to_get [lindex $byteList 15]
      }
      session_id {
         set $info_to_get [lindex $byteList 16]
         append $info_to_get [lindex $byteList 17]
      }
      length {
         set $info_to_get [lindex $byteList 18]
         append $info_to_get [lindex $byteList 19]
      }
      tags {
         if { $pppoeType != "discovery" } {
             return "NONE"
         }
         set max_length [lindex $byteList 18]
         append max_length [lindex $byteList 19]
         scan $max_length %x length
#puts "length $length"
         set inf "type"
         set odd 0
         for {set i 20} {$i< [expr 20 + $length]} {incr i} {
            set pkByte [lindex $byteList $i]
            if { $inf == "type" } {
               if { $odd == 0} {
                  set tag_type ""
                  set tag_length ""
                  set tag_value ""
                  set odd 1
               } else {
                  set inf "length"
                  set odd 0
               }
               append tag_type $pkByte

            } elseif { $inf == "length"} {
               append tag_length $pkByte
               if { $odd == 0} {
                  set odd 1
               } else {
                  set odd 0
                  set inf "val"

                  scan $tag_length %x bytes_length
#puts "tag_lenght $bytes_length"
                  if { $bytes_length == 0} {
                     lappend $info_to_get [list $tag_type $bytes_length $tag_value]

puts "type $tag_type length $bytes_length value $tag_value"
                     set inf "type"
                  }
               }
            } elseif { $inf == "val" } {
               lappend tag_value $pkByte
               if { $odd < [expr $bytes_length-1] } {
                  incr odd
               } else {
                  set odd 0
                  lappend $info_to_get [list $tag_type $bytes_length $tag_value]
puts "type $tag_type length $bytes_length value $tag_value"
                  set inf "type"
               }
            }
         }
      }
      pppProtoId {
         if { $pppoeType != "session" } {
             return "NONE"
         }
         set $info_to_get [lindex $byteList 20]
         append $info_to_get [lindex $byteList 21]
puts "pppProtoId = [set $info_to_get]"
      }
      other { if { $pppoeType != "session" } {
             return "NONE"
         }
         set max_length [lindex $byteList 18]
         append max_length [lindex $byteList 19]
         scan $max_length %x length
         for {set i 22} {$i< [expr 20 + $length]} {incr i} {
            set pkByte [lindex $byteList $i]
            lappend $info_to_get $pkByte
         }
puts "other $other"
      }
      default {
         set  $info_to_get "NONE"
      }
   }
# puts [set $info_to_get]
   return [set $info_to_get] 
}

# --- end eth procedures --- #



##############################################################################
# procedures for IP packets
#
#
##############################################################################
proc {IpGetProto} {IPpacket} {
   set protTypeID [lindex [GetByteList $IPpacket] 23]
   switch $protTypeID {
      "1"  {set protType ICMP}
      "2"  {set protType IGMP}
      "6"  {set protType TCP}
      "11" {set protType UDP}
      default {set protType UNKNOWN}
   }
   return $protType
}

###############################################################
# IpFilterProtPackets
#
#      IN:
#            protType   = type of protocol: TCP, UDP, ICMP, IGMP
#            packetList = a list with packets that you want to filter by protocol type
# 
#      OUT:  a list with packets having protocol $protType
#
###############################################################
proc {IpFilterProtPackets} {protType packetList} {
   set filtrPacketList ""
   foreach packet $packetList {
      if {[IpGetProto [GetByteList $packet]] == $protType} {
         lappend filtrPacketList $packet
      }
   }
   return $filtrPacketList
}

#######################################
#      IN:  an IP packet
#      OUT: IP header length in bytes
#######################################
proc {IpGetHeaderLength} {IPpacket} {
   set ipHeaderLength 0
   set verLengthByte [lindex [GetByteList $IPpacket] 14]
   #puts $VerLengthByte
   set length [lindex [split $verLengthByte ""] 1]
   set ipHeaderLength [expr [ConvertHexDec $length] * 4]
   return $ipHeaderLength
}


proc {IpGetPacketLength} {IPpacket} {
   set packetLengthByte1 [lindex [GetByteList $IPpacket] 16]
   set packetLengthByte2 [lindex [GetByteList $IPpacket] 17]
   append packetLengthByte1 $packetLengthByte2
   set ipPacketLength [ConvertHexDec $packetLengthByte1]
   return $ipPacketLength
}

######################################
#      IN:  an IP packet
#      OUT: IP source address
######################################
proc {IpGetSourceAddress} {IPpacket} {
   set Ip ""
   for {set i 26} {$i <= 29} {incr i} {
      set HexIpByte [lindex [GetByteList $IPpacket] $i]
      set DecIpByte [ConvertHexDec [set HexIpByte]]
      lappend Ip $DecIpByte
   }
   regsub -all " " $Ip "." Ip
   return $Ip
}

######################################
#      IN:  an IP packet
#      OUT: IP dest address
######################################
proc {IpGetDestAddress} {IPpacket} {
   set Ip ""
   for {set i 30} {$i <= 33} {incr i} {
      set HexIpByte [lindex [GetByteList $IPpacket] $i]
      set DecIpByte [ConvertHexDec [set HexIpByte]]
      lappend Ip $DecIpByte
   }
   regsub -all " " $Ip "." Ip
   return $Ip
}

# --- end IP procedures --- #








##############################################################################
# procedures for UDP packets
##############################################################################
proc {UdpGetSourcePort} {UDPpacket} {
   set udpPort ""; set HexUdpPort ""
   set firstUdpByte [expr [IpGetHeaderLength $UDPpacket] +14]
   for {set i 0} {$i <= 1} {incr i} {
      set HexUdpByte [lindex [GetByteList $UDPpacket] [expr $i + $firstUdpByte]]
      append HexUdpPort $HexUdpByte
   }
   set DecUdpPort [ConvertHexDec $HexUdpPort]
   return $DecUdpPort
}


proc {UdpGetDestPort} {UDPpacket} {
   set udpPort ""; set HexUdpPort ""
   set firstUdpByte [expr [IpGetHeaderLength $UDPpacket] +14 + 2]
   for {set i 0} {$i <= 1} {incr i} {
      set HexUdpByte [lindex [GetByteList $UDPpacket] [expr $i + $firstUdpByte]]
      append HexUdpPort $HexUdpByte
   }
   set DecUdpPort [ConvertHexDec $HexUdpPort]
   return $DecUdpPort
} 

proc {UdpFilterPortPackets} {{srcPort NONE} {dstPort NONE} UDPpacketList} {
   set filtPortList ""
   foreach packet $UDPpacketList {
      set x 0;
      if {$srcPort != "NONE"} {
         if {[UdpGetSourcePort $packet] == $srcPort} {
            lappend filtPortList $packet
            set x 1
         }
      }
      if {$dstPort != "NONE" && $x == 0} {
         if {[UdpGetDestPort $packet] == $srcPort} {
            lappend filtPortList $packet
            set x 0
         }
      }
   }
   return $filtPortList
}


#--- end UDP procedures --- #



##############################################################################
# procedures for UDP BOOTP packets (UDP/DHCP
##############################################################################
proc {DhcpGetMessagegType} {DHCPpacket} {
   set msgType ""
   set firstDhcpByte [expr [IpGetHeaderLength $DHCPpacket] + 8 + 14]
   set HexDhcpByte [lindex [GetByteList $DHCPpacket] $firstDhcpByte]
   set DecDhcpByte [ConvertHexDec $HexDhcpByte]
   switch $DecDhcpByte {
      "1" {set msgType REQUEST}
      "2" {set msgType REPLY}
   }
   return $msgType
}

proc {DhcpGetClientMACLength} {DHCPpacket} {
   set macLength ""
   set firstDhcpByte [expr [IpGetHeaderLength $DHCPpacket] + 8 + 14]
   set HexMacLength [lindex [GetByteList $DHCPpacket] [expr $firstDhcpByte + 2]]
   set macLength [ConvertHexDec $HexMacLength]
   return $macLength
}

proc {DhcpGetClientMAC} {macLength DHCPpacket} {
   set clientMac ""
   set firstClientMacByte [expr [IpGetHeaderLength $DHCPpacket] + 14 + 8 + 28]
   for {set i 0} {$i < $macLength} {incr i} {
      set clientMacByte [lindex [GetByteList $DHCPpacket] [expr $firstClientMacByte + $i]]
      lappend clientMac $clientMacByte
   }
   regsub -all " " $clientMac ":" clientMac
   set clientMac [convertMac $clientMac]
   return $clientMac
}

# --- end UDP/DHCP procedures --- #

