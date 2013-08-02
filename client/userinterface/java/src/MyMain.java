/*
File: MyMain.java ; This file is part of Twister.
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
import javax.swing.JFrame;
import java.io.InputStream;
import javax.swing.ImageIcon;
import javax.imageio.ImageIO;
import java.awt.Graphics;

public class MyMain{
    private static String bar = System.getProperty("file.separator");//System specific file.separator
    
    public static void main(String [] args){
        JFrame frame = new JFrame();
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setBounds(100,100,800,600);
        frame.setVisible(true);
        frame.setLayout(null);
        loadResourcesFromLocal();
        MainRepository.initialize(null,"tsc-server",frame.getContentPane());
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
