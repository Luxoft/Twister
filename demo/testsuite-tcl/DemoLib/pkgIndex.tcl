
package provide DemoLib  1.0
#package require Tcl      8.4

if {[info exists env(DEMO_PATH)] == 1} {
   set dirname [file join $env(DEMO_PATH) DemoLib]
} else {
   set dirname [file join . DemoLib]
}

# verify if directory $dirname exists
if {[catch {glob $dirname/*.tcl} err_path1] != 0} {   
   puts "Bad DemoLib path: $err_path1 !"
}

# load DemoLib package
package ifneeded  DemoLib 1.0 [list loadlib $dirname]

proc loadlib {dirname} {
    foreach file [glob $dirname/*.tcl] {
        uplevel #0 source [list $file]
    }
}
