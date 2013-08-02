#!/bin/bash

JDK_PATH=/usr/lib/jvm/jdk1.7.0/bin
EXTLIBS=extlibs/Twister.jar:\
extlibs/jcalendar-1.4.jar:\
extlibs/jsch-0.1.44.jar:\
extlibs/gson-2.2.1.jar:\
extlibs/ws-commons-util-1.0.2.jar:\
extlibs/commons-vfs-1.0.jar:\
extlibs/jgoodies-looks-2.5.1.jar:\
extlibs/jgoodies-common-1.3.1.jar:\
extlibs/jxl.jar:\
extlibs/runner.jar:\
extlibs/ControlPanel.jar:\
extlibs/UserManagement.jar:\
extlibs/ws-commons-util-1.0.2.jar:\
extlibs/xmlrpc-client-3.1.3.jar:\
extlibs/xmlrpc-common-3.1.3.jar

# Compile sources
$JDK_PATH/javac  -deprecation -d classes -source 1.6 -target 1.6  -cp $EXTLIBS  src/*.java

# Generate JAR file
cd classes;
$JDK_PATH/jar  cf ../target/applet.jar Icons *.class

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
echo "Signing jar file jsch-0.1.44.jar"
$JDK_PATH/jarsigner ../extlibs/jsch-0.1.44.jar Twister -storepass password
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
