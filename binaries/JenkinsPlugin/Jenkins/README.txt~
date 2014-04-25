
Jenkins readme

How it’s working:
After a Jenkins job it’s done it will execute the Jenkins Post Script.
This script will verify if the build finished successfully. If yes, it tells the Twister Plugin that the build is ready.
The plugin will run first the build script in order to upload the build on the DUT (Device Under Test).
After will start to run the tests previously saved in a Project File.
After execution it will save the result in the database if needed.


Jenkins Post Script (Jenkins_Post_Script.py) : after the Jenkins job is done this script verifies if the job/build it finished successfully.
If yes then it tells to the Twister Plugin that the build is ready. The Jenkins_Post_Script.py file it’s located in /plugins/Jenkins folder.
You will need to install the Hudson Post build task plugin (http://wiki.hudson-ci.org/display/HUDSON/Post+build+task) in Jenkins.

Twister Plugin : it runs the Build script that uploads the build to the DUT(Device Under Test) and it runs the tests previously saved
in the Project File(XML file). After the execution it saves the results to the Database if needed. When you enable the plugin from
the interface you have to setup the Build Script and the Project File.

Build Script : It uploads the build to the DUT (Device Under Test).


You will have to edit the following files to match your configuration:
- Jenkins Post Script – enter the name of your Job in line 6
- Build Script – this script can be bash, python, tcl
- Project File (XML file) – if you want to save the results in the database after test running the you have to set dbautosave value as true.
