/*
File: WelcomeScreen.java ; This file is part of Twister.
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

public class WelcomeScreen extends JPanel{
    private KeyEventDispatcher ked;
    private JTextArea tf;
    
    public WelcomeScreen(){
        Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
        setBounds((int)(screenSize.getWidth()-700)/2,(int)(screenSize.getHeight()-380)/2,700,380);
        //setAlwaysOnTop(true);
        setFocusable(true);
        ked = new KeyEventDispatcher() {
            @Override
            public boolean dispatchKeyEvent(KeyEvent e) {
                MainRepository.continueLogin();
                MainRepository.countdown = true;
                KeyboardFocusManager.getCurrentKeyboardFocusManager().removeKeyEventDispatcher(ked);
                return false;
            }
        };
        setLayout(null);
        tf = new JTextArea();
        tf.setBackground(getBackground());
        tf.setFont(new Font("TimesRoman", Font.BOLD, 14));
        tf.setBounds(15,120,230,120);
        tf.setEditable(false);
        tf.setBorder(null);
        tf.setText(MainRepository.logotxt);
        add(tf);
        
//         component.getInputMap().put(KeyStroke.getKeyStroke("F2"),
//                                     "login");
//         component.getActionMap().put("login",
//                                      login);
        
//         addKeyListener(new KeyAdapter(){
//             public void keyReleased(KeyEvent ev){
//                 MainRepository.continueLogin();
//                 //WelcomeScreen.this.dispose();
//                 MainRepository.countdown = true;
//             }
//         });

        KeyboardFocusManager.getCurrentKeyboardFocusManager()
          .addKeyEventDispatcher(ked);

        //setVisible(true);
        //requestFocusInWindow();
        //requestFocus(true);
    }
    
//     Action login = new AbstractAction() {
//         public void actionPerformed(ActionEvent e) {
//             MainRepository.continueLogin();
//             //WelcomeScreen.this.dispose();
//             MainRepository.countdown = true;
//         }
//     };
    
    public void paint(Graphics g){
        super.paint(g);
        g.drawImage(MainRepository.background, 260, 20, null);
        g.drawImage(MainRepository.logo, 15, 20, null);
        g.setFont(new Font("TimesRoman", Font.BOLD, 14));
        g.drawString("Twister Framework", 490, 130);
        g.drawString("V.: "+MainRepository.getVersion(), 530, 165);
        g.drawString("Build date: "+MainRepository.getBuildDate(), 483, 180);
        g.drawString("Press any Key to Logon", 275, 350);
    }
}