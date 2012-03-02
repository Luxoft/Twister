#!/usr/bin/perl
use warnings;

#

sub test001 {
	$testName = "test001.plx";
	$error_code = "PASS";

	logMsg("logTest", "\nTestCase: $testName starting\n");
	print "Starting test $testName ...\n";

	foreach ((1..10)) {
		# Exposed Python function
		logMsg("logDebug", "$testName: working $_...\n");
		print "$testName: working $_...\n";
		sleep(1);
	}

	logMsg("logRunning", "TEST: working even more 111...\n");
	logMsg("logTest", "TestCase:$testName $error_code\n");
	sleep(1);

	return $error_code
}

test001();

#

use Inline Python => <<"END_OF_PYTHON_CODE";

import os, sys
sys.path.append(os.getenv("HOME") + "/.twister_cache/")
from ce_libs import logMsg

END_OF_PYTHON_CODE

#
