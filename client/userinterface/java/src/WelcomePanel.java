/*
File: WelcomePanel.java ; This file is part of Twister.
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
import javax.swing.JPanel;
import javax.swing.BoxLayout;
import javax.swing.JLabel;
import java.awt.BorderLayout;
import javax.swing.JTextField;
import javax.swing.JPasswordField;
import javax.swing.JButton;
import java.awt.Dimension;
import javax.swing.Box;
import java.awt.Graphics;
import java.awt.GridBagLayout;
import java.awt.GridBagConstraints;
import java.awt.Color;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.awt.event.KeyEvent;
import java.awt.event.KeyAdapter;


public class WelcomePanel extends JPanel{
    private JPasswordField tf2;
    private JTextField tf1;
    private JButton login;
    
    public WelcomePanel(){
        JPanel p = new JPanel();
        tf1 = new JTextField();
        tf2 = new JPasswordField();
        tf2.addKeyListener(new KeyAdapter(){
            public void keyReleased(KeyEvent ev){
                if(ev.getKeyCode()==KeyEvent.VK_ENTER){
                    login.doClick();
                }
            }
        });
        p.setLayout(new BoxLayout(p, BoxLayout.Y_AXIS));
        JPanel jPanel1 = new JPanel();
        JLabel jLabel3 = new JLabel();
        JPanel jPanel2 = new JPanel();
        JLabel jLabel4 = new JLabel();
        jPanel1.setLayout(new BorderLayout());
        jLabel3.setText("User: ");
        jPanel1.add(jLabel3, BorderLayout.CENTER);
        p.add(jPanel1);
        p.add(tf1);
        jPanel2.setLayout(new BorderLayout());
        jLabel4.setText("Password: ");
        jPanel2.add(jLabel4, BorderLayout.CENTER);
        p.add(jPanel2);
        p.add(tf2);
        login = new JButton("Login");
        login.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                MainRepository.login(tf1.getText(),new String(tf2.getPassword()));
            }
        });
        p.add(Box.createRigidArea(new Dimension(0,5)));
        p.add(login);
        p.setBounds(210, 120, 200, 110);
        setLayout(null);
        add(p);
        setPreferredSize(new Dimension(420,280));
        setMaximumSize(new Dimension(420,280));
        setMinimumSize(new Dimension(420,280));
    }
    
    public void paint(Graphics g){
        super.paint(g);
        g.drawImage(MainRepository.background, 10, 10, null);
    }
}