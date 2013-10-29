/*
File: MyMain.java ; This file is part of Twister.
Version: 2.003

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
import javax.swing.JFrame;
import java.io.InputStream;
import javax.swing.ImageIcon;
import javax.imageio.ImageIO;
import java.awt.Graphics;
import java.net.URL;
import java.awt.Image;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import javax.imageio.IIOException;
import java.io.FileNotFoundException;

public class MyMain{
    private static String bar = System.getProperty("file.separator");//System specific file.separator
    
    public static void main(String [] args){
        JFrame frame = new JFrame();
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setBounds(100,100,800,600);
        frame.setVisible(true);
        frame.setLayout(null);
        loadResourcesFromLocal();
        URL url = null;
        try {
            url = new URL("http://tsc-server/twister_gui/logo.png");
            MainRepository.logo = ImageIO.read(url).getScaledInstance(230, 100, Image.SCALE_FAST);
        } catch (IIOException e) {
            System.out.println("Could not get image: "+url.toExternalForm());
        } catch (Exception e){
            e.printStackTrace();
        }
        readLogoTxt();
        MainRepository.initialize(null,"tsc-server",frame.getContentPane());
    }
    
    public static void readLogoTxt(){
        URL logo = null;
        try{
            logo = new URL("http://tsc-server/twister_gui/logo.txt");
            BufferedReader in = new BufferedReader(new InputStreamReader(logo.openStream()));
            
            StringBuilder sb = new StringBuilder();
            String inputLine;
            while ((inputLine = in.readLine()) != null){
                sb.append(inputLine);
                sb.append("\n");
            }
            in.close();
            MainRepository.logotxt = sb.toString();
        }catch(FileNotFoundException e){
            System.out.println("Could not get file: "+logo.toExternalForm());
        } catch(Exception e){
            e.printStackTrace();
        }
    }
    
    /*
     * load resources needed for framework
     * from local pc
     */
    public static void loadResourcesFromLocal(){
        try{
            InputStream in;
            in = MainRepository.class.getResourceAsStream("Icons"+bar+"background.png"); 
            MainRepository.background = new ImageIcon(ImageIO.read(in)).getImage();
        } catch (Exception e){
            e.printStackTrace();
        }
    }
}
