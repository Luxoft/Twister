#set dirname /usr/local/lib/Acelib
if {[info exists env(ACE_PATH)] == 1} {
   set dirname [file join $env(ACE_PATH) Acelib]
} else {
   set dirname [file join . Acelib]
}

# verify if directory $dirname exists
if {[catch {glob $dirname/*.tcl} err_path1] != 0} {   

   puts "Bad Acelib path:"
   puts "    $err_path1"

} 

# load Acelib package
package ifneeded  Acelib 2.1 [list loadlib $dirname]

proc loadlib {dirname} {

    foreach file [glob $dirname/*.tcl] {
        #puts $file
        uplevel #0 source [list $file]
    }
}


