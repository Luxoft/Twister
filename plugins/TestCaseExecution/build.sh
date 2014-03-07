#!/bin/bash

JDK_PATH=/usr/lib/jvm/jdk1.7.0/bin
EXTLIBS=../../client/userinterface/java/extlibs/Twister.jar:\
../../client/userinterface/java/extlibs/jcalendar-1.4.jar:\
../../client/userinterface/java/extlibs/gson-2.2.1.jar:\
../../client/userinterface/java/extlibs/ws-commons-util-1.0.2.jar:\
../../client/userinterface/java/extlibs/commons-vfs-1.0.jar:\
../../client/userinterface/java/extlibs/jgoodies-looks-2.5.1.jar:\
../../client/userinterface/java/extlibs/jgoodies-common-1.3.1.jar:\
../../client/userinterface/java/extlibs/jxl.jar:\
../../client/userinterface/java/extlibs/runner.jar:\
../../client/userinterface/java/extlibs/ControlPanel.jar:\
../../client/userinterface/java/extlibs/UserManagement.jar:\
../../client/userinterface/java/extlibs/ws-commons-util-1.0.2.jar:\
../../client/userinterface/java/extlibs/xmlrpc-client-3.1.3.jar:\
../../client/userinterface/java/extlibs/xmlrpc-common-3.1.3.jar

# Compile sources
$JDK_PATH/javac  -deprecation -d classes -source 1.6 -target 1.6  -cp $EXTLIBS  *.java

cd classes;
$JDK_PATH/jar  cfm ../target/runner.jar ../manifestaddition.txt Icons *.class

