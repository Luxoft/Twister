lappend auto_path /xtra/home/speaktst/twister/tools/lib/expect5.32
lappend auto_path "/xtra/home/speaktst/speak/BayLib"

package require Expect

set gLogLevel 1
set timeout 30
source "/xtra/home/speaktst/speak/tools/et1000.tcl"
source "/xtra/home/speaktst/speak/tools/globals.tcl"
source "/xtra/home/speaktst/speak/tools/utils.tcl"
source "/xtra/home/speaktst/speak/tools/linking.tcl"
source "/xtra/home/speaktst/speak/tools/errno.tcl"
source "/xtra/home/speaktst/speak/tools/initial.tcl"
source "/xtra/home/speaktst/speak/tools/etcount.tcl"
source "/xtra/home/speaktst/speak/tools/smbcount.tcl"
source "/xtra/home/speaktst/speak/tools/etherPhy.tcl"
source "/xtra/home/speaktst/speak/tools/smbshell.tcl"
source "/xtra/home/speaktst/speak/tools/thunder.tcl"
source "/xtra/home/speaktst/speak/tools/token.tcl"
source "/xtra/home/speaktst/speak/tools/gigcards.tcl"
source "/xtra/home/speaktst/speak/tools/capture.tcl"
source "/xtra/home/speaktst/speak/tools/decodes.tcl"
source "/xtra/home/speaktst/speak/tools/fstvlan.tcl"

global env
set env(TsIpAddr) 10.100.100.168
set env(TsPort) "5002 5003 5009"
set env(DutIpAddr) 10.106.17.10
set env(GwIpAddr) 10.106.17.1
set env(GwNetmask) 255.255.255.0
set env(TftpServerIp) 10.100.100.15

global twister_exitcode 
set twister_exitcode "FAIL"

proc Exit { exit_code } {
   puts "Test exit with code: $exit_code"
   global twister_exitcode
   if {$exit_code} {
        set $twister_exitcode "FAIL"
   }
   else {
        set $twister_exitcode "PASS"
   }
}


source "/xtra/home/speaktst/speak/plan/IpMgr/Cases.IpMgr.tcl"
 
