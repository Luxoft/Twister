SET EXTLIBS="../../client/userinterface/java/extlibs/Twister.jar;../../client/userinterface/java/extlibs/gson-2.2.1.jar;../../client/userinterface/java/extlibs/ws-commons-util-1.0.2.jar;../../client/userinterface/java/extlibs/commons-vfs-1.0.jar;../../client/userinterface/java/extlibs/jgoodies-looks-2.5.1.jar;../../client/userinterface/java/extlibs/jgoodies-common-1.3.1.jar;../../client/userinterface/java/extlibs/VFSJFileChooser-0.0.3.jar;../../client/userinterface/java/extlibs/jxl.jar;../../client/userinterface/java/extlibs/ws-commons-util-1.0.2.jar;../../client/userinterface/java/extlibs/xmlrpc-client-3.1.3.jar;../../client/userinterface/java/extlibs/xmlrpc-common-3.1.3.jar;../../client/userinterface/java/extlibs/UserManagement.jar;../../client/userinterface/java/extlibs/ControlPanel.jar;../../client/userinterface/java/extlibs/runner.jar"

javac.exe -deprecation -d classes -source 1.6 -target 1.6 -cp %EXTLIBS% *.java

cd classes
jar cfm ../target/runner.jar ../manifestaddition.txt Icons  *.class

pause
