

proc SSHExec { host cmd {user "root"} {pass "contivity"} {prompt "# "} } {
	
    global spawn_id timeout spawnId spawnPid
    set backupTimeout $timeout
    set timeout 30
        
    set pid [spawn ssh $user@$host]
    match_max 100000
    set notConnected 1

    set rcode ""

    expect {
        -re "assword: " {
            exp_send -- "$pass\r"
            expect {
                -re  "$prompt$" {
                    set notConnected 0
                }
            }
        } -re "(yes/no)" {
				exp_send -- "yes\r"
				expect -re "assword: " {
					exp_send -- "$pass\r"
					expect {
						-re  "$prompt$" {
							set notConnected 0
						}
					}
				}
		} -re "verification failed" {
				set rcode "ERROR: Host key verification failed. Please check .ssh/known_hosts"
				return [ErrCheck $rcode SSHExec]
			}
		}

		if {$notConnected == 0} {
			set spawnPid($host) $pid
			set spawnId($host)  $spawn_id

			exp_send -- "$cmd\r"
			expect -re  "$prompt$" 

			exp_send -- "echo \$\?\r"
			expect -re  "$prompt$" 

			if { [regexp "\[\r\n\]+0\[\r\n\]+" $expect_out(buffer)] != 1} {
				set rcode "ERROR: Warning: SSH Command FAILED"
			}

			set timeout $backupTimeout
			return [ErrCheck $rcode SSHExec]

		} else {
			set timeout $backupTimeout
			set rcode ""
			Disconnect $host
			lappend rcode "ERROR: connection failure"
			return [ErrCheck $rcode SSHExec]
		}

		set timeout $backupTimeout
		
		logCliFile "\n---------------------------- sshServer: $host ----------------------------\n"
		
}

