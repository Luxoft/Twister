/*
File: About.java ; This file is part of Twister.
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
import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.Color;
import java.awt.Graphics;
import java.awt.Font;

public class About extends JPanel{
    public About(){
        setLayout(new BorderLayout());
        JPanel p = new JPanel(){
            public void paint(Graphics g){
                g.drawImage(RunnerRepository.background, 0, 0, null);
                g.setFont(new Font("TimesRoman", Font.BOLD, 14));
                g.drawString("Twister Framework", 225, 130);
                g.drawString("V.: "+RunnerRepository.getVersion(), 265, 165);
                g.drawString("Build date: "+RunnerRepository.getBuildDate(), 218, 180);
            }
        };
        p.setBackground(Color.RED);
        p.setSize(new Dimension(400,300));
        p.setPreferredSize(new Dimension(400,300));
        p.setMinimumSize(new Dimension(400,300));
        p.setMaximumSize(new Dimension(400,300));
        add(p,BorderLayout.CENTER );
    }
}