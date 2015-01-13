#!/usr/bin/perl

#
# version: 3.001
# <title>globals file</title>
# <description>Test status</description>
#

use warnings;


sub test_g2 {
	# Must return one of the statuses:
	# $STATUS_PASS, $STATUS_FAIL, $STATUS_SKIPPED, $STATUS_ABORTED,
	# $STATUS_NOT_EXEC, $STATUS_TIMEOUT, or $STATUS_INVALID
	$error_code = $STATUS_PASS;

	log_msg("logTest", "\nTestCase: $SUITE_NAME::$FILE_NAME starting\n");
	print "Starting test $FILE_NAME ...\n\n";

	print "Getting globals from previous glob test.\n";

	$g0 = get_global("/some_global1");
	print "Getting some global 1  =  $g0\n";

	$g0 = get_global("/some_global2");
	print "Getting some global 2  =  $g0\n";

	log_msg("logTest", "TestCase: $SUITE_NAME::$FILE_NAME returned $error_code\n");
	return $error_code
}

exit( test_g2() );
