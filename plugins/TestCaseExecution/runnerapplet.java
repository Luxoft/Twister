// /*
// File: runnerapplet.java ; This file is part of Twister.
// Version: 2.003
// 
// Copyright (C) 2012-2013 , Luxoft
// 
// Authors: Andrei Costachi <acostachi@luxoft.com>
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
// 
// http://www.apache.org/licenses/LICENSE-2.0
// 
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
// */
// import java.applet.Applet; 
// import java.awt.Graphics; 
// import java.awt.Color;
// import java.awt.Dimension;
// import java.awt.Toolkit;
// import javax.swing.ImageIcon;
// import javax.swing.JOptionPane;
// import java.io.File;
// import javax.imageio.ImageIO;
// import java.io.InputStream;
// import java.io.BufferedReader;
// import java.io.StringWriter;
// import java.io.InputStreamReader;
// import java.io.PrintWriter;
// import java.io.ByteArrayOutputStream;
// import java.io.ByteArrayInputStream;
// import java.awt.image.BufferedImage;
// import java.awt.Image;
// import javax.swing.UIManager;
// import javax.swing.SwingUtilities;
// import java.net.URLClassLoader;
// import com.twister.MySecurityManager;
// import java.net.URL;
// 
// public class runnerapplet extends Applet{ 
//     private static final long serialVersionUID = 1L;
//     
//     //applet initialization
//     public void init(){
// //         try{UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");}
// //         catch(Exception e){e.printStackTrace();} 
//         
//         /*
//          * load all icons from jar into RunnerRepository
//          */
//         try{
//             System.out.println("OS current temporary directory is : "+
//                                 System.getProperty("java.io.tmpdir"));
//             System.setSecurityManager(new MySecurityManager());
//             RunnerRepository.tcicon = loadIcon("tc.png");
//             RunnerRepository.background = loadIcon("background.png");
//             RunnerRepository.pendingicon = loadIcon("pending.png");
//             RunnerRepository.deviceicon = loadIcon("device.png");
//             RunnerRepository.upicon = loadIcon("up.png");
//             RunnerRepository.moduleicon = loadIcon("module.png");
//             RunnerRepository.notexecicon = loadIcon("notexec.png");
//             RunnerRepository.skipicon = loadIcon("skip.png");
//             RunnerRepository.stoppedicon = loadIcon("stopped.png");
//             RunnerRepository.timeouticon = loadIcon("timeout.png");
//             RunnerRepository.waiticon = loadIcon("waiting.png");
//             RunnerRepository.workingicon = loadIcon("working.png");
//             RunnerRepository.suitaicon = loadIcon("suita.png");
//             RunnerRepository.propicon = loadIcon("prop.png");
//             RunnerRepository.vlcclient = loadIcon("vlcclient.png");
//             RunnerRepository.failicon = loadIcon("fail.png");
//             RunnerRepository.passicon = loadIcon("pass.png");
//             RunnerRepository.stopicon = loadIcon("stop.png");
//             RunnerRepository.switche = loadIcon("switch.png");
//             RunnerRepository.switche2 = loadIcon("switch.jpg");
//             RunnerRepository.flootw = loadIcon("twisterfloodlight.png");
//             RunnerRepository.rack150 = loadIcon("150.png");
//             RunnerRepository.rack151 = loadIcon("151.png");
//             RunnerRepository.rack152 = loadIcon("152.png");
//             RunnerRepository.vlcserver = loadIcon("vlcserver.png");
//             RunnerRepository.playicon = loadIcon("play.png");
//             RunnerRepository.addsuitaicon = loadIcon("addsuita.png");
//             RunnerRepository.removeicon = loadIcon("deleteicon.png");
//             RunnerRepository.pauseicon = loadIcon("pause.png");
//             RunnerRepository.porticon = loadIcon("port.png");
//             RunnerRepository.testbedicon = loadIcon("testbed.png");
//             RunnerRepository.inicon = loadIcon("in.png");
//             RunnerRepository.outicon = loadIcon("out.png");
//             RunnerRepository.passwordicon = loadIcon("passwordicon.png");
//             RunnerRepository.baricon = loadIcon("bar.png");
//             RunnerRepository.invalid = loadIcon("invalid.png");
//             //RunnerRepository.optional = loadIcon("optional.png");
//         }
//         catch(Exception e){e.printStackTrace();}
//         setLayout(null);
//         /*
//          * start RunnerRepository initialization and passing to it
//          * true - because starts from applet
//          * host - server address
//          * this - as container
//          */
//         RunnerRepository.initialize("true", getCodeBase().getHost(),runnerapplet.this);
//         try{
//             getAppletContext().showDocument(new URL("javascript:resize()"));
//         } catch (Exception e) {
//             System.err.println("Failed to call JavaScript function appletLoaded()");
//         }    
//     }
//         
//         
//     /*
//      * the general method to load icons from jar
//      */
//     public Image loadIcon(String icon){
//         Image image = null;
//         try{System.out.println("Getting "+icon+" from applet jar...");
//             InputStream in = getClass().getResourceAsStream("Icons"+"/"+icon);
//             System.out.println("Saving "+icon+" in memory.....");
//             image = new ImageIcon(ImageIO.read(in)).getImage();
//             if(image !=null)System.out.println(icon+" succsesfully loaded.");
//             else System.out.println(icon+" not loaded.");}
//         catch(Exception e){
//             System.out.println("There was a problem in loading "+icon+
//                 " on "+image.toString());
//             e.printStackTrace();}
//         return image;}
//     
//         
//     /*
//      * set size method for applet
//      * called by javascript when browser resizes
//      */
//     public void setSize(int width, int height){
//         super.setSize(width,height);
//         RunnerRepository.window.mainpanel.setSize(width-20,height-20);
//         //RunnerRepository.window.mainpanel.p2.splitPane.setSize(width-52,height-120);
//         RunnerRepository.window.mainpanel.p1.splitPane.setSize(width-52,height-120);
//         RunnerRepository.window.mainpanel.setSize(width-28,height-40);
//         RunnerRepository.window.mainpanel.p4.getScroll().setSize(width-310,height-150);
//         RunnerRepository.window.mainpanel.p4.getMain().setSize(width-300,height-130);
//         RunnerRepository.window.mainpanel.p4.getTB().setPreferredSize(
//             new Dimension(width-300,height-150));
//         RunnerRepository.window.appletpanel.setSize(width-20,height-20);        
//         RunnerRepository.window.mainpanel.p4.getPlugins().setPreferredSize(
//             new Dimension(getWidth()-300,getHeight()-150));
//         RunnerRepository.window.mainpanel.p4.getPlugins().horizontalsplit.setPreferredSize(
//             new Dimension(getWidth()-305,getHeight()-155));
//         
// //         RunnerRepository.window.mainpanel.p5.setPreferredSize(new Dimension(getWidth()-50,672));
//         System.out.println("Runner applet resizing to: "+width+" - "+height);
//         validate();}
//     
//     /*
//      * applet stop method
//      */
//     public void stop(){
//         System.out.println("applet stopping");}
//         
//     /*
//      * applet destroy method
//      * removes the temp directory created
//      * by twister on startup
//      */
//     public void destroy(){
//         System.out.println("applet destroying");
//         RunnerRepository.saveMainLayout();
//         File file = new File(RunnerRepository.temp);
//         if(file.exists()){
//             if(Window.deleteTemp(file))
//                 System.out.println(RunnerRepository.temp+" deleted successfull");
//             else System.out.println("Could not delete: "+RunnerRepository.temp);}
//         System.exit(0);}
//         
//     /*
//      * applet start method
//      */
//     public void start(){
//         System.out.println("applet starting");}}
