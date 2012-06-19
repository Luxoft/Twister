#!/bin/bash

JDK_PATH=/usr/lib/jvm/jdk1.7.0/bin
EXTLIBS=extlibs/jsch-0.1.44.jar:\
extlibs/gson-2.2.1.jar:\
extlibs/ws-commons-util-1.0.2.jar:\
extlibs/commons-vfs-1.0.jar:\
extlibs/jgoodies-looks-2.5.1.jar:\
extlibs/jgoodies-common-1.3.1.jar:\
extlibs/VFSJFileChooser-0.0.3.jar:\
extlibs/jxl.jar:\
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
jarsigner applet.jar Twister -storepass password
echo "Signing jar file gson-2.2.1.jar"
jarsigner ../extlibs/gson-2.2.1.jar Twister -storepass password
echo "Signing jar file commons-logging-1.1.1.jar"
jarsigner ../extlibs/commons-logging-1.1.1.jar Twister -storepass password
echo "Signing jar file commons-vfs-1.0.jar"
jarsigner ../extlibs/commons-vfs-1.0.jar Twister -storepass password
echo "Signing jar file jsch-0.1.44.jar"
jarsigner ../extlibs/jsch-0.1.44.jar Twister -storepass password
echo "Signing jar file jxl.jar"
jarsigner ../extlibs/jxl.jar Twister -storepass password
echo "Signing jar file VFSJFileChooser-0.0.3.jar"
jarsigner ../extlibs/VFSJFileChooser-0.0.3.jar Twister -storepass password
echo "Signing jar file ws-commons-util-1.0.2.jar"
jarsigner ../extlibs/ws-commons-util-1.0.2.jar Twister -storepass password
echo "Signing jar file xmlrpc-client-3.1.3.jar"
jarsigner ../extlibs/xmlrpc-client-3.1.3.jar Twister -storepass password
echo "Signing jar file xmlrpc-common-3.1.3.jar"
jarsigner ../extlibs/xmlrpc-common-3.1.3.jar Twister -storepass password
echo "Signing jar file jgoodies-looks-2.5.1.jar"
jarsigner ../extlibs/jgoodies-looks-2.5.1.jar Twister -storepass password
echo "Signing jar file jgoodies-common-1.3.1.jar"
jarsigner ../extlibs/jgoodies-common-1.3.1.jar Twister -storepass password


# Export the keystore as X509
$JDK_PATH/keytool  -export -alias Twister -rfc -file ../target/sig.x509 -storepass password
