#!/usr/bin/perl

#
# version: 3.001
# <title>init file</title>
# <description>Test status</description>
#

use warnings;


sub test001 {
	# Must return one of the statuses:
	# $STATUS_PASS, $STATUS_FAIL, $STATUS_SKIPPED, $STATUS_ABORTED,
	# $STATUS_NOT_EXEC, $STATUS_TIMEOUT, or $STATUS_INVALID
	$error_code = $STATUS_PASS;

	log_msg("logTest", "\nTestCase: $SUITE_NAME::$FILE_NAME starting\n");
	print "Starting test $FILE_NAME ...\n";

	log_msg("logRunning", "TEST: working working...\n");

	foreach ((1..10)) {
		log_msg("logDebug", "$FILE_NAME: working $_...\n");
		print "$FILE_NAME: working $_...\n";
		sleep(1);
	}

	log_msg("logRunning", "TEST: working even more...\n");

	log_msg("logTest", "TestCase: $SUITE_NAME::$FILE_NAME returned $error_code\n");
	return $error_code
}

exit( test001() );
