#!/usr/bin/perl
use warnings;
use strict;
use Net::Telnet;
use Inline::Python qw(py_eval py_bind_func py_bind_class);

py_eval(<<'END_OF_PYTHON_CODE');

import os, sys
sys.path.append(os.getenv("HOME") + "/.twister_cache/")

import ce_libs
import telnetlib

END_OF_PYTHON_CODE

#

sub test003_python {
	py_bind_func("main::logMsg", "ce_libs", "logMsg");
	py_bind_class("main::Telnet", "telnetlib", "Telnet", "read_until", "write", "read_very_eager");

	my $testName = "test003.plx";
	my $error_code = "PASS";

	logMsg("logTest", "\nTestCase: $testName starting\n");
	print "Starting test $testName ...\n";

	my $tn = new Telnet("134.117.136.48", 23, 60);
	print "Connected: $tn";

	print $tn->read_until("login:", 30);
	$tn->write("guest\n");

	print $tn->read_until("any key to continue...", 10);
	$tn->write("\n\n");

	print $tn->read_until('"q" to quit', 10);
	$tn->write("q\n");

	print $tn->read_until("About the National Capital FreeNet", 10);
	$tn->write("1\n");

	print $tn->read_until("Your Choice ==>", 10);
	$tn->write("x\n");
	$tn->write("y\n");

	print $tn->read_very_eager();

	logMsg("logTest", "TestCase:$testName $error_code\n");
	return $error_code;
}

#

sub test003_perl {
	my $tn = Net::Telnet->new(Timeout => 60, Prompt => '/%/', Host => "134.117.136.48");

	$tn->login("guest", "\n");

	@lines = $tn->cmd("who");
	print @lines;

	@files = $tn->cmd("ls");
	print @files;

	$tn->close;
}

test003_python();
#test003_perl();

#
