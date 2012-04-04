#!/bin/bash

JDK_PATH=/opt/java1.7/bin

EXTLIBS=extlibs/jsch-0.1.44.jar:\
extlibs/ws-commons-util-1.0.2.jar:\
extlibs/commons-vfs-1.0.jar:\
extlibs/VFSJFileChooser-0.0.3.jar:\
extlibs/jcommon-1.0.16.jar:\
extlibs/jxl.jar:\
extlibs/ws-commons-util-1.0.2.jar:\
extlibs/xmlrpc-client-3.1.3.jar:\
extlibs/xmlrpc-common-3.1.3.jar

# Compile sources
$JDK_PATH/javac  -deprecation -d classes -source 1.6 -target 1.6  -cp $EXTLIBS  src/*.java

# Generate JAR file
$JDK_PATH/jar  cf target/applet.jar classes/Icons classes/*.class

# Sign the JAR file using the keystore
$JDK_PATH/jarsigner  target/applet.jar Twister -storepass password

# Export the keystore as X509
$JDK_PATH/keytool  -export -alias Twister -rfc -file target/sig.x509 -storepass password
