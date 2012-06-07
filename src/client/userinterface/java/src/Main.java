/*
   File: Main.java ; This file is part of Twister.

   Copyright (C) 2012 , Luxoft

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


/*
 * main method for starting Twister local
 */
public class Main{
    public static void main(String args[]){  
// com.jtattoo.plaf.acryl.AcrylLookAndFeel
// com.jtattoo.plaf.smart.SmartLookAndFeel
// javax.swing.plaf.nimbus.NimbusLookAndFeel
// com.jtattoo.plaf.aero.AeroLookAndFeel
// com.jtattoo.plaf.aluminium.AluminiumLookAndFeel
// com.jtattoo.plaf.bernstein.BernsteinLookAndFeel
// com.jtattoo.plaf.fast.FastLookAndFeel
// com.jtattoo.plaf.graphite.GraphiteLookAndFeel
// com.jtattoo.plaf.hifi.HiFiLookAndFeel
// com.jtattoo.plaf.luna.LunaLookAndFeel
// com.jtattoo.plaf.mcwin.McWinLookAndFeel
// com.jtattoo.plaf.mint.MintLookAndFeel
// com.jtattoo.plaf.noire.NoireLookAndFeel
// com.jtattoo.plaf.smart.SmartLookAndFeel
// ch.randelshofer.quaqua.QuaquaLookAndFeel
// ch.randelshofer.quaqua.QuaquaLookAndFeel15
// ch.randelshofer.quaqua.BasicQuaquaLookAndFeel
// net.sourceforge.napkinlaf.NapkinLookAndFeel
// org.pushingpixels.substance.api.skin.SubstanceAutumnLookAndFeel
// org.pushingpixels.substance.api.skin.SubstanceBusinessBlackSteelLookAndFeel     
// org.pushingpixels.substance.api.skin.SubstanceBusinessBlueSteelLookAndFeel
// org.pushingpixels.substance.api.skin.SubstanceBusinessLookAndFeel        
// org.pushingpixels.substance.api.skin.SubstanceChallengerDeepLookAndFeel        
// org.pushingpixels.substance.api.skin.SubstanceCremeCoffeeLookAndFeel        
// org.pushingpixels.substance.api.skin.SubstanceCremeLookAndFeel     
// org.pushingpixels.substance.api.skin.SubstanceDustCoffeeLookAndFeel    
// org.pushingpixels.substance.api.skin.SubstanceDustLookAndFeel        
// org.pushingpixels.substance.api.skin.SubstanceEmeraldDuskLookAndFeel   
// org.pushingpixels.substance.api.skin.SubstanceGeminiLookAndFeel    
// org.pushingpixels.substance.api.skin.SubstanceGraphiteAquaLookAndFeel        
// org.pushingpixels.substance.api.skin.SubstanceGraphiteGlassLookAndFeel        
// org.pushingpixels.substance.api.skin.SubstanceGraphiteLookAndFeel        
// org.pushingpixels.substance.api.skin.SubstanceMagellanLookAndFeel        
// org.pushingpixels.substance.api.skin.SubstanceMarinerLookAndFeel        
// org.pushingpixels.substance.api.skin.SubstanceMistAquaLookAndFeel
// org.pushingpixels.substance.api.skin.SubstanceMistSilverLookAndFeel        
// org.pushingpixels.substance.api.skin.SubstanceModerateLookAndFeel            
// org.pushingpixels.substance.api.skin.SubstanceNebulaBrickWallLookAndFeel        
// org.pushingpixels.substance.api.skin.SubstanceNebulaLookAndFeel
// org.pushingpixels.substance.api.skin.SubstanceOfficeBlack2007LookAndFeel
// org.pushingpixels.substance.api.skin.SubstanceOfficeBlue2007LookAndFeel        
// org.pushingpixels.substance.api.skin.SubstanceOfficeSilver2007LookAndFeel    
// org.pushingpixels.substance.api.skin.SubstanceRavenLookAndFeel        
// org.pushingpixels.substance.api.skin.SubstanceSaharaLookAndFeel             
// org.pushingpixels.substance.api.skin.SubstanceTwilightLookAndFeel        
// de.hillenbrand.swing.plaf.threeD.ThreeDLookAndFeel
//         try{UIManager.setLookAndFeel("org.pushingpixels.substance.api.skin.SubstanceMistAquaLookAndFeel");}
//         catch(Exception e){
//             e.printStackTrace();
//             System.out.println("Could not load look and feel");}
//        SwingUtilities.invokeLater(new Runnable(){
//           public void run(){
            try{UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");}
            catch(Exception e){e.printStackTrace();}
            /*
             * start Repository initialization and passing to it
             * false - because it does not start from applet
             * host - server address
             * null - to use the default window
             */
            Repository.initialize(false,"tsc-server",null);

            
// }});
//         
//         for(LookAndFeelInfo info : UIManager.getInstalledLookAndFeels()) {
//                 System.out.println(info.getName());
//             if(info.getClassName().equals("com.jtattoo.plaf.smart.SmartLookAndFeel")){
//                 try{UIManager.setLookAndFeel(info.getClassName());}
//                 catch(Exception e){
//                     e.printStackTrace();
//                     System.out.println("Could not load look and feel");}}
//                 }
        }}      
