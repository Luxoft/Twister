/*
File: applet.java ; This file is part of Twister.
Version: 2.002

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
import java.applet.Applet; 
import java.awt.Color;
import java.net.URL;
import com.twister.MySecurityManager;
import java.awt.Image;
import java.io.InputStream;
import javax.swing.ImageIcon;
import javax.imageio.ImageIO;
import java.io.BufferedReader;
import java.io.InputStreamReader;

public class applet extends Applet{ 
    private static final long serialVersionUID = 1L;
    
    //applet initialization
    public void init(){
        System.setSecurityManager(new MySecurityManager());
        setLayout(null);
//         try{
//             getAppletContext().showDocument(new URL("javascript:resize()"));
//         } catch (Exception e) {
//             System.err.println("Failed to call JavaScript function appletLoaded()");
//         }
        MainRepository.background = loadIcon("background.png");
        try {
            URL url = new URL(this.getCodeBase()+"/logo.png");
            MainRepository.logo = ImageIO.read(url).getScaledInstance(230, 100, Image.SCALE_FAST);
        } catch (Exception e) {
            e.printStackTrace();
        }
        
        readLogoTxt();
        MainRepository.initialize(this,getCodeBase().getHost(),this);
    }
    
    public void readLogoTxt(){
        try{
            URL logo = new URL(this.getCodeBase()+"/logo.txt");
            BufferedReader in = new BufferedReader(
            new InputStreamReader(logo.openStream()));
            
            StringBuilder sb = new StringBuilder();
            String inputLine;
            while ((inputLine = in.readLine()) != null){
                sb.append(inputLine);
                sb.append("\n");
            }
            in.close();
            MainRepository.logotxt = sb.toString();
        } catch(Exception e){
            e.printStackTrace();
        }
    }
    
    /*
     * the general method to load icons from jar
     */
    public Image loadIcon(String icon){
        Image image = null;
        try{System.out.println("Getting "+icon+" from applet jar...");
            InputStream in = getClass().getResourceAsStream("Icons"+"/"+icon);
            System.out.println("Saving "+icon+" in memory.....");
            image = new ImageIcon(ImageIO.read(in)).getImage();
            if(image !=null)System.out.println(icon+" succsesfully loaded.");
            else System.out.println(icon+" not loaded.");
        }
        catch(Exception e){
            System.out.println("There was a problem in loading "+icon+
                " on "+image.toString());
            e.printStackTrace();}
        return image;}
    
    /*
     * set size method for applet
     * called by javascript when browser resizes
     */
    public void setSize(int width, int height){
        super.setSize(width,height);
//         System.out.println("applet resizing to: "+width+" - "+height);
//         validate();
//         MainRepository.resize(width,height);
    }
    
    public void resize(int width, int height){
        System.out.println("applet resizing : "+width+" - "+height);
        validate();
        MainRepository.resize(width,height);
    }
    
    /*
     * applet stop method
     */
    public void stop(){
        System.out.println("applet stopping");}
        

    public void destroy(){
        System.exit(0);}
        
    /*
     * applet start method
     */
    public void start(){
        System.out.println("applet starting");}}
