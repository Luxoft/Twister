/*
File: About.java ; This file is part of Twister.
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
import javax.swing.JTextArea;
import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.Color;
import java.awt.Graphics;
import java.awt.Font;
import javax.swing.BorderFactory;

public class About extends JPanel{
    private JTextArea ta;
    
    public About(){
        setLayout(new BorderLayout());
        //setBackground(Color.WHITE);
        setBorder(BorderFactory.createTitledBorder("About"));
        JPanel p1 = new JPanel();
        p1.setBackground(Color.WHITE);
        //p1.setLayout(new FlowLayout());
        JPanel p = new JPanel(){
            public void paintComponent(Graphics g){
                super.paintComponent(g);
                g.drawImage(RunnerRepository.background, 260, 10, null);
                g.drawImage(RunnerRepository.logo, 5, 10, null);
//                 g.setFont(new Font("TimesRoman", Font.BOLD, 14));
//                 g.drawString("Twister Framework", 485, 130);
//                 g.drawString("V.: "+RunnerRepository.getVersion(), 525, 165);
//                 g.drawString("Build date: "+RunnerRepository.getBuildDate(), 478, 180);
//                 g.drawString(RunnerRepository.os, 478, 195);
//                 g.drawString(RunnerRepository.python, 478, 210);
            }
        };
        p1.setBorder(BorderFactory.createLineBorder(Color.GRAY, 1));
        p.setLayout(null);
        p.setBackground(Color.WHITE);
        
        JTextArea ta2 = new JTextArea();
        ta2.setBackground(Color.WHITE);
        ta2.setBackground(p.getBackground());
        ta2.setFont(new Font("TimesRoman", Font.BOLD, 14));
        ta2.setBounds(480,140,230,120);
        ta2.setEditable(false);
        ta2.setBorder(null);
        ta2.setText("   Twister Framework \n\n             V.: "+RunnerRepository.getVersion()+" \nBuild date: "+RunnerRepository.getBuildDate()+
                    "\n"+RunnerRepository.os+"\n"+RunnerRepository.python);
        p.add(ta2);
        
        
        ta = new JTextArea();
        ta.setBackground(p.getBackground());
        ta.setFont(new Font("TimesRoman", Font.BOLD, 14));
        ta.setBounds(5,140,230,120);
        ta.setEditable(false);
        ta.setBorder(null);
        ta.setText(RunnerRepository.logotxt);
        p.add(ta);
        p.setSize(new Dimension(730,380));
        p.setPreferredSize(new Dimension(730,380));
        p.setMinimumSize(new Dimension(730,380));
        p.setMaximumSize(new Dimension(730,380));
        p1.add(p);
        add(p1,BorderLayout.CENTER);
    }
}