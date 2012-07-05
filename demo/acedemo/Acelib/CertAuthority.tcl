############################
# Certificate Authority library
#
#  GetServerCertificate { host {CS_id "first"} }
#  GetCACertificate { host {CS_id "first"} }
#  EnterCaLevel { certificate host }
#  EnterCaIdentityLevel { host }
#  EnterServerCertConfLevel { serverCertificate host }
############################


proc GetServerCertificate {host {CS_id "first"}} {
    
    global cmdOut
    set rcode ""

    SetCliLevel "CONFIG" $host

    set execResult [Exec "show crypto server certificates" "CONFIG" $host]

    if {$execResult != "SUCCESS"} {
        return "ERROR"
    }

    set okCert 0
    set certDN ""
    set allCert ""
    set newCert "NONE"
    set prevLineSubjDN 0

    foreach line [split $cmdOut "\n"] {
       if {[regexp "Certificate:" $line] == 1} {
          set okCert 1          
       }       
       
       # get the 'Subject DN' from certificate
       if {$okCert && [regexp {Subject DN[\t\ ]*:[\t\ ]*((.+=.+,?[\t\ ]*)+)\n?} $line all certDN xx] ==1} {
          regsub -all {[\x000-\x010]} $certDN "" newCert   
          set okCert 0
          set prevLineSubjDN 1 
          #puts "HERE 1"
          continue
       }

       # if the line after 'Subject DN : ...' line is a continuation of the previous line, parse these line too
       if {$prevLineSubjDN == 1} {
          #puts "HERE 2"
          if {[regexp {[a-zA-Z0-9]+[\t\ ]*:} $line] == 0} {
             regsub -all {[\x000-\x010]} $line "" newLine
             append newCert $newLine
          } else {
             set prevLineSubjDN 0
          }          
       }

       if {$okCert == 0 && $prevLineSubjDN == 0 && $newCert != "NONE"} {
          #puts "HERE 3"
          if {$CS_id == "first"} {
             set allCert $newCert
             break
          } else {             
             lappend allCert $newCert
          }
       }

    }
    return $allCert    

}

proc GetCACertificate { host {CA_id "first"}} {
    
    global cmdOut
    set rcode ""

    SetCliLevel "CONFIG" $host

    set execResult [Exec "show crypto ca certificates" "CONFIG" $host]

    if {$execResult != "SUCCESS"} {
        return "ERROR"
    }

    set okCert 0
    set certDN ""
    set allCert ""
    set newCert "NONE"
    set prevLineSubjDN 0

    foreach line [split $cmdOut "\n"] {
       if {[regexp "CA Certificate:" $line] == 1} {
          set okCert 1
       }
       
       # get the 'Subject DN' from certificate
       if {$okCert && [regexp {Subject DN[\t\ ]*:[\t\ ]*((.+=.+,?[\t\ ]*)+)\n?} $line all certDN xx] ==1} {
          regsub -all {[\x000-\x010]} $certDN "" newCert   
          set okCert 0
          set prevLineSubjDN 1 
          #puts "HERE 1"
          continue
       }

       # if the line after 'Certifiate: ...' line is a continuation of the previous line, parse these line too
       if {$prevLineSubjDN == 1} {
          #puts "HERE 2"
          if {[regexp {[a-zA-Z0-9]+[\t\ ]*:} $line] == 0} {
             regsub -all {[\x000-\x010]} $line "" newLine
             append newCert $newLine
          } else {
             set prevLineSubjDN 0
          }          
       }

       if {$okCert == 0 && $prevLineSubjDN == 0 && $newCert != "NONE"} {
          #puts "HERE 3"
          if {$CA_id == "first"} {
             set allCert $newCert
             break
          } else {             
             lappend allCert $newCert
          }
       }

    }
    return $allCert    

}

proc EnterCaLevel { certificate host } {

    set prompt "CES\\(config-ca\\)\#"
    
    SetCliLevel "CONFIG" $host

    Exec "crypto ca configure \"[set certificate]\"" $prompt $host
}


proc EnterCaIdentityLevel { host } {

    global cmdOut
    set cmdOut ""

    set prompt "CES\\(ca-identity\\)\#"

    SetCliLevel "CONFIG" $host
    Exec "show crypto password" "CONFIG" $host 1 5
    if { [regexp -nocase {No Key Storage Password defined} $cmdOut] == 1 }  {
            return "NOPASSKEY"
        }

    Exec "crypto ca identity" $prompt $host 1 5
}


proc EnterServerCertConfLevel { serverCertificate host} {
    set prompt "CES\\(config-servercert\\)\#"
    
    SetCliLevel "CONFIG" $host

    Exec "crypto server configure \"$serverCertificate\"" $prompt $host
}

#############################################################
# SetPrivateKeyPass: Sets private key password
# 
# IN:  host: (management IP) / (terminal server Ip:port)
#      pass: password
#
# OUT: SUCCESS/ERROR
#############################################################
proc SetPrivateKeyPass {host pass} {

   set err_count [GetGlobalErr]
   
   SetCliLevel "CONFIG" $host
   
   Exec "crypto password $pass" "CONFIG" $host

   return [CheckGlobalErr $err_count]
   
}
