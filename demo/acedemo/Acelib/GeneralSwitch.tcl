############################################################################
#  This file, GeneralSwitch.tcl is a collection of functions used to       #
#  manipulate or get information about aspects of a switch.  The functions #
#  included are:                                                           #
#                                                                          #
#     HexToBinary {digit}                                                  #
#     DecToHex {decNum}                                                    #
#     HexToDec {hexNum}                                                    #
#     OctetToBitString {octetString}                                       #
#     BitStringToOctet {bitString}                                         #
#     Convert4BitsToOctet {bitString index}                                #
#     ConvertPortToInteger {port}                                          #
#     ConvertPortsToOctet {portList host}                                  #
#     AddOctets {octet1 octet2}                                            #
#     SubtractOctets {octet1 octet2}                                       #
#     DecodeOctet8600 {octetString}                                        #
#     DecodeOctet {octetString {omitFirstNBits false}}                     #
#     Collect1Indices {bitString {card ""}}                                #
#     MyPing {host {count 1}}                                              #
#     MyTraceRoute {route host}                                            #
#     Revert {host}                                                        #
#     RevertApply {host}                                                   #
#     Apply {host {timeout 120} {errcheck set}}                            #
#     Save {host}                                                          #
#     GetSwitchName {host}                                                 #
#     GetTime {host}                                                       #
#     GetSwitchSWVerNum {host}                                             #
#     FactoryResetSwitch {host}                                            #
#     ResetSwitch {host}                                                   #
#     ResetSwitchToDefault {tftpServer host}                               #
#     IsSwitchAlive {host}                                                 #
#     CfgHttpServerPort {port host}                                        #
#     DoTFTP {tftpsrvr tftpType tftpFileName image nextBootImage host}     #
#     GetSWInfo {img1 img2 bootimg bootver host}                           #
#     SetConfigForNextBoot {config host}                                   #
#     SetIPFwd {state host}                                                #
#     GetSwitchType {host}                                                 #
#     IsSwitchTigon {host}                                                 #
#     IsSwitchGNE {host}                                                   #
#     IsSwitch8600 {host}                                                  #
#     IsSwitchWSM {host}                                                   #
#     LinuxGetHostByName {}                                                #
#     LinuxGetIPIntf {ipAddrToFind}                                        #
#     LinuxRemoveIF {ipAddr}                                               #
#     LinuxAddIF {ipAddr}                                                  #
#     LinuxGetConfiguredInterfaces {}                                      #
#     LinuxGetInterfaceIP {intf}                                           #
#     LinuxFindLocalSameNetIP {IPAddr}   
#
#     LogFile {comment {flag false}}
#     FormatMac {mac_addr}                                  #
#                                                                          #
#  For more detail on each function, see the comments above the function.  #
#                                                                          #
# Modified:         mmccawley 06/24/2002 Rework CreateMIBArray to accept   #
#                   arguments to build array from mib files.               #
#                                                                          #
############################################################################

proc GeneralSwitchVer {} {
    set ver 1.3
    LogFile "GeneralSwitch version $ver"
    return "$ver"
}

proc FindMin {list} {
    set min ""
    foreach num $list {
        if {$num < $min || $min == ""} {
            set min $num
        }
    }
    return $min
}


proc FindMax {list} {
    set max ""
    foreach num $list {
        if {$num > $max || $max == ""} {
            set max $num
        }
    }
    return $max
}


############################################################################
#  Procedure HexToBinary converts a hexidecimal number to a bitstring      #
#  which is then returned.                                                 #
#                                                                          #
#  Variables                                                               #
#    IN:                                                                   #
#         hexNum:       Hexidecimal number                                 #
#                                                                          #
#    OUT:                                                                  #
#         Function returns the binary representation of the hex number     #
#                                                                          #
#  Limitations:  There is no error checking to ensure that the number is   #
#                hex.                                                      #
#                                                                          #
#  Bugs:  None known.                                                      #
#                                                                          #
############################################################################

proc HexToBinary {hexNum} {
    set len [string length $hexNum]
    for {set i 0} {$i < $len} {incr i} {
        set digit [string index $hexNum $i]
        set digit [expr 0x$digit + 0x0]
        if {$digit >= 8} {
            append bitArray 1
            set digit [expr $digit - 8]
        } else {
            append bitArray 0
        }
        if {$digit >= 4} {
            append bitArray 1
            set digit [expr $digit - 4]
        } else {
            append bitArray 0
        }
        if {$digit >= 2} {
            append bitArray 1
            set digit [expr $digit - 2]
        } else {
            append bitArray 0
        }
        if {$digit == 1} {
            append bitArray 1
        } else {
            append bitArray 0
        }
    }
    return $bitArray
}


############################################################################
#  Procedure DecToHex converts a decimal number to a hexidecimal number    #
#  which is then returned.                                                 #
#                                                                          #
#  Variables                                                               #
#    IN:                                                                   #
#         decNum:       Decimal number to be converted                     #
#                                                                          #
#    OUT:                                                                  #
#         Function returns the hexidecimal representation of the decimal   #
#         number.                                                          #
#                                                                          #
#  Limitations:  There is no error checking to ensure that the number is   #
#                decimal.                                                  #
#                                                                          #
#  Bugs:  None known.                                                      #
#                                                                          #
############################################################################

proc DecToHex {decNum} {
    set base $decNum
    set hex ""
    while {$base > 15} {
        set base [expr $decNum / 16]
        append hex [DecToHex [expr $decNum - ($base * 16)]]
        set decNum $base
    }
    if {$base < 10} {
        return $base$hex
    } else {
        switch $base {
            10 { return A$hex }
            11 { return B$hex }
            12 { return C$hex }
            13 { return D$hex }
            14 { return E$hex }
            15 { return F$hex }
        }
    }
}


############################################################################
#  Procedure DecToBinary converts a decimal number to a binary number      #
#  which is then returned.                                                 #
#                                                                          #
#  Variables                                                               #
#    IN:                                                                   #
#         decNum:       Decimal number to be converted                     #
#                                                                          #
#    OUT:                                                                  #
#         Function returns the binary representation of the decimal        #
#         number.                                                          #
#                                                                          #
#  Limitations:  There is no error checking to ensure that the number is   #
#                decimal.                                                  #
#                                                                          #
#  Bugs:  None known.                                                      #
#                                                                          #
############################################################################

proc DecToBinary {decNum} {
    set exp 2
    set bin ""
    while {$exp <= $decNum} {
        set exp [expr $exp * 2]
    }
    set exp [expr $exp / 2]
    while {$exp > 0} {
        if {[expr $decNum - $exp] >= 0} {
            append bin 1
            set decNum [expr $decNum - $exp]
        } else {
            append bin 0
        }
        set exp [expr $exp / 2]
    }
    return $bin
}


############################################################################
#  Procedure BinaryToDec converts a binary number to a decimal number      #
#  which is then returned.                                                 #
#                                                                          #
#  Variables                                                               #
#    IN:                                                                   #
#         binNum:       Binary number to be converted                      #
#                                                                          #
#    OUT:                                                                  #
#         Function returns the decimal representation of the binary        #
#         number.                                                          #
#                                                                          #
#  Limitations:  There is no error checking to ensure that the number is   #
#                binary.                                                   #
#                                                                          #
#  Bugs:  None known.                                                      #
#                                                                          #
############################################################################

proc BinaryToDec {binNum} {
    set len [expr [string length $binNum] - 1]
    set decNum 0
    set index 0
    for {set index 0} {$index < $len} {incr index} {
        set decNum [expr ([string index $binNum $index] * 2) + ($decNum * 2)]
    }
    set decNum [expr [string index $binNum $index] + $decNum]
    return $decNum
}

############################################################################
#  Procedure HexToDec converts a hexidecimal number to a decimal number    #
#  which is then returned.                                                 #
#                                                                          #
#  Variables                                                               #
#    IN:                                                                   #
#         digit:        Hexidecimal number to be converted                 #
#                                                                          #
#    OUT:                                                                  #
#         Function returns the decimal representation of the hex number.   #
#                                                                          #
#  Limitations:  There is no error checking to ensure that the number is   #
#                hex.                                                      #
#                                                                          #
#  Bugs:  None known.                                                      #
#                                                                          #
############################################################################

proc HexToDec {hexNum} {
    set hexNum [string toupper $hexNum]
    set len [string length $hexNum]
    set count 0
    set total 0
    while {$count < $len} {
        set hexDigit [string index $hexNum $count]
        switch $hexDigit {
            A { set hexDigit 10 }
            B { set hexDigit 11 }
            C { set hexDigit 12 }
            D { set hexDigit 13 }
            E { set hexDigit 14 }
            F { set hexDigit 15 }
        }
        set total [expr ($total * 16) + $hexDigit]
        incr count
    }
    return $total
}


############################################################################
#  Procedure OctetToBitString converts an octet string (FF:FC:35:...) to a #
#  binary bit string which is then returned.                               #
#                                                                          #
#  Variables                                                               #
#    IN:                                                                   #
#         digit:        Hexidecimal number to be converted                 #
#                                                                          #
#    OUT:                                                                  #
#         Function returns the binary bit string representation of the     #
#         octet.                                                           #
#                                                                          #
#  Limitations:  There is no error checking to ensure that the input is in #
#                the correct octet format.                                 #
#                                                                          #
#  Bugs:  None known.                                                      #
#                                                                          #
############################################################################

proc OctetToBitString {octetString} {
    set len [string length $octetString]
    set i 0
    set bitString ""
    while {$i < $len} {
        append bitString [HexToBinary [string index $octetString $i]]
        incr i 1
        append bitString [HexToBinary [string index $octetString $i]]
        incr i 2
    }
    return $bitString
}


############################################################################
#  Procedure BitStringToOctet converts a binary bit string to an octet     #
#  string (FF:FC:35:...) which is then returned.                           #
#                                                                          #
#  Variables                                                               #
#    IN:                                                                   #
#         bitString:    Binary bit string to be converted                  #
#                                                                          #
#    OUT:                                                                  #
#         Function returns the octet representation of the bit string      #
#                                                                          #
#  Limitations:  There is no error checking to ensure that the input is in #
#                the correct bit string format.                            #
#                                                                          #
#  Bugs:  None known.                                                      #
#                                                                          #
############################################################################

proc BitStringToOctet {bitString} {
    set index 0
    set len [string length $bitString]
    while {$index < $len} {
        append octet [Convert4BitsToOctet $bitString $index]
        set index [expr $index + 4]
        append octet [Convert4BitsToOctet $bitString $index]
        set index [expr $index + 4]
        if {$index < $len} {
            append octet :
        }
    }
    return $octet
}


############################################################################
#  Procedure Convert4BitsToOctet converts four bits of a binary bit string #
#  to an octet digit which is then returned.                               #
#                                                                          #
#  Variables                                                               #
#    IN:                                                                   #
#         bitString:    Binary bit string to be converted                  #
#         index:        Integer index specifying the starting bit of the   #
#                       four bits to be converted                          #
#                                                                          #
#    OUT:                                                                  #
#         Function returns the octet digit of the four bits                #
#                                                                          #
#  Limitations:  There is no error checking to ensure that the input is in #
#                the correct bit string format.                            #
#                                                                          #
#  Bugs:  None known.                                                      #
#                                                                          #
############################################################################

proc Convert4BitsToOctet {bitString index} {
    set sum 0
    if {[string index $bitString $index] == 1} {
        set sum [expr $sum + 8]
    }
    if {[string index $bitString [expr $index + 1]] == 1} {
        set sum [expr $sum + 4]
    }
    if {[string index $bitString [expr $index + 2]] == 1} {
        set sum [expr $sum + 2]
    }
    if {[string index $bitString [expr $index + 3]] == 1} {
        set sum [expr $sum + 1]
    }
    if {$sum < 10} {
        return $sum
    } else {
        switch $sum {
            10 { return A }
            11 { return B }
            12 { return C }
            13 { return D }
            14 { return E }
            15 { return F }
        }
    }
}


############################################################################
#  Procedure FormatHex takes in a hex number less than FFFF and converts   #
#  it to the format FF:FF.  The result is then returned.                   #
#                                                                          #
#  Variables                                                               #
#    IN:                                                                   #
#         hexNum:       Hexidecimal number to be formatted                 #
#                                                                          #
#    OUT:                                                                  #
#         Function returns the formatted version of the hex number.        #
#                                                                          #
#  Limitations:  There is no error checking to ensure that the input is a  #
#                hexidecimal number less than FFFF.                        #
#                                                                          #
#  Bugs:  None known.                                                      #
#                                                                          #
############################################################################

proc FormatHex {hexNum} {
    if {[string length $hexNum] == 4} {
        return "[string range $hexNum 0 1]:[string range $hexNum 2 3]"
    } elseif {[string length $hexNum] == 3} {
        return "0[string range $hexNum 0 0]:[string range $hexNum 1 2]"
    } elseif {[string length $hexNum] == 2} {
        return "00:$hexNum"
    } elseif {[string length $hexNum] == 1} {
        return "00:0$hexNum"
    } else {
        return ERROR
    }
}

############################################################################
#  Procedure ASCIIToHex takes a text in ACSII format and converts          #
#  every character in hex format. The result is then returned in a list.   #                                                                          #
#  Variables                                                               #
#    IN:                                                                   #
#         Text:   text to be formatted                                     #
#                                                                          #
#    OUT:                                                                  #
#         Function returns a list with the caracters formatted             #
#         in the hex numbers.                                              #
#                                                                          #
#  Bugs:  None known.                                                      #
#                                                                          #
############################################################################
proc ASCIIToHex {text} {
   set index 0
   set hexValue ""
   while { $index != [string length $text] } {
      scan [string index $text $index] %c dec
      lappend hexValue [format %x $dec]
      incr index
   }
   return $hexValue
}


############################################################################
#  Procedure ConvertPortsToOctet converts a list of ports in 8600 format   #
#  to an octet format that the mibs will accept.  This function only works #
#  on 8600 ports.                                                          #
#                                                                          #
#  Variables                                                               #
#    IN:                                                                   #
#         portList:     Integer specifying a single port, or a string list #
#                       of ports of the form x-y where 'x' is the low port #
#                       and 'y' is the high port and all ports between 'x' #
#                       and 'y' are to be included.                        # 
#                                                                          #
#    OUT:                                                                  #
#         Function returns the octet version of the port list.             #
#                                                                          #
#  Limitations:  There is no error checking to ensure that the input is a  #
#                list of valid 8600 ports.                                 #
#                                                                          #
#  Bugs:  None known.                                                      #
#                                                                          #
############################################################################

proc ConvertPortsToOctet {portList host} {
    set base 00:00:00:00:00:00:00:00:
    if {[string match "*-*" $portList] == 1} {
        set portLow [lindex [split $portList -] 0]
        set portHigh [lindex [split $portList -] 1]
    } else {
        set portLow $portList
        set portHigh $portList
    }

    set card [lindex [split $portLow "/"] 0]
    set portInCard [lindex [split $portLow "/"] 1]
    # Add blank octets for all the cards that are higher than the destination card
    for {set i 0} {$i < $card} {incr i} {
        append octet $base
    }
    # Add blank octets for all the ports that are before destination port
    for {set i 1} {$i < $portInCard} {incr i} {
        append bitString 0
    }
    # For single port case, append the bit to the string and return
    if {$portLow == $portHigh} {
        append bitString 1
    } else {
        set endCard [lindex [split $portHigh "/"] 0]
        set endPortInCard [lindex [split $portHigh "/"] 1]
        while {$card <= $endCard} {
            set endPort [GetNumPortsInCard $card $host]
            if {$endPortInCard < $endPort && $card == $endCard} {
                set endPort $endPortInCard
            }
            for {set i $portInCard} {$i <= $endPort} {incr i} {
                append bitString 1
            }
            if {$card != $endCard} {
                # Fill in 0's to fill up the rest of the 64 virtual ports on the card
                for {set i $endPort} {$i < 64} {incr i} {
                    append bitString 0
                }
                set portInCard 1
            }
            incr card
        }
    }
    append octet [BitStringToOctet $bitString]
    return $octet
}


############################################################################
#  Procedure AddOctets does a logical OR with two octet strings.  This     #
#  is used to add values of one octet the another octet.  The resulting    #
#  "sum" is returned.                                                      #
#                                                                          #
#  Variables                                                               #
#    IN:                                                                   #
#         octet1/2:     Octet strings to be added together.                #
#                                                                          #
#    OUT:                                                                  #
#         Function returns the octet sum.                                  #
#                                                                          #
#  Limitations:  There is no error checking to ensure that the octet       #
#                strings are valid.                                        #
#                                                                          #
#  Bugs:  None known.                                                      #
#                                                                          #
############################################################################

proc AddOctets {octet1 octet2} {
    if {$octet1 == ""} {
        return $octet2
    }
    set bitString1 [OctetToBitString $octet1]
    set bitString2 [OctetToBitString $octet2]
    set len [string length $bitString1]
    if {[string length $bitString2] > $len} {
        set len [string length $bitString2]
    }
    set i 0
    while {$i < $len} {
        set digit [string index $bitString1 $i]
        if {[string index $bitString1 $i] == "1" || [string index $bitString2 $i] == "1"} {
            append mergeString 1
        } else {
            append mergeString 0
        }
        incr i
    }
    set octet [BitStringToOctet $mergeString]
    return $octet
}


############################################################################
#  Procedure SubtractOctets does a subtraction of octet2 from octet1.      #
#  The resulting octet difference is returned.                             #
#                                                                          #
#  Variables                                                               #
#    IN:                                                                   #
#         octet1:       Octet string                                       #
#         octet2:       Octet string to be subtracted from octet1          #
#                                                                          #
#    OUT:                                                                  #
#         Function returns the octet difference of octet1 - octet2         #
#                                                                          #
#  Limitations:  There is no error checking to ensure that the octet       #
#                strings are valid.                                        #
#                                                                          #
#  Bugs:  None known.                                                      #
#                                                                          #
############################################################################

proc SubtractOctets {octet1 octet2} {
    set bitString1 [OctetToBitString $octet1]
    set bitString2 [OctetToBitString $octet2]
    set len [string length $bitString1]
    if {[string length $bitString2] > $len} {
        set len [string length $bitString2]
    }
    set i 0
    while {$i < $len} {
        set digit [string index $bitString1 $i]
        if {[string index $bitString2 $i] == "1"} {
            append mergeString 0
        } else {
            append mergeString [string index $bitString1 $i]
        }
        incr i
    }
    set octet [BitStringToOctet $mergeString]
    return $octet
}


############################################################################
#  Procedure DecodeOctet8600 converts an octet string into a port list     #
#  using the 8600 port format (blade/port).  The resulting port list is    #
#  returned.                                                               #
#                                                                          #
#  Variables                                                               #
#    IN:                                                                   #
#         octetString:  Octet string to be converted to a port list        #
#                                                                          #
#    OUT:                                                                  #
#         Function returns the port list resulting from the octet string   #
#                                                                          #
#  Limitations:  There is no error checking to ensure that the octet       #
#                string is valid.                                          #
#                                                                          #
#  Bugs:  None known.                                                      #
#                                                                          #
############################################################################

proc DecodeOctet8600 {octetString} {
    set bitString [OctetToBitString $octetString]
    set len [string length $bitString]
    set bitString [string range $bitString 64 [expr $len - 1]]
    set len [string length $bitString]
    set card 1
    set returnString ""
    while {$len > 0} {
        set tempBitString [string range $bitString 0 63]
        set cardResult [Collect1Indices $tempBitString]
        if {$cardResult != "NONE"} {
            set tempReturnString [Collect1Indices $tempBitString "$card/"]
            if {[string index $returnString [expr [string length $returnString] - 1]] != "," && [string length $returnString] > 0} {
                append returnString ","
            }
            append returnString $tempReturnString
        }
        set bitString [string range $bitString 64 [expr $len - 1]]
        set len [string length $bitString]
        incr card
    }
    if {$returnString == ""} {
        return NONE
    }
    return $returnString
}


############################################################################
#  Procedure DecodeOctet converts an octet string into a number list which #
#  is returned.  For some MIB functions, certain bits of an octet are      #
#  reserved or are not used.  For these cases, the optional variable,      #
#  omitFirstNBits, is set to the number of high-order bits to be excluded. #
#                                                                          #
#  Variables                                                               #
#    IN:                                                                   #
#         octetString:    Octet string to be converted to a port list      #
#         omitFirstNBits: Integer specifying the number of bits to ignore  #
#                                                                          #
#    OUT:                                                                  #
#         Function returns the number list resulting from the octet string #
#                                                                          #
#  Limitations:  There is no error checking to ensure that the octet       #
#                string is valid.                                          #
#                                                                          #
#  Bugs:  None known.                                                      #
#                                                                          #
############################################################################

proc DecodeOctet {octetString {omitFirstNBits 0}} {
    set bitString [OctetToBitString $octetString]
    set len [string length $bitString]
    set bitString [string range $bitString $omitFirstNBits [expr $len - 1]]
    return [Collect1Indices $bitString]
}


############################################################################
#  Procedure Collect1Indices converts a bit string (ordered low to high)   #
#  into a number list.  The resulting port list is returned.  If the       #
#  "card" variable is set, then the resulting list is formatted to the     #
#  8600 port formatting.                                                   #
#                                                                          #
#  Variables                                                               #
#    IN:                                                                   #
#         bitString:    Bit string to be converted to a number list        #
#         card:         Integer specifying the card to be prepended to the #
#                       values of the list to conform to the 8600 port     #
#                       format.                                            #
#                                                                          #
#    OUT:                                                                  #
#         Function returns the list resulting from the bit string          #
#                                                                          #
#  Limitations:  There is no error checking to ensure that the bit         #
#                string is valid.                                          #
#                                                                          #
#  Bugs:  None known.                                                      #
#                                                                          #
############################################################################

proc Collect1Indices {bitString {card ""}} {
    set len [string length $bitString]
    set dashSet FALSE
    set lastWasGood FALSE
    set firstTime TRUE
    for {set i 0} {$i < $len} {incr i 1} {
        if {[string index $bitString $i] == 1} {
            if {$lastWasGood == "TRUE"} {
                set dashSet TRUE
            } else {
                if {$firstTime == "TRUE"} {
                    append portList $card[expr $i + 1]
                    set firstTime FALSE
                } else {
                    append portList ","
                    append portList $card[expr $i + 1]
                }
                set lastWasGood TRUE
            }
        } elseif {$dashSet == "TRUE"} {
            append portList "-"
            append portList $card$i
            set lastWasGood FALSE
            set dashSet FALSE
        } elseif {$lastWasGood == "TRUE"} {
            set lastWasGood FALSE
        }
    }
    if {$dashSet == "TRUE"} {
        append portList "-"
        append portList $card$i
    }
    if {[info exists portList] == 0} {
        return NONE
    }
    return $portList
}


############################################################################
#  Procedure CreateListFromTCLList converts a TCL style list of numbers    #
#  into a consolidated list (ex. 1-5,8,10).  The TCL style list passed in  #
#  must be sorted in order for the conversion to be most effective.        #
#                                                                          #
#  Variables                                                               #
#    IN:                                                                   #
#         tclList:      TCL list of sorted numbers to convert              #
#                                                                          #
#    OUT:                                                                  #
#         Function returns the converted list.                             #
#                                                                          #
#  Bugs:  None known.                                                      #
#                                                                          #
############################################################################

proc CreateListFromTCLList {tclList} {
    if {$tclList == ""} {
        return NONE
    }
    set dashSet FALSE
    set resultList [lindex $tclList 0]
    set len [llength $tclList]
    set i 1
    while {$i < $len} {
        if {[expr [lindex $tclList [expr $i - 1]] + 1] == [lindex $tclList $i] && $dashSet == "FALSE"} {
            append resultList -
            set dashSet TRUE
        } elseif {[expr [lindex $tclList [expr $i - 1]] + 1] < [lindex $tclList $i] && $dashSet == "TRUE"} {
            append resultList "[lindex $tclList [expr $i - 1]],[lindex $tclList $i]"
            set dashSet FALSE
        } elseif {$dashSet == "FALSE"} {
            append resultList ",[lindex $tclList $i]"
        }
        incr i
    }
    if {$dashSet == "TRUE"} {
        append resultList "[lindex $tclList [expr $i - 1]]"
    }
    return $resultList
}


############################################################################
#  Procedure IsNumInList checks to determine whether the given number is   #
#  included in the given list.  The list can be a TCL list, or a list of   #
#  numbers containing '-' and/or ',' characters.  If the number is in the  #
#  list, TRUE is returned.  Otherwise, FALSE is returned.                  #
#                                                                          #
#  Variables                                                               #
#    IN:                                                                   #
#         num:          Integer to search for                              #
#         list:         List string in which to search                     #
#                                                                          #
#    OUT:                                                                  #
#         Function returns TRUE or FALSE depending on whether the integer  #
#         was found in the list or not.                                    #
#                                                                          #
#  Bugs:  None known.                                                      #
#                                                                          #
############################################################################

proc IsNumInList {num list} {
    set list [ExpandList $list]
    foreach item $list {
        if {$item == $num} {
            return TRUE
        }
    }
    return FALSE
}


############################################################################
#  Procedure ExpandList takes a list of numbers with ',' and '-' and       #
#  expands it into a TCL list of all the numbers in the given list.        #
#                                                                          #
#  Variables                                                               #
#    IN:                                                                   #
#         list:         List string in which to search                     #
#                                                                          #
#    OUT:                                                                  #
#         Function returns the TCL list of all numbers in the original     #
#         list.  (Ex.  1-4,6 returns 1 2 3 4 6)                            #
#                                                                          #
#  Bugs:  Not compatible with 8600 port format yet.                        #
#                                                                          #
############################################################################

proc ExpandList {list} {
    set tclList ""
    foreach sublist $list {
        set splitList [split $sublist ,]
        foreach item $splitList {
            if {[string match "*-*" $item] == 1} {
                if {[string match "*/*" [lindex [split $item -] 0]] == 1} {
                    set card [lindex [split [lindex [split $item -] 0] "/"] 0]
                    set startPort [lindex [split [lindex [split $item -] 0] "/"] 1]
                    set endPort [lindex [split [lindex [split $item -] 1] "/"] 1]
                    for {set i $startPort} {$i <= $endPort} {incr i} {
                        lappend tclList "$card/$i"
                    }
                } else {
                    for {set i [lindex [split $item -] 0]} {$i <= [lindex [split $item -] 1]} {incr i} {
                        lappend tclList $i
                    }
                }
            } else {
                lappend tclList $item
            }
        }
    }
    return $tclList
}


############################################################################
#  Procedure MyPing will execute "ping" to the given host IP address and   #
#  will parse the results to determine whether the ping was received or    #
#  not.  If the host is alive, TRUE is returned, otherwise, FALSE is       #
#  returned.                                                               #
#                                                                          #
#  Variables                                                               #
#    IN:                                                                   #
#         host:         IP address to ping                                 #
#         count:        Integer specifying the number of pings to send     #
#                                                                          #
#    OUT:                                                                  #
#         Function returns TRUE or FALSE depending on whether the host     #
#         responded to pings or not.                                       #
#                                                                          #
#  Bugs:  None known.                                                      #
#                                                                          #
############################################################################

proc MyPing {host {count 1}} {
    if {$count < 1} {
        set count 1
    }
    #   catch {Icmp -delay 1 -retries 1 -timeout 1 echo $host} result 
    #   if {[lindex [lindex $result 0] 1] >= 0} {
    #      return TRUE
    #   } else {
    #      return FALSE
    #   }
    catch {exec ping $host -c 1 -w 1} result
    if {[regexp {transmitted, ([1]+)} $result] == 1} {
        return TRUE
    } else {
        return FALSE
    }
}


############################################################################
#  Procedure MyTraceRoute will execute "traceroute" to the given host IP   #
#  address and will parse the results to determine whether the given route #
#  was traversed.  If the route was used, TRUE is returned, otherwise,     #
#  FALSE is returned.                                                      #
#                                                                          #
#  Variables                                                               #
#    IN:                                                                   #
#         host:         IP address to ping                                 #
#         count:        Integer specifying the number of pings to send     #
#                                                                          #
#    OUT:                                                                  #
#         Function returns TRUE or FALSE depending on whether the route    #
#         was used or not.                                                 #
#                                                                          #
#  Limitations:  This function may break depending on the output of        #
#                traceroute on different Linux/Unix platforms.             #
#                                                                          #
#  Bugs:  None known.                                                      #
#                                                                          #
############################################################################

proc MyTraceRoute {route host} {
    catch {exec traceroute -w 2 -m 4 $host} string
    if {[regexp {(\*)} $string] == 1} {
        return "FALSE"
    }
    if {[string match "*$route*" $string] == 1} {
        return "TRUE"
    } else {
        return "FALSE"
    }
}



############################################################################
#  Procedure LinuxGetHostByName returns a list of IP addresses configured  #
#  on the local machine.  If the current user doesn't have rights to run   #
#  ifconfig, the error ERRORBADRIGHTS is returned.                         #
#                                                                          #
#  Variables                                                               #
#    IN:                                                                   #
#                                                                          #
#    OUT:                                                                  #
#         Function returns a list of IPs.  No variables are modified.      #
#                                                                          #
#  Bugs:  None known.                                                      #
#                                                                          #
############################################################################

proc LinuxGetHostByName {} {
    set ipList ""
    set intfList [LinuxGetConfiguredInterfaces]
    if {$intfList == "ERRORBADRIGHTS"} {
        return $intfList
    }

    foreach intf $intfList {
        set result [LinuxGetInterfaceIP $intf]
        if {$result != "NOTCONFIGURED" && $result != "ERRORBADRIGHTS"} {
            lappend ipList $result
        }
    }
    return $ipList
}


############################################################################
#  Procedure LinuxGetIPIntf returns the local interface name of the IP     #
#  address on the local machine.  If the current user doesn't have rights  #
#  to run ifconfig, the error ERRORBADRIGHTS is returned.  If the IP       #
#  address isn't found, NOTFOUND is returned.                              #
#                                                                          #
#  Variables                                                               #
#    IN:                                                                   #
#         ipAddrToFind: IP address to find                                 #
#                                                                          #
#    OUT:                                                                  #
#         Function returns the interface name (ex eth0).  No variables are #
#         modified.                                                        #
#                                                                          #
#  Bugs:  None known.                                                      #
#                                                                          #
############################################################################

proc LinuxGetIPIntf {ipAddrToFind} {
    set intfList [LinuxGetConfiguredInterfaces]
    if {$intfList == "ERRORBADRIGHTS"} {
        return $intfList
    }
    foreach intf $intfList {
        set result [LinuxGetInterfaceIP $intf]
        if {$result != "NOTCONFIGURED" && $result != "ERRORBADRIGHTS"} {
            if {$result == $ipAddrToFind} {
                return $intf
            }
        }
    }
    return NOTFOUND
}


############################################################################
#  Procedure LinuxRemoveIF will attempt to remove the IP address from the  #
#  local machine configuration.  If the current user doesn't have rights   #
#  to run ifconfig, the error ERRORBADRIGHTS is returned.  If the IP       #
#  address was successfully removed, SUCCESS is returned, otherwise ERROR. #
#                                                                          #
#  Variables                                                               #
#    IN:                                                                   #
#         ipAddr:       IP address to remove                               #
#                                                                          #
#    OUT:                                                                  #
#         Function returns SUCCESS or "ERR*".  No variables are modified.  #
#                                                                          #
#  Bugs:  None known.                                                      #
#                                                                          #
############################################################################
proc LinuxRemoveIF {ipAddr} {
    set intf [LinuxGetIPIntf $ipAddr]
    if {$intf == "NOTFOUND"} {
        return SUCCESS
    } elseif {$intf == "ERRORBADRIGHTS"} {
        return $intf
    }
    catch {exec ifconfig $intf down} err
    if {$err == ""} {
        return SUCCESS
    } else {
        return ERROR
    }
}


############################################################################
#  Procedure LinuxAddIF will attempt to add the IP address to the local    #
#  machine configuration.  By default, the address will be added to eth0,  #
#  but the interface card can be specified in the "card" variable.  If the #
#  address was successfully added, SUCCESS is returned, otherwise ERROR.   #
#                                                                          #
#  Variables                                                               #
#    IN:                                                                   #
#         ipAddr:       IP address to add to the local Linux configuration #
#         card:         Integer specifying the interface card to add the   #
#                       IP address to                                      #
#                                                                          #
#    OUT:                                                                  #
#         Function returns SUCCESS or "ERR*".  No variables are modified.  #
#                                                                          #
#  Bugs:  None known.                                                      #
#                                                                          #
############################################################################
proc LinuxAddIF {ipAddr {card 0}} {

    set rcode [CheckIP $ipAddr mask broad]
    if {$rcode != "SUCCESS"} {
        return "ERRORBADIPADDR"
    }

    set cardDone FALSE
    set intf 0
    set intfDone FALSE
    while {$cardDone == "FALSE"} {
        set result [LinuxGetInterfaceIP eth$card]
        if {$result == "NOTCONFIGURED"} {
            set cardDone TRUE
        }
        while {$cardDone == "FALSE" && $intfDone == "FALSE"} {
            set result [LinuxGetInterfaceIP eth$card:$intf]
            if {$result == "NOTCONFIGURED"} {
                set intfDone TRUE
                set cardDone TRUE
            } else {
                set intf [expr $intf + 1]
            }
        }
    }

    catch {exec ifconfig eth$card:$intf $ipAddr broadcast $broad netmask $mask} err
    if {$err == ""} {
        return SUCCESS
    } else {
        return ERROR
    }
}


############################################################################
#  Procedure LinuxReplaceIF will attempt to replace the IP address of the  #
#  specified local interface.  If the address was successfully replaced,   #
#  SUCCESS is returned, otherwise ERROR.                                   #
#                                                                          #
#  Variables                                                               #
#    IN:                                                                   #
#         ipAddr:       IP address to add to the local Linux configuration #
#         intf:         Interface with the address to replace (ie eth0:0)  #
#         card:         Integer specifying the interface card to add the   #
#                       IP address to                                      #
#                                                                          #
#    OUT:                                                                  #
#         Function returns SUCCESS or "ERR*".  No variables are modified.  #
#                                                                          #
#  Bugs:  None known.                                                      #
#                                                                          #
############################################################################
proc LinuxReplaceIF {ipAddr intf {card 0}} {

    set rcode [CheckIP $ipAddr mask broad]
    if {$rcode != "SUCCESS"} {
        return "ERRORBADIPADDR"
    }

    set result [LinuxGetInterfaceIP $intf]
    if {$result == "NOTCONFIGURED"} {
        return ERRORNOTCONFIGURED
    }

    catch {exec ifconfig $intf $ipAddr broadcast $broad netmask $mask} err
    if {$err == ""} {
        return SUCCESS
    } else {
        return ERROR
    }
}


############################################################################
#  Procedure LinuxGetConfiguredInterfaces returns a list of interfaces     #
#  that are configured on the local Linux machines.  If the current user   #
#  doesn't have rights to run ifconfig, the error ERRORBADRIGHTS is        #
#  returned.                                                               #
#                                                                          #
#  Variables                                                               #
#    IN:                                                                   #
#                                                                          #
#    OUT:                                                                  #
#         Function returns a list of interfaces or ERRORBADRIGHTS.  No     #
#         variables are modified.                                          #
#                                                                          #
#  Bugs:  None known.                                                      #
#                                                                          #
############################################################################
proc LinuxGetConfiguredInterfaces {} {
    catch {exec ifconfig | grep eth} result
    if {[string match "*no such file or directory" $result] == 1} {
        return ERRORBADRIGHTS
    }
    set lines [split $result "\n"]
    set len [llength $lines]
    for {set i 0} {$i < $len} {incr i} {
        lappend intf [lindex [lindex $lines $i] 0]
    }
    return $intf
} 


############################################################################
#  Procedure LinuxGetInterfaceIP will return the IP address associated     #
#  with the local interface given.  If the current user doesn't have       #
#  rights to run ifconfig, the error ERRORBADRIGHTS is returned.  If the   #
#  interface given isn't configured, NOTCONFIGURED is returned.            #
#                                                                          #
#  Variables                                                               #
#    IN:                                                                   #
#         intf:         Interface of the local Linux machine               #
#                                                                          #
#    OUT:                                                                  #
#         Function returns the IP address of the given interface,          #
#         ERRORBADRIGHTS, or NOTCONFIGURED.  No variables are modified.    #
#                                                                          #
#  Bugs:  None known.                                                      #
#                                                                          #
############################################################################
proc LinuxGetInterfaceIP {intf} {
    catch {exec ifconfig $intf} result
    if {[string match "*no such file or directory" $result] == 1} {
        return ERRORBADRIGHTS
    }
    set match ""
    regexp {addr:[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+} $result match
    if {$match != ""} {
        set ipAddr [lindex [split $match :] 1]
        return $ipAddr
    }
    return NOTCONFIGURED
}

############################################################################
#  Procedure LinuxGetInterfaceMask will return the IP mask associated      #
#  with the local interface given.  If the current user doesn't have       #
#  rights to run ifconfig, the error ERRORBADRIGHTS is returned.  If the   #
#  interface given isn't configured, NOTCONFIGURED is returned.            #
#                                                                          #
#  Variables                                                               #
#    IN:                                                                   #
#         intf:         Interface of the local Linux machine               #
#                                                                          #
#    OUT:                                                                  #
#         Function returns the IP mask of the given interface,             #
#         ERRORBADRIGHTS, or NOTCONFIGURED.  No variables are modified.    #
#                                                                          #
#  Bugs:  None known.                                                      #
#                                                                          #
############################################################################
proc LinuxGetInterfaceMask {intf} {
    catch {exec ifconfig $intf} result
    if {[string match "*no such file or directory" $result] == 1} {
        return ERRORBADRIGHTS
    }
    set match ""
    regexp -nocase {mask:[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+} $result match
    if {$match != ""} {
        set ipMask [lindex [split $match :] 1]
        return $ipMask
    }
    return NOTCONFIGURED
}


############################################################################
#  Procedure LinuxFindLocalSameNetIP will attempt to find an IP address    #
#  configured on the local Linux machine that is on the same IP network as #
#  the given IP address.  If an IP address is found on the local machine   #
#  that is on the same network as the given IP address, the local IP       #
#  address is returned.  Otherwise, NOTFOUND is returned.                  #
#                                                                          #
#  Variables                                                               #
#    IN:                                                                   #
#         IPAddr:       IP address used to compare against local IP        #
#                       addresses                                          #
#                                                                          #
#    OUT:                                                                  #
#         Function returns the IP address of the local machine that is on  #
#         the same network as the given IP address or NOTFOUND.  No        #
#         variables are modified.                                          #
#                                                                          #
#  Bugs:  None known.                                                      #
#                                                                          #
############################################################################
proc LinuxFindLocalSameNetIP {IPAddr} {
    set rcode [CheckIP $IPAddr cmask cbroad]
    if {[string match "*ERR*" $rcode] == 1} {
        return NOTFOUND
    }
    set localIP [LinuxGetHostByName]
    foreach ip $localIP {
        set rcode [CheckIP $ip mask broad]
        if {[string match "*ERR*" $rcode] == 1} {
            return NOTFOUND
        }
        if {$cbroad == $broad} {
            return $ip
        }
    }
    return NOTFOUND
}


proc LinuxGetDefaultGW {} {
    catch {exec route | grep default} result
    if {[string match "*no such file or directory" $result] == 1} {
        return ERRORBADRIGHTS
    }
    set ipAddr ""
    regexp {[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+} $result ipAddr
    if {$ipAddr != ""} {
        return $ipAddr
    }
    return NOTCONFIGURED
}


proc LinuxSetDefaultGW {ipAddr} {
    catch {exec route add default gw $ipAddr} result
    if {[string match "*no such file or directory" $result] == 1} {
        return ERRORBADRIGHTS
    }
    if {[LinuxGetDefaultGW] == $ipAddr} {
        return SUCCESS
    }
    return ERROR
}


proc LinuxRemoveDefaultGW {} {
    catch {exec route del default} result
    if {[string match "*no such file or directory" $result] == 1} {
        return ERRORBADRIGHTS
    }
    return SUCCESS
}


proc AreIPsOnSameNet {ipAddr1 ipAddr2} {
    set octet1 [lindex [split $ipAddr1 .] 0]
    set octet2 [lindex [split $ipAddr1 .] 1]
    set octet3 [lindex [split $ipAddr1 .] 2]
    set octet4 [lindex [split $ipAddr1 .] 3]
    if {$octet1 < 128} {
        if {$octet1 == [lindex [split $ipAddr2 .] 0]} {
            return TRUE
        }
    } elseif {$octet1 < 192} {
        if {$octet1 == [lindex [split $ipAddr2 .] 0] && \
                $octet2 == [lindex [split $ipAddr2 .] 1]} {
            return TRUE
        }
    } elseif {$octet1 < 224} {
        if {$octet1 == [lindex [split $ipAddr2 .] 0] && \
                $octet2 == [lindex [split $ipAddr2 .] 1] && \
                $octet3 == [lindex [split $ipAddr2 .] 2]} {
            return TRUE
        }
    } else {
        return ERROR
    }
    return FALSE
}


###############################
#  Get the mask and broadcast #
#  address of the given ip    #
#  address.  Function returns #
#  "ERRORBADIP" if the IP     #
#  address is invalid.        #
#  Otherwise, "SUCCESS" is    #
#  returned.                  #
###############################
proc {CheckIP} {ipAddr {msk NULL} {bcst NULL}} {
    if {$msk != "NULL"} {
        upvar $msk mask
    }
    if {$bcst != "NULL"} {
        upvar $bcst bcast
    }

    set o1 [lindex [split $ipAddr .] 0]
    set o2 [lindex [split $ipAddr .] 1]
    set o3 [lindex [split $ipAddr .] 2]
    set o4 [lindex [split $ipAddr .] 3]

    if {$o1 < 1 || $o1 > 254} {
        return ERRORBADIP
    }
    if {$o2 < 0 || $o2 > 254} {
        return ERRORBADIP
    }
    if {$o3 < 0 || $o3 > 254} {
        return ERRORBADIP
    }
    if {$o4 < 1 || $o4 > 254} {
        return ERRORBADIP
    }
    if {$o1 < 128} {
        set class A
        set mask 255.0.0.0
        set bcast $o1.255.255.255
    } elseif {$o1 < 192} {
        set class B
        set mask 255.255.0.0
        set bcast $o1.$o2.255.255
    } elseif {$o1 < 224} {
        set class C
        set mask 255.255.255.0
        set bcast $o1.$o2.$o3.255
    } else {
        set class D
        return ERRORBADIP
    }
    return SUCCESS
}


proc {IncrHost} {ipAddr {num 1}} {
    if {$num == 0} {
        return $ipAddr
    }

    set oct1 [lindex [split $ipAddr .] 0]
    set oct2 [lindex [split $ipAddr .] 1]
    set oct3 [lindex [split $ipAddr .] 2]
    set oct4 [lindex [split $ipAddr .] 3]
    if {[expr $oct4 + $num] < 0} {
        # if $num is negative, oct4 + num could be less than zero
        set oct4ovrflow [expr (((($oct4 + $num) * -1) / 255) + 1) * -1]
    } else {
        set oct4ovrflow [expr ($oct4 + $num) / 255]
    }
    # add 255 in case $num is negative, mod 255 to eliminate the broadcast address
    set oct4 [expr ($oct4 + $num + 255) % 255]
    # Since .0 is not a legal host address, take care of the case where the mod result is 0
    if {$oct4ovrflow != 0 || $oct4 == 0} {
        if {$oct4 == 0} {
            if {$num < 0} {
                set oct4 254
                set oct4ovrflow [expr $oct4ovrflow - 1]
            } else {
                set oct4 1
            }
        } else {
            # every time it wraps around, we loose one, so this corrects for that
            set oct4 [expr $oct4 + $oct4ovrflow]
        }
    }
    if {[expr $oct3 + $oct4ovrflow] < 0} {
        set oct3ovrflow [expr (((($oct3 + $oct4ovrflow) * -1) / 256) + 1) * -1]
    } else {
        set oct3ovrflow [expr ($oct3 + $oct4ovrflow) / 256]
    }
    set oct3 [expr ($oct3 + $oct4ovrflow + 256) % 256]
    if {[expr $oct2 + $oct3ovrflow] < 0} {
        set oct2ovrflow [expr (((($oct2 + $oct3ovrflow) * -1) / 256) + 1) * -1]
    } else {
        set oct2ovrflow [expr ($oct2 + $oct3ovrflow) / 256]
    }
    set oct2 [expr ($oct2 + $oct3ovrflow + 256) % 256]
    set oct1 [expr ($oct1 + $oct2ovrflow + 256) % 256]
    set orgOct1 [lindex [split $ipAddr .] 0]
    # Check to see that the resulting host is in the same network
    if {($orgOct1 < 128 && \
             ($oct2ovrflow != 0 || ($oct2 == 255 && $oct3 == 255 && $oct4 == 255) || \
                  ($oct2 == 0 && $oct3 == 0 && $oct4 == 0))) || \
            ($orgOct1 < 192 && $orgOct1 >= 128 && \
                 ($oct3ovrflow != 0 || ($oct3 == 255 && $oct4 == 255) || \
                      ($oct3 == 0 && $oct4 == 0))) || \
            ($orgOct1 < 224 && $orgOct1 >= 192 && \
                 ($oct4ovrflow != 0 || $oct4 == 255 || $oct4 == 0))} {
        return ERROR
    }
    return "$oct1.$oct2.$oct3.$oct4"
}


proc {IncrNet} {ipAddr {num 1} {class NULL}} {
    if {$num == 0} {
        return $ipAddr
    }

    set oct1 [lindex [split $ipAddr .] 0]
    set oct2 [lindex [split $ipAddr .] 1]
    set oct3 [lindex [split $ipAddr .] 2]
    set oct4 [lindex [split $ipAddr .] 3]

    if {$oct1 >= 192 || [string toupper $class] == "C"} {
        set oct4ovrflow $num
        set oct3ovrflow 0
        set oct2ovrflow 0
        set class C
    } elseif {$oct1 >= 128 || [string toupper $class] == "B"} {
        set oct3ovrflow $num
        set oct2ovrflow 0
        set class B
    } elseif {$oct1 >= 1 || [string toupper $class] == "A"} {
        set oct3ovrflow 0
        set oct2ovrflow $num
        set class A
    }

    if {$class == "C"} {
        if {[expr $oct3 + $oct4ovrflow] < 0} {
            set oct3ovrflow [expr (((($oct3 + $oct4ovrflow) * -1) / 256) + 1) * -1]
        } else {
            set oct3ovrflow [expr ($oct3 + $oct4ovrflow) / 256]
        }
        set oct3 [expr ($oct3 + $oct4ovrflow + 256) % 256]
    }

    if {$class == "B" || $oct3ovrflow != 0} {
        if {[expr $oct2 + $oct3ovrflow] < 0} {
            set oct2ovrflow [expr (((($oct2 + $oct3ovrflow) * -1) / 256) + 1) * -1]
        } else {
            set oct2ovrflow [expr ($oct2 + $oct3ovrflow) / 256]
        }
        set oct2 [expr ($oct2 + $oct3ovrflow + 256) % 256]
    }

    set oct1 [expr $oct1 + $oct2ovrflow]
    if {$oct1 > 254 || $oct1 < 1} {
        return ERROR
    }

    return "$oct1.$oct2.$oct3.$oct4"
}


proc {GetRandomIP} {{class C} args} {
    set ipListToAvoid $args
    if {$ipListToAvoid == ""} {
        set ipListToAvoid NULL
    }
    set class [string toupper $class]

    if {$class == "A"} {
        set low 1
        set high 126
    } elseif {$class == "B"} {
        set low 128
        set high 191
    } elseif {$class == "C"} {
        set low 192
        set high 223
    } elseif {$class == "D"} {
        set low 224
        set high 239
    } elseif {$class == "E"} {
        set low 240
        set high 254
    } else {
        return ERROR
    }

    set octet1 [GetRandomInt $low $high]
    set octet2 [GetRandomInt 0 254]
    set octet3 [GetRandomInt 0 254]
    set octet4 [GetRandomInt 1 254]

    if {$ipListToAvoid != "NULL"} {
        foreach ip $ipListToAvoid {
            lappend avoidOctet1 [lindex [split $ip .] 0]
        }
        while {[IsNumInList $octet1 $avoidOctet1] == "TRUE"} {
            set octet1 [GetRandomInt $low $high]
        }
    }

    return $octet1.$octet2.$octet3.$octet4
}


proc {getrandomip} {{class C}} {
    return [GetRandomIP $class]
}


proc GetRandomInt {low high} {
    set num [expr rand() * ($high - $low) + $low]
    set num [expr round($num)]
    return $num
}

proc LogFile {comment {flag false}} {
   global globalLogErrorFlag

   #set flag [string tolower $flag]

   if {[info exists globalLogErrorFlag] != 1} {
      set globalLogErrorFlag 1
   }

   if {[info command logFile] == ""} {
      if {$globalLogErrorFlag == 1} {
         if {$flag == "false"} {
            puts "$comment"
         } elseif {$flag == "ERROR"} {
            puts "ERROR: $comment"
         } else {
            puts "****$flag: $comment"
         }
      }
   } elseif {$globalLogErrorFlag == 1} {

      if {$flag == "false"} {
         #catch {logFile "$comment"} err
         catch {logFile "$comment"}
         logFile "#######    $comment" debug
      } elseif {$flag == "error"} {
         #catch {logFile "$comment" error} err
         catch {logFile "$comment" error color red}
         logFile "#######    ERROR: $comment" debug
      } elseif {[regexp -nocase coredump $flag] && [info command logTest] != ""} {
         # CES project
         # - cip -
         logTest "Core Dump while running the following CLI command:" $comment
      } else {
         logFile "$comment" $flag
      }
   }
}


#############################################################
# FormatMac: Adds first digit 0 where needed in order to set 
#            a MAC address format to XX:XX:XX:XX:XX:XX
#
# IN:  mac_addr
#
# OUT: formated MAC
#############################################################
proc FormatMac {mac_addr} {
   set new_mac ""
   foreach elem [split $mac_addr ":"] {
      if {[string length $elem] == 1} {
         set elem "0$elem"
      }
      append new_mac $elem ":"
   }
   set new_mac [string trimright $new_mac ":"]
   return $new_mac
}
