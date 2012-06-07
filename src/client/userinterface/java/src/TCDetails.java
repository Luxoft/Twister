/*
   File: TCDetails.java ; This file is part of Twister.

   Copyright (C) 2012 , Luxoft

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
import java.awt.Font;
import java.awt.Color;
import java.awt.BorderLayout;
import java.awt.Dimension;
import javax.swing.JLabel;
import javax.swing.BorderFactory;

public class TCDetails extends JPanel{
    JTextArea text = new JTextArea("This is a sample text for helping on screen allignament");
    JLabel title = new JLabel("This is the title");
    
    public TCDetails(){
        setBorder(BorderFactory.createEmptyBorder(15, 10, 5, 10));
        setPreferredSize(new Dimension(450,100));
        setMinimumSize(new Dimension(0,0));
        setMaximumSize(new Dimension(1000,1000));
        setLayout(new BorderLayout());
        text.setWrapStyleWord(true);
        text.setLineWrap(true);
        text.setEditable(false);        
        text.setCursor(null);  
        text.setOpaque(false);  
        text.setFocusable(false);         
        text.setFont(new Font("Arial",Font.PLAIN,12));
        setBackground(Color.WHITE); 
        text.setBackground(Color.WHITE);       
        JPanel p1 = new JPanel();
        p1.setBackground(Color.WHITE); 
        p1.setLayout(new BorderLayout());
        p1.add(new JLabel("Title:  "),BorderLayout.WEST);
        title.setFont(new Font("Arial",Font.PLAIN,12));
        p1.add(title,BorderLayout.CENTER);        
        JPanel p2 = new JPanel();
        p2.setBackground(Color.WHITE); 
        p2.setLayout(new BorderLayout());
        p2.add(new JLabel("Description:  "),BorderLayout.NORTH);
        p2.add(text,BorderLayout.CENTER);        
        add(p1,BorderLayout.NORTH);
        add(p2,BorderLayout.CENTER);}}
