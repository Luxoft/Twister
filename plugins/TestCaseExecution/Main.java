/*
File: Main.java ; This file is part of Twister.
Version: 2.001

Copyright (C) 2012-2013 , Luxoft

Authors: Andrei Costachi <acostachi@luxoft.com>
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/
import javax.swing.UIManager;
import javax.swing.UIManager.LookAndFeelInfo;
import javax.swing.SwingUtilities;

import java.awt.BorderLayout;
import java.awt.EventQueue;
import java.awt.event.ActionEvent;
import java.net.URLClassLoader;
import java.rmi.RMISecurityManager;


/*
 * main method for starting Twister local
 */
public class Main{
    
    public static void main(String args[]){
//         RunnerRepository.initialize(false,"11.126.32.20",null);}
        RunnerRepository.user = "tscguest";
        RunnerRepository.password = "tscguest";
        RunnerRepository.host = "tsc-server";
        RunnerRepository.initialize("false","tsc-server",null);}
//             RunnerRepository.initialize(false,"11.126.32.15",null);}
}
