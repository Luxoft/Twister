#############################################
#// Converts standart ip dot notation to hex
proc {ipToHex} {address} {
  foreach ipByte [split $address {.}] {
    append hexAddr [format {%02x} $ipByte]
  }
  return "0x$hexAddr"
}

#############################################
#// Converts an integer to Doted notation
proc {intToQuad} {number} {
  binary scan [binary format I $number] cccc a b c d
  format %d.%d.%d.%d \
  [expr $a&255] [expr $b&255] [expr $c&255] [expr $d&255]
}

#############################################
#// Converts a dot notation address to int
proc {quadToInt} {address} {
  set temp [expr 256 * 256 * 256 * [lindex [split $address .] 0] + 256*256*[lindex [split $address .] 1] + \
      256*[lindex [split $address .] 2] + [lindex [split $address .] 3]]
  return $temp
}
#############################################
#// Splits the IP Address into net and host
proc {splitIP} {number {netwidth 24}} {
  set numwidth [expr {32-$netwidth}]
  binary scan [binary format I $number] B${netwidth}B${numwidth} a b
  binary scan [binary format B* [format %032s $a]] I net
  binary scan [binary format B* [format %032s $b]] I num
  return [list $net $num]
}

#############################################
#// Combines a number into the net addr.
proc {joinIP} {net num {netwidth 24}} {
  set numwidth [expr {32-$netwidth}]
  binary scan [binary format I $net] B${numwidth}B${netwidth} x netb
  binary scan [binary format I $num] B${netwidth}B${numwidth} x numb
  binary scan [binary format B32 $netb$numb] I number
  format %u $number; # Convert to unsigned!
}

#############################################
#// Get local client ip address
proc {getLocalIp} {} {
  if {[catch {set sock [socket -server xxx -myaddr [info hostname] 0]} err]} {
    set ip [interfaceLocal:get]
  } else {
    set ip [lindex [fconfigure $sock -sockname] 0]
    close $sock
  }
  if {$ip == "" || $ip == "127.0.0.1"} {
    set ip [interfaceLocal:get]
  }
  return $ip
}
###########################################################
## Procedure:  Global:getrandomip

proc {getrandomip} {{class c}} {
global widget objIpList
#// Returns a random IP Address....
set octet1 127;
set octet2 0;
set octet3 0;
set octet4 0;
set mask 0.0.0.0;
set broad 0.0.0.0;
set error false;
if {$class == "a" || $class == "A"} {
  set low 1
  set high 126
} elseif {$class == "b" || $class == "B"} {
  set low 128
  set high 191
} elseif {$class == "c" || $class == "C"} {
  set low 192
  set high 223
} elseif {$class == "d" || $class == "D"} {
  set low 224
  set high 239
} elseif {$class == "e" || $class == "E"} {
  set low 240
  set high 254
} elseif {$class == "r" || $class == "R"} {
  set low 1
  set high 223
}
 while {$octet1 == "127"} {
   set octet1 [expr rand() * ($high - $low) + $low]
   set octet1 [expr int($octet1)]
 }
 
 set octet2 [expr rand() * 254]
 set octet2 [expr int($octet2)]
 
 set octet3 [expr rand() * 254] 
 set octet3 [expr int($octet3)]
 
 set octet4 [expr rand() * 253 + 1]
 set octet4 [expr int($octet4)]
 
 return $octet1.$octet2.$octet3.$octet4
}

#############################################
#// Get the network from an ip address
proc {getNet_old} {address} {
 set brokeip [split $address .]
 if {[lindex $brokeip 0] < 128} {
   set network "[lindex $brokeip 0].0.0.0"
 } elseif {[lindex $brokeip 0] < 192} {
   set network "[lindex $brokeip 0].[lindex $brokeip 1].0.0"
 } elseif {[lindex $brokeip 0] > 191} {
   set network "[lindex $brokeip 0].[lindex $brokeip 1].[lindex $brokeip 2].0"
 }
 return $network
}

proc getNet {address {mask NONE}} {
	if {$mask == "NONE"} {
		return [getNet_old $address]
	}

	set net ""
	set brokeIp [split $address "."]  
	set brokeMask [split $mask "."]  
	append net [expr [lindex $brokeIp 0] & [lindex $brokeMask 0]] \
		. [expr [lindex $brokeIp 1] & [lindex $brokeMask 1]] \
		. [expr [lindex $brokeIp 2] & [lindex $brokeMask 2]] \
		. [expr [lindex $brokeIp 3] & [lindex $brokeMask 3]]
	
	return $net	

}

proc getBroadcast {address mask} {

	set broadIp ""; #broadcast address

	set brokeIp [split $address "."]  
	set brokeMask [split $mask "."]  
	append broadIp [expr 255 ^ [lindex $brokeMask 0] | [lindex $brokeIp 0]] \
		. [expr 255 ^ [lindex $brokeMask 1] | [lindex $brokeIp 1]] \
		. [expr 255 ^ [lindex $brokeMask 2] | [lindex $brokeIp 2]] \
		. [expr 255 ^ [lindex $brokeMask 3] | [lindex $brokeIp 3]]
	
	return $broadIp
}

#############################################
#// Get the host from an ip address
proc {getHost} {address} {
 set brokeip [split $address .]
 if {[lindex $brokeip 0] < 128} {
   set host "[lindex $brokeip 1].[lindex $brokeip 2].[lindex $brokeip 3]"
 } elseif {[lindex $brokeip 0] < 192} {
   set host "[lindex $brokeip 2].[lindex $brokeip 3]"
 } elseif {[lindex $brokeip 0] > 191} {
   set host "[lindex $brokeip 3]"
 }
 return $host
}

#############################################
#// Get the network mask
proc {getNetMask} {address args} {
 set brokeip [split $address .]
 if {[lindex $brokeip 0] < 128} {
   set mask "255.0.0.0"
   set Mask 8
 } elseif {[lindex $brokeip 0] < 192} {
   set mask "255.255.0.0"
   set Mask 16
 } elseif {[lindex $brokeip 0] > 191} {
   set mask "255.255.255.0"
   set Mask 24
 }
 if {$args != "int"} {
   return $mask
 } else {
   return $Mask
 }
}

#############################################
#// get the network by what mask is used.
proc {getByMask} {address mask} {
 set brokeip [split $address .]
 if {$mask == 8} {
   set addr "[lindex $brokeip 0]"
 } elseif {$mask == 16} {
   set addr "[lindex $brokeip 0].[lindex $brokeip 1]"
 } elseif {$mask == 24} {
   set addr "[lindex $brokeip 0].[lindex $brokeip 1].[lindex $brokeip 2]"
 }
 return $addr
}

#############################################################
# incrHost: Increment the last octed from an IP address.
#           The incrementing is done modulo 255
#
# IN:  address: A.B.C.D  ip address
#      num:     the value for incrementing D (from the IP address)
#               
# OUT: the new IP address
#############################################################
proc {incrHost} {address num} {
   set brokeip [split $address .]
   set host [lindex $brokeip 3]
   set net "[lindex $brokeip 0].[lindex $brokeip 1].[lindex $brokeip 2]"
   incr host $num
   #set host [expr $host % 255]
   #change to modulo 256 so that hosts like A.B.C.255 will be allowed
   set host [expr $host % 256]
   set ip "$net.$host"
   return $ip
}

