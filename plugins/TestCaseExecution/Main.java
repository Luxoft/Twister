/*
File: Main.java ; This file is part of Twister.
Version: 2.010

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
import javax.imageio.ImageIO;
import java.awt.BorderLayout;
import java.awt.EventQueue;
import java.awt.event.ActionEvent;
import java.net.URLClassLoader;
import java.rmi.RMISecurityManager;
import java.net.URL;
import java.awt.Image;
import java.io.BufferedReader;
import java.io.InputStreamReader;

import javax.swing.JFrame;
import javax.swing.JButton;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;


/*
 * main method for starting Twister local
 */
public class Main{
    
    public static void main(String args[]){
        try {
//             JFrame f = new JFrame();
//             JButton b = new JButton("STOP");
//             b.addActionListener(new ActionListener(){
//                 public void actionPerformed(ActionEvent ev){
//                     RunnerRepository.run = false;
//                     RunnerRepository.session.disconnect();
//                     RunnerRepository.connection.disconnect();        
//                     RunnerRepository.window.mainpanel.p1.ep.session.disconnect();
//                     RunnerRepository.window.mainpanel.p1.ep.connection.disconnect();
//                     RunnerRepository.window.mainpanel.p1.lp.session.disconnect();
//                     RunnerRepository.window.mainpanel.p1.lp.connection.disconnect();
//                     RunnerRepository.window.mainpanel.p4.getPlugins().session.disconnect();
//                     RunnerRepository.window.mainpanel.p4.getPlugins().ch.disconnect();
//                     RunnerRepository.window.mainpanel.p4.getGlobals().session.disconnect();
//                     RunnerRepository.window.mainpanel.p4.getGlobals().ch.disconnect();
//                     RunnerRepository.window.mainpanel.p4.getTestConfig().tree.session.disconnect();
//                     RunnerRepository.window.mainpanel.p4.getTestConfig().tree.connection.disconnect();
//                     RunnerRepository.window.mainpanel.p4.getTestConfig().cfgedit.session.disconnect();
//                     RunnerRepository.window.mainpanel.p4.getTestConfig().cfgedit.ch.disconnect();
//                 }
//             });
//             f.add(b);
//             f.setVisible(true);
            URL url = new URL("http://tsc-server/twister_gui/logo.png");
            RunnerRepository.logo = ImageIO.read(url).getScaledInstance(230, 100, Image.SCALE_FAST);
        } catch (Exception e) {
            e.printStackTrace();
        }
        readLogoTxt();
        
        PermissionValidator.init("CREATE_PROJECT,CHANGE_PROJECT,DELETE_PROJECT,CHANGE_PLUGINS,"+
                                 "CHANGE_FWM_CFG,CHANGE_GLOBALS,RUN_TESTS,EDIT_TC,"+
                                 "CHANGE_DB_CFG, CHANGE_EML_CFG,CHANGE_SERVICES,CHANGE_SUT");
    //         RunnerRepository.initialize("false","tsc-server",null);
        RunnerRepository.user = "user";
        RunnerRepository.password = "password";
        RunnerRepository.host = "11.126.32.21";
        RunnerRepository.initialize("false",RunnerRepository.host,null);
    }
//             RunnerRepository.initialize(false,"11.126.32.15",null);}

    public static void readLogoTxt(){
        try{
            URL logo = new URL("http://tsc-server/twister_gui/logo.txt");
            BufferedReader in = new BufferedReader(
            new InputStreamReader(logo.openStream()));
            
            StringBuilder sb = new StringBuilder();
            String inputLine;
            while ((inputLine = in.readLine()) != null){
                sb.append(inputLine);
                sb.append("\n");
            }
            in.close();
            RunnerRepository.logotxt = sb.toString();
        } catch(Exception e){
            e.printStackTrace();
        }
    }

}
