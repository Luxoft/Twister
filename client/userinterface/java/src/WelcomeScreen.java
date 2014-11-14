/*
File: WelcomeScreen.java ; This file is part of Twister.
Version: 2.004

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
import javax.swing.JPanel;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.awt.Graphics;
import java.awt.Font;
import java.awt.Dimension;
import java.awt.Toolkit;
import java.awt.KeyboardFocusManager;
import java.awt.KeyEventDispatcher;
import java.awt.event.KeyEvent;
import javax.swing.JTextArea;
import java.awt.event.AWTEventListener;
import java.awt.AWTEvent;
import javax.swing.JLabel;

public class WelcomeScreen extends JPanel{
    private AWTEventListener ked;
    private JTextArea tf,tf2;
    
    public WelcomeScreen(){
        setPreferredSize(new Dimension(700,380));
        setFocusable(true);
        ked = new AWTEventListener(){
                public void eventDispatched(AWTEvent e){
                    MainRepository.continueLogin();
                    MainRepository.countdown = true;
                    Toolkit.getDefaultToolkit().removeAWTEventListener(ked);
                }
            };
        Toolkit.getDefaultToolkit().addAWTEventListener(ked
            , AWTEvent.KEY_EVENT_MASK);
        setLayout(null);
        tf = new JTextArea();
        tf.setBackground(getBackground());
        tf.setFont(new Font("TimesRoman", Font.BOLD, 14));
        tf.setBounds(15,130,230,120);
        tf.setEditable(false);
        tf.setBorder(null);
        tf.setText(MainRepository.logotxt);
        tf2 = new JTextArea();
        tf2.setBackground(getBackground());
        tf2.setFont(new Font("TimesRoman", Font.BOLD, 14));
        tf2.setBounds(480,130,230,120);
        tf2.setEditable(false);
        tf2.setBorder(null);
        tf2.setText("   Twister Framework \n\n             V.: "+MainRepository.getVersion()+" \n Build date: "+MainRepository.getBuildDate());
        add(tf);
        add(tf2);
    }
    
    public void paint(Graphics g){
        super.paint(g);
        g.drawImage(MainRepository.background, 260, 20, null);
        g.drawImage(MainRepository.logo, 15, 20, null);
        g.setFont(new Font("TimesRoman", Font.BOLD, 14));
        g.drawString("Press any Key to Logon", 275, 350);
        requestFocus();
    }
}