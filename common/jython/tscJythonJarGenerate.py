#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
# version: 1.000
#
#
# Copyright (C) 2012 , Luxoft
#
#
# Authors:
#    Adrian Toader <adtoader@luxoft.com>
#
#


from os.path import split
from os import chdir

from subprocess import Popen




chdir(split(__file__)[0])

print '## begin ##'

print 'compile..'
Popen('javac -classpath /usr/share/java/jython.jar ' \
	'/home/adr/twister/common/jython/tscJython/interfaces/ExternalVariableType.java ' \
	'/home/adr/twister/common/jython/tscJython/utilities/ExternalVariableFactory.java',
	shell=True)

print 'create jar file..'
Popen('jar -cf tscJython.jar ' \
	'tscJython/interfaces/ExternalVariableType.class ' \
	'tscJython/utilities/ExternalVariableFactory.class', shell=True)

print '## done ##'
