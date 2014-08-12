#!/bin/bash

JDK_PATH=/usr/lib/jvm/jdk1.7.0_09/bin
TWISTER_EXLIB=~/twister_rel2/client/userinterface/java/extlibs
EXTLIBS=$TWISTER_EXLIB/Twister.jar:\
$TWISTER_EXLIB/jcalendar-1.4.jar:\
$TWISTER_EXLIB/jsch-0.1.44.jar:\
$TWISTER_EXLIB/gson-2.2.1.jar:\
$TWISTER_EXLIB/ws-commons-util-1.0.2.jar:\
$TWISTER_EXLIB/commons-vfs-1.0.jar:\
$TWISTER_EXLIB/jgoodies-looks-2.5.1.jar:\
$TWISTER_EXLIB/jgoodies-common-1.3.1.jar:\
$TWISTER_EXLIB/jxl.jar:\
$TWISTER_EXLIB/ws-commons-util-1.0.2.jar:\
$TWISTER_EXLIB/xmlrpc-client-3.1.3.jar:\
$TWISTER_EXLIB/xmlrpc-common-3.1.3.jar

# Compile sources
$JDK_PATH/javac  -deprecation -source 1.6 -target 1.6  -cp $EXTLIBS  SamplePlugin.java

# Generate JAR file
#cd classes;
$JDK_PATH/jar  cf SamplePlugin.jar SamplePlugin.class

mkdir SamplePluginDir
mv SamplePlugin.jar SamplePluginDir
cd SamplePluginDir
$JDK_PATH/jar -xvf SamplePlugin.jar
rm SamplePlugin.jar

cd META-INF
mkdir services
cd services
echo "SamplePlugin" > "com.twister.plugin.twisterinterface.TwisterPluginInterface"
cd ../../
$JDK_PATH/jar -cvf SamplePlugin.jar *
cd ..
mv SamplePluginDir/SamplePlugin.jar .
rm -rf SamplePluginDir

