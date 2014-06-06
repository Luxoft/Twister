#!/usr/bin/perl

#
# version: 3.001
# <title>init file</title>
# <description>Test status</description>
#

# `USER`, `EP`, `SUITE_NAME` and `FILE_NAME` are magic variables,
# injected inside all Twister tests.

use warnings;

print "I am not doing anything special, just printing some variables.";

print "Hello, user $USER !\n";
print "System Under Test: $SUT \n";
print "Exec process: $EP \n";
print "Suite: $SUITE_NAME \n";
print "Remote file: $FILE_NAME \n";

exit($STATUS_FAIL);

#
