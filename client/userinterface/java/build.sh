#!/bin/bash

JDK_PATH=/usr/lib/jvm/jdk1.7.0_09/bin/
CURRENT_PWD=`pwd`
EXTLIBS=$CURRENT_PWD/extlibs/Twister.jar:\
$CURRENT_PWD/extlibs/jcalendar-1.4.jar:\
$CURRENT_PWD/extlibs/gson-2.2.1.jar:\
$CURRENT_PWD/extlibs/ws-commons-util-1.0.2.jar:\
$CURRENT_PWD/extlibs/commons-vfs-1.0.jar:\
$CURRENT_PWD/extlibs/jgoodies-looks-2.5.1.jar:\
$CURRENT_PWD/extlibs/jgoodies-common-1.3.1.jar:\
$CURRENT_PWD/extlibs/jxl.jar:\
$CURRENT_PWD/extlibs/runner.jar:\
$CURRENT_PWD/extlibs/ControlPanel.jar:\
$CURRENT_PWD/extlibs/UserManagement.jar:\
$CURRENT_PWD/extlibs/ws-commons-util-1.0.2.jar:\
$CURRENT_PWD/extlibs/xmlrpc-client-3.1.3.jar:\
$CURRENT_PWD/extlibs/xmlrpc-common-3.1.3.jar

# need to build runner.jar first from 
cd ../../../plugins/TestCaseExecution/
rm target/runner.jar
$JDK_PATH/javac  -deprecation -d classes -source 1.6 -target 1.6  -cp $EXTLIBS  *.java
cd classes
$JDK_PATH/jar  cfm ../target/runner.jar ../manifestaddition.txt Icons *.class
cp ../target/runner.jar $CURRENT_PWD/extlibs
cd $CURRENT_PWD

# Compile sources
$JDK_PATH/javac  -deprecation -d classes -source 1.6 -target 1.6  -cp $EXTLIBS  src/*.java

# Generate JAR file
cd classes;
$JDK_PATH/jar  cfm ../target/applet.jar ../manifestaddition.txt Icons *.class

# Sign the JAR file using the keystore
cd ../target
echo "Signing jar file applet.jar"
$JDK_PATH/jarsigner applet.jar Twister -storepass password
echo "Signing jar file gson-2.2.1.jar"
$JDK_PATH/jarsigner ../extlibs/gson-2.2.1.jar Twister -storepass password
echo "Signing jar file commons-logging-1.1.1.jar"
$JDK_PATH/jarsigner ../extlibs/commons-logging-1.1.1.jar Twister -storepass password
echo "Signing jar file commons-vfs-1.0.jar"
$JDK_PATH/jarsigner ../extlibs/commons-vfs-1.0.jar Twister -storepass password
echo "Signing jar file jxl.jar"
$JDK_PATH/jarsigner ../extlibs/jxl.jar Twister -storepass password
echo "Signing jar file ws-commons-util-1.0.2.jar"
$JDK_PATH/jarsigner ../extlibs/ws-commons-util-1.0.2.jar Twister -storepass password
echo "Signing jar file xmlrpc-client-3.1.3.jar"
$JDK_PATH/jarsigner ../extlibs/xmlrpc-client-3.1.3.jar Twister -storepass password
echo "Signing jar file xmlrpc-common-3.1.3.jar"
$JDK_PATH/jarsigner ../extlibs/xmlrpc-common-3.1.3.jar Twister -storepass password
echo "Signing jar file jgoodies-looks-2.5.1.jar"
$JDK_PATH/jarsigner ../extlibs/jgoodies-looks-2.5.1.jar Twister -storepass password
echo "Signing jar file jgoodies-common-1.3.1.jar"
$JDK_PATH/jarsigner ../extlibs/jgoodies-common-1.3.1.jar Twister -storepass password
echo "Signing jar file jcalendar-1.4.jar"
$JDK_PATH/jarsigner ../extlibs/jcalendar-1.4.jar Twister -storepass password

echo "Signing jar file UserManagement.jar"
$JDK_PATH/jarsigner ../extlibs/UserManagement.jar Twister -storepass password
echo "Signing jar file runner.jar"
$JDK_PATH/jarsigner ../extlibs/runner.jar Twister -storepass password
echo "Signing jar file ControlPanel.jar"
$JDK_PATH/jarsigner ../extlibs/ControlPanel.jar Twister -storepass password

echo "Signing jar file Twister.jar"
$JDK_PATH/jarsigner ../extlibs/Twister.jar Twister -storepass password


# Export the keystore as X509
$JDK_PATH/keytool  -export -alias Twister -rfc -file ../target/sig.x509 -storepass password
