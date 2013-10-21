/*
File: IntroScreen.java ; This file is part of Twister.
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
import javax.swing.JFrame;
import java.awt.Dimension;
import java.awt.Toolkit;
import com.sun.awt.AWTUtilities;
import java.awt.Graphics;
import java.awt.Color;
import java.io.InputStream;
import javax.swing.ImageIcon;
import java.awt.Image;
import javax.imageio.ImageIO;
import java.awt.Font;
import java.awt.Graphics2D;
import java.awt.AlphaComposite;
import java.awt.Frame;
import javax.swing.JPanel;

/*
 * intro screen with Twister logo
 * and loading status bar
 */
public class IntroScreen extends JPanel{
    private String text = ""; //text used to display initialization status on loading bar
//     int width;
    private double percent = 0; //percent of status bar set by initialization methods
    /*
     * intro screen initialization
     */
    public IntroScreen(){
//         Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
        //setBounds((int)(screenSize.getWidth()-640)/2,(int)(screenSize.getHeight()-480)/2,640,480);
        
        setMinimumSize(new Dimension(640,480));
        setMaximumSize(new Dimension(640,480));
        setPreferredSize(new Dimension(640,480));
        setSize(new Dimension(640,480));
//         setUndecorated(true);
//         setAlwaysOnTop(true);
//         try{if(AWTUtilities.isTranslucencySupported(AWTUtilities.Translucency.PERPIXEL_TRANSLUCENT))
//                 AWTUtilities.setWindowOpaque(this, false);
//             else if(AWTUtilities.isTranslucencySupported(AWTUtilities.Translucency.TRANSLUCENT))
//                 AWTUtilities.setWindowOpacity(this, 0.7f);}
//         catch(Exception e){e.printStackTrace();}
    }    
    
    public void paint(Graphics g){
        //Graphics2D g2d = (Graphics2D)g;
        //g2d.setComposite(AlphaComposite.Clear);
        g.setColor(getParent().getBackground());
        g.fillRect(0, 0, 640, 480);
        //g2d.setComposite(AlphaComposite.SrcOver);
        g.setColor(Color.GRAY);
        g.fillRoundRect(10, 350, (int)(620*percent), 30, 15, 15);
        g.setColor(Color.BLACK);
        g.drawRoundRect(10, 350, 620, 30, 15, 15);
        g.setFont(new Font("TimesRoman", 0, 14));
        g.drawString(text, 30, 374);
        g.drawImage(RunnerRepository.background, 55, 10, null);
    }
    
    /*
     * text - the text to display on loading
     * bar
     */   
    public void setStatus(String text){
        this.text = text;
    }
        
    /*
     * add percent to ilustrate
     * on loading bar
     */
    public void addPercent(double percent){
        this.percent+=percent;
    }
}