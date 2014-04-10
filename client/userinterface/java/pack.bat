cd ../../../plugins/TestCaseExecution
CALL build.bat
cd ../../../client/userinterface/java/
copy "..\..\..\plugins\TestCaseExecution\target\runner.jar" "extlibs\runner.jar"

SET EXTLIBS="extlibs/Twister.jar;extlibs/gson-2.2.1.jar;extlibs/ws-commons-util-1.0.2.jar;extlibs/commons-vfs-1.0.jar;extlibs/jgoodies-looks-2.5.1.jar;extlibs/jgoodies-common-1.3.1.jar;extlibs/VFSJFileChooser-0.0.3.jar;extlibs/jxl.jar;extlibs/ws-commons-util-1.0.2.jar;extlibs/xmlrpc-client-3.1.3.jar;extlibs/xmlrpc-common-3.1.3.jar;extlibs/UserManagement.jar;extlibs/ControlPanel.jar;extlibs/runner.jar"


javac.exe -deprecation -d classes -source 1.6 -target 1.6 -cp %EXTLIBS% src/*.java

cd classes
jar cfm ../target/applet.jar ../manifestaddition.txt Icons  *.class

cd ../target

jarsigner applet.jar                                               Twister -storepass password
jarsigner ../extlibs/commons-logging-1.1.1.jar  Twister -storepass password
jarsigner ../extlibs/commons-vfs-1.0.jar             Twister -storepass password
jarsigner ../extlibs/jxl.jar                                        Twister -storepass password
jarsigner ../extlibs/ws-commons-util-1.0.2.jar    Twister -storepass password
jarsigner ../extlibs/xmlrpc-client-3.1.3.jar           Twister -storepass password
jarsigner ../extlibs/xmlrpc-common-3.1.3.jar     Twister -storepass password
jarsigner ../extlibs/jgoodies-looks-2.5.1.jar       Twister -storepass password
jarsigner ../extlibs/jgoodies-common-1.3.1.jar Twister -storepass password
jarsigner ../extlibs/gson-2.2.1.jar                        Twister -storepass password
jarsigner ../extlibs/jcalendar-1.4.jar                    Twister -storepass password
jarsigner ../extlibs/Twister.jar                              Twister -storepass password
jarsigner ../extlibs/runner.jar                               Twister -storepass password
jarsigner ../extlibs/ControlPanel.jar                   Twister -storepass password
jarsigner ../extlibs/UserManagement.jar           Twister -storepass password

keytool -export -alias Twister -rfc -file sig.x509 -storepass password

pause
